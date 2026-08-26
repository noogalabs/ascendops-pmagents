---
name: owner-draws
description: "Calculate owner draws net of the reserve floor and authorized holdbacks, run the preflight that catches unreversed NSFs and unposted bills, and route the disbursement for approval. The reserve floor is never drawn down. The draw is always a draft; a human releases it."
triggers: ["owner draw", "owner disbursement", "distribution", "draw calculation", "reserve floor", "holdback", "disburse to owner", "draw window", "net distribution"]
---

# Owner Draws

Source: monthly workflow Step 8. The draw is the single largest money movement this seat touches and it is never unattended.

---

## The calculation

```
available balance
  − reserve requirement          (thresholds.reserve_floor, B3, or this owner's override)
  − authorized holdbacks         (written PM instruction only)
  = draw amount
```

If the result is at or below zero, **there is no draw.** Generate a contribution request instead — `.claude/skills/owner-contributions/SKILL.md`.

**The reserve floor is never drawn down.** Not to make a draw work, not because the owner asked, not because next month's rent will cover it.

**A holdback requires written authorization** from the property manager, naming the reason and the amount — a large repair pending, a vendor bill expected. A holdback with no written basis is just a number somebody remembered.

---

## Preflight — every item, every owner, every month

| Check | Why it matters |
|---|---|
| All income posted | A missing receipt understates the draw |
| All bills posted | A missing payable overstates it, and the shortfall lands next month |
| All fees posted and verified | Fees come out before the draw, not after |
| **Every NSF reversal complete** | A draw computed over an unreversed NSF distributes money that is not there |
| No pending items that would change the balance | Pending is not cleared |
| Three-way reconciliation balances | Same gate as statements |
| Owner balance clears the reserve floor after the draw | Otherwise it is a contribution, not a draw |

---

## Timing

`policy.owner_draw_deadline_day` (B8) is the outside date; `policy.owner_draw_target_day` is the goal. Both must match what the management agreements promise, and both must be reachable after the reconciliation finishes.

Where `state_rules.owner_disbursement_statutory_deadline` (A12) carries a value, it governs and it is a legal clock, not a policy preference. Where it is empty, the management agreement governs.

---

## The draft

Every draw draft carries: opening balance, income, expenses, fees, reserve held and why, holdbacks and their written authorization, the computed draw, and the destination account by purpose label — never by account number.

Route it with the statement. The property manager reviews both together; the draw releases only after that approval.

---

## Hard gates

- This agent does not initiate an ACH, cut a check, or release a distribution.
- The reserve floor does not flex.
- A holdback with no written authorization does not exist.
- An unreversed NSF stops the draw for that owner, alone, without stopping the others.
- `money_movement` is in the `never_graduate` set. No accuracy record changes this.
