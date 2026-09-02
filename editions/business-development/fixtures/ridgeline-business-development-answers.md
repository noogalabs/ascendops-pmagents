---
title: "BDM Agent Setup Questionnaire"
source: "Derived from the three BDM library docs: Owner-Acquisition Playbook, Pipeline Board, Judgment Guide (owner-reviewed, 2026-08-21)"
converted: 2026-08-21
google_doc_id: 1udeDaCwTxJq8bQkKm_hpe_1vN2iWH8iEy26LK_ImoSk
google_doc_url: https://docs.google.com/document/d/1udeDaCwTxJq8bQkKm_hpe_1vN2iWH8iEy26LK_ImoSk/edit
library_folder: 1-wBpk_TiPFqSPntxrHvXyQv6MLtFKdBC
audience: all agents
status: reference
---

# Configuration Cover Sheet

Company name: Ridgeline Residential Management
Org short-name: ridgeline
Forward email: bd@ridgeline.example
Timezone: America/Denver
Autonomy mode: [documented] copilot
Unlock window: [documented] last_10
Qualifying accuracy: [documented] null
Resident messaging autonomy: [documented] no

Cover-sheet field notes, because this seat spends them differently from its siblings:
Company name is the only one of the four that has a template placeholder in this seat.
Timezone has no placeholder here and reaches `config.json` as a config key instead (K1 in the
mapping table) - a cover-sheet field does not need a placeholder to be load-bearing, it needs a
destination. Forward email has no placeholder, no config key, and no consumer at all: this seat
has no email-forwarding intake path, because leads arrive through the board platform (D1) and the
configured lead sources (D2). It is carried here for install coherence and is marked unspent.

Seat-specific fifth field (leasing `{{prospect_sla_minutes}}` precedent):

Owner speed-to-lead window: 30

This value lands in structured config and renders into the playbook and pipeline board. The
configured value is the authority; reviewed companion prose no longer hardcodes five minutes.

Pointer-seeded values, NOT cover-sheet fields: day-mode start/end are maintenance-owned peer
values. They remain absent until the maintenance seat registers; boot surfaces then read them
from the structured config. No local Business Development answer substitutes for that authority
(leasing X2 precedent).

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

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

Answer: 186 doors under management today across the two fictional markets, with a monthly
  new-door growth target of 8. That lands Ridgeline in the 150-to-400 benchmark tier.
  (CROSS-SEAT: the door count of record is owned by the turnover seat's B6 answer; this seat
  records the profile that selects the benchmark tier and points there for the grain.
  DUPLICATE-QUESTION: D8 asks this same monthly door goal - one number, 8, written once. If a
  company answers the two differently, carry both and flag it; never average and never take the
  later question.)

A2. Which states and markets do you operate in, and what is the county or tax record website used to verify ownership in each?

Hint: The states feed the board's State dropdown. Ownership is verified against public tax records before every PMA is sent; name the lookup site per market.

Answer: One fictional state, Basin. Two markets. Pine Basin: ownership verified at the fictional
  Pine Basin County Assessor portal, assessor.pinebasin.example. Cedar Mesa: the fictional Cedar
  Mesa County records portal, records.cedarmesa.example. Both markets have a lookup site, so the
  ownership-verification lane runs for both. A market added later without one is a lane that
  cannot run - it gets flagged, and it never gets pointed at the other market's site.

A3. What is your service area boundary, and what is your minimum rent threshold?

Hint: Leads outside the area or below the minimum are declined gracefully and referred out; neither is taken without manager approval.

Answer: Service area: within 30 miles of the Pine Basin and Cedar Mesa metro cores, both inside
  Basin state. Minimum rent threshold: $1,050 a month. Anything outside the boundary or under
  the minimum is declined gracefully and referred out, and neither is ever taken without Rhea
  Calder's approval.

A4. What property conditions and types do you accept, and at what percentage above market rent do you walk away?

Hint: Common default: a rent demand more than 20 percent above market escalates to the manager before any PMA is sent. Properties with code violations or habitability issues are never accepted without manager approval and a documented remediation plan.

