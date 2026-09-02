---
name: stage-gates
description: "Load this before moving any deal between stages, and whenever you are unsure whether a deal has actually earned its next stage. It carries entry criteria, exit criteria, required fields, and the maximum days for every stage from S0 through handoff, plus the terminal lanes and the archive rules. A stage move without its required fields is the most common way this board stops being true."
triggers: ["stage", "move stage", "advance", "S0", "S1", "S2", "S3", "S4", "S5", "S6", "won", "lost", "nurture", "redirect", "archive", "stage gate", "required fields", "can I advance", "max days in stage"]
---

# Stage Gates

Stages in order: **S0 New Lead → S1 Discovery Scheduled → S2 Discovery Completed → S3 Appointment Scheduled → S4 Appointment Held → S5 Agreement Sent → S6 Handoff → WON**, with **LOST**, **REDIRECT**, **NURTURE**, and **ARCHIVE** as terminal lanes.

**The rule that makes stages mean something:** a deal moves when it *meets the exit criteria*, not when it feels like it has moved on. A deal parked one stage ahead of where it really is hides from exactly the alert built to catch it.

Whenever the stage changes, **A6 date-entered-stage is updated in the same write.** A5 days-in-stage is computed from A6, and every stale alert is computed from A5.

---

## S0 — New Lead
No live contact yet.

| | |
|---|---|
| Entry | Inbound inquiry arrives, or an outbound prospect is logged |
| Required | A2 date created, B1–B4 contact, C1 address, D1 source, D5 inbound/outbound |
| Action | Respond inside the speed-to-lead window on inbound; log the attempt immediately on outbound |
| Exit → S1 | Live contact made **and** a discovery call is on the calendar |
| Exit → LOST/ARCHIVE | No response after the configured attempts over the configured window <!-- D5 --> |
| Max days | `clocks.stage_max_days.S0` <!-- D6 --> — alert if no live contact |

## S1 — Discovery Call Scheduled

| | |
|---|---|
| Entry | Spoke with the owner; call date and time confirmed |
| Required | F1 call date, F16 next action due date |
| Action | Recap staged within minutes of the call; confirmation touch same day |
| Exit → S2 | Call held and qualification complete |
| Exit → S0 | No-show or reschedule — reset and rebook |
| Exit → LOST | Cancelled and declines to rebook |
| Max days | `clocks.stage_max_days.S1` <!-- D6 --> |

## S2 — Discovery Call Completed

| | |
|---|---|
| Entry | F2 = Yes; every Block E field populated |
| Required | E1–E6, C1–C16, D1, E10 started |
| Action | Start the rental analysis; identify **all** decision-makers; decide PM vs redirect; book the appointment |
| Exit → S3 | Appointment booked, analysis in progress |
| Exit → REDIRECT | Better fit for another department <!-- C8 --> |
| Exit → NURTURE | Not ready; timeline well out |
| Exit → LOST | Fails the gates: under minimum rent, outside the service area, condition <!-- A3, A4 --> |
| Max days | `clocks.stage_max_days.S2` <!-- D6 --> |

## S3 — Appointment Scheduled

| | |
|---|---|
| Entry | F3 populated; **all decision-makers confirmed to attend** |
| Required | F3, F5 = Yes, E10 range, F6 analysis sent or in progress |
| Action | Finish the analysis; run the pre-appointment touches; **verify ownership against the tax record** <!-- A2 --> |
| Exit → S4 | Appointment held |
| Exit → S3 | Rescheduled — update F3, restart the touches |
| Exit → NURTURE | Postponed indefinitely |
| Max days | `clocks.stage_max_days.S3` <!-- D6 --> |

> **F5 is a gate, not a note.** An appointment where one decision-maker is missing is not held, it is a preview — and the second conversation starts from zero.

## S4 — Appointment Held

| | |
|---|---|
| Entry | F4 = Held; analysis, services, and pricing presented; close attempted |
| Required | F4, E10, F12 package discussed, F13 fee discussed, G10 notes from the appointment |
| Action | Signed on the call → S6 immediately. Not signed → agreement out **the same business day**, hard follow-up inside 24 hours |
| Exit → S5 | Agreement sent, unsigned |
| Exit → S6 | Signed on the call |
| Exit → LOST | Declines and closes the conversation |
| Exit → NURTURE | Interested, timeline pushed |
| Max days | `clocks.stage_max_days.S4` <!-- D6 --> — the shortest gate on the board |

