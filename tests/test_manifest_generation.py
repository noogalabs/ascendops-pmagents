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
