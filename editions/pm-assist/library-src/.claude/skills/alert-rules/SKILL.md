---
name: alert-rules
effort: medium
description: "The threshold register across maintenance, leasing, delinquency, financial, and compliance, plus which fire automatically and which are a named person's manual duty. Run the pass every heartbeat; read it whenever a threshold question comes up."
triggers: ["alert rules", "threshold", "alert fired", "which alert", "sla breach", "alert pass", "auto flag", "manual flag", "alert owner", "does this trip"]
---

# Alert Rules

The register. Every rule has a value, a source question, and a **named human** at the end of it.

Run the full pass every heartbeat (HEARTBEAT.md Step 7b) and again during the Daily Pulse build.

## Auto vs manual

`seat-config.platform.auto_alert_rules` lists what {{pm_platform}} <!-- D1: property management platform --> flags on its own. Everything else is a named person's manual duty in `seat-config.platform.manual_alert_flags`.

**An alert with no owner does not exist.** A rule with no named person is `UNRESOLVED` — it goes into Escalation Triage and the calibration digest and stays there until someone is named. It is never a rule you silently watch yourself.

## Maintenance (B12)

| Rule | Value |
|---|---|
| Emergency assigned + resolved | `seat-config.clocks.maintenance_sla.emergency_hours` |
| Urgent | `seat-config.clocks.maintenance_sla.urgent_hours` |
| Routine | `seat-config.clocks.maintenance_sla.routine_days` |
| Invoice unapproved in queue | `seat-config.clocks.invoice_queue_alert_days` |

Cross-seat: if a maintenance agent is installed for the same company, these are its numbers too. A difference between the two is an `unresolved` flag for {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> — surfaced as a pair, never averaged, never silently preferred.

## Leasing (B10)

Listing live after move-out; price review with no showings; price decision with showings but no application; vacancy age escalating to the PM; application decision turnaround. Values in `seat-config.clocks`.

A leasing alert names the leasing coordinator when one exists, and whoever covers that board when one does not (A2).

## Delinquency (A5, B6)

Late-notice day, the no-payment-no-contact alert day, and the portfolio percentage against target. See `delinquency-clock`. The legal half comes from the state-law answers — **if those are unconfirmed, this lane is not live and the alerts do not run.** Say that; do not substitute a hint default.

## Financial (B5, B14)

- Owner reserve below {{owner_reserve_minimum}} <!-- B5: minimum owner reserve per unit --> per unit → flag; the reserve conversation is the PM's
- Trust-account variance open past its resolution window → flag
- Any variance above {{trust_variance_broker_threshold}} <!-- B14: dollar size that goes straight to the broker --> → straight to {{broker_name}} <!-- A3: principal broker or company owner --> regardless of explanation
- Any variance that looks like more than an error → up immediately. State trust law may require notifying the real-estate commission; **that is the broker's call, never yours and never the PM's to skip**

## Compliance (A6, A9, A10)

Every state filing, registration, and inspection deadline inside its lead time; notice-template review dates; retention actions. See `compliance-calendar`.

## Turnover (B11)

Days past target make-ready before escalation, and scope beyond the approved budget — which is a PM approval, and above {{owner_approval_threshold}} <!-- B1: owner pre-approval spend threshold --> an owner approval.

## Renewal (B9)

Pipeline look-ahead, owner decision window, tenant follow-ups, and a flag on any lease inside the window with no action started. See `renewal-pipeline`.

## Firing a rule

1. Compute against the configured value — not a remembered one, not a hint default
2. Land it in Escalation Triage with owner and due date
3. Put anything needing the PM today on the Daily Pulse with a time
4. Draft what the decision needs
5. **Never decide.** A fired alert is a surface, not a verdict

## Never

- Never adjust a threshold to avoid a noisy alert. Noise is a config conversation with the PM
- Never fire on a stale pull without saying the pull is stale
- Never suppress a repeat alert because it fired yesterday. Age it instead
