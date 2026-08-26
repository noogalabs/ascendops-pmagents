---
name: daily-money-review
description: "Run the bookkeeper's recurring review: the daily queue (payments, NSF alerts, delinquency day counts, new invoices, trust alerts), the weekly sweep (escalation status, bill aging, reserve floors, W-9 gaps, contributions, deposit deadlines), and the month-end list. This is also the money-critical sweep that runs on every heartbeat and every session start. Draft and flag only — never post, never pay."
triggers: ["daily review", "money sweep", "money-critical sweep", "daily digest", "morning check", "weekly sweep", "what needs attention", "payment queue", "daily dashboard", "bookkeeper review", "recurring review"]
---

# Daily Money Review

The seat's heartbeat. Runs every weekday morning on cron, and again as a shortened sweep on every heartbeat cycle and session start. Nothing here writes to a ledger or moves a dollar.

Every threshold below reads from `accounting-config.json`. If a value is unanswered, that check is DISABLED — say so in the digest rather than substituting a default.

---

## The money-critical sweep (runs first, always)

In this order. Stop and escalate on the first red before continuing.

| # | Check | Red condition | Action |
|---|---|---|---|
| 1 | Unrecognized trust transaction | Any debit, wire, ACH pull, or check nobody initiated | Drop everything. `.claude/skills/fraud-and-unauthorized-transactions/SKILL.md` |
| 2 | Three-way balance | Any open variance | If statements are due, they do not release. `.claude/skills/trust-reconciliation/SKILL.md` |
| 3 | Deposit clocks | Any disposition inside its warning window or past its deadline | `.claude/skills/security-deposit-accounting/SKILL.md` |
| 4 | Returned payments | Any NSF or ACH reject since the last cycle | `.claude/skills/returned-payments/SKILL.md` |
| 5 | Suspense | Anything unidentified; same-day escalation at or above `thresholds.unidentified_payment_escalation_threshold` (B4) | `.claude/skills/suspense-and-unmatched-payments/SKILL.md` |
| 6 | Vendor banking requests | Any change request received | Freeze payments to that vendor immediately. `.claude/skills/vendor-banking-change/SKILL.md` |
| 7 | Reserve floors | Any owner ledger below `thresholds.reserve_floor` (B3) or its per-owner override | `.claude/skills/owner-contributions/SKILL.md` |
| 8 | Approvals aging | Pending more than 24h (remind) / 48h (escalate) | Escalate immediately if a statutory deadline sits inside the window |

---

## Daily queue (source: monthly workflow, Bookkeeper Recurring Review Schedule — Every Day)

- **Payment queue** — new payments received, applied, or pending. Every payment that does not match exactly gets flagged, not forced.
- **NSF / returned payment alerts** from the bank.
- **Delinquency list** — who is unpaid and what day they are on.
- **New vendor invoices** received. Log each one the day it arrives.
- **Trust account alerts** or unusual transactions.

---

## Weekly sweep (source: Every Week)

- Delinquency escalation status — are notices going out on time against `state_rules.late_fee_grace_days` (A1) and `state_rules.nonpayment_notice_days` (A3)?
- Vendor bill aging — any approved invoice not yet paid, measured against `policy.vendor_payment_run_dates` (B9).
- Owner ledger balances approaching or below the reserve floor.
- 1099 tracker — any vendor paid without a W-9 on file.
- Pending owner contributions — have they cleared?
- Security deposit tracker — any move-out with an approaching disposition deadline.

---

## Month-end list (source: Every Month End)

- Three-way trust reconciliation complete and balanced
- Every owner statement reviewed before release
- Management and leasing fees verified against the management agreements
- Delinquency report finalized
- 1099 tracker updated with the month's payments
- Security deposit ledger confirmed intact
- Period locked

---

## The digest

One message, plain, to the human bookkeeper (`roles.human_bookkeeper`, C3), copied to the property manager when anything is red.

Shape it as: **what is red, what is amber, what is clean, what needs a decision from whom by when.** Lead with the decision if there is one. A clean sweep is still worth one line — "clean" is a result; silence is not.

Never put an account number, a routing number, or a payment instrument in the digest.

---

## Hard gates

- Nothing in this skill posts, pays, applies, reverses, or sends. It reads, computes, and flags.
- A number in the digest was re-derived from source this cycle. A remembered figure is not a read figure.
- A disabled check is reported as disabled, never as clean.
