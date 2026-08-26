---
name: returned-payments
description: "Handle returned payments — NSF checks and ACH rejects — on the same-day clock: confirm the bank return, verify the reversal, check the fee against the lease and the state cap, notify the property manager within two hours, set certified-funds going forward, and restart the delinquency clock. The agent verifies and flags; the bookkeeper reverses."
triggers: ["NSF", "returned payment", "ACH reject", "bounced check", "insufficient funds", "payment reversed", "chargeback", "returned item", "certified funds"]
---

# Returned Payments (NSF / ACH Rejects)

Source: monthly workflow Step 4. A returned payment is a same-day event, not a next-cycle event, because everything downstream of it is wrong until it is reversed — the ledger, the delinquency day count, and any owner draw computed over it.

---

## The sequence

1. **Bank confirms the return.** Not the platform, not an assumption. The bank's notice is the trigger.
2. **Reversal is posted the same day.** The resident ledger goes back to unpaid. The agent verifies the reversal landed and matches; the bookkeeper posts it.
3. **Fee posts only if both are true:** the lease carries an NSF / returned-payment fee, and the amount is at or under `state_rules.nsf_fee_cap` (A10). Check whether that cap applies to ACH returns as well as checks — in many places it does. **Never charge a fee that is not in the lease.**
4. **Property manager notified within two hours.** The property manager notifies the resident and the owner.
5. **Certified funds going forward.** For the remainder of the lease, require cashier's check or money order from this resident. Document it in the ledger notes so the next person does not quietly accept an ACH.
6. **Delinquency clock restarts** from the ladder in `.claude/skills/delinquency-ladder/SKILL.md`.

---

## Before any owner draw

A reversal must be posted before an owner draw is processed against that balance. A draw computed over an unreversed NSF distributes money the portfolio does not have, and pulling it back is a conversation nobody wants to have twice.

Check this explicitly in the draw preflight — see `.claude/skills/owner-draws/SKILL.md`.

---

## Second occurrence

A second NSF on the same resident within twelve months is a different signal from the first. Flag it to the property manager as a pattern, not as another instance. Rising NSF counts across the portfolio are a portfolio-health metric the property manager watches monthly.

---

## What the property manager decides

- Whether to require certified funds going forward (default: yes)
- Whether to waive the fee (rare — and if waived, it is documented per `policy.waiver_and_writeoff_authority`, B12)
- What to tell the resident and the owner

---

## Write it down

Date the bank notified, original payment date and method, amount, reversal date, fee posted or waived and why, time the property manager was notified, certified-funds note added, delinquency clock restart date.

---

## Hard gates

- This agent does not reverse a payment, post a fee, or waive one.
- A fee never posts on a lease that does not carry it, and never above the state cap.
- Notification is not optional and not batchable: two hours, same day, every time.
