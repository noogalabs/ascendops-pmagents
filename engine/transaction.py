"""Crash-recoverable directory replacement primitives for the Betty glue wrapper."""
from __future__ import annotations

import fcntl
import json
import os
import re
import shutil
from contextlib import nullcontext
from pathlib import Path
from typing import Callable, NamedTuple


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
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


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
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
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
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
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
    os.replace(temporary, path)
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
        os.replace(backup, destination)
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
            os.replace(destination, backup)
            _fsync_directory(destination.parent)
        payload["phase"] = "old_moved"
        _write_journal(journal, payload)
        if after_old_move is not None:
            after_old_move()
        try:
            os.replace(candidate, destination)
            _fsync_directory(destination.parent)
        except BaseException:
            if backup.exists() and not destination.exists():
                os.replace(backup, destination)
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