Answer: Accepted types: single-family, townhome, duplex through fourplex, and small multifamily
  up to 12 units. Accepted conditions: rent-ready, or with a documented remediation plan and a
  date on it. Walk-away at more than 20 percent above the rent the analysis supports - above
  that margin it is a manager call before any agreement is sent. Code violations or habitability
  issues are never accepted without Rhea Calder's approval and a written remediation plan
  attached; a verbal assurance is not a plan.

A5. Does your state require one PMA per unit or one per owner, and which ownership entity types do you accept on a PMA?

Hint: A broker-of-record and counsel question. The PMA must be executed by the entity on the tax record; a mismatch means re-execution before onboarding proceeds.

Answer: CONFIRMED with counsel. Basin state requires one agreement per owner entity with a unit
  schedule attached, not one per unit. Accepted ownership entity types: individual, married
  couple, revocable trust, LLC, and limited partnership. The agreement must be executed by the
  entity on the tax record; a mismatch means re-execution before onboarding proceeds.

A6. Who must sign the PMA on the company side, and what disclosures does your state require at signing?

Hint: Broker signature requirements, required disclosures at time of agreement, and fee disclosure rules all vary by state. Confirm with your broker and counsel.

Answer: CONFIRMED with counsel. Sloane Karr, Principal Broker, signs every management agreement
  on the company side. Required at signing in Basin state: the agency disclosure and the written
  fee disclosure schedule, both delivered before signature rather than after.
  (DUPLICATE-QUESTION: D4 asks who executes on the company side - same person, Sloane Karr,
  written once. A difference between the two answers is surfaced, never averaged and never
  silently picked.)

A7. What are your state's security deposit limits and handling rules?

Hint: This governs takeover deals: never accept liability for a deposit you did not collect and cannot verify. Confirm with counsel.

Answer: CROSS-SEAT POINTER, not a second copy: the deposit disposition deadline and handling
  rules are owned by the maintenance seat's A3 answer - 30 calendar days from lease termination
  - and are recorded here as a pointer. Basin state caps a residential security deposit at one
  and a half months' rent and requires it held in a separate trust account. BD-owned rule on top
  of the pointer, because this is a takeover question no other seat asks: Ridgeline never
  accepts liability for a deposit it did not collect and cannot verify. A takeover requires a
  deposit ledger and a bank verification in hand before the agreement is executed; without both,
  the deposit line is excluded in writing and Harlan Voss reviews it.

A8. What fair housing confirmations apply in your markets, including any age or student restriction questions?

Hint: A counsel question. An owner who expresses preferences based on any protected class is declined, always; that rule is not configurable. The screening-criteria script depends on this answer.

Answer: CONFIRMED with counsel (Harlan Voss). Federal protected classes apply in both markets,
  and Basin state adds source of income - which is why the leasing seat accepts housing vouchers
  portfolio-wide in Pine Basin. No age-restricted and no student-restricted communities anywhere
  in the portfolio, so there is no age or student restriction question to answer for any
  property. The one rule with no approver and no configuration: an owner who expresses a
  preference about who lives in the property based on any protected class is declined, always,
  and the exact words are logged and routed to Harlan Voss and Rhea Calder the same day. An
  answer here can only narrow the screening-criteria script; nothing in this file can unlock a
  preference.

A9. What are your state's data retention requirements for real estate and sales records?

Hint: Common board defaults: won deals kept permanently, lost deals 12 months active then archived, duplicates 30 days then deleted. Confirm with counsel.

Answer: UNCONFIRMED - PENDING COUNSEL. Harlan Voss has not yet confirmed Basin state's statutory
  retention period for real estate and sales records. The board defaults are carried as a
  starting point and are explicitly marked unconfirmed: won deals kept permanently, lost deals
  12 months active then archived, duplicates 30 days then deleted. Because the legal answer is
  unconfirmed, the archive-and-delete automation is NOT LIVE - nothing is deleted or purged on a
  clock until Harlan Voss confirms the period. The defaults sit in the config as a starting
  point, not as permission.

### Group B: Pricing, Fees, and Authority
B1. What are your management package tier names and the monthly fee range from lowest to highest?

