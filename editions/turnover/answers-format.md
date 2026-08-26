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

Company name: ________________________________________
Org short-name: ________________________________________
Forward email: ________________________________________
Timezone: ________________________________________

Day mode start: ________________________________________
Day mode end: ________________________________________
Inspection SLA hours: ________________________________________
Scope SLA hours: ________________________________________
Stale-stage alert days: ________________________________________

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

Answer: ________________________________________

A2. Is a pre-move-out inspection legally required or regulated in your state?

Hint: Some states require offering one or regulate its timing and notice. Confirm with counsel before adopting the pre-move-out walkthrough as a standard step.

Answer: ________________________________________

A3. What dispute window do you give residents on damage charges?

Hint: Recommended: 7 to 14 days for mid-tenancy charges; the statutory window applies at move-out. Your lease governs; confirm with counsel.

Answer: ________________________________________

A4. Does your state require certified mail for damage charge notices at move-out or for final notices before collections?

Hint: A counsel question. The answer controls how the highest-consequence notice templates are delivered.

Answer: ________________________________________

A5. Which sections of your standard lease cover damage responsibility, the wear-and-tear definition, cost recovery, and collections or attorney fees?

Hint: Every damage charge notice must cite a lease section. Build this list once from your standard lease before any notice is drafted.

Answer: ________________________________________

A6. Who does your lease assign lawn care and HVAC filter changes to?

Hint: This drives the damage-versus-wear call on two of the most common move-out findings. Read the answer from your lease form, not from memory.

Answer: ________________________________________

### Group B: Property Classes and Benchmarks
B1. Which property class is each of your units: A, B, C, or D?

Hint: Every benchmark, budget band, and status color keys off the class map. If no per-unit map exists, building it is a phase-zero task before the agent grades anything.

Answer: ________________________________________

B2. What are your turn-time targets per property class?

Hint: Lead the answer with `Default turn target days: NN`, then give the per-class targets and warning bands. Common working values: Class B 12 days, Class C 14 days, Class D 21 days.

Answer: ________________________________________

B3. What are your make-ready budget bands per class for a standard turn with no major damage?

Hint: Common working values: Class B $1,000, Class C $800, Class D $1,200 as the on-budget ceilings, with warning and over-budget bands above.

Answer: ________________________________________

B4. What are your punch-list completion deadlines per class?

Hint: Common working values: 24 hours for Class B and C, 48 hours for Class D.

Answer: ________________________________________

B5. What weights does your turnover grading scorecard use?

Hint: Common default: turn time 30, budget 25, inspection quality 20, owner communication 15, documentation 10. Adopt the framework as written unless you want different weights.

Answer: ________________________________________

B6. What is your turnover-rate baseline, and what door count of record does it divide by?

Hint: The monthly report header needs both numbers. Pick the door count source once and keep it consistent.

Answer: ________________________________________

### Group C: Scope and Owner-Approval Rules
C1. What is the pre-approved reserve threshold per owner?

Hint: Common default: $500 unless the management agreement says otherwise. This single number is the auto-approve line for the whole make-ready flow; list every per-owner override.

Answer: ________________________________________

C2. What is your scope-change ladder?

Hint: Common default: within the reserve, proceed; over by less than $500, call the owner plus an email confirmation within 2 hours; over by $500 or more, formal bid with a 24-hour owner approval window. A human executes the call step.

Answer: ________________________________________

C3. For safety items, is fix-first-notify-after pre-authorized, and up to what dollar cap?

Hint: Safety items: smoke and CO detectors, exposed wiring, gas smell, no heat or air conditioning in extreme weather. Name one cap number; above it, the on-call human is woken first.

Answer: ________________________________________

C4. When an owner is silent past the approval window on a scope request, who decides proceed-without-item versus hold?

Hint: Common default window: 24 hours. Name the decision-maker for the silent-owner call; the agent chases the response but never makes this decision.

Answer: ________________________________________

C5. When may a scope draft include suggested upgrades?

Hint: Common default: upgrades such as plank flooring over carpet in lower property classes are always presented as an owner option, never dispatched without approval.

Answer: ________________________________________

C6. What are your standing no-approval items on every turnover?

Hint: Common default list: rekey, deep clean, preventive pest treatment, and HVAC filter change on every turnover; never skipped, never asked.

Answer: ________________________________________

C7. At what security-deposit chargeback amount must the coordinator stop and get PM review before it goes on the disposition? Set a per-line-item number and a per-unit-total number.

