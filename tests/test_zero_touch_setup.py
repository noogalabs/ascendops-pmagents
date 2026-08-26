#!/usr/bin/env python3
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import io
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pmagents_setup", ROOT / "setup.py")
setup = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(setup)


def tree_digest(root: Path):
    return [
        (str(path.relative_to(root)), hashlib.sha256(path.read_bytes()).hexdigest())
        for path in sorted(root.rglob("*")) if path.is_file()
    ]


class ZeroTouchSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pmagents-zero-touch-"))
        self.source = self.tmp / "source"
        shutil.copytree(ROOT / "engine" / "tests" / "fixtures" / "raw-maintenance-template", self.source)
        replacements = {
            "agent_name": "ridge-maint",
            "org": "ridgeline",
            "current_timestamp": "2026-08-25T00:00:00Z",
            "upstream_update_minute": "17",
        }
        for path in self.source.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text()
            for name, value in replacements.items():
                text = text.replace("{{" + name + "}}", value)
            path.write_text(text)
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        parsed = setup.engine.intake.preflight(fixture, setup.engine.load_core().QUESTION_IDS)
        self.responses = list(parsed.raw_cover.values()) + [
            parsed.raw_answers[q] for q in setup.engine.load_core().QUESTION_IDS
        ]

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_named_guided_happy_path_equals_direct_configure_bytes(self):
        print("ARMED: wrapper artifact mutation dies against direct configure bytes")
        wrapped = self.tmp / "wrapped"
        direct = self.tmp / "direct"
        answers = self.tmp / "guided-answers.md"
        terminated = [item for response in self.responses for item in (response, "")]
        scripted = iter([
            "1", str(self.source), str(wrapped), "1", str(answers), *terminated,
        ])
        clock = lambda: datetime.date(2026, 8, 25)
        stdout = io.StringIO()
        code = setup.run_setup(ask=lambda _prompt: next(scripted), out=stdout, clock=clock)
        self.assertEqual(code, 0)
        setup.engine.configure(
            self.source,
            answers,
            direct,
            "maintenance-coordinator",
            clock=clock,
            seat_registry={},
        )
        self.assertEqual(tree_digest(wrapped), tree_digest(direct))
        self.assertIn(f"Configured agent: {wrapped.resolve()}", stdout.getvalue())

    def test_named_mapping_declared_extra_cover_fields_flow_through_guided_setup(self):
        print("ARMED: mapping-declared extra cover fields flow through production guided setup")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers_template = self.tmp / "extra-cover-answers-format.md"
        answers_template.write_text(fixture.read_text().replace(
            "Timezone: America/Denver\n",
            "Timezone: America/Denver\nPortfolio code: ____________________\n",
        ))
        mapping = self.tmp / "extra-cover-mapping.json"
        mapping_payload = json.loads(
            setup.engine.SUPPORTED["maintenance-coordinator"]["mapping"].read_text()
        )
        mapping_payload["cover_fields"] = [
            {"label": label, "key": key}
            for label, key in setup.engine.intake.COVER_FIELDS.items()
        ] + [{"label": "Portfolio code", "key": "portfolio_code"}]
        mapping.write_text(json.dumps(mapping_payload, indent=2) + "\n")
        seat = "test-extra-cover"
        original_seats = setup.SEATS
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-extra-cover-2026-08-25",
            "answers": answers_template,
            "library": ROOT / "editions" / "maintenance" / "library-src",
            "mapping": mapping,
            "question_ids": list(setup.engine.load_core().QUESTION_IDS),
            "runner": "mapping",
        }
        setup.SEATS = (*original_seats, {"id": seat, "label": "Test extra cover"})
        try:
            output = self.tmp / "extra-cover-output"
            answers = self.tmp / "extra-cover-guided.md"
            (self.source / "seat-config.json").write_text("{}\n")
            scripted = iter([
                str(len(setup.SEATS)), str(self.source), str(output), "1", str(answers),
                "portfolio-17\nsecondary", "",
            ])
            self.assertEqual(setup.run_setup(
                ask=lambda _prompt: next(scripted),
                clock=lambda: datetime.date(2026, 8, 25),
            ), 0)
            configured = json.loads((output / "seat-config.json").read_text())
            self.assertEqual(configured["cover_sheet"]["portfolio_code"],
                             "[documented] portfolio-17\nsecondary")
            self.assertIn("Portfolio code: [documented] portfolio-17\n  secondary",
                          answers.read_text())
        finally:
            setup.SEATS = original_seats
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_mapping_without_cover_declaration_gets_exact_standard_four(self):
        print("ARMED: absent cover_fields declaration defaults to exactly the standard four")
        fields = setup.engine.cover_fields_for_seat("maintenance-coordinator")
        self.assertEqual(fields, setup.engine.intake.COVER_FIELDS)
        prompted = [field.label for field in setup.questionnaire_fields(
            setup.engine.SUPPORTED["maintenance-coordinator"]["answers"].read_text(), fields
        ) if field.key.startswith("cover.")]
        self.assertEqual(prompted, list(setup.engine.intake.COVER_FIELDS))

    def test_named_guided_setup_collects_declared_e_questions(self):
        print("ARMED: production guided setup collects declared E questions")
        template = self.tmp / "e-question-answers-format.md"
        template.write_text(
            "Company name: ____________________\n"
            "Org short-name: ____________________\n"
            "Forward email: ____________________\n"
            "Timezone: ____________________\n\n"
            "E1. What is the turnover escalation rule?\n\n"
            "Answer: ____________________\n"
        )
        answers = self.tmp / "e-question-answers.md"
        seat = "test-e-question"
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-e-question-2026-08-26",
            "answers": template,
            "library": ROOT / "editions" / "maintenance" / "library-src",
            "mapping": setup.engine.SUPPORTED["maintenance-coordinator"]["mapping"],
            "question_ids": ["E1"],
            "runner": "mapping",
        }
        try:
            raw_responses = [
                "Example Company", "example", "ops@example.invalid", "America/Denver",
                "Escalate after operator review",
            ]
            responses = iter([item for response in raw_responses for item in (response, "")])
            setup.guided_answers(answers, lambda _prompt: next(responses), io.StringIO(), seat)
            text = answers.read_text()
            self.assertIn("E1. What is the turnover escalation rule?", text)
            self.assertIn("Answer: [documented] Escalate after operator review", text)
            self.assertEqual(
                setup.answer_values(text)["E1"],
                "[documented] Escalate after operator review",
            )
            parsed = setup.engine.validate(answers, seat)
            self.assertEqual(
                parsed.raw_answers["E1"],
                "[documented] Escalate after operator review",
            )
        finally:
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_guided_multiline_answer_reaches_two_labeled_runtime_values(self):
        print("ARMED: guided multiline B8-style answer reaches both labeled config values")
        template = ROOT / "editions" / "leasing" / "answers-format.md"
        fixture = ROOT / "editions" / "leasing" / "fixtures" / "ridgeline-leasing-answers.md"
        mapping = self.tmp / "multiline-mapping.json"
        mapping_payload = json.loads(
            setup.engine.SUPPORTED["leasing-coordinator"]["mapping"].read_text()
        )
        mapping_payload["config_keys"].extend([
            {"path": "/owner_draw_deadline_day", "source": "B8",
             "extractor": "labeled_integer", "label": "Owner draw deadline day",
             "value_type": "integer", "minimum": 1, "mode": "create"},
            {"path": "/owner_draw_target_day", "source": "B8",
             "extractor": "labeled_integer", "label": "Owner draw target day",
             "value_type": "integer", "minimum": 1, "mode": "create"},
        ])
        mapping.write_text(json.dumps(mapping_payload, indent=2) + "\n")
        source = ROOT / "editions" / "leasing" / "library-src"
        output = self.tmp / "multiline-output"
        answers = self.tmp / "multiline-guided.md"
        seat = "test-multiline"
        original_seats = setup.SEATS
        setup.engine.SUPPORTED[seat] = {
            "library_id": "test-multiline-2026-08-26", "answers": template,
            "library": source, "mapping": mapping,
            "question_ids": setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"],
            "runner": "mapping",
        }
        setup.SEATS = (*original_seats, {"id": seat, "label": "Test multiline"})
        try:
            parsed = setup.engine.validate(fixture, "leasing-coordinator")
            responses = list(parsed.raw_cover.values()) + [
                parsed.raw_answers[q]
                for q in setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"]
            ]
            b8_index = len(parsed.raw_cover) + list(
                setup.engine.SUPPORTED["leasing-coordinator"]["question_ids"]
            ).index("B8")
            responses[b8_index] = (
                "Owner draw deadline day: 15\nOwner draw target day: 10"
            )
            terminated = [item for response in responses for item in (response, "")]
            scripted = iter([
                str(len(setup.SEATS)), str(source), str(output), "1", str(answers),
                *terminated,
            ])
            self.assertEqual(setup.run_setup(
                ask=lambda _prompt: next(scripted),
                clock=lambda: datetime.date(2026, 8, 26),
            ), 0)
            config = json.loads((output / "config.json").read_text())
            self.assertEqual(
                (config["owner_draw_deadline_day"], config["owner_draw_target_day"]),
                (15, 10),
            )
            self.assertIn(
                "Answer: [documented] Owner draw deadline day: 15\n"
                "  Owner draw target day: 10",
                answers.read_text(),
            )
            self.assertIn("### What Happens Next", answers.read_text())
            self.assertIn("Keep the answers current", answers.read_text())
        finally:
            setup.SEATS = original_seats
            setup.engine.SUPPORTED.pop(seat, None)

    def test_named_create_then_reconfigure_succeeds_through_wrapper(self):
        print("ARMED: wrapper create then reconfigure uses the production rerun entry")
        output = self.tmp / "configured"
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        clock = lambda: datetime.date(2026, 8, 25)
        for _run in (1, 2):
            scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])
            self.assertEqual(setup.run_setup(ask=lambda _prompt: next(scripted), clock=clock), 0)
        self.assertTrue((output / "seat-config.json").is_file())

    def test_named_member_interrupt_leaves_no_partial_configured_output(self):
        print("ARMED: interrupt before configure leaves zero output bytes")
        output = self.tmp / "never-configured"
        answers = self.tmp / "partial-answers.md"
        responses = iter(["1", str(self.source), str(output), "1", str(answers)])

        def interrupt_after_paths(_prompt):
            try:
                return next(responses)
            except StopIteration:
                raise KeyboardInterrupt

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(ask=interrupt_after_paths, err=stderr), 130)
        self.assertFalse(output.exists())
        self.assertTrue(answers.is_file())
        self.assertIn("No partial configured agent was written", stderr.getvalue())

    def test_named_interrupt_during_configuration_removes_wrapper_candidates(self):
        print("ARMED: configure-time interrupt removes candidate and scratch sidecars")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / "interrupted-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])

        def interrupting_configure(_source, _answers, destination, _seat, **_kwargs):
            (destination.parent / f".{destination.name}.glue-scratch-planted").mkdir()
            (destination.parent / f".{destination.name}.glue-candidate-planted").mkdir()
            raise KeyboardInterrupt

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=interrupting_configure,
        ), 130)
        self.assertFalse(output.exists())
        self.assertEqual(list(output.parent.glob(f".{output.name}.glue-*-*")), [])

    def test_named_answer_retry_fixes_in_place_without_restarting_flow(self):
        print("ARMED: named answer rejection and retry resolve the full question label")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers = self.tmp / "answers-with-one-error.md"
        answers.write_text(fixture.read_text().replace(
            "Answer: 12 percent.",
            "Answer: [documented] 900 percent.",
        ))
        output = self.tmp / "retry-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(answers),
                         "15 percent", ""])
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            return next(scripted)

        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(ask=ask, err=stderr), 0)
        self.assertTrue(output.is_dir())
        full_question = "B4. At what percentage above estimate does an invoice get flagged for review before payment?"
        self.assertIn(f"Question to fix: {full_question}", stderr.getvalue())
        self.assertTrue(any(full_question in prompt for prompt in prompts))

    def test_named_unresolvable_question_label_falls_back_to_bare_code(self):
        print("ARMED: missing questionnaire label falls open to the raw question code")
        stderr = io.StringIO()
        setup.render_rejection(
            setup.engine.IntakeRejected([("B4", "percentage invalid")]),
            stderr,
            {},
        )
        self.assertIn("Issue: B4: percentage invalid", stderr.getvalue())
        self.assertIn("Question to fix: B4", stderr.getvalue())

    def test_named_unknown_rejection_stays_visible_with_support_language(self):
        print("ARMED: unknown rejection is shown, never swallowed")
        self._assert_renderer_case(
            "novel.future.row",
            "a future structured reason",
            "not recognized by this wrapper",
        )

    def test_named_unexpected_exception_is_clean_error_without_traceback(self):
        print("ARMED: fallback removal exposes traceback")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / "unexpected-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture)])
        stderr = io.StringIO()

        def explode(*_args, **_kwargs):
            raise RuntimeError("planted invariant")

        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=explode,
        ), 1)
        self.assertEqual(stderr.getvalue(), "ERROR planted invariant\n")
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertFalse(output.exists())

    def test_named_renderer_table_covers_every_code_family(self):
        table = (ROOT / "docs" / "rejection-renderer.md").read_text()
        for prefix, _question, _problem, _example in setup.REJECTION_RULES:
            with self.subTest(prefix=prefix):
                self.assertIn(prefix.rstrip("."), table)

    def _assert_renderer_case(self, row, reason, expected_question):
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        output = self.tmp / f"rejected-{re.sub('[^a-z0-9]+', '-', row.lower())}"
        scripted = iter(["1", str(self.source), str(output), "2", str(fixture), ""])
        stderr = io.StringIO()

        def reject(*_args, **_kwargs):
            raise setup.engine.IntakeRejected([(row, reason)])

        self.assertEqual(setup.run_setup(
            ask=lambda _prompt: next(scripted), err=stderr, configure_fn=reject,
        ), 2)
        rendered = stderr.getvalue()
        self.assertIn(f"Issue: {row}: {reason}", rendered)
        self.assertIn(expected_question, rendered)
        self.assertNotIn("Traceback", rendered)
        self.assertFalse(output.exists())


