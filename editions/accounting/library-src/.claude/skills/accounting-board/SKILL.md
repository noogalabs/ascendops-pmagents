---
name: accounting-board
description: "Maintain the bookkeeping tracking board: one row per financial event, the status lifecycle and who moves each status, the daily/weekly/month-end views, and the alert thresholds that fire off it. Spreadsheet-first by design. Append rows and update cells; never rewrite a tab in place — a lost audit-log column is unrecoverable."
triggers: ["board", "tracking board", "board row", "item ID", "board view", "alerts", "conditional formatting", "board status", "dashboard", "board hygiene", "archive queue"]
---

# Bookkeeping Tracking Board

Source: the Bookkeeping Tracking Board. Location: `platform.board_location` (D6). One row per financial event; the row lives until archived.

---

## Row structure (34 columns)

| Group | Columns |
|---|---|
| Identity | Item ID, Item Type, Property, Owner, Tenant, Lease Month, Due Date |
| Money | Amount Expected, Amount Received/Paid, Variance (formula), Payment Method, Trust Account |
| State | Status, Delinquency Day Count (formula), NSF Flag, Late Fee Applied, Notice Issued |
| Approval | PM Approval Required, PM Approval Status, PM Approval Date |
| Compliance | W-9 on File, Reserve Balance, Reserve Floor, Reserve Alert (formula) |
| Deposits | Deposit Deadline, Deposit Deadline Status (formula) |
| Reconciliation | Reconciled to Bank, Reconciled to Ledger, Reconciled to Trust Register, Three-Way Rec Status (formula) |
| Admin | Assigned To, Notes / Audit Log, Archive Date, Archive Status |

**Item types:** Rent Charge, Payment Received, NSF, Late Fee, Security Deposit, Deposit Disposition, Owner Disbursement, Vendor Bill, Reserve Replenishment, Management Fee, W-9 Flag, Reconciliation Variance, Eviction Cost, HOA/Tax Payment, Misc Credit.

**Trust Account** is populated on every row and takes exactly one value — Operating Trust, Security Deposit Trust, or Reserve Account. A row never spans two. That single constraint is how no-commingling shows up structurally rather than as a policy nobody checks.

---

## Views

### Bookkeeper daily
Unpaid Today · Delinquency Counter · NSF Queue · Notices Due · PM Approvals Pending · Deposit Deadline Watch · Unreconciled Payments · Reserve Floor Alerts

### Property manager weekly
My Approval Queue · Delinquency Summary · Disbursements This Week · Overdue Deposits · W-9 Missing · Reserve Health · Legal Items

### Month-end, together
Three-Way Rec Status Board · Variance Report · Full Delinquency Roll · Owner Statement Pre-Send Review · Deposit Trust Audit · Reserve Reconciliation · W-9 / 1099 Readiness · Archive Queue

---

## Alerts that fire off the board

| Alert | Trigger | To | Urgency |
|---|---|---|---|
| Delinquency day 1 | Day count = 1 | Bookkeeper | Info |
| Grace period ending | Day count = `state_rules.late_fee_grace_days` (A1) | Bookkeeper | Warning |
| Notice required | Day count = A1 + 1 | Bookkeeper + PM | Action |
| Legal escalation window | Day count in `state_rules.eviction_filing_decision_days` (A11) | PM | Action |
| NSF received | NSF flag flips to Yes | Bookkeeper + PM | Immediate |
| NSF second occurrence | Prior NSF, same resident, last 12 months | PM | Escalate |
| Reserve below floor | Balance < `thresholds.reserve_floor` (B3) | Bookkeeper + PM | Warning |
| Reserve critically low | Balance < half the floor | PM | Action |
| Deposit deadline in 3 days | Deadline − today ≤ 3 | Bookkeeper | Warning |
| Deposit deadline passed | Today > deadline, not returned | Bookkeeper + PM | Legal risk |
| W-9 missing at disbursement | W-9 on File = No | Bookkeeper | Hold disbursement |
| Unreconciled variance | Variance ≥ `thresholds.variance_alert_amount` (B6), age > `variance_alert_age_days` | Bookkeeper | Warning |
| Unreconciled over 7 days | Three-Way Rec Status open > 7 days | PM | Escalate |
| PM approval pending > 24h / > 48h | Approval age | PM | Reminder / Action |
| Owner disbursement not sent | Past `policy.owner_draw_deadline_day` (B8), status not Disbursed | Bookkeeper + PM | Action |

Any alert whose driving value is unanswered in `accounting-config.json` is **disabled and reported as disabled**, never silently skipped.

---

## Archiving

Per `retention` (B11) and the board's archive triggers: rent charges 90 days after payment confirmed; NSF items 90 days after cleared; deposits 30 days after disposition confirmed; vendor bills 60 days after reconciled; owner disbursements at fiscal year end plus a month; write-offs immediately after PM approval; W-9 records annually after the 1099 is filed.

Archive means status change plus archive date. It never means delete.

---

## Hygiene rules

- **Append, never rewrite.** Never regenerate a tab in place; the Notes / Audit Log column is unrecoverable if lost.
- Every Notes entry is date-stamped.
- A manual override of a formula column requires an audit-log entry with the date and the name of whoever made it.
- No account numbers, routing numbers, or payment instruments on the board.

---

## Hard gates

- This agent updates board rows and produces views. It does not move a row to Disbursed, Approved, or Paid on its own authority — those transitions follow a human action, they do not precede one.
- If the board does not exist yet, building it is a phase-zero task, and this agent watches nothing until it does.
