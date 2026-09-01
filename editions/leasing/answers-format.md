---
title: "Leasing Agent Setup Questionnaire"
source: "Derived from the leasing agent spec (owner-reviewed, 2026-08-21) Section 4 and the leasing library docs"
converted: 2026-08-21
google_doc_id: 1I5TQu4zKxZwjinSsNuD1pazOwkYsltmBJdqTt4ucGlY
google_doc_url: https://docs.google.com/document/d/1I5TQu4zKxZwjinSsNuD1pazOwkYsltmBJdqTt4ucGlY/edit
library_folder: 16qrHGavF6BT3bHe1fACOdkldFYkBj5VH
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
Prospect response SLA (minutes): ________________________________________
Application decision SLA (business hours): ________________________________________
Leasing approval threshold (USD): ________________________________________
Renewal offer lead (days): ________________________________________
Renewal response window (days): ________________________________________

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

An answer or cover value may begin with exactly one provenance tag: `[documented]`,
`[inferred]`, or `[NEEDS-DAVID]`. The configurator preserves tagged source text in
`leasing-config.json`, strips `[documented]` and `[inferred]` before executable use,
and keeps `[NEEDS-DAVID]` on the named-skip path. Any other tag fails shut.

# Leasing Agent Setup Questionnaire

## Leasing Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic leasing agent into your company's agent.

Companion documents shipped in this folder: Leasing Message Template Library and Renewal and Rent-Increase Workflow.

### What This Is and How To Use It
The leasing agent ships as a generic baseline with a renewal workflow and message library that work for any residential property management company. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every check, every clock, and every template merge the agent runs reads from that file, and the generic documents themselves are never edited.

There are 39 questions in four groups: published application criteria and policy, state rules, showing rules, platform and wiring. Most answers take a minute. A handful need your attorney or a pass through your standard lease; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

Group A is the anchor of the whole interview. The criteria the agent publishes with every listing and checks every file against are YOUR company's published criteria, not the library's example table. If no written published criteria exist today, that is the first thing to fix before the agent boots: the property manager writes them, with counsel where flagged, and the agent publishes them.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law and fair-housing answer should be confirmed with your attorney before the agent relies on it.

### Group A: Published Application Criteria and Policy
A1. Do written, published screening criteria exist today, per property class?

Hint: The library's class-based example table is an example, not your policy. If the answer is no, writing and publishing criteria is a pre-boot blocker: the agent cannot check files against criteria that do not exist.

Answer: ________________________________________

A2. What is your income-to-rent ratio per property class?

Hint: Baseline example: 3x rent for Class B, 2.5 to 3x for Class C and D.

Answer: ________________________________________

A3. What is your credit score floor per property class?

Hint: Baseline example: 620 and up for Class B, 580 to 620 for Class C and D at the property manager's discretion.

Answer: ________________________________________

A4. What is your eviction lookback per property class?

Hint: Baseline example: 5 years for Class B, 3 years for Class C and D.

Answer: ________________________________________

A5. What is your individualized assessment process for criminal history, and who performs it?

Hint: Confirm with counsel. Blanket felony bans are a fair-housing risk; the property manager reviews every criminal flag personally, and the agent never touches this.

Answer: ________________________________________

A6. What is your application fee, and what is the refund policy by outcome?

Hint: Include the backup application rule: the common practice is that a backup applicant's fee is not charged until the primary application is denied.

Answer: ________________________________________

A7. What is your co-signer policy: allowed on which properties, and under what criteria?

Hint: Baseline: a co-signer meets the full income criteria independently.

Answer: ________________________________________

A8. What is the conditional approval menu the property manager may draw from?

Hint: Common options: a deposit multiple, prepaid rent, a shorter term. State law caps some of these; confirm with counsel.

Answer: ________________________________________

A9. What is your backup application policy, and what is the tie-break rule for competing applications?

Hint: A common tie-break: the first fully complete application by timestamp. Whatever the rule is, it must be written down and applied identically every time.

