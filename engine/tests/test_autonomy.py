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
        sets = (autonomy.EXTERNAL_SEND_CATEGORIES, autonomy.INTERNAL_CATEGORIES,
                autonomy.IRREVERSIBLE_CATEGORIES)
        both = set().union(*sets)
        for i, a in enumerate(sets):
            for b in sets[i + 1:]:
                self.assertEqual(a & b, set(), f"categories classified twice: {a & b}")
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
                         f"unclassified categories (add to EXTERNAL_SEND_CATEGORIES, INTERNAL_CATEGORIES, or IRREVERSIBLE_CATEGORIES): {unclassified}")


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
        # correction-relock is the copilot ladder's rule: full prose must not claim it
        self.assertNotIn("re-locks", doctrine)
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")

    def test_supervised_prose_promises_no_unlock_and_code_agrees(self):
        print("ARMED: supervised doctrine promises no unlock and evaluate_unlock agrees")
        doctrine, state = self._render("supervised")
        self.assertIn("No accuracy record unlocks anything", doctrine)
        self.assertIn("kept for a later mode change", doctrine)
        self.assertNotIn("automatic unlocks stay real", doctrine)
        row = state["categories"]["lock_change"]
        row.update(total_decisions=10, accuracy_pct=100,
                   qualifying_accuracy=90, window="last_10")
        self.assertFalse(autonomy.evaluate_unlock(state, "lock_change"))
        self.assertEqual(row["status"], "locked")



class BridgeExternalExclusion(unittest.TestCase):
    """OPTED-OUT external categories (the fail-closed default: safety_gate
    rendered True) never auto-unlock; an internal category at the same bar
    must. The former bridge hard-exclusion is superseded by this
    choice-dependent row guard — the fixture carries the rendered
    opted-out marker explicitly."""

    def _state(self, category):
        row = {"mode": "copilot", "status": "locked", "window": "last_10",
               "qualifying_accuracy": 90, "total_decisions": 10, "accuracy_pct": 100}
        if category in autonomy.EXTERNAL_SEND_CATEGORIES:
            row["safety_gate"] = True  # opted-out default, as rendered
        return {"autonomy_mode": "copilot", "categories": {category: row}}

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

