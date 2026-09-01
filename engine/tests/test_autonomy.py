from __future__ import annotations

import datetime
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import setup
sys.path.insert(0, str(ROOT / "engine"))
import autonomy
import transaction


class AutonomyCasualties(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="autonomy-casualty-"))

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _render(self, mode="copilot", window="last_10", accuracy="90"):
        root = self.temp / mode
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        settings = autonomy.parse_settings({
            "autonomy_mode": mode,
            "unlock_window": window,
            "qualifying_accuracy": accuracy,
        })
        autonomy.render(root, settings, "2026-09-01T12:00:00Z")
        return root, json.loads((root / "copilot-thresholds.json").read_text())

    def test_full_mode_retains_fair_housing_and_external_send_safety_gates(self):
        print("ARMED: full mode must retain fair-housing and external-send safety gates")
        root, state = self._render("full")
        for gate in ("fair_housing_screening", "external_resident_send"):
            self.assertEqual(state["safety_gates"][gate]["status"], "locked")
            self.assertTrue(state["safety_gates"][gate]["safety_gate"])
        doctrine = (root / "GUARDRAILS.md").read_text()
        self.assertIn("Fair-Housing-adjacent", doctrine)
        self.assertIn("external or resident-facing send always requires human approval", doctrine)
        self.assertEqual(state["categories"]["resident_comms"]["status"], "locked")
        self.assertTrue(state["categories"]["resident_comms"]["safety_gate"])
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")

    def test_supervised_accuracy_never_unlocks(self):
        print("ARMED: supervised accuracy cannot unlock a category")
        _, state = self._render("supervised")
        row = state["categories"]["lock_change"]
        row.update(total_decisions=10, accuracy_pct=100, qualifying_accuracy=90, window="last_10")
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))
        self.assertEqual(row["status"], "locked")

    def test_configured_window_drives_render_and_evaluation(self):
        print("ARMED: unlock evaluation must use the configured non-default window")
        _, state = self._render("copilot", "last_3", "90")
        row = state["categories"]["lock_change"]
        self.assertEqual(row["window"], "last_3")
        row.update(total_decisions=3, accuracy_pct=100)
        self.assertTrue(autonomy.evaluate_unlock(state, "lock_change"))

    def test_invalid_mode_rejected_through_production_setup_without_materialization(self):
        print("ARMED: production questionnaire rejects invalid autonomy mode before materialization")
        answers = self.temp / "answers.md"
        text = (ROOT / "editions" / "maintenance" / "fixtures" / "ridgeline-maintenance-answers.md").read_text()
        for label, value in (("Autonomy mode", "typo"), ("Unlock window", "last_10"), ("Qualifying accuracy", "null")):
            text = setup.set_answer(text, setup.PromptField(f"cover.{label}", label), f"[documented] {value}")
        transaction.atomic_write_text(answers, text)
        output = self.temp / "configured"
        prompts = iter([
            "1", str(ROOT / "templates" / "maintenance-coordinator"), str(output), "2", str(answers), "",
        ])
        called = []
        def configure_fn(*args, **kwargs):
            called.append(True)
            return setup.engine.configure(*args, **kwargs)
        err = io.StringIO()
        result = setup.run_setup(
            ask=lambda _prompt: next(prompts), out=io.StringIO(), err=err,
            now=lambda: datetime.datetime(2026, 9, 1, tzinfo=datetime.timezone.utc),
            configure_fn=configure_fn,
        )
        self.assertEqual(result, 2)
        self.assertEqual(called, [True])
        self.assertIn("autonomy_mode must be exactly one of: copilot, supervised, full", err.getvalue())
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()


class CategoryClassificationCompleteness(unittest.TestCase):
    def test_every_shipped_category_is_explicitly_classified(self):
        print("ARMED: an unclassified new category must fail this suite, not silently unlock in full mode")
        both = autonomy.EXTERNAL_SEND_CATEGORIES | autonomy.INTERNAL_CATEGORIES
        overlap = autonomy.EXTERNAL_SEND_CATEGORIES & autonomy.INTERNAL_CATEGORIES
        self.assertEqual(overlap, set(), f"categories classified twice: {overlap}")
        thresholds_files = sorted(ROOT.glob("templates/**/copilot-thresholds.json")) + \
            sorted(ROOT.glob("editions/**/copilot-thresholds.json"))
        self.assertGreaterEqual(len(thresholds_files), 2, "thresholds census lost its subjects")
        unclassified = {}
        for f in thresholds_files:
            cats = set(json.loads(f.read_text())["categories"].keys())
            missing = cats - both
            if missing:
                unclassified[str(f.relative_to(ROOT))] = sorted(missing)
        self.assertEqual(unclassified, {},
                         f"unclassified categories (add to EXTERNAL_SEND_CATEGORIES or INTERNAL_CATEGORIES): {unclassified}")