Answer: ________________________________________

A10. What is your pet policy per property, your pet fee schedule, and your pet screening service, and who owns the ESA documentation process?

Hint: Pet screening services are commonly third-party. ESA and service-animal requests are never pets: no pet fees, no pet screening, immediate routing to the property manager.

Answer: ________________________________________

A11. What is your Section 8 or housing voucher position per property?

Hint: Confirm with counsel per jurisdiction; this depends on the source-of-income answer in B6. The agent answers voucher questions only from the confirmed per-property answer and never improvises.

Answer: ________________________________________

A12. What are your hold policy parameters: approval-hold window, showings-during-processing default, and holding fee?

Hint: Baseline: a 48-hour approval hold. Decide whether showings continue while an application is processing, and whether a holding fee applies.

Answer: ________________________________________

A13. What is your occupancy limit standard?

Hint: Baseline: 2 persons per bedroom plus 1, following HUD guidance. Confirm with counsel for local rules.

Answer: ________________________________________

A14. What response deadline do you give applicants with incomplete files?

Hint: Baseline: 3 business days to supply missing items before the file goes inactive.

Answer: ________________________________________

### Group B: State Rules
B1. What is the security deposit disposition deadline in your state, and what date starts the clock?

Hint: Many states use around 30 days from termination of tenancy, but the trigger date matters as much as the count. Confirm with counsel.

Answer: ________________________________________

B2. What tenant notice-to-vacate period does your lease and your state require, and what notice ends a month-to-month tenancy in each direction?

Hint: A 30-day month-to-month notice is a common working value. Confirm with counsel.

Answer: ________________________________________

B3. What is your non-renewal notice period and required delivery method? Begin the answer with a labeled numeric line: `Notice days: NN`.

Hint: The first line must be `Notice days: NN`, using the confirmed integer notice period (commonly 30 to 60 days). Put delivery methods and service ownership on following lines. The property manager or the attorney serves non-renewal notices, never the agent. Confirm with counsel.

Answer: ________________________________________

B4. What are your state's application fee refund requirements?

Hint: Confirm with counsel. Common practice: do not refund on applicant abandonment unless state law requires it.

Answer: ________________________________________

B5. How long must application and screening records be retained in your state?

Hint: Commonly 2 to 3 years. Confirm with counsel.

Answer: ________________________________________

B6. Is source of income a protected class in any jurisdiction you operate in?

Hint: Confirm with counsel, per county and city, not just per state. The entire Section 8 conversation script forks on this answer.

Answer: ________________________________________

B7. What are the consequences of insufficient tenant notice, and what may be said to the tenant about them?

Hint: The property manager decides what is communicated; the agent only flags an insufficient notice, it never states consequences to a tenant.

Answer: ________________________________________

B8. Which properties in your portfolio were built before 1978?

Hint: The lead-based paint disclosure list. Build it once from your property records; every lease and listing for those properties carries the disclosure.

Answer: ________________________________________

B9. Does your company conduct a pre-move-out walkthrough inspection while the tenant still occupies the unit, and if yes, who conducts it?

Hint: Answer Y or N, and if yes name the seat that performs it. Some states, for example California, require offering a pre-move-out inspection on the tenant's request; confirm with counsel. This optional walkthrough happens roughly 1 to 2 weeks before move-out and is separate from the binding move-out inspection done after the unit is vacant. Record the approved inspection process and checklist location; this edition does not ship inspection checklist artifacts.

Answer: ________________________________________

### Group C: Showing Rules
C1. What is the showing method per property or class: self-show, agent-led, or both?

Hint: A property manager policy decision. Many companies run self-show for Class B and agent-led for higher-risk properties; write down the rule per property or class.

Answer: ________________________________________

C2. What self-show platform do you use, and what is the ID verification protocol before any code release?

Hint: If no ID verification protocol exists today, that is a pre-boot blocker for self-show: a code never releases without completed ID verification, no exceptions.

Answer: ________________________________________

