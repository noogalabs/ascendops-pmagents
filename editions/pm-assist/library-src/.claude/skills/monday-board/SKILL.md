---
name: monday-board
effort: medium
description: "The Monday Board (the week ahead) and the Follow-Through Log sweep: every open promise, its due date, its owner, and everything overdue past the red threshold. Use on the Monday cron, or whenever a promise, commitment, or 'we said we would' needs tracking."
triggers: ["monday board", "week ahead", "follow-through", "follow through log", "promise", "we said we would", "overdue promise", "weekly sweep", "commitments", "what did we promise"]
---

# Monday Board + Follow-Through Log

Two artifacts, one cadence. Fires on the `monday-board` cron, {{followthrough_sweep_day}} <!-- C8: when the assistant sweeps the Follow-Through Log --> morning — the sweep day is `seat-config.clocks.followthrough_sweep_day`, default Monday.

## The Follow-Through Log

Every promise made to an owner, a tenant, a coordinator, or a vendor gets a row the moment it is made. A promise nobody wrote down is a promise the company will break.

A row is:

| Field | Rule |
|---|---|
| Promise | The commitment in the words it was made in |
| Made to | Owner / tenant / coordinator / vendor, named |
| Made by | The human who made it. Never you — you do not make promises |
| Made on | Date, local time |
| Due | A real date. "Soon" is not a due date; ask for one |
| Owner of the next move | A named human |
| Status | open / done / red |
| Source | Where the promise was made: email, call log, meeting note, board row |

## The sweep

Every {{followthrough_sweep_day}} morning, and again on every heartbeat's alert pass:

1. Every open row — is it still open, and is its due date still real?
2. Anything due this week → onto the Monday Board
3. Anything overdue past {{promise_overdue_hours}} <!-- C8: how long a promise may be overdue before it flags red --> hours → **red**, and it moves to the top of the Daily Pulse. Every time, no exceptions, no "it'll probably resolve itself"
4. Anything closed → mark done with the date and the evidence, and file the closure in {{decision_log_location}} <!-- D7: where the decision log lives -->
5. Anything with no named owner → **UNRESOLVED**, into Escalation Triage

## The Monday Board

The week ahead, assembled from the same pulls the Daily Pulse uses:

- **Clocks firing this week** — legal, renewal, turnover, compliance, approval rungs
- **Promises due this week** — from the log, with owners
- **Red carryover** — anything red from last week, with how long it has been red
- **Renewals entering the window** — leases crossing inside {{renewal_lookahead_days}} <!-- B9: renewal pipeline look-ahead window --> days
- **Vacancy and make-ready aging** — against the B7 and B11 targets
- **Approvals aging** — with the next rung and its time
- **KPIs against target** — from `kpi-scorecard`, sourced and pull-timed
- **Broker check-in** — anything queued for the {{broker_name}} <!-- A3: principal broker or company owner --> cadence, plus a reminder that legal escalations, owner relationship risk, and compliance questions go up as they arise and are never held for the meeting

## Staging the weekly surface

One message, plain, in priority order: what is red, what fires this week, what is slipping. Drafts named. Nothing sent.

## What this never does

- It never renegotiates a due date. Only the human who made the promise can move it, and the move gets logged
- It never marks a promise done on inference. Done needs evidence
- It never quietly drops a promise whose owner left the company — that becomes UNRESOLVED, loudly

## Logging

```bash
cortextos bus log-event action followthrough_sweep info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","open":<n>,"due_this_week":<n>,"red":<n>,"unresolved":<n>}'
```
