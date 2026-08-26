#!/usr/bin/env python3
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "editions" / "turnover" / "fixtures" / "ridgeline-turnover-answers.md"
MAPPING = ROOT / "engine" / "mappings" / "turnover-coordinator.json"
SOURCE = ROOT / "editions" / "turnover" / "library-src"
import sys
sys.path.insert(0, str(ROOT / "engine"))
import engine

SPEC = importlib.util.spec_from_file_location("pmagents_setup", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(setup)


def digest(root: Path):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()]


class TurnoverConfiguratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-turnover-"))
        self.source = SOURCE

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def configure(self, destination: Path):
        engine.configure(
            self.source, FIXTURE, destination, "turnover-coordinator",
            clock=lambda: datetime.date(2026, 8, 25), seat_registry={},
        )

    def fixture_variant(self, pattern: str, replacement: str) -> Path:
        text, count = re.subn(pattern, replacement, FIXTURE.read_text(), count=1, flags=re.M)
        self.assertEqual(count, 1, f"fixture mutation pattern drifted: {pattern}")
        path = self.tmp / f"variant-{len(list(self.tmp.glob('variant-*')))}.md"
        path.write_text(text)
        return path

    def test_production_entry_declared_filename_and_library(self):
        output = self.tmp / "configured"
        self.configure(output)
        self.assertTrue((output / "turnover-config.json").is_file())
        self.assertFalse((output / "seat-config.json").exists())
        payload = json.loads((output / "turnover-config.json").read_text())
        self.assertEqual(payload["seat"], "turnover-coordinator")
        self.assertEqual(set(payload["answers"]), set(engine.SUPPORTED["turnover-coordinator"]["question_ids"]))
        companions = json.loads((ROOT / "engine" / "edition-review-ledger.json").read_text())[
            "editions"
        ]["turnover-coordinator"]["companions"]
        self.assertEqual(len(companions), 10)
        self.assertTrue(all((output / name).is_file() for name in companions))

    def test_create_then_reconfigure_is_stable(self):
        print("ARMED: turnover create-then-reconfigure uses the production rerun entry")
        output = self.tmp / "configured"
        self.configure(output)
        self.source = output
        self.configure(output)
        self.assertTrue((output / "turnover-config.json").is_file())
        self.assertEqual(json.loads((output / "turnover-config.json").read_text())["seat"], "turnover-coordinator")

    def test_declared_filename_mutation_rejects_by_name(self):
        print("ARMED: wrong declared turnover filename rejects by name")
        mapping = json.loads(MAPPING.read_text())
        mapping["structured_answers_file"] = "../wrong.json"
        with self.assertRaises(engine.cross_seat.CrossSeatRejected) as caught:
            engine.cross_seat.structured_answers_filename(mapping)
        self.assertIn("structured_answers_file", str(caught.exception.failures))

    def test_declared_seam_types_fire_and_absent_owners_are_inert_safe(self):
        print("ARMED: turnover POLICY_DIVERGE seam checks fire; unnormalized timezone fact is absent")
        mapping = json.loads(MAPPING.read_text())
        current = {"seat":"turnover-coordinator", "answers":{"C1":"$500", "D6":"local policy"},
                   "company":{"timezone":"America/Denver"},
                   "configuration_engine":{"version":"1.1.0"}}
        peer_root = self.tmp / "maintenance"; peer_root.mkdir()
        (peer_root / "seat-config.json").write_text(json.dumps({
            "seat":"maintenance-coordinator", "answers":{"B1":"$400", "C7":"peer policy"},
            "company":{"timezone":"America/New_York"},
            "configuration_engine":{"version":"1.1.0"},
        }))
        self.assertNotIn("SEAM-19", {row["check_id"] for row in mapping["cross_seat"]["checks"]})
        selected = {**mapping, "cross_seat": {"checks": [mapping["cross_seat"]["checks"][0], mapping["cross_seat"]["checks"][-1]]}}
        result = engine.cross_seat.apply(current, selected, {"maintenance-coordinator": peer_root}, engine_version="1.1.0")
        self.assertEqual({row["doctrine"] for row in result.report_items}, {"POLICY_DIVERGE"})
        absent = engine.cross_seat.apply(current, selected, {}, engine_version="1.1.0")
        self.assertEqual(absent.report_items, [])

    def test_zero_touch_wrapper_equals_direct_and_uses_turnover_labels(self):
        print("ARMED: setup renders turnover question labels and wrapper bytes equal direct configure")
        wrapped, direct = self.tmp / "wrapped", self.tmp / "direct"
        seat_number = next(
            number for number, row in enumerate(setup.SEATS, 1)
            if row["id"] == "turnover-coordinator"
        )
        scripted = iter([str(seat_number), str(self.source), str(wrapped), "2", str(FIXTURE)])
        stdout = io.StringIO()
        self.assertEqual(setup.run_setup(ask=lambda _p: next(scripted), out=stdout,
                                         clock=lambda: datetime.date(2026, 8, 25)), 0)
        engine.configure(self.source, FIXTURE, direct, "turnover-coordinator",
                         clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertEqual(digest(wrapped), digest(direct))
        labels = setup.questionnaire_fields(
            FIXTURE.read_text(), engine.cover_fields_for_seat("turnover-coordinator")
        )
        self.assertIn("E8. Which channels carry escalations, and to whom?", {row.label for row in labels})

    def test_named_content_divergent_fixture_cannot_substitute_for_turnover(self):
        print("ARMED: turnover rerun derives its own content-divergent fixture")
        output = self.tmp / "configured-divergent"
        self.configure(output)
        before = digest(output)
        maintenance = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(output, maintenance, output, "turnover-coordinator",
                             clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertIn("E1", caught.exception.render())
        self.assertEqual(digest(output), before)

    def test_named_b2_labeled_number_rejects_earlier_unbound_number(self):
        print("ARMED: turnover legal/operational number requires its labeled line")
        adversarial = self.fixture_variant(
            r"^Answer: Default turn target days: 12\n  Class B 12 days.*$",
            "Answer: Use 2 delivery methods at least 60 days before the turn target.",
        )
        output = self.tmp / "unlabeled-number"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, adversarial, output, "turnover-coordinator",
                             clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertIn("Default turn target days", caught.exception.render())
        self.assertFalse(output.exists())

    def test_named_all_turnover_numeric_domains_reject_zero_before_activation(self):
        print("ARMED: every turnover numeric config value is strictly positive")
        mapping = json.loads(MAPPING.read_text())
        expected = {
            "/turn_target_days", "/inspection_sla_hours",
            "/scope_sla_hours", "/stale_stage_alert_days", "/approval_threshold",
        }
        rows = {row["path"]: row for row in mapping["config_keys"] if row["path"] in expected}
        self.assertEqual(set(rows), expected)
        self.assertTrue(all(row.get("minimum") == 1 for row in rows.values()))
        for label in ("Inspection SLA hours", "Scope SLA hours", "Stale-stage alert days"):
            variant = self.fixture_variant(rf"^{re.escape(label)}: .*$", f"{label}: 0")
            output = self.tmp / ("zero-" + label.casefold().replace(" ", "-"))
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(self.source, variant, output, "turnover-coordinator",
                                 clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
            self.assertIn("minimum 1", caught.exception.render())
            self.assertFalse(output.exists())
        approval = self.fixture_variant(r"^Answer: \$500 base pre-approved reserve\..*$", "Answer: $0")
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, approval, self.tmp / "zero-approval", "turnover-coordinator",
                             clock=lambda: datetime.date(2026, 8, 25), seat_registry={})
        self.assertIn("minimum 1", caught.exception.render())

    def test_named_turnover_seam_contract_and_permanent_human_gates(self):
        print("ARMED: SEAM-2 targets turnover D2 and shipped posture stays human-released")
        leasing = json.loads((ROOT / "engine" / "mappings" / "leasing-coordinator.json").read_text())
        pointer = next(row for row in leasing["cross_seat"]["pointers"]
                       if row["value_name"] == "move_out_inspection_owner")
        self.assertEqual(pointer["owner_seat"], "turnover-coordinator")
        self.assertEqual(pointer["owner_question_id"], "D2")
        self.assertEqual(pointer["owner_value_path"], "/answers/D2")
        questionnaire = (ROOT / "editions" / "turnover" / "answers-format.md").read_text()
        self.assertRegex(questionnaire, r"(?m)^D2\. Who conducts pre-move-out, move-out, and final inspections on-site\?")
        self.assertIn("Human release remains the shipped posture for every outbound message", questionnaire)
        self.assertNotIn("graduate to autonomous send", questionnaire)
        mapping = json.loads(MAPPING.read_text())
        self.assertEqual(
            {row["gate_id"] for row in mapping["cross_seat"]["never_graduate"]},
            {"make_ready_scope_budget", "deposit_deductions", "vendor_pricing", "damage_charge_notice"},
        )

    def test_named_readme_routes_only_through_guided_setup(self):
        print("ARMED: turnover README routes configuration through setup.py only")
        readme = (SOURCE / "README.md").read_text()
        self.assertIn("run `python3 setup.py`", readme)
        self.assertIn("`turnover-config.json` source of truth", readme)
        self.assertNotIn("Setup (manual)", readme)
        self.assertNotIn("replace the placeholders", readme)
        self.assertNotIn("not a guided setup wizard", readme)

    def test_named_onboarding_is_post_config_and_does_not_recollect_answers(self):
        print("ARMED: turnover first boot verifies configured custody without a second interview")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        skill = (SOURCE / ".claude" / "skills" / "onboarding" / "SKILL.md").read_text()
        self.assertIn("Read `turnover-config.json`", onboarding)
        self.assertIn("only new values collected at first boot are deployment credentials", onboarding)
        self.assertIn("rerun `python3 setup.py`", onboarding)
        for required in (
            "Repository `setup.py` is the single configuration interview",
            "read `turnover-config.json` in full",
            "Do not correct, recollect, or silently substitute turnover answers",
            "The only values first boot may collect",
        ):
            self.assertIn(required, skill)
        for stale in (
            "what's your name", "How many units do you manage",
            "Who are your go-to vendors", "A few operating numbers",
            "What timezone should I use",
            "reverse-prompting interview", "YOU ask the operator questions",
            "write each answer into your config",
        ):
            self.assertNotIn(stale, onboarding)
            self.assertNotIn(stale, skill)

    def test_named_onboarding_completion_preserves_all_five_custody_properties(self):
        print("ARMED: turnover completion is gated, idempotent, rollback-safe, durable, and heartbeat-last")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        gate = onboarding.index("if grep -rlE")
        remove_set = onboarding.index("for c in heartbeat pipeline-review certify-check")
        pipeline = onboarding.index('add-cron "$CTX_AGENT_NAME" pipeline-review')
        certify = onboarding.index('add-cron "$CTX_AGENT_NAME" certify-check')
        marker = onboarding.index('touch "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"')
        heartbeat = onboarding.index('add-cron "$CTX_AGENT_NAME" heartbeat')
        self.assertLess(gate, remove_set)
        self.assertLess(remove_set, pipeline)
        self.assertLess(pipeline, marker)
        self.assertLess(certify, marker)
        self.assertLess(marker, heartbeat)
        failure = onboarding.split("  else\n", 1)[1]
        self.assertIn('rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"', failure)
        self.assertIn("for c in pipeline-review certify-check", failure)
        self.assertNotIn("for c in heartbeat pipeline-review certify-check", failure)
        self.assertIn("durably marked complete but heartbeat registration failed", onboarding)

    def test_named_every_turnover_onboarding_bash_block_parses(self):
        print("ARMED: every embedded turnover onboarding Bash block passes bash -n")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        blocks = re.findall(r"(?m)^([ \t]*)```bash\n(.*?)\n\1```$", onboarding, re.S)
        self.assertEqual(len(blocks), 3)
        for index, (_indent, block) in enumerate(blocks, 1):
            parsed = subprocess.run(
                ["bash", "-n"], input=block, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(parsed.returncode, 0,
                             f"ONBOARDING bash block {index} does not parse: {parsed.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
