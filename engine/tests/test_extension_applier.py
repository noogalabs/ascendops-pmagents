#!/usr/bin/env python3
import hashlib, importlib.util, json, shutil, tempfile, unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parent
SPEC = importlib.util.spec_from_file_location("glue_engine_extension", HERE / "engine.py")
engine = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(engine)
DEMO = REPO / "editions" / "maintenance"
FIXTURE = DEMO / "fixtures" / "ridgeline-maintenance-answers.md"
META = HERE / "tests" / "fixtures" / "e2" / "maintenance-v2-golden.json"
ADD_AGENT_ROWS = {
    "agent_name": "ridge-maint",
    "org": "ridgeline",
    "current_timestamp": "2026-08-25T00:00:00Z",
    "upstream_update_minute": "17",
}


def prepare_raw(source):
    shutil.copytree(HERE / "tests" / "fixtures" / "raw-maintenance-template", source, symlinks=True)
    for path in source.rglob("*"):
        if not path.is_file() or path.is_symlink(): continue
        try: text = path.read_text()
        except UnicodeDecodeError: continue
        for name, value in ADD_AGENT_ROWS.items(): text = text.replace("{{" + name + "}}", value)
        path.write_text(text)


def manifest_bytes(root):
    rows = []
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root)}\n")
    return "".join(rows).encode()


