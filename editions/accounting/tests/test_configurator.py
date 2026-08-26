#!/usr/bin/env python3
import hashlib, importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("pmagents_engine", ROOT / "engine" / "engine.py")
engine = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(engine)
FIXTURE = ROOT / "editions" / "accounting" / "fixtures" / "ridgeline-accounting-answers.md"


def digest(root):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()]


class AccountingConfiguratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-accounting-"))
        self.source = self.tmp / "source"
        shutil.copytree(ROOT / "engine" / "tests" / "fixtures" / "raw-maintenance-template", self.source)
        replacements = {"agent_name": "ridge-accounting", "org": "ridgeline",
                        "current_timestamp": "2026-08-25T00:00:00Z", "upstream_update_minute": "17"}
        for path in self.source.rglob("*"):
            if path.is_file():
                text = path.read_text()
                for name, value in replacements.items(): text = text.replace("{{" + name + "}}", value)
                path.write_text(text)

    def tearDown(self): shutil.rmtree(self.tmp)

    def test_production_entry_and_declared_filename(self):
        print("ARMED: wrong declared accounting filename rejects by name")
        out = self.tmp / "out"
        engine.configure(self.source, FIXTURE, out, "accounting")
        self.assertTrue((out / "accounting-config.json").is_file())
        self.assertFalse((out / "seat-config.json").exists())
        self.assertEqual(json.loads((out / "accounting-config.json").read_text())["seat"], "accounting")

    def test_create_then_reconfigure_is_byte_stable(self):
        out = self.tmp / "out"
        clock = lambda: __import__("datetime").date(2026, 8, 25)
        engine.configure(self.source, FIXTURE, out, "accounting", clock=clock)
        engine.configure(out, FIXTURE, out, "accounting", clock=clock)
        payload = json.loads((out / "accounting-config.json").read_text())
        self.assertEqual(payload["configuration_engine"]["configuration_date"], "2026-08-25")
        self.assertTrue((out / "GUARDRAILS.md").is_file())

    def test_sealed_core_unchanged(self):
        self.assertEqual(hashlib.sha256(engine.SEALED_CORE.read_bytes()).hexdigest(),
                         "0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551")


if __name__ == "__main__": unittest.main()
