---
title: "Maintenance Agent Setup Questionnaire"
source: "Derived from the maintenance coordinator agent spec and six shipped maintenance library docs (owner-reviewed, 2026-08-21)"
converted: 2026-08-21
google_doc_id: 1WjWw9xujNs7fjX_grrcwyCCNoDLvezOHYuXm3v56xbg
google_doc_url: https://docs.google.com/document/d/1WjWw9xujNs7fjX_grrcwyCCNoDLvezOHYuXm3v56xbg/edit
library_folder: 1fz1-NDVwhrfuvK0_LwrXywfHjx6lO1Vb
audience: all agents
status: reference
---

# Configuration Cover Sheet

Company name: ________________________________________
Org short-name: ________________________________________
Forward email: ________________________________________
Timezone: ________________________________________
Autonomy mode: ________________________________________
Unlock window: ________________________________________
Qualifying accuracy: ________________________________________
Resident messaging autonomy: ________________________________________
Work order closure autonomy: ________________________________________

> Work order closure autonomy is your company choice: answer yes only if the agent may close a completed work order under the configured mode; answer no (the default) for human approval before every closure.

> Autonomy mode notes: `copilot` (default) ships the earned-autonomy ladder;
> `supervised` keeps every category approval-gated permanently; `full` grants
> day-one autonomy with fair-housing screening still human-reviewed. Resident
> messaging autonomy is your choice: do you want your agents messaging
> residents directly, or would you rather approve those messages first?
> Answer yes for direct messaging under your configured mode rules; answer no
> (or leave it blank) and every resident message routes through you first.
> Built-in fair-housing safeguards stay on either way. A missing or unclear
> answer keeps messages routing through you. PLAIN WARNING for existing installs: re-running setup RESETS
> ladder progress — every earned unlock returns to locked and must be re-earned
> under the configured window.

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

An answer or cover value may begin with exactly one provenance tag: `[documented]`,
`[inferred]`, or `[NEEDS-DAVID]`. The configurator preserves the tagged source text in
`seat-config.json`, strips `[documented]` and `[inferred]` before derived or executable
use, and keeps `[NEEDS-DAVID]` on the named-skip path. Any other leading bracketed tag
fails shut for human confirmation; provenance annotations never become runtime values.

# Maintenance Agent Setup Questionnaire

## Maintenance Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic maintenance coordinator agent into your company's agent.

Companion documents shipped in this folder: Occupied Unit Maintenance Workflow, Occupied Unit Maintenance Board, Maintenance Auto-Send Message Library, Maintenance Coordinator Judgment Guide, Coordinator Scope Playbook, and Invoice Review Example.

### What This Is and How To Use It
The maintenance coordinator agent ships as a generic baseline: a workflow, a board, a message library, and a set of hard gates that work for any residential property management company. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every check, every clock, and every gate the agent runs reads from that file, and the generic documents themselves are never edited.

There are 38 questions in four groups: portfolio and state rules, thresholds and clocks, people and roles, platform and wiring. Most answers take a minute. A handful need your attorney or a pass through your standard lease; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law answer should be confirmed with your attorney before the agent relies on it.

### Group A: Portfolio and State Rules
A1. What is your portfolio size, which markets do you operate in, and what property classes do you manage?

Hint: Property class tunes urgency: Class C and D properties carry higher habitability risk, so the agent bumps a doubtful call one priority tier up.

Answer: ________________________________________

A2. What is the entry notice requirement in each jurisdiction you operate in?

Hint: Common working values: 24 hours for urgent work, 24 to 48 hours for routine, 5 to 7 days for scheduled work. State law governs; confirm with counsel.

Answer: ________________________________________

A3. What is the security deposit disposition deadline in your state?

Hint: This gates the timing of the deposit disposition notice. Many states use 30 days; confirm with counsel.

Answer: ________________________________________

A4. Does your state require certified mail for damage charge notices at move-out or for final notices before collections?

Hint: A counsel question. The answer controls how the two highest-consequence notice templates are delivered.

Answer: ________________________________________

A5. What dispute window do you give residents on damage charges?

Hint: Recommended: 7 to 14 business days for mid-tenancy charges; the statutory window applies at move-out. Your lease governs.

Answer: ________________________________________

