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
BLOCK = re.compile(rf"\n?{re.escape(BEGIN)}.*?{re.escape(END)}\n?", re.S)
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
    """Unlock a copilot category only when the accuracy bar is met AND a
    property-manager approval act is RECORDED on the row. The rendered
    doctrine promises explicit human approval of every unlock; an unlock
    from counters alone would be that promise lying (code follows doctrine,
    dane ruling 1788290274614). The approval act is a dict written by the
    approval workflow: {"approved_by": <name>, "approved_at": <ISO time>}."""
    row = state["categories"][category]
    if state.get("autonomy_mode") != "copilot" or row.get("mode") != "copilot":
        return False
    accuracy = row.get("qualifying_accuracy")
    if accuracy is None:
        return False
    required = int(str(row.get("window", "last_20")).removeprefix("last_"))
    if row.get("total_decisions", 0) < required or row.get("accuracy_pct") is None:
        return False
    if row["accuracy_pct"] < accuracy:
        return False
    approval = row.get("pm_approval")
    if (not isinstance(approval, dict) or not approval.get("approved_by")
            or not approval.get("approved_at")):
        return False
    row["status"] = "unlocked"
    return True


def _doctrine(settings: dict[str, object], has_thresholds: bool, authority_markers: list[str] | None = None) -> str:
    mode = settings["mode"]
    if mode == "copilot":
        accuracy = settings["qualifying_accuracy"]
        if accuracy is None:
            earned = (
                f"No numeric qualifying accuracy is configured; after the configured {settings['unlock_window']} "
                "evidence window, unlock still requires explicit property-manager approval."
            )
        else:
            earned = (
                f"They may unlock only after {accuracy}% qualifying accuracy over the configured "
                f"{settings['unlock_window']} window and explicit property-manager approval."
            )
        posture = f"Eligible categories start locked. {earned} A correction re-locks the category."
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
            "`decision_presented` with `\"autonomous\": true`. An unlock itself only takes "
            "effect once the property manager's approval act is recorded on the category "
            "(`pm_approval` with approver and timestamp)."
        )
    threshold_note = " Runtime state is recorded in `copilot-thresholds.json`." if has_thresholds else ""
    authority_note = ""
    if authority_markers:
        authority_note = " Approval authority remains " + " and ".join(authority_markers) + "."
    return f"{BEGIN}\n\n### Configured mode: {mode}\n\n{posture}{threshold_note}{authority_note}{act_directly}\n\n{END}"


def _render_thresholds(path: Path, settings: dict[str, object], configured_at: str) -> None:
    state = json.loads(path.read_text(encoding="utf-8"))
    mode = settings["mode"]
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
        if mode == "copilot":
            row["status"] = "locked"
            row["window"] = settings["unlock_window"]
            row["qualifying_accuracy"] = settings["qualifying_accuracy"]
            row["unlocked_at"] = None
        elif mode == "supervised":
            row["status"] = "locked"
            row["window"] = None
            row["qualifying_accuracy"] = None
            row["unlocked_at"] = None
        else:
            row["status"] = "locked" if is_safety_gate else "unlocked"
            row["window"] = None
            row["qualifying_accuracy"] = None
            row["unlocked_at"] = None if is_safety_gate else configured_at
    transaction.atomic_write_text(path, json.dumps(state, indent=2) + "\n")


def render(root: Path, settings: dict[str, object], configured_at: str) -> None:
    thresholds = root / "copilot-thresholds.json"
    if thresholds.is_file():
        _render_thresholds(thresholds, settings, configured_at)
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
