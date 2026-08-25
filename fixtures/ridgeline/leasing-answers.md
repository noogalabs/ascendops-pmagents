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

Company name: Ridgeline Residential Management
Org short-name: ridgeline
Forward email: leasing@ridgeline.example
Timezone: America/Denver
Prospect response SLA (minutes): 15
Application decision SLA (business hours): 24
Leasing approval threshold (USD): 500
Renewal offer lead (days): 60
Renewal response window (days): 10

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

# Leasing Agent Setup Questionnaire

## Leasing Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic leasing agent into your company's agent.

Companion documents in this folder: Leasing Process End to End, The Leasing Board Full System Design, Leasing Coordinator Judgment Guide, Leasing Message Template Library, Renewal and Rent-Increase Workflow, CMA Process and Owner Conversation Scripts, Tenant Offer and Negotiation Scripts, and the Leasing Board Template spreadsheet.

### What This Is and How To Use It
The leasing agent ships as a generic baseline: a process, a board, a judgment guide, and a message library that work for any residential property management company. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every check, every clock, and every template merge the agent runs reads from that file, and the generic documents themselves are never edited.

There are 39 questions in four groups: published application criteria and policy, state rules, showing rules, platform and wiring. Most answers take a minute. A handful need your attorney or a pass through your standard lease; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

Group A is the anchor of the whole interview. The criteria the agent publishes with every listing and checks every file against are YOUR company's published criteria, not the library's example table. If no written published criteria exist today, that is the first thing to fix before the agent boots: the property manager writes them, with counsel where flagged, and the agent publishes them.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law and fair-housing answer should be confirmed with your attorney before the agent relies on it.

### Group A: Published Application Criteria and Policy
A1. Do written, published screening criteria exist today, per property class?

Hint: The library's class-based example table is an example, not your policy. If the answer is no, writing and publishing criteria is a pre-boot blocker: the agent cannot check files against criteria that do not exist.

Answer: Yes. Ridgeline publishes written screening criteria per property class, and the Class B and
  Class C tables are attached to every listing and to every published ad. CRITERIA-
  PUBLISHED=true for both classes in this fictional scenario.

A2. What is your income-to-rent ratio per property class?

Hint: Baseline example: 3x rent for Class B, 2.5 to 3x for Class C and D.

Answer: Class B: 3.0x monthly rent. Class C: 2.75x monthly rent. Measured on gross monthly household
  income with all adult applicants combined.

A3. What is your credit score floor per property class?

Hint: Baseline example: 620 and up for Class B, 580 to 620 for Class C and D at the property manager's discretion.

Answer: Class B: 620. Class C: 580, at the property manager's discretion, with a conditional-
  approval option instead of an outright denial.

A4. What is your eviction lookback per property class?

Hint: Baseline example: 5 years for Class B, 3 years for Class C and D.

Answer: Class B: 5 years. Class C: 3 years. Any filing inside the lookback routes to the property
  manager for individualized review; it is never an automatic denial.

A5. What is your individualized assessment process for criminal history, and who performs it?

Hint: Confirm with counsel. Blanket felony bans are a fair-housing risk; the property manager reviews every criminal flag personally, and the agent never touches this.

Answer: Dana Wren, Property Manager, performs every individualized assessment personally: nature and
  seriousness of the offense, time elapsed since it occurred, and evidence of rehabilitation,
  documented in the file every time. No blanket bans. The agent never evaluates criminal
  history and never states a criminal-history outcome to anyone; it routes the flag to Dana
  Wren and stops. Confirmed with counsel for this fictional scenario.

A6. What is your application fee, and what is the refund policy by outcome?

Hint: Include the backup application rule: the common practice is that a backup applicant's fee is not charged until the primary application is denied.

Answer: $55 per adult applicant. Non-refundable once screening is ordered; refunded in full if
  Ridgeline withdraws the unit before screening runs. A backup applicant is not charged until
  the primary application is denied or withdrawn.

