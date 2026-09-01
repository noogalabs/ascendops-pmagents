---
name: meld-intake-triage
description: "You MUST use this skill whenever a NEW Property Meld maintenance request arrives and BEFORE any vendor or tech is assigned to it. It runs the front-gate intake: read the notes, classify emergency vs routine from the full meld content, pull the unit's meld history for callback signals, confirm we have photos/eyes on the problem, and actively request photos from the tenant if missing. True emergencies route to immediate mitigation while photos are requested in parallel; routine work waits at the photo gate. Pass the meld ID after the command. Do not assign a vendor or trade inline in the main session before this gate returns a decision."
triggers: ["new meld", "intake meld", "triage intake", "before assigning", "new maintenance request", "should I assign this", "assign a vendor", "photos before assign", "emergency meld subject", "is this ready to assign"]
context: fork
model: sonnet
---

# Meld Intake Triage — the front gate

Run the intake gate on the Property Meld passed in `$ARGUMENTS` (a meld ID like `MELD123`, optionally with a hint, e.g. `MELD123 water under sink, no photos yet`).

**Why this is a forked Sonnet skill:** intake triage is a repeating judgment call — read, gate on evidence, classify — not heavy multi-step root-cause diagnosis. Sonnet is the right tier for a classification/gate decision. It is `context: fork` so the gate runs in its own window and the main session stays lean for routing and comms; the triage never bloats the main context.

## Steps

1. **Read the meld** named in `$ARGUMENTS` — tenant notes, description, work_location, any attached media, current status (`pm work-orders inspect <meld_id> --json`).
2. **Pull the unit's meld history — callback check (hard rule 5).** List other melds at the same unit before any outreach.
3. **Classify emergency vs routine first** — against habitability/safety criteria (see hard rule 3), NOT against the subject line.
4. **If gas smell / gas leak is reported** — return `GAS_UTILITY_REFERRAL` with the tenant-facing message below EXACTLY, copying it verbatim and adding nothing before or after it. Do NOT request photos first, do NOT classify as `EMERGENCY_NOW`, and do NOT route property-side emergency mitigation.

   ```text
   Please call your gas company.
   ```
5. **Check for photos / eyes on the problem.** Does the meld carry photos (or an equivalent clear description that lets us pick the right trade with confidence)? Check `pm work-orders files <meld_id> --json`.
6. **If it is a true emergency** — route immediate mitigation now with the confirmed emergency facts. If photos are missing, request them from the tenant in parallel; do NOT park an active emergency waiting on photos.
7. **If it is routine and no photos / clear detail are present** — actively request photos from the tenant (hard rules 1, 2, 6) and WAIT. The meld is PARKED at the intake gate as "awaiting tenant photos," not advanced.
8. **If it is routine and the evidence gate passes** — return `CLEAR_TO_ASSIGN` to the main session with the classification + confirmed problem + any callback flag. The main session proceeds via the `vendor-coordination` skill (or in-house dispatch per SOUL.md autonomy rules).

## Hard rules — these fire EVERY time (the slippage these prevent is real)