Hint: This is distinct from the owner pre-approval threshold in C1. That threshold gates repair-spend authority; this one gates deposit-deduction authority, a different authority, so keep the two numbers labeled separately. The chargeback number is commonly set below the repair-approval line. Below both the per-line and the per-unit numbers, with documented evidence and no dispute anticipated, the coordinator proceeds; at or above either number, or on any dispute, missing documentation, or ambiguous wear-versus-damage, it goes to the PM before the disposition is drawn.

Answer: ________________________________________

### Group D: Roles and People
D1. Do you have in-house techs today, or are you vendor-only?

Hint: This determines the whole tech column of the dispatch decision matrix. If vendor-only, the matrix collapses to its vendor column and the on-site inspector question below becomes the first hire conversation.

Answer: ________________________________________

D2. Who conducts pre-move-out, move-out, and final inspections on-site?

Hint: Inspections need a person at the property within tight windows. Name the person or role per inspection type.

Answer: ________________________________________

D3. Who is the property manager of record for scope escalation and the damage charge notice gates?

Hint: This person approves scope escalations and releases every damage charge notice. Name them, and name anyone else authorized to approve turnover decisions.

Answer: ________________________________________

D4. Who is the photographer of record for listing photos, and what is their turnaround SLA?

Hint: The listing cannot launch without photos; the SLA keeps the final stage from stalling.

Answer: ________________________________________

D5. Who receives the leasing handoff when a unit goes rent-ready?

Hint: The last board stage hands the unit to the leasing pipeline. Name the person or team.

Answer: ________________________________________

D6. Who executes the security deposit disposition today?

Hint: The person who actually sends the disposition notice. This interlocks with your bookkeeping process; the turnover agent only delivers the evidence package, never the decision.

Answer: ________________________________________

D7. Who is the backup decision-maker when the property manager is unreachable and a scope or deadline clock is burning?

Hint: If there is no answer, that is the first thing to fix: a deadline with no available decision-maker is a company structure problem.

Answer: ________________________________________

### Group E: Platform and Wiring
E1. What is your turnover board of record?

Hint: A dedicated turnover product, a project board tool, or a spreadsheet configured from the shipped Turnover Tracking Board Full System Design. Pick one; a board of record that lives in two places is not a board of record.

Answer: ________________________________________

E2. What app or flow captures your inspections?

Hint: The tool used for pre-move-out, move-out, and final inspection capture: photos, checklist answers, and signatures.

Answer: ________________________________________

E3. What system carries work orders for turnover work?

Hint: Your maintenance platform, your accounting system's work orders, or the board itself. Name where a make-ready line item becomes a dispatched job.

Answer: ________________________________________

E4. Where does your vendor roster live, and what is the per-trade list?

Hint: Include the dedicated vendor list for your toughest property class if you run one. If no roster exists yet, building it is a phase-zero task before the agent schedules anything.

Answer: ________________________________________

E5. Which channel reaches your owners, and whose name do the owner emails go out under?

Hint: Portal or email, and confirm the sender identity for the owner communication templates while sends are human-released.

Answer: ________________________________________

E6. Where are photos and documents stored, and under what naming convention?

Hint: Owner portal, cloud drive, or the inspection tool's storage. One convention, applied on every turn, so evidence is findable at dispute time.

Answer: ________________________________________

E7. What messaging bot or channel is provisioned for the turnover agent itself?

Hint: The channel your team uses to talk to the agent directly, for example a Telegram or Slack bot created at deploy time. Name who administers it.

Answer: ________________________________________

E8. Which channels carry escalations, and to whom?

Hint: Per person: channel and hours, for example the property manager by email during business hours and the owner-operator by instant message for urgent items at any time.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The board design gets your values. Configure the board described by the shipped Turnover Tracking Board Full System Design from your class map, turn-time targets, budget bands, punch-list deadlines, and reserve threshold. Your Group B and Group C answers are the source of truth for those board formulas and alerts.
- The agent starts in operator-supervised copilot mode. The operator reviews the board, every proposed update, and every draft while the team calibrates the configured workflow; the shipped edition does not run an automated digest or an automatic exit from this mode.
- Human release remains the shipped posture for every outbound message. Any future change to a message class requires a separate operator-and-owner decision and an implemented runtime policy. Make-ready scope and budget approval, security deposit deduction decisions, vendor pricing commitments, and tenant damage charge notices always end with a human.

Keep the answers current. When a threshold, a person, a vendor, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Property Management Operations Library, generic baseline document. Derived from the turnover and make-ready coordinator agent specification and the turnover documents in this library. Nothing in this document is legal advice; confirm every state-law answer with your attorney.