A7. What is your co-signer policy: allowed on which properties, and under what criteria?

Hint: Baseline: a co-signer meets the full income criteria independently.

Answer: Allowed on Class C properties only. A co-signer must independently meet the full Class C
  income criterion of 2.75x and clear the same credit floor. Co-signers are not accepted on
  Class B.

A8. What is the conditional approval menu the property manager may draw from?

Hint: Common options: a deposit multiple, prepaid rent, a shorter term. State law caps some of these; confirm with counsel.

Answer: The property manager may draw from three options, in this order: a second month's security
  deposit, capped at two months' rent total under the fictional state cap; one month of
  prepaid rent; or a shortened initial term of six months. Confirmed with counsel for this
  fictional scenario.

A9. What is your backup application policy, and what is the tie-break rule for competing applications?

Hint: A common tie-break: the first fully complete application by timestamp. Whatever the rule is, it must be written down and applied identically every time.

Answer: Backup applications are accepted and ranked. Tie-break: the first fully complete application
  by timestamp wins, where complete means every adult application, every income document, and
  every fee received. The rule is published alongside the criteria and applied identically
  every time.

A10. What is your pet policy per property, your pet fee schedule, and your pet screening service, and who owns the ESA documentation process?

Hint: Pet screening services are commonly third-party. ESA and service-animal requests are never pets: no pet fees, no pet screening, immediate routing to the property manager.

Answer: Pets are allowed at all Ridgeline-leased properties. $300 non-refundable pet fee per pet
  plus $35 per month pet rent, two pets maximum, breed and weight limits published per class.
  Pet screening runs through the fictional PawCheck service. ESA and service-animal requests
  are never pets: no pet fee, no pet rent, no pet screening, and immediate routing to Dana
  Wren, who owns the reasonable-accommodation documentation process end to end.

A11. What is your Section 8 or housing voucher position per property?

Hint: Confirm with counsel per jurisdiction; this depends on the source-of-income answer in B6. The agent answers voucher questions only from the confirmed per-property answer and never improvises.

Answer: Pine Basin: Ridgeline accepts housing vouchers portfolio-wide, VOUCHER-POSITION-
  CONFIRMED=true. Cedar Mesa: the position is still with counsel, VOUCHER-POSITION-
  CONFIRMED=false. For any Cedar Mesa property the agent gives no voucher answer at all and
  routes the question to Dana Wren.

A12. What are your hold policy parameters: approval-hold window, showings-during-processing default, and holding fee?

Hint: Baseline: a 48-hour approval hold. Decide whether showings continue while an application is processing, and whether a holding fee applies.

Answer: Approval hold: 48 hours from the approval notice for the applicant to sign and fund.
  Showings continue while an application is processing, up until a lease is signed. Holding
  fee: one week's rent, credited to the first month's rent at signing and forfeited if the
  applicant withdraws.

A13. What is your occupancy limit standard?

Hint: Baseline: 2 persons per bedroom plus 1, following HUD guidance. Confirm with counsel for local rules.

Answer: Two persons per bedroom plus one, following HUD guidance. Confirmed with counsel for the
  fictional Pine Basin and Cedar Mesa jurisdictions.

A14. What response deadline do you give applicants with incomplete files?

Hint: Baseline: 3 business days to supply missing items before the file goes inactive.

Answer: 3 business days to supply the missing items. The file goes inactive after that, and the
  applicant is told the deadline and the consequence in writing at the moment the request is
  sent.

### Group B: State Rules
B1. What is the security deposit disposition deadline in your state, and what date starts the clock?

Hint: Many states use around 30 days from termination of tenancy, but the trigger date matters as much as the count. Confirm with counsel.

Answer: 30 calendar days. The clock starts on the later of the lease termination date or the date
  the tenant surrenders possession; Ridgeline records surrender as the key-return timestamp
  captured at move-out. Confirmed with counsel for this fictional scenario.

