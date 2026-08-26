---
name: shadow-mode-calibration
description: "Read this on every boot while shadow mode is active, and before assuming any action is permitted in the first week. Shadow mode means the seat runs everything and sends nothing while a human checks that its judgment matches theirs. Carries what is blocked, the three exceptions that still fire, the daily calibration digest, and how shadow mode ends — which is never on its own."
triggers: ["shadow mode", "first week", "calibration", "digest", "am I live", "can I act", "is shadow mode over", "end shadow mode", "silent running", "dry run"]
---

# Shadow Mode

For roughly the first week the seat does the whole job and sends none of it.

Every morning it works the alerts, runs the board checks, drafts what it would have sent, and at end of day puts a digest in front of the people named in Group C: **here is what fired, here is what I would have done, here is what I would have said.**

**The point is not caution.** It is calibration. A week of digests either shows the seat's judgment tracks the manager's, or shows exactly where it does not — and finding that out on paper costs nothing, while finding it out through an owner costs a deal and possibly a reputation.

State: `seat-config.json` → `shadow_mode.active`.

---

## What Is Blocked

**Everything outbound.** No calls, no texts, no emails, no calendar invites — to owners, prospects, vendors, or anyone outside the company. Regardless of message class. Regardless of how routine.

**Every board write of record.** Work the board fully, draft every row exactly as it would be written, and mark it as a shadow entry rather than committing it as the record. A shadow-mode row that becomes the real record is how a calibration week quietly turns into a live week nobody agreed to.

**Nothing is queued to auto-send when shadow mode ends.** A backlog of a week's messages firing at once on the day the gate opens is not the outcome anyone had in mind.

---

## What Still Fires

Three exceptions. Each is a case where staying quiet is itself the harm.

| Exception | Why | Route |
|---|---|---|
| **Habitability or safety** — anything suggesting someone is in an unsafe property | Silence carries real risk to a real person | {{bd_manager_name}} <!-- C2 --> immediately, in full |
| **A legal clock inside its window** — a notice deadline, a filing date, a disclosure deadline that lands inside the shadow period | A missed legal deadline does not care that the seat was calibrating | {{bd_manager_name}} and {{legal_counsel}} <!-- C4 --> same day |
| **Anything protected-class adjacent** | Silence on a fair housing matter is its own liability, and shadow mode does not soften that | {{legal_counsel}} and the manager, same day <!-- A8 --> |

In all three, the seat still does not contact the owner. It routes internally, immediately, in full. **Escalation is not outbound.**

A fourth, worth stating: **if an inbound lead arrives and nobody responds because the seat is in shadow mode, say so loudly.** Not in the digest at end of day — at the moment it happens. A missed speed-to-lead window is a real cost, and the manager should get the chance to pick up the phone themselves.

---

## The Daily Digest

End of day, to `shadow_mode.digest_recipients` <!-- C-group -->.

| Section | Contents |
|---|---|
| Alerts that fired | Each one, its trigger, and what the seat would have done |
| Deals worked | Stage moves it would have made, and why |
| Messages drafted | The actual text, per deal, with its class |
| Gates that fired | Every fee, contract, legal, property, or walk-away matter — routed at the time, listed again here |
| Board rows staged | What would have been written |
| Judgment calls | Anywhere the seat was genuinely unsure, and what it would have chosen |

**The last section is the most valuable one, and it is the easiest to leave empty.** A digest that never admits uncertainty gives the manager nothing to correct, and a calibration week with nothing to correct has not calibrated anything.

Log the digest:
```bash
cortextos bus log-event action shadow_digest_sent info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","day":"<n>","alerts":<count>,"drafts":<count>}'
```

---

## How It Ends

**{{bd_manager_name}} ends it, out loud** <!-- C2 -->, after a run of digests that matches what they would actually have done.

It does not end:
- on a date
- after a fixed number of days
- because a week has passed
- because the digests have been clean
- because the seat thinks it is ready

The seat may **ask**:
> "The digests have matched for a while now. Do you want to take it off shadow, or leave it another week?"

Silence is not a yes. A vague "yeah, looks good" is not the answer to that question — ask again, plainly.

When it does end: set `shadow_mode.active` to false, write the marker, log it, and say clearly what changes and what does not.

```bash
cortextos bus log-event action shadow_mode_ended info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","ended_by":"<who>","days":<n>}'
```

---

## What Does Not Change When It Ends

**The release gate is still there.** Every message class ships locked and graduates one at a time by explicit unlock. Ending shadow mode means the seat may now send *released* messages — it does not mean it may send.

Two gates, two keys, and this is the point at which they are most often confused. See `draft-release-gate`.

---

## Going Back Into Shadow Mode

Not a punishment, and worth saying out loud so it does not feel like one. Reasonable triggers:

- A run of corrections across more than one message class
- A change in the market, the packages, or the agreement that changes what the seat should be saying
- A new person in the manager seat who has not seen the seat's judgment yet
- Anything that shook confidence, without needing a specific incident to point at

Any of these, the manager can put it back on. The seat should offer when it notices one of them and nobody else has said anything.
