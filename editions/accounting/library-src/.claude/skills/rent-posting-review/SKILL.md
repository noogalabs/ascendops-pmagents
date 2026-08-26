---
name: rent-posting-review
description: "Review the monthly rent cycle: pre-rent readiness on days 25-28, auto-posted charges on the 1st, and payment application through day 5. Verify every payment matches a ledger exactly, verify the platform applies partial payments in the configured order, and flag every mismatch instead of forcing it. Review only — this agent never posts a charge or applies a payment."
triggers: ["rent posting", "post rent", "rent charges", "apply payment", "payment application", "rent roll", "monthly rent", "pre-rent", "recurring charges", "payment matching", "rent cycle"]
---

# Rent Posting Review

Source: monthly workflow Steps 1 and 2. This agent reviews and flags; the human bookkeeper posts and applies.

---

## Pre-rent readiness (days 25-28 of the prior month)

Before the new month's charges post, confirm:

- The prior month is closed and reconciled. If it is not, say so now — charges posting into an unclosed month compound every later problem.
- Every active resident ledger is zero-balanced and ready to receive the charge, or its non-zero balance is explained.
- Recurring charges are set to auto-post: pet rent, parking, storage, utility billbacks, anything in the lease beyond base rent.
- Rent amounts and lease terms in the platform match the executed leases. A mismatch here is a leasing-seat handoff question, not a silent correction.

Reminders themselves are a policy the property manager set once. This agent confirms they went, it does not decide their content.

---

## Rent posting (day 1)

The platform auto-posts. Verify it actually did:

- Charge count against active lease count. A gap is a lease that did not post, not a rounding issue.
- Charge amounts against lease amounts.
- Recurring charges present where expected.

Anything missing gets flagged the same day. A charge that never posted is invisible delinquency.

---

## Payment application (days 1-5, then daily)

Monitor the payment queue every business day. For each incoming payment (ACH, check, money order, portal):

1. Match it to a resident ledger exactly — name, unit, amount, period.
2. Confirm the platform applied it in the configured order: `policy.payment_application_order` (B7).
3. Flag anything that does not match exactly: wrong amount, wrong unit, unidentified payor, unexpected period.

**Target: payments applied within one business day of receipt.** Aging in the queue is the same as unapplied.

### The four flags that never resolve themselves

| Situation | Route |
|---|---|
| Payment matches no ledger | `.claude/skills/suspense-and-unmatched-payments/SKILL.md` |
| Payor is not on the lease | Hold unposted, pull the lease, check for a documented guarantor. PM decides. |
| Partial payment on an account with a notice served | STOP. Do not apply. `.claude/skills/delinquency-ladder/SKILL.md`. This is the single most common junior mistake in the seat. |
| Payment on an account with an eviction filed | Do not post, do not deposit. Immediate PM escalation. |

---

## Payment application order is a verification question

`policy.payment_application_order` records what the platform is **configured** to do, not what anyone assumes it does. Fees, then past-due rent, then current rent is a common baseline, but the wrong assumption silently misapplies every partial payment in the portfolio and the error only surfaces at a deposit disposition or an eviction.

If the config carries an assumed value rather than a verified one, say so in the first month's digest and ask for the platform confirmation.

Any exception to the configured order requires the property manager's approval — per payment, in writing.

---

## Hard gates

- This agent does not post a charge, apply a payment, or move a payment between ledgers.
- A payment is never applied to the closest-matching account to clear a queue.
- A partial payment on a noticed account is never applied without the property manager's written direction, regardless of what `state_rules.partial_payment_voids_notice` (A5) says, until that answer is confirmed by counsel.
