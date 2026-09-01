#!/usr/bin/env python3
import ast
import ctypes
import importlib.util
import multiprocessing
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


HERE = Path(__file__).resolve().parents[1]
TRANSACTION_SOURCE = HERE / "transaction.py"
SPEC = importlib.util.spec_from_file_location("glue_transaction", TRANSACTION_SOURCE)
transaction = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(transaction)


def load_windows_shaped_module(fake_msvcrt, fake_kernel32=None):
    """Load a fresh transaction module as if running natively on Windows.

    Patches ``sys.platform`` to ``win32`` and hides the real ``fcntl``
    module (raising ``ImportError`` for it, exactly as a real Windows host
    would) for the duration of the exec, so the module's own platform
    branch is what determines which lock/fsync path gets wired up, not an
    accident of running on a POSIX CI runner. ``ctypes.WinDLL`` only exists
    on a real Windows build of ctypes, so its constructor is patched in too
    (with ``create=True``, since the real attribute is absent on this CI
    host) to return ``fake_kernel32`` for the module's
    ``ctypes.WinDLL("kernel32", use_last_error=True)`` call to resolve. The
    constructor mock itself is stashed on the returned module (as
    ``_test_windll_ctor``) so a caller can assert it was invoked with
    ``use_last_error=True`` - the actual fix this shape exists to prove.
    """
    spec = importlib.util.spec_from_file_location("glue_transaction_win32", TRANSACTION_SOURCE)
    module = importlib.util.module_from_spec(spec)
    kernel32 = fake_kernel32 if fake_kernel32 is not None else MagicMock()
    fake_windll_ctor = MagicMock(return_value=kernel32)
    with patch.object(sys, "platform", "win32"), \
         patch.dict(sys.modules, {"fcntl": None, "msvcrt": fake_msvcrt}), \
         patch.object(ctypes, "WinDLL", fake_windll_ctor, create=True):
        spec.loader.exec_module(module)
    module._test_windll_ctor = fake_windll_ctor
    return module


def hold_lock(destination: str, ready, release):
    with transaction.DestinationLock(Path(destination)):
        ready.set()
        release.wait(10)


def die_after_old_move(candidate: str, destination: str):
    transaction.replace_directory_transactional(
        Path(candidate), Path(destination), after_old_move=lambda: os._exit(73)
    )


def _count_fsync_directory_call_sites(source: str) -> int:
    """Count real calls to _fsync_directory, both bare (`_fsync_directory(x)`)
    and attribute-qualified (`module._fsync_directory(x)`, `self._fsync_directory(x)`,
    any receiver expression) - the qualified shape is a real Call node whose
    func is an ast.Attribute, not an ast.Name, so it needs its own branch.
    The `def _fsync_directory(` definition itself is never an ast.Call, so it
    is excluded automatically without needing the retired regex's lookbehind.
    """
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "_fsync_directory":
            count += 1
        elif isinstance(func, ast.Attribute) and func.attr == "_fsync_directory":
            count += 1
    return count


def _count_os_open_call_sites(source: str) -> int:
    """Count real os.open( call sites in `source`, resolving three evasion
    shapes the retired substring regex `os\\.open\\(` incidentally caught:
    `import os as X` (rebinds the module name), `from os import open as Y`
    (binds the function name directly), and a nested attribute chain ending
    `.os.open` (e.g. `holder.os.open(...)`) - the retired regex matched that
    last shape as a plain literal substring regardless of what precedes
    `.os.open(`, so the AST census fails closed on it the same way: ANY
    attribute-call whose immediate receiver is itself an attribute access
    named "os" counts, regardless of what that receiver's own receiver is.
    Scanned file-wide via ast.walk, not scope-restricted, so a locally
    scoped alias import inside a function body is still caught.
    """
    tree = ast.parse(source)
    os_module_names = {"os"}
    os_open_direct_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "os":
                    os_module_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            for alias in node.names:
                if alias.name == "open":
                    os_open_direct_names.add(alias.asname or alias.name)

    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "open"):
            if isinstance(func, ast.Name) and func.id in os_open_direct_names:
                count += 1
            continue
        receiver = func.value
        if isinstance(receiver, ast.Name) and receiver.id in os_module_names:
            count += 1
        elif isinstance(receiver, ast.Attribute) and receiver.attr in os_module_names:
            count += 1
    return count