class RecordDecisionConcurrency(unittest.TestCase):
    """record_decision holds the SAME DestinationLock the configurator uses
    across the complete read-evaluate-persist-rerender sequence. Deterministic
    casualties, no race: contention refuses BY NAME; the normal path releases
    cleanly; a serialized pair both count."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="rd-lock-"))
        root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        self.root = root

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _cli(self, *args):
        import subprocess, sys as _sys
        return subprocess.run(
            [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision", *args],
            capture_output=True, text=True)

    def test_held_destination_lock_refuses_by_name(self):
        print("ARMED: with the configurator lock held, the CLI refuses by name, exit 3")
        with transaction.DestinationLock(self.root):
            result = self._cli(str(self.root), "lock_change", "--correct")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("already being configured", result.stderr)
        state = json.loads((self.root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["total_decisions"], 0,
                         "a refused invocation must not have counted")

    def test_normal_path_releases_and_serialized_pair_both_count(self):
        print("ARMED: normal path releases the lock; two sequential calls both count")
        r1 = self._cli(str(self.root), "lock_change", "--correct")
        self.assertEqual(r1.returncode, 0, r1.stderr)
        r2 = self._cli(str(self.root), "lock_change", "--incorrect")
        self.assertEqual(r2.returncode, 0, r2.stderr)
        state = json.loads((self.root / "copilot-thresholds.json").read_text())
        row = state["categories"]["lock_change"]
        self.assertEqual(row["total_decisions"], 2)
        self.assertEqual(len(row["recent_outcomes"]), 2)
        # and the lock is free again for a configurator
        with transaction.DestinationLock(self.root):
            pass

class RerunPreservesEarnedState(unittest.TestCase):
    """MERGE-NOT-REPLACE: re-running the configurator must never silently
    revoke earned autonomy (owner follow-up made load-bearing: the member
    choice round tells members to re-run setup)."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="rerun-"))
        self.root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.root)
        self.settings = autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"})
        autonomy.render(self.root, self.settings, "2026-09-01T12:00:00Z")

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _earn_unlock(self):
        import subprocess, sys as _sys
        for n in range(3):
            r = subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                 str(self.root), "lock_change", "--correct"],
                capture_output=True, text=True)
            assert r.returncode == 0, r.stderr

    def _state(self):
        return json.loads((self.root / "copilot-thresholds.json").read_text())

    def test_same_answers_rerun_preserves_earned_unlock_and_history(self):
        print("ARMED: an unchanged-answers rerun preserves the earned unlock and its history")
        self._earn_unlock()
        before = self._state()["categories"]["lock_change"]
        self.assertEqual(before["status"], "unlocked")
        autonomy.render(self.root, self.settings, "2026-09-02T12:00:00Z")
        after = self._state()["categories"]["lock_change"]
        self.assertEqual(after["status"], "unlocked", "rerun revoked an earned unlock")
        self.assertEqual(after["total_decisions"], before["total_decisions"])
        self.assertEqual(after["recent_outcomes"], before["recent_outcomes"])
        self.assertEqual(after["unlocked_at"], before["unlocked_at"])

    def test_mode_change_preserves_history_and_recomputes_status(self):
        print("ARMED: a mode-change rerun preserves the accuracy record and recomputes statuses")
        self._earn_unlock()
        sup = autonomy.parse_settings({"autonomy_mode": "supervised"})
        autonomy.render(self.root, sup, "2026-09-02T12:00:00Z")
        row = self._state()["categories"]["lock_change"]
        self.assertEqual(row["status"], "locked")
        self.assertEqual(len(row["recent_outcomes"]), 3, "mode change wiped the accuracy record")
        self.assertEqual(row["total_decisions"], 3)
        # and back to copilot: history intact, status starts locked, resumes via next decision
        autonomy.render(self.root, self.settings, "2026-09-03T12:00:00Z")
        row = self._state()["categories"]["lock_change"]
        self.assertEqual(row["status"], "locked")
        self.assertEqual(len(row["recent_outcomes"]), 3)

    def test_rerender_remains_byte_idempotent(self):
        print("ARMED: same-settings re-render stays byte-idempotent with runtime state present")
        self._earn_unlock()
        autonomy.render(self.root, self.settings, "2026-09-02T12:00:00Z")
        first = (self.root / "copilot-thresholds.json").read_bytes()
        g_first = (self.root / "GUARDRAILS.md").read_bytes()
        autonomy.render(self.root, self.settings, "2026-09-02T12:00:00Z")
        self.assertEqual((self.root / "copilot-thresholds.json").read_bytes(), first)
        self.assertEqual((self.root / "GUARDRAILS.md").read_bytes(), g_first)

class DoctrineLineRunnable(unittest.TestCase):
    """The doctrine instruction must be runnable AS WRITTEN: the casualty
    extracts the rendered command from GUARDRAILS and executes it verbatim
    from the seat root; the wrapper also works by absolute path from any cwd
    (dirname-$0 resolution). Both must actually record."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="doctrine-run-"))
        self.root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.root)
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(self.root)

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _count(self):
        state = json.loads((self.root / "copilot-thresholds.json").read_text())
        return state["categories"]["lock_change"]["total_decisions"]

    def test_doctrine_line_executes_verbatim_from_seat_root(self):
        print("ARMED: the rendered doctrine command runs verbatim from the seat root and records")
        import re as _re, shlex, subprocess
        doctrine = (self.root / "GUARDRAILS.md").read_text()
        m = _re.search(r"`(\./record-decision\.sh <category> --correct\|--incorrect)`", doctrine)
        self.assertIsNotNone(m, "doctrine no longer carries the runnable line")
        cmd = m.group(1).replace("<category>", "lock_change").split("|")[0].strip()
        result = subprocess.run(shlex.split(cmd), cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self._count(), 1)

    def test_wrapper_by_absolute_path_from_other_cwd(self):
        print("ARMED: the wrapper records when invoked by absolute path from a different cwd")
        import subprocess
        elsewhere = self.temp / "elsewhere"
        elsewhere.mkdir()
        result = subprocess.run(
            [str(self.root / "record-decision.sh"), "lock_change", "--correct"],
            cwd=elsewhere, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self._count(), 1)

    def test_wrapper_bytes_are_destination_independent(self):
        print("ARMED: the wrapper embeds nothing — byte-identical across destinations")
        other = self.temp / "other-seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", other)
        autonomy.render(other, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(other)
        self.assertEqual((self.root / "record-decision.sh").read_bytes(),
                         (other / "record-decision.sh").read_bytes())

class ModeChangeByName(unittest.TestCase):
    """Drives the EXACT branch the mode_changed flag guards (the earlier
    copilot-supervised-copilot round trip converged through supervised's
    unconditional lock and never touched it — fourth convergent-outcome mask
    of the shift)."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="mode-change-"))
        self.root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.root)

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _state(self):
        return json.loads((self.root / "copilot-thresholds.json").read_text())

    def test_full_to_copilot_rerun_locks_unearned_internal(self):
        print("ARMED: full->copilot rerun locks internal categories nothing earned")
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "full"}), "2026-09-01T12:00:00Z")
        self.assertEqual(self._state()["categories"]["lock_change"]["status"], "unlocked")
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-02T12:00:00Z")
        row = self._state()["categories"]["lock_change"]
        self.assertEqual(row["status"], "locked",
                         "copilot posture violated: day-one unlock survived with nothing earned")

    def test_copilot_earned_to_full_stays_unlocked_with_history(self):
        print("ARMED: copilot-earned unlock survives a rerun into full with unlocked_at preserved")
        import subprocess, sys as _sys
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(self.root)
        for n in range(3):
            r = subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                 str(self.root), "lock_change", "--correct"],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        earned_at = self._state()["categories"]["lock_change"]["unlocked_at"]
        self.assertIsNotNone(earned_at)
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "full"}), "2026-09-02T12:00:00Z")
        row = self._state()["categories"]["lock_change"]
        self.assertEqual(row["status"], "unlocked")
        self.assertEqual(row["unlocked_at"], earned_at, "earned unlocked_at was rewritten")
        self.assertEqual(len(row["recent_outcomes"]), 3)


