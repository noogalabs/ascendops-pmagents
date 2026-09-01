---
name: work-order-intake-triage
description: "Use this skill whenever a new maintenance work order arrives and before any vendor or tech is assigned. It reads the record, classifies urgency, checks unit history, and enforces the evidence gate. Use the selected platform skill for exact commands."
triggers: ["new work order", "intake work order", "triage intake", "before assigning", "new maintenance request", "should I assign this", "assign a vendor", "photos before assign", "emergency work order subject", "is this ready to assign"]
context: fork
---

# Work-Order Intake Triage — the front gate

Run the intake gate on the work order passed in `$ARGUMENTS` (an ID like `WO123`, optionally with a hint).

The gate runs in its own context so the main session stays lean for routing and communications.

## Steps

1. **Read the work order** named in `$ARGUMENTS` — resident notes, description, work location, attached media, and current status. Run the platform skill's inspect command.
2. **Pull the unit's work order history — callback check (hard rule 5).** List other work orders at the same unit before any outreach.
3. **Classify emergency vs routine first** — against habitability/safety criteria (see hard rule 3), NOT against the subject line.
4. **If gas smell / gas leak is reported** — return `GAS_UTILITY_REFERRAL` with the tenant-facing message below EXACTLY, copying it verbatim and adding nothing before or after it. Do NOT request photos first, do NOT classify as `EMERGENCY_NOW`, and do NOT route property-side emergency mitigation.

   ```text
   Please call your gas company.
   ```
5. **Check for photos / eyes on the problem.** Does the work order carry photos or equivalent clear detail? Run the platform skill's list-files command.
6. **If it is a true emergency** — route immediate mitigation now with the confirmed emergency facts. If photos are missing, request them from the tenant in parallel; do NOT park an active emergency waiting on photos.
7. **If it is routine and no photos / clear detail are present** — actively request photos from the tenant (hard rules 1, 2, 6) and WAIT. The work order is PARKED at the intake gate as "awaiting tenant photos," not advanced.
8. **If it is routine and the evidence gate passes** — return `CLEAR_TO_ASSIGN` to the main session with the classification + confirmed problem + any callback flag. The main session proceeds via the `vendor-coordination` skill (or in-house dispatch per SOUL.md autonomy rules).

## Hard rules — these fire EVERY time (the slippage these prevent is real)

1. **Photos-and-notes-before-routine-assign — HARD GATE.** No routine assignment until we have eyes on the problem. If photos are missing, run the platform skill's resident-message command to request them, then wait. An automated acknowledgment does not satisfy this gate.
2. **Tenant photo-request uses generic, plain language.** Ask for "a photo of the problem" in plain words; do NOT name a trade or prescribe a cause in the request. (Generic-noun rule, learned from a real correction: the property manager edited a draft's "plumber" to "someone." Default to "someone"/"a tech," never a trade noun, in any tenant-facing intake line.)
3. **Classify, don't assume — the subject line is not the signal.** An "Emergency work order" subject is an intake CATEGORY, not an urgency signal. Emergency classification requires real habitability/safety criteria from the work order CONTENT (water/electrical/lockout/no-heat/no-AC/habitability), verified against the body — not the subject. Gas smell is not `EMERGENCY_NOW`; it returns `GAS_UTILITY_REFERRAL` with exactly this tenant-facing output and nothing else: `Please call your gas company.` (The "Emergency work order" subject trap was caught twice in one week in live operation; verify the activity body before treating as urgent.)
4. **Emergency dispatch is not photo-blocked.** If the full work order content already proves active water, electrical hazard, lockout, no-heat/no-AC in extreme conditions, or another non-gas habitability/safety threat, request missing photos in parallel but route mitigation immediately. Photos improve scope; they do not delay emergency response. Gas smell is different: return only `Please call your gas company.` as the tenant-facing output, not property-side emergency mitigation or extra action wording.
5. **Pull the unit/work order history BEFORE sending anything — callback check.** Before the photo/diagnostic request goes out, list the OTHER work orders at the same unit (recent visits, prior work on the same system, who was there, what was done). Ask: were we just there? Is this a CALLBACK on a recent visit (same system, prior work may not have held, or our prior visit caused it)? Reference the relevant history in the message and flag callback status in the gate return. Do NOT fire a cold generic ask on a unit we just serviced — that is the same shortcut as relying on the template, in a different form. (Locked by the property manager after a real miss: a cold AC photo-ask went out on a unit with a recent AC-vent visit AND a contact-mismatch flag on file, WO789.) Also verify the tenant CONTACT is correct if a prior work order flagged a wrong-number/mismatch.
6. **NEVER rely on platform auto-templates — property-manager HARD LOCK.** Every resident communication comes actively from us through the platform skill. An auto-ack never counts as outreach.

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
/work-order-intake-triage WO123
/work-order-intake-triage WO456 tenant says water under sink, no photos attached
```

The text after the command replaces `$ARGUMENTS`. It returns `GAS_UTILITY_REFERRAL`, `EMERGENCY_NOW`, `AWAITING_TENANT_PHOTOS`, or `CLEAR_TO_ASSIGN`, with the callback flag when history shows one.
