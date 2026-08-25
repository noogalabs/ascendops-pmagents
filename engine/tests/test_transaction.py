#!/usr/bin/env python3
import importlib.util
import multiprocessing
import os
import shutil
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("glue_transaction", HERE / "transaction.py")
transaction = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(transaction)


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


if __name__ == "__main__":
    print("ARMED: transactional replacement crash, lock, rerun-source, and census checks")
    unittest.main(verbosity=2)
