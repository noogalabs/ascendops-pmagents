"""Configure-time autonomy doctrine and threshold-state rendering."""
from __future__ import annotations

import datetime
import json
import os
import re
import shutil
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
    # business-development seat (PR18): every prospect/owner-facing send
    "cold_outreach_first_touch",
    "nurture_value_touch",
    "appointment_reminder",
    "meeting_confirmation",
    "intake_form_link_send",
    "post_call_recap",
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
    # business-development seat (PR18): internal notes to the manager, no external recipient
    "alert_triage_note",
    "internal_status_to_manager",
    "board_row_write",
    "decision_log_filing",
    "emergency_dispatch",
    "inhouse_dispatch",
    "known_vendor_dispatch",
    "lock_change",
    "new_vendor_assignment",
}
# Closure is irreversible, but the member decides whether its agent may close
# work orders. Silence stays human-only; an explicit opt-in lets closure follow
# the configured mode just like another operational category.
IRREVERSIBLE_CATEGORIES = {
    "work_order_closure",
}
# WRITE-NEW, READ-BOTH: the category was renamed platform-neutral; a
# thresholds file rendered under the legacy key migrates to the new key with
# its runtime state intact, and the runtime entry accepts the legacy name.
LEGACY_CATEGORY_KEYS = {
    "meld_closure": "work_order_closure",
}


class LegacyCategoryConflict(KeyError):
    """Both the legacy and the current key carry a row: two accuracy histories
    for one category. REFUSED BY NAME rather than merged or dropped — a merge
    would invent an accuracy record, a drop would lose one. The operator
    resolves by removing the row that is not the seat's real history."""

    def __init__(self, legacy: str, current: str):
        super().__init__(
            f"legacy category '{legacy}' and current category '{current}' both present in "
            f"copilot-thresholds.json; remove the stale row (nothing was written)")


def migrate_legacy_categories(state: dict) -> list[str]:
    """Rename legacy category keys in place, preserving every row field.
    Returns the list of migrated legacy keys (empty when nothing legacy).
    Raises LegacyCategoryConflict when both keys exist (piper F3: the old
    shape dropped the legacy row and still reported it migrated)."""
    migrated = []
    categories = state.get("categories", {})
    for legacy, current in LEGACY_CATEGORY_KEYS.items():
        if legacy in categories:
            if current in categories:
                raise LegacyCategoryConflict(legacy, current)
            categories[current] = categories.pop(legacy)
            migrated.append(legacy)
    return migrated


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
    # Owner-ruled 2026-09-01: resident/external messaging is the MEMBER'S
    # choice. FAIL-CLOSED: only an explicit affirmative opts in — a missing,
    # blank, or unrecognized answer keeps messages routing through the
    # property manager. The choice is theirs; silence is not a choice.
    raw_external = raw_cover.get("external_send_autonomy", "").strip().lower()
    external_send = raw_external in {"yes", "y", "true"}
    raw_closure = raw_cover.get("work_order_closure_autonomy", "").strip().lower()
    closure = raw_closure in {"yes", "y", "true"}
    return {"mode": mode, "unlock_window": window, "qualifying_accuracy": accuracy,
            "external_send_autonomy": external_send,
            "work_order_closure_autonomy": closure}


