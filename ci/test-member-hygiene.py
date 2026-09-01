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


    # Owner rule 2026-09-01: software-agnostic AND model-agnostic duty surfaces.
    def _stage(self, root, relative, text):
        path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text); subprocess.run(["git","add",relative],cwd=root,check=True)

    def test_named_planted_platform_name_on_duty_surface_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "SOUL.md", "Open the ticket in Property" + "Meld.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0)
        self.assertIn("SOUL.md:1: platform name 'Property" + "Meld' on duty surface",result.stdout)

    def test_named_lowercase_platform_noun_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "SOUL.md", "Close the me" + "ld when done.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("SOUL.md:1: platform name",result.stdout)

    def test_named_platform_name_inside_platform_variant_skill_passes(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, ".claude/skills/propertymeld/SKILL.md", "# Property" + "Meld variant\nRun pm me" + "ld list.\n")
        result=self.run_gate(root); self.assertEqual(result.returncode,0,result.stdout)

    def test_named_path_reference_to_platform_variant_skill_passes(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "MANIFEST.txt", "abc  .claude/skills/property" + "meld/SKILL.md\n")
        result=self.run_gate(root); self.assertEqual(result.returncode,0,result.stdout)

    def test_named_prose_platform_name_sharing_a_line_with_the_variant_path_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "SOUL.md", "See .claude/skills/property" + "meld/SKILL.md when Property" + "Meld shows a new ticket.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("SOUL.md:1: platform name 'Property" + "Meld'",result.stdout)

    def test_named_platform_exact_site_allowlist_passes_then_moved_site_dies(self):
        import hashlib
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        line="Example answer: App" + "Folio"
        self._stage(root, "answers.md", line + "\n")
        allow = root / "ci/internal-codename-allowlist.tsv"
        allow.write_text(allow.read_text() + f"answers.md\t1\t{hashlib.sha256(line.encode()).hexdigest()}\tplatform\tsetup-answer example\n")
        subprocess.run(["git","add","ci/internal-codename-allowlist.tsv"],cwd=root,check=True)
        self.assertEqual(self.run_gate(root).returncode,0)
        self._stage(root, "answers.md", "# moved\n" + line + "\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0)
        self.assertIn("answers.md:2: platform name",result.stdout); self.assertIn("stale internal-codename allowlist row",result.stdout)

    def test_named_planted_model_name_on_duty_surface_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "GUARDRAILS.md", "Ask Cla" + "ude before sending.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0)
        self.assertIn("GUARDRAILS.md:1: model name 'Cla" + "ude' on duty surface",result.stdout)

    def test_named_planted_model_id_on_duty_skill_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, ".claude/skills/intake/SKILL.md", "Route triage to cla" + "ude-sonnet-4-5 when unsure.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("SKILL.md:1: model name",result.stdout)

    def test_named_model_name_on_runtime_surfaces_passes_as_declared_class(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "CLAUDE.md", "# Cla" + "ude Remote Agent\n")
        self._stage(root, ".claude/skills/agent-management/SKILL.md", "Spawn a Cla" + "ude Code worker.\n")
        self._stage(root, "engine/scan.py", "OPENAI_KEY = 'sk-'\n")
        result=self.run_gate(root); self.assertEqual(result.returncode,0,result.stdout)

    def test_named_frontmatter_model_routing_line_passes_but_body_model_prose_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, ".claude/skills/intake/SKILL.md", "---\nname: intake\nmodel: Son" + "net\n---\nTriage the ticket.\n")
        self.assertEqual(self.run_gate(root).returncode,0)
        self._stage(root, ".claude/skills/intake/SKILL.md", "---\nname: intake\nmodel: Son" + "net\n---\nWhy this is a Son" + "net skill.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("SKILL.md:5: model name",result.stdout)

    def test_named_model_key_outside_the_frontmatter_block_dies(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, ".claude/skills/intake/SKILL.md", "---\nname: intake\n---\nTriage.\nmodel: Son" + "net\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("SKILL.md:5: model name",result.stdout)

    def test_named_readme_is_a_scanned_duty_surface(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "README.md", "# Pack\nRuns on Cla" + "ude.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("README.md:2: model name",result.stdout)

    def test_named_hyphenated_model_forms_die_and_bare_controls_die(self):
        # piper F1: a hyphen after the token must not hide it (platform_re never allowed it)
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        for i, form in enumerate(("Anthro" + "pic-built", "Open" + "AI-compatible", "Gem" + "ini-powered", "Co" + "dex-driven", "Op" + "us-class", "bare Anthro" + "pic", "bare Op" + "us")):
            self._stage(root, "SOUL.md", f"An {form} step.\n")
            result=self.run_gate(root); self.assertNotEqual(result.returncode,0,form); self.assertIn("SOUL.md:1: model name",result.stdout,form)

    def test_named_agents_md_is_a_scanned_duty_surface(self):
        # piper F2: AGENTS.md ships to members as session protocol + role steps
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "AGENTS.md", "# Session start\nAsk Cla" + "ude first.\n")
        result=self.run_gate(root); self.assertNotEqual(result.returncode,0); self.assertIn("AGENTS.md:2: model name",result.stdout)

    def test_named_clean_line_declares_the_runtime_exempt_denominator(self):
        # piper F2: the exempt class must be visible beside CLEAN, with its count
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "CLAUDE.md", "# Cla" + "ude Remote Agent\n"); self._stage(root, "engine/scan.py", "X = 1\n")
        result=self.run_gate(root); self.assertEqual(result.returncode,0,result.stdout)
        # fixture: internal.py (.py code class) + engine/scan.py + CLAUDE.md = 3 exempt files
        self.assertIn("exempt as runtime class: 3 files", result.stdout)

    def test_named_english_word_case_does_not_false_positive(self):
        root=self.fixture(); self.addCleanup(shutil.rmtree, root)
        self._stage(root, "SOUL.md", "Tell the resident a short fable about patience.\n")
        result=self.run_gate(root); self.assertEqual(result.returncode,0,result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
