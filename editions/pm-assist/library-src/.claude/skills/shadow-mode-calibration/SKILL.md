---
name: shadow-mode-calibration
effort: medium
description: "The first week: read every lane board, compute every clock, and send a daily digest of what you WOULD have flagged, filed, and drafted. No outbound, no board writes. Use every day until the PM explicitly ends shadow mode."
triggers: ["shadow mode", "calibration", "calibration digest", "first week", "go live", "am I live", "end shadow mode", "dry run", "would have"]
---

# Shadow Mode + Calibration Digest

For roughly the first week this seat runs silently. It reads, computes, and reports what it *would* have done. **Nothing outbound. No board writes of record.**

## Checking state

```bash
[[ -f "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.shadow-mode-ended" ]] && echo "LIVE" || echo "SHADOW"
```

Check this at session start, before anything outbound, and before any board write. When in doubt, you are in shadow.

## What runs in shadow

Everything except the last step:

- Lane board pulls — yes, with source and pull time
- Clock computation and the full alert pass — yes
- Daily Pulse, Monday Board, KPI scorecard — built, held in the digest
- Drafts — written, complete, held in the digest
- Classification and routing decisions — made and recorded, **not executed**
- Decision log filings — prepared, held

## What never runs in shadow

- Any outbound to an owner, tenant, vendor, or coordinator
- Any write to a board of record
- Any platform status, date, rate, or dollar change

**The one exception:** a genuine habitability or safety emergency, or a legal clock inside 12 hours, still reaches {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> directly. Shadow mode silences routine outbound; it does not silence an emergency. And a broker-only matter still routes same day per `broker-escalation` — silence on a Fair Housing matter is its own liability.

## The digest

One per day, to {{property_manager_name}}, at the configured digest time.

| Section | Content |
|---|---|
| Would have flagged | Every alert that fired, with its rule, its value, and the named owner it would have gone to |
| Would have drafted | Each draft by class, with the artifact attached or linked |
| Would have filed | Decisions prepared for the log |
| Would have routed | Gated matters, their class, and where they would have gone |
| Discrepancies | Sources that disagreed, both values, both pull times |
| Unresolved | Clocks with no named human, alerts with no owner, thresholds two lanes answered differently |
| Not live | Lanes dark because a state-law answer is unconfirmed |

The digest is a comparison instrument. Its value is in what the PM says was **wrong** — a flag that should not have fired, a draft with the wrong tone, an alert routed to the wrong person. Ask for that explicitly.

## How shadow mode ends

Only {{property_manager_name}} ends it, explicitly, after a week of digests matches reality. **You never end it yourself** — not on day 3 because calibration looks good, not because a deadline would be easier to hit live.

When they say go:
```bash
touch "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.shadow-mode-ended"
cortextos bus log-event action shadow_mode_ended info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","days":<n>,"ended_by":"property_manager"}'
```

Going live does **not** unlock any message class. Every class in `copilot-thresholds.json` is still locked, and every draft is still released by a human. Shadow mode and the release gate are two separate gates; ending one does not open the other.

## Re-entering shadow

If a configuration changes materially — new platform, new operating board, a lane board moves, thresholds re-set — propose re-entering shadow for that lane. The PM decides.
