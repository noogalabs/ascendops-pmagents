#!/usr/bin/env python3
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import io
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EDITION = ROOT / "editions" / "pm-assist"
FIXTURE = EDITION / "fixtures" / "ridgeline-pm-assist-answers.md"

SPEC = importlib.util.spec_from_file_location("pmagents_setup", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(setup)


def digest(root: Path):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()]


class PMAssistConfiguratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmassist-edition-"))
        self.source = self.tmp / "source"
        shutil.copytree(EDITION / "library-src", self.source)
        self.clock = lambda: datetime.date(2026, 8, 25)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_named_production_entry_and_declared_filename(self):
        print("ARMED: pm-assist production configure and declared filename casualty")
        output = self.tmp / "configured"
        setup.engine.configure(self.source, FIXTURE, output, "pm-assist", clock=self.clock, seat_registry={})
        payload = json.loads((output / "seat-config.json").read_text())
        self.assertEqual(payload["seat"], "pm-assist")
        self.assertFalse((output / "pm-assist-config.json").exists())
        self.assertEqual(payload["configuration_engine"]["seat_library"], "pm-assist-2026-08-25")

    def test_named_create_then_reconfigure(self):
        print("ARMED: pm-assist create then reconfigure uses managed rerun")
        output = self.tmp / "configured"
        setup.engine.configure(self.source, FIXTURE, output, "pm-assist", clock=self.clock, seat_registry={})
        setup.engine.configure(output, FIXTURE, output, "pm-assist", clock=self.clock, seat_registry={})
        payload = json.loads((output / "seat-config.json").read_text())
        self.assertEqual(payload["seat"], "pm-assist")
        self.assertEqual(payload["answers"]["A2"].split(",", 1)[0], "Dana Wren")

    def test_named_member_census_and_skill_placeholder(self):
        print("ARMED: skill-walk removal leaves a PM-assist member marker and dies")
        output = self.tmp / "configured"
        setup.engine.configure(self.source, FIXTURE, output, "pm-assist", clock=self.clock, seat_registry={})
        residual = []
        for path in output.rglob("*"):
            if path.is_file():
                try: text = path.read_text()
                except UnicodeDecodeError: continue
                tokens = re.findall(r"\{\{[a-zA-Z0-9_]+\}\}", text)
                if any(token != "{{CTX_ROOT}}" for token in tokens):
                    residual.append(str(path.relative_to(output)))
        self.assertEqual(residual, [])
        skill = output / ".claude" / "skills" / "monday-board" / "SKILL.md"
        self.assertIn("BETTY-PH:followthrough_sweep_day", skill.read_text())

    def test_named_absent_owner_seams_are_inert_and_each_type_registered(self):
        print("ARMED: FACT_MATCH POLICY_DIVERGE ORDERING seam-type removals die by name")
        output = self.tmp / "configured"
        setup.engine.configure(self.source, FIXTURE, output, "pm-assist", clock=self.clock, seat_registry={})
        payload = json.loads((output / "seat-config.json").read_text())
        checks = {row["doctrine"]: row for row in payload["cross_seat_checks"]}
        self.assertEqual(set(checks), {"FACT_MATCH", "POLICY_DIVERGE", "ORDERING"})
        self.assertTrue(all(row["status"] == "peer_absent" for row in checks.values()))
        self.assertEqual(set(payload["cross_seat"]["held"]),
                         {"deposit_disposition_days", "entry_notice_hours", "maintenance_sla", "platform_of_record"})

    def test_named_zero_touch_wrapper_equals_direct_tree_and_labels(self):
        print("ARMED: pm-assist zero-touch wrapper tree and question-label casualty")
        wrapped, direct = self.tmp / "wrapped", self.tmp / "direct"
        scripted = iter(["2", str(self.source), str(wrapped), "2", str(FIXTURE)])
        stdout = io.StringIO()
        self.assertEqual(setup.run_setup(ask=lambda _p: next(scripted), out=stdout, clock=self.clock), 0)
        setup.engine.configure(self.source, FIXTURE, direct, "pm-assist", clock=self.clock, seat_registry={})
        self.assertEqual(digest(wrapped), digest(direct))
        fields = setup.answer_field_map(FIXTURE)
        self.assertIn("A10. What state-required landlord filings", fields["A10"].label)


if __name__ == "__main__":
    unittest.main(verbosity=2)
