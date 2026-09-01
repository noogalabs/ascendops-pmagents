"""Configure-time autonomy doctrine and threshold-state rendering."""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

import transaction


MODES = {"copilot", "supervised", "full"}
DEFAULT_MODE = "copilot"
DEFAULT_UNLOCK_WINDOW = "last_10"
DEFAULT_QUALIFYING_ACCURACY = None
BEGIN = "<!-- PMAGENTS-AUTONOMY:BEGIN -->"
END = "<!-- PMAGENTS-AUTONOMY:END -->"
# WRITE-NEW, READ-BOTH: render emits only the member-neutral marker, but the
# removal path recognizes the legacy sentinel forever — an install rendered
# before the rename must rerender to exactly ONE new-marker block, never an
# appended second section beside a legacy remnant.
BLOCK = re.compile(r"\n?<!-- (?:PMAGENTS|BETTY)-AUTONOMY:BEGIN -->.*?<!-- (?:PMAGENTS|BETTY)-AUTONOMY:END -->\n?", re.S)
EXTERNAL_SEND_CATEGORIES = {
    "resident_comms",
    "templated_owner_update",
    "owner_statement_delivery",
    "tenant_scheduling_notice",
    "coordinator_status_request",
    "renewal_offer_send_after_terms_set",
}
# Every category in every shipped thresholds file must appear in exactly one of
# these two sets. The completeness casualty fails the suite when a NEW category
# is added unclassified — the closed list above cannot silently miss a future
# external-send-shaped category in full mode.
INTERNAL_CATEGORIES = {
    "board_row_write",
    "decision_log_filing",
    "emergency_dispatch",
    "inhouse_dispatch",
    "known_vendor_dispatch",
    "lock_change",
    "meld_closure",
    "new_vendor_assignment",
}


class SettingsError(ValueError):
    """A settings failure that names the questionnaire field it belongs to,
    so guided setup re-prompts the RIGHT field instead of always blaming
    the autonomy-mode answer."""

    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


def parse_settings(raw_cover: dict[str, str]) -> dict[str, object]:
    mode = raw_cover.get("autonomy_mode", "").strip().lower()
    if mode not in MODES:
        raise SettingsError("cover.Autonomy mode",
                            "autonomy_mode must be exactly one of: copilot, supervised, full")
    window = raw_cover.get("unlock_window", DEFAULT_UNLOCK_WINDOW).strip().lower()
    if not re.fullmatch(r"last_[1-9]\d*", window):
        raise SettingsError("cover.Unlock window",
                            "unlock_window must use last_N with N greater than zero")
    raw_accuracy = raw_cover.get("qualifying_accuracy", "null").strip().lower()
    if raw_accuracy in {"null", "none", "not set"}:
        accuracy = None
    else:
        try:
            accuracy = float(raw_accuracy.removesuffix("%"))
        except ValueError as exc:
            raise SettingsError("cover.Qualifying accuracy",
                                "qualifying_accuracy must be null or a number from 0 through 100") from exc
        if not 0 <= accuracy <= 100:
            raise SettingsError("cover.Qualifying accuracy",
                                "qualifying_accuracy must be null or a number from 0 through 100")
        if accuracy.is_integer():
            accuracy = int(accuracy)
    return {"mode": mode, "unlock_window": window, "qualifying_accuracy": accuracy}


def evaluate_unlock(state: dict, category: str) -> bool:
    """Unlock a copilot category AUTOMATICALLY when the accuracy bar over the
    configured window is met. Owner-ruled 2026-09-01 (overruling the earlier
    human-approves-each-unlock reading): unlocks are earned by the numbers;
    doctrine follows code. Supervised and full modes never evaluate here."""
    row = state["categories"][category]
    if state.get("autonomy_mode") != "copilot" or row.get("mode") != "copilot":
        return False
    if category in EXTERNAL_SEND_CATEGORIES:
        # BRIDGE EXCLUSION (PR34 seam): with the approval act removed, an
        # accuracy-only unlock would grant external-send autonomy nobody
        # chose. External categories are hard-excluded from automatic unlock
        # until the member-choice setting (external_send_autonomy, PR34's
        # six-cell matrix) replaces this exclusion with choice-dependence.
        # Every merged head must be safe STANDALONE.
        return False
    accuracy = row.get("qualifying_accuracy")
    if accuracy is None:
        return False
    required = int(str(row.get("window", "last_20")).removeprefix("last_"))
    if row.get("total_decisions", 0) < required or row.get("accuracy_pct") is None:
        return False
    if row["accuracy_pct"] < accuracy:
        return False
    row["status"] = "unlocked"
    return True


