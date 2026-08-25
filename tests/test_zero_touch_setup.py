#!/usr/bin/env python3
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import io
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
        scripted = iter([
            "1", str(self.source), str(wrapped), "1", str(answers), *self.responses,
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
        print("ARMED: named answer rejection retries in place")
        fixture = ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
        answers = self.tmp / "answers-with-one-error.md"
        answers.write_text(fixture.read_text().replace(
            "Answer: 12 percent.",
            "Answer: [documented] 900 percent.",
        ))
        output = self.tmp / "retry-output"
        scripted = iter(["1", str(self.source), str(output), "2", str(answers), "15 percent"])
        stderr = io.StringIO()
        self.assertEqual(setup.run_setup(ask=lambda _prompt: next(scripted), err=stderr), 0)
        self.assertTrue(output.is_dir())
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
    ("question", "B4", "percentage invalid", "Question to fix: B4"),
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
