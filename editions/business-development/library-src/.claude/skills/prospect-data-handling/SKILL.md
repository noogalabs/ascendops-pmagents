---
name: prospect-data-handling
description: "Read this before writing any prospect or owner information anywhere, before using any contact list, before any first touch to someone whose source you did not personally confirm, and before archiving or deleting any record. This seat's entire subject matter is named people and their contact details, which makes it the seat with the most to leak. Carries the where-data-lives rule, source compliance, opt-out handling, retention, and the sweep."
triggers: ["prospect data", "PII", "personal data", "contact list", "purchased list", "scraped", "where do I put", "can I write this down", "retention", "delete", "opt out", "do not contact", "compliance", "privacy", "owner details", "phone number", "email address"]
---

# Prospect Data

Every other seat handles people's data incidentally. This one handles it as the job — names, mobile numbers, personal email addresses, home addresses, financial circumstances, and in the discovery notes, things people said about their lives that they would not expect to be readable a year later.

That is not a reason to be nervous about the work. It is a reason to have exactly one place it lives.

---

## Rule 1 — One Home

**Prospect and owner data lives on the pipeline board. Nowhere else.**

| Allowed | Not allowed |
|---|---|
| Board Blocks B, C, E, G | `MEMORY.md` or any memory file |
| The CRM or platform of record | Skill files, examples, templates |
| A staged message to that person | Status messages that did not need the name |
| An escalation entry that needs the exact words | Task titles and descriptions |
| The handoff package to onboarding | Event log metadata |
| | Anything committed to version control |

**Memory is for patterns, not people.** "The fee objection lands better when you ask what they're comparing to" belongs in `MEMORY.md`. "The Thompson deal" does not — and the pattern is the useful half anyway.

**The name-in-a-status-message habit** is the most common leak in this seat and the easiest to fix. "Escalating a fee ask on deal PM-0142" carries everything the manager needs. The name adds nothing the deal ID does not, and it puts a real person's identity into a channel that outlives the deal.

---

## Rule 2 — Source Compliance, Before The First Touch

Every lead source is confirmed compliant before anything goes to anyone on it <!-- D2, compliance -->.

**Never contact:**
- Anyone from a purchased list
- Anyone from a scraped list
- Anyone whose source you cannot name

"Someone sent me a spreadsheet" is not a source. "It was on a public listing" is a source and is usually fine. If you cannot say where a contact came from, it does not get contacted — it goes to {{bd_manager_name}} <!-- C2 -->.

This is not only a legal question. A list nobody can account for is a list somebody will eventually be asked to account for.

---

## Rule 3 — Opt-Outs Override Everything

Any form of "stop contacting me" — explicit, implied, on any channel:

1. **Stop every cadence immediately.** Every channel, not the one they used.
2. **Log it the same minute** to `compliance.do_not_contact_list_location`.
3. **Never contact again.** No re-engagement window. No new campaign. No "it's been a year". No exception for a different property.
4. Archive as a hard no, immediately <!-- D5 -->.

This outranks every clock, every cadence, and every activity target in the seat. There is no version of a missed number that justifies one more touch.

**Check the do-not-contact list before any new campaign.** An opt-out that was honoured in one cadence and forgotten in the next is worse than one never recorded — the person now knows the record exists and was ignored.

---

## Rule 4 — Retention

Per `state_rules.record_retention` <!-- A9 -->, confirmed with counsel.

| Record | Retention |
|---|---|
| Won deals | Permanent — feeds conversion metrics indefinitely |
| Lost deals | The configured active window, then archived |
| Unresponsive | The configured window |
| Disqualified | The configured window |
| Nurture exhausted | The configured window |
| Duplicates | The configured window, then deleted — the one record type that is deleted rather than archived |

**Archive, do not delete.** Archived records are read-only and searchable; deleted ones take the lost-reason analysis with them. The duplicate is the exception, and only after its notes are merged into the surviving row.

**Where retention is unconfirmed, that is not a reason to keep everything forever.** It is an open question for counsel, and it belongs in the review until it is answered.

---

## Rule 5 — What Goes In A Discovery Note

Discovery notes are the richest data on this board and they last for years.

**Write:** what they said about the property, the timeline, the motivation, the gap and the consequence in their own words, the objections raised, what they said matters most.

**Do not write:** health information, family circumstances beyond who the decision-makers are, financial detail beyond carrying costs and the rent target, anything about a person's characteristics, or your opinion of them as a person.

The test: *would this read as reasonable to the owner if they saw it?* An owner reading "wants to be close to grandchildren, moving next spring" is fine. An owner reading a judgment about them is not, and it will not have helped anyone close anything.

**The one exception is the fair housing quote.** When a protected-class matter fires, the exact words go on the record verbatim, because that is what counsel needs — see `fair-housing-guard`. That is a legal record, deliberately made, not a note.

---

## Rule 6 — Never Into A Template

Nothing in `.claude/skills/`, the bootstrap files, or any example ever carries a real person's name, company, phone number, or email address.

Examples use invented names. If a real one is needed to explain something, use the deal ID.

**This applies to what you write and to what you copy.** Pasting a real message into a skill as a "good example" carries the whole contact block with it, and it will be read by everyone who ever installs from that template.

---

## The Sweep

Before any board export, any handoff package to a channel outside the platform, any report, and on every heartbeat's guardrail self-check:

1. Did a name land anywhere outside the board this cycle?
2. Did a phone number or email land in a task, event, or memory file?
3. Did any first touch go to a contact whose source is not named?
4. Was an opt-out logged the same minute it arrived?
5. Is anything past its retention window still sitting in an active tab?

Any yes is a guardrail event. Log it and tell {{bd_manager_name}} the same cycle.

```bash
cortextos bus log-event action prospect_data_guardrail info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","check":"<which>","action":"<what was done>"}'
```

---

## Why This Sits At The Top Of The Seat

Every other rule here protects a deal. This one protects people who never agreed to be in a database, and who mostly do not know they are in one. The seat exists because they might want a service. It does not exist because they signed up for a record.