## S5 — Agreement Sent, Unsigned
**The highest-risk stage. Deals die here, quietly.**

| | |
|---|---|
| Entry | F8 = Yes; F9 populated |
| Required | F8, F9, F15, F16 (within 24 hours) |
| Action | Follow up by call inside 24 hours; surface the remaining objection; re-close |
| Escalate | Past `clocks.unsigned_agreement_escalate_days` → {{bd_manager_name}} <!-- D6, C2 --> |
| Exit → S6 | Signed |
| Exit → LOST | Declines after follow-up |
| Exit → NURTURE | Wants to wait |
| Alerts | Warning at `clocks.unsigned_agreement_alert_hours`; escalation at the escalate window <!-- D6 --> |

## S6 — Handoff In Progress

| | |
|---|---|
| Entry | F10 = Yes; F11 populated; **ownership entity verified and matching** <!-- A2, A5 --> |
| Required | F10, F11, F12, F13, G7, G8 |
| Action | Full handoff package — see `pma-and-handoff` |
| Exit → WON | Intake form received; onboarding has made first contact; G7 = Yes |
| Alert | Handoff unconfirmed past its window → the seat **and** the manager |
| Max days | `clocks.stage_max_days.S6` <!-- D6 --> |

---

## Terminal Lanes

### WON
Entry: G7 = Yes and onboarding confirmed receipt. Required: G2, F11, F12, F13, D3, G9. Then: final notes, referral fee flagged to {{referral_fee_payer}} <!-- C7 -->, row to CLOSED WON. Retained permanently — it feeds every conversion number forever <!-- A9 -->.

### LOST
Entry: the owner confirmed they are not proceeding. Required: G3, G4 lost reason, G5 if they chose a competitor. Then: staged decline message, add to re-engagement nurture where appropriate <!-- D5 -->, row to CLOSED LOST. Retained per the configured window; eligible to re-enter if the owner comes back.

> **G4 is a business field.** A protected-class matter never lands here — it is routed by escalation id. See `fair-housing-guard`.

### REDIRECT
Entry: E6 = brokerage or investment redirect. Required: G6, G10. Warm handoff to the named recipient <!-- C8 -->, then the REDIRECTED tab. Tracked in case it becomes a PM deal later.

### NURTURE
Entry: engaged, timeline pushed. **Required: F16 must be set.** There is no open-ended nurture. F20 = Yes. Touch on the configured schedule <!-- D5 -->. Exits back to active on re-engagement, or to ARCHIVE when nurture is exhausted <!-- D5 -->. Alert at `clocks.nurture_no_touch_alert_days`.

---

## Archive Rules

| Record | Trigger | Who approves |
|---|---|---|
| Unresponsive lead | No live contact after the configured attempts and window <!-- D5 --> | Seat |
| Lost, no re-engagement expected | After the configured retention window <!-- A9 --> | Seat + manager |
| Hard no — asked never to be contacted | **Immediately** | Seat |
| Nurture exhausted | Configured touches over the configured window <!-- D5 --> | Seat + manager |
| Disqualified | On disqualification | Seat |
| Duplicate | On discovery — merge notes into the survivor first | Seat |
| Redirect confirmed handled | After the configured window with no PM re-engagement | Seat |
| Won and fully onboarded | After the configured post-handoff window | Onboarding confirms |

**Required before anything archives:** G1 final status · G2 or G3 date · G4 lost reason (all LOST records) · G5 if competitor · G10 closing note · D1 lead source · D3 resolved · G9 = Yes or N/A · B10 whatever was determined.

Archive rows are read-only. Additional archive columns: date archived, archived by, archive reason, re-engage eligible, re-engage date.

**Never delete instead of archiving.** The one exception is a duplicate, after its notes are merged, per the retention schedule <!-- A9 -->.

### Quarterly archive audit
Any re-engage dates landing this quarter → back to nurture. Any disqualified properties whose condition may have changed → re-qualify. Any records missing required fields → complete them. And the diagnostic question: **is the archive growing faster than the wins?** If it is, the problem is upstream of the archive.
