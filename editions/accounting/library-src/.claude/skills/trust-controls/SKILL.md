---
name: trust-controls
description: "The twelve trust-account controls that protect resident and owner money and protect the broker's license: segregation of duties, dual authorization, no commingling, no cross-owner borrowing, W-9 before first payment, positive pay, monthly reconciliation, deposit deadline tracking, locked periods, vendor change verification, read-only owner access, and the annual internal audit. Plus the do-not-ever list."
triggers: ["trust controls", "trust account", "commingling", "segregation of duties", "dual authorization", "positive pay", "locked period", "backdating", "do not ever", "trust compliance", "license risk", "internal audit"]
---

# Trust Account Controls

Source: monthly workflow, Trust Account Controls, plus the judgment guide's do-not-ever list. These are what this agent is checking for, continuously, in the background of every other skill.

---

## The controls

| Control | What it means here |
|---|---|
| **Segregation of duties** | No single person both approves and executes a payment. The bookkeeper processes; the property manager approves above `thresholds.vendor_bill_approval_threshold` (B1). This agent is on neither side of that line — it prepares. |
| **Dual authorization** | Payments at or above `thresholds.dual_auth_threshold` (B2) need two sets of eyes, in writing, before release. |
| **No commingling** | Company operating funds never touch the trust account. Fees sweep to operating only after they are earned and posted. |
| **No cross-owner borrowing** | One owner's funds never cover another's shortfall. Each sub-ledger stands alone. The most common violation there is. |
| **W-9 before first payment** | No exceptions. |
| **Positive pay** | Where `platform.positive_pay_enrolled` (D4) is true, the bank pays only registered checks. Where it is false and the bank offers it, that is a standing recommendation to the property manager. |
| **Monthly three-way reconciliation** | Completed, reviewed, signed, and retained every month. Non-negotiable. |
| **Deposit deadline tracker** | A live log of every deposit held, move-out date, and statutory deadline. Reviewed weekly, alerted daily. |
| **Locked periods** | Once a month is closed and reconciled, the period locks. No backdating without written property-manager approval and a documented reason. |
| **Vendor change verification** | Any change to vendor banking or payment information is verified by phone before the record changes. The number-one fraud vector in this seat. |
| **Read-only owner portal access** | Owners see statements and ledgers; they never initiate a transaction. |
| **Annual internal audit** | The property manager or a third party reviews trust records, reconciliations, and 1099 compliance once a year, ideally before year-end. |

---

## The do-not-ever list

One page. No exceptions, no context, no "just this once."

1. Never commingle trust funds with company operating funds — not for a day, not for an hour.
2. Never use one owner's funds to cover another owner's shortfall, even temporarily.
3. Never disburse more than an owner's available balance.
4. Never post a payment after an eviction filing without property-manager and attorney sign-off.
5. Never accept or post a partial payment after a notice without property-manager authorization.
6. Never change a vendor's banking information on an email or written request alone.
7. Never pay an invoice without a matching, approved work order.
8. Never send owner statements over an unbalanced trust account.
9. Never post a plug or adjustment entry to force a reconciliation to balance.
10. Never mark a resident account paid on a receipt you cannot verify in the bank.
11. Never refund a duplicate payment without confirming the bank received both deposits.
12. Never delete or alter a ledger entry without written property-manager authorization.
13. Never hold a security deposit past the statutory deadline waiting for a perfect invoice.
14. Never apply an unidentified payment to a random ledger to clear it.
15. Never attempt to investigate or reverse a suspected fraud transaction on your own.
16. Never make any owner-money decision. That authority belongs to the property manager, always.

---

## Where the controls show up on the board

- `Trust Account` is populated on every row; operating and deposit trusts are separate values and a row never spans both.
- `PM Approval Status` must read Approved before any row can move to Disbursed.
- Month-end compares held deposits to the deposit trust bank balance; any gap is a red variance.
- Reserve balance is a running formula; a manual override requires an audit-log entry with date and name.
- `PM Approval Required` is auto-set for every owner disbursement, every vendor bill at or above B1, every write-off, and every eviction cost.

---

## Hard gates

- This agent enforces controls by flagging, never by acting.
- A control that cannot run because a source is missing is reported as not-run, never as passed.
- No control on this list is subject to graduated autonomy.
