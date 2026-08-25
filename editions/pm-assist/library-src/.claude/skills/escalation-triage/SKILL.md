---
name: escalation-triage
effort: medium
description: "The front gate: classify every exception that reaches this seat, route gated matters with zero substance, and land everything else on a board with a named owner and a due date. Use the moment anything arrives that is not routine board work."
triggers: ["escalation", "triage", "exception", "flag", "this came in", "what do I do with", "route this", "who owns this", "escalation triage", "unassigned alert"]
---

# Escalation Triage

Everything that is not routine board work comes through here first. This is where the never-graduates test is applied, before any drafting happens.

## Step 1 — classify, before anything else

Ask in this order. The first yes ends the sequence.

| Is it… | Then |
|---|---|
| Protected class, Fair Housing, accommodation, assistance animal? | **Broker-only.** Route to {{broker_name}} <!-- A3: principal broker or company owner --> on {{broker_channel}} <!-- A3: channel broker-only escalations travel --> the same day. Send **nothing** of substance — not a reassurance, not an acknowledgement of the merits. See `fair-housing-guard` |
| Any other broker-only class? | Route same day on the same channel. See `broker-escalation` |
| A legal demand letter or attorney contact? | {{broker_name}} **and** counsel, same day it arrives |
| A housing decision — approve/deny/terms/rate/renewal/non-renewal? | Route to {{property_manager_name}} <!-- A2: who holds the Property Manager seat -->. Draft the options and consequences; never a recommendation |
| A money decision — spend, draw, trust, deposit, waiver, chargeback? | Route to {{property_manager_name}}. `approval-queue` for the spend path |
| A legal notice — serve, time, or draft outside the template library? | Route to {{property_manager_name}} |
| A relationship call — unhappy owner, tenant dispute, vendor confrontation, staff? | Route to {{property_manager_name}} |
| A habitability or safety issue? | Surface immediately, skip every ladder. Never authorize |
| None of the above | It is execution. Draft it, board it, clock it |

**Routing is not deciding, and it is not "handling it quietly."** A routed matter stays on this tab, tracked, until it closes.

## Step 2 — every row gets an owner and a due date

| Field | Rule |
|---|---|
| What | The exception, in one line, factual |
| Class | broker-only / housing / money / legal / relationship / execution |
| Source | Which lane, which board, which message. With its pull or arrival time |
| Owner | A **named human**. Not a role, not "the team", not you |
| Due | A real date derived from the clock that is running |
| Status | routed / drafted / staged / closed |
| Evidence | Where the closure is recorded |

**An alert with no owner does not exist.** If you cannot name the human, the row is `UNRESOLVED` and it goes into the calibration digest and onto the Daily Pulse until someone is named. You never hold it yourself to be helpful.

## Step 3 — what arrives here

- Manual coordinator flags (the `seat-config.platform.manual_alert_flags` set — anything the platform cannot auto-flag)
- Alerts fired by `alert-rules` that need a human
- Stale-source rows: a lane board that has not been updated
- `DISCREPANCY` rows: two sources disagreeing, both values carried
- Owner non-response items that ran out of ladder
- Promises with no owner, clocks with no decision-maker

## Cross-lane discipline

You read lane boards. You never run a lane. When maintenance, leasing, turnover, or bookkeeping is behind, the row names their coordinator and their SLA — you do not do the piece yourself to unblock it, and you do not overrule their board.

## Logging

Every routed gated matter gets an event. That log is the proof you did not answer it.

```bash
cortextos bus log-event action matter_routed info \
  --meta '{"class":"housing|money|legal|relationship|broker_only","to":"<named human>","item_id":"<id>","substance_sent":false}'
```
