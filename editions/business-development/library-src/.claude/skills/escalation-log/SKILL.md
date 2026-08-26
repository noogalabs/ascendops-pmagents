---
name: escalation-log
description: "Use this every single time something is escalated — a fee ask, a contract change, a legal or fair housing matter, a red-flag property, a walk-away, or a surprise found after signing. The log entry is written BEFORE the conversation with the manager or the broker, never after. Carries the entry schema, the routing table, and what makes an escalation complete enough to be decidable."
triggers: ["escalate", "escalation", "log escalation", "before I ask the manager", "route this", "who do I tell", "escalation log", "document the escalation", "raise this"]
---

# The Escalation Log

**The entry comes first.** Before the message to the manager, before the call to the broker, before the conversation with counsel.

## Why The Order Is The Whole Point

An escalation logged after the decision is a reconstruction. It records what everyone remembers, which is reliably a cleaner version of what happened. Written first, it records what was actually asked, in the owner's words, before anyone's view of it has settled.

Three things it protects:
- **The seat.** A logged escalation is proof the judgment went up rather than being made at the table.
- **The company.** If an owner complains later, the record is contemporaneous.
- **The decision itself.** Writing the ask down forces it into a specific shape, and half the time that alone reveals it is not the ask you thought it was.

It also removes the failure this seat is most prone to: pre-shaping. Escalating a fee ask *before* it has a form the owner has heard is what keeps it an escalation instead of a deviation that has already happened.

---

## The Entry

Nine fields. All of them, every time.

| Field | What goes in |
|---|---|
| Date and time | When the situation arose, not when you wrote it down |
| Deal ID | The board row |
| What was asked or said | **The owner's exact words where possible.** "Can you do 8 instead of 10, the other place quoted 8" — not "owner requested fee reduction" |
| Which class | Fee · contract · legal or fair housing · property acceptance · walk-away · handoff surprise |
| Why it requires escalation | Which rule. Naming it stops the drift toward "this one's small" |
| Your recommendation | What you think should happen, and why. **You have a view — say it.** Routing is not the same as having no opinion |
| Routed to | Person and channel |
| Decision | What was decided, by whom, and when |
| What was communicated back | The exact response given to the owner |
| Outcome | Won · lost · modified · walked away |

The last three are filled in when the loop closes. **An escalation with an empty decision field is still open**, and an open escalation older than the quoted turnaround is its own problem — the owner is waiting on a promise you made about timing.

---

## Routing

| Class | Goes to | Speed |
|---|---|---|
| Fee: discount, waiver, match, package change | {{bd_manager_name}} <!-- C2, B12 --> | Before any answer reaches the owner |
| Contract: any clause, term, threshold | {{broker_of_record}} <!-- C3, B12 --> | Before any answer reaches the owner |
| Legal, state law, litigation, eviction | {{legal_counsel}} <!-- C4 --> plus the manager | Same day |
| Fair housing, protected class, accommodation | {{legal_counsel}} plus the manager <!-- A8 --> | **Same day, without exception.** Silence here is its own liability |
| Red-flag property, above-market rent demand | {{bd_manager_name}} <!-- A4 --> | Before the agreement is sent |
| Walk-away or decline | {{bd_manager_name}} <!-- C2 --> | **Before** the conversation with the owner |
| Surprise found after signing | {{bd_manager_name}} <!-- judgment §7 --> | Same day |
| Tenant approval rights | Broker **and** counsel — it is both classes at once | Same day |

---

## What To Say To The Owner While It Is Open

Never the answer. The turnaround.

> "That's a fair question and I want to get you the right answer rather than a fast one. Let me take it to [person] and come back to you within {{escalation_turnaround}} <!-- B12 -->."

Then come back inside it. A missed turnaround costs more than the answer would have — the owner now has evidence about how the company handles commitments.

**Never:** "I'm sure that'll be fine." "We can probably do that." "Let me see what I can do" said in a tone that means yes. Each of these is a decision, delivered in a form that can be denied later.

---

## Making It Decidable

An escalation the manager has to chase for context wastes the turnaround you just quoted. Include:

- The exact ask, in the owner's words
- Where the deal is: stage, doors, package discussed, days in pipeline
- What is already known: gates cleared, condition, entity verified, competing companies
- **Your recommendation and your reasoning**
- What you have told the owner so far, verbatim
- When you promised to come back

---

## Logging The Event

```bash
cortextos bus log-event action escalation_created info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","class":"<class>","deal_id":"<id>","routed_to":"<role>"}'
```

And on close:

```bash
cortextos bus log-event action escalation_resolved info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","class":"<class>","deal_id":"<id>","outcome":"<outcome>"}'
```

---

## The Pattern Worth Watching

Escalations are data. If the same class fires repeatedly — the fee ask every time, the same clause every time — that is not a run of difficult owners. It is a signal about the pricing presentation, the agreement, or the market, and it belongs in the weekly review rather than being absorbed one deal at a time. See `pipeline-metrics-and-review`.
