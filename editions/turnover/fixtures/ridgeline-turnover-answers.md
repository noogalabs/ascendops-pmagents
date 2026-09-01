---
title: "Turnover Agent Setup Questionnaire"
source: "Derived from the turnover and make-ready coordinator agent spec (owner-reviewed, 2026-08-21) and the ten turnover library docs"
converted: 2026-08-21
google_doc_id: 17fM7U3fHcIn3zJEthQFR-ff8ALa4i_agWMsGz3ewxag
google_doc_url: https://docs.google.com/document/d/17fM7U3fHcIn3zJEthQFR-ff8ALa4i_agWMsGz3ewxag/edit
library_folder: 1b8QQF8nw0CkVmN_WDxU9OeWSvFYEXNgn
audience: all agents
status: reference
---

# Configuration Cover Sheet

Company name: Ridgeline Residential Management
Org short-name: ridgeline
Forward email: turnover@ridgeline.example
Timezone: America/Denver
Autonomy mode: [documented] copilot
Unlock window: [documented] last_10
Qualifying accuracy: [documented] null

Day mode start: 08:00
Day mode end: 18:00
Inspection SLA hours: 48
Scope SLA hours: 24
Stale-stage alert days: 2

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

# Turnover Agent Setup Questionnaire

## Turnover Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic turnover and make-ready coordinator agent into your company's agent.

Companion documents shipped in this folder: In-House Tech vs. Vendor Dispatch Decision Matrix, Make-Ready Checklist, Monthly Turnover Performance Report Template, Move-Out Final Inspection Checklist, Owner Make-Ready Communication Templates, Pre-Move-Out Inspection Checklist, The Coordinator Scope Playbook, The Make-Ready Deep Dive, Turn-Time and Make-Ready Budget Benchmarks by Property Class, and Turnover Tracking Board Full System Design.

### What This Is and How To Use It
The turnover and make-ready coordinator agent ships as a generic baseline: a tracking board, a make-ready process, a scope playbook, inspection checklists, owner communication templates, and a set of hard gates that work for any residential property management company. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every check, every clock, and every gate the agent runs reads from that file, and the generic documents themselves are never edited.

There are 34 questions in five groups: legal and deposit interlocks, property classes and benchmarks, scope and owner-approval rules, roles and people, platform and wiring. Most answers take a minute. A handful need your attorney or a pass through your standard lease; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law answer should be confirmed with your attorney before the agent relies on it.

### Group A: Legal and Deposit Interlocks
A1. What is the security deposit disposition deadline in your state, and how fast must the move-out evidence package reach the deposit disposition process?

Hint: The statutory deadline is owned by your bookkeeping process; many states use 30 days from lease termination. Recommended handoff SLA: complete evidence package (move-in versus move-out comparison, photos, invoices) within 48 hours of the move-out inspection. Confirm with counsel.

