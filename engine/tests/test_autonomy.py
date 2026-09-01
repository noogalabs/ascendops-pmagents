from __future__ import annotations

import datetime
import io
import json
import re
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
        # and 2 decisions under a last_3 window must not unlock
        row.update(status="locked", total_decisions=2)
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))

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


class AutomaticUnlockCasualties(unittest.TestCase):
    """Owner-ruled 2026-09-01: unlocks are AUTOMATIC on the accuracy numbers
    (doctrine follows code). These supersede the approval-act casualties."""

    def _copilot_row(self):
        return {"autonomy_mode": "copilot", "categories": {"lock_change": {
            "mode": "copilot", "status": "locked", "window": "last_10",
            "qualifying_accuracy": 90, "total_decisions": 10, "accuracy_pct": 100,
        }}}

    def test_met_accuracy_bar_unlocks_automatically(self):
        print("ARMED: a met accuracy bar unlocks with no sign-off step")
        state = self._copilot_row()
        self.assertTrue(autonomy.evaluate_unlock(state, "lock_change"))
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")

    def test_unmet_bar_does_not_unlock(self):
        state = self._copilot_row()
        state["categories"]["lock_change"]["accuracy_pct"] = 50
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))

    def test_null_accuracy_never_auto_unlocks(self):
        state = self._copilot_row()
        state["categories"]["lock_change"]["qualifying_accuracy"] = None
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))


class RendererPurity(unittest.TestCase):
    """render() must be a pure function of (mode, template content): a
    supervised render followed by a copilot re-render reconstructs the
    act-directly guidance instead of having destroyed it."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="autonomy-purity-"))

    def tearDown(self):
        shutil.rmtree(self.temp)

    def test_supervised_then_copilot_rerender_reconstructs_guidance(self):
        print("ARMED: mode round-trip must reconstruct act-directly guidance (pure renderer)")
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        sup = autonomy.parse_settings({"autonomy_mode": "supervised"})
        autonomy.render(root, sup, "2026-09-01T12:00:00Z")
        self.assertNotIn("Reply UNDO", (root / "GUARDRAILS.md").read_text())
        cop = autonomy.parse_settings({"autonomy_mode": "copilot"})
        autonomy.render(root, cop, "2026-09-01T12:05:00Z")
        text = (root / "GUARDRAILS.md").read_text()
        self.assertIn("Reply UNDO", text)
        # and a second identical render is byte-stable (idempotent)
        autonomy.render(root, cop, "2026-09-01T12:05:00Z")
        self.assertEqual(text, (root / "GUARDRAILS.md").read_text())


class FieldAttribution(unittest.TestCase):
    def test_each_invalid_field_names_itself(self):
        print("ARMED: settings failures must attribute to the failing FIELD, not always autonomy_mode")
        cases = [
            ({"autonomy_mode": "typo"}, "cover.Autonomy mode"),
            ({"autonomy_mode": "copilot", "unlock_window": "twenty"}, "cover.Unlock window"),
            ({"autonomy_mode": "copilot", "qualifying_accuracy": "150"}, "cover.Qualifying accuracy"),
        ]
        for cover, expected_field in cases:
            with self.assertRaises(autonomy.SettingsError) as ctx:
                autonomy.parse_settings(cover)
            self.assertEqual(ctx.exception.field, expected_field, cover)


class LegacySentinelMigration(unittest.TestCase):
    """WRITE-NEW, READ-BOTH: an install rendered under the legacy sentinel
    rerenders to exactly ONE member-neutral block — never an appended second
    section beside a legacy remnant."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="autonomy-legacy-"))

    def tearDown(self):
        shutil.rmtree(self.temp)

    def test_legacy_sentinel_install_rerenders_to_single_new_block(self):
        print("ARMED: legacy-sentinel install must rerender to exactly one new-marker block")
        # The DISCRIMINATING layout is the fallback path (no Copilot Thresholds
        # heading): the heading path splices between anchors and incidentally
        # removes any old block, so only the fallback exposes a read-new-only
        # BLOCK leaving a legacy remnant plus an appended second section.
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        guardrails = root / "GUARDRAILS.md"
        stripped = re.sub(r"^## Copilot Thresholds[^\n]*$", "## Decision Ledger",
                          guardrails.read_text(), flags=re.M)
        transaction.atomic_write_text(guardrails, stripped)
        settings = autonomy.parse_settings({"autonomy_mode": "copilot"})
        autonomy.render(root, settings, "2026-09-01T12:00:00Z")
        # simulate a pre-rename install: rewrite the block markers to legacy form
        legacy = guardrails.read_text().replace("PMAGENTS-AUTONOMY", "BET" "TY-AUTONOMY")
        transaction.atomic_write_text(guardrails, legacy)
        autonomy.render(root, settings, "2026-09-01T12:05:00Z")
        text = guardrails.read_text()
        self.assertEqual(text.count("PMAGENTS-AUTONOMY:BEGIN"), 1)
        self.assertNotIn("BET" "TY-AUTONOMY", text)
        self.assertEqual(text.count("### Configured mode:"), 1)