Hint: The pricing script presents three full-service packages from a low to a high monthly number; the tier names feed the board's Package dropdown.

Answer: Three full-service tiers. Essential at 8 percent of collected rent with a floor of $110
  a month per door; Standard at 10 percent; Full Service at 12 percent. The tier names feed the
  board's Package dropdown.

B2. What is your one-time setup fee?

Hint: Quoted in the pricing presentation and collected or invoiced at handoff.

Answer: $295 one-time per management agreement, quoted in the pricing presentation and invoiced
  at handoff.

B3. What maintenance reserve do you hold per property?

Hint: Presented as "your money, not a fee" in the pricing script; collected or invoiced at handoff.

Answer: $500 held per property as a maintenance reserve, presented as the owner's money rather
  than a fee. NOTE ON GRAIN, because two other seats hold a reserve number and it is not this
  number: this one is PER PROPERTY. The pm-assist seat's B5 and the bookkeeping seat's B3 hold
  an owner reserve floor measured PER UNIT, at $400. On a fourplex those produce different
  totals and neither is wrong; they are different keys and must not be compared as if they were
  one. NOTE ON THE VALUE: $500 also appears as the turnover seat's C1 base make-ready reserve
  and as the pm-assist seat's B14 broker trust-variance threshold. Three gates, one number,
  deliberate - if a configurator collapses any two of them, that is the failure this fixture is
  built to make visible.

B4. What does your top package cost, and which guarantee programs does it include?

Hint: The generic script cites eviction protection, damage coverage above the deposit, on-time owner payments, and a waived placement fee. List only programs you actually run.

Answer: Full Service at 12 percent is the top package. It includes exactly two guarantee
  programs, because those are the two Ridgeline actually runs: eviction protection, and on-time
  owner payments by the 12th of the month. It does NOT include damage coverage above the deposit
  and it does NOT include a waived placement fee - the generic script cites both, Ridgeline runs
  neither, and the agent never references a program that is not on this list.

B5. What is your tenant placement or leasing fee, and do you have a documented leasing guarantee program?

Hint: A leasing guarantee is only ever quoted if it is a documented, approved program in that market. If none exists, the agent never references one.

Answer: Tenant placement fee: 50 percent of one month's rent, Class B and Class C alike, charged
  when a tenant takes possession. Leasing guarantee: NO documented program in either market.
  Because no approved program exists, the agent never references a leasing guarantee at any
  stage, in any market, to any owner - not as a maybe, not as something we usually do. Absent
  here is a mute, not an unset value waiting for a default to be filled in.

B6. What are your protection program terms and coverage caps, exactly as written?

Hint: The generic scripts use "up to $2,500 in damage beyond the deposit" as an example. Coverage is never overstated; owners get the written terms.

Answer: Eviction protection, exactly as written in the agreement: 'Ridgeline will cover up to
  $1,500 in filing fees and attorney costs for the eviction of a Ridgeline-placed tenant during
  the first twelve months of tenancy, one claim per tenancy, provided screening was run to
  Ridgeline's published criteria for that property class.' That is the whole program and that is
  the sentence that gets quoted, word for word. The generic script's example of $2,500 in damage
  coverage beyond the deposit is NOT a Ridgeline program and is never referenced. Coverage is
  never paraphrased upward, and every owner gets the written terms.

B7. What is your pet policy: screening process, monthly pet fee and where it goes, and pet damage coverage amount?

Hint: The pet objection script quotes a formal pet screening, a monthly pet fee paid to the owner, and a damage coverage cap.

Answer: Pets are allowed at all Ridgeline-managed properties. Screening: every pet goes through
  a formal profile on the fictional PetCheck service before approval, with the assistance-animal
  path handled separately under fair housing. Fees: a $300 non-refundable pet fee per pet, plus
  $35 a month in pet rent paid through to the owner. CROSS-SEAT: the $300 fee is owned by the
  leasing seat, which administers it to the tenant - this seat quotes it to the owner and holds
  a pointer, not a second number. Pet damage coverage: NONE. Ridgeline runs no pet damage
  program, so the agent may not quote a coverage amount; the honest line is that pet damage is
  handled through the deposit and the standard damage process.

