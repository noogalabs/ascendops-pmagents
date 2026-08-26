---
name: listing-appointment
description: "Load this when an appointment gets booked and again the day before it happens. It covers the pre-appointment sequence, the decision-maker gate, the ownership verification that has to be done before any agreement can be valid, what happens in the appointment, and what happens in the first hour afterwards whether it was signed or not."
triggers: ["listing appointment", "appointment", "book appointment", "pre-appointment", "reminder call", "day before", "morning of", "decision makers", "verify ownership", "tax record", "entity check", "appointment held", "no-show"]
---

# The Listing Appointment

The appointment where an agreement gets signed, or where a clear next step with a date gets set. Those are the only two acceptable outcomes; "they're going to think about it" without a date is neither.

---

## Two Gates Before The Appointment Can Happen

### Gate 1 — Every decision-maker attending (F5)

Confirmed at booking, confirmed again in the reminder. An appointment missing a decision-maker is not an appointment — it is a preview, and the real conversation happens later without you in the room.

If someone cannot attend, **move the appointment**. Running it short a decision-maker is the single most common cause of "I need to talk to my partner", and that objection cannot be handled — only prevented.

### Gate 2 — Ownership verified against the public record (B10)

Before the appointment, look up the property on the tax-record site for that market <!-- A2, `markets.tax_record_lookup_by_market` -->. Confirm the legal entity name exactly.

**Why this is before and not after:** an agreement executed against the wrong entity may be unenforceable <!-- A5 -->, and finding the mismatch after signing means re-execution, an awkward conversation, and a delay on a deal that felt done. Finding it before means one question in the appointment.

If the market has no lookup site configured, that market cannot run this gate — say so rather than skipping it.

If the record does not match what the owner told you, that is not necessarily a problem, but it is a question to ask in person: *"The record shows [entity] — is that the entity that'll be signing?"*

---

## The Pre-Appointment Sequence

| When | Touch | Why |
|---|---|---|
| At booking | Recap staged within minutes; confirm date, time, who is attending | Speed after a live conversation is what makes the booking stick |
| Before the appointment | Finish the rental analysis; run the ownership check | You cannot build the analysis in the room |
| Day before | A **reminder** call | See the framing note below |
| Morning of | A short text: looking forward to it, check your email beforehand | Reduces no-shows more than anything else in the sequence |

**Reminder, not confirmation.** "I'm calling to remind you about tomorrow" assumes it is happening. "I'm calling to confirm" invites the owner to reconsider whether it is. Same call, entirely different outcome rate.

Use the day-before call to pre-qualify further: what is driving the timing, what they are still unsure about, who else they are talking to, what matters most, and whether they are in a position to sign at the appointment. Every answer changes how you run the room.

---

## In The Appointment

Order:
1. **Their situation first.** Re-open with what they said in discovery, in their words. It shows you listened, and it re-surfaces the gap.
2. **The rental analysis.** Their asset, their comparables, their number. See `pricing-presentation` Part 1.
3. **Services and packages**, mapped to what they told you matters — not the full catalogue. See `pricing-presentation` Part 2.
4. **Objections as they arrive.** Diffuse, do not rebut. See `objection-handling`.
5. **The close.** See `pricing-presentation` Part 3.

Read `never-promise-list` before you walk in. The appointment is where the promises get made, because it is the moment where saying yes to something feels cheap and refusing feels awkward.

**If a fee or a term needs to move to close it — it does not move.** Quote the turnaround and escalate <!-- B12 -->. A deal closed on a concession you were not authorised to make is not closed; it is a problem with a signature on it.

---

## The First Hour Afterwards

### Signed on the call
Best outcome. Straight to S6 and the handoff package — see `pma-and-handoff`. Do not let the paperwork sit overnight; the post-signing sequence starts the same day.

### Not signed
1. **The agreement goes out the same business day.** Not tomorrow. S4 has the shortest maximum on the board for exactly this reason <!-- D6 -->.
2. A hard follow-up date inside 24 hours, into F15 and F16.
3. Move to S5 and update A6.
4. Write G10 while it is fresh: what they responded to, what they hesitated on, what was left unresolved. In their words.

S5 is the stage where deals die quietly. See `stage-gates`.

### No-show
Call within the hour — not the next day. Calm, no guilt:
> "Hey, we had time booked this morning and I want to make sure nothing's gone wrong on your end. Should we find another slot?"

Rebook the same day if you can. Log it in F4. A second no-show without a rebooking is a signal, not an accident: move to nurture and stop the appointment cadence.

---

## Board Writes

F3 date · F4 status · F5 decision-makers · F6/F7 analysis sent and date · B10 ownership verified · E10 recommended range with pull date · F12 package discussed · F13 fee discussed · G10 notes · then F15 and F16.

**F4 = Held only when it was genuinely held**, with all decision-makers present. Marking a short-handed meeting as Held corrupts the appointment-to-close rate, and that rate is the number the company uses to decide whether the problem is the pitch or the pipeline.
