---
name: delinquency-clock
effort: medium
description: "Track delinquency against the legal clock and the portfolio target: late-notice day, the no-payment-no-contact alert, and the percentage against target. Use daily, and whenever an account goes past due."
triggers: ["delinquency", "past due", "late rent", "late notice", "pay or quit", "rent roll", "delinquent", "no payment", "collections", "eviction clock"]
---

# Delinquency Clock

Two clocks run side by side: the **legal** clock from Group A, and the **operational** clock from B6. Never confuse them.

## The legal clock (A5) — not yours to run

The late-notice day, the notice type, the cure period, and what must happen before a filing all come from `seat-config.state_rules`, confirmed with counsel.

**If any of those are blank or read "confirm with counsel," this lane is not live.** Say so plainly on the Daily Pulse; do not substitute the questionnaire's hint default. A working default is a starting point for a conversation with an attorney, never a clock the company runs on.

Even when the answers are confirmed: serving a notice, deciding when to serve, and every eviction step are never-graduates. You track dates and prepare from the attorney-reviewed template library in `seat-config.platform.notice_template_location` (D8). You never author a notice outside it, and you never decide to send one.

## The operational clock (B6)

| Rule | Value |
|---|---|
| Late notice goes out | `seat-config.clocks.delinquency_late_notice_day` |
| PM alert: no payment **and** no contact logged | day {{delinquency_alert_day}} <!-- B6: day an account with no payment and no contact alerts the PM --> |
| Portfolio target | `seat-config.clocks.delinquency_target_pct` of rent roll |

Above target alerts {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> **and** {{broker_name}} <!-- A3: principal broker or company owner -->.

## The daily pass

1. Pull the delinquency report. Source and pull time on every row
2. Compute the portfolio percentage as a **derived** number with its inputs named: past due ÷ rent roll, both pull times shown
3. Age each account: days past due, whether a notice went out on the configured day, whether contact is logged
4. Fire the alert on any account at {{delinquency_alert_day}} days with no payment and no contact
5. Anything at a legal milestone → to the PM with the date arithmetic shown
6. Portfolio above target → PM and broker, with the accounts driving it named

## The "no contact" half matters

The alert is **no payment AND no contact logged**. A tenant who is past due but talking, with the conversation logged, is a different situation from silence. Check the contact log before firing — and if a coordinator had the conversation but did not log it, that is a stale-source row against their name, not a reason to fire or to suppress.

## Never

- Never contact a tenant about money owed. Not a reminder, not a "just checking in." That is the PM's or the money side's
- Never state what the law requires. Cite the configured answer and name it as configured
- Never estimate a rent-roll denominator. If two boards disagree on it, that is a `DISCREPANCY` and the percentage reads unavailable
- Never characterize a tenant's situation, reliability, or intent
- Never run a clock derived from an unconfirmed state-law answer
