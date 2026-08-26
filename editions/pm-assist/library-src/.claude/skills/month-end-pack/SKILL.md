---
name: month-end-pack
effort: medium
description: "Assemble the Month-End Pack: financial close rows, compliance rows, KPI roll-up, and the inputs the owner report pack reads. Use at month-end, on the financial review window, or when the PM asks for the monthly picture."
triggers: ["month end", "month-end pack", "monthly close", "monthly numbers", "close the month", "monthly compliance", "financial review", "monthly roll-up"]
---

# Month-End Pack

The monthly picture, assembled by you and signed off by a human before anything reaches an owner.

## Sequence (this order is load-bearing)

1. **Financial rows pulled** — from the accounting system named in `seat-config.platform.accounting_system`, with source and pull time on every row
2. **Financial review and sign-off** — by {{property_manager_name}} <!-- A2: who holds the Property Manager seat -->, inside the window in `seat-config.owner_reporting.financial_review_window_days`. **Nothing sends before sign-off**
3. **Owner draws** — on the configured draw day, executed by the money side. You surface the schedule; you never move money
4. **Owner report pack staged** — assembled and released by day {{owner_report_day}} <!-- D6: day of the month the owner report pack goes out -->. See `owner-report-pack`

Compressing this sequence — staging the pack before sign-off, or letting a draw land before review — is the failure this ordering prevents.

## What goes on the tab

**Financial**
- Rent roll, collected, past due, delinquency percentage against target (derived, inputs named)
- Owner reserves per unit, with anything below {{owner_reserve_minimum}} <!-- B5: minimum owner reserve per unit --> flagged
- Open trust-account variances, their age against the resolution window, and anything above {{trust_variance_broker_threshold}} <!-- B14: dollar size that goes straight to the broker --> already routed to {{broker_name}} <!-- A3: principal broker or company owner -->
- Invoices in queue past the B12 limit
- Month-over-month movement on each, with both pull times

**Compliance** — from `compliance-calendar`
- Every state-required filing, registration, or inspection deadline landing this month or next
- Notice-template review dates coming due
- Tenant-file retention actions due
- Anything whose underlying state-law answer is still unconfirmed: listed as **not live**, never as "compliant"

**KPI roll-up** — from `kpi-scorecard`
- Occupancy, work-order close rate within SLA, renewal rate, owner retention, lease-expiry concentration
- Days vacant and days to make-ready against target
- Each against its configured target, each sourced and pull-timed

**Exceptions**
- Everything still open in Escalation Triage at month close, with age and owner
- Every red promise from the Follow-Through Log
- Every discrepancy still unresolved, both values shown

## Never

- Never present a KPI without its source and pull time
- Never close a compliance row on inference — a filing is done when there is proof of filing
- Never smooth a month-over-month movement, and never explain a bad number. The numbers are yours; the framing is the PM's
- Never let the pack leave before financial sign-off, even if the report day is tomorrow. A late pack with a signature beats an on-time pack without one — say so and let the PM decide

## Logging

```bash
cortextos bus log-event action month_end_pack_assembled info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","signed_off":<true|false>,"compliance_open":<n>,"kpis_off_target":<n>}'
```