A6. Which sections of your standard lease cover damage responsibility, the wear-and-tear definition, cost recovery, and collections or attorney fees?

Hint: Every damage charge notice must cite a lease section. Build this list once from your standard lease before any notice is drafted.

Answer: ________________________________________

A7. Which trades legally require a licensed contractor in your state?

Hint: The default always-vendor list is electrical, plumbing, HVAC, gas, structural, rekeying, pest, roofing, restoration, and pool. List anything your state adds or relaxes.

Answer: ________________________________________

A8. What are the habitability triggers in your state?

Hint: Temperature thresholds, hot water, and similar. Common default: no heat below 55F is an emergency. Confirm with counsel; this tunes the priority matrix.

Answer: ________________________________________

### Group B: Thresholds, SLAs, and Clocks
B1. What is your owner pre-approval threshold, and which owners have a different number in their management agreement?

Hint: Common default: $500 unless the management agreement says otherwise. List every per-owner override.

Answer: ________________________________________

B2. What is the hard emergency spend cap for after-hours dispatch without live human approval?

Hint: Name one number. Under the cap, an emergency dispatch to protect life or property proceeds with simultaneous notification; over the cap wakes the on-call human first.

Answer: ________________________________________

B3. What is your tenant responsibility floor, and does your lease actually say it?

Hint: Common default: items under $25 are resident-handled per the lease. Confirm the clause exists before the resident-responsibility message is ever allowed to send.

Answer: ________________________________________

B4. At what percentage above estimate does an invoice get flagged for review before payment?

Hint: Pick one number, commonly 10 or 15 percent, and use it everywhere: the invoice review and the board variance flag should read the same value.

Answer: ________________________________________

B5. What are your SLA windows per priority, and at what point does a card turn yellow?

Hint: Common defaults: Emergency dispatch within 2 hours and complete within 4; Urgent complete within 24 to 48 hours; Routine complete within 7 to 10 days. Yellow warning at 75, 60, and 50 percent of the window respectively.

Answer: ________________________________________

B6. How long does an owner have to answer an approval request, and does your management agreement authorize proceeding on owner silence?

Hint: Common default: 24 hours with a reminder at 12. The proceed-per-agreement message is a liability checkpoint: it never sends unless a human has confirmed the clause actually exists in the signed agreement. If the clause does not exist, that message class is disabled.

Answer: ________________________________________

B7. What are your callback and recurring-issue windows, and do your vendor agreements carry a labor warranty?

Hint: Common defaults: same issue within 30 days is a callback, within 31 to 90 days or 3 or more times in 12 months is recurring. A minimum 30-day vendor labor warranty is the standard roster condition; confirm your agreements carry it.

Answer: ________________________________________

B8. What are your quiet hours and your external communications window?

Hint: The hours inside which residents, vendors, and owners may be contacted. Anything outside the window queues for the next morning except live emergencies.

Answer: ________________________________________

B9. What is your on-call coverage window and your emergency response clock?

Hint: Common default: coordinator reachable 7 days a week, 8am to 8pm, with emergency response within 1 hour.

Answer: ________________________________________

B10. At what age does an open ticket escalate, and how fast must a finished job be closed out?

Hint: Common defaults: urgent open past 7 days and routine past 14 days escalate to the PM; close-out within 48 hours of confirmed completion.

Answer: ________________________________________

B11. What survey score counts as a low score, and what average are you holding the operation to?

Hint: Common default: below 3 out of 5 triggers the apology message and a callback flag; target average 4.0 or higher.

Answer: ________________________________________

B12. For non-habitability tenant-caused issues, how long does the resident get to self-repair before you dispatch a vendor and charge back?

Hint: Common default: 14 days. Your lease governs.

Answer: ________________________________________

### Group C: People and Roles
C1. Who is the property manager or supervisor of record for maintenance?

Hint: This person owns owner contact, chargeback decisions, habitability calls, and the human gate on every legal notice. Name them, and name anyone else authorized to approve maintenance decisions.

Answer: ________________________________________

C2. Who is on-call for life-safety and after-hours emergencies?

Hint: The human the after-hours dispatcher and the agent wake. Name and channel.

Answer: ________________________________________

C3. Who are your in-house techs, what are their confirmed skill sets and coverage areas, and what are their IDs in your maintenance platform?

