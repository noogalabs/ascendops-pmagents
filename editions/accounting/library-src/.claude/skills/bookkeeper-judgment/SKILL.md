---
name: bookkeeper-judgment
description: "The lookup index for the fourteen situations that actually go wrong in this seat. If something feels off, match it to a scenario and follow the four columns exactly — do right now, never do, goes to the PM when, write down. Do not improvise and do not delay: the most dangerous move in trust accounting is doing nothing while you think about it."
triggers: ["something feels off", "what do I do", "judgment", "scenario", "lookup", "unusual situation", "not sure what to do", "escalate or not", "bookkeeper judgment", "when in doubt", "edge case"]
---

# Bookkeeper Judgment and Lookup

Source: the Bookkeeper Judgment and Lookup Guide. Fourteen scenarios. Find the match, follow the columns, do not improvise.

Every scenario has a full treatment in a dedicated skill. This file is the index and the escalation rule.

---

## The index

| # | Situation | Skill |
|---|---|---|
| S1 | Payment that does not match any ledger | `suspense-and-unmatched-payments` |
| S2 | Resident paying someone else's rent / payor not on the lease | `suspense-and-unmatched-payments` |
| S3 | Partial payment on a delinquent account after a notice went out | `delinquency-ladder` |
| S4 | Vendor invoice with no work order | `vendor-bill-intake` |
| S5 | Vendor asking to change their bank details | `vendor-banking-change` |
| S6 | Owner asking for money beyond their balance | `owner-contributions` |
| S7 | Request to cover a shortfall from another owner's funds | `owner-contributions` |
| S8 | Deposit disposition where invoices are not in and the deadline is close | `security-deposit-accounting` |
| S9 | Bank reconciliation that is off (A: small, B: large) | `trust-reconciliation` |
| S10 | Resident claiming they paid, with a receipt you cannot find | `suspense-and-unmatched-payments` |
| S11 | Duplicate payment | `suspense-and-unmatched-payments` |
| S12 | Payment received after eviction filing | `delinquency-ladder` |
| S13 | Month end, three-way does not balance, statements are due | `owner-statement-drafting` |
| S14 | Suspected fraud or unauthorized transaction in the trust account | `fraud-and-unauthorized-transactions` |

Every scenario opens a PM decision log entry with its scenario number — `.claude/skills/pm-decision-log/SKILL.md`.

---

## The four columns

Every scenario answers the same four questions, and the value is in answering all four rather than the first one:

1. **Do right now** — the immediate action, usually a hold and a record
2. **Never do** — the specific wrong move, named, because it is the one that feels reasonable in the moment
3. **Goes to the PM when** — the trigger and the clock
4. **Write down** — what the log entry has to contain to prove the protocol was followed

---

## The when-in-doubt escalation rule

One rule. Memorize it.

> **"If I am not fully certain this transaction is correct, authorized, and fully traceable, I stop, I hold, and I tell the property manager before I do anything else."**

This seat is the last line of defense before money moves incorrectly. **Stopping is never wrong. Guessing is always wrong.**

- Hold the transaction.
- Document what you have.
- Notify the property manager in writing within the hour.
- Wait for written direction before proceeding.

If the property manager is unavailable and a statutory deadline is imminent, escalate to `roles.backup_decision_maker` (C4), then `roles.principal_or_managing_broker` (C2). There is always a decision-maker available for a time-sensitive trust matter — and if there genuinely is not, that is a company structure problem to name out loud before it becomes a legal one.

---

## What "feels off" looks like

You will not always match a scenario cleanly. These are the tells:

- a number that ties out only if you assume something you have not verified
- a request that comes with a reason why the normal step can be skipped this once
- pressure from a deadline to act before a check completes
- a document that arrives unprompted and asks for a change
- a familiar counterparty behaving slightly unlike themselves
- your own sentence starting with "it's probably"

Any of these is a hold, not a judgment call.

---

## Hard gates

- No scenario in this guide resolves with the agent taking an action. Every one resolves with a hold, a record, and a routed decision.
- This guide is reviewed quarterly and updated wherever state law, company policy, or the platform workflow changed.
- Every unfilled state-law marker must be filled from `accounting-config.json` before the scenario relying on it is used in practice.