class ProductionEntryThroughStaging(unittest.TestCase):
    """ENFORCEMENT-ENV: the configurator stages the seat and renames it into
    place — the wrapper and its sidecar must work at the FINAL name after the
    real production path, not in a directly-rendered test dir. A sidecar
    named for the staging dir left record-decision inert on every real
    install and the direct-render casualties never saw it."""

    def test_configured_seat_wrapper_records_and_no_orphan_sidecar(self):
        print("ARMED: a configurator-built seat (through the staging rename) has a working wrapper and no orphan sidecar")
        import subprocess, sys as _sys
        sys.path.insert(0, str(ROOT / "engine" / "tests"))
        import test_contract_goldens as g
        temp = Path(tempfile.mkdtemp(prefix="staging-"))
        self.addCleanup(shutil.rmtree, temp)
        source = temp / "raw"
        output = temp / "configured-seat"
        g.prepare_raw_template(source)
        g.engine.configure(
            source,
            g.DEMO / "fixtures" / "ridgeline-maintenance-answers.md",
            output,
            "maintenance-coordinator",
            clock=g.golden_clock,
        )
        self.assertTrue((output / "record-decision.sh").is_file())
        sidecar = output.parent / f".{output.name}.engine-path"
        self.assertTrue(sidecar.is_file(), "sidecar missing at the FINAL destination name")
        orphans = list(output.parent.glob(".*.glue-candidate-*.engine-path"))
        self.assertEqual(orphans, [], f"orphan staging sidecars left behind: {orphans}")
        run = subprocess.run(
            [str(output / "record-decision.sh"), "lock_change", "--correct"],
            cwd=output, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        state = json.loads((output / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["total_decisions"], 1)

class FullModeCorrectionByName(unittest.TestCase):
    """Correction-based demotion is COPILOT-ONLY: in full mode an incorrect
    outcome RECORDS (history advances) but never changes status — the
    unconditional relock silently degraded full mode to permanent
    approval-gating one correction at a time."""

    def test_full_mode_incorrect_records_but_never_demotes(self):
        print("ARMED: full-mode incorrect outcome records history but the day-one unlock stands")
        import subprocess, sys as _sys
        temp = Path(tempfile.mkdtemp(prefix="full-corr-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "full"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(root)
        result = subprocess.run(
            [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
             str(root), "lock_change", "--incorrect"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        row = state["categories"]["lock_change"]
        self.assertEqual(row["status"], "unlocked",
                         "full-mode day-one unlock demoted by a correction")
        self.assertEqual(row["total_decisions"], 1)
        self.assertEqual(row["recent_outcomes"], [False])

class IrreversibleGateByName(unittest.TestCase):
    """Meld closure is irreversible (doctrine: a closed meld cannot be
    reopened) — it never earns autonomy in any mode."""

    def test_meld_closure_met_bar_never_unlocks_via_cli(self):
        print("ARMED: meld_closure at a met accuracy bar never auto-unlocks")
        import subprocess, sys as _sys
        temp = Path(tempfile.mkdtemp(prefix="irrev-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(root)
        for n in range(3):
            r = subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                 str(root), "meld_closure", "--correct"],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["meld_closure"]["status"], "locked")
        self.assertTrue(state["categories"]["meld_closure"]["irreversible_gate"])

    def test_full_mode_leaves_meld_closure_locked(self):
        print("ARMED: full mode day-one leaves the irreversible category locked")
        temp = Path(tempfile.mkdtemp(prefix="irrev-full-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "full"}), "2026-09-01T12:00:00Z")
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["meld_closure"]["status"], "locked")
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")


class ThresholdChangeReEvaluation(unittest.TestCase):
    """A copilot rerun with CHANGED window/accuracy re-evaluates every
    unlocked row against the new settings over the preserved history."""

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="thresh-"))
        self.root = self.temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", self.root)

    def tearDown(self):
        shutil.rmtree(self.temp)

    def _earn(self, window, accuracy, n):
        import subprocess, sys as _sys
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": window,
            "qualifying_accuracy": accuracy}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(self.root)
        for _ in range(n):
            r = subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                 str(self.root), "lock_change", "--correct"],
                capture_output=True, text=True)
            assert r.returncode == 0, r.stderr

    def _row(self):
        return json.loads((self.root / "copilot-thresholds.json").read_text())["categories"]["lock_change"]

    def test_raised_window_relocks_underqualified_row(self):
        print("ARMED: earned under last_1, rerun last_10 — re-locks with history intact")
        self._earn("last_1", "90", 1)
        self.assertEqual(self._row()["status"], "unlocked")
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-02T12:00:00Z")
        row = self._row()
        self.assertEqual(row["status"], "locked")
        self.assertEqual(row["recent_outcomes"], [True], "history lost on threshold relock")
        self.assertEqual(row["demotion_reason"], "threshold change")

    def test_lowered_accuracy_keeps_qualifying_row_unlocked(self):
        print("ARMED: earned 3/3 under last_3/90, rerun last_3/80 — stays unlocked, unlocked_at intact")
        self._earn("last_3", "90", 3)
        earned_at = self._row()["unlocked_at"]
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "80"}), "2026-09-02T12:00:00Z")
        row = self._row()
        self.assertEqual(row["status"], "unlocked")
        self.assertEqual(row["unlocked_at"], earned_at)

    def test_narrowed_window_scores_the_last_n_not_the_whole_ring(self):
        print("ARMED: narrowing the window scores the LAST N — an overall-90 ring whose last 3 are T,F,T re-locks")
        import subprocess, sys as _sys
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"}), "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(self.root)
        sequence = ["--correct"] * 7 + ["--correct", "--incorrect", "--correct"]
        for outcome in sequence:
            r = subprocess.run(
                [_sys.executable, str(ROOT / "engine" / "engine.py"), "record-decision",
                 str(self.root), "lock_change", outcome],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        row = self._row()
        self.assertEqual(row["status"], "unlocked", "fixture failed to earn: overall ring is 9/10 = 90")
        self.assertEqual(row["recent_outcomes"][-3:], [True, False, True])
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90"}), "2026-09-02T12:00:00Z")
        row = self._row()
        self.assertEqual(row["status"], "locked",
                         "narrowed window kept a row its own last-3 accuracy (66.7) scores below bar")
        self.assertEqual(len(row["recent_outcomes"]), 10, "history lost on windowed relock")

    def test_null_accuracy_rerun_relocks(self):
        print("ARMED: rerun with accuracy null re-locks — no automatic unlock exists to have earned")
        self._earn("last_3", "90", 3)
        autonomy.render(self.root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "null"}), "2026-09-02T12:00:00Z")
        self.assertEqual(self._row()["status"], "locked")

