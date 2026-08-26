---
name: vendor-bill-intake
description: "Log every vendor invoice on arrival, match it to an approved work order before touching payment, apply the approval-threshold matrix, code the expense to the right property and owner, and prepare the payment draft with backup. Never pay an invoice without a matching approved work order and never without a W-9 on file. Covers judgment scenario 4."
triggers: ["vendor bill", "vendor invoice", "invoice", "AP", "accounts payable", "pay vendor", "invoice approval", "no work order", "invoice matching", "expense coding", "payment run", "bill aging"]
---

# Vendor Bill Intake and Payment Preparation

Source: monthly workflow Step 5, plus judgment scenario 4.

---

## Intake

Log every invoice the day it arrives, by whatever channel it arrives on. An unlogged invoice is an invisible payable, and it surfaces as an angry vendor call rather than as a line on an aging report.

Record: vendor, invoice number, date, amount, property, claimed work order, and the channel it came in on.

**Target: logged within one business day of receipt.**

---

## The match

Match the invoice to an **approved work order** before touching payment. The work order is what proves the work was authorized and what the maintenance seat verified.

### No matching work order (scenario 4)

**Do right now.** Do not pay. Log it as `pending: no WO match`. Acknowledge receipt to the vendor and request the work order number. Flag to the property manager the same day.

**Never.** Never pay an invoice without a matching approved work order. Never assume the work was verbally authorized. Never let it age past five business days unresolved.

**Escalate when.** Immediately. The property manager determines whether the work was verbally authorized and now needs retroactive documentation, or whether the invoice is disputed.

**Write down.** Invoice date, vendor, amount, property, date flagged, PM response, work order created retroactively if applicable, payment date once approved. Decision-log scenario S4.

---

## The approval matrix

| Invoice amount | Who approves |
|---|---|
| Under `thresholds.vendor_bill_approval_threshold` (B1) | Standing property-manager authorization, on a matched work order |
| At or above B1 | Property manager approves before payment |
| Emergency repairs, any amount | Property manager authorizes verbally, documented in writing within 24 hours |
| Capital or major repairs | Property manager **and** owner, in writing |
| At or above `thresholds.dual_auth_threshold` (B2) | Dual authorization — two people, in writing, before release |

Two independent flags, checked separately from the amount:

- **Licensing.** At or above `state_rules.contractor_license_threshold` (A15), or from any trade in `state_rules.license_required_trades`, the invoice goes to the property manager for licensing review regardless of amount.
- **W-9.** No W-9 on file means no first payment. Hold and request it. See `.claude/skills/w9-and-1099-tracking/SKILL.md`.

---

## Coding and the payment draft

Once approved, code the expense to the correct property and owner. Then prepare the payment draft carrying:

- the invoice and the matched work order
- the property and owner ledger it codes to
- the owner's available balance after the payment, and whether it clears `thresholds.reserve_floor` (B3)
- the approval reference
- the run date it belongs to, from `policy.vendor_payment_run_dates` (B9)

If the owner's balance will not cover it, do not proceed to the payment run — route to `.claude/skills/owner-contributions/SKILL.md`. Never cover the gap from another owner's funds; that is commingling and there is no temporary version of it.

**Target: payment processed within 3-5 business days of approval.** Fixed run dates are what make the aging alerts mean anything.

---

## Aging

Any approved invoice unpaid beyond 30 days lands on the property manager's monthly numbers. Surface it weekly, before it gets there.

---

## Hard gates

- This agent does not release a payment. It prepares the batch, attaches the backup, and routes the approval.
- No work order, no payment. No W-9, no first payment. No exceptions for a trusted vendor.
- A vendor banking change freezes every pending payment to that vendor immediately — see `.claude/skills/vendor-banking-change/SKILL.md`.