B2. What tenant notice-to-vacate period does your lease and your state require, and what notice ends a month-to-month tenancy in each direction?

Hint: A 30-day month-to-month notice is a common working value. Confirm with counsel.

Answer: Lease-end notice to vacate: 30 days written notice from the tenant. Month-to-month tenancy:
  30 days from the tenant and 30 days from Ridgeline, the same period in each direction.
  Confirmed with counsel for this fictional scenario.

B3. What is your non-renewal notice period and required delivery method?

Hint: Commonly 30 to 60 days. The property manager or the attorney serves non-renewal notices, never the agent. Confirm with counsel.

Answer: 30 days before the lease end date, delivered by first-class mail and email together, with
  proof of mailing retained in the unit record. Dana Wren or Ridgeline's attorney serves every
  non-renewal notice; the agent never serves one and never drafts one for direct send.
  Confirmed with counsel for this fictional scenario.

B4. What are your state's application fee refund requirements?

Hint: Confirm with counsel. Common practice: do not refund on applicant abandonment unless state law requires it.

Answer: The fictional jurisdictions impose no statutory refund requirement beyond disclosing the fee
  and its use before it is charged. Ridgeline does not refund on applicant abandonment.
  Confirmed with counsel for this fictional scenario.

B5. How long must application and screening records be retained in your state?

Hint: Commonly 2 to 3 years. Confirm with counsel.

Answer: 3 years from the application decision date, covering applications, screening results, and
  adverse-action records. Confirmed with counsel for this fictional scenario.

B6. Is source of income a protected class in any jurisdiction you operate in?

Hint: Confirm with counsel, per county and city, not just per state. The entire Section 8 conversation script forks on this answer.

Answer: Yes inside Pine Basin city limits; no elsewhere in the fictional Pine Basin county and no in
  Cedar Mesa. SOURCE-OF-INCOME-CONFIRMED=true, reviewed city by city and county by county with
  counsel for this fictional scenario.

B7. What are the consequences of insufficient tenant notice, and what may be said to the tenant about them?

Hint: The property manager decides what is communicated; the agent only flags an insufficient notice, it never states consequences to a tenant.

Answer: Insufficient notice leaves the tenant responsible for rent through the end of the proper
  notice period, subject to Ridgeline's duty to re-rent. Dana Wren decides what is said in
  every instance. The agent flags the short notice on the leasing board and says nothing to
  the tenant about consequences.

B8. Which properties in your portfolio were built before 1978?

Hint: The lead-based paint disclosure list. Build it once from your property records; every lease and listing for those properties carries the disclosure.

Answer: 41 of the 186 doors: the Pine Basin Elm Court and Foster Row buildings and the Cedar Mesa
  Alder Street duplexes. The list is held as a unit-level flag in WorkTrail and is confirmed
  present and complete for this fictional scenario; every lease and every listing for those
  units carries the lead-based paint disclosure.

B9. Does your company conduct a pre-move-out walkthrough inspection while the tenant still occupies the unit, and if yes, who conducts it?

Hint: Answer Y or N, and if yes name the seat that performs it. Some states, for example California, require offering a pre-move-out inspection on the tenant's request; confirm with counsel. This optional walkthrough happens roughly 1 to 2 weeks before move-out and is separate from the binding move-out inspection done after the unit is vacant. If your company runs one, the Pre-Move-Out Inspection Checklist in this library covers it; if not, the company goes straight to the Move-Out Inspection Checklist.

Answer: Yes. The turnover coordinator seat conducts the optional pre-move-out walkthrough 1 to 2
  weeks before move-out when the tenant requests it, and the binding move-out inspection after
  the unit is vacant also belongs to the turnover seat. Leasing schedules the walkthrough onto
  the shared calendar and hands off; leasing never conducts either inspection.

### Group C: Showing Rules
C1. What is the showing method per property or class: self-show, agent-led, or both?

Hint: A property manager policy decision. Many companies run self-show for Class B and agent-led for higher-risk properties; write down the rule per property or class.