RENDER_CASES = (
    ("mapping_config_keys", "mapping.config_keys./timezone", "bad type", "configuration question"),
    ("config_keys", "config_keys./timezone", "bad path", "configuration question"),
    ("mapping", "mapping", "bad mapping", "edition's setup mapping"),
    ("template", "template.IDENTITY.md", "unmanaged marker", "template agent directory"),
    ("protected_state", "protected_state", "copy failed", "existing agent directory"),
    ("structured_answers", "structured_answers_file", "missing", "configured-answer artifact"),
    ("sealed_core", "sealed_core.parse", "rejected", "questionnaire answer"),
    ("cross_seat", "cross_seat.pointer", "missing peer", "connected-seat question"),
    ("append_plan", "append-plan", "missing artifact", "cross-seat handoff plan"),
    ("appender", "appender.seat-config.json", "bad JSON", "appending seat"),
    ("owner", "owner.seat-config.json", "bad JSON", "owner seat"),
    ("file", "file", "not UTF-8", "completed answers file"),
    ("output", "output", "not a directory", "configured agent destination"),
    ("seat", "seat", "not installed", "setup edition"),
    (
        "question",
        "B4",
        "percentage invalid",
        "Question to fix: B4. At what percentage above estimate does an invoice get flagged for review before payment?",
    ),
    ("cover", "cover.Timezone", "missing", "Timezone"),
)


def _renderer_test(name, row, reason, expected):
    def test(self):
        print(f"ARMED: renderer family {row} remains mapped and visible")
        self._assert_renderer_case(row, reason, expected)
    test.__name__ = f"test_named_renderer_{name}"
    return test


for _name, _row, _reason, _expected in RENDER_CASES:
    setattr(
        ZeroTouchSetupTests,
        f"test_named_renderer_{_name}",
        _renderer_test(_name, _row, _reason, _expected),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
