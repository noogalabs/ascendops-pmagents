---
name: vendor-coordination
description: "Run vendor dispatch with follow-through: pick the right vendor, confirm the window with the vendor BEFORE telling the resident, track every contact attempt in a state log, chase silence on a fixed ladder, sweep for stale work orders daily, and verify the work against the original complaint before close-out. Every outward message is approval-gated per SOUL.md."
triggers: ["vendor", "dispatch", "vendor dispatch", "contractor", "trade dispatch", "vendor follow-up", "vendor acceptance", "vendor silent", "stale work order", "SLA clock", "schedule vendor"]
context: fork
---

# Vendor Coordination

Dispatching is easy. This skill enforces the hard half: that the vendor said yes, has a confirmed window, showed up, did the real work, and that it was verified before anyone was told the problem is solved.

---

## Hard Gates

- **Approval:** vendor dispatch, any vendor-facing message, any resident-facing message, and any PO/quote approval are external actions — check the SOUL.md autonomy rules and copilot-thresholds category status. Locked categories: draft + route for approval; a human releases them.
- **Vendor-before-resident:** confirm with the vendor and get a real appointment window BEFORE you promise the resident any time. A silent vendor is not an accepted vendor. Never tell the resident a job is scheduled until the vendor has confirmed.

---

## Contact Log (state file)

Every outreach attempt to a vendor is logged. Before contacting any vendor, read the log. After contacting any vendor, update it.

**Path:** `.state/vendor-contact-log.json`

```json
{
  "work_orders": {
    "<work_order_id>": {
      "issue": "one-line description",
      "vendor_name": "<vendor>",
      "status": "pending_outreach | outreach_sent | response_received | scheduled | resolved | stale",
      "last_updated": "<ISO8601>",
      "outreach": [
        {"attempt": 1, "when": "<ISO8601>", "method": "platform-thread | sms | call | email", "message": "<what was said>", "response": null, "response_at": null}
      ]
    }
  }
}
```

**Silence ladder (from last attempt, no response):** < 24h → do NOT re-contact. 24–48h → one follow-up eligible. 48h+ → escalate to the property manager with full context. Also log outreach the property manager makes themselves ("I called the plumber") — ask what was said and whether they responded, then record it, so the log reflects ALL contact.

---

## Dispatch Workflow

1. **Select the vendor** from the roster (`cortextos bus kb-query "<trade> vendor" --org $CTX_ORG`): handyman-first; escalate to a licensed specialist or emergency vendor only when the work demands it (serious electrical, structural, or a true emergency; gas goes to the gas utility per SOUL.md, never property-side dispatch).
2. **Assign in the {{platform}} platform** after approval where required. Run the platform skill's assign-vendor command. If there is no match, surface the available names; do not guess.
3. **Message the vendor, NOT the resident** — scope, unit, access, severity, photos; hidden from the tenant so the resident sees nothing until a window is real:
   Run the platform skill's vendor-message command with: "Hi <vendor>, can you take <work summary> at <unit> <proposed window or 'this week'>? Reply with a confirmed window once you've checked your schedule." Keep it hidden from the resident.
   Log the attempt in the contact log.
4. **Track acceptance.** Run the platform skill's read-comments command at heartbeat cadence. Confirmation = an explicit date/time ("we'll be there Tuesday at 10"). A counter-proposal is NOT a confirmation — route the new window for approval before answering. "We can't make it" → surface for a vendor swap. Silence → run the silence ladder.
5. **Only after the vendor confirms:** run the platform skill's schedule-vendor command, then its resident-message command with: "Hi <resident>, <vendor> confirmed they'll arrive <confirmed window>. Please make sure access is available." Keep it hidden from the vendor.
   (Resident message is approval-gated while `resident_comms` is locked.)
6. **Quotes/POs over the approval threshold** (per SOUL.md's approval threshold): draft and route for approval before work proceeds. Push back once on high estimates — ask for wiggle room or a justification you can pass to the owner.
7. **Close the loop:** verify the work against the ORIGINAL complaint with evidence (photos, verified result, or tenant confirmation) via the `closeout-verification` skill. Do not close on "looks done" or "the vendor said so."

---

## Stale Work-Order Sweep (daily)

Catch the slow-bleed items no single snapshot flags:

Run the platform skill's list command for open work orders silent for at least 48 hours.

Bucket by silence age and propose (never auto-send):
- **48–72h silent — WARNING:** draft an on-thread nudge to the assigned tech/vendor.
- **72–120h silent — ESCALATION:** vendor SLA review + alternate vendor consideration; surface to the property manager.
- **>120h silent — CRITICAL:** propose reassign now OR cancel + recreate; ALWAYS surface to the property manager — never decide alone.

Treat tech-silence and vendor-silence differently: tech-silence is an internal management issue; vendor-silence is an SLA issue. "Scheduled" status is NOT proof of progress — scheduled-then-no-show is itself a staleness signal. If all buckets are empty, report "sweep clean" in one line; silence is ambiguous.

---

## Validation (every run)

- No vendor was dispatched and no message was sent without the required approval.
- No resident was promised a time before the vendor confirmed the window.
- Every contact attempt landed in `.state/vendor-contact-log.json`.
- Silent vendors were chased on the ladder, not assumed accepted.
- Close-out is tied to the original complaint with evidence, or the ticket stays open with a reason.