class RenderCodeConsistency(unittest.TestCase):
    """Per-mode consistency between rendered doctrine CLAIMS about unlock
    requirements and evaluate_unlock BEHAVIOR (direction is always
    doctrine-matches-code; the agreed truth is AUTOMATIC unlock-by-accuracy
    per owner ruling 2026-09-01). Any mode prose promising an approval step the code
    does not require dies here by name."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="autonomy-consistency-"))

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _render(self, mode):
        root = self.temp / mode
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        settings = autonomy.parse_settings({
            "autonomy_mode": mode, "unlock_window": "last_10",
            "qualifying_accuracy": "90"})
        autonomy.render(root, settings, "2026-09-01T12:00:00Z")
        return ((root / "GUARDRAILS.md").read_text(),
                json.loads((root / "copilot-thresholds.json").read_text()))

    NO_SIGNOFF_CLAIMS = ("pm_approval", "approval act is recorded",
                         "explicit property-manager approval",
                         "explicit property manager approval")

    def test_copilot_prose_claims_auto_and_code_auto_unlocks(self):
        print("ARMED: copilot doctrine claims automatic unlock and the code delivers it")
        doctrine, state = self._render("copilot")
        self.assertIn("unlocks AUTOMATICALLY", doctrine)
        for claim in self.NO_SIGNOFF_CLAIMS:
            self.assertNotIn(claim, doctrine, claim)
        row = state["categories"]["lock_change"]
        row.update(total_decisions=10, accuracy_pct=100,
                   qualifying_accuracy=90, window="last_10")
        self.assertTrue(autonomy.evaluate_unlock(state, "lock_change"))

    def test_full_prose_claims_day_one_and_no_signoff(self):
        print("ARMED: full-mode doctrine claims day-one autonomy with no sign-off promises")
        doctrine, state = self._render("full")
        for claim in self.NO_SIGNOFF_CLAIMS:
            self.assertNotIn(claim, doctrine, claim)
        self.assertIn("day one", doctrine)
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")

    def test_supervised_prose_promises_no_unlock_and_code_agrees(self):
        print("ARMED: supervised doctrine promises no unlock and evaluate_unlock agrees")
        doctrine, state = self._render("supervised")
        self.assertIn("No accuracy record unlocks anything", doctrine)
        row = state["categories"]["lock_change"]
        row.update(total_decisions=10, accuracy_pct=100,
                   qualifying_accuracy=90, window="last_10")
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))
        self.assertEqual(row["status"], "locked")



class BridgeExternalExclusion(unittest.TestCase):
    """BRIDGE (PR34 seam): until the member-choice setting ships, external
    send categories are hard-excluded from automatic unlock and from full's
    day-one autonomy — a merged head must be safe standalone. Both polarities:
    an external category at a met bar must NOT unlock; an internal category
    at the same bar MUST."""

    def _state(self, category):
        return {"autonomy_mode": "copilot", "categories": {category: {
            "mode": "copilot", "status": "locked", "window": "last_10",
            "qualifying_accuracy": 90, "total_decisions": 10, "accuracy_pct": 100,
        }}}

    def test_external_category_met_bar_does_not_unlock(self):
        print("ARMED: external-send category at met accuracy bar must NOT auto-unlock (bridge)")
        state = self._state("resident_comms")
        self.assertFalse(autonomy.evaluate_unlock(state, "resident_comms"))
        self.assertEqual(state["categories"]["resident_comms"]["status"], "locked")

    def test_internal_category_met_bar_unlocks(self):
        state = self._state("lock_change")
        self.assertTrue(autonomy.evaluate_unlock(state, "lock_change"))

    def test_full_mode_keeps_external_locked_day_one(self):
        temp = Path(tempfile.mkdtemp(prefix="bridge-"))
        try:
            root = temp / "seat"
            shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
            settings = autonomy.parse_settings({"autonomy_mode": "full"})
            autonomy.render(root, settings, "2026-09-01T12:00:00Z")
            state = json.loads((root / "copilot-thresholds.json").read_text())
            self.assertEqual(state["categories"]["resident_comms"]["status"], "locked")
            self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")
        finally:
            shutil.rmtree(temp)

class RecordDecisionProductionEntry(unittest.TestCase):
    """The automatic-unlock promise is only real because a PRODUCTION entry
    runs it: this casualty drives the engine CLI (not the function) from
    record through unlock and asserts the persisted state and the re-rendered
    doctrine — zero non-test callers was the unarmed-by-construction finding."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="record-decision-"))

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _run_cli(self, *args):
        import subprocess, sys as _sys
        return subprocess.run(
            [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision", *args],
            capture_output=True, text=True)

    def test_cli_records_to_unlock_persists_and_rerenders(self):
        print("ARMED: CLI record-decision drives counters to an automatic unlock with persisted state + re-rendered doctrine")
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        settings = autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"})
        autonomy.render(root, settings, "2026-09-01T12:00:00Z")
        for n in range(3):
            result = self._run_cli(str(root), "lock_change", "--correct")
            self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertTrue(summary["unlocked_now"], summary)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        row = state["categories"]["lock_change"]
        self.assertEqual(row["status"], "unlocked")
        self.assertEqual(row["accuracy_pct"], 100.0)
        self.assertIsNotNone(row["unlocked_at"])
        # doctrine was re-rendered on the transition (block present exactly once)
        doctrine = (root / "GUARDRAILS.md").read_text()
        self.assertEqual(doctrine.count("### Configured mode: copilot"), 1)

    def test_cli_correction_relocks(self):
        print("ARMED: an incorrect outcome re-locks an unlocked category through the CLI")
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        for n in range(3):
            self._run_cli(str(root), "lock_change", "--correct")
        result = self._run_cli(str(root), "lock_change", "--incorrect")
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["status"], "locked")

    def test_cli_external_category_never_unlocks(self):
        print("ARMED: the bridge holds at the production entry — external categories never unlock via CLI")
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        for n in range(3):
            result = self._run_cli(str(root), "resident_comms", "--correct")
            self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["resident_comms"]["status"], "locked")

    def test_no_thresholds_seat_gets_honest_prose(self):
        print("ARMED: a seat without a thresholds file renders honest no-tracking prose")
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        (root / "copilot-thresholds.json").unlink()
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot"}), "2026-09-01T12:00:00Z")
        doctrine = (root / "GUARDRAILS.md").read_text()
        self.assertIn("Accuracy tracking is not provisioned", doctrine)
        self.assertNotIn("unlocks AUTOMATICALLY", doctrine)