B8. What do you charge to manage rehab or make-ready work?

Hint: Generic structure: a percentage on invoices under $3,000 and a flat fee above. Name your percentage and your flat fee.

Answer: 10 percent of the invoice on rehab and make-ready work under $3,000, and a flat $350
  above it. NOTE: the $3,000 boundary between the two is not something this questionnaire asks -
  it comes from the playbook's generic structure and is carried as a literal. Ridgeline is
  accepting it as written; a company that wanted a different boundary would have nowhere to say
  so today.

B9. What is your referral fee schedule, and do you require a signed referral agreement before paying?

Hint: Amount or percentage per referral type. Referral fees are never a verbal commitment, and an unpaid fee 7 days after a won deal fires an alert to accounting.

Answer: Owner referral that signs an agreement: $250. Multi-property owner referral of three or
  more doors: $500. Vendor referrals: no fee. A signed referral agreement is required before any
  fee is paid, always - a referral fee is never a verbal commitment and no exception is
  available at any level. An unpaid fee 7 days after a deal is won fires an alert to Avery Moss.
  NOTE: the $500 tier is the fourth distinct gate in this fixture carrying that number; see B3.

B10. What is your maintenance authorization threshold: the amount above which owner approval is required?

Hint: Common default: $500. When an owner asks to lower it, the script explains the operational impact; it never goes below your company minimum without manager and legal approval.

Answer: $450 is the maintenance authorization threshold - the amount above which owner approval
  is required. CROSS-SEAT, AND IT IS GENUINELY THE SAME NUMBER: this is the threshold the
  maintenance seat enforces at its B1 base answer, which is also $450. What we quote an owner at
  the sale is what maintenance runs afterwards; if the two ever differ, the owner was mis-sold,
  and that is an error rather than a per-seat policy difference. Company minimum: $300. That is
  a floor on negotiation - the number the threshold never goes below without Rhea Calder and
  Harlan Voss both approving - and it is NOT an operating threshold. Two numbers in one answer
  that pattern-match and mean different things: do not collapse them. NOTE: $300 also appears as
  the maintenance seat's Northstar Homes owner override, as the pm-assist seat's Northstar
  override, and as the pm-assist seat's coordinator spend authority. Four gates, one number,
  none of them the same thing.

B11. What is your PMA termination notice period, and do you offer a satisfaction guarantee window?

Hint: The generic script pairs the notice requirement with a 90-day satisfaction guarantee. Never promise cancel-anytime; quote your actual clause.

Answer: 30 days written notice from either party, available after the first 90 days of the
  agreement. Satisfaction guarantee: a 90-day window - if Ridgeline has not placed a tenant or
  the owner is not satisfied inside the first 90 days, the agreement terminates with no
  termination fee. That is the actual clause and it is what gets quoted. Never cancel-anytime;
  the notice requirement is real and it is always stated together with the guarantee, not
  instead of it.

B12. Who can approve a fee deviation or a PMA modification, and what turnaround do you quote the owner while you escalate?

Hint: The BDM never discounts or modifies unilaterally: fees go to the manager, contract language to the broker of record. Common quoted turnaround: 24 to 48 hours.

Answer: Fee deviations, discounts, waivers, and price matches: Rhea Calder, BD manager.
  Management-agreement language, any clause, any threshold: Sloane Karr, broker of record.
  Nothing is agreed at the table in either case. Quoted turnaround while the escalation is open:
  by end of the next business day. NOTE: the approver half of this question is already answered
  by C2 and C3 - only the turnaround is new here, and an answer naming a third approver would be
  an inconsistency to surface, not a third route.

### Group C: People, Escalation, and Handoff
C1. Who are the BDMs on your team?

Hint: Names feed the board's BDM Owner dropdown. In a small portfolio this may be the owner wearing the BDM hat; write that down too.

Answer: Two BDMs. Nika Ansell covers Pine Basin; Bram Teller covers Cedar Mesa. Both names feed
  the board's BDM Owner dropdown.