Answer: Class B: self-show by default, agent-led on request. Class C: agent-led only. Any unit Dana
  Wren flags higher-risk is agent-led regardless of class.

C2. What self-show platform do you use, and what is the ID verification protocol before any code release?

Hint: If no ID verification protocol exists today, that is a pre-boot blocker for self-show: a code never releases without completed ID verification, no exceptions.

Answer: The fictional OpenDoorway self-show platform. Verification is three parts, all completed
  inside OpenDoorway before any code is released: government ID upload, a live selfie matched
  to that ID, and a $1 card authorization on a card whose name matches the ID. ID-
  VERIFICATION-PROTOCOL=true. A partial verification releases nothing, there are no
  exceptions, and the agent has no manual override.

C3. Who is on the showing agent roster, and where do their calendars live?

Hint: A showing time is never promised before the resource is confirmed. Name every person who can hold a showing and the calendar the agent checks.

Answer: Priya Sandoval covers Pine Basin and Colton Reyes covers Cedar Mesa for agent-led showings;
  Dana Wren backs up both markets. All three calendars live on the shared Ridgeline Leasing
  Calendar, which the agent reads before it offers any showing time to anyone.

C4. What are your lockbox conventions: code rotation, and time-limited codes where offered?

Hint: Common practice: rotate codes on a schedule and use time-limited codes for higher-risk properties.

Answer: Codes rotate on every tenancy change and, for vacant units, on the first Monday of each
  month. Time-limited codes valid for a 2-hour window are used for every self-show and for
  every unit flagged higher-risk. Codes live in the fictional encrypted access vault and never
  appear on a resident-facing or owner-facing surface.

C5. What showing windows and hours do you offer?

Hint: The days and hours inside which showings are booked. Anything outside the window is offered the next available slot, not an exception.

Answer: Monday through Saturday, 09:00 to 18:00 America/Denver. Sunday showings are not offered.
  Anything requested outside that window is offered the next available slot inside it, never
  booked as an exception.

C6. Which properties have video tour assets available?

Hint: The standing alternative when a prospect cannot attend in person or a unit is not yet showable. List what exists and where it lives.

Answer: Video tours exist for every Class B unit in the Pine Basin Elm Court and Foster Row
  buildings and for the Cedar Mesa Alder Street duplexes. They live in the fictional Ridgeline
  shared media library and are linked from each unit record in WorkTrail. No Class C video
  assets exist yet.

### Group D: Platform, People, and Wiring
D1. What property management software do you run?

Hint: For example AppFolio, Buildium, Rent Manager, Propertyware. The PM software is the system of record; the leasing board references it and never re-enters what it already holds.

Answer: WorkTrail is the property management system of record for the whole portfolio; LedgerPeak
  carries accounting. The leasing board references WorkTrail and never re-enters what
  WorkTrail already holds.

D2. What screening service do you use, and what may the agent see of a screening result?

Hint: The safe default: the agent sees summary flags and pass-or-fail against a documented criterion only, never report contents. Screening detail is FCRA-sensitive and never reaches an owner.

Answer: The fictional ClearFile Screening service. The agent sees only the summary flags and the
  pass-or-fail result against each published criterion: income, credit, eviction history, and
  criminal-flag-present. It never sees report contents, never a score narrative, and never the
  underlying records. No screening detail of any kind reaches an owner.

D3. What e-signature tool do you use, and does it save executed documents into your PM software automatically?

Hint: If the executed lease does not auto-file, name who files it and where, because lease follow-up clocks read from that record.

Answer: The fictional InkPath e-signature tool. Executed leases auto-file into the WorkTrail unit
  record within minutes of the last signature, and every lease follow-up clock reads from that
  WorkTrail record. AUTO-FILE=true.

D4. Which listing platforms are in your syndication set, and who holds the credentials?

Hint: The set of sites a listing pushes to, plus the login owner for each. Most PM software syndicates automatically; list anything manual.

