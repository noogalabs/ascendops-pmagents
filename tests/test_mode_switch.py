#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
import autonomy  # noqa: E402


SKILL_SOURCES = (
    ROOT / "templates" / "maintenance-coordinator",
    ROOT / "editions" / "pm-assist" / "library-src",
    ROOT / "editions" / "leasing" / "library-src",
    ROOT / "editions" / "turnover" / "library-src",
    ROOT / "editions" / "accounting" / "library-src",
    ROOT / "editions" / "business-development" / "library-src",
)


class ModeSwitchCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="pmagents-mode-switch-"))
        self.seat = self.temp / "maintenance"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.seat)
        autonomy.render(self.seat, autonomy.parse_settings({
            "autonomy_mode": "copilot",
            "unlock_window": "last_3",
            "qualifying_accuracy": "90",
            "external_send_autonomy": "no",
            "work_order_closure_autonomy": "no",
        }), "2026-09-05T12:00:00Z")

    def tearDown(self):
        shutil.rmtree(self.temp)

    def run_cli(self, mode: str, *extra: str):
        return subprocess.run(
            [sys.executable, str(ROOT / "setup.py"), "--set-mode", str(self.seat), mode, *extra],
            cwd=ROOT, capture_output=True, text=True,
        )

    def state(self):
        return json.loads((self.seat / "copilot-thresholds.json").read_text())

    def test_production_cli_reads_back_opt_ins_writes_audit_and_preserves_member_state(self):
        print("ARMED: setup.py --set-mode is the one-step production entry and never touches memory/tasks")
        (self.seat / "memory").mkdir()
        (self.seat / "memory" / "2026-09-05.md").write_text("member memory\n")
        (self.seat / "tasks").mkdir()
        (self.seat / "tasks" / "open.json").write_text('{"member":true}\n')
        (self.seat / ".env").write_text("MEMBER_SECRET=unchanged\n")
        protected = {
            "memory": (self.seat / "memory" / "2026-09-05.md").read_bytes(),
            "tasks": (self.seat / "tasks" / "open.json").read_bytes(),
            "env": (self.seat / ".env").read_bytes(),
        }

        result = self.run_cli(
            "full", "--external-send-autonomy", "yes",
            "--work-order-closure-autonomy", "yes",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(
            {key: summary[key] for key in (
                "previous_mode", "autonomy_mode", "external_send_autonomy",
                "work_order_closure_autonomy",
            )},
            {"previous_mode": "copilot", "autonomy_mode": "full",
             "external_send_autonomy": True, "work_order_closure_autonomy": True},
        )
        self.assertEqual((self.seat / "memory" / "2026-09-05.md").read_bytes(), protected["memory"])
        self.assertEqual((self.seat / "tasks" / "open.json").read_bytes(), protected["tasks"])
        self.assertEqual((self.seat / ".env").read_bytes(), protected["env"])
        audit_rows = (self.seat / "logs" / "autonomy-mode-audit.jsonl").read_text().splitlines()
        self.assertEqual(len(audit_rows), 1)
        self.assertEqual(json.loads(audit_rows[0])["autonomy_mode"], "full")

    def test_cli_downgrade_relocks_and_preserves_earned_history_and_opt_ins(self):
        print("ARMED: full-to-copilot CLI downgrade re-locks while preserving history and omitted choices")
        first = self.run_cli(
            "full", "--external-send-autonomy", "yes",
            "--work-order-closure-autonomy", "yes",
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        state = self.state()
        row = state["categories"]["lock_change"]
        row.update(total_decisions=3, correct=3, recent_outcomes=[True, True, True],
                   accuracy_pct=100.0, unlocked_at="2026-09-05T12:30:00Z")
        (self.seat / "copilot-thresholds.json").write_text(json.dumps(state, indent=2) + "\n")

        result = self.run_cli("copilot")
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertTrue(summary["external_send_autonomy"])
        self.assertTrue(summary["work_order_closure_autonomy"])
        row = self.state()["categories"]["lock_change"]
        self.assertEqual(row["status"], "locked")
        self.assertEqual(row["recent_outcomes"], [True, True, True])
        self.assertEqual(row["total_decisions"], 3)
        self.assertEqual(row["unlocked_at"], "2026-09-05T12:30:00Z")
        self.assertEqual(
            len((self.seat / "logs" / "autonomy-mode-audit.jsonl").read_text().splitlines()), 2
        )

    def test_cli_refuses_unknown_mode_without_writing(self):
        before = (self.seat / "copilot-thresholds.json").read_bytes()
        result = self.run_cli("automatic")
        self.assertEqual(result.returncode, 2)
        self.assertIn("mode must be exactly one of", result.stderr)
        self.assertEqual((self.seat / "copilot-thresholds.json").read_bytes(), before)
        self.assertFalse((self.seat / "logs" / "autonomy-mode-audit.jsonl").exists())

    def test_renderer_failure_leaves_the_installed_agent_byte_unchanged(self):
        print("ARMED: a mode-render failure cannot partially change the installed seat")
        before = {
            str(path.relative_to(self.seat)): path.read_bytes()
            for path in self.seat.rglob("*") if path.is_file()
        }

        def refuse(candidate, settings, timestamp):
            (candidate / "GUARDRAILS.md").write_text("partial candidate\n")
            raise ValueError("injected mode renderer failure")

        with mock.patch.object(autonomy, "render", side_effect=refuse):
            with self.assertRaisesRegex(ValueError, "injected mode renderer failure"):
                autonomy.set_mode(self.seat, "full")
        after = {
            str(path.relative_to(self.seat)): path.read_bytes()
            for path in self.seat.rglob("*") if path.is_file()
        }
        self.assertEqual(after, before)
        self.assertEqual(list(self.temp.glob(".maintenance.mode-candidate-*")), [])

    def test_no_threshold_edition_switches_from_engine_doctrine_fail_closed(self):
        print("ARMED: editions without threshold ledgers preserve explicit choices from engine doctrine")
        root = self.temp / "leasing"
        shutil.copytree(ROOT / "editions" / "leasing" / "library-src", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot",
            "external_send_autonomy": "yes",
            "work_order_closure_autonomy": "no",
        }), "2026-09-05T12:00:00Z")
        self.seat = root
        result = self.run_cli("supervised")
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["autonomy_mode"], "supervised")
        self.assertTrue(summary["external_send_autonomy"])
        self.assertFalse(summary["work_order_closure_autonomy"])


class ShippedSkillTests(unittest.TestCase):
    def test_every_edition_ships_identical_owner_word_mode_switch_skill(self):
        print("ARMED: every edition ships one owner-word-only autonomy switch skill")
        bodies = []
        for source in SKILL_SOURCES:
            path = source / ".claude" / "skills" / "autonomy-mode-switch" / "SKILL.md"
            self.assertTrue(path.is_file(), source)
            text = path.read_text()
            bodies.append(text)
            self.assertIn("only when the owner explicitly instructs", text)
            self.assertIn("--set-mode", text)
            self.assertIn("autonomy-mode-audit.jsonl", text)
            self.assertIn("Never patch", text)
        self.assertTrue(all(body == bodies[0] for body in bodies[1:]))


if __name__ == "__main__":
    unittest.main()