def evaluate_unlock(state: dict, category: str) -> bool:
    """Unlock a copilot category AUTOMATICALLY when the accuracy bar over the
    configured window is met. Owner-ruled 2026-09-01 (overruling the earlier
    human-approves-each-unlock reading): unlocks are earned by the numbers;
    doctrine follows code. Supervised and full modes never evaluate here."""
    row = state["categories"][category]
    if state.get("autonomy_mode") != "copilot" or row.get("mode") != "copilot":
        return False
    if (category in IRREVERSIBLE_CATEGORIES
            and not state.get("work_order_closure_autonomy")):
        return False
    if category in EXTERNAL_SEND_CATEGORIES and not state.get("external_send_autonomy"):
        # CHOICE-DEPENDENT, keyed on the ONE persisted fact render writes
        # (top-level external_send_autonomy, absent = opted out). The per-row
        # safety_gate flag is rendered METADATA only — a derived cache of
        # membership x opt-in — never the gate: a hand-edited row flag must
        # not let an external category earn autonomy the member never chose
        # in the window between reruns, which is exactly when record_decision
        # runs. Opted-in external rows earn like any other category.
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
    elif settings.get("external_send_autonomy"):
        posture = (
            "Eligible categories INCLUDING resident/external messaging begin autonomous on day "
            "one (the member chose direct resident messaging). Safety gates remain locked: "
            "Fair-Housing-adjacent screening or housing decisions always require human review."
        )
    else:
        posture = (
            "Eligible non-safety categories begin autonomous on day one. Safety gates remain locked: "
            "Fair-Housing-adjacent screening or housing decisions always require human review, and every "
            "external or resident-facing send always requires human approval (the member chose "
            "to approve resident messages first)."
        )
    if mode == "supervised":
        act_directly = ""
    else:
        act_directly = (
            "\n\nWhen a category is unlocked (earned or day-one autonomy): act directly, "
            "send a post-action note (\"[action taken]. Reply UNDO if needed.\"), and log "
            "`decision_presented` with `\"autonomous\": true`. Irreversible categories (work "
            "order closure) follow the member's separately recorded closure choice."
        )
        if not settings.get("external_send_autonomy"):
            act_directly += (
                " External or resident-facing categories are likewise never acted on directly, "
                "regardless of any status value in the thresholds file (the member chose to "
                "approve resident messages first)."
            )
    if settings.get("external_send_autonomy"):
        choice_note = (
            "\n\nResident/external messaging: the member chose direct messaging — messaging "
            "categories follow the same mode rules as every other category. Built-in "
            "fair-housing safeguards remain active."
        )
    else:
        choice_note = (
            "\n\nResident/external messaging: routes through the property manager — the "
            "member chose to approve resident messages first. Built-in fair-housing "
            "safeguards remain active."
        )
    if settings.get("work_order_closure_autonomy"):
        choice_note += (
            "\n\nWork order closure: the member chose agent closure autonomy. Closure "
            "follows the configured mode; completion evidence and every other safety check still apply."
        )
    else:
        choice_note += (
            "\n\nWork order closure: human approval required. The member did not opt in, "
            "so the agent must not close a work order in any mode."
        )
    if has_thresholds and mode == "supervised":
        threshold_note = (
            " Runtime state is recorded in `copilot-thresholds.json`; after each logged "
            "decision outcome, run: `./record-decision.sh <category> --correct|--incorrect` "
            "(the seat-root wrapper; works from any directory by absolute path). In "
            "supervised mode the record is kept for a later mode change — nothing unlocks. "
            "If the PMAgents repo moves, re-run setup to refresh the engine path it resolves."
        )
    elif has_thresholds:
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
    return f"{BEGIN}\n\n### Configured mode: {mode}\n\n{posture}{threshold_note}{authority_note}{act_directly}{choice_note}\n\n{END}"