1. **Photos-and-notes-before-routine-assign — HARD GATE.** No routine assignment until we have eyes on the problem (photos, or detail clear enough to pick the trade right). Blind assignment → wrong trade → wasted truck roll. In the property manager's own words: "we know it's right and we rarely do it" — so this gate fires automatically, not when we remember it. If photos are missing on routine work, request + wait; do not advance the meld. **The photo request MUST be sent ACTIVELY BY US** via `pm work-orders send-message --meld-id <id> --text "..."`, tenant-visible (not hidden). The PM auto-workflow acknowledgment ("we received this, submit photos / troubleshoot") does NOT satisfy this gate and NEVER counts as us having requested anything — see hard rule 6. After sending, the meld is `AWAITING_TENANT_PHOTOS` only because OUR message went out, never because the platform template did.
2. **Tenant photo-request uses generic, plain language.** Ask for "a photo of the problem" in plain words; do NOT name a trade or prescribe a cause in the request. (Generic-noun rule, learned from a real correction: the property manager edited a draft's "plumber" to "someone." Default to "someone"/"a tech," never a trade noun, in any tenant-facing intake line.)
3. **Classify, don't assume — the subject line is not the signal.** An "Emergency meld" subject is an intake CATEGORY, not an urgency signal. Emergency classification requires real habitability/safety criteria from the meld CONTENT (water/electrical/lockout/no-heat/no-AC/habitability), verified against the body — not the subject. Gas smell is not `EMERGENCY_NOW`; it returns `GAS_UTILITY_REFERRAL` with exactly this tenant-facing output and nothing else: `Please call your gas company.` (The "Emergency meld" subject trap was caught twice in one week in live operation; verify the activity body before treating as urgent.)
4. **Emergency dispatch is not photo-blocked.** If the full meld content already proves active water, electrical hazard, lockout, no-heat/no-AC in extreme conditions, or another non-gas habitability/safety threat, request missing photos in parallel but route mitigation immediately. Photos improve scope; they do not delay emergency response. Gas smell is different: return only `Please call your gas company.` as the tenant-facing output, not property-side emergency mitigation or extra action wording.
5. **Pull the unit/meld history BEFORE sending anything — callback check.** Before the photo/diagnostic request goes out, list the OTHER melds at the same unit (recent visits, prior work on the same system, who was there, what was done). Ask: were we just there? Is this a CALLBACK on a recent visit (same system, prior work may not have held, or our prior visit caused it)? Reference the relevant history in the message and flag callback status in the gate return. Do NOT fire a cold generic ask on a unit we just serviced — that is the same shortcut as relying on the template, in a different form. (Locked by the property manager after a real miss: a cold AC photo-ask went out on a unit with a recent AC-vent visit AND a contact-mismatch flag on file, MELD789.) Also verify the tenant CONTACT is correct if a prior meld flagged a wrong-number/mismatch.
6. **NEVER rely on anything from the PM auto-templates — property-manager HARD LOCK.** Treat the platform's auto-templates as if they do not exist. Every resident communication — photo requests, diagnostic questions, scheduling confirmations, follow-ups — comes ACTIVELY from us via `pm work-orders send-message`. The auto-ack having "asked for photos / troubleshooting" never counts as us doing anything. The recurring miss this rule kills: two real melds (a mold/moisture report, MELD790, and an AC callback, MELD789) were both left sitting on auto-ack only, with zero real outreach, on the same day.

## Trade Intake Modules

Gate-zero ALWAYS fires first regardless of trade: **active send, auto-ack never counts (hard rules 1 + 6), and pull unit history / callback check (hard rule 5).** Only then run the matching trade module below. Modules are a reusable shape — each new trade drops into the same structure:

> **Module shape (reusable):** TRIGGER (category/keywords) → TROUBLESHOOT (active diagnostic questions, often resident-fixable) → SAFETY/MITIGATION (immediate resident instruction if a hazard/damage-risk is present, surfaced prominently) → PHOTOS (the specific shots that let us pick parts) → URGENCY FORK (named routine-vs-urgent criteria) → ROUTE (which vendor/trade + what diagnostics to hand them for first-trip).

### Module 1 — HVAC (AC warm-air / no-cool / no-heat)

- **TRIGGER:** work_category HVAC, or keywords AC/cooling/warm air/not cooling/no heat/heat not working.
- **TROUBLESHOOT (active message to resident):** thermostat set to cool/heat and set past room temp (+ batteries)? outdoor/condenser unit running? when did they last change the air filter (a dirty filter is the #1 cause of warm air / weak cooling)? any ice built up on the coil or refrigerant lines?
- **SAFETY / MITIGATION — FROZEN COIL (surface prominently, not a checkbox):** if there is ANY ice on the coil/lines, immediately instruct the resident: **turn the AC OFF and run the FAN ONLY for a few hours to let it thaw, then switch cooling back on.** A frozen coil blows warm air, and running it iced risks compressor damage. This mitigation goes to the resident right away, like a safety step.
- **PHOTOS:** thermostat (showing setting + current temp), the outdoor unit, the air filter, and any ice or water.
- **URGENCY FORK (named decision):**
  - **URGENT (habitability dispatch path):** extreme indoor temp AND a vulnerable occupant (elderly, infant, medical condition), OR no-heat in winter. Treat as habitability — expedite HVAC, do not park as routine.
  - **ROUTINE:** tolerable indoor conditions, no vulnerable occupant. Standard HVAC scheduling at the photo gate.
  - ALWAYS ASK to make this call: how hot/cold is it inside, and is anyone elderly, an infant, or medically fragile in the home.
- **ROUTE:** your designated HVAC primary per the vendor roster (query the KB: `cortextos bus kb-query "HVAC vendor" --org $CTX_ORG`) or in-house, handed the gathered diagnostics + photos so they arrive with the right parts the first trip.

*(Future modules drop in here under the same shape: Plumbing — shutoff/mitigation + leak source; Appliance — make/model/serial + age; Electrical — panel/sounds safety branch; etc. HVAC is module #1 of the pattern.)*

## Invocation example

```
/meld-intake-triage MELD123
/meld-intake-triage MELD456 tenant says water under sink, no photos attached
```

The text after the command replaces `$ARGUMENTS`. The main agent stays on its lean model; this gate runs on Sonnet in its own window. It returns exactly one of: `GAS_UTILITY_REFERRAL` (tenant-facing output must equal `Please call your gas company.`), `EMERGENCY_NOW` (route non-gas mitigation immediately, photos parallel if needed), `AWAITING_TENANT_PHOTOS` (routine work parked, OUR request actively sent), or `CLEAR_TO_ASSIGN` (routine work has enough evidence and classification for the main session's live assignment path, with callback flag if the unit history showed one).
