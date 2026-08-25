#!/usr/bin/env python3
import importlib.util, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import engine
SPEC = importlib.util.spec_from_file_location("glue_engine_cross_seat", HERE / "cross_seat.py")
cross_seat = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cross_seat)


class CrossSeatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.current = {
            "seat": "turnover-coordinator",
            "answers": {"A1": "30 days", "C1": "$500"},
            "derived": {"threshold": "$500"},
            "configuration_engine": {"version": "1.1.0"},
        }

    def tearDown(self): shutil.rmtree(self.tmp)

    def owner(self, *, version="1.0.0", answer="30 days"):
        root = self.tmp / "maintenance-coordinator"; root.mkdir(exist_ok=True)
        (root / "seat-config.json").write_text(json.dumps({
            "seat": "maintenance-coordinator",
            "answers": {"A3": answer},
            "configuration_engine": {"version": version},
        }))
        return root

    def mapping(self):
        return {"cross_seat": {
            "pointers": [{
                "value_name": "deposit_deadline", "owner_seat": "maintenance-coordinator",
                "owner_question_id": "A3", "holding_question_id": "A1",
                "owner_value_path": "/answers/A3",
            }],
            "checks": [],
            "never_graduate": [{"gate_id": "deposit_deduction", "question_id": "C7", "reason": "human decision"}],
        }}

    def test_named_legacy_mapping_without_cross_seat_is_byte_shape_unchanged(self):
        result = cross_seat.apply(self.current, {}, {}, engine_version="1.1.0")
        self.assertEqual(result.current, self.current)

    def test_named_fact_pointer_resolves_owner_present_without_local_derived_copy(self):
        result = cross_seat.apply(
            self.current, self.mapping(), {"maintenance-coordinator": self.owner()},
            engine_version="1.1.0",
        )
        pointer = result.current["cross_seat"]["pointers"]["deposit_deadline"]
        self.assertEqual(pointer["owner_question_id"], "A3")
        self.assertNotIn("deposit_deadline", result.current["cross_seat"]["held"])
        self.assertNotIn("value", pointer)

    def test_named_fact_pointer_owner_absent_holds_once_and_names_pending_owner(self):
        result = cross_seat.apply(self.current, self.mapping(), {}, engine_version="1.1.0")
        held = result.current["cross_seat"]["held"]["deposit_deadline"]
        self.assertEqual(held["held_pending_seat"], "maintenance-coordinator")
        self.assertEqual(held["value"], "30 days")
        self.assertNotIn("deposit_deadline", result.current["cross_seat"]["pointers"])

    def test_named_policy_disagreement_surfaces_eyeball_and_never_unifies(self):
        owner = self.owner(); payload = json.loads((owner / "seat-config.json").read_text())
        payload["derived"] = {"threshold": "$450"}
        (owner / "seat-config.json").write_text(json.dumps(payload))
        mapping = {"cross_seat": {
            "pointers": [], "never_graduate": [],
            "checks": [{
                "check_id": "approval-policy", "doctrine": "POLICY",
                "local_ref": "/derived/threshold", "peer_seat": "maintenance-coordinator",
                "peer_ref": "/derived/threshold",
            }],
        }}
        result = cross_seat.apply(
            self.current, mapping, {"maintenance-coordinator": owner}, engine_version="1.1.0"
        )
        self.assertEqual(result.current["derived"]["threshold"], "$500")
        self.assertEqual(payload["derived"]["threshold"], "$450")
        self.assertEqual(result.report_items[0]["status"], "EYEBALL")
        report = cross_seat.render_report_block(result.report_items)
        self.assertIn("no auto-unification", report)

    def test_named_new_engine_reads_legacy_but_rejects_newer_owner(self):
        result = cross_seat.apply(
            self.current, self.mapping(), {"maintenance-coordinator": self.owner(version="1.0.0")},
            engine_version="1.10.0",
        )
        self.assertEqual(result.current["cross_seat"]["pointers"]["deposit_deadline"]["state"], "resolved")
        with self.assertRaises(cross_seat.CrossSeatRejected) as caught:
            cross_seat.apply(
                self.current, self.mapping(), {"maintenance-coordinator": self.owner(version="2.0.0")},
                engine_version="1.10.0",
            )
        self.assertIn("newer than reader", str(caught.exception.failures))

    def append_mapping(self):
        return {"cross_seat": {"pointers": [], "checks": [], "appends": [{
            "value_name": "vendor_roster", "owner_seat": "maintenance-coordinator",
            "owner_question_id": "C5", "appender_question_id": "D4",
            "value_path": "/answers/D4", "owner_target_path": "/derived/roster/vendors",
        }]}}

    def append_configs(self):
        current = {**self.current, "answers": {**self.current["answers"], "D4": "Mesa Vendor"}}
        planned = cross_seat.apply(current, self.append_mapping(), {}, engine_version="1.1.0").current
        owner = {
            "seat": "maintenance-coordinator",
            "derived": {"roster": {"vendors": ["Base Vendor"]}},
            "configuration_engine": {"version": "1.0.0"},
        }
        plan_id = next(iter(planned["cross_seat"]["append_plans"]))
        return planned, owner, plan_id

    def test_named_crash_between_transactions_leaves_replayable_plan_and_zero_owner_write(self):
        planned, owner, plan_id = self.append_configs()
        before = json.dumps(owner, sort_keys=True)
        pending = cross_seat.pending_append_plans(planned, owner)
        self.assertEqual(pending[0]["plan_id"], plan_id)
        self.assertEqual(json.dumps(owner, sort_keys=True), before)
        self.assertNotIn("roster", planned.get("derived", {}))

    def test_named_append_not_fork_and_double_apply_is_noop_by_plan_id(self):
        planned, owner, plan_id = self.append_configs()
        updated, changed = cross_seat.apply_append_plan(
            owner, planned, plan_id, engine_version="1.1.0"
        )
        self.assertTrue(changed)
        self.assertEqual(updated["derived"]["roster"]["vendors"], ["Base Vendor", "Mesa Vendor"])
        self.assertIn(plan_id, planned["cross_seat"]["append_plans"])
        self.assertIn(plan_id, updated["cross_seat"]["appends"])
        replayed, changed = cross_seat.apply_append_plan(
            updated, planned, plan_id, engine_version="1.1.0"
        )
        self.assertFalse(changed)
        self.assertEqual(replayed, updated)
        self.assertEqual(cross_seat.pending_append_plans(planned, updated), [])

    def test_named_first_class_append_operation_atomically_updates_owner_only(self):
        planned, owner, plan_id = self.append_configs()
        appender_dir = self.tmp / "turnover-coordinator"; appender_dir.mkdir()
        owner_dir = self.tmp / "owner"; owner_dir.mkdir()
        (appender_dir / "seat-config.json").write_text(json.dumps(planned))
        (owner_dir / "seat-config.json").write_text(json.dumps(owner))
        (owner_dir / "organic.txt").write_text("unchanged")
        self.assertTrue(engine.apply_persisted_append(appender_dir, owner_dir, plan_id))
        applied = json.loads((owner_dir / "seat-config.json").read_text())
        self.assertEqual(applied["derived"]["roster"]["vendors"], ["Base Vendor", "Mesa Vendor"])
        self.assertEqual((owner_dir / "organic.txt").read_text(), "unchanged")
        self.assertFalse(engine.apply_persisted_append(appender_dir, owner_dir, plan_id))

    def test_named_legacy_engine_rejects_v2_compatibility_guard(self):
        legacy_path = self.tmp / "legacy_placeholders.py"
        legacy_path.write_bytes(
            (HERE / "tests" / "fixtures" / "e2" / "legacy-placeholders-v1.py").read_bytes()
        )
        spec = importlib.util.spec_from_file_location("legacy_placeholders", legacy_path)
        legacy = importlib.util.module_from_spec(spec); sys.modules[spec.name] = legacy
        spec.loader.exec_module(legacy)
        root = self.tmp / "legacy-root"; root.mkdir()
        (root / "seat-config.json").write_text("{}")
        guard = cross_seat.compatibility_guard("1.1.0")
        with self.assertRaises(legacy.PlaceholderRejected) as caught:
            legacy.apply_rerun(root, {"placeholders": [{
                "placeholder": "company_name", "source": "cover.company_name",
                "extractor": "identity",
            }]}, {}, {}, object(), [guard])
        self.assertIn(cross_seat.COMPATIBILITY_PLACEHOLDER, str(caught.exception.failures))

    def test_named_current_engine_rejects_future_compatibility_guard(self):
        with self.assertRaises(cross_seat.CrossSeatRejected) as caught:
            cross_seat.validate_compatibility_guards(
                [cross_seat.compatibility_guard("2.0.0")], "1.10.0"
            )
        self.assertIn("requires engine 2.0.0", str(caught.exception.failures))


if __name__ == "__main__":
    print("ARMED: graduated cross-seat pointers, holding, checks, and version directionality")
    unittest.main(verbosity=2)
