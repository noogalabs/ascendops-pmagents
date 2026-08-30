"""Crash-recoverable directory replacement primitives for the Betty glue wrapper."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from contextlib import nullcontext
from pathlib import Path
from typing import Callable, NamedTuple

_IS_WINDOWS = sys.platform == "win32"

if _IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    import msvcrt

    _MOVEFILE_REPLACE_EXISTING = 0x1
    _MOVEFILE_WRITE_THROUGH = 0x8

    _MoveFileExW = ctypes.windll.kernel32.MoveFileExW
    _MoveFileExW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD]
    _MoveFileExW.restype = wintypes.BOOL
else:
    import fcntl


class TransactionError(RuntimeError):
    """The destination could not be committed or recovered safely."""


class ConcurrentTransactionError(TransactionError):
    """Another process owns the destination transaction."""


class DistinctSourceOutputError(TransactionError):
    """A rerun tried to preserve state from somewhere other than its destination."""


class TransactionResult(NamedTuple):
    committed: bool
    recovered: bool = False
    cleanup_warning: str | None = None


def _sidecar(destination: Path, suffix: str) -> Path:
    return destination.parent / f".{destination.name}.{suffix}"


def _fsync_directory(path: Path) -> None:
    """Durably record a directory-entry change (e.g. after ``_durable_replace``).

    Windows has no CRT-level directory-handle fsync (``os.open`` on a
    directory raises ``OSError`` there), so this remains an explicit,
    DECLARED no-op on that platform, not a silent one. That is no longer a
    weaker guarantee, though: on POSIX, durability for a completed rename
    comes from fsyncing the parent directory's entry right after (this
    function); on Windows it comes from ``_durable_replace`` itself, which
    every rename in this module now goes through instead of a bare
    ``os.replace`` - see its docstring. What stays equally strong on both
    platforms regardless: every journal write in this module fsyncs its own
    regular file handle first (see ``_write_journal`` and
    ``DestinationLock.__enter__``), which this no-op does not touch.
    """
    if _IS_WINDOWS:
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _durable_replace(src: Path, dst: Path) -> None:
    """Atomically replace ``dst`` with ``src``, durable against a crash on
    both platforms, through the one chokepoint every rename in this module
    goes through.

    POSIX: ``os.replace`` is already atomic; the caller's follow-up
    ``_fsync_directory`` on the parent is what makes the completed rename
    durable across a crash or power loss.

    Windows has no directory-fsync equivalent, so durability has to come
    from the rename call itself: ``MoveFileExW`` with
    ``MOVEFILE_WRITE_THROUGH`` does not return until the replace is flushed
    to stable storage, closing the same crash window ``_fsync_directory``
    closes on POSIX. ``MOVEFILE_REPLACE_EXISTING`` matches ``os.replace``'s
    semantics of silently replacing an existing destination.
    """
    if _IS_WINDOWS:
        flags = _MOVEFILE_REPLACE_EXISTING | _MOVEFILE_WRITE_THROUGH
        if not _MoveFileExW(str(src), str(dst), flags):
            raise OSError(ctypes.get_last_error(), f"MoveFileExW failed replacing {dst} with {src}")
    else:
        os.replace(src, dst)


def _lock_exclusive_nonblocking(handle) -> None:
    """Acquire a non-blocking exclusive lock; raise ``BlockingIOError`` on contention.

    ``fcntl.flock`` and ``msvcrt.locking`` give the same operational
    guarantee ``DestinationLock`` depends on: the lock is kernel-owned and
    releases automatically the instant the holding process dies or its
    handle closes, so a crashed configurator never leaves a stale lock
    behind. Any failure other than contention propagates unchanged; this
    never silently degrades to an unlocked state.
    """
    if _IS_WINDOWS:
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise BlockingIOError(exc.errno, exc.strerror) from exc
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _unlock(handle) -> None:
    if _IS_WINDOWS:
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class DestinationLock:
    """A non-blocking lock whose kernel ownership disappears when its process dies."""

    def __init__(self, destination: Path):
        self.destination = destination.resolve(strict=False)
        self.path = _sidecar(self.destination, "glue.lock")
        self._handle = None

    def __enter__(self):
        self.destination.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("a+", encoding="utf-8")
        try:
            _lock_exclusive_nonblocking(self._handle)
        except BlockingIOError as exc:
            self._handle.close()
            self._handle = None
            raise ConcurrentTransactionError(
                f"destination is already being configured: {self.destination}"
            ) from exc
        self._handle.seek(0)
        self._handle.truncate()
        self._handle.write(json.dumps({"pid": os.getpid(), "destination": str(self.destination)}) + "\n")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self._handle is not None:
            _unlock(self._handle)
            self._handle.close()
            self._handle = None


def require_existing_output_as_source(source: Path, output: Path) -> None:
    """Fail before staging if a rerun would copy accumulated state from the wrong tree."""
    if not output.exists():
        return
    try:
        same = source.samefile(output)
    except (FileNotFoundError, OSError):
        same = source.resolve(strict=False) == output.resolve(strict=False)
    if not same:
        raise DistinctSourceOutputError(
            "existing-output rerun requires source_agent_dir and output_dir to name "
            "the same directory; refusing to clobber accumulated state"
        )


_DAILY_LOG = re.compile(r"^\d{4}-\d{2}-\d{2}(?:\.[^.]+)?$")


def protected_class_census(agent_dir: Path) -> dict[str, list[str]]:
    """Enumerate the top-level state classes a rerun must preserve byte-for-byte."""
    result = {"memory": [], "tasks": [], "environment": [], "daily_logs": []}
    if not agent_dir.is_dir():
        return result
    for child in sorted(agent_dir.iterdir(), key=lambda path: path.name):
        if child.name == "memory":
            result["memory"].append(child.name)
            if child.is_dir():
                result["daily_logs"].extend(
                    str(path.relative_to(agent_dir))
                    for path in sorted(child.iterdir())
                    if path.is_file() and _DAILY_LOG.match(path.name)
                )
        elif child.name == "tasks":
            result["tasks"].append(child.name)
        elif child.name == ".env" or child.name.startswith(".env."):
            result["environment"].append(child.name)
        elif child.name in {"logs", "daily-logs"}:
            result["daily_logs"].append(child.name)
        elif child.is_file() and _DAILY_LOG.match(child.name):
            result["daily_logs"].append(child.name)
    for paths in result.values():
        paths.sort()
    return result


def _write_journal(path: Path, payload: dict[str, str]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    _durable_replace(temporary, path)
    _fsync_directory(path.parent)


def _read_journal(path: Path, destination: Path) -> dict[str, str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TransactionError(f"transaction journal is unreadable: {path}") from exc
    expected = destination.resolve(strict=False)
    if Path(payload.get("destination", "")).resolve(strict=False) != expected:
        raise TransactionError(f"transaction journal destination mismatch: {path}")
    if payload.get("phase") not in {"prepared", "old_moved", "new_installed"}:
        raise TransactionError(f"transaction journal phase is invalid: {path}")
    return payload


def _remove_journal(path: Path) -> None:
    path.unlink(missing_ok=True)
    path.with_suffix(path.suffix + ".tmp").unlink(missing_ok=True)
    _fsync_directory(path.parent)


def recover_directory_transaction(destination: Path) -> TransactionResult:
    """Recover a transaction while the caller holds ``DestinationLock``."""
    destination = destination.resolve(strict=False)
    journal = _sidecar(destination, "glue-transaction.json")
    if not journal.exists():
        return TransactionResult(committed=False, recovered=False)
    payload = _read_journal(journal, destination)
    backup = Path(payload["backup"])
    candidate = Path(payload["candidate"])
    for path, label in ((backup, "backup"), (candidate, "candidate")):
        if path.parent.resolve(strict=False) != destination.parent.resolve(strict=False):
            raise TransactionError(f"transaction {label} escaped destination parent")

    if destination.exists():
        # The new tree is visible. Finish the commit even if death preceded phase update.
        warning = None
        if backup.exists():
            try:
                shutil.rmtree(backup)
            except OSError as exc:
                warning = f"committed; old-tree cleanup remains pending: {exc}"
        if warning is None:
            _remove_journal(journal)
        return TransactionResult(committed=True, recovered=True, cleanup_warning=warning)

    if backup.exists():
        _durable_replace(backup, destination)
        _fsync_directory(destination.parent)
        _remove_journal(journal)
        return TransactionResult(committed=False, recovered=True)

    if payload["phase"] in {"prepared", "old_moved"} and candidate.exists():
        # A first install has no backup. Its canonical destination was absent before
        # the crash, so abandoning the uncommitted candidate preserves that state.
        _remove_journal(journal)
        return TransactionResult(committed=False, recovered=True)
    raise TransactionError("transaction has neither a live destination nor a recoverable backup")


def replace_directory_transactional(
    candidate: Path,
    destination: Path,
    *,
    after_old_move: Callable[[], None] | None = None,
    already_locked: bool = False,
) -> TransactionResult:
    """Install a complete candidate with locking, journaling, and next-run recovery."""
    candidate = candidate.resolve(strict=True)
    destination = destination.resolve(strict=False)
    if not candidate.is_dir():
        raise TransactionError(f"candidate is not a directory: {candidate}")
    if candidate.parent != destination.parent:
        raise TransactionError("candidate and destination must share a filesystem parent")
    backup = _sidecar(destination, f"glue-previous-{os.getpid()}")
    journal = _sidecar(destination, "glue-transaction.json")

    with (nullcontext() if already_locked else DestinationLock(destination)):
        recovery = recover_directory_transaction(destination)
        if recovery.cleanup_warning:
            return recovery
        if backup.exists():
            raise TransactionError(f"transaction backup already exists: {backup}")
        payload = {
            "destination": str(destination),
            "candidate": str(candidate),
            "backup": str(backup),
            "phase": "prepared",
        }
        _write_journal(journal, payload)
        if destination.exists():
            _durable_replace(destination, backup)
            _fsync_directory(destination.parent)
        payload["phase"] = "old_moved"
        _write_journal(journal, payload)
        if after_old_move is not None:
            after_old_move()
        try:
            _durable_replace(candidate, destination)
            _fsync_directory(destination.parent)
        except BaseException:
            if backup.exists() and not destination.exists():
                _durable_replace(backup, destination)
                _fsync_directory(destination.parent)
                _remove_journal(journal)
            raise
        payload["phase"] = "new_installed"
        _write_journal(journal, payload)
        warning = None
        if backup.exists():
            try:
                shutil.rmtree(backup)
            except OSError as exc:
                warning = f"committed; old-tree cleanup remains pending: {exc}"
        if warning is None:
            _remove_journal(journal)
        return TransactionResult(committed=True, cleanup_warning=warning)
