---
title: "BDM Agent Setup Questionnaire"
source: "Derived from the three BDM library docs: Owner-Acquisition Playbook, Pipeline Board, Judgment Guide (Dane, 2026-08-21)"
converted: 2026-08-21
google_doc_id: 1udeDaCwTxJq8bQkKm_hpe_1vN2iWH8iEy26LK_ImoSk
google_doc_url: https://docs.google.com/document/d/1udeDaCwTxJq8bQkKm_hpe_1vN2iWH8iEy26LK_ImoSk/edit
library_folder: 1-wBpk_TiPFqSPntxrHvXyQv6MLtFKdBC
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

# BDM Agent Setup Questionnaire

## BDM Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic business development (BDM) agent into your company's agent.

Companion documents in this folder: BDM Owner-Acquisition Playbook, BDM Pipeline Board, and BDM Judgment Guide (all Generic Baseline).

### What This Is and How To Use It
The BDM agent ships as a generic baseline: an owner-acquisition playbook, a pipeline board, and a judgment guide with hard escalation rules that work for any residential property management company. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every pipeline gate, every alert clock, and every script the agent uses reads from that file, and the generic documents themselves are never edited.

There are 42 questions in four groups: company, market, and legal; pricing, fees, and authority; people, escalation, and handoff; platform, cadence, and quoted standards. Most answers take a minute. A handful need your broker of record or your attorney; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law answer, every PMA term, and every fair housing question should be confirmed with your broker of record and your attorney before the agent relies on it.

### Group A: Company, Market, and Legal
A1. What is your current door count, and what is your monthly new-door growth target?

Hint: This picks your benchmark tier. Common targets: under 150 doors, 5 to 10 new doors a month; 150 to 400 doors, 10 to 20; 400 plus, 20 to 40 or more. A healthy pipeline always holds 3 to 5 times your monthly door goal in active opportunities.

Answer: ________________________________________

A2. Which states and markets do you operate in, and what is the county or tax record website used to verify ownership in each?

Hint: The states feed the board's State dropdown. Ownership is verified against public tax records before every PMA is sent; name the lookup site per market.

Answer: ________________________________________

A3. What is your service area boundary, and what is your minimum rent threshold?

Hint: Leads outside the area or below the minimum are declined gracefully and referred out; neither is taken without manager approval.

Answer: ________________________________________

A4. What property conditions and types do you accept, and at what percentage above market rent do you walk away?

Hint: Common default: a rent demand more than 20 percent above market escalates to the manager before any PMA is sent. Properties with code violations or habitability issues are never accepted without manager approval and a documented remediation plan.

Answer: ________________________________________

A5. Does your state require one PMA per unit or one per owner, and which ownership entity types do you accept on a PMA?

Hint: A broker-of-record and counsel question. The PMA must be executed by the entity on the tax record; a mismatch means re-execution before onboarding proceeds.

Answer: ________________________________________

A6. Who must sign the PMA on the company side, and what disclosures does your state require at signing?

Hint: Broker signature requirements, required disclosures at time of agreement, and fee disclosure rules all vary by state. Confirm with your broker and counsel.

Answer: ________________________________________

A7. What are your state's security deposit limits and handling rules?

Hint: This governs takeover deals: never accept liability for a deposit you did not collect and cannot verify. Confirm with counsel.

Answer: ________________________________________

A8. What fair housing confirmations apply in your markets, including any age or student restriction questions?

Hint: A counsel question. An owner who expresses preferences based on any protected class is declined, always; that rule is not configurable. The screening-criteria script depends on this answer.

Answer: ________________________________________

A9. What are your state's data retention requirements for real estate and sales records?

Hint: Common board defaults: won deals kept permanently, lost deals 12 months active then archived, duplicates 30 days then deleted. Confirm with counsel.

Answer: ________________________________________

### Group B: Pricing, Fees, and Authority
B1. What are your management package tier names and the monthly fee range from lowest to highest?

Hint: The pricing script presents three full-service packages from a low to a high monthly number; the tier names feed the board's Package dropdown.

Answer: ________________________________________

B2. What is your one-time setup fee?

Hint: Quoted in the pricing presentation and collected or invoiced at handoff.

Answer: ________________________________________

B3. What maintenance reserve do you hold per property?

Hint: Presented as "your money, not a fee" in the pricing script; collected or invoiced at handoff.

Answer: ________________________________________

B4. What does your top package cost, and which guarantee programs does it include?

Hint: The generic script cites eviction protection, damage coverage above the deposit, on-time owner payments, and a waived placement fee. List only programs you actually run.

Answer: ________________________________________

B5. What is your tenant placement or leasing fee, and do you have a documented leasing guarantee program?

Hint: A leasing guarantee is only ever quoted if it is a documented, approved program in that market. If none exists, the agent never references one.

Answer: ________________________________________

B6. What are your protection program terms and coverage caps, exactly as written?