class AtBarCorrectionCasualty(unittest.TestCase):
    """A correction re-locks IMMEDIATELY even when windowed accuracy stays at
    the bar: 9T+1F in last_10 at a 90 bar is exactly 90.0 — the same call
    must never re-unlock. The earlier casualty's last_3 fixture dropped
    accuracy BELOW bar and masked this (convergent-outcome class); the
    accuracy assertion here pins the fixture at bar so it cannot re-mask."""

    def test_at_bar_correction_relocks_and_does_not_reunlock(self):
        print("ARMED: at-bar correction re-locks and never re-unlocks in the same call")
        import subprocess, sys as _sys
        temp = Path(tempfile.mkdtemp(prefix="at-bar-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        def cli(*args):
            return subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision", *args],
                capture_output=True, text=True)
        for n in range(9):
            result = cli(str(root), "lock_change", "--correct")
            self.assertEqual(result.returncode, 0, result.stderr)
        # 9 corrects in a last_10 window: occupancy 9 < 10, still locked
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["status"], "locked")
        result = cli(str(root), "lock_change", "--correct")
        summary = json.loads(result.stdout)
        self.assertTrue(summary["unlocked_now"], summary)
        # the at-bar correction: windowed outcomes become 9T+1F = exactly 90.0
        result = cli(str(root), "lock_change", "--incorrect")
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["accuracy_pct"], 90.0,
                         "fixture drifted off the bar — the mask this casualty exists to prevent")
        self.assertFalse(summary["unlocked_now"], summary)
        self.assertEqual(summary["status"], "locked")
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["status"], "locked")


if __name__ == "__main__":
    unittest.main()