class ExtensionApplierTests(unittest.TestCase):
    def setUp(self): self.tmp = Path(tempfile.mkdtemp(prefix="betty-e2-"))
    def tearDown(self): shutil.rmtree(self.tmp)

    def test_named_schema_v2_requires_exact_timezone_config_key(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["config_keys"] = [row for row in mapping["config_keys"] if row["path"] != "/timezone"]
        path = self.tmp / "mapping.json"; path.write_text(json.dumps(mapping))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("schema v2+ requires exactly one timezone", str(caught.exception.failures))

    def test_named_v2_timezone_k_row_writes_denver_and_matches_extension_golden(self):
        outputs = []
        for number in (1, 2):
            source = self.tmp / f"source-{number}"; output = self.tmp / f"output-{number}"
            prepare_raw(source)
            engine.configure(source, FIXTURE, output, "maintenance-coordinator", clock=lambda: date(2026, 8, 25))
            outputs.append(output)
        self.assertEqual(manifest_bytes(outputs[0]), manifest_bytes(outputs[1]))
        config = json.loads((outputs[0] / "config.json").read_text())
        self.assertEqual(config["timezone"], "America/Denver")
        seat = json.loads((outputs[0] / "seat-config.json").read_text())
        rows = [row for row in seat["configuration_engine"]["managed_surfaces"]
                if row.get("row_type") == "config_key"]
        self.assertEqual(rows, [{
            "row_type": "config_key", "config_path": "/timezone",
            "question_id": "cover.timezone", "file": "config.json#/timezone",
            "count": 1, "value": "America/Denver",
        }])
        metadata = json.loads(META.read_text())
        actual = manifest_bytes(outputs[0])
        self.assertEqual(len(actual.splitlines()), metadata["file_count"])
        self.assertEqual(hashlib.sha256(actual).hexdigest(), metadata["tree_manifest_sha256"])
        self.assertEqual(metadata["runs"], ["e2-maintenance-v2-1", "e2-maintenance-v2-2"])

    def test_named_cross_seat_wrapper_persists_holding_plan_pending_report_and_guard_deterministically(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["cross_seat"] = {
            "pointers": [{
                "value_name": "deposit_deadline", "owner_seat": "leasing",
                "owner_question_id": "B1", "holding_question_id": "A3",
                "owner_value_path": "/answers/B1",
            }],
            "checks": [],
            "appends": [{
                "value_name": "vendor_roster", "owner_seat": "turnover-coordinator",
                "owner_question_id": "D4", "appender_question_id": "C5",
                "value_path": "/answers/C5", "owner_target_path": "/derived/roster/vendors",
            }],
            "never_graduate": [{
                "gate_id": "vendor_pricing", "question_id": "C5", "reason": "human approval",
            }],
        }
        mapping_path = self.tmp / "mapping-v2-seams.json"
        mapping_path.write_text(json.dumps(mapping))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = mapping_path
        try:
            outputs = []
            for number in (1, 2):
                source = self.tmp / f"seam-source-{number}"; output = self.tmp / f"seam-output-{number}"
                prepare_raw(source)
                engine.configure(
                    source, FIXTURE, output, "maintenance-coordinator",
                    clock=lambda: date(2026, 8, 25), seat_registry={},
                )
                outputs.append(output)
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original
        self.assertEqual(manifest_bytes(outputs[0]), manifest_bytes(outputs[1]))
        seat = json.loads((outputs[0] / "seat-config.json").read_text())
        held = seat["cross_seat"]["held"]["deposit_deadline"]
        self.assertEqual(held["held_pending_seat"], "leasing")
        plans = seat["cross_seat"]["append_plans"]
        self.assertEqual(len(plans), 1)
        self.assertIn("PENDING", (outputs[0] / "contradiction-report.md").read_text())
        guards = [row for row in seat["configuration_engine"]["managed_surfaces"]
                  if row.get("row_type") == "compatibility_guard"]
        self.assertEqual(len(guards), 1)

    def test_named_pointer_k_row_production_path_owner_fallback_and_missing_fallback(self):
        base = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        base["cross_seat"] = {"pointers": [{
            "value_name": "org_timezone", "owner_seat": "leasing",
            "owner_question_id": "B8", "holding_question_id": "A3",
            "owner_value_path": "/answers/B8",
        }]}
        base["config_keys"] = [{
            "path": "/timezone", "value_from": "pointer", "pointer_name": "org_timezone",
            "fallback": "America/Denver", "value_type": "string", "mode": "replace",
        }]
        owner = self.tmp / "leasing"; owner.mkdir()
        (owner / "seat-config.json").write_text(json.dumps({
            "seat": "leasing", "answers": {"B8": "America/Chicago"},
        }))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        try:
            mapping = self.tmp / "pointer-mapping.json"; mapping.write_text(json.dumps(base))
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = mapping
            source = self.tmp / "pointer-source"; prepare_raw(source)
            owner_output = self.tmp / "pointer-owner-output"
            engine.configure(source, FIXTURE, owner_output, "maintenance-coordinator",
                             seat_registry={"leasing": owner})
            self.assertEqual(json.loads((owner_output / "config.json").read_text())["timezone"],
                             "America/Chicago")
            owner_manifest = json.loads((owner_output / "seat-config.json").read_text())[
                "configuration_engine"]["managed_surfaces"]
            self.assertEqual([row for row in owner_manifest if row.get("question_id") == "pointer:org_timezone"][0]["resolution"],
                             "owner")

            source = self.tmp / "pointer-fallback-source"; prepare_raw(source)
            fallback_output = self.tmp / "pointer-fallback-output"
            engine.configure(source, FIXTURE, fallback_output, "maintenance-coordinator",
                             seat_registry={})
            self.assertEqual(json.loads((fallback_output / "config.json").read_text())["timezone"],
                             "America/Denver")
            fallback_manifest = json.loads((fallback_output / "seat-config.json").read_text())[
                "configuration_engine"]["managed_surfaces"]
            self.assertEqual([row for row in fallback_manifest if row.get("question_id") == "pointer:org_timezone"][0]["resolution"],
                             "held_fallback")

            del base["config_keys"][0]["fallback"]
            mapping.write_text(json.dumps(base))
            source = self.tmp / "pointer-reject-source"; prepare_raw(source)
            rejected = self.tmp / "pointer-rejected-output"
            with self.assertRaises(engine.IntakeRejected):
                engine.configure(source, FIXTURE, rejected, "maintenance-coordinator",
                                 seat_registry={})
            self.assertFalse(rejected.exists())
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original

    def test_named_declared_structured_filename_materializes_through_production_configure(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["structured_answers_file"] = "accounting-config.json"
        path = self.tmp / "declared-artifact-mapping.json"; path.write_text(json.dumps(mapping))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = path
        try:
            source = self.tmp / "declared-artifact-source"; prepare_raw(source)
            output = self.tmp / "declared-artifact-output"
            engine.configure(source, FIXTURE, output, "maintenance-coordinator")
            self.assertTrue((output / "accounting-config.json").is_file())
            self.assertFalse((output / "seat-config.json").exists())
            payload = json.loads((output / "accounting-config.json").read_text())
            self.assertEqual(payload["configuration_engine"]["version"], engine.ENGINE_VERSION)
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original

    def test_named_custom_declared_filename_create_then_reconfigure_uses_fresh_core_output(self):
        print("ARMED: custom declared filename create-then-reconfigure uses fresh core output")
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["structured_answers_file"] = "accounting-config.json"
        path = self.tmp / "sequential-declared-artifact-mapping.json"
        path.write_text(json.dumps(mapping))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = path
        try:
            source = self.tmp / "sequential-declared-artifact-source"; prepare_raw(source)
            output = self.tmp / "sequential-declared-artifact-output"
            engine.configure(source, FIXTURE, output, "maintenance-coordinator")
            declared = output / "accounting-config.json"
            stale = json.loads(declared.read_text())
            stale["stale_source_marker"] = True
            declared.write_text(json.dumps(stale, indent=2) + "\n")

            engine.configure(output, FIXTURE, output, "maintenance-coordinator")

            fresh = json.loads(declared.read_text())
            self.assertNotIn("stale_source_marker", fresh)
            self.assertEqual(fresh["configuration_engine"]["version"], engine.ENGINE_VERSION)
            self.assertFalse((output / "seat-config.json").exists())
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original

    def test_named_pointer_config_rerun_uses_production_resolver_deterministically(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["cross_seat"] = {"pointers": [{
            "value_name": "org_timezone", "owner_seat": "leasing",
            "owner_question_id": "B8", "holding_question_id": "A3",
            "owner_value_path": "/answers/B8",
        }]}
        mapping["config_keys"] = [{
            "path": "/timezone", "value_from": "pointer", "pointer_name": "org_timezone",
            "fallback": "America/Denver", "value_type": "string", "mode": "replace",
        }]
        mapping_path = self.tmp / "rerun-pointer-mapping.json"
        mapping_path.write_text(json.dumps(mapping))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = mapping_path
        try:
            outputs = []
            for number in (1, 2):
                source = self.tmp / f"rerun-pointer-source-{number}"
                output = self.tmp / f"rerun-pointer-output-{number}"
                prepare_raw(source)
                engine.configure(source, FIXTURE, output, "maintenance-coordinator", seat_registry={})
                engine.configure(output, FIXTURE, output, "maintenance-coordinator", seat_registry={})
                outputs.append(output)
            self.assertEqual(manifest_bytes(outputs[0]), manifest_bytes(outputs[1]))
            self.assertEqual(json.loads((outputs[0] / "config.json").read_text())["timezone"],
                             "America/Denver")
            managed = json.loads((outputs[0] / "seat-config.json").read_text())["configuration_engine"]["managed_surfaces"]
            pointer_rows = [row for row in managed if row.get("question_id") == "pointer:org_timezone"]
            self.assertEqual(len(pointer_rows), 1)
            self.assertEqual(pointer_rows[0]["resolution"], "held_fallback")
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original

    def test_named_pointer_config_replace_absent_rejects_and_declared_create_creates(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["cross_seat"] = {"pointers": [{
            "value_name": "org_timezone", "owner_seat": "leasing",
            "owner_question_id": "B8", "holding_question_id": "A3",
            "owner_value_path": "/answers/B8",
        }]}
        row = {
            "path": "/pointer_only", "value_from": "pointer", "pointer_name": "org_timezone",
            "fallback": "America/Denver", "value_type": "string", "mode": "replace",
        }
        mapping["config_keys"].append(row)
        mapping_path = self.tmp / "commit-mode-mapping.json"
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = mapping_path
        try:
            replace_source = self.tmp / "replace-absent-source"; prepare_raw(replace_source)
            mapping_path.write_text(json.dumps(mapping))
            rejected = self.tmp / "replace-absent-output"
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(replace_source, FIXTURE, rejected, "maintenance-coordinator", seat_registry={})
            self.assertIn("declared replace target is absent", caught.exception.render())
            self.assertFalse(rejected.exists())

            create_source = self.tmp / "declared-create-source"; prepare_raw(create_source)
            mapping["config_keys"][-1]["mode"] = "create"
            mapping_path.write_text(json.dumps(mapping))
            created = self.tmp / "declared-create-output"
            engine.configure(create_source, FIXTURE, created, "maintenance-coordinator", seat_registry={})
            self.assertEqual(json.loads((created / "config.json").read_text())["pointer_only"],
                             "America/Denver")
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original

    def test_named_uncoercible_pointer_value_is_a_structured_row_rejection(self):
        mapping = json.loads(engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text())
        mapping["cross_seat"] = {"pointers": [{
            "value_name": "turn_target", "owner_seat": "leasing",
            "owner_question_id": "B1", "holding_question_id": "A3",
            "owner_value_path": "/answers/B1",
        }]}
        mapping["config_keys"].append({
            "path": "/turn_target_days", "value_from": "pointer",
            "pointer_name": "turn_target", "fallback": "not-an-integer",
            "value_type": "integer", "mode": "replace",
        })
        mapping_path = self.tmp / "uncoercible-pointer-mapping.json"
        mapping_path.write_text(json.dumps(mapping))
        original = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = mapping_path
        try:
            source = self.tmp / "uncoercible-pointer-source"; prepare_raw(source)
            output = self.tmp / "uncoercible-pointer-output"
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(source, FIXTURE, output, "maintenance-coordinator", seat_registry={})
            rendered = caught.exception.render()
            self.assertIn("mapping.config_keys./turn_target_days", rendered)
            self.assertIn("pointer value coercion failed", rendered)
            self.assertFalse(output.exists())
        finally:
            engine.SUPPORTED["maintenance-coordinator"]["mapping"] = original


if __name__ == "__main__":
    print("ARMED: schema-v2 timezone sourcing and deterministic extension golden")
    unittest.main(verbosity=2)