class ForceLockGuardArmed(unittest.TestCase):
    """The doctrine promises gated categories are never honored "regardless
    of any status value in the thresholds file" — a promise about UNTRUSTED
    file content. Piper proved the copilot-branch force-lock line had no
    casualty (dropping it stayed green) and is the ONLY re-lock on the
    same-settings rerun path. These arm it by name for both gated families."""

    def _hand_unlocked_rerun(self, category):
        temp = Path(tempfile.mkdtemp(prefix="force-lock-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        settings = autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_10",
            "qualifying_accuracy": "90"})
        autonomy.render(root, settings, "2026-09-01T12:00:00Z")
        thresholds = root / "copilot-thresholds.json"
        state = json.loads(thresholds.read_text())
        state["categories"][category]["status"] = "unlocked"
        thresholds.write_text(json.dumps(state, indent=2) + "\n")
        # same settings: mode_changed does not fire, threshold-change does not
        # fire — the force-lock line is the only guard on this path
        autonomy.render(root, settings, "2026-09-02T12:00:00Z")
        return json.loads(thresholds.read_text())["categories"][category]["status"]

    def test_hand_unlocked_irreversible_relocks_on_unchanged_rerun(self):
        print("ARMED: a hand-set unlocked meld_closure re-locks on a same-settings copilot rerun")
        self.assertEqual(self._hand_unlocked_rerun("meld_closure"), "locked")

    def test_hand_unlocked_external_relocks_on_unchanged_rerun(self):
        print("ARMED: a hand-set unlocked resident_comms re-locks on a same-settings copilot rerun")
        self.assertEqual(self._hand_unlocked_rerun("resident_comms"), "locked")