def _render_thresholds(path: Path, settings: dict[str, object], configured_at: str) -> None:
    state = json.loads(path.read_text(encoding="utf-8"))
    migrate_legacy_categories(state)
    mode = settings["mode"]
    # previous_mode MUST be read BEFORE the new mode is assigned: the original
    # ordering self-clobbered the read, mode_changed was always False, and a
    # full->copilot rerun preserved day-one unlocks nothing had earned.
    # NOTE: since the threshold-change re-evaluation landed, this flag is
    # defence-in-depth on that path (a non-copilot prior mode stores window
    # None, which always differs from a copilot window and triggers the
    # re-evaluation) — it is NOT dead code: the explicit lock-on-mode-change
    # in the copilot branch still keys on it directly (its only reader).
    previous_mode = state.get("autonomy_mode")
    mode_changed = previous_mode is not None and previous_mode != mode
    state["autonomy_mode"] = mode
    external_opt_in = bool(settings.get("external_send_autonomy"))
    closure_opt_in = bool(settings.get("work_order_closure_autonomy"))
    state["external_send_autonomy"] = external_opt_in
    state["work_order_closure_autonomy"] = closure_opt_in
    state["safety_gates"] = {
        # Fair-housing screening is NOT messaging: locked in every mode and
        # every choice — the member choice covers resident/external SENDS only.
        "fair_housing_screening": {"status": "locked", "safety_gate": True},
        "external_resident_send": (
            {"status": "member_choice", "safety_gate": False}
            if external_opt_in else
            {"status": "locked", "safety_gate": True}),
        "work_order_closure": (
            {"status": "member_choice", "safety_gate": False}
            if closure_opt_in else
            {"status": "locked", "safety_gate": True}),
    }
    for category, row in state.get("categories", {}).items():
        is_external = category in EXTERNAL_SEND_CATEGORIES
        # human-gated external = external AND the member has not opted in
        is_safety_gate = is_external and not external_opt_in
        is_irreversible = category in IRREVERSIBLE_CATEGORIES
        row["mode"] = mode
        if is_external:
            row["safety_gate"] = is_safety_gate
        if is_irreversible:
            row["irreversible_gate"] = not closure_opt_in
        # MERGE, NOT REPLACE (owner follow-up made load-bearing): a rerun must
        # never silently revoke earned autonomy. Runtime rows (counters,
        # recent_outcomes, unlocked_at/demoted_at history) are ALWAYS
        # preserved. Same-mode rerun preserves status too; a MODE CHANGE
        # preserves the accuracy record but recomputes statuses under the new
        # mode's rules (supervised locks all; full unlocks eligible internal
        # day-one; copilot starts locked and earned unlocks resume via the
        # next record-decision evaluation over the preserved window).
        if mode == "copilot":
            old_window = row.get("window")
            old_accuracy = row.get("qualifying_accuracy")
            row["window"] = settings["unlock_window"]
            row["qualifying_accuracy"] = settings["qualifying_accuracy"]
            if mode_changed or row.get("status") not in ("locked", "unlocked"):
                row["status"] = "locked"
            elif (row.get("status") == "unlocked"
                    and (old_window != settings["unlock_window"]
                         or old_accuracy != settings["qualifying_accuracy"])):
                # THRESHOLD CHANGE RE-EVALUATES: an unlocked row must still
                # qualify under the NEW settings over its preserved history
                # (occupancy = the recorded ring). Qualifying rows keep their
                # unlocked_at; non-qualifying rows re-lock with history
                # preserved; a null accuracy re-locks (no automatic unlock
                # exists to have earned).
                outcomes = list(row.get("recent_outcomes") or [])
                required = int(str(settings["unlock_window"]).removeprefix("last_"))
                new_accuracy = settings["qualifying_accuracy"]
                # The new window means the LAST N outcomes: score the slice,
                # not the whole preserved ring — otherwise a narrowed window
                # keeps a row unlocked on an overall average its own window
                # scores below bar, and the next record-decision (which trims
                # the ring) disagrees with the rerun.
                windowed = outcomes[-required:]
                still_qualifies = (
                    new_accuracy is not None
                    and len(outcomes) >= required
                    and windowed
                    and round(100 * sum(windowed) / len(windowed), 1) >= new_accuracy
                )
                if not still_qualifies:
                    row["status"] = "locked"
                    row["demoted_at"] = configured_at
                    row["demotion_reason"] = "threshold change"
            if is_safety_gate or (is_irreversible and not closure_opt_in):
                row["status"] = "locked"
        elif mode == "supervised":
            row["status"] = "locked"
            row["window"] = None
            row["qualifying_accuracy"] = None
        else:
            gated = is_safety_gate or (is_irreversible and not closure_opt_in)
            row["status"] = "locked" if gated else "unlocked"
            row["window"] = None
            row["qualifying_accuracy"] = None
            if not gated and not row.get("unlocked_at"):
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
    # The member's messaging choice is persisted at the top level by
    # _render_thresholds; a transition re-render that omitted it flipped an
    # opted-in seat's doctrine to opted-out on its first earned unlock.
    # Absent = False (fail-closed), matching parse_settings.
    return {"mode": mode, "unlock_window": window, "qualifying_accuracy": accuracy,
            "external_send_autonomy": bool(state.get("external_send_autonomy", False)),
            "work_order_closure_autonomy": bool(state.get("work_order_closure_autonomy", False))}


