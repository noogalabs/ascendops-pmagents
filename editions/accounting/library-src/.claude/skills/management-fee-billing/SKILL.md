---
name: management-fee-billing
description: "Post and verify management fees, leasing fees, and other agreement-driven fees against each management agreement exactly. Fees reduce the owner's net distribution rather than being invoiced separately, and any discrepancy against the agreement goes to the property manager before posting."
triggers: ["management fee", "leasing fee", "renewal fee", "fee billing", "post fees", "management agreement", "fee schedule", "inspection fee", "lease prep fee", "fee waiver"]
---

# Management and Leasing Fee Billing

Source: monthly workflow Step 7.

---

## What posts, and when

| Fee | Trigger | Target |
|---|---|---|
| Management fee | Monthly, per the management agreement | Posted by day 5 |
| Leasing fee | Execution of a new lease or renewal | Within one business day of execution |
| Other agreement fees (renewal, inspection, lease prep) | The trigger event named in the agreement | On the trigger |

**Collected, not scheduled.** A percentage-of-rent management fee is computed on rent actually collected unless the agreement explicitly says otherwise. Computing on scheduled rent overbills every owner with a delinquency, quietly, every month.

---

## Verify before posting

Every fee is checked against the management agreement on file, exactly:

- the fee basis (flat vs percentage) and the rate
- the collected-vs-scheduled basis
- what triggers a leasing or renewal fee, and at what amount
- any owner-specific override

**Any discrepancy against the agreement goes to the property manager before posting, not after.** A fee posted at the wrong rate produces a wrong statement and a wrong draw, and both have already been sent by the time anyone notices.

If the agreement is not on file, that is the finding. Do not compute a fee from precedent or from what the other owners pay.

---

## How fees flow

Fees are deducted from the owner's trust balance **before** the draw is calculated. They are not invoiced separately; they reduce the net distribution. Every fee is a visible line on the owner statement — see `.claude/skills/owner-statement-drafting/SKILL.md`.

---

## Waivers and adjustments

A waiver or an adjustment requires the authority named in `policy.waiver_and_writeoff_authority` (B12), in writing. Never on a verbal, and never applied retroactively across prior statements without an explicit instruction that says so.

---

## Hard gates

- This agent does not post a fee, waive one, or adjust one.
- A fee that does not match the agreement is flagged, never rounded to the agreement.
- Management fee revenue against collections is a monthly number the property manager reviews; surface it, do not editorialize on it.
