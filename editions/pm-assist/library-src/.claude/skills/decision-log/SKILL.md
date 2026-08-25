---
name: decision-log
effort: low
description: "The write-it-down step: capture, format, and file every PM decision where the next person will find it. Use immediately after any decision is made, and when a past decision needs looking up."
triggers: ["decision log", "log the decision", "write it down", "what did we decide", "past decision", "file this decision", "precedent", "why did we"]
---

# Decision Log

Every scenario ends with a write-it-down step. A decision that is not in {{decision_log_location}} <!-- D7: where the decision log lives --> did not happen, and the next person to touch that owner, tenant, or unit will make it again.

## The division of labour (C8)

{{property_manager_name}} <!-- A2: who holds the Property Manager seat --> dictates or notes the decision. **You format and file it.** You never author the decision, never infer it from an outcome, and never file one that was not explicitly made.

If you believe a decision was made but it was not stated, ask. "Did you decide X, or is that still open?" An assumed decision in the log is worse than a gap.

## The entry

| Field | Rule |
|---|---|
| Date | Local time ({{timezone}} <!-- cover sheet: timezone -->) |
| Decided by | The named human. Never you |
| Subject | Property, unit, owner, tenant, or vendor |
| Class | housing / money / legal / relationship / operational |
| The decision | In the decider's words where you have them |
| Why | The reasoning as given. If none was given, write "reasoning not stated" — do not supply one |
| Inputs | The numbers and documents in front of them, with pull times |
| What follows | The next action, its owner, its due date → goes on the Follow-Through Log |
| Where else recorded | Owner file, tenant file, platform of record |

## Filing rules

- Same day. A decision filed a week later is a decision nobody could find in the week that mattered
- Owner communication is saved in the portal or PM software named in `seat-config.platform.durable_record_locations`, **not just email**
- A decision that reverses an earlier one links to it. Both stay; the log is append-only
- A decision with a promise in it creates a Follow-Through row in the same pass

## Reading the log

Before drafting anything for a property, owner, or tenant, check the log. Recurrence is the signal: the third time the same unit produces the same exception, that is a pattern for the PM, and you surface it as one.

## Never

- Never file a decision that was not stated
- Never write reasoning the decider did not give
- Never edit a filed entry. Append a correction that links to it
- Never keep a decision only in MEMORY.md. Memory is your recall; the log is the record