def _doctrine(settings: dict[str, object], has_thresholds: bool, authority_markers: list[str] | None = None) -> str:
    mode = settings["mode"]
    if mode == "copilot" and not has_thresholds:
        posture = (
            "Every outward-facing decision routes to the property manager for approval. "
            "Accuracy tracking is not provisioned for this seat (no thresholds file), so "
            "no automatic unlock is available until it is."
        )
    elif mode == "copilot":
        accuracy = settings["qualifying_accuracy"]
        if accuracy is None:
            earned = (
                f"No numeric qualifying accuracy is configured, so no automatic unlock fires; "
                f"the {settings['unlock_window']} window still accumulates the accuracy record."
            )
        else:
            earned = (
                f"A category unlocks AUTOMATICALLY once tracked accuracy reaches {accuracy}% "
                f"over the configured {settings['unlock_window']} window — earned by the numbers, "
                "no sign-off step."
            )
        posture = (
            f"Eligible categories start locked. {earned} A correction re-locks the "
            "category. Resident/external messaging categories are excluded from "
            "automatic unlock: every external or resident-facing send stays "
            "human-approved."
        )
    elif mode == "supervised":
        posture = (
            "Every category is permanently approval-gated. No accuracy record unlocks anything; "
            "the unlock evaluator is inert in supervised mode."
        )
    else:
        posture = (
            "Eligible non-safety categories begin autonomous on day one. Safety gates remain locked: "
            "Fair-Housing-adjacent screening or housing decisions always require human review, and every "
            "external or resident-facing send always requires human approval."
        )
    if mode == "supervised":
        act_directly = ""
    else:
        act_directly = (
            "\n\nWhen a category is unlocked (earned or day-one autonomy): act directly, "
            "send a post-action note (\"[action taken]. Reply UNDO if needed.\"), and log "
            "`decision_presented` with `\"autonomous\": true`. External or resident-facing "
            "categories are never acted on directly, regardless of any status value in the "
            "thresholds file."
        )
    if has_thresholds:
        threshold_note = (
            " Runtime state is recorded in `copilot-thresholds.json`; after each logged "
            "decision outcome, run: `./record-decision.sh <category> --correct|--incorrect` "
            "(the seat-root wrapper; works from any directory by absolute path) so the "
            "accuracy record and automatic unlocks stay real. If the PMAgents repo moves, "
            "re-run setup to refresh the engine path it resolves."
        )
    else:
        threshold_note = ""
    authority_note = ""
    if authority_markers:
        authority_note = " Approval authority remains " + " and ".join(authority_markers) + "."
    return f"{BEGIN}\n\n### Configured mode: {mode}\n\n{posture}{threshold_note}{authority_note}{act_directly}\n\n{END}"


def _render_thresholds(path: Path, settings: dict[str, object], configured_at: str) -> None:
    state = json.loads(path.read_text(encoding="utf-8"))
    mode = settings["mode"]
    # previous_mode MUST be read BEFORE the new mode is assigned: the original
    # ordering self-clobbered the read, mode_changed was always False, and a
    # full->copilot rerun preserved day-one unlocks nothing had earned.
    previous_mode = state.get("autonomy_mode")
    mode_changed = previous_mode is not None and previous_mode != mode
    state["autonomy_mode"] = mode
    state["safety_gates"] = {
        "fair_housing_screening": {"status": "locked", "safety_gate": True},
        "external_resident_send": {"status": "locked", "safety_gate": True},
    }
    for category, row in state.get("categories", {}).items():
        is_safety_gate = category in EXTERNAL_SEND_CATEGORIES
        row["mode"] = mode
        if is_safety_gate:
            row["safety_gate"] = True
        # MERGE, NOT REPLACE (owner follow-up made load-bearing): a rerun must
        # never silently revoke earned autonomy. Runtime rows (counters,
        # recent_outcomes, unlocked_at/demoted_at history) are ALWAYS
        # preserved. Same-mode rerun preserves status too; a MODE CHANGE
        # preserves the accuracy record but recomputes statuses under the new
        # mode's rules (supervised locks all; full unlocks eligible internal
        # day-one; copilot starts locked and earned unlocks resume via the
        # next record-decision evaluation over the preserved window).
        if mode == "copilot":
            row["window"] = settings["unlock_window"]
            row["qualifying_accuracy"] = settings["qualifying_accuracy"]
            if mode_changed or row.get("status") not in ("locked", "unlocked"):
                row["status"] = "locked"
            if is_safety_gate:
                row["status"] = "locked"
        elif mode == "supervised":
            row["status"] = "locked"
            row["window"] = None
            row["qualifying_accuracy"] = None
        else:
            row["status"] = "locked" if is_safety_gate else "unlocked"
            row["window"] = None
            row["qualifying_accuracy"] = None
            if not is_safety_gate and not row.get("unlocked_at"):
                row["unlocked_at"] = configured_at
        row.setdefault("unlocked_at", None)
    transaction.atomic_write_text(path, json.dumps(state, indent=2) + "\n")


