---
name: daily-pipeline-run
description: "The first thing this seat does every day, and the thing it does on every heartbeat. Carries the alert register — every Critical and Warning condition with its trigger, its owner, and its required action — plus the day-view build and the order work gets done in. Load it at the start of any working session, before the inbox and before the calendar."
triggers: ["daily run", "morning", "start of day", "alerts", "alert register", "alerts dashboard", "what should I work on", "daily view", "critical alert", "warning alert", "end of day", "day view"]
---

# The Daily Run

**Order matters.** Open the ALERTS DASHBOARD first — before email, before the calendar, before anything that feels more urgent because it is louder. The alerts are quiet by design; that is why they need to go first.

---

## The Register

Severity is not a mood. Critical means *worked before mid-morning*. Warning means *worked before end of day*.

### Critical

| Alert | Trigger | Also goes to | Do |
|---|---|---|---|
| Speed-to-lead breach | S0 deal created today, F17 blank | — | Touch it now. Delay here is measurable conversion loss, and it compounds |
| Unsigned agreement — warning | F8=Yes, F10=No, F9 older than `clocks.unsigned_agreement_alert_hours` <!-- D6 --> | Manager | Call. Surface the objection. Re-close |
| Unsigned agreement — escalation | Same, older than `clocks.unsigned_agreement_escalate_days` <!-- D6 --> | Manager | Escalate. Log first. Consider a live conversation rather than another email |
| Overdue follow-up | F16 earlier than today | — | Today. No exceptions and no rescheduling to tomorrow |
| No next action set | G1=Active and F16 blank | — | Set one now. This is a data-quality failure, not a scheduling gap |
| Handoff not confirmed | F10=Yes, G7≠Yes, F11 past the window | Onboarding | Confirm receipt. The owner is waiting on somebody who may not know they exist yet |

### Warning

| Alert | Trigger | Also goes to | Do |
|---|---|---|---|
| Stale stage S0–S4 | A5 at or past that stage's max <!-- D6 --> | — | Move it, or move it to nurture. Do not let it sit at the gate |
| Cold lead | F18 at or past `clocks.cold_lead_days_no_touch` on any S0–S4 deal <!-- D5 --> | — | A real touch. Not a nudge |
| Nurture gone quiet | G1=Nurture, F18 at or past `clocks.nurture_no_touch_alert_days` <!-- D5 --> | — | Re-engage or archive |
| Decision-makers unconfirmed | Appointment within the pre-appointment window, F5≠Yes | — | Confirm all of them, or move the appointment |
| Ownership unverified pre-appointment | Appointment within the window, B10 ≠ Yes <!-- A2 --> | — | Verify against the tax record before the appointment |
| Appointment no-show | F3 = yesterday, F4 = no-show | — | Call within the hour. Rebook the same day |
| Discovery no-show | F1 = yesterday, F2 = no-show | — | Call within the hour. Rebook or move to lost |
| Referral fee unpaid | G1=Won, D3=Yes, G9=No, G2 past the window <!-- B9 --> | {{referral_fee_payer}} <!-- C7 --> | Flag it by name. Referral relationships are built on this being boring and on time |
| Pipeline below minimum | Active pipeline doors under `activity_targets.pipeline_minimum_multiple` × the monthly door goal <!-- D8 --> | Manager | Raise prospecting volume now. This one does not wait for the weekly review |
| No new leads this week | Zero deals created in seven days | Manager | Prospecting has stopped. Find out why before finding out how much |
| Archive eligible | Per the archive triggers in `stage-gates` | Manager on the two that need it | Review and archive |

---

## Build The Day View

Pull from PIPELINE - ACTIVE where **any** of these is true: F16 due today or overdue · F18 at or past the cold threshold · A5 at or past the stage max · F3 is today · agreement sent and unsigned past the window · active with F16 blank.

Show only: deal id, owner name, mobile, address, stage, days in stage, motivation, next action, next action due, days since touch, last touch, agreement sent, notes.

Sort: **hot motivation first**, then oldest next-action date, then longest days-in-stage.

---

## Working The Day

1. Alerts dashboard. Every Critical before mid-morning.
2. Speed-to-lead on everything that arrived overnight — see `lead-intake`.
3. Top to bottom through the day view: hot, then warm, then cold.
4. **After every call or touch**: F17 last touch, F15 next action, F16 due date. Before the next call, not at end of day. The board is only true if it is written while the conversation is fresh.
5. Prospecting block against the daily call floor <!-- D7 -->.
6. End of day: every Warning worked. **Zero active deals with F16 blank.**

---

## Two Rules About The Alerts Themselves

**No alert carries across two consecutive days** without a logged action and a new next-action date. If one does, the alert is not the problem — surface it.

**An empty alerts tab at end of day is the goal, and an empty alerts tab at 9am is a warning sign.** It usually means a computed column stopped computing, not that the pipeline is perfect. Check A5 and F18 are actually updating before believing a clean board. A stale formula reads as a healthy zero, and that is the most expensive number here.

---

## What Never Happens On A Daily Run

- Nothing owner-facing leaves without release. Working an alert produces a *staged* message, not a sent one — see `draft-release-gate`.
- Nothing owner-facing leaves at all in shadow mode, or in night mode.
- No alert is closed by deciding it is not really a problem. It is closed by an action and a new date.