def _count_os_replace_call_sites(source: str) -> int:
    """Count real os.replace( call sites: alias/nested-receiver resolution
    (matching _count_os_open_call_sites) plus a direct-import-alias branch
    (`from os import replace as X`) that a first pass of this helper
    omitted - proven live by aussie: that shape stayed invisible even
    though it is a real bare rename bypassing the _durable_replace
    chokepoint. Every rename in this module must go through that single
    chokepoint (its own internal POSIX-branch call is the one legitimate
    site) rather than a bare os.replace scattered across the file, which
    is exactly the fragmentation _durable_replace exists to close.
    """
    tree = ast.parse(source)
    os_module_names = {"os"}
    os_replace_direct_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "os":
                    os_module_names.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            for alias in node.names:
                if alias.name == "replace":
                    os_replace_direct_names.add(alias.asname or alias.name)

    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "replace"):
            if isinstance(func, ast.Name) and func.id in os_replace_direct_names:
                count += 1
            continue
        receiver = func.value
        if isinstance(receiver, ast.Name) and receiver.id in os_module_names:
            count += 1
        elif isinstance(receiver, ast.Attribute) and receiver.attr in os_module_names:
            count += 1
    return count


BANNED_UNIX_MODULES = {
    "fcntl", "termios", "grp", "pwd", "resource",
    "posix", "pty", "syslog", "curses", "tty", "crypt",
}


def _bare_unix_module_imports(tree: ast.Module) -> list:
    """Module-scope `import X` and `from X import Y` statements whose
    TOP-LEVEL package is a unix-only stdlib module. Compares the top-level
    component (`name.split(".", 1)[0]`), not the full dotted name, so a
    submodule import like `import curses.ascii` (or `from curses.ascii
    import isprint`) is still caught even though its exact spelling never
    equals the banned root "curses".
    """
    hits = [
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name.split(".", 1)[0] in BANNED_UNIX_MODULES
    ]
    hits.extend(
        node.module
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        and node.module
        and node.module.split(".", 1)[0] in BANNED_UNIX_MODULES
    )
    return hits


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="glue-transaction-test-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def tree(self, name: str, value: str) -> Path:
        path = self.tmp / name
        path.mkdir()
        (path / "value").write_text(value, encoding="utf-8")
        return path

    def test_named_crash_after_old_move_recovers_old_tree_on_next_run(self):
        print("ARMED: killed after old rename => durable-journal recovery")
        destination = self.tree("agent", "old")
        candidate = self.tree("candidate", "new")
        process = multiprocessing.Process(
            target=die_after_old_move, args=(str(candidate), str(destination))
        )
        process.start()
        process.join(10)
        self.assertEqual(process.exitcode, 73)
        self.assertFalse(destination.exists())
        with transaction.DestinationLock(destination):
            result = transaction.recover_directory_transaction(destination)
        self.assertTrue(result.recovered)
        self.assertFalse(result.committed)
        self.assertEqual((destination / "value").read_text(), "old")

    def test_named_second_owner_fails_before_destination_write(self):
        print("ARMED: second owner rejected before destination writes")
        destination = self.tree("agent", "old")
        before = (destination / "value").read_bytes()
        ready = multiprocessing.Event()
        release = multiprocessing.Event()
        process = multiprocessing.Process(target=hold_lock, args=(str(destination), ready, release))
        process.start()
        self.assertTrue(ready.wait(5))
        try:
            with self.assertRaises(transaction.ConcurrentTransactionError):
                with transaction.DestinationLock(destination):
                    self.fail("second lock unexpectedly acquired")
            self.assertEqual((destination / "value").read_bytes(), before)
            self.assertFalse(transaction._sidecar(destination, "glue-transaction.json").exists())
        finally:
            release.set()
            process.join(10)
        self.assertEqual(process.exitcode, 0)

    def test_named_distinct_source_existing_output_fails_shut(self):
        print("ARMED: distinct rerun source cannot clobber accumulated output")
        source = self.tree("source", "template-state")
        output = self.tree("output", "accumulated-state")
        before = (output / "value").read_bytes()
        with self.assertRaises(transaction.DistinctSourceOutputError):
            transaction.require_existing_output_as_source(source, output)
        self.assertEqual((output / "value").read_bytes(), before)

    def test_named_cleanup_failure_is_committed_warning_not_false_failure(self):
        destination = self.tree("agent", "old")
        candidate = self.tree("candidate", "new")
        original = transaction.shutil.rmtree
        transaction.shutil.rmtree = lambda path: (_ for _ in ()).throw(OSError("planted"))
        try:
            result = transaction.replace_directory_transactional(candidate, destination)
        finally:
            transaction.shutil.rmtree = original
        self.assertTrue(result.committed)
        self.assertIn("cleanup remains pending", result.cleanup_warning)
        self.assertEqual((destination / "value").read_text(), "new")

    def test_named_durable_replace_atomically_replaces_on_posix(self):
        print("ARMED: _durable_replace must actually rename src onto dst's path on this platform")
        candidate = self.tree("candidate", "new")
        destination = self.tmp / "agent"
        transaction._durable_replace(candidate, destination)
        self.assertEqual((destination / "value").read_text(), "new")
        self.assertFalse(candidate.exists())

    def test_protected_class_census_includes_daily_log_surfaces(self):
        root = self.tmp / "agent"
        (root / "memory").mkdir(parents=True)
        (root / "memory" / "2026-08-24.md").write_text("daily")
        (root / "tasks").mkdir()
        (root / ".env.local").write_text("secret")
        (root / "logs").mkdir()
        census = transaction.protected_class_census(root)
        self.assertEqual(census["memory"], ["memory"])
        self.assertEqual(census["tasks"], ["tasks"])
        self.assertEqual(census["environment"], [".env.local"])
        self.assertEqual(census["daily_logs"], ["logs", "memory/2026-08-24.md"])


