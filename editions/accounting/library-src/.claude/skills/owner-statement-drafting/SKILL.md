---
name: owner-statement-drafting
description: "Draft owner statements that explain themselves: opening balance, income received, expenses paid, fees charged, reserve activity, and net distribution, with every line traceable to a source record. Statements never release over an unreconciled trust account, and no statement goes out without property-manager approval."
triggers: ["owner statement", "monthly statement", "statement drafting", "owner report", "statement release", "explainable statement", "statement review", "owner ledger summary"]
---

# Owner Statement Drafting

Source: monthly workflow Step 8, plus judgment scenario 13.

---

## Preflight — must all be true before drafting

- all income for the period is posted
- all vendor bills for the period are posted
- all management and leasing fees are posted and verified against the agreements
- every NSF reversal is complete
- no pending item would change the balance
- **the three-way trust reconciliation balances**

If the last one is false, stop. See below.

---

## What a statement carries

| Section | Content |
|---|---|
| Opening balance | Prior period ending, tied to the prior statement |
| Income received | Rent and other receipts, by property, collected in the period |
| Expenses paid | By category, each traceable to an invoice and a work order |
| Fees charged | Management, leasing, and other agreement fees, itemized |
| Reserve activity | Movement against the reserve floor, and the ending reserve |
| Net distribution | Available balance minus reserve minus any authorized holdback |

Every line answers where the number came from. An owner who asks "what is this $340" gets an invoice number and a work order, not a category name.

---

## The hard rule: unreconciled means no release

`policy.owner_statement_release_day` (B10) and the reconciliation date have to agree. Statements do not release while the trust account is unreconciled — not "we'll fix the variance after," not "it's only $12."

### Scenario 13 — it is statement day and the three-way does not balance

**Do right now.** Do not send. Notify the property manager that statements will be delayed. Begin the systematic trace: bank vs ledger first, then ledger vs the sum of sub-ledgers. Isolate which leg is off. Check timing items, unposted transactions, and any manual entry made during the period.

**Never.** Never send statements over an unbalanced trust account. Never post a plug entry to force balance. Never tell owners statements are "on the way" when the account does not reconcile.

**Escalate when.** Immediately on discovery. The property manager communicates the delay. A large or unexplained variance may pull in the broker or an outside accountant.

**Write down.** Date discovered, which leg is off, amount, steps taken, resolution, and the date statements ultimately went out. Decision-log scenario S13.

---

## Review and release

The property manager reviews the full month's statements before any of them go out — the month-end "owner statement pre-send review." Then, and only then, statements publish to the owner portal or send by the configured method.

This is an external financial send. It is approval-gated and it is in the `never_graduate` set.

---

## Hard gates

- This agent does not publish, email, or portal-post a statement.
- A statement never leaves over an open variance.
- No line on a statement carries a number that was not re-derived from source this cycle.
- Owners see statements and ledgers read-only; they never initiate a transaction.