C2. Who is the BDM's manager: the person every fee deviation, red-flag property, stalled deal, and walk-away decision escalates to?

Hint: Also the weekly pipeline review partner. Every escalation is logged in the CRM before the manager conversation, not after.

Answer: Rhea Calder, Business Development Manager. Every fee deviation, red-flag property,
  stalled deal, and walk-away decision escalates to her, and she is the weekly pipeline review
  partner. Every escalation is logged before the conversation, not after. CROSS-SEAT: Rhea
  Calder is deliberately NOT the property manager of record - that seat is held by different
  people in different lanes (Dana Wren for leasing and PM assist, Ellis Shore for turnover and
  accounting, Morgan Vale for maintenance). Six seats, four distinct names, and that is the
  correct state for a per-seat routing question. Cross-check on difference; never unify them.

C3. Who is your broker of record?

Hint: Every PMA modification request goes through this person, and state law may require their signature on the PMA. No contract change is ever agreed at the table.

Answer: Sloane Karr, Principal Broker and company owner. Every agreement modification request
  goes through her, and Basin state requires her signature on the agreement. CROSS-SEAT NOTE:
  this should be one person company-wide, so a difference between seats here is an error rather
  than a policy choice. The pm-assist seat's A3 names Sloane Karr and matches. The accounting
  seat's C2 names a different principal broker; that contradiction is surfaced here rather than
  resolved, because neither of those fixtures is this pass's to edit.

C4. Who is your legal counsel for takeovers involving litigation or eviction, code violations, and fair housing questions?

Hint: Deals with pending eviction, active litigation, or unresolved violations require manager plus legal review before the PMA is executed.

Answer: Harlan Voss of Voss Legal Group. Takeovers involving litigation or eviction, code
  violations, and fair housing questions all go to him. CROSS-SEAT SPLIT: the pm-assist seat
  splits this into two people - Tobin Merritt of Merritt and Cole LLP for eviction filings, and
  Harlan Voss for counsel. This question asks one name and covers a wider set, so the answer
  maps to the counsel arm; the eviction attorney stays owned by pm-assist with no counterpart
  here. Any deal with a pending eviction, active litigation, or an unresolved violation requires
  Rhea Calder plus Harlan Voss before the agreement is executed.

C5. Who is your onboarding specialist, and through what channel does the signed-PMA handoff reach them?

Hint: This person is named in the post-PMA email as the owner's new main point of contact; the onboarding call is scheduled within 48 hours of signing.

Answer: Tam Ruiz, Owner Onboarding Specialist. The signed-agreement handoff reaches her on the
  Ridgeline owner-onboarding chat channel, with the executed agreement auto-filed to the owner
  record in WorkTrail. She is named in the post-agreement email as the owner's new main point of
  contact, and the onboarding call is scheduled within 48 hours of signing.

C6. Who coordinates property access after signing: your local market director or ops lead?

Hint: The post-PMA sequence tells the owner to expect this person's call within 48 hours.

Answer: Morgan Vale, Maintenance Supervisor, coordinates property access after signing. The
  post-agreement sequence tells the owner to expect her call within 48 hours. NOTE: this is a
  commitment made on another seat's behalf - Morgan Vale is the maintenance seat's C1 person,
  and the 48-hour promise is quoted by this seat and delivered by hers.

C7. Who on the accounting side pays referral fees when a deal is won?

Hint: The board flags referral fees owed at won; the flag has to land with a named person or seat.

Answer: Avery Moss, Accounts Payable, pays referral fees when a deal is won. The board's
  referral-fee-owed flag at won lands on her by name. CROSS-SEAT: the same person the
  maintenance seat names at C7, the turnover seat at D6, and the bookkeeping seat at C3 - one
  name across four seats, and it matches. This seat names who the flag lands on; the accounting
  seat names the desk that executes the payment. Same person here, and they must agree.

C8. Who receives brokerage and investment redirects: the leads that are not property management deals?

Hint: The board's REDIRECT lane needs a warm-handoff recipient per department. If you have no brokerage or investment arm, name the outside partner or write "none".