Hint: The generic scripts use "up to $2,500 in damage beyond the deposit" as an example. Coverage is never overstated; owners get the written terms.

Answer: ________________________________________

B7. What is your pet policy: screening process, monthly pet fee and where it goes, and pet damage coverage amount?

Hint: The pet objection script quotes a formal pet screening, a monthly pet fee paid to the owner, and a damage coverage cap.

Answer: ________________________________________

B8. What do you charge to manage rehab or make-ready work?

Hint: Generic structure: a percentage on invoices under $3,000 and a flat fee above. Name your percentage and your flat fee.

Answer: ________________________________________

B9. What is your referral fee schedule, and do you require a signed referral agreement before paying?

Hint: Amount or percentage per referral type. Referral fees are never a verbal commitment, and an unpaid fee 7 days after a won deal fires an alert to accounting.

Answer: ________________________________________

B10. What is your maintenance authorization threshold: the amount above which owner approval is required?

Hint: Common default: $500. When an owner asks to lower it, the script explains the operational impact; it never goes below your company minimum without manager and legal approval.

Answer: ________________________________________

B11. What is your PMA termination notice period, and do you offer a satisfaction guarantee window?

Hint: The generic script pairs the notice requirement with a 90-day satisfaction guarantee. Never promise cancel-anytime; quote your actual clause.

Answer: ________________________________________

B12. Who can approve a fee deviation or a PMA modification, and what turnaround do you quote the owner while you escalate?

Hint: The BDM never discounts or modifies unilaterally: fees go to the manager, contract language to the broker of record. Common quoted turnaround: 24 to 48 hours. End the answer with the labeled lines the engine reads, one per line: `Quoted turnaround: ...`.

Answer: ________________________________________

### Group C: People, Escalation, and Handoff
C1. Who are the BDMs on your team?

Hint: Names feed the board's BDM Owner dropdown. In a small portfolio this may be the owner wearing the BDM hat; write that down too.

Answer: ________________________________________

C2. Who is the BDM's manager: the person every fee deviation, red-flag property, stalled deal, and walk-away decision escalates to?

Hint: Also the weekly pipeline review partner. Every escalation is logged in the CRM before the manager conversation, not after. End the answer with the labeled lines the engine reads, one per line: `BD manager: ...`.

Answer: ________________________________________

C3. Who is your broker of record?

Hint: Every PMA modification request goes through this person, and state law may require their signature on the PMA. No contract change is ever agreed at the table.

Answer: ________________________________________

C4. Who is your legal counsel for takeovers involving litigation or eviction, code violations, and fair housing questions?

Hint: Deals with pending eviction, active litigation, or unresolved violations require manager plus legal review before the PMA is executed.

Answer: ________________________________________

C5. Who is your onboarding specialist, and through what channel does the signed-PMA handoff reach them?

Hint: This person is named in the post-PMA email as the owner's new main point of contact; the onboarding call is scheduled within 48 hours of signing. End the answer with the labeled lines the engine reads, one per line: `Handoff channel: ...`.

Answer: ________________________________________

C6. Who coordinates property access after signing: your local market director or ops lead?

Hint: The post-PMA sequence tells the owner to expect this person's call within 48 hours.

Answer: ________________________________________

C7. Who on the accounting side pays referral fees when a deal is won?

Hint: The board flags referral fees owed at won; the flag has to land with a named person or seat.

Answer: ________________________________________

C8. Who receives brokerage and investment redirects: the leads that are not property management deals?

Hint: The board's REDIRECT lane needs a warm-handoff recipient per department. If you have no brokerage or investment arm, name the outside partner or write "none".

Answer: ________________________________________

C9. Which other property managers do you refer declined owners to?

Hint: The graceful decline script offers names for properties outside your model. Keep a short list current, even if it is empty today.

Answer: ________________________________________

### Group D: Platform, Cadence, and Quoted Standards
D1. What platform hosts your pipeline board?

Hint: The board is platform-agnostic: Google Sheets, Excel, Airtable, Notion, or a CRM all work. Name the system and where it lives. End the answer with the labeled lines the engine reads, one per line: `Board location: ...`.

Answer: ________________________________________

D2. Which lead sources are active for your company today, and what company-specific sources should be added to the board's dropdown?

Hint: Generic list: inbound web, FRBO active and stale, realtor, owner and vendor referrals, direct mail, social media, cold call, investor network, REI club. Healthy mid-size operations run 3 to 5 sources at once with referrals at 20 to 30 percent of leads.

Answer: ________________________________________

D3. Where does your Owner Intake Form live, and what is the link the post-PMA email sends?

Hint: Step 1 of the post-PMA email asks the owner to complete it within 24 hours; the BDM can also offer to complete it together on a call. End the answer with the labeled lines the engine reads, one per line: `Owner intake form link: ...`.

Answer: ________________________________________

D4. How is the PMA sent and signed, and who executes it on the company side?