Hint: The tech-versus-vendor dispatch decision only works against a real skill list. If a tech covers a region regardless of trade, say so.

Answer: ________________________________________

C4. Which markets or regions route to which people?

Hint: Any market where work orders go to a specific person or team, and any market where the standard vendor pool does not apply.

Answer: ________________________________________

C5. What is your approved vendor roster by trade?

Hint: For each vendor: trades, service area, license status, insurance on file, warranty terms, and any hands-off flags. If no roster exists yet, building it is a phase-zero task before the agent dispatches anything.

Answer: ________________________________________

C6. How is your after-hours line answered today, and where does the dispatcher log calls?

Hint: Staffed in-house, an answering service, or nothing yet. If a service, note whether it logs into your maintenance platform directly.

Answer: ________________________________________

C7. Who executes invoice payment on the bookkeeping side, and where does the maintenance-to-bookkeeping handoff land?

Hint: The agent reviews and packages invoices; money moves on the money side. Name the person or seat and the handoff location.

Answer: ________________________________________

C8. Which properties are owner-managed or hands-off for maintenance?

Hint: Properties where the owner uses their own contractor. The agent never chases or dispatches there. Start the exclusion list even if it is empty today.

Answer: ________________________________________

C9. Who is the backup decision-maker when the PM is unreachable and an SLA or legal clock is burning?

Hint: If there is no answer, that is the first thing to fix: a deadline with no available decision-maker is a company structure problem.

Answer: ________________________________________

### Group D: Platform and Wiring
D1. What maintenance platform and what accounting system do you run?

Hint: The maintenance platform is the operating brain: every communication, photo, and status lives there. The accounting system is the money and legal record.

Answer: ________________________________________

D2. How does work get written into your maintenance platform, and what are its known quirks?

Hint: How work orders are created, assigned, scheduled, messaged, and commented, and any platform behaviors that trip automation, for example status values that look like assignment but are not.

Answer: ________________________________________

D3. Which channels reach your residents, and which message classes go on which channel?

Hint: Portal, SMS, email. Formal legal notices are typically email only; acknowledgments and status updates typically portal plus SMS.

Answer: ________________________________________

D4. Which channels reach your vendors and in-house techs?

Hint: Portal, SMS, email, per audience. This carries the vendor work-order, nudge, and invoice-chase messages.

Answer: ________________________________________

D5. Which channel reaches your owners, and who actually sends over-threshold approval requests?

Hint: Portal or email, and confirm whether approval requests go out under the PM's name or the company's.

Answer: ________________________________________

D6. Which channels carry escalation alerts to the PM and on-call human?

Hint: The channel that gets looked at fast: chat, SMS, or both.

Answer: ________________________________________

D7. Where do warranty records live: appliance and system warranty documents, serials, and expiration dates per unit?

Hint: Checked before any appliance, HVAC, or roof dispatch so covered work goes to the warranty contact instead of a standard vendor. If the records do not exist, building them is a phase-zero task.

Answer: ________________________________________

D8. Where are lockbox and access codes stored, and how do access instructions reach the assigned vendor or tech?

Hint: A secured store. Codes go only to the assigned resource, never onto a resident-facing or owner-facing surface.

Answer: ________________________________________

D9. Where should the weekly open-ticket summary and the weekly KPI snapshot land?

Hint: Common cadence: Friday afternoon open-ticket summary to the supervisor, Monday morning leadership KPI review.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The configured maintenance library gets your values. The setup process writes the approved thresholds, clocks, people, and routing answers into the agent's managed configuration surfaces; no separate board-template spreadsheet ships in this edition.
- The agent boots in shadow mode. For about the first week the agent runs its daily checks silently and sends a calibration digest to the people you named in Group C. Nothing outbound, no actions. Shadow mode ends when a week of digests matches reality.
- Autonomy widens by consequence. Triage, tracking, and internal coordination run autonomously from day one. Every outbound message starts as a human-released draft, then message classes graduate to autonomous send one class at a time as they prove clean, lowest consequence first. Three gates never graduate at any setting: money committed, legal notices, and anyone entering a home. Those always end with a human.

Keep the answers current. When a threshold, a person, a vendor, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the maintenance coordinator agent specification and the six shipped maintenance documents in this library. Nothing in this document is legal advice; confirm every state-law answer with your attorney.
