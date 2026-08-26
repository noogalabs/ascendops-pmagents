---
name: month-end-close
description: "Run the month-end close: confirm every step of the cycle is complete, verify the three-way reconciliation balances, produce the close package, and route the period lock for property-manager approval. The period does not lock over an incomplete or unbalanced month."
triggers: ["month end", "close the month", "month-end close", "period lock", "close package", "lock the period", "monthly close", "close checklist", "backdating"]
---

# Month-End Close

Source: monthly workflow Step 11, days 1-5 of the following month.

---

## The checklist

Every item confirmed, in order. A "mostly" is a no.

- [ ] All rent posted and applied, or explicitly marked delinquent
- [ ] All vendor bills for the month posted
- [ ] All management and leasing fees posted and verified against the agreements
- [ ] All NSF reversals complete
- [ ] All owner draws processed
- [ ] **Three-way reconciliation complete and balanced** — `.claude/skills/trust-reconciliation/SKILL.md`
- [ ] Owner statements reviewed and released
- [ ] Security deposit ledger confirmed intact against the deposit trust balance
- [ ] 1099 tracker updated with the month's payments
- [ ] Delinquency report finalized
- [ ] Archive queue processed per `retention` (B11)

---

## The close package

Run and file, per property where applicable:

- Income and expense report by property
- Delinquency report
- Owner statement summary
- Trust account balance report
- The signed three-way reconciliation

Archive every bank statement, reconciliation report, and owner statement for the month.

---

## The lock

Once the checklist is clean, the period locks in the platform to prevent backdating. **The property manager approves the close and the lock.** This agent prepares the package and routes it.

After the lock, a backdated entry requires written property-manager approval and a documented reason, recorded in the decision log. "It's a small correction" is not a reason.

**Target: month fully closed by the 10th of the following month.**

---

## What blocks a close

| Blocker | Why it blocks |
|---|---|
| Open three-way variance | The whole point of the control |
| Unposted transactions in the period | The lock would freeze an incomplete month |
| A draw or statement still pending | The balance is not final |
| Deposit ledger not tying to the deposit trust balance | A liability gap, not a timing item |

Say which one blocks, with its amount and its owner. A close reported as "waiting on a few things" is not a status.

---

## Hard gates

- This agent does not lock a period, post a closing entry, or approve a close.
- A period never locks over an unbalanced trust account or an incomplete month.
- The close package states what could not be verified, separately from what was verified clean.