Answer: WorkTrail syndicates automatically to the fictional RentBasin, HomeSeeker, and ListingHub
  networks; Dana Wren holds the WorkTrail credentials. One site is manual, the fictional Basin
  Community Board, posted by Priya Sandoval, who holds that login.

D5. Where do rental inquiries land today?

Hint: PM software guest cards, a shared inbox, a phone line, portal forms. Every lead source must land somewhere the agent can read, or the speed-to-lead clock is fiction.

Answer: Three places, all readable by the agent: WorkTrail guest cards for every syndicated lead,
  the leasing@ridgeline.example shared inbox for direct email, and the fictional leasing line
  +1-555-010-3310 for calls and texts, which drops transcripts into WorkTrail guest cards.

D6. What is the outbound identity for prospect communications: SMS number, email identity, and sender persona?

Hint: A common practice while a new agent proves itself: outbound goes under an approved company persona with pre-send review until a message class graduates to autonomous send.

Answer: SMS from +1-555-010-3310, email from leasing@ridgeline.example, both under the sender
  persona 'Ridgeline Leasing'. Every outbound message class starts in pre-send review and
  graduates to autonomous send one class at a time, on Dana Wren's decision.

D7. Who holds the property manager seat that decides approvals, denials, rates, renewal terms, and holds, and who is the owner-approval seat above it?

Hint: Name the human decision-maker for each. The agent prepares files and executes instructions; every housing decision belongs to the named person.

Answer: Dana Wren, Property Manager, decides approvals, denials, rates, renewal terms, and holds.
  Ellis Shore, Portfolio Director, is the owner-approval seat above her for concessions, off-
  policy terms, and anything outside the published criteria.

D8. Where does the leasing board live: a spreadsheet bootstrapped from the board design document, or views built inside your PM software?

Hint: A common starting point: bootstrap the spreadsheet from the board design doc during the shadow phase, then decide whether to rebuild inside the PM software.

Answer: A spreadsheet bootstrapped from the Leasing Board Template during the shadow phase.
  Ridgeline revisits rebuilding it inside WorkTrail after the first full leasing cycle.

D9. Which calendar carries showings and move-ins?

Hint: One calendar the agent reads and writes for showings, move-in appointments, and key handoffs. Name it and who else can see it.

Answer: The shared Ridgeline Leasing Calendar carries showings, move-in appointments, and key
  handoffs. Dana Wren, Priya Sandoval, Colton Reyes, and the turnover coordinator seat can all
  see it.

D10. Which channels carry escalations, and to whom?

Hint: The channel that gets looked at fast. Common shape: the property manager on a business-hours channel, and one urgent-anytime channel for the decision-maker above them.

Answer: Dana Wren on the Ridgeline Leasing chat channel during business hours. Ellis Shore on SMS at
  any hour for fair-housing questions, legal notices, and anything with a burning statutory
  clock.

### What Happens Next
Your answers do three things, in order:

- The board gets your values. The Leasing Board Template spreadsheet in this folder is bootstrapped from the board design document; your Group A criteria, Group B clocks, and Group C showing rules become the values its status columns, time clocks, and escalation flags read from.
- The agent boots in shadow mode. For about the first week the agent runs the daily board sweep silently, drafts every message it would have sent, and reports a calibration digest to the people you named in Group D. Nothing outbound, no actions. Shadow mode ends when a week of drafts matches what the property manager would have sent.
- Autonomy widens by consequence. Prospect replies, showing scheduling, and file chasing graduate to autonomous send one message class at a time as they prove clean, lowest consequence first. Some gates never graduate at any setting: application approvals and denials, adverse action notices, legal notices, money and committed terms, holds, and key or code release. Those always end with a human.

Keep the answers current. When a criterion, a person, a property, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the leasing agent specification and the leasing documents in this library. Nothing in this document is legal advice; confirm every state-law and fair-housing answer with your attorney.

