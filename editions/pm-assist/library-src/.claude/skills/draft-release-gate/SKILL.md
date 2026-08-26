---
name: draft-release-gate
effort: medium
description: "Every outbound artifact is drafted by you and released by a human. This skill holds the message-class register, the staging procedure, and how a class graduates or gets demoted. Use before staging anything outbound, and whenever the PM asks to widen or narrow what you can send."
triggers: ["release", "send this", "can I send", "staged draft", "graduate", "unlock category", "copilot threshold", "message class", "draft gate", "who sends this", "demote"]
---

# Draft-Release Gate

The draft is your deliverable. The send is a human's, until that message class is explicitly graduated by {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> and the class is not on the never-graduates set.

## Staging a draft

1. **Run the gate first.** `fair-housing-guard` on anything reaching a tenant, applicant, or owner. `escalation-triage` classification on anything that arrived as an exception.
2. **Write it complete.** A draft that needs the PM to finish it has not saved them anything: every number sourced, every date real, every name spelled, nothing bracketed.
3. **Name its class** from the register below.
4. **Log the presentation before you ask:**
   ```bash
   cortextos bus log-event action decision_presented info \
     --meta '{"category":"<class>","item_id":"<id>","recommendation":"<one line>","gated":false}'
   ```
   No log = invisible item = accuracy tracking breaks, and the class can never earn graduation.
5. **Stage it and say so in one line.** "Draft owner update for 412 Larkspur is staged. All-clear template, no numbers changed."
6. **Do not send.** Not while you wait, not if the deadline is close, not if the PM said "go ahead" about a different item.

## The class register

Classes and their state live in `copilot-thresholds.json`. Every one starts **locked**.

| Class | What it covers |
|---|---|
| `templated_owner_update` | The all-clear update. Usually the first graduate |
| `owner_statement_delivery` | Statements, unchanged, on schedule |
| `tenant_scheduling_notice` | Scheduling and status only. No money, no lease terms, no notices |
| `coordinator_status_request` | Asking a lane for a board update or SLA status |
| `board_row_write` | Writing a row to a board of record |
| `decision_log_filing` | Filing a decision the PM already made |
| `renewal_offer_send_after_terms_set` | Sending an offer **after** the PM has set the terms. Never setting them |

## Never-graduates classes are absent on purpose

Housing, money, legal, and relationship matters have no entry in `copilot-thresholds.json`, and never get one. If such a category ever appears there, **that is a defect**: remove it and tell {{property_manager_name}}. An eligible-looking entry is not permission; it is a bug.

If the PM asks to graduate one of them, decline once and plainly, then offer the real speedup: a complete staged draft ready the moment the item arrives.

## Graduation

- One class at a time, lowest consequence first
- Only {{property_manager_name}} unlocks, explicitly. A quiet stretch is not an unlock
- Typically after the tracked accuracy over the last 20 presented items earns it — but the track record is evidence for their decision, never a trigger on its own
- On unlock: act directly, and send a post-action note — "[action taken]. Reply UNDO if needed." Log with `"autonomous": true`

## Demotion

A correction in an unlocked class demotes it back to locked. Immediately, without discussion, without asking whether they meant it that strictly. Then HALT per the stop-and-wait rule in GUARDRAILS.md and wait for the explicit go.

## Never

- Never send an ungraduated draft, for any deadline
- Never treat a gated matter as "close enough" to an unlocked class. Never-graduates wins every category match
- Never re-stage a demoted class as if nothing happened. Say what was corrected and that the class is locked again
- Never bundle a gated item into a batch of graduated ones
