from __future__ import annotations

import ast
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

    def test_named_zero_task_id_and_dependency_survive_end_to_end(self):
        print("ARMED: numeric zero is a present task identity, never a missing value")
        rows = scheduled([
            task(0),
            task(1, depends=(0,), rekey=True),
        ])
        self.assertEqual([row["id"] for row in rows], ["0", "1"])
        self.assertEqual(rows[1]["depends_on"], ["0"])
        self.assertEqual(rows[1]["start_date"], rows[0]["end_date"])
        ok, open_items = make_ready.certify_gate(rows)
        self.assertTrue(ok, open_items)

    def test_named_present_scalar_dependency_list_rejects_loudly(self):
        print("ARMED: a present scalar depends_on cannot disappear or iterate as characters")
        row = task("child")
        row["depends_on"] = "parent"
        with self.assertRaisesRegex(ValueError, "child.*invalid depends_on: 'parent'"):
            make_ready.topo_sort([task("parent"), row])

    def test_named_falsy_present_values_never_coalesce_to_absent(self):
        print("ARMED: zero and False survive None-only coalescing")
        self.assertEqual(make_ready.none_coalesce(0, "missing"), 0)
        self.assertIs(make_ready.none_coalesce(False, "missing"), False)
        with self.assertRaisesRegex(ValueError, r"repair.*invalid last_progress_date: '0'"):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", progress=0),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 6),
            )

    def test_named_user_input_gets_have_no_falsy_or_coalescing(self):
        print("ARMED: user-input .get values cannot regain value-or-default conflation")
        tree = ast.parse(SCRIPT.read_text())
        found = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.BoolOp) or not isinstance(node.op, ast.Or):
                continue
            if any(
                isinstance(candidate, ast.Call)
                and isinstance(candidate.func, ast.Attribute)
                and candidate.func.attr == "get"
                for candidate in ast.walk(node)
            ):
                found.append(ast.unparse(node))
        self.assertEqual(
            found,
            ["required['id'] == r['id'] or required.get('is_rekey')"],
            "Only the reviewed logical re-key self/exclusion predicate may use .get() under or",
        )

    def test_named_negative_duration_after_rekey_rejects_before_certification(self):
        print("ARMED: negative post-rekey duration rejects before timeline certification")
        with self.assertRaisesRegex(ValueError, "cosmetic.*nonpositive duration_days: -1"):
            scheduled([
                task("rekey", rekey=True),
                task("cosmetic", duration=-1, depends=("rekey",), must_fix=False),
            ])

    def test_named_zero_duration_rejects_by_task_and_field(self):
        print("ARMED: zero duration cannot flatten scheduled work")
        with self.assertRaisesRegex(ValueError, "repair.*nonpositive duration_days: 0"):
            scheduled([task("repair", duration=0)])

    def test_named_malformed_duration_rejects_instead_of_defaulting(self):
        print("ARMED: present malformed duration cannot masquerade as the default")
        with self.assertRaisesRegex(ValueError, r"repair.*invalid duration_days: 'two'"):
            scheduled([task("repair", duration="two")])

    def test_named_absent_duration_preserves_one_day_default(self):
        print("ARMED: genuinely absent duration keeps the documented one-day default")
        row = task("repair")
        row.pop("duration_days")
        result = scheduled([row])
        self.assertEqual(result[0]["duration_days"], 1)
        self.assertEqual(result[0]["end_date"], "2026-08-02")

    def test_named_cpm_consumes_canonical_duration_without_reparse(self):
        print("ARMED: scheduler canonicalizes duration once and CPM consumes that integer")
        rows = scheduled([
            task("repair", duration=" 2 "),
            task("rekey", depends=("repair",), rekey=True),
        ])
        self.assertEqual(rows[0]["duration_days"], 2)
        self.assertIs(type(rows[0]["duration_days"]), int)
        _, finish = make_ready.find_critical_path(rows)
        self.assertEqual(finish, dt.date(2026, 8, 4))

        tree = ast.parse(SCRIPT.read_text())
        find_cpm = next(node for node in ast.walk(tree)
                        if isinstance(node, ast.FunctionDef)
                        and node.name == "find_critical_path")
        reparses = [node for node in ast.walk(find_cpm)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "parse_int"]
        self.assertEqual(reparses, [])

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

    def test_named_malformed_task_dates_reject_distinct_from_absence(self):
        print("ARMED: malformed task dates cannot masquerade as absent optional state")
        with self.assertRaisesRegex(
            ValueError,
            r"repair.*invalid last_progress_date: '2026/08/25'",
        ):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", progress="2026/08/25"),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 26),
            )
        with self.assertRaisesRegex(
            ValueError,
            r"repair.*invalid stage_entered_date: '2026/08/25'",
        ):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", stage_entered="2026/08/25"),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 26),
            )
        with self.assertRaisesRegex(ValueError, "repair.*missing stage_entered_date"):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", stage_entered=""),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 26),
            )

    def test_named_certification_dates_never_skip_malformed_values(self):
        print("ARMED: malformed certification dates reject instead of skipping finality")
        rows = scheduled([task("repair"), task("rekey", depends=("repair",), rekey=True)])
        rows[0]["end_date"] = "2026/08/25"
        with self.assertRaisesRegex(ValueError, r"repair.*invalid end_date: '2026/08/25'"):
            make_ready.certify_gate(rows)

    def test_named_every_parse_date_consumer_is_strict_or_pinned_loud(self):
        print("ARMED: every parse_date consumer has an explicit absent/malformed policy")
        tree = ast.parse(SCRIPT.read_text())
        direct_calls = {}
        for function in [node for node in ast.walk(tree)
                         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            count = sum(
                1 for node in ast.walk(function)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "parse_date"
            )
            if count:
                direct_calls[function.name] = count
        self.assertEqual(
            direct_calls,
            {"strict_task_date": 1, "find_critical_path": 2, "main": 1},
        )

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

    def test_named_progress_before_stage_entry_rejects_both_fields_and_dates(self):
        print("ARMED: prior-stage progress cannot silently age the current stage")
        with self.assertRaisesRegex(
            ValueError,
            "repair.*last_progress_date 2026-08-01 before stage_entered_date 2026-08-25",
        ):
            make_ready.analyze_turn(
                [task("repair", done=False, evidence="", stage_entered="2026-08-25",
                      progress="2026-08-01"),
                 task("rekey", depends=("repair",), rekey=True)],
                dt.date(2026, 8, 1), 10, 2, as_of_date=dt.date(2026, 8, 26),
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