C3. Who is on the showing agent roster, and where do their calendars live?

Hint: A showing time is never promised before the resource is confirmed. Name every person who can hold a showing and the calendar the agent checks.

Answer: ________________________________________

C4. What are your lockbox conventions: code rotation, and time-limited codes where offered?

Hint: Common practice: rotate codes on a schedule and use time-limited codes for higher-risk properties.

Answer: ________________________________________

C5. What showing windows and hours do you offer?

Hint: The days and hours inside which showings are booked. Anything outside the window is offered the next available slot, not an exception.

Answer: ________________________________________

C6. Which properties have video tour assets available?

Hint: The standing alternative when a prospect cannot attend in person or a unit is not yet showable. List what exists and where it lives.

Answer: ________________________________________

### Group D: Platform, People, and Wiring
D1. What property management software do you run?

Hint: For example AppFolio, Buildium, Rent Manager, Propertyware. The PM software is the system of record; the leasing board references it and never re-enters what it already holds.

Answer: ________________________________________

D2. What screening service do you use, and what may the agent see of a screening result?

Hint: The safe default: the agent sees summary flags and pass-or-fail against a documented criterion only, never report contents. Screening detail is FCRA-sensitive and never reaches an owner.

Answer: ________________________________________

D3. What e-signature tool do you use, and does it save executed documents into your PM software automatically?

Hint: If the executed lease does not auto-file, name who files it and where, because lease follow-up clocks read from that record.

Answer: ________________________________________

D4. Which listing platforms are in your syndication set, and who holds the credentials?

Hint: The set of sites a listing pushes to, plus the login owner for each. Most PM software syndicates automatically; list anything manual.

Answer: ________________________________________

D5. Where do rental inquiries land today?

Hint: PM software guest cards, a shared inbox, a phone line, portal forms. Every lead source must land somewhere the agent can read, or the speed-to-lead clock is fiction.

Answer: ________________________________________

D6. What is the outbound identity for prospect communications: SMS number, email identity, and sender persona?

Hint: Outbound goes under an approved company persona with human pre-send review. This shipped edition does not autonomously send external messages.

Answer: ________________________________________

D7. Who holds the property manager seat that decides approvals, denials, rates, renewal terms, and holds, and who is the owner-approval seat above it?

Hint: Name the human decision-maker for each. The agent prepares files and executes instructions; every housing decision belongs to the named person.

Answer: ________________________________________

D8. Where does the leasing board live: a spreadsheet bootstrapped from the board design document, or views built inside your PM software?

Hint: A common starting point: bootstrap the spreadsheet from the board design doc during the shadow phase, then decide whether to rebuild inside the PM software.

Answer: ________________________________________

D9. Which calendar carries showings and move-ins?

Hint: One calendar the agent reads and writes for showings, move-in appointments, and key handoffs. Name it and who else can see it.

Answer: ________________________________________

D10. Which channels carry escalations, and to whom?

Hint: The channel that gets looked at fast. Common shape: the property manager on a business-hours channel, and one urgent-anytime channel for the decision-maker above them.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The configured agent gets your values. Your Group A criteria, Group B clocks, and Group C showing rules become the configuration and operational instructions its checks, time clocks, and escalation flags read from.
- For about the first week, the agent operates as an operator-supervised copilot: a human reviews every draft and may compare it manually with the property manager's preferred response. This edition does not run an automated calibration digest or automatically exit a shadow phase.
- The agent remains a copilot after shadow mode: it prepares prospect replies, showing schedules, and file-chasing drafts, and a human approves every external message. Any future change to a message class requires an explicit operator-and-owner policy decision and a corresponding runtime configuration change. Application approvals and denials, adverse action notices, legal notices, money and committed terms, holds, and key or code release always end with a human.

Keep the answers current. When a criterion, a person, a property, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the leasing agent specification and the leasing documents in this library. Nothing in this document is legal advice; confirm every state-law and fair-housing answer with your attorney.
