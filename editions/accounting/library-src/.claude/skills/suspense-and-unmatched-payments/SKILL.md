---
name: suspense-and-unmatched-payments
description: "Handle money that arrives and cannot be matched: unidentified payments, third-party payors not on the lease, disputed receipts, and duplicate payments. Post to suspense, never to a guess. Escalate on a clock. Covers judgment scenarios 1, 2, 10, and 11."
triggers: ["unidentified payment", "unmatched payment", "suspense", "clearing account", "who paid this", "third party payment", "not on the lease", "guarantor payment", "duplicate payment", "paid twice", "tenant says they paid", "receipt I cannot find", "cannot match payment"]
---

# Suspense and Unmatched Payments

Money that cannot be attributed sits in suspense. It never sits in an owner's ledger, and it never gets applied to the closest match to clear a queue.

If `platform.suspense_account` (D5) is false, there is nowhere legitimate to put this money. That is a phase-zero finding, not a workaround to improvise around — hold the item, document it, and escalate.

---

## Scenario 1 — payment matches no ledger

**Do right now.** Post to the labelled suspense / clearing account. Record date received, amount, payment method, memo or reference number. Screenshot the bank entry.

**Never.** Never apply it to the closest-matching account "just to clear it." Never leave it unposted with no record. Never let it sit past three business days without escalation.

**Escalate when.** You cannot identify the source within one business day, OR the amount is at or above `thresholds.unidentified_payment_escalation_threshold` (B4) — in which case the property manager hears about it the same day, not the next.

**Write down.** Date received, amount, method, suspense account used, who was notified, the PM decision, final resolution. Open a decision-log entry (`.claude/skills/pm-decision-log/SKILL.md`, scenario S1).

---

## Scenario 2 — payment from someone not on the lease

A parent, a partner, a friend, a "guarantor" who is not documented as one.

**Do right now.** Hold the payment unposted. Pull the lease. Check whether the payor is listed as a guarantor or an authorized payer. Check the company's third-party payment policy.

**Never.** Never apply a third-party payment without the property manager's sign-off. Never assume a relationship. Never accept cash from an unknown third party without documentation.

**Escalate when.** The payor is not on the lease and not a documented guarantor — every time. This carries legal implications in some jurisdictions and the property manager owns it.

**Write down.** Payor name, relationship claimed, amount, date, PM decision, any written authorization received. Decision-log scenario S2.

---

## Scenario 10 — resident has a receipt you cannot find

**Do right now.** Ask for the receipt. Do not mark the account paid. Check the bank feed, the portal payment log, and the returned / failed payment queue — a payment that bounced looks exactly like a payment that never arrived from the ledger side.

**Never.** Never mark an account paid on a resident's word or a receipt alone. Never dismiss the resident either; a legitimate receipt means the money went somewhere, and finding where is the job.

**Escalate when.** You cannot locate or explain the payment within one business day. The property manager communicates with the resident and, if needed, the payment processor.

**Write down.** Date of the claim, receipt details provided, every search step taken, outcome, PM decision. Decision-log scenario S10.

---

## Scenario 11 — duplicate payment

**Do right now.** Freeze both entries. Trace both to the bank feed. Determine whether one is a portal auto-pay and one is manual, or whether the bank genuinely received two deposits.

**Never.** Never delete a ledger entry. Never apply the duplicate to a different charge without tracing it. Never draft a refund before confirming at the bank that both deposits actually landed.

**Escalate when.** As soon as the duplicate is confirmed. The property manager authorizes the refund method and amount.

**Write down.** Both transaction dates, amounts, methods, the bank's confirmation of one or two deposits, PM authorization, refund date and method. Decision-log scenario S11.

---

## The suspense aging clock

| Age | State | Action |
|---|---|---|
| Day 0 | Received, posted to suspense | Log it, begin research |
| Day 1 | Unidentified | Escalate to the property manager |
| Day 3 | Still unidentified | Hard escalation; it does not age further in silence |

At or above the B4 threshold the clock collapses to same-day at day 0.

---

## Hard gates

- This agent does not post to suspense, release from suspense, or refund. It identifies, drafts, and routes.
- Suspense is a holding account, not a parking lot. Every item in it has a live clock and a named owner.
- A refund is money movement and is approval-gated without exception.