Answer: 30 calendar days from lease termination for the disposition itself (CROSS-SEAT: owned by the maintenance seat's A3 answer, recorded here as a pointer, not a second copy). Turnover-owned component: the complete evidence package (move-in versus move-out comparison, photos, invoices) reaches Avery Moss within 48 hours of the move-out inspection.

A2. Is a pre-move-out inspection legally required or regulated in your state?

Hint: Some states require offering one or regulate its timing and notice. Confirm with counsel before adopting the pre-move-out walkthrough as a standard step.

Answer: No. Neither Pine Basin nor Cedar Mesa requires or regulates a pre-move-out inspection in this fictional scenario. PRE-MOVE-OUT-REQUIRED-BY-LAW=false, but Ridgeline adopts the pre-move-out walkthrough as a standard step by company policy, so the step is armed by policy rather than by statute.

A3. What dispute window do you give residents on damage charges?

Hint: Recommended: 7 to 14 days for mid-tenancy charges; the statutory window applies at move-out. Your lease governs; confirm with counsel.

Answer: 10 business days for mid-tenancy damage charges; the applicable statutory window governs at move-out. (CROSS-SEAT: same fact as the maintenance seat's A5 answer; pointer, not a second copy.)

A4. Does your state require certified mail for damage charge notices at move-out or for final notices before collections?

Hint: A counsel question. The answer controls how the highest-consequence notice templates are delivered.

Answer: Yes. CERTIFIED-MAIL-CONFIRMED=true for damage charge notices at move-out and for final notices before collections. (CROSS-SEAT: same fact as the maintenance seat's A4 answer; pointer, not a second copy.)

A5. Which sections of your standard lease cover damage responsibility, the wear-and-tear definition, cost recovery, and collections or attorney fees?

Hint: Every damage charge notice must cite a lease section. Build this list once from your standard lease before any notice is drafted.

Answer: Sections 12.2 Damage Responsibility, 12.4 Normal Wear, 18.1 Cost Recovery, and 21.3 Collections and Fees. (CROSS-SEAT: same fact as the maintenance seat's A6 answer; pointer, not a second copy.)

A6. Who does your lease assign lawn care and HVAC filter changes to?

Hint: This drives the damage-versus-wear call on two of the most common move-out findings. Read the answer from your lease form, not from memory.

Answer: Fictional lease section 9.3 assigns lawn care to the resident at single-family and townhome units and to Ridgeline at the multifamily properties; HVAC filter changes are assigned to the resident, with filters supplied by Ridgeline at each renewal. Read from the standard lease form, not from memory.

### Group B: Property Classes and Benchmarks
B1. Which property class is each of your units: A, B, C, or D?

Hint: Every benchmark, budget band, and status color keys off the class map. If no per-unit map exists, building it is a phase-zero task before the agent grades anything.

Answer: 186 doors of record: 112 Class B and 74 Class C. No Class A or Class D units. The per-unit class map lives on the Ridgeline Turnover Board unit tab and is complete today, so no phase-zero task is open.

B2. What are your turn-time targets per property class?

Hint: Lead the answer with `Default turn target days: NN`, then give the per-class targets and warning bands. Common working values: Class B 12 days, Class C 14 days, Class D 21 days.

Answer: Default turn target days: 12
  Class B 12 days from possession to rent-ready; Class C 14 days. Warning band at 80 percent of target; overdue above target. Modal class by door count is Class B, so 12 is the portfolio default number.

B3. What are your make-ready budget bands per class for a standard turn with no major damage?

Hint: Common working values: Class B $1,000, Class C $800, Class D $1,200 as the on-budget ceilings, with warning and over-budget bands above.

Answer: Class B $1,100 and Class C $850 as the on-budget ceilings for a standard turn with no major damage. Warning band from the ceiling to 125 percent; over-budget above 125 percent.

B4. What are your punch-list completion deadlines per class?

Hint: Common working values: 24 hours for Class B and C, 48 hours for Class D.

Answer: 24 hours for both Class B and Class C after a failed final inspection.

B5. What weights does your turnover grading scorecard use?

Hint: Common default: turn time 30, budget 25, inspection quality 20, owner communication 15, documentation 10. Adopt the framework as written unless you want different weights.

Answer: Framework default adopted as written: turn time 30, budget 25, inspection quality 20, owner communication 15, documentation 10.

B6. What is your turnover-rate baseline, and what door count of record does it divide by?

Hint: The monthly report header needs both numbers. Pick the door count source once and keep it consistent.

Answer: Baseline turnover rate 38 percent annualized. Door count of record is 186, taken from the Ridgeline unit roster, and that roster is the single denominator source for every monthly report.

### Group C: Scope and Owner-Approval Rules
C1. What is the pre-approved reserve threshold per owner?

Hint: Common default: $500 unless the management agreement says otherwise. This single number is the auto-approve line for the whole make-ready flow; list every per-owner override.

Answer: $500 base pre-approved reserve. Fictional owner overrides: Juniper Holdings $750; Northstar Homes $350. NOTE: these are make-ready reserve numbers and are deliberately different from the same owners' repair-spend numbers on the maintenance seat; the two are separate authorities, not a contradiction.

C2. What is your scope-change ladder?

Hint: Common default: within the reserve, proceed; over by less than $500, call the owner plus an email confirmation within 2 hours; over by $500 or more, formal bid with a 24-hour owner approval window. A human executes the call step.

Answer: Within the reserve, proceed. Over by less than $500, call the owner plus an email confirmation within 2 hours. Over by $500 or more, formal bid with a 24-hour owner approval window. A human executes the call step; the agent drafts and tracks it but never places the call.

C3. For safety items, is fix-first-notify-after pre-authorized, and up to what dollar cap?

Hint: Safety items: smoke and CO detectors, exposed wiring, gas smell, no heat or air conditioning in extreme weather. Name one cap number; above it, the on-call human is woken first.

Answer: Yes, fix-first-notify-after is pre-authorized for safety items up to $600. Above $600 the on-call human is woken first. Safety items are smoke and CO detectors, exposed wiring, gas smell, and no heat or air conditioning in extreme weather.

C4. When an owner is silent past the approval window on a scope request, who decides proceed-without-item versus hold?

Hint: Common default window: 24 hours. Name the decision-maker for the silent-owner call; the agent chases the response but never makes this decision.

Answer: Ellis Shore, Portfolio Director, decides proceed-without-item versus hold once the 24-hour approval window closes with no owner response. The agent chases the response and surfaces the burning clock but never makes this decision.

C5. When may a scope draft include suggested upgrades?

Hint: Common default: upgrades such as plank flooring over carpet in lower property classes are always presented as an owner option, never dispatched without approval.

Answer: Upgrades may be included in a scope draft only as a clearly labeled owner option with its own line-item price, never dispatched without written owner approval. Plank flooring over carpet at Class C units is the common case.

C6. What are your standing no-approval items on every turnover?

Hint: Common default list: rekey, deep clean, preventive pest treatment, and HVAC filter change on every turnover; never skipped, never asked.

Answer: Rekey, deep clean, preventive pest treatment, and HVAC filter change on every turnover. Never skipped, never asked, and never charged against the owner approval ladder.

C7. At what security-deposit chargeback amount must the coordinator stop and get PM review before it goes on the disposition? Set a per-line-item number and a per-unit-total number.

Hint: This is distinct from the owner pre-approval threshold in C1. That threshold gates repair-spend authority; this one gates deposit-deduction authority, a different authority, so keep the two numbers labeled separately. The chargeback number is commonly set below the repair-approval line. Below both the per-line and the per-unit numbers, with documented evidence and no dispute anticipated, the coordinator proceeds; at or above either number, or on any dispute, missing documentation, or ambiguous wear-versus-damage, it goes to the PM before the disposition is drawn.

Answer: Per-line-item $150 and per-unit total $400. At or above either number, or on any dispute, missing documentation, or ambiguous wear-versus-damage call, the coordinator stops and gets PM review before the disposition is drawn. These are deposit-deduction numbers and are deliberately separate from the C1 repair-approval reserve.

### Group D: Roles and People
D1. Do you have in-house techs today, or are you vendor-only?

Hint: This determines the whole tech column of the dispatch decision matrix. If vendor-only, the matrix collapses to its vendor column and the on-site inspector question below becomes the first hire conversation.

Answer: In-house techs today, three of them, plus the vendor roster for licensed and specialty trades. (CROSS-SEAT: the tech roster with skills, coverage areas, and platform IDs is owned by the maintenance seat's C3 answer; this seat records the yes-or-no shape and points at that roster.)

D2. Who conducts pre-move-out, move-out, and final inspections on-site?

Hint: Inspections need a person at the property within tight windows. Name the person or role per inspection type.

Answer: Pre-move-out inspections are conducted by the market's in-house tech: Tessa Reed in Pine Basin, Omar Flint in Cedar Mesa. Move-out and final inspections are both conducted by Morgan Vale, Maintenance Supervisor.

D3. Who is the property manager of record for scope escalation and the damage charge notice gates?

Hint: This person approves scope escalations and releases every damage charge notice. Name them, and name anyone else authorized to approve turnover decisions.

Answer: Ellis Shore, Portfolio Director, is the property manager of record for turnover scope escalation and for releasing every damage charge notice. Also authorized to approve turnover decisions: Morgan Vale, Maintenance Supervisor.

D4. Who is the photographer of record for listing photos, and what is their turnaround SLA?

Hint: The listing cannot launch without photos; the SLA keeps the final stage from stalling.

Answer: Basin Media, a fictional contract photographer, with a 24-hour turnaround SLA from rent-ready certification to delivered listing photos.

D5. Who receives the leasing handoff when a unit goes rent-ready?

Hint: The last board stage hands the unit to the leasing pipeline. Name the person or team.

Answer: Wren Calloway, Leasing Coordinator, receives the unit at rent-ready certification. The handoff is the last turnover board stage and the first leasing pipeline stage.

D6. Who executes the security deposit disposition today?

Hint: The person who actually sends the disposition notice. This interlocks with your bookkeeping process; the turnover agent only delivers the evidence package, never the decision.

Answer: Avery Moss, Accounts Payable, executes the security deposit disposition and sends the disposition notice. The turnover agent delivers the evidence package to deposits-ap@ridgeline.example and never makes the deduction decision.

D7. Who is the backup decision-maker when the property manager is unreachable and a scope or deadline clock is burning?

Hint: If there is no answer, that is the first thing to fix: a deadline with no available decision-maker is a company structure problem.

Answer: Morgan Vale, Maintenance Supervisor, is the backup when Ellis Shore is unreachable and a scope or deadline clock is burning.

### Group E: Platform and Wiring
E1. What is your turnover board of record?

Hint: A dedicated turnover product, a project board tool, or a spreadsheet configured from the shipped Turnover Tracking Board Full System Design. Pick one; a board of record that lives in two places is not a board of record.

Answer: The Ridgeline Turnover Board, a spreadsheet configured from the shipped Turnover Tracking Board Full System Design and stored in the company cloud drive. It is the single board of record; no second copy is maintained.

E2. What app or flow captures your inspections?

Hint: The tool used for pre-move-out, move-out, and final inspection capture: photos, checklist answers, and signatures.

Answer: SiteProof, a fictional mobile inspection app, captures pre-move-out, move-out, and final inspections including photos, checklist answers, and signatures.

E3. What system carries work orders for turnover work?

Hint: Your maintenance platform, your accounting system's work orders, or the board itself. Name where a make-ready line item becomes a dispatched job.

Answer: WorkTrail, the fictional maintenance platform, carries turnover work orders. Each make-ready line item becomes a dispatched WorkTrail job tagged to the turn. (CROSS-SEAT: WorkTrail as the platform of record is owned by the maintenance seat's D1 answer; this seat records that turnover work rides the same platform.)

E4. Where does your vendor roster live, and what is the per-trade list?

Hint: Include the dedicated vendor list for your toughest property class if you run one. If no roster exists yet, building it is a phase-zero task before the agent schedules anything.

Answer: The approved vendor roster lives with the maintenance seat and is owned there (its C5 answer): Alpine Pipeworks plumbing, Summit Airworks HVAC, Copperline Electric electrical, Hearthside Appliance appliances, Hightrail Restoration roofing and restoration. Make-ready trades added by this seat into that same roster: Trailhead Painting, Basin Floorworks flooring, Clearwater Clean turn cleaning, and Stonecut Landscaping. Turnover-owned annotation: the Class C tough-property list is Trailhead Painting and Clearwater Clean, who both accept short-notice Class C work.

E5. Which channel reaches your owners, and whose name do the owner emails go out under?

Hint: Portal or email, and confirm the sender identity for the owner communication templates while sends are human-released.

Answer: Owners are reached by email. (CROSS-SEAT: the owner channel is owned by the maintenance seat's D5 answer.) Turnover-owned: owner emails from this seat go out under Ellis Shore's name.

E6. Where are photos and documents stored, and under what naming convention?

Hint: Owner portal, cloud drive, or the inspection tool's storage. One convention, applied on every turn, so evidence is findable at dispute time.

Answer: The fictional secured document vault, one folder per unit per turn. Naming convention: UNIT-YYYYMMDD-STAGE-NN, for example PB-104-20260825-MOVEOUT-03, applied on every turn so evidence is findable at dispute time.

E7. What messaging bot or channel is provisioned for the turnover agent itself?

Hint: The channel your team uses to talk to the agent directly, for example a Telegram or Slack bot created at deploy time. Name who administers it.

Answer: Fictional Telegram bot RidgelineTurnoverBot, administered by Ellis Shore. The bot token and chat ID are deploy-time environment inputs, not questionnaire-to-file mapping values.

E8. Which channels carry escalations, and to whom?

Hint: Per person: channel and hours, for example the property manager by email during business hours and the owner-operator by instant message for urgent items at any time.

Answer: Ellis Shore, Portfolio Director: internal chat during business hours 08:00-18:00 America/Denver, SMS for anything with a burning clock at any hour. Morgan Vale, Maintenance Supervisor: internal chat 07:00-17:00 America/Denver. Avery Moss, Accounts Payable: email only, business hours, for deposit evidence deadlines.

### What Happens Next
Your answers do three things, in order:

- The board design gets your values. Configure the board described by the shipped Turnover Tracking Board Full System Design from your class map, turn-time targets, budget bands, punch-list deadlines, and reserve threshold. Your Group B and Group C answers are the source of truth for those board formulas and alerts.
- The agent starts in operator-supervised copilot mode. The operator reviews the board, every proposed update, and every draft while the team calibrates the configured workflow; the shipped edition does not run an automated digest or an automatic exit from this mode.
- Human release remains the shipped posture for every outbound message. Any future change to a message class requires a separate operator-and-owner decision and an implemented runtime policy. Make-ready scope and budget approval, security deposit deduction decisions, vendor pricing commitments, and tenant damage charge notices always end with a human.

Keep the answers current. When a threshold, a person, a vendor, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the turnover and make-ready coordinator agent specification and the ten turnover documents in this library. Nothing in this document is legal advice; confirm every state-law answer with your attorney.
