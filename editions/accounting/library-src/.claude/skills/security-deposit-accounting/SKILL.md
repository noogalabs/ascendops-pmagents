---
name: security-deposit-accounting
description: "Handle security deposits from receipt through disposition: post as a liability at move-in, confirm the balance intact at every reconciliation, set the statutory clock the day a move-out lands, compute the disposition from PM-approved deductions, and draft the itemized letter. Never miss the deadline waiting for a perfect invoice. Covers judgment scenario 8."
triggers: ["security deposit", "deposit disposition", "deposit return", "itemization", "move out deposit", "deposit deadline", "deposit refund", "deposit liability", "deduction", "disposition letter", "deposit clock"]
---

# Security Deposit Accounting

Source: monthly workflow Step 9, plus judgment scenario 8. This is the seat's highest legal-exposure surface: in most states, missing the deadline forfeits the right to deduct at all, and several add double or treble damages.

---

## Receipt (move-in)

- Post the deposit to the resident ledger **as a liability**. It is the resident's money, not income, and it never appears in an owner's distributable balance.
- Hold it in the trust account — the separate deposit trust where `state_rules.separate_deposit_account_required` (A7) says so, and where `platform.deposit_trust_separate` (D3) confirms one exists. **A7 true with D3 false is a day-one finding, not a config gap.**
- Record amount, date received, property, and resident.
- Check the amount against `state_rules.deposit_cap` (A9).
- Where the state requires written notice to the resident of where the deposit is held, that notice is a tracked obligation with its own date.
- Where `state_rules.deposit_interest_required` (A8) is true, the interest obligation accrues from receipt and is tracked from day one, not reconstructed at move-out.

## Holding (during tenancy)

The deposit sits in trust. It is never used for operating expenses and never for an owner draw. Confirm the deposit balance is intact at **every** monthly reconciliation — the month-end deposit trust audit compares the sum of held deposits to the deposit trust bank balance, and any gap is a red variance.

---

## The clock

Set it the day the move-out lands. Not when the inspection is done, not when invoices arrive.

```
deadline = state_rules.deposit_clock_trigger (A6)  +  state_rules.deposit_return_days (A6)
```

The trigger date matters as much as the count: move-out, termination of tenancy, and key return are different days and the statute names one of them. Where the portfolio spans jurisdictions, the clock is per-property, not per-company.

| Timing | State | Who hears about it |
|---|---|---|
| Day 0 | Clock set, logged on the board | Bookkeeper |
| Midpoint | Invoices outstanding → escalate | Property manager |
| 3 days out | Warning | Bookkeeper + property manager |
| Deadline passed, not returned | Legal risk, red | Property manager, immediately |

---

## Disposition

The turnover seat conducts and documents the move-out inspection and supplies the itemized deduction draft with photos, invoices, and estimates. **The property manager decides the deductions.** This seat computes and drafts.

```
deposit received − PM-approved deductions = refund, or balance due
```

Deduction review gate: at or above `chargeback_gates.per_line` or `chargeback_gates.per_unit` (B13), or on any dispute or missing documentation, the disposition goes to the property manager before it is sent. B13 is the same number the turnover seat carries — if the two disagree, surface the mismatch, do not pick one.

Then: prepare the itemized disposition letter, route it for approval, and only after approval does the refund process from trust and the letter send. Deductions post to the correct expense category on the owner's ledger.

---

## Scenario 8 — deadline is close and invoices are not in

**Do right now.** The clock was flagged on day one. At the midpoint, if invoices are not in, escalate. Use documented estimates — from the inspection report or a pre-established fee schedule — where the state allows estimates in the itemization.

**Never.** Never miss the deadline waiting for a perfect invoice. Never hold the entire deposit without itemization because one invoice is missing. Never fabricate a number; documented estimates or actuals only.

**Escalate when.** As soon as it is clear the invoices will not arrive in time. The property manager decides: partial disposition now, documented estimates, or full release and pursue the resident separately.

**Write down.** Move-out date, deposit amount, deadline date, invoices received vs outstanding, PM decision, date sent, method, tracking confirmation. Decision-log scenario S8.

---

## Hard gates

- This agent does not disburse a refund, apply a deposit to a balance, or send a disposition letter.
- The deadline is not negotiable and does not wait on documentation.
- `deposit_disposition_send` is in the `never_graduate` set.
- Deposit funds never touch an operating expense or an owner draw, at any point, for any reason.
