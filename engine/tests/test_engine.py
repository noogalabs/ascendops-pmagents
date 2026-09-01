#!/usr/bin/env python3
import hashlib
import io
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("glue_engine", HERE / "engine.py")
engine = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(engine)
DEMO = HERE.parent / "editions" / "maintenance"
FIXTURE = DEMO / "fixtures" / "ridgeline-maintenance-answers.md"


def digest(path):
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return [(str(p.relative_to(path)), hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(path.rglob("*")) if p.is_file()]


def replace_answer(text, question, value):
    pattern = rf"(^({question})\..*?^Answer:)\s*[^\n]*"
    return re.sub(pattern, rf"\1 {value}", text, count=1, flags=re.M | re.S)


class GlueEngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.source = self.tmp / "source"
        self.source.mkdir()
        (self.source / "config.json").write_text(json.dumps({"timezone":"America/New_York","day_mode_start":"07:30","day_mode_end":"20:30","untouched":{"x":1},"crons":[{"name":"heartbeat","prompt":"Read heartbeat"}]}, indent=2) + "\n")
        (self.source / "seat-config.json").write_text('{"seat":"maintenance-coordinator"}\n')
        for name in ("GUARDRAILS.md", "IDENTITY.md", "SOUL.md"):
            (self.source / name).write_text("# Organic\n")
        self.answers = self.tmp / "answers.md"
        self.answers.write_bytes(FIXTURE.read_bytes())
        self.production_mapping = engine.SUPPORTED["maintenance-coordinator"]["mapping"]
        self.production_version = engine.ENGINE_VERSION
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = (
            HERE / "tests" / "fixtures" / "e2" / "maintenance-mapping-v1.json"
        )
        engine.ENGINE_VERSION = "1.0.0"

    def test_named_engine_warns_but_runs_for_test_fixture_source(self):
        print("ARMED: removing the engine/tests source warning hides fixture misuse")
        output = self.tmp / "warned-output"
        stderr = io.StringIO()
        original = engine.ENGINE_TESTS_ROOT
        engine.ENGINE_TESTS_ROOT = self.tmp
        try:
            engine.configure(
                self.source,
                self.answers,
                output,
                "maintenance-coordinator",
                seat_registry={},
                warning_stream=stderr,
            )
        finally:
            engine.ENGINE_TESTS_ROOT = original
        self.assertTrue(output.is_dir(), "warning must not block configuration")
        self.assertIn("WARNING: template source is inside engine/tests", stderr.getvalue())

    def tearDown(self):
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = self.production_mapping
        engine.ENGINE_VERSION = self.production_version
        shutil.rmtree(self.tmp)

    def register_custom_mapping_seat(self, seat="test-custom-structured"):
        edition = self.tmp / seat
        library = edition / "library-src"
        shutil.copytree(self.source, library)
        (library / "configured.txt").write_text("company={{company_name}}\n")
        fixture_dir = edition / "fixtures"
        fixture_dir.mkdir()
        fixture = fixture_dir / f"ridgeline-{seat}-answers.md"
        fixture.write_bytes(self.answers.read_bytes())
        mapping = self.tmp / f"{seat}-mapping.json"
        mapping.write_text(json.dumps({
            "schema_version": 1,
            "structured_answers_file": f"{seat}-config.json",
            "placeholders": [{
                "placeholder": "company_name",
                "source": "cover.company_name",
                "extractor": "identity",
            }],
            "config_keys": [],
        }))
        engine.SUPPORTED[seat] = {
            "library_id": f"{seat}-2026-08-26",
            "answers": fixture,
            "library": library,
            "mapping": mapping,
            "question_ids": list(engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        return fixture, mapping

    def test_named_golden_round_trip_matches_sealed_core_plus_version_stamp(self):
        print("ARMED: golden round-trip sealed-core byte comparison")
        direct = self.tmp / "direct"
        wrapped = self.tmp / "wrapped"
        pinned_date = date(2026, 8, 25)
        core = engine.load_core()
        clock = lambda: pinned_date
        configuration_date = engine.run_sealed_core(
            core,
            self.source,
            self.answers,
            direct,
            DEMO / "library-src",
            clock,
        )
        engine.configure(
            self.source,
            self.answers,
            wrapped,
            "maintenance-coordinator",
            clock=clock,
        )
        direct_seat = json.loads((direct / "seat-config.json").read_text())
        direct_seat["configuration_engine"] = {
            "version": engine.ENGINE_VERSION,
            "sealed_core_sha256": engine.SEALED_CORE_SHA256,
            "seat_library": "maintenance-2026-08-23",
            "managed_surfaces": [],
            "preserved_runtime_tokens": [],
            "answer_provenance": engine.intake.preflight(self.answers, engine.load_core().QUESTION_IDS).provenance,
            "configuration_date": configuration_date,
        }
        (direct / "seat-config.json").write_text(json.dumps(direct_seat, indent=2) + "\n")
        engine.autonomy.render(
            direct,
            engine.autonomy.parse_settings(engine.validate(self.answers, "maintenance-coordinator").cover),
            configuration_date + "T00:00:00Z",
        )
        self.assertEqual(digest(direct), digest(wrapped))

    def test_named_reject_list_collects_failures_and_writes_zero_bytes(self):
        print("ARMED: malformed enum + contradiction + missing required => reject list and zero writes")
        text = self.answers.read_text()
        text = replace_answer(text, "A4", "perhaps CERTIFIED-MAIL-CONFIRMED=true CERTIFIED-MAIL-CONFIRMED=false")
        text = replace_answer(text, "B4", "900 percent")
        text = replace_answer(text, "C9", "")
        self.answers.write_text(text)
        out = self.tmp / "never-created"
        before = digest(self.tmp)
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, self.answers, out, "maintenance-coordinator")
        rendered = caught.exception.render()
        for question in ("A4", "B4", "C9"):
            self.assertIn(f"- {question}:", rendered)
        self.assertFalse(out.exists())
        after = digest(self.tmp)
        self.assertEqual(before, after)

    def test_named_rejected_validation_never_invokes_configuration_clock(self):
        print("ARMED: rejected validation calls the configuration clock zero times")
        calls = []
        self.answers.write_text(replace_answer(self.answers.read_text(), "B4", "invalid"))
        with self.assertRaises(engine.IntakeRejected):
            engine.configure(
                self.source,
                self.answers,
                self.tmp / "never-created",
                "maintenance-coordinator",
                clock=lambda: calls.append("called") or date(2026, 8, 25),
            )
        self.assertEqual(calls, [])

    def test_named_rerun_no_clobber_preserves_state_byte_identical(self):
        print("ARMED: explicit rerun no-clobber memory/tasks/env")
        output = self.tmp / "configured"
        engine.configure(self.source, self.answers, output, "maintenance-coordinator")
        (output / "memory").mkdir(); (output / "memory" / "2026-08-24.md").write_bytes(b"planted-memory\x00\n")
        (output / "tasks").mkdir(); (output / "tasks" / "active.json").write_bytes(b'{"task":"planted"}\n')
        (output / ".env").write_bytes(b"PLANTED=unchanged\n")
        protected = {name: digest(output / name) for name in ("memory", "tasks", ".env")}
        changed = replace_answer(self.answers.read_text(), "B8", "Quiet hours 21:00-07:00; external communications window 07:00-21:00 America/Denver, except live emergencies.")
        self.answers.write_text(changed)
        engine.configure(output, self.answers, output, "maintenance-coordinator")
        self.assertEqual(protected, {name: digest(output / name) for name in protected})
        cfg = json.loads((output / "config.json").read_text())
        self.assertEqual((cfg["day_mode_start"], cfg["day_mode_end"]), ("07:00", "21:00"))
        stamp = json.loads((output / "seat-config.json").read_text())["configuration_engine"]
        self.assertEqual(stamp["version"], engine.ENGINE_VERSION)

    def test_unmapped_seat_hard_rejects(self):
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.validate(self.answers, "bookkeeper")
        self.assertIn("no mapping table/library", caught.exception.render())

    def test_named_existing_nondirectory_output_rejects_without_mutation(self):
        output = self.tmp / "output"
        output.write_bytes(b"original-file\n")
        before = output.read_bytes()
        with self.assertRaises(engine.IntakeRejected):
            engine.configure(self.source, self.answers, output, "maintenance-coordinator")
        self.assertEqual(output.read_bytes(), before)

    def test_named_existing_output_requires_same_source(self):
        output = self.tmp / "output"
        output.mkdir(); (output / "memory").mkdir(); (output / "memory/x").write_text("accumulated")
        before = digest(output)
        with self.assertRaises(engine.transaction.DistinctSourceOutputError):
            engine.configure(self.source, self.answers, output, "maintenance-coordinator")
        self.assertEqual(digest(output), before)

    def test_named_success_leaves_no_scratch_or_candidate_directories(self):
        output = self.tmp / "output"
        engine.configure(self.source, self.answers, output, "maintenance-coordinator")
        leftovers = [p.name for p in self.tmp.iterdir() if ".glue-scratch-" in p.name or ".glue-candidate-" in p.name]
        self.assertEqual(leftovers, [])

    def test_named_mapping_registry_rejects_akia_answer_with_zero_output(self):
        print("ARMED: every mapping registry seat rejects an AKIA answer with zero output")
        test_edition = self.tmp / "test-mapping-edition"
        test_library = test_edition / "library-src"
        shutil.copytree(HERE.parent / "templates" / "maintenance-coordinator", test_library)
        fixed_rows = {
            "agent_name": "maintenance",
            "org": "sample-org",
            "current_timestamp": "2026-08-24T00:00:00Z",
            "upstream_update_minute": "17",
        }
        for path in test_library.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            for placeholder, value in fixed_rows.items():
                text = text.replace("{{" + placeholder + "}}", value)
            path.write_text(text)
        (test_library / "seat-config.json").write_text('{}\n')
        test_fixtures = test_edition / "fixtures"
        test_fixtures.mkdir()
        (test_fixtures / "ridgeline-test-mapping-answers.md").write_bytes(self.answers.read_bytes())
        engine.SUPPORTED["test-mapping"] = {
            "library_id": "test-mapping-2026-08-25",
            "answers": self.answers,
            "library": test_library,
            "mapping": engine.SUPPORTED["maintenance-coordinator"]["mapping"],
            "question_ids": list(engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        try:
            mapping_seats = [seat for seat, row in engine.SUPPORTED.items()
                             if row.get("runner") == "mapping"]
            self.assertTrue(mapping_seats, "mapping-seat casualty must never be vacuous")
            for seat in mapping_seats:
                row = engine.SUPPORTED[seat]
                fixture_dir = row["library"].parent / "fixtures"
                fixtures = sorted(fixture_dir.glob("ridgeline-*-answers.md"))
                self.assertEqual(
                    len(fixtures), 1,
                    f"{seat} must ship exactly one editions/<seat>/fixtures/ridgeline-*-answers.md",
                )
                fixture = fixtures[0]
                source = self.tmp / f"{seat}-source"
                shutil.copytree(row["library"], source)
                (source / "pre-template-secret.txt").write_text("AKIAABCDEFGHIJKLMNOP\n")
                pre_output = self.tmp / f"{seat}-pre-never-created"
                with self.assertRaises(engine.IntakeRejected) as pre_caught:
                    engine.configure(source, fixture, pre_output, seat, seat_registry={})
                self.assertIn("credential-scan", pre_caught.exception.render())
                self.assertIn("AWS key", pre_caught.exception.render())
                self.assertFalse(pre_output.exists())
                (source / "pre-template-secret.txt").unlink()
                answers = self.tmp / f"{seat}-answers.md"
                answer_id = row["question_ids"][-1]
                injected = replace_answer(fixture.read_text(), answer_id, "AKIAABCDEFGHIJKLMNOP")
                self.assertNotEqual(injected, fixture.read_text(), f"{seat} fixture must carry {answer_id}")
                answers.write_text(injected)
                output = self.tmp / f"{seat}-never-created"
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(source, answers, output, seat, seat_registry={})
                self.assertIn("credential-scan", caught.exception.render())
                self.assertIn("AWS key", caught.exception.render())
                self.assertFalse(output.exists())
        finally:
            engine.SUPPORTED.pop("test-mapping", None)

    def test_named_sealed_path_still_rejects_akia_with_zero_output(self):
        print("ARMED: sealed production entry retains AKIA rejection with zero output")
        self.answers.write_text(replace_answer(self.answers.read_text(), "D8", "AKIAABCDEFGHIJKLMNOP"))
        output = self.tmp / "sealed-never-created"
        with self.assertRaises(engine.IntakeRejected) as caught:
            engine.configure(self.source, self.answers, output, "maintenance-coordinator")
        self.assertIn("credential-scan", caught.exception.render())
        self.assertIn("AWS key", caught.exception.render())
        self.assertFalse(output.exists())

    def test_named_registry_mapping_seats_create_then_reconfigure_with_own_declared_filename(self):
        print("ARMED: every mapping seat create-then-reconfigure uses its declared filename")
        synthetic = "test-custom-structured"
        self.register_custom_mapping_seat(synthetic)
        try:
            mapping_seats = [seat for seat, row in engine.SUPPORTED.items()
                             if row.get("runner") == "mapping"]
            self.assertTrue(mapping_seats, "mapping-seat rerun casualty must never be vacuous")
            custom_seen = default_seen = False
            for seat in mapping_seats:
                row = engine.SUPPORTED[seat]
                declared = engine.cross_seat.structured_answers_filename(
                    engine.load_seat_mapping(seat)
                )
                custom_seen |= declared != "seat-config.json"
                default_seen |= declared == "seat-config.json"
                fixtures = sorted((row["library"].parent / "fixtures").glob("ridgeline-*-answers.md"))
                self.assertEqual(len(fixtures), 1, f"{seat} must ship exactly one conventional fixture")
                output = self.tmp / f"{seat}-sequential-output"
                engine.configure(row["library"], fixtures[0], output, seat, seat_registry={})
                engine.configure(output, fixtures[0], output, seat, seat_registry={})
                self.assertTrue((output / declared).is_file())
                if declared != "seat-config.json":
                    self.assertFalse((output / "seat-config.json").exists())
            self.assertTrue(custom_seen, "registry casualty must include a custom declared filename")
            self.assertTrue(default_seen, "registry casualty must include the default filename")
        finally:
            engine.SUPPORTED.pop(synthetic, None)

    def test_named_custom_rerun_rejects_genuine_core_counterpart_conflict(self):
        print("ARMED: custom rerun rejects a differing declared/core counterpart pair")
        seat = "test-custom-conflict"
        fixture, _ = self.register_custom_mapping_seat(seat)
        try:
            output = self.tmp / "custom-conflict-output"
            engine.configure(engine.SUPPORTED[seat]["library"], fixture, output, seat, seat_registry={})
            declared = output / f"{seat}-config.json"
            (output / "seat-config.json").write_bytes(declared.read_bytes() + b"\n")
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(output, fixture, output, seat, seat_registry={})
            self.assertIn("conflicts with core counterpart", caught.exception.render())
        finally:
            engine.SUPPORTED.pop(seat, None)

    def test_named_custom_rerun_rejects_cross_seat_counterfeit(self):
        print("ARMED: custom rerun rejects a cross-seat counterfeit declared artifact")
        seat = "test-custom-counterfeit"
        fixture, _ = self.register_custom_mapping_seat(seat)
        try:
            output = self.tmp / "custom-counterfeit-output"
            engine.configure(engine.SUPPORTED[seat]["library"], fixture, output, seat, seat_registry={})
            declared = output / f"{seat}-config.json"
            payload = json.loads(declared.read_text())
            payload["seat"] = "different-seat"
            declared.write_text(json.dumps(payload, indent=2) + "\n")
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(output, fixture, output, seat, seat_registry={})
            self.assertIn("belongs to 'different-seat'", caught.exception.render())
        finally:
            engine.SUPPORTED.pop(seat, None)

    def test_named_mapping_production_entry_supports_literal_first_and_labeled_integer(self):
        print("ARMED: mapping production entry supports literal, first_integer, and labeled_integer")
        cases = (
            ("literal", {"source": "B1", "value": "day"}, "day", None),
            ("first_integer", {"source": "B1"}, "450", None),
            ("labeled_integer", {"source": "B1", "label": "Notice days"}, "60",
             "Use 2 delivery methods.\n  Notice days: 60"),
        )
        for kind, extra, expected, answer_value in cases:
            with self.subTest(extractor=kind):
                seat = f"test-{kind}"
                source = self.tmp / f"{seat}-source"
                shutil.copytree(self.source, source)
                (source / "configured.txt").write_text("value={{configured_value}}\n")
                mapping_path = self.tmp / f"{seat}-mapping.json"
                mapping_path.write_text(json.dumps({
                    "schema_version": 1,
                    "placeholders": [{
                        "placeholder": "configured_value",
                        "extractor": kind,
                        **extra,
                    }],
                    "config_keys": [],
                }))
                engine.SUPPORTED[seat] = {
                    "library_id": f"{seat}-2026-08-26",
                    "answers": self.answers,
                    "library": DEMO / "library-src",
                    "mapping": mapping_path,
                    "question_ids": list(engine.load_core().QUESTION_IDS),
                    "runner": "mapping",
                }
                try:
                    output = self.tmp / f"{seat}-output"
                    answers = self.answers
                    if answer_value is not None:
                        answers = self.tmp / f"{seat}-answers.md"
                        answers.write_text(replace_answer(self.answers.read_text(), "B1", answer_value))
                    engine.configure(source, answers, output, seat)
                    self.assertIn(expected, (output / "configured.txt").read_text())
                finally:
                    engine.SUPPORTED.pop(seat, None)

    def test_named_labeled_integer_missing_anchor_rejects_through_production_entry(self):
        print("ARMED: labeled integer refuses an unanchored earlier numeral")
        seat = "test-labeled-integer-missing"
        source = self.tmp / f"{seat}-source"
        shutil.copytree(self.source, source)
        (source / "configured.txt").write_text("value={{configured_value}}\n")
        answers = self.tmp / f"{seat}-answers.md"
        answers.write_text(replace_answer(
            self.answers.read_text(), "B1", "Use 2 delivery methods and allow 60 days"
        ))
        mapping = self.tmp / f"{seat}-mapping.json"
        mapping.write_text(json.dumps({
            "schema_version": 1,
            "placeholders": [{
                "placeholder": "configured_value", "source": "B1",
                "extractor": "labeled_integer", "label": "Notice days",
            }],
            "config_keys": [],
        }))
        engine.SUPPORTED[seat] = {
            "library_id": f"{seat}-2026-08-26",
            "answers": answers,
            "library": DEMO / "library-src",
            "mapping": mapping,
            "question_ids": list(engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        output = self.tmp / f"{seat}-output"
        try:
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(source, answers, output, seat, seat_registry={})
            self.assertIn("Notice days", caught.exception.render())
            self.assertFalse(output.exists())
        finally:
            engine.SUPPORTED.pop(seat, None)

    def test_named_unknown_mapping_extractor_fails_closed_before_output(self):
        print("ARMED: unknown mapping extractor fails closed before output")
        seat = "test-unknown-extractor"
        mapping_path = self.tmp / "unknown-extractor-mapping.json"
        mapping_path.write_text(json.dumps({
            "schema_version": 1,
            "placeholders": [{
                "placeholder": "configured_value",
                "source": "B1",
                "extractor": "future_unreviewed_extractor",
            }],
            "config_keys": [],
        }))
        engine.SUPPORTED[seat] = {
            "library_id": "test-unknown-2026-08-26",
            "answers": self.answers,
            "library": DEMO / "library-src",
            "mapping": mapping_path,
            "question_ids": list(engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        try:
            with self.assertRaises(engine.IntakeRejected) as load_caught:
                engine.load_seat_mapping(seat)
            self.assertIn("unknown extractor", load_caught.exception.render())
            output = self.tmp / "unknown-extractor-never-created"
            with self.assertRaises(engine.IntakeRejected) as caught:
                engine.configure(self.source, self.answers, output, seat)
            self.assertIn("unknown extractor", caught.exception.render())
            self.assertFalse(output.exists())
        finally:
            engine.SUPPORTED.pop(seat, None)

    def test_named_mapping_consumed_unresolved_answers_block_all_types_before_output(self):
        print("ARMED: every mapping-consumed unresolved answer blocks activation")
        edition = HERE.parent / "editions" / "leasing"
        fixture = edition / "fixtures" / "ridgeline-leasing-answers.md"
        cases = (
            ("A2", lambda text: replace_answer(text, "A2", "[NEEDS-DAVID] Confirm later")),
            ("A3", lambda text: replace_answer(text, "A3", "[NEEDS-DAVID] Confirm later")),
            ("D2", lambda text: replace_answer(text, "D2", "[NEEDS-DAVID] Confirm later")),
            ("B8", lambda text: replace_answer(text, "B8", "[NEEDS-DAVID] Confirm later")),
            ("cover.renewal_response_window_days", lambda text: re.sub(
                r"^Renewal response window \(days\):.*$",
                "Renewal response window (days): [NEEDS-DAVID] Confirm later",
                text,
                count=1,
                flags=re.M,
            )),
        )
        for field, mutate in cases:
            with self.subTest(field=field):
                answers = self.tmp / (field.replace(".", "-") + ".md")
                answers.write_text(mutate(fixture.read_text()))
                output = self.tmp / (field.replace(".", "-") + "-output")
                with self.assertRaises(engine.IntakeRejected) as caught:
                    engine.configure(
                        edition / "library-src", answers, output, "leasing-coordinator",
                        seat_registry={},
                    )
                rendered = caught.exception.render()
                self.assertIn(field, rendered)
                self.assertIn("confirmed answer and rerun setup", rendered)
                self.assertFalse(output.exists())

    def test_named_typed_config_key_domains_reject_negative_and_zero_and_accept_valid(self):
        print("ARMED: typed config-key minimum rejects negative and zero values")
        seat = "test-domain"
        fixture, mapping_path = self.register_custom_mapping_seat(seat)
        mapping = json.loads(mapping_path.read_text())
        mapping["config_keys"] = [{
            "path": "/response_days", "source": "B1", "extractor": "first_integer",
            "value_type": "integer", "mode": "create", "minimum": 1,
        }]
        mapping_path.write_text(json.dumps(mapping))
        try:
            for value in (-10, 0):
                with self.subTest(value=value):
                    answers = self.tmp / f"domain-{value}.md"
                    answers.write_text(replace_answer(fixture.read_text(), "B1", str(value)))
                    output = self.tmp / f"domain-{value}-output"
                    with self.assertRaises(engine.IntakeRejected) as caught:
                        engine.configure(engine.SUPPORTED[seat]["library"], answers, output, seat,
                                         seat_registry={})
                    self.assertIn("/response_days", caught.exception.render())
                    self.assertIn("below minimum 1", caught.exception.render())
                    self.assertFalse(output.exists())
            valid = self.tmp / "domain-valid.md"
            valid.write_text(replace_answer(fixture.read_text(), "B1", "3"))
            output = self.tmp / "domain-valid-output"
            engine.configure(engine.SUPPORTED[seat]["library"], valid, output, seat,
                             seat_registry={})
            self.assertEqual(json.loads((output / "config.json").read_text())["response_days"], 3)
        finally:
            engine.SUPPORTED.pop(seat, None)

    def test_named_real_cli_cross_seat_and_default_maintenance_paths_exit_zero(self):
        print("ARMED: real CLI supplies an empty peer registry and preserves default seat")
        cases = (
            ("pm-assist", HERE.parent / "editions" / "pm-assist", ["--seat", "pm-assist"]),
        )
        for label, edition, extra in cases:
            with self.subTest(path=label):
                fixture = next((edition / "fixtures").glob("ridgeline-*-answers.md"))
                output = self.tmp / f"cli-{label}"
                result = subprocess.run(
                    [sys.executable, str(HERE / "engine.py"), str(edition / "library-src"),
                     str(fixture), str(output), *extra],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((output / "seat-config.json").is_file())
        maintenance = HERE.parent / "editions" / "maintenance"
        source = self.tmp / "cli-maintenance-source"
        shutil.copytree(HERE.parent / "templates" / "maintenance-coordinator", source)
        substitutions = {
            "agent_name": "ridge-maint",
            "org": "ridgeline",
            "current_timestamp": "2026-08-25T00:00:00Z",
            "upstream_update_minute": "17",
        }
        for path in source.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            for name, value in substitutions.items():
                text = text.replace("{{" + name + "}}", value)
            path.write_text(text)
        output = self.tmp / "cli-maintenance"
        result = subprocess.run(
            [sys.executable, str(HERE / "engine.py"), str(source),
             str(maintenance / "fixtures" / "ridgeline-maintenance-answers.md"), str(output)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((output / "seat-config.json").is_file())


if __name__ == "__main__":
    print("ARMED: Lane 1 file intake, atomic rejection, sealed-core round-trip, and no-clobber rerun")
    unittest.main(verbosity=2)
