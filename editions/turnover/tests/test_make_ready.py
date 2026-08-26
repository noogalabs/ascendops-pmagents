from __future__ import annotations

import datetime as dt
import contextlib
import importlib.util
import io
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "editions" / "turnover" / "library-src" / ".claude" / "skills" / "make-ready-pipeline" / "make_ready.py"
SKILL = SCRIPT.with_name("SKILL.md")
SPEC = importlib.util.spec_from_file_location("turnover_make_ready", SCRIPT)
make_ready = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(make_ready)


def task(task_id, *, duration=1, depends=(), rekey=False, done=True,
         evidence="proof.jpg", stage_entered="2026-08-01", progress="",
         must_fix=True):
    return {
        "id": task_id,
        "name": task_id,
        "trade": "test",
        "stage": "3",
        "stage_entered_date": stage_entered,
        "last_progress_date": progress,
        "must_fix": must_fix,
        "duration_days": duration,
        "depends_on": list(depends),
        "verified_done": done,
        "evidence": evidence,
        "is_rekey": rekey,
    }


def scheduled(tasks):
    return make_ready.schedule_tasks(make_ready.topo_sort(tasks), dt.date(2026, 8, 1))


class MakeReadySafetyTests(unittest.TestCase):
    def test_named_certification_requires_nonblank_evidence(self):
        print("ARMED: verified work without evidence cannot certify")
        rows = scheduled([
            task("repair", evidence="   "),
            task("rekey", depends=("repair",), rekey=True),
        ])
        ok, open_items = make_ready.certify_gate(rows)
        self.assertFalse(ok)
        self.assertTrue(any("MISSING EVIDENCE must-fix" in item and "repair" in item
                            for item in open_items))

    def test_named_rekey_must_be_scheduled_after_every_required_task(self):
        print("ARMED: early re-key and work scheduled after re-key both fail certification")
        for rows in (
            [task("rekey", rekey=True), task("repair", duration=2)],
            [task("rekey", rekey=True), task("repair", duration=2, depends=("rekey",))],
        ):
            ok, open_items = make_ready.certify_gate(scheduled(rows))
            self.assertFalse(ok)
            self.assertTrue(any("RE-KEY NOT LAST" in item and "repair" in item
                                for item in open_items))

    def test_named_rekey_must_follow_cosmetic_work_too(self):
        print("ARMED: cosmetic work after re-key fails certification by name")
        rows = scheduled([
            task("rekey", rekey=True),
            task("cosmetic-touchup", depends=("rekey",), must_fix=False),
        ])
        ok, open_items = make_ready.certify_gate(rows)
        self.assertFalse(ok)
        self.assertTrue(any("RE-KEY NOT LAST" in item and "cosmetic-touchup" in item
                            for item in open_items))

    def test_named_rekey_contract_says_every_scheduled_task(self):
        print("ARMED: skill contract requires re-key after every scheduled task")
        text = SKILL.read_text()
        self.assertIn("begins only after every other scheduled task ends", text)
        self.assertNotIn("begins only after every other must-fix ends", text)

    def test_named_task_graph_rejects_empty_duplicate_and_undeclared_ids(self):
        print("ARMED: task graph validates identities and every dependency before Kahn")
        with self.assertRaisesRegex(ValueError, "nonempty"):
            make_ready.topo_sort([task("")])
        with self.assertRaisesRegex(ValueError, "Duplicate task IDs: same"):
            make_ready.topo_sort([task("same"), task("same")])
        with self.assertRaisesRegex(ValueError, "Undeclared dependency task IDs.*typo"):
            make_ready.topo_sort([task("repair", depends=("typo",))])

    def test_named_task_ids_normalize_once_through_production_scheduling(self):
        print("ARMED: padded task identities remain one canonical graph through certification")
        rows = scheduled([
            task(" repair "),
            task(" rekey ", depends=(" repair ",), rekey=True),
        ])
        self.assertEqual([row["id"] for row in rows], ["repair", "rekey"])
        self.assertEqual(rows[1]["depends_on"], ["repair"])
        self.assertEqual(rows[1]["start_date"], rows[0]["end_date"])
        ok, open_items = make_ready.certify_gate(rows)
        self.assertTrue(ok, open_items)

    def test_named_critical_path_uses_zero_slack_at_unequal_join(self):
        print("ARMED: short join branch has slack and is not reported critical")
        rows = scheduled([
            task("short", duration=1),
            task("long", duration=8),
            task("join", depends=("short", "long")),
            task("rekey", depends=("join",), rekey=True),
        ])
        critical, _ = make_ready.find_critical_path(rows)
        self.assertNotIn("short", critical)
        self.assertIn("long", critical)
        self.assertIn("join", critical)
        self.assertIn("rekey", critical)

    def test_named_stale_state_uses_configured_threshold_and_progress_anchor(self):
        print("ARMED: stale alert uses configured days and progress-or-stage-entry state")
        result = make_ready.analyze_turn(
            [task("repair", done=False, evidence="", stage_entered="2026-08-01"),
             task("rekey", depends=("repair",), rekey=True, done=False, evidence="",
                  stage_entered="2026-08-01")],
            dt.date(2026, 8, 1), 10, 4, as_of_date=dt.date(2026, 8, 6),
        )
        self.assertEqual(result["stale_stage_alert_days"], 4)
        self.assertTrue(any("no progress recorded; stage entry 2026-08-01" in row
                            and "configured threshold 4" in row for row in result["stale_flags"]))

        boundary = make_ready.analyze_turn(
            [task("repair", done=False, evidence="", stage_entered="2026-08-03"),
             task("rekey", depends=("repair",), rekey=True, done=False, evidence="",
                  stage_entered="2026-08-03")],
            dt.date(2026, 8, 1), 10, 4, as_of_date=dt.date(2026, 8, 6),
        )
        self.assertEqual(boundary["stale_flags"], [])

        fresh = make_ready.analyze_turn(
            [task("repair", done=False, evidence="", stage_entered="2026-08-01",
                  progress="2026-08-05"),
             task("rekey", depends=("repair",), rekey=True, done=False, evidence="",
                  stage_entered="2026-08-05", progress="2026-08-05")],
            dt.date(2026, 8, 1), 10, 4, as_of_date=dt.date(2026, 8, 6),
        )
        self.assertEqual(fresh["stale_flags"], [])

    def test_named_missing_stage_entry_rejects_and_module_constant_is_absent(self):
        print("ARMED: missing progress anchor fails loudly and stale constant cannot shadow config")
        with self.assertRaisesRegex(ValueError, "repair.*missing stage_entered_date"):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", stage_entered=""),
                 task("rekey", depends=("repair",), rekey=True, done=False, evidence="",
                      stage_entered="2026-08-01")],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 6),
            )
        self.assertNotIn("STALE_STAGE_ALERT_DAYS", SCRIPT.read_text())

    def test_named_future_last_progress_date_rejects_by_task_field_and_date(self):
        print("ARMED: year-typo future progress cannot flatter staleness")
        with self.assertRaisesRegex(
            ValueError,
            "repair.*future last_progress_date 2027-08-01",
        ):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", progress="2027-08-01"),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 6),
            )

    def test_named_future_stage_entry_date_rejects_by_task_field_and_date(self):
        print("ARMED: future stage entry cannot flatter staleness")
        with self.assertRaisesRegex(
            ValueError,
            "repair.*future stage_entered_date 2027-08-01",
        ):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", stage_entered="2027-08-01"),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 6),
            )

    def test_named_cli_defaults_to_configured_stale_threshold(self):
        print("ARMED: CLI reads the configured stale threshold when no flag overrides it")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.assertEqual(make_ready.main(["--demo", "--json"]), 0)
        results = json.loads(stdout.getvalue())
        self.assertTrue(results)
        self.assertEqual({row["stale_stage_alert_days"] for row in results}, {2})


if __name__ == "__main__":
    unittest.main(verbosity=2)
