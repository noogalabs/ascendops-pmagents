# Native-Windows fix: transaction.py locking and directory-durability

## Problem

`engine/transaction.py` unconditionally imported `fcntl`, a Unix-only stdlib
module. The chain `setup.py -> engine.py -> transaction.py` means a member
running `python setup.py` on native Windows hit `ModuleNotFoundError` before
the setup interview ever ran. A full read of the file (not just the import
line) found a second, independent Windows-blocking mechanism in the same
file: `_fsync_directory` opened a directory with `os.open(path, os.O_RDONLY)`
to fsync it after a rename, a POSIX directory-durability idiom with no CRT
equivalent on Windows.

## Fix

A single module-level flag, `_IS_WINDOWS = sys.platform == "win32"`, decided
once at import time, gates both mechanisms consistently (a live per-call
`sys.platform` check was tried first and rejected: it can diverge from which
module actually got imported, and was caught by a failing test during build).

**Lock**: `DestinationLock` now calls two small platform-dispatched helpers,
`_lock_exclusive_nonblocking` and `_unlock`, instead of bare `fcntl` calls.
On Windows, `msvcrt.locking(fd, LK_NBLCK, 1)` provides the same operational
guarantee `fcntl.flock(fd, LOCK_EX | LOCK_NB)` gave: a non-blocking exclusive
lock, kernel-owned, released automatically the instant the holding process
dies or its handle closes. Any Windows lock failure is translated to
`BlockingIOError` and re-raised as `ConcurrentTransactionError`, matching the
existing POSIX contract exactly; no other failure mode is swallowed.

**Directory fsync**: `_fsync_directory` is now an explicit, documented no-op
on Windows, not a silent one. What is weaker on Windows: a rename that
completes just before a crash or power loss is not guaranteed recorded by
this mechanism (no CRT directory-handle fsync exists to record it). What
stays equally strong on both platforms: every journal write in this module
fsyncs its own regular file handle first, unaffected by this no-op, and
`os.replace` (which performs the rename itself) is a cross-platform-safe
primitive. A real Windows-durable rename (`MoveFileExW` with
`MOVEFILE_WRITE_THROUGH` via ctypes) is a named successor, not implemented
tonight: the five `os.replace` + `_fsync_directory` call sites in this file
are scattered rather than funneled through one chokepoint, so a targeted
ctypes fix was deferred rather than rushed into a wider refactor under time
pressure. The one plain-English consequence of this tradeoff belongs in
PR25's Windows section (a Windows member should know crash-durability is
declared weaker, not assume parity).

## Full-file census (per explicit review instruction, before any code change)

All 247 lines of `engine/transaction.py` were read start to finish before
touching anything, not just grepped. Confirmed exactly two POSIX-specific
mechanisms exist, no third: the lock and the directory fsync above.
Everything else checked cross-platform-safe: `os.getpid`, `Path.open`,
`os.fsync` on a regular file handle (line 67, distinct from the directory
case), `Path.samefile` (Windows-supported since Python 3.2 via file index
numbers), `os.replace` (deliberately cross-platform-safe, why it is used
here instead of `os.rename`), `iterdir`/`relative_to`/`unlink`, `re.compile`.

One minor, non-blocking note: `shutil.rmtree` (lines 170, 242) could hit
Windows' read-only-file-attribute deletion quirk more often than on POSIX,
but it is already wrapped in an existing `except OSError` that converts
failure into a non-fatal `cleanup_warning` on the returned `TransactionResult`
rather than crashing, so this is not a third blocking mechanism.

## Casualties (all independently mutation-armed, see below)

1. **Import-succeeds on a Windows-shaped environment.** Loads a fresh copy
   of `transaction.py` with `sys.platform` patched to `win32` and the real
   `fcntl` module hidden from `sys.modules` (raising `ImportError` for it,
   as a real Windows host would), a mock `msvcrt` substituted. Asserts the
   module loads without error. This is the direct regression pin for the
   original P1.
2. **Windows-branch lock engagement and lock-failure-raises.** Calls
   `_lock_exclusive_nonblocking` directly against a mocked `msvcrt`, asserts
   `msvcrt.locking` is called with `(fd, LK_NBLCK, 1)` on the success path,
   then asserts `BlockingIOError` is raised when the mock is configured to
   raise `OSError` (simulating contention). Also asserts `_unlock` calls
   `msvcrt.locking(fd, LK_UNLCK, 1)`.
3. **Two-locker contention, named refusal, Windows-mocked.** Mirrors the
   existing real cross-process POSIX test
   (`test_named_second_owner_fails_before_destination_write`) using the
   Windows-shaped module: a first `DestinationLock` acquires successfully
   (mock returns success once), a second attempt on the same destination
   raises `ConcurrentTransactionError` naming the destination path, and the
   destination's existing file content is unchanged.
4. **Standing call-site census.** Asserts `_fsync_directory(` appears
   exactly 6 times as a call (not counting the definition) and asserts no
   bare `import fcntl`/`termios`/`grp`/`pwd`/`resource`/etc. reappears at
   module scope outside the `_IS_WINDOWS` branch. A seventh caller added
   later, or a new unix-only import reintroduced at module scope, fails this
   test, converting tonight's one-time full-file read into a permanent
   guard rather than a one-off audit.

**Mutation-arm performed directly** (not just described): neutralized the
Windows branch of `_lock_exclusive_nonblocking` to a no-op (`pass`, always
"succeeding"). Confirmed casualties 2 and 3 above both fail exactly as
required, proving the fail-open shape is caught, then restored the real
branch and re-confirmed all 9 tests in `test_transaction.py` pass and the
full `engine/tests` suite (105 passed, 34 subtests) stays green.

## Verification

- `engine/tests/test_transaction.py`: 9 passed (5 pre-existing unchanged
  behaviorally on POSIX, 4 new).
- `engine/tests` (full suite): 105 passed, 34 subtests passed.
- `python3 ci/generate-manifest.py --check`: exit 0.
- `python3 ci/member-hygiene.py`: CLEAN. (Caught and fixed one real finding
  during this fix itself: an earlier draft of the docstring referenced the
  internal successor task's bus ID directly in shipped member-facing code;
  removed before this freeze, since an internal tracking identifier has no
  business appearing on a surface members read.)

## Gap Rule

Structural only. No property-management numbers, thresholds, scripts,
workflows, or domain judgment calls. This is a cross-platform compatibility
fix to existing crash-recovery/locking machinery; the durability tradeoff
documented above is an engineering disclosure, not a domain-practice claim.

## Honest non-claim

No CI leg exercises this on an actual Windows runner. Native-Windows
execution of `transaction.py` remains **unproven by CI**; the binding
evidence for this fix is the mocked-Windows-shaped test suite above, plus
direct code review proving both mechanisms now branch correctly at
`_IS_WINDOWS` with no other unix-only call remaining in the file (per the
full-file census). If a Windows CI runner is ever added, these same tests
should be re-run for real there, not just via mocks.
