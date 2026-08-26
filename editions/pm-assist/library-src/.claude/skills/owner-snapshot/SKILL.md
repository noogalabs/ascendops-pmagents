---
name: owner-snapshot
effort: low
description: "Per-owner state: communication tag, preferred channel, reserve position, open items, and threshold overrides. Read it before any owner-facing draft; maintain it on change and monthly."
triggers: ["owner snapshot", "owner tag", "owner preference", "how does this owner", "owner channel", "owner reserve", "high touch owner", "silent investor", "owner file", "which owner"]
---

# Owner Snapshot

One row per owner. Read before any owner-facing draft; the tone, the channel, and the threshold all come from here.

## The row

| Field | Source | Rule |
|---|---|---|
| Owner | — | Legal entity and the human contact |
| Tag | C4 | `silent investor` / `collaborative` / `high touch`. The tag lives where `seat-config.owner_comms.owner_tags.tag_location` says |
| Preferred channel | C4 / D5 | Per-owner, not the portfolio default |
| Approval threshold | B1 | Their override if the management agreement has one, otherwise {{owner_approval_threshold}} <!-- B1: owner pre-approval spend threshold -->. **Check this every time** |
| Reserve position | B5 | Per unit, against {{owner_reserve_minimum}} <!-- B5: minimum owner reserve per unit -->, with the pull time |
| Units | — | Which doors, with class |
| Open items | — | Approvals pending, promises open, exceptions routed |
| Report preferences | D6 | Channels, and whether they get the high-touch follow-up call |
| Last contact | — | When, by whom, on what |

## What the tag changes

The tag changes **tone and cadence**. It never changes what is true, what a threshold is, or what gets disclosed.

- **Silent investor** — the all-clear templated update, on schedule, low volume. Still goes out even when nothing happened
- **Collaborative** — same facts, more context, expects a reply thread
- **High touch** — same facts, plus the follow-up call on report day if D6 says so

A tag is never a reason to soften a number, delay a bad month, or skip a disclosure.

## The reserve flag

When an owner's reserve falls below {{owner_reserve_minimum}} per unit, the row flags and the item lands on the Daily Pulse. **The reserve conversation itself always belongs to {{property_manager_name}} <!-- A2: who holds the Property Manager seat -->.** You surface the number, its pull time, and the gap. You do not ask the owner to fund it.

## Owner contact line

Per C3, and per whatever is configured in `seat-config.owner_comms`:

- Statements and templated updates: preparable and, once that class has graduated, sendable by you
- **Any owner who responds with a concern goes to the PM immediately.** Regardless of how simple the concern reads. You do not answer it, not even the easy part
- A difficult month is always framed by the PM, never by a template

## Maintenance of the snapshot

- On change: threshold override, channel change, tag change, reserve movement, new unit
- Monthly: full refresh alongside the Month-End Pack
- Every change is logged with its source. An override you cannot source is not applied
