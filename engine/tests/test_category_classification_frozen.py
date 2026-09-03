"""FROZEN category classification (piper PR18 seat finding).

The completeness casualty proves every copilot category is classified SOMEWHERE;
it cannot see a category classified WRONGLY, because moving a name moves both
sides of a self-consistency check. This file is the SECOND COPY on purpose: a
literal map of every category name to the class it was judged into and the
description it was judged on. Moving a category in engine/autonomy.py now
requires editing this file by name, with the description in front of the editor.

Classes: EXTERNAL_SEND = a resident/prospect/owner/vendor-facing send, gated by
the member's messaging choice; INTERNAL = no external recipient, earns autonomy
on the ladder; IRREVERSIBLE = never auto-unlocks in any mode.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import setup  # noqa: E402,F401 - same import shape as test_autonomy (engine package path)
sys.path.insert(0, str(ROOT / "engine"))
import autonomy  # noqa: E402

EXTERNAL_SEND, INTERNAL, IRREVERSIBLE = "EXTERNAL_SEND", "INTERNAL", "IRREVERSIBLE"

# name -> (class, the description each category was judged on)
FROZEN = {
    # maintenance-coordinator (GUARDRAILS "Valid categories")
    "lock_change": (INTERNAL, "in-house lock change on a unit; no external message is sent by the act itself"),
    "inhouse_dispatch": (INTERNAL, "assigning an in-house tech to a work order; the earned-autonomy ladder by design"),
    "known_vendor_dispatch": (INTERNAL, "assigning an already-approved vendor to a work order; ladder by design"),
    "emergency_dispatch": (INTERNAL, "dispatching for a true emergency; ladder by design, speed over approval"),
    "new_vendor_assignment": (INTERNAL, "assigning a vendor not yet on the approved list; ladder by design"),
    "resident_comms": (EXTERNAL_SEND, "any message to a resident (routine or diagnostic subtype); the member's messaging choice gates it"),
    "work_order_closure": (IRREVERSIBLE, "closing a work order is irreversible; the member's explicit closure choice gates autonomy"),
    # pm-assist / leasing (GUARDRAILS "Valid categories")
    "templated_owner_update": (EXTERNAL_SEND, "an owner-facing update from an approved template; owner is an external recipient"),
    "owner_statement_delivery": (EXTERNAL_SEND, "delivering an owner statement; owner-facing send"),
    "tenant_scheduling_notice": (EXTERNAL_SEND, "a scheduling notice to a tenant; resident-facing send"),
    "coordinator_status_request": (EXTERNAL_SEND, "a status request sent to a coordinator outside the seat; external recipient"),
    "renewal_offer_send_after_terms_set": (EXTERNAL_SEND, "sending a renewal offer once terms are set; resident-facing send"),
    "board_row_write": (INTERNAL, "writing or updating a row on the operating/pipeline board; no recipient"),
    "decision_log_filing": (INTERNAL, "filing a decision log entry; no recipient"),
    # business-development (copilot-thresholds.json descriptions, PR18)
    "cold_outreach_first_touch": (EXTERNAL_SEND, "the first outbound touch to a prospect who has not engaged; prospect-facing send"),
    "nurture_value_touch": (EXTERNAL_SEND, "a value touch to a nurture-stage lead from the approved library; prospect-facing send"),
    "appointment_reminder": (EXTERNAL_SEND, "the pre-appointment reminder on an appointment already on the calendar; prospect-facing send"),
    "meeting_confirmation": (EXTERNAL_SEND, "confirming a call or appointment already agreed on a live call; prospect-facing send"),
    "intake_form_link_send": (EXTERNAL_SEND, "sending the owner intake form link after an executed agreement; owner-facing send"),
    "post_call_recap": (EXTERNAL_SEND, "the recap of a call that already happened, restating what was agreed; owner-facing send"),
    "alert_triage_note": (INTERNAL, "recording which alert fired, what was done, and the next-action date; no recipient"),
    "internal_status_to_manager": (INTERNAL, "pipeline status, alert digest and review packs to the BD MANAGER inside the company; internal recipient"),
}

SHIPPED = {
    EXTERNAL_SEND: autonomy.EXTERNAL_SEND_CATEGORIES,
    INTERNAL: autonomy.INTERNAL_CATEGORIES,
    IRREVERSIBLE: autonomy.IRREVERSIBLE_CATEGORIES,
}


class FrozenClassification(unittest.TestCase):
    def test_every_shipped_category_matches_its_frozen_class_by_name(self):
        print("ARMED: moving a category between classes in autonomy.py must fail here by name, with the description it was judged on")
        shipped_class = {name: cls for cls, names in SHIPPED.items() for name in names}
        moved = {name: (frozen_cls, shipped_class.get(name), desc)
                 for name, (frozen_cls, desc) in FROZEN.items()
                 if shipped_class.get(name) != frozen_cls}
        self.assertEqual(moved, {}, "category class differs from the frozen judgment "
                                    "(name -> (frozen, shipped, description judged on))")

    def test_frozen_map_and_shipped_sets_name_exactly_the_same_categories(self):
        print("ARMED: a category added to autonomy.py without a frozen judgment, or frozen without shipping, fails here")
        shipped_names = set().union(*SHIPPED.values())
        self.assertEqual(sorted(shipped_names - set(FROZEN)), [], "shipped but not frozen (add the judgment here)")
        self.assertEqual(sorted(set(FROZEN) - shipped_names), [], "frozen but not shipped")

    def test_every_frozen_entry_carries_a_description(self):
        empty = [n for n, (_, d) in FROZEN.items() if not d.strip()]
        self.assertEqual(empty, [])


if __name__ == "__main__":
    unittest.main()