Hint: Name the e-signature tool. The W-9 goes out attached to the PMA send, and an unsigned appointment means the PMA is sent the same business day. End the answer with the labeled lines the engine reads, one per line: `E-signature tool: ...`, `Company signer: ...`.

Answer: ________________________________________

D5. What are your contact-attempt and archive thresholds?

Hint: Common defaults: unresponsive after 6 attempts over 10 days; a lead is cold at 3 days without a touch; nurture is exhausted after 8 touches over 180 days. Also set your re-engagement window for lost leads. End the answer with the labeled lines the engine reads, one per line: `Max contact attempts: ...`, `Attempt window days: ...`, `Cold lead days: ...`, `Nurture exhausted touches: ...`, `Nurture exhausted window days: ...`, `Lost lead re-engagement days: ...`.

Answer: ________________________________________

D6. What are your stall and escalation clocks on an unsigned PMA and on stage age?

Hint: Common defaults: red alert at 48 hours unsigned, manager escalation at 5 days; stage maximums of 3, 5, 3, 7, and 1 days for stages S0 through S4. Also pick the days-in-stage number your weekly review flags. End the answer with the labeled lines the engine reads, one per line: `Unsigned alert hours: ...`, `Unsigned escalate days: ...`, `Stage max days S0: ...`, `Stage max days S1: ...`, `Stage max days S2: ...`, `Stage max days S3: ...`, `Stage max days S4: ...`, `Days in stage review flag: ...`.

Answer: ________________________________________

D7. What are your weekly activity goals, and what is your daily outbound call floor?

Hint: The weekly metrics table needs your numbers: new leads, discovery calls, appointments held, PMAs signed, doors added, outbound calls, follow-up touches. Suggested daily floor: 10 to 20 outbound prospecting calls. End the answer with the labeled lines the engine reads, one per line: `Weekly new leads: ...`, `Weekly discovery calls: ...`, `Weekly appointments held: ...`, `Weekly agreements signed: ...`, `Weekly doors added: ...`, `Weekly outbound calls: ...`, `Weekly follow-up touches: ...`, `Daily outbound call floor: ...`.

Answer: ________________________________________

D8. What is your monthly door goal, and what is your target for average days from lead to close?

Hint: The pipeline-below-minimum alert fires when active pipeline doors fall under 3 times the monthly goal. Benchmark: unsigned-PMA stage averages under 3 days on won deals. End the answer with the labeled lines the engine reads, one per line: `Monthly door goal: ...`, `Target days lead to close: ...`.

Answer: ________________________________________

D9. When is your weekly pipeline review, who attends, and who receives the monthly leadership report?

Hint: Common cadence: 30 to 45 minutes weekly with the BDM and manager or owner; the monthly report carries leads by source, conversion by stage, doors added, lost reasons, and new MRR.

Answer: ________________________________________

D10. What leasing and marketing facts can your BDM truthfully quote: typical days to lease, screening points, marketing reach, leasing line coverage?

Hint: The generic scripts cite a 14-point screening process, marketing on 90 plus websites, and a 24/7 leasing line. Quote only what is true for your company; a specific days-to-lease number is quoted as typical, never guaranteed.

Answer: ________________________________________

D11. What is your inspection schedule, exactly as quoted to owners?

Hint: Generic example: move-in, 60 days, 10 months, move-out. Inspections are described as a strong baseline, never a guarantee that nothing will be missed.

Answer: ________________________________________

D12. What is your standard owner communication model, your non-emergency response SLA, and the typical eviction timeline range in your market?

Hint: Generic defaults: a defined update cadence plus 24/7 portal access, and response within one business day on non-emergencies. The eviction range is quoted as typical for the market, never as a promise; confirm the range with counsel.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The pipeline board gets your values. The BDM Pipeline Board's LOOKUP TABLES tab and its alert clocks read straight from your answers: BDM names, states, lead sources, package tiers, referral fee schedule, attempt and touch thresholds, and the monthly door goal behind the pipeline-below-minimum alert. Every fill-in marker on the board's master list maps to a question above.
- The agent boots in shadow mode. For about the first week the agent runs its daily pipeline checks silently and sends a calibration digest to the people you named in Group C. Nothing outbound, no actions. Shadow mode ends when a week of digests matches reality.
- Autonomy widens by consequence. Pipeline tracking, CRM hygiene, and alert monitoring run autonomously from day one. Every outbound message to an owner starts as a human-released draft, then message classes graduate to autonomous send one class at a time as they prove clean, lowest consequence first. Three gates never graduate at any setting: fee or contract deviations (manager and broker only), anything on the Never-Promise List, and the decision to decline or walk away from an owner. Those always end with a human.

Keep the answers current. When a fee, a person, a threshold, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the three BDM documents in this folder: the Owner-Acquisition Playbook, the Pipeline Board, and the Judgment Guide. Nothing in this document is legal advice; confirm every state-law, PMA, and fair housing answer with your broker of record and your attorney.
