#!/usr/bin/env python3
import importlib.util, shutil, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "member-hygiene.py"


class MemberHygieneTests(unittest.TestCase):
    def fixture(self):
        root = Path(tempfile.mkdtemp(prefix="pmagents-hygiene-"))
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        (root / "ci").mkdir(); shutil.copy2(SCRIPT, root / "ci/member-hygiene.py")
        (root / "README.md").write_text("# AscendOps PMAgents\n")
        (root / "internal.py").write_text("SCHEMA = 'bet" + "ty-seat-config'\n")
        (root / "VALIDATION-REPORT.md").write_text("Tracked internally as task_123_456.\n")
        (root / "engine").mkdir()
        (root / "engine/E3-EXTENSION-REPORT.md").write_text("# Member guide\n")
        line=(root / "internal.py").read_text().splitlines()[0]
        import hashlib
        digest=hashlib.sha256(line.encode()).hexdigest()
        (root / "ci/member-visible-paths.txt").write_text("README.md\nengine/E3-EXTENSION-REPORT.md\n")
        (root / "ci/internal-codename-allowlist.tsv").write_text(f"internal.py\t1\t{digest}\tbetty\tcompatibility schema\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        return root

    def run_gate(self, root):
        return subprocess.run(["python3", str(root / "ci/member-hygiene.py"), "--root", str(root)], text=True, capture_output=True)

    def test_named_clean_seed_passes_without_baseline(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self.assertEqual(self.run_gate(root).returncode, 0)

    def test_named_planted_private_first_name_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        (root / "README.md").write_text("Send this to Da" + "vid.\n"); subprocess.run(["git","add","README.md"],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("README.md:1: private identity token",result.stdout)

    def test_named_planted_banned_token_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        (root / "README.md").write_text("Use NE" + "PQ.\n"); subprocess.run(["git","add","README.md"],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("README.md:1: banned sales token",result.stdout)

    def test_named_member_visible_codename_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        (root / "README.md").write_text("Bet" + "ty guide.\n"); subprocess.run(["git","add","README.md"],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("member-visible surface",result.stdout)

    def test_named_planted_member_task_id_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        (root / "README.md").write_text("Wait for task_123_456.\n"); subprocess.run(["git","add","README.md"],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("README.md:1: internal task id on shipped member surface",result.stdout)

    def test_named_planted_member_visible_report_task_id_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        report = root / "engine/E3-EXTENSION-REPORT.md"
        report.write_text("Wait for task_123_456.\n"); subprocess.run(["git","add",str(report.relative_to(root))],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("engine/E3-EXTENSION-REPORT.md:1: internal task id on shipped member surface",result.stdout)

    def test_named_internal_unlisted_report_task_id_passes(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        result=self.run_gate(root); self.assertEqual(result.returncode,0)
        self.assertNotIn("VALIDATION-REPORT.md", result.stdout)

    def test_named_moved_internal_allowlist_site_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        (root / "internal.py").write_text("# moved\nSCHEMA = 'bet" + "ty-seat-config'\n"); subprocess.run(["git","add","internal.py"],cwd=root,check=True)
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("lacks exact-site allowlist",result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