class WindowsPlatformShapeTests(unittest.TestCase):
    def test_named_windows_shaped_import_succeeds_without_real_fcntl_or_msvcrt(self):
        print("ARMED: fcntl-absent import crash and directory-fsync-on-windows crash both regressed here")
        module = load_windows_shaped_module(MagicMock())
        self.assertTrue(hasattr(module, "DestinationLock"))
        self.assertTrue(hasattr(module, "_fsync_directory"))
        self.assertTrue(hasattr(module, "_durable_replace"))

    def test_named_windows_durable_replace_uses_movefileexw_write_through(self):
        print("ARMED: windows rename must call MoveFileExW with REPLACE_EXISTING|WRITE_THROUGH, never a bare rename")
        fake_kernel32 = MagicMock()
        fake_kernel32.MoveFileExW.return_value = 1
        module = load_windows_shaped_module(MagicMock(), fake_kernel32=fake_kernel32)
        src, dst = Path("C:/src"), Path("C:/dst")
        module._durable_replace(src, dst)
        fake_kernel32.MoveFileExW.assert_called_once_with(
            str(src), str(dst), module._MOVEFILE_REPLACE_EXISTING | module._MOVEFILE_WRITE_THROUGH
        )

    def test_named_windows_durable_replace_arms_real_last_error_capture(self):
        print("ARMED: MoveFileExW must be bound via a WinDLL loaded with use_last_error=True, "
              "or a failure's OSError reads a stale/zero ctypes-private slot instead of the real Win32 error")
        module = load_windows_shaped_module(MagicMock())
        module._test_windll_ctor.assert_called_once_with("kernel32", use_last_error=True)

    def test_named_windows_durable_replace_raises_on_movefileexw_failure(self):
        print("ARMED: a MoveFileExW failure must raise, never be swallowed as a silent no-op rename")
        fake_kernel32 = MagicMock()
        fake_kernel32.MoveFileExW.return_value = 0
        module = load_windows_shaped_module(MagicMock(), fake_kernel32=fake_kernel32)
        # ctypes.get_last_error is itself a real-Windows-only function, patched
        # the same way ctypes.WinDLL is for the duration of this call.
        with patch.object(ctypes, "get_last_error", lambda: 5, create=True):
            with self.assertRaises(OSError):
                module._durable_replace(Path("C:/src"), Path("C:/dst"))

    def test_named_windows_branch_engages_lk_nblck_and_lock_failure_raises(self):
        print("ARMED: windows lock path must call LK_NBLCK and must raise on contention, never swallow")
        fake_msvcrt = MagicMock()
        fake_msvcrt.LK_NBLCK = "NBLCK-SENTINEL"
        fake_msvcrt.LK_UNLCK = "UNLCK-SENTINEL"
        module = load_windows_shaped_module(fake_msvcrt)
        fake_handle = MagicMock()
        fake_handle.fileno.return_value = 7

        module._lock_exclusive_nonblocking(fake_handle)
        fake_msvcrt.locking.assert_called_once_with(7, "NBLCK-SENTINEL", 1)
        fake_handle.seek.assert_called_with(0)

        fake_msvcrt.locking.side_effect = OSError(13, "Permission denied")
        with self.assertRaises(BlockingIOError):
            module._lock_exclusive_nonblocking(fake_handle)

        fake_msvcrt.reset_mock(side_effect=True)
        module._unlock(fake_handle)
        fake_msvcrt.locking.assert_called_once_with(7, "UNLCK-SENTINEL", 1)

    def test_named_windows_mocked_two_locker_contention_named_refusal(self):
        print("ARMED: windows-mocked second locker is rejected by name before any destination write")
        fake_msvcrt = MagicMock()
        fake_msvcrt.LK_NBLCK = 1
        fake_msvcrt.LK_UNLCK = 0
        acquire_attempts = {"count": 0}

        def locking_side_effect(fd, mode, length):
            if mode == fake_msvcrt.LK_UNLCK:
                return None
            acquire_attempts["count"] += 1
            if acquire_attempts["count"] == 1:
                return None
            raise OSError(13, "Permission denied")

        fake_msvcrt.locking.side_effect = locking_side_effect
        module = load_windows_shaped_module(fake_msvcrt)

        tmp = Path(tempfile.mkdtemp(prefix="glue-transaction-win32-test-"))
        try:
            destination = tmp / "agent"
            destination.mkdir()
            (destination / "value").write_text("before", encoding="utf-8")
            before = (destination / "value").read_bytes()

            first = module.DestinationLock(destination)
            first.__enter__()
            try:
                with self.assertRaises(module.ConcurrentTransactionError) as caught:
                    with module.DestinationLock(destination):
                        self.fail("second windows-mocked lock unexpectedly acquired")
                self.assertIn(str(destination), str(caught.exception))
                self.assertEqual((destination / "value").read_bytes(), before)
            finally:
                first.__exit__(None, None, None)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_named_transaction_posix_only_call_site_census_is_pinned(self):
        print("ARMED: a new _fsync_directory caller or bare posix-only import must update this census")
        source = TRANSACTION_SOURCE.read_text()
        tree = ast.parse(source, filename=str(TRANSACTION_SOURCE))

        fsync_directory_calls = _count_fsync_directory_call_sites(source)
        os_open_calls = _count_os_open_call_sites(source)
        os_replace_calls = _count_os_replace_call_sites(source)
        bare_unix_imports = _bare_unix_module_imports(tree)

        # AST Call/Import nodes only ever describe executable code, never comments
        # or string literals, so this census cannot be false-tripped by a comment
        # that merely mentions these tokens, and cannot be evaded by whitespace
        # variants like `os.open (path)` the way a text-regex census could.
        self.assertEqual(
            fsync_directory_calls, 7,
            "call-site count changed; review the new site's cross-platform behavior "
            "and update this pin deliberately, do not just bump the number",
        )
        self.assertEqual(
            bare_unix_imports, [],
            "a bare unix-only stdlib import reappeared at module scope; it must live inside "
            "the sys.platform branch, matching the fcntl/msvcrt split",
        )
        self.assertIn('_IS_WINDOWS = sys.platform == "win32"', source)
        self.assertEqual(
            os_open_calls, 1,
            "a new bare os.open( call site appeared; a hand-rolled directory-fsync "
            "(or any other raw os.open) bypasses this census and the _IS_WINDOWS "
            "branch entirely, since os is imported unconditionally on both platforms "
            "and adds no _fsync_directory( token. Route any new directory-durability "
            "need through _fsync_directory itself instead of a fresh os.open call.",
        )
        self.assertEqual(
            os_replace_calls, 1,
            "a new bare os.replace( call site appeared outside _durable_replace's own "
            "POSIX branch; every rename must go through _durable_replace so Windows gets "
            "the same crash-durability guarantee POSIX gets, not a mix of durable and "
            "non-durable renames",
        )

    def test_named_census_helpers_resolve_alias_and_dotted_import_evasions(self):
        print("ARMED: os.open alias shapes, dotted unix-import shapes, and qualified "
              "_fsync_directory calls must not evade the census helpers")
        bare_call_source = "def _fsync_directory(path):\n    pass\n\n\ndef f(path):\n    _fsync_directory(path)\n"
        qualified_call_source = (
            "def _fsync_directory(path):\n    pass\n\n\n"
            "def f(module, path):\n    module._fsync_directory(path)\n"
        )
        definition_only_source = "def _fsync_directory(path):\n    pass\n"

        self.assertEqual(_count_fsync_directory_call_sites(bare_call_source), 1)
        self.assertEqual(
            _count_fsync_directory_call_sites(qualified_call_source), 1,
            "`module._fsync_directory(path)` (Attribute-qualified) must still be counted "
            "as a real call site, the retired regex's own coverage this replaces did",
        )
        self.assertEqual(
            _count_fsync_directory_call_sites(definition_only_source), 0,
            "the `def _fsync_directory(` definition line itself is never a Call node "
            "and must not be counted",
        )

        literal_source = "import os\n\n\ndef f(path):\n    return os.open(path, 0)\n"
        module_alias_source = "import os as o\n\n\ndef f(path):\n    return o.open(path, 0)\n"
        from_import_alias_source = "from os import open as raw_open\n\n\ndef f(path):\n    return raw_open(path, 0)\n"
        unrelated_source = "import os\n\n\ndef f(path):\n    return len(path)\n"

        self.assertEqual(_count_os_open_call_sites(literal_source), 1)
        self.assertEqual(
            _count_os_open_call_sites(module_alias_source), 1,
            "`import os as o` then `o.open(...)` must still be counted as a real os.open call site",
        )
        self.assertEqual(
            _count_os_open_call_sites(from_import_alias_source), 1,
            "`from os import open as raw_open` then `raw_open(...)` must still be counted",
        )
        self.assertEqual(_count_os_open_call_sites(unrelated_source), 0)

        nested_receiver_source = (
            "class Holder:\n    import os\n\n\n"
            "def f(path):\n    holder = Holder()\n    return holder.os.open(path, 0)\n"
        )
        unrelated_nested_receiver_source = (
            "class Holder:\n    pass\n\n\n"
            "def f(holder, path):\n    return holder.zipfile.open(path)\n"
        )
        self.assertEqual(
            _count_os_open_call_sites(nested_receiver_source), 1,
            "`holder.os.open(...)` (nested attribute chain ending .os.open) must still be "
            "counted; the retired regex caught this as a plain `os.open(` substring match "
            "regardless of what precedes it",
        )
        self.assertEqual(
            _count_os_open_call_sites(unrelated_nested_receiver_source), 0,
            "an unrelated .something.open( chain that doesn't end in .os.open must not "
            "false-positive",
        )

        nested_aliased_receiver_source = (
            "class Holder:\n    import os as platform_os\n\n\n"
            "def f(path):\n    holder = Holder()\n    return holder.platform_os.open(path, 0)\n"
        )
        self.assertEqual(
            _count_os_open_call_sites(nested_aliased_receiver_source), 1,
            "`holder.platform_os.open(...)` must still be counted; the nested-receiver "
            "check must compare against the same os_module_names alias set the direct-"
            "receiver check uses, not a hardcoded literal 'os'",
        )

        replace_from_import_alias_source = (
            "from os import replace as raw_replace\n\n\ndef f(src, dst):\n    raw_replace(src, dst)\n"
        )
        replace_literal_source = "import os\n\n\ndef f(src, dst):\n    os.replace(src, dst)\n"
        self.assertEqual(
            _count_os_replace_call_sites(replace_from_import_alias_source), 1,
            "`from os import replace as raw_replace` then `raw_replace(...)` must still be "
            "counted; this shape stayed invisible in a first pass of the helper - a real "
            "bare rename that bypasses the _durable_replace chokepoint undetected",
        )
        self.assertEqual(_count_os_replace_call_sites(replace_literal_source), 1)

        dotted_submodule_source = "import curses.ascii\n"
        exact_root_source = "import curses\n"
        unrelated_import_source = "import json\n"
        from_import_dotted_source = "from curses.ascii import isprint\n"
        from_import_exact_source = "from fcntl import flock\n"
        from_import_unrelated_source = "from pathlib import Path\n"

        self.assertEqual(
            _bare_unix_module_imports(ast.parse(dotted_submodule_source)), ["curses.ascii"],
            "`import curses.ascii` must still be flagged as a banned-root unix import, "
            "not evade the check just because the dotted spelling isn't an exact match",
        )
        self.assertEqual(_bare_unix_module_imports(ast.parse(exact_root_source)), ["curses"])
        self.assertEqual(_bare_unix_module_imports(ast.parse(unrelated_import_source)), [])
        self.assertEqual(
            _bare_unix_module_imports(ast.parse(from_import_exact_source)), ["fcntl"],
            "`from fcntl import flock` must be flagged; the retired regex never covered "
            "from-import syntax at all, so this closes a pre-existing gap",
        )
        self.assertEqual(
            _bare_unix_module_imports(ast.parse(from_import_dotted_source)), ["curses.ascii"],
            "`from curses.ascii import isprint` must be flagged by its top-level component",
        )
        self.assertEqual(_bare_unix_module_imports(ast.parse(from_import_unrelated_source)), [])


if __name__ == "__main__":
    print("ARMED: transactional replacement crash, lock, rerun-source, census, and windows-shape checks")
    unittest.main(verbosity=2)
