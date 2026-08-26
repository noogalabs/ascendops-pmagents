---
name: owner-report-pack
effort: medium
description: "Assemble and stage the monthly owner report pack: what goes in, the sign-off sequence, per-owner channels and tone, and the all-clear rule. Use at month-end and on the report day."
triggers: ["owner report", "report pack", "monthly owner", "owner statement", "send the reports", "owner update", "all-clear update", "report day"]
---

# Owner Report Pack

Assembled by you, released by a human, out by day {{owner_report_day}} <!-- D6: day of the month the owner report pack goes out -->.

## The sequence — never compressed

1. Month-End Pack assembled (`month-end-pack`)
2. **Financial review signed off** by {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> inside the configured window
3. Owner draws on the configured draw day, executed by the money side
4. Packs assembled per owner and **staged**
5. Released by a human on the configured channels by day {{owner_report_day}}
6. High-touch owners get the follow-up call if `seat-config.owner_reporting.high_touch_followup_call` says so — **the call is the PM's**, not yours

Staging before sign-off is the failure this ordering prevents. If the report day arrives without sign-off, say so plainly and let the PM decide; do not send.

## Per pack

- Owner statement from the accounting system, sourced and pull-timed
- Property performance: occupancy, work orders opened/closed, turnover status
- Reserve position against {{owner_reserve_minimum}} <!-- B5: minimum owner reserve per unit -->, flagged if under
- Open approvals and their age
- Anything promised to this owner and its status, from the Follow-Through Log
- Compliance items touching their properties

Tone follows the Owner Snapshot tag. Facts never do.

## The all-clear rule

**The all-clear version goes out even when nothing happened.** A quiet month is a report, not a skipped report. An owner who hears nothing assumes nothing is being done.

The templated all-clear update is usually the first message class to graduate — no numbers changed, no framing, no judgment. It graduates only when {{property_manager_name}} says so, and only through `draft-release-gate`.

## What never goes in a pack

- Any framing of a difficult month. That is drafted, reviewed, personalized, and sent by the PM
- Any explanation of a bad number. The numbers are yours; the story is theirs
- Any forward-looking promise, date, or dollar figure
- Any legal characterization of a tenant matter
- Any number you could not source, in place of saying it is unavailable

## When an owner replies

Any reply with a concern in it goes to the PM. Immediately, unanswered. A reply that is purely a receipt ("got it, thanks") is logged and closed.