class MemberChoiceCasualties(unittest.TestCase):
    """external_send_autonomy: the member's choice, fail-closed on silence."""

    def test_fail_closed_parse_silence_is_not_a_choice(self):
        print("ARMED: missing, blank, or unrecognized answer keeps external sends human-gated")
        for raw in ({}, {"external_send_autonomy": ""}, {"external_send_autonomy": "maybe"},
                    {"external_send_autonomy": "definitely"}):
            self.assertFalse(autonomy.parse_settings({"autonomy_mode": "copilot", **raw})
                             ["external_send_autonomy"], raw)
        for raw in ("yes", "y", "true", "YES"):
            self.assertTrue(autonomy.parse_settings(
                {"autonomy_mode": "copilot", "external_send_autonomy": raw})
                ["external_send_autonomy"], raw)

    def _render(self, mode, choice):
        temp = Path(tempfile.mkdtemp(prefix="choice-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": mode, "unlock_window": "last_10",
            "qualifying_accuracy": "90", "external_send_autonomy": choice}),
            "2026-09-01T12:00:00Z")
        return ((root / "GUARDRAILS.md").read_text(),
                json.loads((root / "copilot-thresholds.json").read_text()))

    def test_opted_in_full_unlocks_external_day_one(self):
        print("ARMED: opted-in full mode unlocks external categories day one, screening stays locked")
        _, state = self._render("full", "yes")
        self.assertEqual(state["categories"]["resident_comms"]["status"], "unlocked")
        self.assertFalse(state["categories"]["resident_comms"]["safety_gate"])
        self.assertEqual(state["safety_gates"]["fair_housing_screening"]["status"], "locked")

    def test_opted_out_full_keeps_external_locked(self):
        print("ARMED: opted-out full mode keeps external categories human-gated")
        _, state = self._render("full", "no")
        self.assertEqual(state["categories"]["resident_comms"]["status"], "locked")
        self.assertTrue(state["categories"]["resident_comms"]["safety_gate"])

    def test_opted_in_copilot_external_earns_by_accuracy(self):
        print("ARMED: opted-in copilot lets an external category earn unlock by accuracy")
        _, state = self._render("copilot", "yes")
        row = state["categories"]["resident_comms"]
        row.update(total_decisions=10, accuracy_pct=100)
        self.assertTrue(autonomy.evaluate_unlock(state, "resident_comms"))

    def test_opted_out_copilot_external_never_auto_unlocks(self):
        print("ARMED: opted-out copilot never auto-unlocks an external category")
        _, state = self._render("copilot", "no")
        row = state["categories"]["resident_comms"]
        row.update(total_decisions=10, accuracy_pct=100)
        self.assertFalse(autonomy.evaluate_unlock(state, "resident_comms"))

    def test_fair_housing_screening_locked_in_every_cell(self):
        print("ARMED: fair-housing screening gate locked in all six mode-choice cells")
        for mode in ("copilot", "supervised", "full"):
            for choice in ("yes", "no"):
                _, state = self._render(mode, choice)
                gate = state["safety_gates"]["fair_housing_screening"]
                self.assertEqual((gate["status"], gate["safety_gate"]), ("locked", True), (mode, choice))


