#!/usr/bin/env python3
from __future__ import annotations

import datetime
import base64
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine"))
import engine

SETUP_SPEC = importlib.util.spec_from_file_location("pmagents_setup_leasing", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SETUP_SPEC)
assert SETUP_SPEC.loader
SETUP_SPEC.loader.exec_module(setup)

EDITION = ROOT / "editions" / "leasing"
FIXTURE = EDITION / "fixtures" / "ridgeline-leasing-answers.md"
SOURCE = EDITION / "library-src"
MAPPING = ROOT / "engine" / "mappings" / "leasing-coordinator.json"


def digest(root):
    return [(str(p.relative_to(root)), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob("*")) if p.is_file()]


class LeasingEditionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-leasing-"))
        self.clock = lambda: datetime.date(2026, 8, 25)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def configure(self, output, mapping=None, answers=FIXTURE):
        original = engine.SUPPORTED["leasing-coordinator"]["mapping"]
        if mapping is not None:
            engine.SUPPORTED["leasing-coordinator"]["mapping"] = mapping
        try:
            engine.configure(SOURCE, answers, output, "leasing-coordinator",
                             clock=self.clock, seat_registry={})
        finally:
            engine.SUPPORTED["leasing-coordinator"]["mapping"] = original

    def test_named_production_entry_and_create_then_reconfigure(self):
        print("ARMED: leasing production entry and create-then-reconfigure")
        output = self.tmp / "configured"
        self.configure(output)
        engine.configure(output, FIXTURE, output, "leasing-coordinator",
                         clock=self.clock, seat_registry={})
        payload = json.loads((output / "leasing-config.json").read_text())
        self.assertEqual(payload["seat"], "leasing-coordinator")
        self.assertEqual(len(payload["answers"]), 39)

    def test_named_wrong_declared_filename_rejects(self):
        print("ARMED: wrong declared filename rejects by name")
        mapping = json.loads(MAPPING.read_text())
        mapping["structured_answers_file"] = "../wrong-leasing-config.json"
        path = self.tmp / "wrong-mapping.json"
        path.write_text(json.dumps(mapping))
        with self.assertRaises(engine.IntakeRejected) as caught:
            self.configure(self.tmp / "wrong", path)
        self.assertIn("mapping.structured_answers_file", str(caught.exception.failures))
        self.assertFalse((self.tmp / "wrong").exists())

    def test_named_each_declared_seam_type_fires_when_peer_present(self):
        print("ARMED: incomparable platform and escalation prose checks stay absent")
        mapping = json.loads(MAPPING.read_text())
        checks = {row["check_id"] for row in mapping["cross_seat"]["checks"]}
        self.assertEqual(checks, set())
        self.assertNotIn("platform-fact", checks)
        self.assertNotIn("escalation-policy", checks)

    def test_named_onboarding_gate_precedes_every_heartbeat_instruction(self):
        print("ARMED: leasing first boot gates heartbeat until onboarding completes")
        agents = (SOURCE / "AGENTS.md").read_text()
        searchable = agents.casefold()
        gate = searchable.index("${ctx_root}/state/${ctx_agent_name}/.onboarded")
        heartbeat = searchable.index("update heartbeat")
        self.assertLess(gate, heartbeat)
        self.assertIn("Do not continue into Session Start", agents)

        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        self.assertIn("always replace the `## Name` marker line", onboarding)
        self.assertIn("Use `$CTX_AGENT_NAME` as the default display value", onboarding)
        self.assertNotIn("only when the operator wants", onboarding)

    def test_named_onboarding_failure_cannot_leave_heartbeat_live(self):
        print("ARMED: heartbeat registration follows the durable onboarding marker")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        heartbeat = onboarding.index('add-cron "$CTX_AGENT_NAME" heartbeat')
        marker = onboarding.index('touch "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"')
        self.assertLess(marker, heartbeat)
        for name in (
            "applicant-screening-digest", "renewal-window-am", "renewal-window-pm",
            "lease-abstraction-intake", "fair-housing-presend-sweep",
        ):
            self.assertLess(onboarding.index(f'add-cron "$CTX_AGENT_NAME" {name}'), heartbeat)
        failure = onboarding.split("  else\n", 1)[1]
        self.assertIn("ROLLBACK", failure)
        self.assertIn('rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"', failure)
        self.assertIn('remove-cron "$CTX_AGENT_NAME" "$c"', failure)
        for name in (
            "applicant-screening-digest", "renewal-window-am",
            "renewal-window-pm", "lease-abstraction-intake", "fair-housing-presend-sweep",
        ):
            self.assertIn(name, failure)
        self.assertNotIn("for c in heartbeat", failure)
        self.assertIn("durably marked complete but heartbeat registration failed", onboarding)
        self.assertIn("Re-run this block", onboarding)
        self.assertLess(failure.index("rm -f"), failure.index("STOP:"))
        self.assertLess(failure.index("remove-cron"), failure.index("STOP:"))

    def test_named_every_onboarding_bash_block_parses(self):
        print("ARMED: every embedded onboarding Bash block passes the real parser")
        onboarding = (SOURCE / "ONBOARDING.md").read_text()
        fenced = re.findall(
            r"(?m)^([ \t]*)```bash\n(.*?)\n\1```$", onboarding, re.S,
        )
        self.assertEqual(len(fenced), 5)
        for index, (_, block) in enumerate(fenced, start=1):
            parsed = subprocess.run(
                ["bash", "-n"], input=block, text=True,
                capture_output=True, check=False,
            )
            self.assertEqual(
                parsed.returncode, 0,
                f"ONBOARDING bash block {index} does not parse: {parsed.stderr}",
            )

    def test_named_d7_and_cross_seat_contract_rows_match_authority(self):
        print("ARMED: leasing D7 and cross-seat authority rows stay exact")
        mapping = json.loads(MAPPING.read_text())
        placeholders = {row["placeholder"] for row in mapping["placeholders"]}
        self.assertNotIn("owner_name", placeholders)
        for relative in ("README.md", "USER.md", "ONBOARDING.md"):
            self.assertNotIn("{{owner_name}}", (SOURCE / relative).read_text())

        pointers = {row["value_name"]: row for row in mapping["cross_seat"]["pointers"]}
        self.assertNotIn("external_communications_window", pointers)
        inspection = pointers["move_out_inspection_owner"]
        self.assertEqual((inspection["owner_question_id"], inspection["owner_value_path"]),
                         ("D2", "/answers/D2"))
        self.assertNotIn("notice-ordering",
                         {row["check_id"] for row in mapping["cross_seat"]["checks"]})

        output = self.tmp / "authority-row-output"
        self.configure(output)
        payload = json.loads((output / "leasing-config.json").read_text())
        self.assertNotIn("external_communications_window", payload["cross_seat"]["held"])
        self.assertNotIn("external_communications_window", payload["cross_seat"]["pointers"])

    def test_named_declared_leasing_configuration_reaches_runtime_consumers(self):
        print("ARMED: leasing identity criteria and cover configuration reach runtime consumers")
        output = self.tmp / "runtime-consumers"
        self.configure(output)
        parsed = engine.validate(FIXTURE, "leasing-coordinator")

        config = json.loads((output / "config.json").read_text())
        self.assertEqual(config["agent_name"], "leasing-coordinator")
        agent_name_carriers = [
            path.relative_to(SOURCE) for path in SOURCE.rglob("*")
            if path.is_file() and "{{agent_name}}" in path.read_text(errors="ignore")
        ]
        self.assertGreater(len(agent_name_carriers), 1)
        for relative in agent_name_carriers:
            rendered = (output / relative).read_text()
            self.assertIn("leasing-coordinator", rendered)
            self.assertNotIn("{{agent_name}}", rendered)
        self.assertEqual({key: config[key] for key in (
            "prospect_response_sla_minutes",
            "application_decision_sla_hours",
            "leasing_approval_threshold_usd",
            "renewal_offer_lead_days",
            "renewal_response_window_days",
        )}, {
            "prospect_response_sla_minutes": 15,
            "application_decision_sla_hours": 24,
            "leasing_approval_threshold_usd": 500,
            "renewal_offer_lead_days": 60,
            "renewal_response_window_days": 10,
        })

        identity = (output / "IDENTITY.md").read_text()
        screening = (output / ".claude/skills/applicant-screening/SKILL.md").read_text()
        for answer_id in ("A2", "A3"):
            value = parsed.raw_answers[answer_id]
            self.assertIn(value, identity)
            self.assertIn(value, screening)
        self.assertNotIn("{{income_multiplier}}", identity + screening)
        self.assertNotIn("{{credit_min_score}}", identity + screening)

    def fixture_variant(self, question_id, answer):
        text = FIXTURE.read_text()
        next_number = int(question_id[1:]) + 1
        next_id = f"{question_id[0]}{next_number}"
        pattern = rf"(?ms)(^{re.escape(question_id)}\..*?^Answer:).*?(?=\n{re.escape(next_id)}\.)"
        replaced, count = re.subn(pattern, rf"\1 {answer}\n", text)
        self.assertEqual(count, 1)
        path = self.tmp / f"{question_id}-variant.md"
        path.write_text(replaced)
        return path

    def cover_variant(self, label, value):
        text = FIXTURE.read_text()
        pattern = rf"(?m)^({re.escape(label)}:).*$"
        replaced, count = re.subn(pattern, rf"\1 {value}", text)
        self.assertEqual(count, 1)
        path = self.tmp / f"{label.casefold().replace(' ', '-')}-variant.md"
        path.write_text(replaced)
        return path

    def test_named_session_boot_reads_mapping_declared_structured_config(self):
        print("ARMED: session boot reads the mapping-declared structured config")
        mapping = json.loads(MAPPING.read_text())
        declared = engine.cross_seat.structured_answers_filename(mapping)
        agents = (SOURCE / "AGENTS.md").read_text()
        self.assertIn(f"Read `{declared}`", agents)

    def test_named_configured_renewal_cadence_violation_reaches_stop(self):
        print("ARMED: configured renewal cadence violation reaches the boot STOP")
        violating = self.cover_variant("Renewal offer lead (days)", "35")
        output = self.tmp / "cadence-violation"
        self.configure(output, answers=violating)
        agents = (output / "AGENTS.md").read_text()
        config = json.loads((output / "config.json").read_text())
        self.assertEqual(config["renewal_offer_lead_days"], 35)
        self.assertEqual(config["renewal_response_window_days"], 10)
        for value in ("35", "10", "30"):
            self.assertIn(value, agents)
        self.assertIn("RENEWAL CADENCE STOP", agents)
        self.assertIn("/renewal_offer_lead_days", agents)
        self.assertIn("/renewal_response_window_days", agents)
        self.assertRegex(agents, r"surface the conflicting configured\s+values")

    def test_named_b3_notice_days_label_controls_configured_floor(self):
        print("ARMED: B3 notice floor comes from the labeled numeric line")
        questionnaire = (EDITION / "answers-format.md").read_text()
        self.assertIn("Notice days: NN", questionnaire)
        parsed = engine.validate(FIXTURE, "leasing-coordinator")
        self.assertTrue(parsed.raw_answers["B3"].startswith("Notice days: 30\n"))
        output = self.tmp / "labeled-notice-days"
        self.configure(output)
        agents = (output / "AGENTS.md").read_text()
        self.assertRegex(agents, re.compile(
            r"configured B3 non-renewal notice floor .*?-->30<!--.*?days\)", re.S))

    def test_named_readme_routes_members_through_guided_setup(self):
        print("ARMED: README advertises the complete guided setup path")
        readme = (SOURCE / "README.md").read_text()
        self.assertIn("python3 setup.py", readme)
        self.assertIn("leasing-config.json", readme)
        for stale in ("## Setup (manual)", "replace the placeholders",
                      "cortextos add-agent", "engine/engine.py"):
            self.assertNotIn(stale, readme)

    def test_named_companion_claim_matches_shipped_library(self):
        print("ARMED: companion claim names only the shipped leasing documents")
        claimed = ("Leasing Message Template Library", "Renewal and Rent-Increase Workflow")
        absent = (
            "Leasing Process End to End", "The Leasing Board Full System Design",
            "Leasing Coordinator Judgment Guide", "CMA Process and Owner Conversation Scripts",
            "Tenant Offer and Negotiation Scripts", "Leasing Board Template spreadsheet",
            "Pre-Move-Out Inspection Checklist", "Move-Out Inspection Checklist",
        )
        for path in (EDITION / "answers-format.md", FIXTURE):
            text = path.read_text()
            for name in claimed:
                self.assertIn(name, text)
            for name in absent:
                self.assertNotIn(name, text)
        shipped = {path.stem for path in SOURCE.glob("*.md")}
        self.assertTrue(set(claimed).issubset(shipped))

    def test_named_shadow_mode_never_promises_unshipped_autonomy(self):
        print("ARMED: shadow-mode outcome matches permanent copilot approval policy")
        banned = ("Autonomy widens by consequence", "graduate to autonomous send",
                  "graduates to autonomous send", "runs the daily board sweep silently",
                  "reports a calibration digest", "Shadow mode ends when")
        for path in (EDITION / "answers-format.md", FIXTURE):
            text = path.read_text()
            self.assertIn("operator-supervised copilot", text)
            self.assertIn("does not run an automated calibration digest", text)
            self.assertIn("remains a copilot after shadow mode", text)
            self.assertIn("a human approves every external message", text)
            for phrase in banned:
                self.assertNotIn(phrase, text)

    def test_named_compliance_promises_reach_value_bound_runtime_gates(self):
        print("ARMED: A1 D2 and B8 compliance promises reach value-bound runtime gates")
        output = self.tmp / "compliance-gates"
        self.configure(output)
        parsed = engine.validate(FIXTURE, "leasing-coordinator")
        config = json.loads((output / "config.json").read_text())
        screening = (output / ".claude/skills/applicant-screening/SKILL.md").read_text()
        onboarding = (output / "ONBOARDING.md").read_text()
        lease = (output / ".claude/skills/lease-abstraction/SKILL.md").read_text()

        self.assertEqual(config["screening_criteria_established"], parsed.raw_answers["A1"])
        self.assertIn(parsed.raw_answers["A1"], screening)
        self.assertIn(parsed.raw_answers["A1"], onboarding)
        self.assertIn("PRE-SCREENING STOP", screening)
        self.assertIn("PRE-BOOT BLOCKER", onboarding)

        self.assertEqual(config["screening_visibility_policy"], parsed.raw_answers["D2"])
        self.assertIn(parsed.raw_answers["D2"], screening)
        self.assertIn("refuse and do not ingest report contents", screening)

        self.assertEqual(config["pre_1978_properties"], parsed.raw_answers["B8"])
        self.assertIn(parsed.raw_answers["B8"], lease)
        self.assertIn("LEAD-DISCLOSURE STOP", lease)

        blocked = self.fixture_variant("A1", "No. Written published criteria are not established.")
        blocked_output = self.tmp / "criteria-blocked"
        self.configure(blocked_output, answers=blocked)
        blocked_config = json.loads((blocked_output / "config.json").read_text())
        blocked_skill = (blocked_output / ".claude/skills/applicant-screening/SKILL.md").read_text()
        self.assertEqual(blocked_config["screening_criteria_established"],
                         "No. Written published criteria are not established.")
        self.assertIn("No. Written published criteria are not established.", blocked_skill)
        self.assertIn("PRE-SCREENING STOP", blocked_skill)

        summary = self.fixture_variant(
            "D2", "Summary-only policy: pass/fail flags only; report contents are prohibited."
        )
        summary_output = self.tmp / "summary-only"
        self.configure(summary_output, answers=summary)
        summary_skill = (summary_output / ".claude/skills/applicant-screening/SKILL.md").read_text()
        self.assertIn("Summary-only policy: pass/fail flags only; report contents are prohibited.",
                      summary_skill)
        self.assertIn("refuse and do not ingest report contents", summary_skill)

    def test_named_zero_touch_leasing_equals_direct_tree_and_labels_render(self):
        print("ARMED: leasing zero-touch tree digest and human question labels")
        parsed = engine.validate(FIXTURE, "leasing-coordinator")
        responses = list(parsed.raw_cover.values()) + [
            parsed.raw_answers[q] for q in engine.SUPPORTED["leasing-coordinator"]["question_ids"]
        ]
        leasing_choice = str(next(
            index for index, row in enumerate(setup.SEATS, 1)
            if row["id"] == "leasing-coordinator"
        ))
        wrapped, direct = self.tmp / "wrapped", self.tmp / "direct"
        answers = self.tmp / "guided.md"
        scripted = iter([leasing_choice, str(SOURCE), str(wrapped), "1", str(answers), *responses])
        out = io.StringIO()
        self.assertEqual(setup.run_setup(ask=lambda _p: next(scripted), out=out,
                                         clock=self.clock), 0)
        engine.configure(SOURCE, answers, direct, "leasing-coordinator",
                         clock=self.clock, seat_registry={})
        self.assertEqual(digest(wrapped), digest(direct))
        self.assertIn("Leasing Coordinator", out.getvalue())
        self.assertIn("A1. Do written, published screening criteria exist today", answers.read_text())

    def test_named_configured_output_carries_leasing_renewal_library(self):
        print("ARMED: configured leasing output carries the complete renewal library")
        output = self.tmp / "renewal-library-output"
        self.configure(output)
        expected = {
            Path("Renewal and Rent-Increase Workflow.md"):
                "A renewal signal never becomes a tenant offer until a human approves it.",
            Path("Leasing Message Template Library.md"):
                "## Renewal Offer — approval required before send",
            Path(".claude/skills/renewals-coordinator/SKILL.md"):
                "Sending a renewal offer, or any resident- or owner-facing message, is approval-gated.",
        }
        for relative, distinctive_line in expected.items():
            configured = output / relative
            self.assertTrue(configured.is_file(), f"missing renewal carrier: {relative}")
            self.assertIn(distinctive_line, configured.read_text())

    def test_named_member_census_has_no_private_identity_rows(self):
        print("ARMED: leasing member census remains fictional-only")
        forbidden = tuple(base64.b64decode(value).decode() for value in (
            "QXNjZW5kIFByb3BlcnR5IE1hbmFnZW1lbnQ=",
            "RGF2aWQgSHVudGVy",
            "ZGF2aWRAbm9vZ2FsYWJzLmNvbQ==",
        ))
        hits = []
        for path in EDITION.rglob("*"):
            if path.is_file() and "tests" not in path.parts:
                text = path.read_text(errors="ignore")
                hits.extend((path, token) for token in forbidden if token in text)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