RECORD_DECISION_WRAPPER = """#!/bin/sh
# Thin exec shim: the engine owns all record-decision logic (counters,
# unlock evaluation, persistence, doctrine re-render). The engine path lives
# in a sidecar BESIDE this seat (machine-local, outside the digested tree);
# if the PMAgents repo moves, re-run setup to refresh it. This file embeds
# nothing machine-specific and is byte-identical on every install.
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ENGINE=$(cat "$SCRIPT_DIR/../.$(basename -- "$SCRIPT_DIR").engine-path")
exec python3 "$ENGINE" record-decision "$SCRIPT_DIR" "$@"
"""


def _write_runtime_entry(root: Path) -> None:
    """Write the byte-constant exec wrapper into the seat. The machine-local
    engine-path SIDECAR is deliberately NOT written here: render() runs
    against the configurator's STAGING directory, and a sidecar named for the
    staging dir is orphaned by the final rename, leaving the wrapper inert on
    every real install. The configurator writes the sidecar against the FINAL
    destination via write_engine_sidecar() after the rename."""
    import os as _os
    wrapper = root / "record-decision.sh"
    transaction.atomic_write_text(wrapper, RECORD_DECISION_WRAPPER)
    _os.chmod(wrapper, 0o755)


def write_engine_sidecar(final_root: Path) -> None:
    """Write the resolved engine path to the sidecar named for the FINAL
    destination (the DestinationLock placement). Called by the configurator
    AFTER the staging rename — and by any caller that renders directly into a
    final-named directory."""
    engine_path = Path(__file__).resolve().with_name("engine.py")
    sidecar = final_root.parent / f".{final_root.name}.engine-path"
    transaction.atomic_write_text(sidecar, str(engine_path) + "\n")


def render(root: Path, settings: dict[str, object], configured_at: str) -> None:
    thresholds = root / "copilot-thresholds.json"
    if thresholds.is_file():
        _render_thresholds(thresholds, settings, configured_at)
        _write_runtime_entry(root)
    render_doctrine(root, settings)


def render_doctrine(root: Path, settings: dict[str, object]) -> None:
    """GUARDRAILS-only render. Used by record_decision on an unlock
    transition: the full render() would reset threshold statuses (it renders
    state from settings), clobbering the runtime unlock it is reporting."""
    thresholds = root / "copilot-thresholds.json"
    guardrails = root / "GUARDRAILS.md"
    if guardrails.is_file():
        original = guardrails.read_text(encoding="utf-8")
        original_heading = re.search(r"^## Copilot Thresholds[^\n]*$", original, flags=re.M)
        authority_markers = []
        if original_heading:
            original_categories = re.search(r"^Valid categories:", original[original_heading.end():], flags=re.M)
            authority_segment_end = (
                original_heading.end() + original_categories.start()
                if original_categories else len(original)
            )
            authority_markers = re.findall(
                r"<!-- BETTY-PH:property_manager_name -->.*?<!-- /BETTY-PH:property_manager_name -->",
                original[original_heading.end():authority_segment_end],
                flags=re.S,
            )
        text = BLOCK.sub("\n", original).rstrip()
        # The static act-directly row is ALWAYS stripped: its guidance lives in
        # the mode-rendered block (copilot/full) so every re-render reconstructs
        # it from constants. Rendering must stay a pure function of
        # (mode, template content) - stripping per-mode from a previously
        # rendered file destroyed the row for later mode switches.
        text = re.sub(r"^\| Category is unlocked \(earned autonomy\).*\n?", "", text, flags=re.M)
        block = _doctrine(settings, thresholds.is_file(), authority_markers)
        heading = re.search(r"^## Copilot Thresholds[^\n]*$", text, flags=re.M)
        if thresholds.is_file() and heading:
            paragraph_start = heading.end()
            categories = re.search(r"^Valid categories:", text[paragraph_start:], flags=re.M)
            if categories:
                categories_start = paragraph_start + categories.start()
                text = text[:paragraph_start] + "\n\n" + block + "\n\n" + text[categories_start:]
            else:
                text = text[:paragraph_start] + "\n\n" + block + "\n" + text[paragraph_start:]
        else:
            text = text + "\n\n## Configured Autonomy\n\n" + block
        transaction.atomic_write_text(
            guardrails, text.rstrip() + "\n"
        )

