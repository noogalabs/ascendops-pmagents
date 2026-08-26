#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tracked_manifest", ROOT / "ci" / "generate-manifest.py")
manifest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(manifest)


class ManifestGenerationTests(unittest.TestCase):
    def test_named_ci_runs_tracked_manifest_check(self):
        workflow = (ROOT / ".github" / "workflows" / "test.yml").read_text()
        self.assertIn("python3 ci/generate-manifest.py --check", workflow)

    def test_named_ci_discovers_every_edition_suite_in_separate_processes(self):
        print("ARMED: CI discovers every edition suite from the filesystem")
        workflow = (ROOT / ".github" / "workflows" / "test.yml").read_text()
        suite_dirs = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "editions").glob("*/tests") if path.is_dir()
        )
        self.assertEqual(suite_dirs, [
            "editions/accounting/tests",
            "editions/business-development/tests",
            "editions/leasing/tests",
            "editions/maintenance/tests",
            "editions/pm-assist/tests",
            "editions/turnover/tests",
        ])
        self.assertIn("for suite in editions/*/tests", workflow)
        self.assertIn('python3 -m unittest discover -s "$suite"', workflow)
        for suite in suite_dirs:
            self.assertNotIn(suite, workflow)
        self.assertIn("python3 -m unittest -v tests.test_manifest_generation", workflow)
        self.assertIn("python3 -m unittest -v tests.test_review_sweeps", workflow)

    def test_named_untracked_cache_can_never_enter_manifest(self):
        print("ARMED: untracked __pycache__ is outside the tracked manifest census")
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            planted = Path(directory) / "__pycache__" / "planted.pyc"
            planted.parent.mkdir()
            planted.write_bytes(b"untracked")
            rendered = manifest.render()
            self.assertNotIn(str(planted.relative_to(ROOT)), rendered)
        self.assertEqual(
            [str(path.relative_to(ROOT)) for path in manifest.tracked_files()],
            sorted(str(path.relative_to(ROOT)) for path in manifest.tracked_files()),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
