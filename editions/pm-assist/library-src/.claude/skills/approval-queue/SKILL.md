---
name: approval-queue
effort: medium
description: "The Approval Queue: drafting complete spend-approval requests, aging them, and running the owner non-response ladder. Use whenever a repair, project, or scope needs a decision, or when an approval has been sitting."
triggers: ["approval queue", "needs approval", "owner approval", "spend approval", "approval request", "aging approval", "owner hasn't responded", "non-response", "escalate approval", "over threshold"]
---

# Approval Queue

Every spend decision that needs a human, drafted complete and aged on the clock.

## The three thresholds — keep them separate

They look alike and they are not. Never let one populate another.

| Gate | Value | What it means |
|---|---|---|
| Coordinator escalation | {{coordinator_spend_authority}} <!-- B2: coordinator spend authority, cost above which a work order escalates to the PM --> | Above this, a work order leaves the coordinator and lands in this queue for {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> |
| Owner pre-approval | {{owner_approval_threshold}} <!-- B1: owner pre-approval spend threshold --> | Above this, written owner approval must be in hand **before work proceeds**. Per-owner overrides are in `seat-config.thresholds.owner_threshold_overrides` — check the owner every time, not the default |
| Multiple bids | `seat-config.thresholds.multi_bid_threshold` <!-- B13: project cost requiring multiple bids --> | Above this, the request is incomplete without 2–3 bids |

Check the per-owner override before the portfolio default. An owner with a different number in their management agreement is the common case, not the exception.

## A complete request

An approval request with a missing field wastes a decision cycle. Every row carries:

- Property and unit
- What the work is, in the words the vendor used
- Exact cost. **Never round toward a threshold** — $498 is $498
- Which threshold it crossed, and whose approval that requires
- Quotes attached; if the multi-bid line is crossed, all of them, or a named reason one is missing
- Occupancy status and whether habitability is involved
- History: has this unit or this system been here before? Pull it
- The decision-by date, and what happens if it passes
- **Options and their consequences — never a recommendation.** "The options are" not "I recommend"

## The owner non-response ladder (B4)

Fires from the moment the request goes to the owner. Never let a rung pass unfired.

| Rung | Time | Action |
|---|---|---|
| 1 | {{owner_followup_1_hours}} <!-- B4: owner non-response ladder, first follow-up --> h | Follow-up on the owner's preferred channel from the Owner Snapshot. Logged |
| 2 | {{owner_followup_2_hours}} <!-- B4: second follow-up with documented attempts --> h | Second follow-up, **with every attempt documented in the owner file** |
| 3 | {{owner_escalate_hours}} <!-- B4: escalation rung of the owner non-response ladder --> h | To {{property_manager_name}} for the urgent / non-urgent call |

At rung 3 the PM decides: urgent items they decide and log; non-urgent items escalate to {{broker_name}} <!-- A3: principal broker or company owner --> and get flagged in the owner file. **You make neither call.** You fire the rung, you draft what the call needs, you log the outcome.

## Habitability skips the ladder

A genuine habitability emergency does not wait rungs. It goes to {{property_manager_name}} immediately; if unreachable, to {{backup_decision_maker}} <!-- C5: backup decision-maker when the PM is unreachable -->. The PM's emergency authority is {{pm_emergency_authority}} <!-- B3: PM emergency spend authority when the owner is unreachable -->, and above {{broker_emergency_threshold}} <!-- B3: cost at which the broker is looped in even on an emergency --> the broker is looped in even on an emergency.

**None of those authorities are yours.** You surface, you document every contact attempt, you log the time of each. You never authorize.

## Aging

Every heartbeat pass: age every open request, compute the next rung and its clock time, and put anything firing today on the Daily Pulse with the time.

An approval sitting with no next rung — because the ladder ran out, or the owner is unreachable and the PM has not decided — is **UNRESOLVED**, into Escalation Triage. It is never something you quietly keep waiting on.

## Never

- Never approve, at any amount, for any reason, in any emergency
- Never round a figure toward a threshold, and never quote "about"
- Never apply the portfolio default when the owner has an override
- Never let a rung pass because the owner "usually answers late"
- Never write "I recommend" on a request
