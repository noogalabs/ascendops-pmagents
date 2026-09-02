#!/usr/bin/env python3
import importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("glue_engine_placeholders", HERE / "engine.py")
engine = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(engine)


class PlaceholderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); self.root = self.tmp / "root"; self.root.mkdir()
        self.core = engine.load_core()
        self.cover = {"timezone":"America/Denver","company_name":"Ridgeline","org_short_name":"ridge","forward_email":"x@example.test"}
        self.answers = {"B1":"$450 base threshold", "B5":"Emergency dispatch 90 minutes", "C1":"Morgan Vale, Supervisor", "D1":"WorkTrail for maintenance", "B8":"08:00-20:00"}
    def tearDown(self): shutil.rmtree(self.tmp)

    def mapping(self, *rows): return {"placeholders": list(rows)}

    def test_named_unknown_template_placeholder_rejects_by_file(self):
        (self.root / "IDENTITY.md").write_text("Hello {{unknown_surface}}")
        mapping = self.mapping({"placeholder":"company_name","source":"cover.company_name","extractor":"identity"})
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        self.assertIn("template.IDENTITY.md", str(caught.exception.failures))

    def test_named_exact_ctx_root_runtime_token_is_preserved_and_recorded(self):
        path = self.root / "ONBOARDING.md"; original = "path={{CTX_ROOT}}/state\n"; path.write_text(original)
        records = engine.placeholders.preserved_runtime_manifest(self.root)
        self.assertEqual(records, [{"token":"{{CTX_ROOT}}", "file":"ONBOARDING.md", "count":1}])
        engine.placeholders.verify_preserved_runtime_tokens(self.root, records)
        self.assertEqual(path.read_text(), original)

    def test_named_nearby_runtime_token_is_not_allowlisted(self):
        (self.root / "ONBOARDING.md").write_text("path={{CTX_HOME}}/state\n")
        mapping = self.mapping({"placeholder":"company_name","source":"cover.company_name","extractor":"identity"})
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        self.assertIn("CTX_HOME", str(caught.exception.failures))

    def test_named_mapping_row_missing_from_template_rejects_by_row(self):
        (self.root / "IDENTITY.md").write_text("no tokens")
        mapping = self.mapping({"placeholder":"company_name","source":"cover.company_name","extractor":"identity"})
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        self.assertIn("mapping.company_name", str(caught.exception.failures))

    def test_named_skill_p_row_substitutes_and_manifests_exact_site(self):
        skill = self.root / ".claude" / "skills" / "make-ready-pipeline" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("Target: {{company_name}}\n")
        mapping = self.mapping({
            "placeholder": "company_name",
            "source": "cover.company_name",
            "extractor": "identity",
            "sites": [{"file": ".claude/skills/make-ready-pipeline/SKILL.md", "count": 1}],
        })
        manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, self.answers, self.core
        )
        self.assertIn("BETTY-PH:company_name -->Ridgeline", skill.read_text())
        self.assertEqual(manifest[0]["file"], ".claude/skills/make-ready-pipeline/SKILL.md")

    def test_named_declared_skill_site_missing_rejects_even_when_token_exists_elsewhere(self):
        path = self.root / "IDENTITY.md"
        path.write_text("Company: {{company_name}}\n")
        before = path.read_bytes()
        mapping = self.mapping({
            "placeholder": "company_name",
            "source": "cover.company_name",
            "extractor": "identity",
            "sites": [{"file": ".claude/skills/make-ready-pipeline/SKILL.md", "count": 1}],
        })
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, self.answers, self.core
            )
        self.assertIn("make-ready-pipeline/SKILL.md", str(caught.exception.failures))
        self.assertEqual(path.read_bytes(), before)

    def test_named_unknown_skill_token_rejects_before_any_write(self):
        skill = self.root / ".claude" / "skills" / "make-ready-pipeline" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("Unknown: {{unmapped_skill_value}}\n")
        before = skill.read_bytes()
        mapping = self.mapping({
            "placeholder": "company_name",
            "source": "cover.company_name",
            "extractor": "identity",
        })
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, self.answers, self.core
            )
        self.assertIn("unmapped_skill_value", str(caught.exception.failures))
        self.assertEqual(skill.read_bytes(), before)

    def test_named_markdown_delimiter_rerun_changes_only_managed_surface(self):
        path = self.root / "IDENTITY.md"; path.write_text("managed={{company_name}}\norganic=Ridgeline\n")
        mapping = self.mapping({"placeholder":"company_name","source":"cover.company_name","extractor":"identity"})
        manifest = engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        changed = dict(self.cover, company_name="Mesa")
        updated = engine.placeholders.apply_rerun(self.root, mapping, changed, self.answers, self.core, manifest)
        self.assertIn("BETTY-PH:company_name -->Mesa", path.read_text())
        self.assertIn("organic=Ridgeline", path.read_text())
        self.assertEqual(updated[0]["value"], "Mesa")

    def test_named_json_pointer_rerun_changes_only_recorded_value(self):
        path = self.root / "config.json"; path.write_text(json.dumps({"managed":"{{company_name}}", "organic":"Ridgeline"}))
        mapping = self.mapping({"placeholder":"company_name","source":"cover.company_name","extractor":"identity"})
        manifest = engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        engine.placeholders.apply_rerun(self.root, mapping, dict(self.cover, company_name="Mesa"), self.answers, self.core, manifest)
        data = json.loads(path.read_text()); self.assertEqual(data, {"managed":"Mesa", "organic":"Ridgeline"})

    def test_named_json_pointer_repeated_token_in_one_string_tracks_each_occurrence(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({
            "managed": "{{company_name}} + {{company_name}}",
            "organic": "Ridgeline",
        }))
        mapping = self.mapping({
            "placeholder": "company_name",
            "source": "cover.company_name",
            "extractor": "identity",
        })
        manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, self.answers, self.core
        )
        self.assertEqual(
            json.loads(path.read_text()),
            {"managed": "Ridgeline + Ridgeline", "organic": "Ridgeline"},
        )
        self.assertEqual(len(manifest), 2)
        self.assertTrue(all(row["file"] == "config.json#/managed" for row in manifest))
        self.assertTrue(all(row["count"] == 1 for row in manifest))
        self.assertTrue(all(row["value"] == "Ridgeline" for row in manifest))

        updated = engine.placeholders.apply_rerun(
            self.root,
            mapping,
            dict(self.cover, company_name="Mesa"),
            self.answers,
            self.core,
            manifest,
        )
        self.assertEqual(
            json.loads(path.read_text()),
            {"managed": "Mesa + Mesa", "organic": "Ridgeline"},
        )
        self.assertEqual(len(updated), 2)
        self.assertTrue(all(row["file"] == "config.json#/managed" for row in updated))
        self.assertTrue(all(row["count"] == 1 for row in updated))
        self.assertTrue(all(row["value"] == "Mesa" for row in updated))

    def test_named_config_key_literal_default_is_overwritten_typed_and_manifested(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({"turn_target_days": 10, "timezone": "", "untouched": {"x": 1}}))
        mapping = {
            "placeholders": [{
                "placeholder": "company_name", "source": "cover.company_name",
                "extractor": "identity",
            }],
            "config_keys": [{
                "path": "/turn_target_days", "source": "B1", "extractor": "currency",
                "value_type": "integer", "mode": "replace",
            }],
        }
        (self.root / "IDENTITY.md").write_text("{{company_name}}")
        answers = dict(self.answers, B1="$12.00 base threshold")
        manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, answers, self.core
        )
        self.assertEqual(json.loads(path.read_text()), {
            "turn_target_days": 12, "timezone": "", "untouched": {"x": 1},
        })
        row = next(item for item in manifest if item.get("row_type") == "config_key")
        self.assertEqual(row, {
            "row_type": "config_key", "config_path": "/turn_target_days",
            "question_id": "B1", "file": "config.json#/turn_target_days",
            "count": 1, "value": 12,
        })

    def test_named_config_key_rerun_uses_manifest_and_rejects_hand_edit(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({"turn_target_days": 10, "untouched": "same"}))
        mapping = {
            "placeholders": [{
                "placeholder": "company_name", "source": "cover.company_name",
                "extractor": "identity",
            }],
            "config_keys": [{
                "path": "/turn_target_days", "source": "B1", "extractor": "currency",
                "value_type": "integer",
            }],
        }
        (self.root / "IDENTITY.md").write_text("{{company_name}}")
        manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, dict(self.answers, B1="$12 base threshold"), self.core
        )
        updated = engine.placeholders.apply_rerun(
            self.root, mapping, self.cover, dict(self.answers, B1="$14 base threshold"),
            self.core, manifest,
        )
        self.assertEqual(json.loads(path.read_text()), {"turn_target_days": 14, "untouched": "same"})
        self.assertEqual(next(item for item in updated if item.get("row_type") == "config_key")["value"], 14)
        path.write_text(json.dumps({"turn_target_days": 99, "untouched": "same"}))
        before = path.read_bytes()
        with self.assertRaises(engine.placeholders.PlaceholderRejected):
            engine.placeholders.apply_rerun(
                self.root, mapping, self.cover, dict(self.answers, B1="$16 base threshold"),
                self.core, updated,
            )
        self.assertEqual(path.read_bytes(), before)

    def test_named_config_key_file_target_lands_in_declared_file_and_survives_rerun(self):
        print("ARMED: a config row with a file target writes that file, not config.json, and replays on rerun")
        config = self.root / "config.json"; config.write_text(json.dumps({"timezone": ""}))
        structured = self.root / "seat-config.json"
        structured.write_text(json.dumps({"people": {"bd_manager": ""}, "clocks": {"max_contact_attempts": None}}))
        placeholder = {"placeholder": "company_name", "source": "cover.company_name", "extractor": "identity"}
        mapping = {
            "placeholders": [placeholder],
            "config_keys": [
                {"path": "/timezone", "source": "cover.timezone", "extractor": "identity", "value_type": "string"},
                {"path": "/people/bd_manager", "source": "C2", "extractor": "labeled_text", "label": "BD manager",
                 "value_type": "string", "file": "seat-config.json"},
                {"path": "/clocks/max_contact_attempts", "source": "D5", "extractor": "labeled_integer",
                 "label": "Max contact attempts", "value_type": "integer", "minimum": 1, "file": "seat-config.json"},
            ],
        }
        (self.root / "IDENTITY.md").write_text("{{company_name}}")
        answers = dict(self.answers, C2="Rhea Calder, manager.\n  BD manager: Rhea Calder",
                       D5="Six attempts over ten days.\n  Max contact attempts: 6")
        manifest = engine.placeholders.apply_initial(self.root, mapping, self.cover, answers, self.core)
        self.assertEqual(json.loads(structured.read_text()),
                         {"people": {"bd_manager": "Rhea Calder"}, "clocks": {"max_contact_attempts": 6}})
        self.assertEqual(json.loads(config.read_text()), {"timezone": "America/Denver"})
        rows = {item["config_path"]: item for item in manifest if item.get("row_type") == "config_key"}
        self.assertEqual(rows["/people/bd_manager"]["config_file"], "seat-config.json")
        self.assertEqual(rows["/people/bd_manager"]["file"], "seat-config.json#/people/bd_manager")
        self.assertNotIn("config_file", rows["/timezone"])
        updated = engine.placeholders.apply_rerun(
            self.root, mapping, self.cover, dict(answers, D5="  Max contact attempts: 7"), self.core, manifest,
        )
        self.assertEqual(json.loads(structured.read_text()),
                         {"people": {"bd_manager": "Rhea Calder"}, "clocks": {"max_contact_attempts": 7}})
        self.assertEqual(json.loads(config.read_text()), {"timezone": "America/Denver"})
        self.assertEqual(next(item for item in updated if item.get("config_path") == "/clocks/max_contact_attempts")
                         ["config_file"], "seat-config.json")
        structured.write_text(json.dumps({"people": {"bd_manager": "Someone Else"}, "clocks": {"max_contact_attempts": 7}}))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_rerun(self.root, mapping, self.cover, answers, self.core, updated)
        self.assertIn("manifest.config_key./people/bd_manager", str(caught.exception.failures))

    def test_named_config_key_file_target_missing_file_or_unsafe_target_rejects_by_name(self):
        print("ARMED: an absent target file, an unsafe file value, and a file on a pointer row reject by name")
        (self.root / "config.json").write_text(json.dumps({"timezone": ""}))
        (self.root / "IDENTITY.md").write_text("{{company_name}}")
        placeholder = {"placeholder": "company_name", "source": "cover.company_name", "extractor": "identity"}
        row = {"path": "/people/bd_manager", "source": "C2", "extractor": "labeled_text", "label": "BD manager",
               "value_type": "string", "file": "seat-config.json"}
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(self.root, {"placeholders": [placeholder], "config_keys": [row]},
                                              self.cover, dict(self.answers, C2="  BD manager: Rhea Calder"), self.core)
        self.assertIn("seat-config.json is missing", str(caught.exception.failures))
        path = self.tmp / "mapping.json"
        for bad in ("../config.json", "state/config.json", "config.txt", ""):
            path.write_text(json.dumps({"placeholders": [placeholder], "config_keys": [dict(row, file=bad)]}))
            with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
                engine.placeholders.load_mapping(path)
            self.assertIn("file must be a bare .json filename", str(caught.exception.failures), bad)
        path.write_text(json.dumps({"placeholders": [placeholder], "config_keys": [
            {"path": "/timezone", "value_from": "pointer", "pointer_name": "tz", "file": "seat-config.json"}]}))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("file is not supported on pointer rows", str(caught.exception.failures))

    def test_named_literal_row_needs_no_source_and_other_rows_reject_without_one(self):
        print("ARMED: a literal row carries no dead source; every other row must name one")
        (self.root / "IDENTITY.md").write_text("{{agent_name}} {{company_name}}")
        mapping = self.mapping({"placeholder": "agent_name", "extractor": "literal", "value": "seat-x"},
                               {"placeholder": "company_name", "source": "cover.company_name", "extractor": "identity"})
        manifest = engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        row = next(item for item in manifest if item["placeholder"] == "agent_name")
        self.assertEqual((row["question_id"], row["value"]), ("literal", "seat-x"))
        self.assertIn("<!-- BETTY-PH:agent_name -->seat-x<!-- /BETTY-PH:agent_name -->", (self.root / "IDENTITY.md").read_text())
        rerun = engine.placeholders.apply_rerun(self.root, mapping, self.cover, self.answers, self.core, manifest)
        self.assertEqual(next(item for item in rerun if item["placeholder"] == "agent_name")["question_id"], "literal")
        path = self.tmp / "mapping.json"
        path.write_text(json.dumps(self.mapping({"placeholder": "company_name", "extractor": "identity"})))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("row requires a source", str(caught.exception.failures))
        path.write_text(json.dumps({"placeholders": [{"placeholder": "company_name", "source": "cover.company_name", "extractor": "identity"}],
                                    "config_keys": [{"path": "/timezone", "extractor": "identity", "value_type": "string"}]}))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("mapping.config_keys./timezone", str(caught.exception.failures))
        self.assertIn("row requires a source", str(caught.exception.failures))
        # fleet rule (task 1788358269857): a literal row with a source is a dead provenance field
        path.write_text(json.dumps(self.mapping({"placeholder": "agent_name", "source": "cover.org_short_name",
                                                 "extractor": "literal", "value": "seat-x"})))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("must not carry a source", str(caught.exception.failures))
        path.write_text(json.dumps({"placeholders": [{"placeholder": "company_name", "source": "cover.company_name", "extractor": "identity"}],
                                    "config_keys": [{"path": "/timezone", "source": "cover.timezone", "extractor": "literal", "value": "UTC"}]}))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.load_mapping(path)
        self.assertIn("mapping.config_keys./timezone", str(caught.exception.failures))
        self.assertIn("must not carry a source", str(caught.exception.failures))
        shipped = [json.loads(path.read_text()) for path in sorted((HERE / "mappings").glob("*.json"))]
        self.assertTrue(shipped)
        for mapping in shipped:
            for row in mapping.get("placeholders", []) + mapping.get("config_keys", []):
                if row.get("extractor") == "literal":
                    self.assertNotIn("source", row, row)

    def test_named_currency_integral_decimal_configures_without_rounding_fractional_value(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({"threshold": 1}))
        mapping = {
            "placeholders": [],
            "config_keys": [{
                "path": "/threshold", "source": "B1", "extractor": "currency",
                "value_type": "integer",
            }],
        }
        manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, dict(self.answers, B1="$30.00"), self.core
        )
        self.assertEqual(json.loads(path.read_text())["threshold"], 30)
        path.write_text(json.dumps({"threshold": 1}))
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, dict(self.answers, B1="$30.50"), self.core
            )
        self.assertIn("threshold must be stated in whole dollars", str(caught.exception.failures))
        self.assertEqual(json.loads(path.read_text())["threshold"], 1)
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as malformed:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, dict(self.answers, B1="$30.00.50"), self.core
            )
        self.assertIn("currency value not found", str(malformed.exception.failures))
        self.assertEqual(json.loads(path.read_text())["threshold"], 1)
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as trailing_digit:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, dict(self.answers, B1="$30.001"), self.core
            )
        self.assertIn("threshold must be stated in whole dollars",
                      str(trailing_digit.exception.failures))
        self.assertEqual(json.loads(path.read_text())["threshold"], 1)
        with self.assertRaises(engine.placeholders.PlaceholderRejected) as malformed_commas:
            engine.placeholders.apply_initial(
                self.root, mapping, self.cover, dict(self.answers, B1="$3,0,0"), self.core
            )
        self.assertIn("standard comma grouping", str(malformed_commas.exception.failures))
        self.assertEqual(json.loads(path.read_text())["threshold"], 1)
        grouped_manifest = engine.placeholders.apply_initial(
            self.root, mapping, self.cover, dict(self.answers, B1="$1,250"), self.core
        )
        self.assertEqual(json.loads(path.read_text())["threshold"], 1250)
        self.assertEqual(next(row for row in manifest if row["row_type"] == "config_key")["value"], 30)
        self.assertEqual(next(row for row in grouped_manifest
                             if row["row_type"] == "config_key")["value"], 1250)

    def test_named_every_integer_currency_consumer_uses_strict_shared_token_path(self):
        print("ARMED: every mapped integer currency consumer rejects malformed decimals")
        consumers = []
        for mapping_path in sorted((HERE / "mappings").glob("*.json")):
            mapping = json.loads(mapping_path.read_text())
            for section in ("placeholders", "config_keys"):
                for row in mapping.get(section, []):
                    if (row.get("extractor") == "currency"
                            and row.get("value_type", "string") == "integer"):
                        consumers.append((mapping_path.name, row.get("path") or row.get("placeholder")))
        self.assertGreaterEqual(len(consumers), 2)
        self.assertIn(("accounting.json", "/vendor_bill_approval_threshold"), consumers)
        self.assertIn(("turnover-coordinator.json", "/approval_threshold"), consumers)
        for consumer in consumers:
            with self.subTest(consumer=consumer):
                self.assertEqual(engine.placeholders._number("$30.00", integer=True), "30")
                with self.assertRaisesRegex(ValueError, "currency value not found"):
                    engine.placeholders._number("$30.00.50", integer=True)
                with self.assertRaisesRegex(ValueError, "whole dollars"):
                    engine.placeholders._number("$30.001", integer=True)
                with self.assertRaisesRegex(ValueError, "standard comma grouping"):
                    engine.placeholders._number("$3,0,0", integer=True)
                self.assertEqual(engine.placeholders._number("$1,250", integer=True), "1250")

    def test_named_config_key_replace_missing_rejects_but_explicit_create_works(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({"untouched": True}))
        (self.root / "IDENTITY.md").write_text("{{company_name}}")
        base_row = {
            "path": "/timezone", "source": "cover.timezone", "extractor": "identity",
            "value_type": "string",
        }
        mapping = {
            "placeholders": [{
                "placeholder": "company_name", "source": "cover.company_name",
                "extractor": "identity",
            }],
            "config_keys": [base_row],
        }
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(engine.placeholders.PlaceholderRejected):
            engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        mapping["config_keys"] = [{**base_row, "mode": "create"}]
        engine.placeholders.apply_initial(self.root, mapping, self.cover, self.answers, self.core)
        self.assertEqual(json.loads(path.read_text())["timezone"], "America/Denver")

    def test_named_numeric_domain_schema_rejects_invalid_declarations(self):
        base = {
            "path": "/turn_target_days", "source": "B1", "extractor": "first_integer",
            "value_type": "integer", "mode": "create",
        }
        cases = (
            ({**base, "minimum": "one"}, "minimum must be a number"),
            ({**base, "minimum": 5, "maximum": 4}, "minimum must not exceed maximum"),
            ({**base, "minimum": float("inf")}, "minimum must be finite"),
            ({**base, "value_type": "string", "minimum": 1},
             "minimum is only valid for numeric value types"),
        )
        for row, message in cases:
            with self.subTest(message=message):
                path = self.tmp / (message.split()[0] + ".json")
                path.write_text(json.dumps({
                    "placeholders": [{
                        "placeholder": "company_name", "source": "cover.company_name",
                        "extractor": "identity",
                    }],
                    "config_keys": [row],
                }))
                with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
                    engine.placeholders.load_mapping(path)
                self.assertIn(message, str(caught.exception.failures))

    def test_named_labeled_integer_requires_declared_anchor(self):
        row = {"source": "B1", "extractor": "labeled_integer", "label": "Notice days"}
        answers = dict(self.answers, B1="Use 2 delivery methods.\nNotice days: 60")
        self.assertEqual(engine.placeholders.extract(row, self.cover, answers, self.core), "60")
        with self.assertRaises(ValueError) as caught:
            engine.placeholders.extract(row, self.cover,
                                        dict(answers, B1="Use 2 delivery methods; 60 days"),
                                        self.core)
        self.assertIn("Notice days", str(caught.exception))
        with self.assertRaises(ValueError) as duplicate:
            engine.placeholders.extract(
                row, self.cover,
                dict(answers, B1="Notice days: 30\nNotice days: 60"), self.core,
            )
        self.assertIn("appears more than once", str(duplicate.exception))

    def test_named_pointer_rows_admit_only_window_extractors_and_one_fallback_kind(self):
        base = {
            "path": "/day_mode_start", "value_from": "pointer",
            "pointer_name": "communications_window", "value_type": "string",
        }
        cases = (
            ({**base, "extractor": "first_integer"},
             "pointer extractor must be window_start or window_end"),
            ({**base, "fallback_from": "cached_answer"},
             "fallback_from must be holding_answer"),
            ({**base, "fallback": "08:00", "fallback_from": "holding_answer"},
             "mutually exclusive"),
        )
        for index, (row, message) in enumerate(cases):
            with self.subTest(message=message):
                path = self.tmp / f"pointer-row-{index}.json"
                path.write_text(json.dumps({
                    "placeholders": [{
                        "placeholder": "company_name", "source": "cover.company_name",
                        "extractor": "identity",
                    }],
                    "config_keys": [row],
                }))
                with self.assertRaises(engine.placeholders.PlaceholderRejected) as caught:
                    engine.placeholders.load_mapping(path)
                self.assertIn(message, str(caught.exception.failures))

    def test_named_numeric_domain_honors_zero_and_optional_maximum(self):
        row = {"value_type": "integer", "minimum": 0, "maximum": 3}
        self.assertEqual(engine.placeholders._typed_value(row, "0"), 0)
        self.assertEqual(engine.placeholders._typed_value(row, "3"), 3)
        with self.assertRaises(ValueError) as caught:
            engine.placeholders._typed_value(row, "4")
        self.assertIn("above maximum 3", str(caught.exception))


if __name__ == "__main__":
    print("ARMED: mapping-table two-direction integrity and managed-surface locators")
    unittest.main(verbosity=2)
