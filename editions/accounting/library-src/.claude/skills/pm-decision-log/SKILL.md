---
name: pm-decision-log
description: "Open, fill, and close PM decision log entries — the record that proves an escalation was raised, decided, and resolved correctly. Four blocks: opening (bookkeeper, immediately on escalation), PM decision, resolution, and audit. An entry with no Block A is an escalation that did not happen."
triggers: ["decision log", "PM decision log", "log the escalation", "log entry", "escalation record", "audit trail", "log ID", "document the decision", "written confirmation"]
---

# PM Decision Log

Source: the PM Decision Log Template. This is the record that survives the people who made the decisions.

Location: `platform.decision_log_location` (D6). Retention: `state_rules.decision_log_retention_years` (A16) — commonly matched to the trust-record retention period so the log outlives the records it explains.

---

## Block A — Opening (filled immediately on escalation)

| Column | Content |
|---|---|
| 1 | Log ID |
| 2 | Date and time escalated |
| 3 | Scenario number (S1–S14, from `bookkeeper-judgment`) |
| 4 | Board item ID |
| 5 | Property / unit |
| 6 | Owner |
| 7 | Resident |
| 8 | Vendor |
| 9 | Dollar amount involved |
| 10 | What happened — plain-language summary |
| 11 | Action taken before escalation |
| 12 | Legal deadline applicable? |
| 13 | Deadline date |
| 14 | Escalation method |
| 15 | Written confirmation sent? |

**Immediately** means at the moment of escalation, not at the end of the day. Columns 12 and 13 are what make a deadline visible to anyone reviewing the log later, so they are filled even when the answer is "no."

---

## Block B — PM decision (same business day, or next morning for after-hours)

| Column | Content |
|---|---|
| 16 | Date and time the PM responded |
| 17 | PM decision |
| 18 | PM decision notes |
| 19 | External party notified |
| 20 | Date external party notified |
| 21 | Attorney consulted? |

A verbal decision is recorded here **and** confirmed in writing. An unwritten decision is an unmade decision when someone reviews this a year from now.

---

## Block C — Resolution (filled when fully resolved)

| Column | Content |
|---|---|
| 22 | Resolution action taken |
| 23 | Date resolved |
| 24 | Supporting documents filed |
| 25 | File path / document reference |
| 26 | Status |

---

## Block D — Audit (filled by the broker or designated reviewer)

| Column | Content |
|---|---|
| 27 | Reviewed by |
| 28 | Review date |
| 29 | Review notes / follow-up required |
| 30 | Policy or guide update triggered? |

Column 30 is the feedback loop: an entry that exposed a gap in the policy is supposed to change the policy, and this is where that gets recorded rather than remembered.

---

## Review cadence

| Who | When | Looking for |
|---|---|---|
| Bookkeeper | Daily | Open entries with no PM response; anything with a deadline approaching |
| Property manager | Daily | New escalations needing a decision |
| Property manager | Weekly | Aging open entries; patterns |
| Broker or senior reviewer | Monthly | Block D audit across the month's entries |
| Broker + PM | Quarterly | Recurring scenarios; policy updates triggered |
| — | Annually | Full retention audit |

---

## What this agent does

Opens Block A immediately on every escalation, with the scenario number and the deadline columns filled. Drafts the Block C resolution once the decision lands. Surfaces aging entries on the daily and weekly sweeps.

## What this agent does not do

Fill Block B. That is the property manager's decision, in their words, recorded as they gave it. Never paraphrase a decision into the log, and never pre-fill what the decision is expected to be.

---

## Hard gates

- No escalation happens without a Block A entry. The entry is part of the escalation, not a follow-up to it.
- A log entry is never edited to look tidier after the fact. Corrections are appended with their own date.
- The log holds no account numbers, no routing numbers, and no payment instruments.