Answer: Brokerage redirects: Ridgeline has no brokerage arm, so they go to the outside partner
  Basin Ridge Realty as a warm handoff, with the owner told who they are being introduced to and
  why. Investment redirects: none - Ridgeline has no investment arm and no partner for it, so
  those leads are declined gracefully with the standard script rather than routed. NOTE: 'none'
  is a routed answer here, not an empty one. An empty value would be an unrouted lane, and the
  REDIRECT lane would drop leads quietly.

C9. Which other property managers do you refer declined owners to?

Hint: The graceful decline script offers names for properties outside your model. Keep a short list current, even if it is empty today.

Answer: Two, both fictional: Cedar Ridge Property Group for properties outside the service area,
  and Foothill Rentals LLC for properties under the rent minimum. The graceful decline script
  offers these names. If this list ever empties, the referral sentence is muted rather than
  filled with a guess - the agent never invents a partner just to have someone to name.

### Group D: Platform, Cadence, and Quoted Standards
D1. What platform hosts your pipeline board?

Hint: The board is platform-agnostic: Google Sheets, Excel, Airtable, Notion, or a CRM all work. Name the system and where it lives.

Answer: A spreadsheet workbook bootstrapped from the BDM Pipeline Board Template, living in the
  Ridgeline shared drive under the BD folder. CROSS-SEAT: this is deliberately NOT the property
  management platform. WorkTrail remains the platform of record for the portfolio, owned by the
  maintenance seat's D1 answer, and this seat holds a pointer to it. A BD pipeline board being a
  different system from the PM software is normal rather than a discrepancy: this answer records
  which platform carries this seat's work and claims nothing about the inventory.

D2. Which lead sources are active for your company today, and what company-specific sources should be added to the board's dropdown?

Hint: Generic list: inbound web, FRBO active and stale, realtor, owner and vendor referrals, direct mail, social media, cold call, investor network, REI club. Healthy mid-size operations run 3 to 5 sources at once with referrals at 20 to 30 percent of leads.

Answer: Active today, five sources: inbound web, owner referrals, realtor referrals, FRBO active
  listings, and vendor referrals. Referrals run about 25 percent of leads. Company-specific
  sources to add to the board dropdown: Basin Ridge Realty partner referrals, and Ridgeline
  resident-to-owner conversions - a tenant who buys and keeps us on. No purchased lists and no
  scraped lists; every source is confirmed compliant before the first touch. CROSS-SEAT WARNING:
  the leasing seat's D5 is also a lead-source inventory and it is a DIFFERENT population -
  theirs is where tenant rental inquiries land (WorkTrail guest cards, the leasing shared inbox,
  the leasing phone line). Same words, disjoint populations, disjoint destinations. Neither list
  is the other's default, and a configurator that writes one into the other's key has failed.

D3. Where does your Owner Intake Form live, and what is the link the post-PMA email sends?

Hint: Step 1 of the post-PMA email asks the owner to complete it within 24 hours; the BDM can also offer to complete it together on a call.

Answer: The Owner Intake Form lives on the fictional FormBasin service. The link the
  post-agreement email sends is https://forms.ridgeline.example/owner-intake. Step 1 of that
  email asks the owner to complete it within 24 hours, and the BDM offers to fill it out
  together on a call for owners who would rather do it that way.

D4. How is the PMA sent and signed, and who executes it on the company side?

Hint: Name the e-signature tool. The W-9 goes out attached to the PMA send, and an unsigned appointment means the PMA is sent the same business day.

Answer: The agreement is sent and signed through InkPath, and the W-9 goes out attached to the
  send. Sloane Karr, Principal Broker, executes on the company side. An unsigned appointment
  means the agreement goes out the same business day, not the next morning. CROSS-SEAT: InkPath
  is the same e-signature tool the leasing seat uses for executed leases - one tool company-wide
  is the expected shape, and a difference would be a finding. DUPLICATE-QUESTION: A6 already
  asked who signs on the company side; same person, written once.

D5. What are your contact-attempt and archive thresholds?

