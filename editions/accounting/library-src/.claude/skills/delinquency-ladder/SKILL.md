---
name: delinquency-ladder
description: "Run the delinquency escalation ladder from grace-period expiry through the eviction decision window: confirm late fees posted correctly, track notice clocks against state law, prepare the delinquency file, and hold every payment that lands on a noticed or filed account. The agent tracks and drafts; the property manager decides and the attorney files."
triggers: ["delinquency", "late fee", "late notice", "pay or quit", "demand letter", "nonpayment", "eviction", "notice served", "delinquent account", "past due rent", "escalation ladder", "unpaid rent", "day count"]
---

# Delinquency Ladder

Source: monthly workflow Step 3, plus judgment scenarios 3 and 12.

Every clock in this skill is a state-law clock. It reads from `accounting-config.json` → `state_rules`, and **a value with `confirmed: false` disables its check.** Do not substitute a common default for an unconfirmed legal value; flag it and name the question.

---

## The ladder

| Day | What happens | Who |
|---|---|---|
| End of grace period (`state_rules.late_fee_grace_days`, A1) | Platform auto-posts the late fee per the lease | Agent confirms it posted, and posted correctly against the cap in `state_rules.late_fee_cap` (A2) |
| Day 5 | First written late notice: amount owed, late fee, payment instructions | Bookkeeper sends; agent drafts |
| Day 7–8 | Still unpaid: property manager notified, owner notified | Agent flags; PM communicates |
| Day 10 | Second notice / demand letter, from the attorney-reviewed template | Bookkeeper sends; agent drafts |
| Day 15–20 | Delinquency file prepared and handed to the property manager for the file-or-hold decision | Agent prepares; PM decides |
| Day 15–20 | Written owner authorization to file | PM, then owner |
| Beyond | Eviction filed | PM or `roles.eviction_attorney` (C5) |

**Time targets.** First notice within 24 hours of grace-period expiration. File-or-hold decision by the window in `state_rules.eviction_filing_decision_days` (A11), so no account ages without a decision.

---

## The delinquency file

When an account reaches the decision window, hand the property manager a file that decides itself:

- Full ledger history for the tenancy
- Every notice sent, with dates and method of service
- Payment history including any partial payments and how each was handled
- Current balance broken into rent, late fees, and other charges
- The applicable notice period (A3) and notice type (A4) for that property's jurisdiction
- Days elapsed against the statutory clock, stated as calendar dates rather than day counts

---

## The two payment situations that stop everything

### Partial payment after a notice was served (scenario 3)

**Do right now.** Stop. Do not post. Pull the notice, pull the lease, pull the state rule in `state_rules.partial_payment_voids_notice` (A5). Flag immediately.

**Never.** Never post a partial payment after a notice without the property manager's authorization. In many states accepting payment voids the notice and restarts the clock.

**Escalate when.** Every single time, without exception.

**Write down.** Date the notice was served, date the payment was received, amount, PM decision, whether the payment was accepted or returned, and the method of return. Decision-log scenario S3.

While A5 is unconfirmed, the working rule stands regardless: every payment on a noticed account is flagged before it is applied.

### Payment received after an eviction was filed (scenario 12)

**Do right now.** Do not post. Do not deposit. Contact the property manager immediately.

**Never.** Never accept or post a payment after filing without the property manager and counsel signing off. In many states accepting any payment after filing dismisses the case or creates a new tenancy. This is not a bookkeeper decision under any circumstances.

**Escalate when.** Immediately — before the check is deposited, before the portal payment is acknowledged.

**Write down.** Date received, amount, method, time the PM was notified, whether the attorney was consulted, final disposition of the payment. Decision-log scenario S12.

---

## Late fee discipline

- A late fee posts only if the lease carries it and the state allows it at that amount.
- Check the posted amount against `state_rules.late_fee_cap` (A2). A fee above the cap is a company exposure, not a rounding question.
- A waived fee requires the authority named in `policy.waiver_and_writeoff_authority` (B12), in writing. Never on a verbal.

---

## Hard gates

- This agent does not post a fee, send a notice, apply a payment, or file anything.
- The file-or-hold decision belongs to the property manager. The agent supplies the file and the clock, never a recommendation to file.
- Collections conversations, payment plans, and negotiation belong to the property manager. This agent emits facts: unit, resident, amount short, days late, last payment, notices served and when.
- No statement of a state-law rule goes out that has not been confirmed with counsel.
