---
name: followup-and-nurture
description: "Load this whenever a deal goes quiet, a lead does not respond, an appointment is missed, or an owner says they are not ready yet. Covers the attempt ladder, the cold-lead recovery, the nurture cadence and its hard-date rule, the no-show recovery, re-engagement of lost deals, and the opt-out handling that overrides all of it."
triggers: ["follow up", "followup", "gone quiet", "no response", "cold lead", "nurture", "not ready", "re-engage", "no-show", "unresponsive", "cadence", "touch", "when do I stop", "opt out", "do not contact", "stop contacting"]
---

# Follow-Up and Nurture

Most deals are won in follow-up, not first touch. And most follow-up is done badly, because a bare nudge is easy and a real touch is not.

---

## The Rule That Governs Every Touch

**Every touch adds something or asks something real.** No exceptions.

Banned outright:
- "Just checking in"
- "Following up on my last email"
- "Wanted to bump this to the top of your inbox"
- Any message whose entire content is that you sent a previous message

A bare nudge tells the owner two things: that you have nothing new, and that their silence was a scheduling oversight rather than an answer. Neither helps.

**What counts as a real touch:** a market update relevant to their street. A property that leased nearby and what it went for. An answer to something left open. A genuine question about something that changed. A useful document. And varying the channel — a call after two emails is a different conversation, not the same one louder.

---

## The Attempt Ladder — Unresponsive Leads (S0)

Run to `clocks.max_contact_attempts` over `clocks.max_attempt_window_days` <!-- D5 -->, then archive as unresponsive.

Every attempt is logged. The count is what makes "unresponsive" a fact rather than an impression, and it is what lets the seat archive without wondering.

Vary the channel across the ladder. Six identical emails is one attempt repeated six times.

The last one is worth writing well:
> "I've tried you a few times and haven't managed to connect, so I'll assume the timing isn't right and stop here. If that changes, I'm easy to find."

No guilt, no final-notice framing. It reads as professional, and it leaves the door open — a meaningful share of these come back months later.

---

## Cold Leads (S0–S4)

Fires at `clocks.cold_lead_days_no_touch` <!-- D5 -->. An active deal going quiet is more urgent than an unresponsive one, because there was momentum and it is decaying.

Do not re-send. Change the angle: what has changed since you last spoke, what you have found out since, or the specific unresolved thing from the last conversation.

---

## No-Show Recovery

**Within the hour.** Not the next day.

> "Hey — we had time booked this morning and I want to make sure nothing's gone wrong at your end. Should we find another slot?"

Calm, no guilt trip. A guilt trip converts an embarrassed owner into an avoidant one.

Rebook the same day where possible. Log it in F2 or F4 — no-show rate is a real diagnostic. **A second no-show without a rebooking is an answer**: move to nurture and stop the appointment cadence.

---

## Nurture

For owners genuinely interested but not ready — timeline well out.

**The hard rule: every nurture record has a next-action date.** There is no open-ended nurture. A row without F16 is a row nobody will ever look at again, and the nurture tab quietly becomes an archive with a nicer name.

| | |
|---|---|
| Entry | Engaged, timeline pushed. Not lost, not active |
| Required | F16 set, F20 = Yes |
| Cadence | Per `clocks` <!-- D5 --> |
| Alert | No touch in `clocks.nurture_no_touch_alert_days` <!-- D5 --> |
| Exhausted | `clocks.nurture_exhausted_touches` over `clocks.nurture_exhausted_window_days` <!-- D5 --> → archive |
| Exit to active | They re-engage — re-enter at the right stage, not at S0 |

Nurture touches are the ones most likely to become nudges. Keep a rotation of things that are actually worth sending: what leased nearby and for how much, a seasonal note on timing, a relevant change in the market.

---

## Re-Engaging Lost Deals

After `clocks.lost_lead_reengagement_window_days` <!-- D5 -->, a lost deal becomes eligible again.

**Lead with what changed**, not with the fact that time passed:
> "We spoke back in [month] about [property] — you went a different way at the time, which was completely fair. A couple of things have shifted since then and I thought it was worth one message. [The specific thing.] Worth a conversation, or is it settled?"

Three rules:
- **Never reference the competitor they chose, and never disparage them.** Not once, not implicitly.
- One message. If it does not land, it is settled.
- If the loss reason was a fee, nothing has changed unless the manager says it has.

---

## Opt-Outs — This Overrides Everything

An opt-out, a do-not-contact, or any version of "stop contacting me":

1. **Stop every cadence on that contact immediately.** Every channel, not just the one they replied on.
2. **Log it the same minute** to `compliance.do_not_contact_list_location` <!-- compliance -->.
3. **Never contact again.** No re-engagement window applies. No new campaign applies. No "it's been a year" applies.
4. Archive the record as a hard no — immediately, not on a schedule <!-- D5 -->.

This outranks every clock in this document and every target in `activity_targets`. There is no version of a missed goal that justifies a touch to someone who asked you to stop.

**Source compliance is the same discipline running earlier:** never contact anyone whose source you cannot confirm as compliant. No purchased lists, no scraped lists. Unsure means it goes to the manager, not out. See `prospect-data-handling`.

---

## Logging

Every touch: F17 last touch date, F19 total touches, F15 next action, F16 due date, and a line in G10 saying what the touch actually was — channel and angle, not just "followed up".

**Why the angle matters:** without it, the next touch repeats the last one. The record of what was tried is what makes the cadence a sequence instead of a loop.