Hint: Common defaults: unresponsive after 6 attempts over 10 days; a lead is cold at 3 days without a touch; nurture is exhausted after 8 touches over 180 days. Also set your re-engagement window for lost leads.

Answer: Unresponsive after 6 attempts over 10 days, then archived. A lead is cold at 3 days with
  no touch. Nurture is exhausted after 8 touches over 180 days. Re-engagement window for lost
  leads: 90 days before a lost lead can be worked again. CROSS-SEAT WARNING: the leasing seat
  runs clocks that look like these and are not - a 48-hour approval hold, a 3-business-day
  missing-items window - but their subject is a tenant applicant and this seat's is a property
  owner. Different populations, similar shapes. Do not collapse them.

D6. What are your stall and escalation clocks on an unsigned PMA and on stage age?

Hint: Common defaults: red alert at 48 hours unsigned, manager escalation at 5 days; stage maximums of 3, 5, 3, 7, and 1 days for stages S0 through S4. Also pick the days-in-stage number your weekly review flags.

Answer: Unsigned agreement: red alert at 48 hours, escalation to Rhea Calder at 5 days. Stage
  maximums: S0 3 days, S1 5 days, S2 3 days, S3 7 days, S4 1 day. Days-in-stage the weekly
  review flags: 10. NOTE: this question asks S0 through S4 only. S5 and S6 have specs in the
  board document but nothing here asks for their numbers, so they stay unset rather than being
  filled from the board's example. An unset stage maximum is a gate that does not fire, which is
  honest; a guessed one is a gate that fires at a number nobody chose.

D7. What are your weekly activity goals, and what is your daily outbound call floor?

Hint: The weekly metrics table needs your numbers: new leads, discovery calls, appointments held, PMAs signed, doors added, outbound calls, follow-up touches. Suggested daily floor: 10 to 20 outbound prospecting calls.

Answer: Weekly: 20 new leads, 12 discovery calls, 6 appointments held, 3 agreements signed, 8
  doors added, 75 outbound calls, 40 follow-up touches. Daily outbound call floor: 15.

D8. What is your monthly door goal, and what is your target for average days from lead to close?

Hint: The pipeline-below-minimum alert fires when active pipeline doors fall under 3 times the monthly goal. Benchmark: unsigned-PMA stage averages under 3 days on won deals.

Answer: Monthly door goal: 8. Target average days from lead to close: 21. DUPLICATE-QUESTION: A1
  already asked the monthly new-door growth target and the answer is the same 8. One number,
  written once - if a company answers these two differently, carry both and flag the
  disagreement rather than picking the later one.

D9. When is your weekly pipeline review, who attends, and who receives the monthly leadership report?

Hint: Common cadence: 30 to 45 minutes weekly with the BDM and manager or owner; the monthly report carries leads by source, conversion by stage, doors added, lost reasons, and new MRR.

Answer: Weekly pipeline review Tuesdays at 09:00 America/Denver, 45 minutes, attended by Rhea
  Calder, Nika Ansell, and Bram Teller. The monthly leadership report goes to Ellis Shore,
  Portfolio Director, and Sloane Karr, Principal Broker. NOTE: the seat ships a
  weekly-review-prep job seeded at Monday 08:00. This answer is Tuesday 09:00, and there is no
  step in onboarding that re-points the job - so the prose and the job disagree unless the
  install fixes it by hand.

D10. What leasing and marketing facts can your BDM truthfully quote: typical days to lease, screening points, marketing reach, leasing line coverage?

Hint: The generic scripts cite a 14-point screening process, marketing on 90 plus websites, and a 24/7 leasing line. Quote only what is true for your company; a specific days-to-lease number is quoted as typical, never guaranteed.

