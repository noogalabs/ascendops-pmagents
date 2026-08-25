---
name: daily-pulse
effort: medium
description: "Build the Daily Pulse each weekday morning: pull every lane board, recompute every clock, age the Approval Queue, promote overdue promises, and stage one surface message for the PM. Use on the daily-pulse cron or whenever the PM asks where things stand today."
triggers: ["daily pulse", "morning build", "where are we today", "today's list", "build the pulse", "morning surface", "what needs me today", "daily board"]
---

# Daily Pulse

The PM's day starts here. The Pulse is the one tab that must be true at the moment they open it, and it must have needed no assembly from them.

Fires on the `daily-pulse` cron (weekday mornings, local time).

## Build order

Do these in order. Later steps read earlier ones.

1. **Pull the lane boards** — maintenance, leasing, turnover, bookkeeping, decision log. Record value, source, and pull time on every row (`pm-operating-board`). A lane you could not pull is a named stale source, not a blank.
2. **Recompute every clock** — delinquency, renewal, turnover, maintenance SLA, compliance, owner non-response. `alert-rules` holds the register.
3. **Age the Approval Queue** — every open request gets its age and its next B4 rung with a time. `approval-queue`.
4. **Sweep the Follow-Through Log** — anything overdue past {{promise_overdue_hours}} <!-- C8: how long a promise may be overdue before it flags red --> hours flags red.
5. **Read Escalation Triage** — anything still unassigned or past due.
6. **Assemble the Pulse** in priority order (below).
7. **Stage the surface message** — three to five lines, plain, numbers first.

## Priority order on the tab

Red-flagged items move to the top. Within that, this order:

1. **Habitability, safety, and legal clocks** — anything with a statutory deadline inside its lead time
2. **Red promises** — Follow-Through items overdue past the threshold
3. **Approval Queue rungs firing today** — with the exact time each fires
4. **Discrepancies** — two sources disagreeing, both values shown
5. **Threshold breaches** — reserve below {{owner_reserve_minimum}} <!-- B5: minimum owner reserve per unit -->, delinquency above target, KPI slipped
6. **SLA misses by lane** — with the coordinator's name on each
7. **Unresolved** — clocks with no named human at the end of them
8. **Everything else due today**

## The surface message

Three to five plain sentences. Lead with what needs the PM today, with a time on each. Drafts are named, not attached in prose.

> Daily Pulse is built. Three things need you today: approval #14 hits its {{owner_escalate_hours}} <!-- B4: escalation rung of the owner non-response ladder -->-hour rung at 2 PM, 88 Rowan is 4 days past target make-ready, and the Riverbend owner reserve dropped under {{owner_reserve_minimum}} per unit on this morning's pull. Drafts are staged for the first two.

Rules for the message:
- Numbers carry their pull time
- Every item names who owns the next move
- Nothing on it is a recommendation about a gated matter — options and consequences only
- If nothing needs the PM, say that in one line. An all-clear Pulse still goes out

## What the Pulse never does

- It never resolves a discrepancy. It shows both.
- It never decides which of two SLA misses matters more to the business. It orders by clock, not by judgment.
- It never carries yesterday's number forward. Missing is missing.
- It never fires an outbound. Everything it produces is staged.

## Shadow mode

While shadow mode is active, build the Pulse fully and report it inside the calibration digest instead of writing the tab. No board writes, no outbound. See `shadow-mode-calibration`.

## Logging

```bash
cortextos bus log-event action daily_pulse_built info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","red":<n>,"approvals_aging":<n>,"discrepancies":<n>,"unresolved":<n>}'
```
