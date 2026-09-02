---
name: draft-release-gate
description: "Use this before any owner-facing message leaves — email, text, call script, recap, reminder, nurture touch, or post-signing sequence. It carries the staging flow, the message-class register, how a class graduates to autonomous send and how it demotes, and the checks every draft passes before it is even staged. Nothing owner-facing bypasses this."
triggers: ["send", "can I send", "draft", "stage this", "release", "outbound", "message class", "graduate", "unlock", "autonomous send", "approved to send", "release gate", "before sending"]
---

# The Release Gate

**Every owner-facing message is written to be sent and then staged.** Release is a human's.

This is separate from shadow mode. In shadow mode nothing leaves at all. Once shadow mode ends, this gate is still here. Ending one does not open the other — two gates, two keys. See `shadow-mode-calibration`.

---

## The Flow

1. **Write the message properly.** The real thing, in the seat's voice, ready to send. Not a summary, not three options, not a note about what you would say. A draft that needs rewriting before it can go is not a draft.
2. **Run the pre-stage checks** below.
3. **Stage it** with its class, the deal ID, and what it is responding to.
4. **A human releases it** — or edits it and releases, which is a correction, see below.
5. **Log the send**: F17 last touch, F19 total touches, and the channel and angle in G10.

---

## Pre-Stage Checks

Every draft, every time. In order, because the first one catches the most.

| # | Check | Skill |
|---|---|---|
| 1 | Any number, date, timeline, outcome, or coverage amount in it? | `never-promise-list` |
| 2 | Does anything in it touch a fee, a term, or a threshold? | `fee-and-contract-gates` — if yes, it does not get staged, it gets escalated |
| 3 | Anything protected-class adjacent? | `fair-housing-guard` — route, do not stage |
| 4 | Is every quoted figure from `business-development-config.json` rather than the generic example? | `pricing-presentation` |
| 5 | Is this a bare nudge? | `followup-and-nurture` — rewrite it |
| 6 | Does it name anyone it did not need to name? | `prospect-data-handling` |
| 7 | Would two or three plain sentences do the job better? | Usually yes |

A draft failing check 2 or 3 is not a draft. It is an escalation wearing one.

---

## The Class Register

Classes ship **locked**. Owner/prospect-facing classes stay locked until the member opts in on the cover sheet (external send autonomy: yes); once opted in, a class graduates by its accuracy window one category at a time, lowest consequence first, and {{bd_manager_name}} <!-- C2 --> can re-lock any class at any time. Never by this seat's own assessment outside that window, and never while the member has not opted in.

Register: `copilot-thresholds.json`.

Roughly in the order they should be considered for graduation:

| Class | What it covers |
|---|---|
| `board_row_write` | Board writes — stage moves, next actions, touch log |
| `alert_triage_note` | What fired, what was done, the new date |
| `internal_status_to_manager` | Status, digests, review packs |
| `meeting_confirmation` | Confirming a time already agreed on a live call |
| `appointment_reminder` | The reminder on an appointment already booked |
| `post_call_recap` | A recap restating only what was said and agreed |
| `nurture_value_touch` | An approved-library value touch — no offer, no fee, no promise |
| `intake_form_link_send` | The intake link after full execution |
| `cold_outreach_first_touch` | The first touch to someone who has not engaged |

**The ordering principle:** a message that only restates something a human already said and did is low consequence. A message that initiates a relationship, or that an owner could reasonably read as a commitment, is not.

`cold_outreach_first_touch` sits last deliberately. It is the highest-volume class and the most tempting to unlock early, and it is the one where a mistake reaches someone who never asked to hear from the company at all.

---

## What Never Appears In The Register

The never-graduates six: fee deviations, agreement language, anything on the Never-Promise List, legal and fair housing, red-flag property acceptance, and the decline or walk-away decision.

**A category in `copilot-thresholds.json` matching one of those is a defect in that file, not a permission.** Delete it and tell the manager. See GUARDRAILS.md.

---

## Graduation

A class unlocks when the manager says so, out loud, having seen a run of that class go out clean. Not on a count, not on a percentage, not on time served.

The seat may *ask*:
> "The appointment reminders have been going out unedited for a few weeks now. Worth unlocking that class, or leave it?"

The seat may not decide, and it may not treat silence as a yes.

---

## Demotion

**Any correction demotes the class immediately.**

A correction is any edit a human makes to a staged draft, and any "actually, don't send that." It is not a judgment on the message — it is information that the class is not calibrated, and the calibration is the point.

On a correction:
1. Class returns to locked, same day.
2. **Stop and wait.** No further sends in that class until the manager says go.
3. Log what was wrong and what the corrected version did differently. That log is the useful artefact — a demotion with no note repeats itself.

Demotion is never argued with. A class that was unlocked early can be unlocked again in a fortnight; a message that should not have gone cannot be recalled.

---

## Two Independent Gates

| | Shadow mode | Release gate |
|---|---|---|
| Blocks | Everything outbound, plus board writes of record | Owner-facing messages in locked classes |
| Ends when | The manager says the first week is done | Per class, by explicit unlock |
| Ending it opens | Nothing else | Nothing else |

Both are checked before anything leaves. Shadow mode active means the answer is no regardless of class.

---

## The Speed-To-Lead Exception That Is Not An Exception

An inbound lead needs a response inside the speed-to-lead window, and staging plus routine release will usually blow that window.

The answer is not to send it anyway. It is to **flag it for immediate release and say so**, and if immediate release is not going to happen, tell {{bd_manager_name}} so a human can pick up the phone. See `lead-intake`.

A staged speed-to-lead response sitting four hours in a queue is the same as no response, and pretending otherwise turns a process gap into a silent one.