Answer: Days to lease: NOTHING TO QUOTE. Ridgeline has no days-to-lease figure it would stand
  behind. The leasing seat tracks screening criteria, hold windows, and notice periods, and
  holds no typical-days-to-lease number anywhere in its configuration. The agent leaves this
  empty and says so out loud rather than reaching for the generic example. Screening: NO POINT
  COUNT. Ridgeline runs documented written screening criteria per property class, not a scored
  point process, so there is no number to quote and the generic 14-point figure describes a
  process we do not run. Marketing reach: 3 syndication sites - the fictional RentBasin,
  HomeSeeker, and ListingHub, syndicated automatically from WorkTrail. CROSS-SEAT AND EXACT:
  that is precisely the leasing seat's syndication set. The generic script says 90 plus
  websites; quoting that here would be quoting 30 times the reach the company actually delivers,
  which is a promise operations cannot keep rather than a configuration difference. Leasing line
  coverage: business hours, Monday through Saturday, 09:00 to 18:00 America/Denver, matching the
  leasing seat's showing hours. Not 24/7, and the agent never says 24/7.

D11. What is your inspection schedule, exactly as quoted to owners?

Hint: Generic example: move-in, 60 days, 10 months, move-out. Inspections are described as a strong baseline, never a guarantee that nothing will be missed.

Answer: Quoted to owners as: move-in, 60 days after move-in, 10 months, and move-out. FLAG,
  DELIBERATE: two of those four inspections have no operational owner anywhere in the portfolio
  today. The maintenance seat runs no periodic mid-tenancy inspection, and the turnover seat
  runs only an optional pre-move-out walkthrough one to two weeks before move-out. So move-in
  and move-out are delivered; the 60-day and the 10-month inspections are quoted and delivered
  by nobody. This is the sharpest form of a quoted-standard failure - not a number that differs
  from the delivering seat, but a promise with no delivering seat at all - and it sits in this
  fixture on purpose, so a checker that treats a missing counterpart as 'nothing to compare' can
  be caught reporting clean. Inspections are always described as a strong baseline, never as a
  guarantee that nothing gets missed.

D12. What is your standard owner communication model, your non-emergency response SLA, and the typical eviction timeline range in your market?

Hint: Generic defaults: a defined update cadence plus 24/7 portal access, and response within one business day on non-emergencies. The eviction range is quoted as typical for the market, never as a promise; confirm the range with counsel.

Answer: Owner communication model: a monthly owner statement plus 24/7 owner portal access in
  WorkTrail, and a call from the BDM at 30 days and at 90 days after onboarding. Non-emergency
  response SLA: acknowledged the same business day. NOTE ON MEASURE, because this one is easy to
  compare wrongly: the maintenance seat holds completion windows, not acknowledgement windows -
  routine work completes in 8 days and urgent in 36 hours at its B5 answer. Acknowledgement and
  completion are different measures, and comparing them as if they were one manufactures a
  mismatch that is not real. Eviction timeline range: UNANSWERED PENDING COUNSEL. Harlan Voss
  has not confirmed a typical range for Basin state, so there is no range to quote - the agent
  says it has no number it would stand behind and comes back with one, rather than quoting the
  market rumour. Empty here is a claim we may not make, not a gap to fill.

### What Happens Next
Your answers do three things, in order:

- The pipeline board gets your values. The BDM Pipeline Board's LOOKUP TABLES tab and its alert clocks read straight from your answers: BDM names, states, lead sources, package tiers, referral fee schedule, attempt and touch thresholds, and the monthly door goal behind the pipeline-below-minimum alert. Every fill-in marker on the board's master list maps to a question above.
- The agent boots in shadow mode. For about the first week the agent runs its daily pipeline checks silently and sends a calibration digest to the people you named in Group C. Nothing outbound, no actions. Shadow mode ends when a week of digests matches reality.
- Autonomy widens by consequence. Pipeline tracking, CRM hygiene, and alert monitoring run autonomously from day one. Every outbound message to an owner starts as a human-released draft, then message classes graduate to autonomous send one class at a time as they prove clean, lowest consequence first. Three gates never graduate at any setting: fee or contract deviations (manager and broker only), anything on the Never-Promise List, and the decision to decline or walk away from an owner. Those always end with a human.

Keep the answers current. When a fee, a person, a threshold, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the three BDM documents in this folder: the Owner-Acquisition Playbook, the Pipeline Board, and the Judgment Guide. Nothing in this document is legal advice; confirm every state-law, PMA, and fair housing answer with your broker of record and your attorney.