def settings_from_root(root: Path) -> dict[str, object]:
    """Read the installed seat's current autonomy settings fail-closed.

    Seats with a threshold ledger use that structured source of truth. Seats
    without one persist the same choices in the engine-owned doctrine block;
    exact engine phrases are read here so an unknown or hand-edited shape is
    refused instead of guessed.
    """
    thresholds = root / "copilot-thresholds.json"
    if thresholds.is_file():
        try:
            state = json.loads(thresholds.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError("copilot-thresholds.json is unreadable") from exc
        return settings_from_state(state)

    guardrails = root / "GUARDRAILS.md"
    if not guardrails.is_file():
        raise FileNotFoundError(str(guardrails))
    text = guardrails.read_text(encoding="utf-8")
    blocks = list(BLOCK.finditer(text))
    if len(blocks) != 1:
        raise ValueError("GUARDRAILS.md must contain exactly one configured autonomy block")
    block = blocks[0].group(0)
    mode_match = re.search(r"^### Configured mode: (copilot|supervised|full)$", block, re.M)
    if not mode_match:
        raise ValueError("configured autonomy block does not name a valid mode")
    direct = "the member chose direct messaging" in block
    routed = "the member chose to approve resident messages first" in block
    closure = "the member chose agent closure autonomy" in block
    human_closure = "Work order closure: human approval required" in block
    if direct == routed or closure == human_closure:
        raise ValueError("configured autonomy block does not carry unambiguous opt-ins")
    return {
        "mode": mode_match.group(1),
        "unlock_window": DEFAULT_UNLOCK_WINDOW,
        "qualifying_accuracy": DEFAULT_QUALIFYING_ACCURACY,
        "external_send_autonomy": direct,
        "work_order_closure_autonomy": closure,
    }


def set_mode(root: Path, mode: str, *, external_send_autonomy: bool | None = None,
             work_order_closure_autonomy: bool | None = None,
             changed_at: str | None = None) -> dict[str, object]:
    """Change one installed seat's autonomy through the engine renderer.

    The destination lock and crash-recoverable directory replacement are
    shared with setup. Member memory and tasks remain byte-identical. Omitted
    opt-ins retain their persisted values; only explicit flags change them.
    """
    root = root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(str(root))
    if mode not in MODES:
        raise ValueError("mode must be exactly one of: copilot, supervised, full")
    timestamp = changed_at or datetime.datetime.now(datetime.timezone.utc).replace(
        microsecond=0).isoformat().replace("+00:00", "Z")
    with transaction.DestinationLock(root):
        transaction.recover_directory_transaction(root)
        current = settings_from_root(root)
        previous_mode = current["mode"]
        settings = dict(current)
        settings["mode"] = mode
        if external_send_autonomy is not None:
            settings["external_send_autonomy"] = external_send_autonomy
        if work_order_closure_autonomy is not None:
            settings["work_order_closure_autonomy"] = work_order_closure_autonomy
        summary = {
            "agent_dir": str(root),
            "previous_mode": previous_mode,
            "autonomy_mode": mode,
            "external_send_autonomy": bool(settings["external_send_autonomy"]),
            "work_order_closure_autonomy": bool(settings["work_order_closure_autonomy"]),
            "changed_at": timestamp,
        }
        # TODO: give pre-commit scratch leftovers a stable census/cleanup path;
        # the pid suffix prevents collision but a different process will not
        # discover an orphan left before the scoped file commit.
        candidate = root.parent / f".{root.name}.mode-scratch-{os.getpid()}"
        if candidate.exists():
            raise transaction.TransactionError(
                f"mode-switch candidate already exists: {candidate}"
            )
        try:
            candidate.mkdir()
            for name in ("GUARDRAILS.md", "copilot-thresholds.json"):
                source = root / name
                if source.is_file():
                    shutil.copy2(source, candidate / name)
            render(candidate, settings, timestamp)
            rendered = {
                name: (candidate / name).read_text(encoding="utf-8")
                for name in ("GUARDRAILS.md", "copilot-thresholds.json", "record-decision.sh")
                if (candidate / name).is_file()
            }
            audit_name = "logs/autonomy-mode-audit.jsonl"
            audit = root / audit_name
            existing = audit.read_text(encoding="utf-8") if audit.is_file() else ""
            rendered[audit_name] = existing + json.dumps(summary, sort_keys=True) + "\n"
            # Enforcement lands before doctrine, so process death can never
            # leave a newly permissive promise ahead of the state that gates it.
            # The audit is an account of a completed switch and therefore last.
            write_order = (
                "copilot-thresholds.json", "record-decision.sh",
                "GUARDRAILS.md", audit_name,
            )
            writes = {name: rendered[name] for name in write_order if name in rendered}
            originals = {
                name: ((root / name).read_bytes(), (root / name).stat().st_mode)
                if (root / name).is_file() else None
                for name in writes
            }
            applied = []
            try:
                for name, text in writes.items():
                    target = root / name
                    transaction.atomic_write_text(target, text)
                    applied.append(name)
                    if name == "record-decision.sh":
                        os.chmod(target, (candidate / name).stat().st_mode)
            except BaseException:
                for name in reversed(applied):
                    target = root / name
                    original = originals[name]
                    if original is None:
                        target.unlink(missing_ok=True)
                    else:
                        transaction.atomic_write_bytes(target, original[0])
                        os.chmod(target, original[1])
                raise
        finally:
            if candidate.exists():
                shutil.rmtree(candidate)
        return summary


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
    migrate_legacy_categories(state)
    category = LEGACY_CATEGORY_KEYS.get(category, category)
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
    # The synthetic evaluation state must carry the persisted messaging
    # choice: the evaluator keys on that top-level fact, and omitting it here
    # would refuse every external unlock on the production path even for an
    # opted-in member (caught by the opted-in mirror casualty).
    eval_state = {"autonomy_mode": state.get("autonomy_mode"),
                  "external_send_autonomy": bool(state.get("external_send_autonomy", False)),
                  "work_order_closure_autonomy": bool(state.get("work_order_closure_autonomy", False)),
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