class RenderCodeConsistencyChoice(unittest.TestCase):
    """Six-cell mode x choice matrix: doctrine claims about resident messaging
    must match threshold state and evaluator behavior in every cell."""

    def _render(self, mode, choice):
        temp = Path(tempfile.mkdtemp(prefix="matrix-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": mode, "unlock_window": "last_10",
            "qualifying_accuracy": "90", "external_send_autonomy": choice}),
            "2026-09-01T12:00:00Z")
        return ((root / "GUARDRAILS.md").read_text(),
                json.loads((root / "copilot-thresholds.json").read_text()))

    def test_six_cells_prose_matches_state_and_evaluator(self):
        print("ARMED: all six mode-choice cells — doctrine matches state and evaluator on resident messaging")
        for mode in ("copilot", "supervised", "full"):
            for choice, opted in (("yes", True), ("no", False)):
                cell = (mode, choice)
                doctrine, state = self._render(mode, choice)
                self.assertEqual(state["external_send_autonomy"], opted, cell)
                self.assertIn("fair-housing safeguards remain active", doctrine, cell)
                if opted:
                    self.assertIn("member chose direct messaging", doctrine, cell)
                    self.assertNotIn("chose to approve resident messages first", doctrine, cell)
                else:
                    self.assertIn("chose to approve resident messages first", doctrine, cell)
                    self.assertNotIn("member chose direct messaging", doctrine, cell)
                ext = state["categories"]["resident_comms"]
                self.assertEqual(ext["safety_gate"], not opted, cell)
                if mode == "full":
                    self.assertEqual(ext["status"], "unlocked" if opted else "locked", cell)
                else:
                    self.assertEqual(ext["status"], "locked", cell)
                # evaluator agrees with the prose in every cell
                ext.update(total_decisions=10, accuracy_pct=100)
                expect_unlock = (mode == "copilot" and opted)
                self.assertEqual(autonomy.evaluate_unlock(state, "resident_comms"), expect_unlock, cell)


class TestFileStructure(unittest.TestCase):
    def test_main_guard_is_last_statement_in_every_test_file(self):
        print("ARMED: the __main__ guard must be the final statement of every test file (append-below-main class)")
        import ast
        for pattern in ("engine/tests/test_*.py", "tests/test_*.py"):
            for f in sorted(ROOT.glob(pattern)):
                tree = ast.parse(f.read_text())
                mains = [i for i, node in enumerate(tree.body)
                         if isinstance(node, ast.If) and isinstance(node.test, ast.Compare)
                         and getattr(node.test.left, "id", "") == "__name__"]
                if not mains:
                    continue
                self.assertEqual(len(mains), 1, f"{f}: multiple __main__ guards")
                self.assertEqual(mains[0], len(tree.body) - 1,
                                 f"{f}: __main__ guard is not the last statement")

class TransitionRerenderKeepsChoice(unittest.TestCase):
    """An earned-unlock transition re-renders doctrine from persisted state;
    the member's messaging choice must survive that re-render (it flipped to
    opted-out on the first unlock when settings_from_state omitted it).
    Driven through the production entry (the seat wrapper), both mirrors."""

    def _seat(self, choice):
        temp = Path(tempfile.mkdtemp(prefix="transition-choice-"))
        self.addCleanup(shutil.rmtree, temp)
        root = temp / "seat"
        shutil.copytree(ROOT / "templates" / "maintenance-coordinator", root)
        autonomy.render(root, autonomy.parse_settings({
            "autonomy_mode": "copilot", "unlock_window": "last_3",
            "qualifying_accuracy": "90", "external_send_autonomy": choice}),
            "2026-09-01T12:00:00Z")
        autonomy.write_engine_sidecar(root)
        return root

    def _earn(self, root):
        import subprocess
        for _ in range(3):
            r = subprocess.run([str(root / "record-decision.sh"), "lock_change", "--correct"],
                               cwd=root, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        state = json.loads((root / "copilot-thresholds.json").read_text())
        self.assertEqual(state["categories"]["lock_change"]["status"], "unlocked")
        return (root / "GUARDRAILS.md").read_text()

    def test_opted_in_choice_survives_earned_unlock_rerender(self):
        print("ARMED: opted-in doctrine survives the first earned-unlock re-render")
        doctrine = self._earn(self._seat("yes"))
        self.assertIn("member chose direct messaging", doctrine)
        self.assertNotIn("chose to approve resident messages first", doctrine)
        self.assertNotIn("External or resident-facing categories are likewise never", doctrine)

    def test_opted_out_choice_survives_earned_unlock_rerender(self):
        print("ARMED: opted-out doctrine survives the first earned-unlock re-render")
        doctrine = self._earn(self._seat("no"))
        self.assertIn("chose to approve resident messages first", doctrine)
        self.assertNotIn("member chose direct messaging", doctrine)


if __name__ == "__main__":
    unittest.main()