def settings_from_state(state: dict) -> dict[str, object]:
    """Reconstruct render settings from a persisted thresholds state so a
    runtime unlock transition can re-render doctrine without the original
    answers file. INVARIANT this relies on: _render_thresholds writes window
    and qualifying_accuracy UNIFORMLY across all rows from one settings dict,
    so any row's values speak for the install; mode from the top level."""
    mode = state.get("autonomy_mode", DEFAULT_MODE)
    window = DEFAULT_UNLOCK_WINDOW
    accuracy = DEFAULT_QUALIFYING_ACCURACY
    for row in state.get("categories", {}).values():
        if row.get("window"):
            window = row["window"]
        if row.get("qualifying_accuracy") is not None:
            accuracy = row["qualifying_accuracy"]
        break
    return {"mode": mode, "unlock_window": window, "qualifying_accuracy": accuracy}


def record_decision(root: Path, category: str, correct: bool,
                    decided_at: str | None = None) -> dict:
    """PRODUCTION ENTRY for the earned-autonomy ladder: record one presented
    decision's outcome, update the category's windowed accuracy record,
    evaluate the automatic unlock, persist atomically, and re-render the
    doctrine on an unlock transition. The rendered promise (automatic
    unlock-by-accuracy) is only real because this entry runs — seats invoke
    it after every logged decision (see GUARDRAILS doctrine).

    Returns a summary dict: {category, correct, total_decisions,
    accuracy_pct, status, unlocked_now}."""
    thresholds = root / "copilot-thresholds.json"
    if not thresholds.is_file():
        raise FileNotFoundError(str(thresholds))
    # The COMPLETE read-evaluate-persist-rerender sequence holds the SAME
    # DestinationLock the configurator uses (one lock namespace): an unlocked
    # read-modify-write let two concurrent invocations read identical counters
    # and silently drop an outcome, and a configurator rerun could interleave.
    with transaction.DestinationLock(root):
        return _record_decision_locked(root, thresholds, category, correct, decided_at)


def _record_decision_locked(root: Path, thresholds: Path, category: str,
                            correct: bool, decided_at: str | None) -> dict:
    state = json.loads(thresholds.read_text(encoding="utf-8"))
    if category not in state.get("categories", {}):
        raise KeyError(f"unknown category: {category}")
    row = state["categories"][category]
    required = int(str(row.get("window") or "last_20").removeprefix("last_"))
    outcomes = list(row.get("recent_outcomes") or [])
    outcomes.append(bool(correct))
    outcomes = outcomes[-required:]
    row["recent_outcomes"] = outcomes
    row["total_decisions"] = int(row.get("total_decisions", 0)) + 1
    row["correct"] = int(row.get("correct", 0)) + (1 if correct else 0)
    row["accuracy_pct"] = round(100 * sum(outcomes) / len(outcomes), 1)
    if (not correct and row.get("status") == "unlocked"
            and state.get("autonomy_mode") == "copilot"):
        # Correction-based demotion is COPILOT-ONLY (the ladder's rule). In
        # full mode a correction still RECORDS (history and accuracy stay
        # useful for a later mode change) but never changes status: an
        # unconditional relock let one incorrect outcome permanently degrade a
        # day-one category, since evaluate_unlock never fires outside copilot.
        row["status"] = "locked"
        row["demoted_at"] = decided_at
    was_unlocked = row.get("status") == "unlocked"
    # evaluate against the WINDOWED record: total gate uses window occupancy.
    # An INCORRECT outcome never produces an unlock: at-bar windowed accuracy
    # (e.g. 9T+1F = exactly 90.0 at a 90 bar) would otherwise re-unlock in the
    # same call that recorded the correction, silently ignoring "a correction
    # re-locks the category, immediately" — re-earning waits for at least the
    # next correct decision.
    eval_state = {"autonomy_mode": state.get("autonomy_mode"),
                  "categories": {category: {**row, "total_decisions": len(outcomes)}}}
    unlocked_now = bool(correct) and evaluate_unlock(eval_state, category) and not was_unlocked
    if unlocked_now:
        row["status"] = "unlocked"
        row["unlocked_at"] = decided_at
    transaction.atomic_write_text(thresholds, json.dumps(state, indent=2) + "\n")
    if unlocked_now:
        render_doctrine(root, settings_from_state(state))
    return {"category": category, "correct": bool(correct),
            "total_decisions": row["total_decisions"],
            "accuracy_pct": row["accuracy_pct"], "status": row["status"],
            "unlocked_now": unlocked_now}

