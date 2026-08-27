#!/usr/bin/env python3
import importlib.util
import multiprocessing
import os
import re
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


def load_windows_shaped_module(fake_msvcrt):
    """Load a fresh transaction module as if running natively on Windows.

    Patches ``sys.platform`` to ``win32`` and hides the real ``fcntl``
    module (raising ``ImportError`` for it, exactly as a real Windows host
    would) for the duration of the exec, so the module's own platform
    branch is what determines which lock/fsync path gets wired up, not an
    accident of running on a POSIX CI runner.
    """
    spec = importlib.util.spec_from_file_location("glue_transaction_win32", TRANSACTION_SOURCE)
    module = importlib.util.module_from_spec(spec)
    with patch.object(sys, "platform", "win32"), \
         patch.dict(sys.modules, {"fcntl": None, "msvcrt": fake_msvcrt}):
        spec.loader.exec_module(module)
    return module


def hold_lock(destination: str, ready, release):
    with transaction.DestinationLock(Path(destination)):
        ready.set()
        release.wait(10)


def die_after_old_move(candidate: str, destination: str):
    transaction.replace_directory_transactional(
        Path(candidate), Path(destination), after_old_move=lambda: os._exit(73)
    )


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
        call_sites = re.findall(r"(?<!def )_fsync_directory\(", source)
        self.assertEqual(
            len(call_sites), 6,
            "call-site count changed; review the new site's cross-platform behavior "
            "and update this pin deliberately, do not just bump the number",
        )
        self.assertNotRegex(
            source,
            r"(?m)^import (fcntl|termios|grp|pwd|resource|posix|pty|syslog|curses|tty|crypt)\b",
            "a bare unix-only stdlib import reappeared at module scope; it must live inside "
            "the sys.platform branch, matching the fcntl/msvcrt split",
        )
        self.assertIn('_IS_WINDOWS = sys.platform == "win32"', source)
        open_sites = re.findall(r"os\.open\(", source)
        self.assertEqual(
            len(open_sites), 1,
            "a new bare os.open( call site appeared; a hand-rolled directory-fsync "
            "(or any other raw os.open) bypasses this census and the _IS_WINDOWS "
            "branch entirely, since os is imported unconditionally on both platforms "
            "and adds no _fsync_directory( token. Route any new directory-durability "
            "need through _fsync_directory itself instead of a fresh os.open call.",
        )


if __name__ == "__main__":
    print("ARMED: transactional replacement crash, lock, rerun-source, census, and windows-shape checks")
    unittest.main(verbosity=2)
