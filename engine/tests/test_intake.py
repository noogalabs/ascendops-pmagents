#!/usr/bin/env python3
import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("glue_intake", HERE / "intake.py")
intake = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = intake
SPEC.loader.exec_module(intake)
FIXTURE = HERE.parent / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md"
QIDS = [*(f"A{i}" for i in range(1, 9)), *(f"B{i}" for i in range(1, 13)), *(f"C{i}" for i in range(1, 10)), *(f"D{i}" for i in range(1, 10))]


def replace(text, question, value):
    return re.sub(rf"(^({question})\..*?^Answer:)\s*[^\n]*", rf"\1 {value}", text, count=1, flags=re.M | re.S)


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "answers.md"
        self.path.write_bytes(FIXTURE.read_bytes())

    def failures(self, text):
        self.path.write_text(text)
        with self.assertRaises(intake.IntakeRejected) as caught:
            intake.preflight(self.path, QIDS)
        return caught.exception

    def test_named_all_unknown_provenance_tags_are_aggregated(self):
        text = replace(replace(self.path.read_text(), "B2", "[estimated] $500"), "C3", "[guessed] Alex")
        rejected = self.failures(text)
        self.assertEqual([field for field, _ in rejected.failures if field in {"B2", "C3"}], ["B2", "C3"])

    def test_named_semantic_numeric_parser_ignores_unrelated_number(self):
        rejected = self.failures(replace(self.path.read_text(), "B1", "3 owners; base owner pre-approval threshold is $2,000,000."))
        self.assertIn("B1", [field for field, _ in rejected.failures])

    def test_named_conditional_gates_fail_shut(self):
        text = replace(self.path.read_text(), "A4", "Yes. CERTIFIED-MAIL-CONFIRMED=false")
        text = replace(text, "B3", "$30; LEASE-CLAUSE-CONFIRMED=maybe")
        rejected = self.failures(text)
        self.assertIn("contradicts", rejected.render())
        self.assertIn("LEASE-CLAUSE-CONFIRMED=true|false", rejected.render())

    def test_named_derived_grammar_failures_aggregate_before_writes(self):
        text = replace(self.path.read_text(), "B8", "quiet hours are overnight")
        text = replace(text, "D9", "Friday afternoon; Monday morning")
        before = sorted(self.tmp.iterdir())
        rejected = self.failures(text)
        self.assertEqual([field for field, _ in rejected.failures if field in {"B8", "D9"}], ["B8", "D9"])
        self.assertEqual(before, sorted(self.tmp.iterdir()))

    def test_named_non_utf8_is_a_reject_list(self):
        self.path.write_bytes(b"\xff\xfe")
        with self.assertRaises(intake.IntakeRejected) as caught:
            intake.preflight(self.path, QIDS)
        self.assertIn("REJECT LIST", caught.exception.render())
        self.assertEqual(caught.exception.failures[0][0], "file")

    def test_named_per_field_provenance_is_explicit(self):
        text = self.path.read_text().replace("Company name: Ridgeline Residential", "Company name: [documented] Ridgeline Residential")
        text = replace(text, "B2", "[inferred] $1,200")
        text = replace(text, "D6", "[NEEDS-DAVID] confirm alert channel")
        self.path.write_text(text)
        result = intake.preflight(self.path, QIDS)
        self.assertEqual(result.provenance["cover.company_name"], "documented")
        self.assertEqual(result.provenance["B2"], "inferred")
        self.assertEqual(result.provenance["D6"], "NEEDS-DAVID")
        self.assertTrue(result.answers["D6"].startswith("[NEEDS-DAVID]"))

    def test_named_declared_e_question_parses_and_undeclared_id_rejects(self):
        print("ARMED: declared E questions parse and undeclared question ids reject loudly")
        text = self.path.read_text() + "\nE1. What is the turnover escalation rule?\n\nAnswer: [documented] Escalate after review.\n"
        self.path.write_text(text)
        parsed = intake.preflight(self.path, [*QIDS, "E1"])
        self.assertEqual(parsed.raw_answers["E1"], "[documented] Escalate after review.")
        with self.assertRaises(intake.IntakeRejected) as caught:
            intake.preflight(self.path, QIDS)
        self.assertIn(
            ("E1", "question id is not declared for this edition"),
            caught.exception.failures,
        )

    def test_named_question_id_consumers_use_the_canonical_surface(self):
        print("ARMED: question-id consumers cannot regress to an A-D spelling")
        for path in [
            HERE / "intake.py",
            HERE.parent / "setup.py",
            HERE.parent / "tests" / "test_review_sweeps.py",
        ]:
            self.assertNotIn("[A-D]", path.read_text(), str(path))


if __name__ == "__main__":
    print("ARMED: complete intake aggregation, semantic validation, and provenance")
    unittest.main(verbosity=2)
