#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import shutil
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

    def tearDown(self):
        engine.SUPPORTED["maintenance-coordinator"]["mapping"] = self.production_mapping
        engine.ENGINE_VERSION = self.production_version
        shutil.rmtree(self.tmp)

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


if __name__ == "__main__":
    print("ARMED: Lane 1 file intake, atomic rejection, sealed-core round-trip, and no-clobber rerun")
    unittest.main(verbosity=2)
