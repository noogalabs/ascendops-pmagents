---
title: "Property Manager Agent Setup Questionnaire"
source: "Derived from the three Property Manager library docs: The Property Manager Seat, The PM Operating Board, PM Judgment and Lookup Guide (owner-reviewed, 2026-08-21)"
converted: 2026-08-21
google_doc_id: 1_f9dSxe25gCDe60nI-sz8E7t9DGUbfRJDq0pF_8xWRQ
google_doc_url: https://docs.google.com/document/d/1_f9dSxe25gCDe60nI-sz8E7t9DGUbfRJDq0pF_8xWRQ/edit
library_folder: 1bb7G3scG9jk34vq6wndsRBc_QwM9BQ0c
audience: all agents
status: reference
---

# Configuration Cover Sheet

Company name: Ridgeline Residential Management
Org short-name: ridgeline
Forward email: pm@ridgeline.example
Timezone: America/Denver

Pointer-seeded values, NOT cover-sheet fields: the external-communications window
({{day_mode_start}} / {{day_mode_end}}) is seeded from the org `context.json` and owned by
the maintenance seat's B8 answer. It is recorded here as a pointer so the member confirms it,
and it is deliberately not minted as a fifth cover-sheet field (leasing X2 precedent).

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.


# Property Manager Agent Setup Questionnaire

## Property Manager Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic PM-seat assistant agent into your company's agent.

Companion documents in this folder: The Property Manager Seat, The PM Operating Board, and the PM Judgment and Lookup Guide.

### What This Is and How To Use It
The Property Manager is a hired human seat: the judgment hub of the portfolio, accountable for owners, tenants, vendors, and every board underneath. The agent this questionnaire configures is not that seat. It is the PM's assistant: it owns the execution lane the seat documents carve out (pulling reports, updating boards, drafting from templates, tracking clocks, filing the decision log) and it never owns a judgment call. The three companion documents ship as a generic baseline that works for any residential property management company; nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the assistant's configuration file; every flag, every clock, and every board the assistant runs reads from that file, and the generic documents themselves are never edited.

There are 41 questions in four groups: company, portfolio, and state rules; thresholds, KPI targets, and clocks; delegation and people; platform and wiring. Most answers take a minute. A handful need your attorney, your broker of record, or a pass through your management agreements; those are marked in the hint under the question, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass.

---
Where a question offers a common default, the default is a starting point, not legal advice. Every state-law answer should be confirmed with your attorney and broker of record before the assistant relies on it. And one line never moves regardless of your answers: the assistant owns execution, the PM owns judgment, and the broker-only decisions in the PM Judgment and Lookup Guide stay above both.

### Group A: Company, Portfolio, and State Rules
A1. What is your portfolio size, which markets do you operate in, and what property classes do you manage?

Hint: The PM seat documents are written for any company size; portfolio scale and class mix set the load on every board and the weight of each KPI target in Group B.

Answer: 186 residential doors in the fictional Pine Basin and Cedar Mesa markets: 112 Class B and 74
  Class C, apartments and townhomes. No Class A and no Class D. Both markets are managed from one
  office. (CROSS-SEAT: the door count of record is owned by the turnover seat's B6 answer and the
  per-unit class map by its B1 answer; this seat records the portfolio profile that weights the
  Group B KPI targets and points at those for the grain.)

A2. Who holds the Property Manager seat, and which coordinator lanes exist in your company: leasing, maintenance, turnover, bookkeeping?

Hint: The assistant assists a hired human PM; it never replaces the seat. Name the PM, and for any lane with no coordinator, name who covers that board so the assistant knows where each lane flag routes.

Answer: Dana Wren, Property Manager, holds the seat. Coordinator lanes: LEASING - Wren Calloway, Leasing
  Coordinator. MAINTENANCE - Morgan Vale, Maintenance Supervisor. TURNOVER - no dedicated
  coordinator; Morgan Vale covers the make-ready board day to day and Ellis Shore, Portfolio
  Director, holds turnover scope escalation. BOOKKEEPING - Avery Moss, Accounts Payable, covers
  the money board. Lane flags route to the named person for that lane, never to the PM by default.

A3. Who is the principal broker or company owner, and on what channel do broker-only escalations travel?

Hint: Twelve decision classes never sit with the PM: Fair Housing responses, trust account variances, management agreement terminations, staff discipline, fee concessions, and the rest of the broker-only table in the PM Judgment and Lookup Guide. Pick a channel that gets read the same day.

Answer: Sloane Karr, Principal Broker and company owner. Broker-only escalations travel by SMS to Sloane
  Karr, with the same item mirrored into the Ridgeline broker escalation chat channel for the
  record. Same-day read is a requirement of the channel, not a hope.

A4. Who is your eviction attorney, and who is your property or general counsel?

Hint: The eviction attorney handles filings and pre-filing reviews; any legal demand letter or attorney contact goes to the broker and counsel the same day it arrives.

Answer: Eviction attorney: Tobin Merritt of the fictional firm Merritt and Cole LLP, who handles filings
  and pre-filing reviews. Property and general counsel: Harlan Voss of the fictional Voss Legal
  Group. Any legal demand letter or attorney contact goes to Sloane Karr and Harlan Voss the same
  day it arrives.

A5. What are your state's late-rent and eviction notice rules: what day does the late notice go out, what notice type and cure period applies, and what must happen before a filing?

Hint: Common working default: late notice on day 1 or 2 per the lease, then Pay-or-Quit per your state's notice requirements. State law governs; confirm with counsel.

Answer: Late notice goes out on day 2 per the lease in both markets. Pine Basin: Pay-or-Quit with a
  5-day cure period. Cedar Mesa: Pay-or-Quit with a 7-day cure period. Before any filing: proof of
  service of the notice, a current resident ledger, and a certified-mail record for the notice.
  CONFIRMED-WITH-COUNSEL=true for both fictional jurisdictions (Harlan Voss, this fictional
  scenario).

A6. What notice does your state require for non-renewal, and what notice for entry?

Hint: Both carry a state-set clock. The renewal pipeline and the compliance calendar read these values. Confirm with counsel.

Answer: Non-renewal notice: 60 days in Pine Basin, 30 days in Cedar Mesa. Entry notice: 24 hours in Pine
  Basin, 48 hours in Cedar Mesa. CONFIRMED-WITH-COUNSEL=true for both. (CROSS-SEAT: the entry-
  notice-per-jurisdiction map is owned by the maintenance seat's A2 answer; this seat carries the
  same two values as a pointer record so the renewal pipeline and the compliance calendar can read
  them, and a difference between the two seats is a contradiction to surface, never an average.)

A7. How must security deposits be held in your state, and what is the disposition deadline after move-out?

Hint: Deposits are trust funds: never spent early, disbursed only after the tenancy ends and within the state deadline. Many states use 30 days; confirm with counsel.

Answer: Security deposits are held in a separate deposit trust account at the fictional Basin State
  Bank, never commingled with operating funds, and the resident is told in writing at signing
  where the deposit is held. Disposition deadline: 30 calendar days after the tenancy ends.
  (CROSS-SEAT: the 30-day deadline VALUE is owned by the maintenance seat's A3 answer today,
  SEAM-1; this seat holds a pointer, not a second number. The bookkeeping questionnaire's A6 asks
  the same deadline plus the date that starts the clock, so ownership migrates to the bookkeeper
  seat when that seat ships - the accounting mapping pass owns that ruling, not this one.)

A8. What are the habitability standards in your state, and what response timeframes do they set?

Hint: A heating failure in winter is the canonical trigger. Common working default: a written owner deadline of 24 to 48 hours on a habitability approval, and PM emergency repair authority when the owner is unreachable. Confirm with counsel.

Answer: Habitability triggers, matching the maintenance seat's A8 list: no heat below 55F, no hot water,
  active sewage backup, uncontrolled interior water, exposed energized wiring, or an unsecured
  exterior opening. Owner deadline on a habitability approval: 24 hours. When the owner is
  unreachable after documented attempts across 2 hours, Dana Wren holds emergency repair authority
  and logs every contact attempt. CONFIRMED-WITH-COUNSEL=true.

A9. What inspection cadence do your state law and your management agreement set for routine and mid-lease inspections, and how long must tenant files be retained?

Hint: Retention is typically 3 to 7 years. Pre-move-out inspections are scheduled 1 to 2 weeks before move-out; move-in inspections are completed and uploaded on or before move-in day.

Answer: Move-in inspections are completed and uploaded on or before move-in day. Mid-lease inspection
  once per lease year. Pre-move-out inspections are scheduled 10 days before move-out. (CROSS-
  SEAT: whether a pre-move-out inspection is legally required and who conducts each inspection
  type are owned by the turnover seat's A2 and D2 answers; this seat carries only the cadence for
  the compliance calendar.) Tenant files are retained 7 years after the tenancy ends.

A10. What state-required landlord filings, registrations, or inspection deadlines belong on your compliance calendar?

Hint: These fill the compliance rows on the Month-End Pack and the compliance alert rules. Anything with a government deadline goes here.

Answer: Pine Basin: annual rental registration per property, due March 31, plus a smoke and CO detector
  certification at every turn. CONFIRMED-WITH-COUNSEL=true. Cedar Mesa: confirm with counsel - the
  registration requirement and its deadline are UNCONFIRMED today. The Cedar Mesa compliance lane
  is therefore NOT LIVE: no Cedar Mesa filing clock runs and the compliance calendar says so
  plainly rather than defaulting to the Pine Basin dates.

### Group B: Thresholds, KPI Targets, and Clocks
B1. What is your owner pre-approval spend threshold, and which owners have a different number in their management agreement?

Hint: The cost above which a repair needs written owner approval before work proceeds. List every per-owner override; the Approval Queue and the maintenance alert rules read this value.

Answer: $450 base owner pre-approval threshold. Fictional owner overrides: Juniper Holdings $700;
  Northstar Homes $300. NOTE: these are the same numbers the maintenance seat carries for
  occupied-unit repair spend, and they are deliberately NOT the same as the turnover seat's make-
  ready reserve numbers ($500 base, Juniper $750, Northstar $350). Two different authorities that
  happen to share owners - a cross-check surfaces the pair, it never unifies them.

B2. What is the coordinator spend authority: the repair cost above which a work order escalates to the PM?

Hint: Common working default: $300. Anything above it lands in the Approval Queue for a PM decision.

Answer: $300. A work order above $300 escalates to Dana Wren for a decision before it proceeds. NOTE for
  whoever configures this: $300 is also Northstar Homes' owner pre-approval override in B1. Same
  number, different gate - the B2 number is the coordinator-to-PM escalation line and applies to
  every property; the B1 number is one owner's contract threshold. A configurator that pattern-
  matches on the value would grant the wrong authority portfolio-wide.

B3. What is the PM's emergency spend authority when the owner is unreachable, and at what cost does even an emergency loop in the broker?

Hint: On a genuine habitability emergency the PM authorizes the repair, documents every contact attempt, and never waits more than 2 to 4 hours for an owner callback. Common extraordinary threshold: above $5,000 the broker is looped in even for an emergency.

Answer: $1,200 PM emergency spend authority when the owner is unreachable on a genuine habitability
  emergency, matching the maintenance seat's after-hours emergency cap. Every contact attempt is
  documented and the owner callback is never waited on longer than 2 hours. Above $5,000 Sloane
  Karr is looped in even on an emergency, and the loop-in is a notification with a decision
  attached, not a request for permission to keep someone safe.

B4. What is your owner non-response ladder on approval requests?

Hint: Common defaults: follow-up call or text at 24 hours, second follow-up with documented attempts at 48, PM decides if urgent at 72 and logs it in the decision log, and non-urgent items at 72 hours escalate to the broker and get flagged in the owner file.

Answer: 24 hours: follow-up call or text, logged. 48 hours: second follow-up with every attempt
  documented in the owner file. 72 hours: if the item is urgent Dana Wren decides and files it in
  the decision log; if it is not urgent it escalates to Sloane Karr and is flagged in the owner
  file as a responsiveness pattern. No rung is skipped because the next one is close.

B5. What is your minimum owner reserve per unit?

Hint: Typical range: $300 to $500 per unit. The financial alert fires when an owner falls below it; the reserve conversation itself always belongs to the PM.

Answer: $400 per unit. The financial alert fires when an owner's balance falls below $400 per unit; the
  reserve conversation itself is always Dana Wren's, never a templated note.

B6. What are your delinquency clocks: the day the late notice goes out, the day an account with no payment and no contact alerts the PM, and your portfolio delinquency target?

Hint: Common defaults: late notice on day 1 or 2, PM alert at day 3 to 5 with nothing logged, and a portfolio target under 2 percent of rent roll; above 2 percent alerts the PM and the broker.

Answer: Late notice on day 2. An account with no payment and no contact logged alerts Dana Wren on day
  5. Portfolio delinquency target is under 2 percent of rent roll; above 2 percent alerts Dana
  Wren and Sloane Karr together.

B7. What are your targets for days vacant and days to make-ready?

Hint: Both are fill-ins on the KPI scorecard: days vacant is usually set to your market average; days to make-ready is your company standard.

Answer: Days vacant target: 21 days, set to the fictional Pine Basin and Cedar Mesa market average. Days
  to make-ready target: 12 days. (CROSS-SEAT: the turnover seat's B-group owns the per-class grain
  - Class B 12 days, Class C 14 days from possession to rent-ready. 12 is the portfolio default
  because Class B is the modal class by door count. This seat carries the portfolio scalar and
  points at turnover for the class split.)

B8. Do the standard KPI benchmarks hold for your company, or do any get overridden?

Hint: Standard set: occupancy 95 percent or higher, work order close rate 90 percent within SLA, renewal rate 60 to 70 percent or higher, owner retention 90 percent annually, and no more than 20 to 25 percent of leases expiring in any one month. Write only the overrides.

Answer: One override: renewal rate target is 68 percent, not the standard 60 to 70 band's low end,
  because Ridgeline's Class B stock renews well in this fictional scenario. Everything else holds
  at the standard set: occupancy 95 percent or higher, work order close rate 90 percent within
  SLA, owner retention 90 percent annually, no more than 25 percent of leases expiring in any one
  month.

B9. What are your renewal clocks: the pipeline look-ahead window, the owner decision window, and the tenant follow-up schedule?

Hint: Common defaults: pipeline pulled at 90 to 120 days out, owner decision within 7 to 10 days of the recommendation, tenant follow-ups at 30 and 60 days, and a flag on any lease inside 90 days with no action started.

Answer: Renewal pipeline is pulled at 105 days out. Owner decision window: 7 days from the
  recommendation. Tenant follow-ups at 30 and 60 days. Any lease inside 90 days with no action
  started is flagged on the Daily Pulse. (CROSS-SEAT: the leasing seat carries its own renewal
  offer lead of 60 days and a 10-day tenant response window; those are the leasing execution
  clocks and they sit inside this pipeline window rather than competing with it.)

B10. What are your leasing alert thresholds: days to list after move-out, days on market with no showings, days with showings but no application, and the vacancy age that escalates to the PM?

Hint: Common defaults: listing live within 2 days of move-out, price review at 7 days with no showings, price decision at 14 days with showings but no application, escalation at 21 days with no application, and an application decision within 48 hours.

Answer: Listing live within 2 days of move-out. Price review at 7 days with no showings. Price decision
  at 14 days with showings but no application. Escalation to Dana Wren at 21 days with no
  application. Application decision within 24 business hours. (CROSS-SEAT: the 24-business-hour
  application decision SLA is owned by the leasing seat's configuration; this seat carries it as
  the alert threshold it watches, not as a second standard.)

B11. How many days past the target make-ready date does a turnover escalate, and what happens when scope exceeds the approved budget?

Hint: Common default: 3 days past target escalates. Any scope beyond the approved turnover budget is a PM approval, and above the owner threshold it goes to the owner.

Answer: 3 days past the target make-ready date escalates to Dana Wren. Any scope beyond the approved
  turnover budget is a Dana Wren approval; if the overage crosses that property's owner threshold
  from B1 it goes to the owner before the work proceeds. (CROSS-SEAT: the turnover seat owns the
  escalation mechanics on its own board; this seat owns the escalation landing on the PM board.)

B12. What maintenance SLA windows does the PM board hold vendors and coordinators to, and how long may an invoice sit unapproved?

Hint: Common defaults: Emergency assigned within 2 hours and resolved same day, Urgent within 24 to 48 hours, Routine within 7 to 10 days, and invoices flagged after 5 days in queue. If you run the maintenance agent, use the same values as its configuration.

Answer: Emergency assigned within 90 minutes and resolved within 4 hours. Urgent within 36 hours.
  Routine within 8 days. An invoice may sit unapproved for 5 days before it is flagged. The first
  three values are taken from the maintenance seat's configuration exactly, as this question's own
  hint instructs; if the maintenance seat's numbers ever differ from these, that is an unresolved
  flag for Dana Wren, never an average of the two. The 5-day invoice-queue limit has no
  maintenance counterpart and is owned here.

B13. At what project cost do you require multiple bids?

Hint: The seat standard is 2 to 3 bids for larger projects; name the dollar line where that kicks in.

Answer: $2,500. At or above $2,500 in project cost, 2 to 3 bids are required before the recommendation
  reaches Dana Wren or the owner.

B14. What is your trust account variance rule: how long does the bookkeeper get to resolve an unexplained variance, and what dollar size goes straight up?

Hint: Common defaults: 24 to 48 hours to resolve, and above $500 the broker is notified regardless. Any deposit-account variance, or any suspicion beyond error, goes up immediately; state trust law may require notifying the real estate commission, which is the broker's call.

Answer: Avery Moss has 24 hours to resolve an unexplained variance. Above $500 Sloane Karr is notified
  regardless of whether it is explained. Any deposit-trust-account variance, and any variance
  where the explanation is something other than an error, goes up immediately. Whether state trust
  law requires notifying the real estate commission is Sloane Karr's call, not this seat's and not
  the bookkeeper's. NOTE: $500 here is a variance-escalation line and is not the turnover seat's
  $500 make-ready reserve base, which is a different authority that happens to carry the same
  number.

### Group C: Delegation and People
C1. Go through the 20-row Assistant Can Own table in The Property Manager Seat, Part 7: which rows does your company delegate to the assistant on day one, which later, and which never?

Hint: The rows cover pulling reports, drafting owner updates, scheduling, board updates, status tracking, sending renewal offers once terms are set, logging decisions, formatting inspection reports, drafting approval requests, deadline tracking, KPI dashboards, invoice logging, reserve flagging, turnover scheduling, vendor list upkeep, memo drafting, and tenant follow-ups. Mark each row: now, later, or never.

Answer: Marking the 17 rows named in the hint; the remaining 3 rows of the Part 7 table are marked on
  the copy filed with the operating board workbook.
  NOW: pulling reports; board updates; status tracking; logging decisions once Dana Wren has made
  them; deadline tracking; KPI dashboards; invoice logging; reserve flagging; formatting
  inspection reports.
  LATER: drafting owner updates; scheduling; drafting approval requests; turnover scheduling;
  vendor list upkeep; memo drafting; tenant follow-ups.
  NEVER: sending renewal offers, even after terms are set - Ridgeline keeps the send with Dana
  Wren in this fictional scenario.
  Every row above is the EXECUTION half only. The judgment half of each row stays with Dana Wren
  at every setting, and no combination of "now" rows adds up to authority over a housing, money,
  legal, or relationship matter.

C2. Which drafted communications, if any, may the assistant send without PM review?

Hint: Default: every draft is PM-reviewed before it sends. The templated all-clear owner update is the usual first graduate. Anything with judgment or framing in it is always reviewed, personalized, and sent by the PM.

Answer: None at go-live. Every drafted communication is reviewed and released by Dana Wren. The
  templated all-clear owner update is the intended first graduate, and it graduates only when Dana
  Wren says so explicitly, after shadow mode has ended and a clean tracked record exists - not on
  a date, not on a score, and not as part of this setup. This answer records intent; it does not
  unlock anything.

C3. Where is the line on owner contact: what may the assistant send to owners directly, and what must always carry the PM's review?

Hint: The seat rule: statements and templated updates can be prepped and sent by the assistant; any owner who responds with a concern goes to the PM, and a difficult month is always framed by the PM, never by a template.

Answer: Once the class is graduated, the assistant may prep and send owner statements and the templated
  all-clear update, unchanged, on schedule. Everything else carries Dana Wren's review: any owner
  who responds with a concern goes straight to her, a difficult month is framed by her and never
  by a template, and any owner question touching rates, renewals, concessions, or money movement
  is hers by definition.

C4. How are your owners tagged by communication style, and where does that tag live?

Hint: Silent investor, collaborative, or high-touch, with a preferred contact method per owner. The Owner Snapshot and the report pack tone both read this tag.

Answer: Three tags: silent investor, collaborative, high touch, each with a preferred contact method.
  The tag lives on the Owner Snapshot tab of the Ridgeline PM Operating Board and is mirrored to
  the owner record in WorkTrail so the two never drift silently. Fictional examples: Juniper
  Holdings - silent investor, email only. Northstar Homes - high touch, phone first with an email
  summary after.

C5. Who is the backup decision-maker when the PM is unreachable and an SLA or legal clock is burning?

Hint: The default path is up: the broker or company owner. If there is no answer, that is the first thing to fix before the assistant goes live; a deadline with no available decision-maker is a company structure problem.

Answer: Ellis Shore, Portfolio Director, is the backup when Dana Wren is unreachable and an SLA or legal
  clock is burning. If Ellis Shore is also unreachable, the path goes up to Sloane Karr. (CROSS-
  SEAT: the maintenance seat names Ellis Shore for the same role and the turnover seat names
  Morgan Vale for its own; per-seat ownership is intentional and a difference between them is
  surfaced for eyeball, never auto-unified.)

C6. Who works the financial board day to day: who pulls reports, posts payments, generates statements, and flags anomalies?

Hint: Bookkeeper, assistant, or both. The PM reviews and signs off before statements go to owners; money itself always moves on the money side.

Answer: Avery Moss, Accounts Payable, works the financial board day to day: pulls reports, posts
  payments, generates statements, and flags anomalies. Dana Wren reviews and signs off before any
  statement goes to an owner. Money itself only ever moves on the money side - this seat surfaces,
  drafts, and tracks, and authorizes nothing. (CROSS-SEAT: the bookkeeping questionnaire's C3 asks
  who executes the human bookkeeper role; if the accounting seat names someone other than Avery
  Moss for this fictional company, that is a fixture-merge conflict for the QA seat, not a defect
  in either table.)

C7. What is the PM's check-in cadence with the broker?

Hint: The seat recommends a weekly check-in, with legal escalations, owner relationship risk, and compliance questions going up as they arise, not held for the meeting.

Answer: Weekly, Thursday, 30 minutes with Sloane Karr. Legal escalations, owner-relationship risk, and
  compliance questions go up the same day they arise and are never held for the meeting; the
  meeting is for pattern and portfolio, not for anything with a clock on it.

C8. How do the PM's decisions reach the assistant for the decision log, and when does the assistant sweep the Follow-Through Log?

Hint: Seat defaults: the PM dictates or notes the decision and the assistant formats and files it; the assistant reviews the Follow-Through Log every Monday morning and flags anything due that week; a promise overdue by 24 hours flags red and moves to the top of the Daily Pulse.

Answer: Dana Wren dictates or notes the decision - in the Ridgeline PM chat channel, or as a note on the
  Approval Queue row - and the assistant formats and files it in the decision log with the date,
  the item, the options presented, the decision, and who made it. The Follow-Through Log is swept
  every Monday morning and anything due that week is flagged. A promise overdue by 24 hours flags
  red and moves to the top of the Daily Pulse.

### Group D: Platform and Wiring
D1. What property management platform and what accounting system do you run?

Hint: The PM documents are platform-agnostic; every board, tag, and alert has to be wired to a real system. Name both, and note whether they are the same product.

Answer: WorkTrail is the fictional property management platform of record; LedgerPeak is the fictional
  accounting system. They are not the same product, and the two do not reconcile automatically.
  (CROSS-SEAT: the platform inventory is owned by the maintenance seat's D1 answer; this seat
  records which platform carries its own work and that the money board rides LedgerPeak.)

D2. Where will the PM Operating Board workbook live, and which of its nine tabs go live on day one?

Hint: The board is designed spreadsheet-first: one workbook, nine tabs (Daily Pulse, Monday Board, Month-End Pack, Approval Queue, Escalation Triage, Owner Snapshot, Owner Report Pack, Alert Rules, Follow-Through Log). Some tabs may map to native platform views instead; say which.

Answer: A Google Sheets workbook, "Ridgeline PM Operating Board", in the fictional Ridgeline Operations
  shared drive. Live on day one: Daily Pulse, Approval Queue, Escalation Triage, Follow-Through
  Log, Alert Rules. Later, after shadow mode ends: Monday Board, Month-End Pack, Owner Snapshot,
  Owner Report Pack. No tab maps to a native WorkTrail view in this fictional scenario; WorkTrail
  is a source, not the board.

D3. Where does each lane board live (maintenance, leasing, turnover, bookkeeping, decision log), and how does the operating board pull from them?

Hint: Coordinators update the lane boards; the PM Operating Board pulls from them and never replaces them. Note whether each pull is a linked sheet, an export, or a manual update, and who does it.

Answer: MAINTENANCE - Ridgeline Maintenance Board, a linked sheet fed from WorkTrail saved views,
  refreshed by Morgan Vale. LEASING - Ridgeline Leasing Board spreadsheet, linked sheet, kept by
  Wren Calloway. TURNOVER - Ridgeline Turnover Board spreadsheet, manual weekly export by Ellis
  Shore. BOOKKEEPING - LedgerPeak reports, manual pull by Avery Moss. DECISION LOG - a tab in the
  operating board workbook, mirrored to the WorkTrail owner record. The operating board pulls from
  all five and replaces none of them; every pulled row carries its source and its pull time.

D4. Which alert rules fire automatically in your platform, and which are manual coordinator flags into Escalation Triage?

Hint: The Alert Rules tab lists thresholds across maintenance, leasing, delinquency, financial, and compliance. Anything your software cannot auto-flag becomes a named person's manual duty; an alert with no owner does not exist.

Answer: Automatic in WorkTrail: work order SLA breach, invoice aging past 5 days in queue, and vacancy
  age. Manual coordinator flags into Escalation Triage, each with a named owner: delinquency day-5
  no-contact - Avery Moss. Owner non-response ladder rungs - surfaced by the assistant, owned by
  Dana Wren. Make-ready 3 days past target - Morgan Vale. Trust variance - Avery Moss. Compliance
  deadlines - Dana Wren, and the Cedar Mesa half of that row is NOT LIVE pending the A10 counsel
  answer, which is stated on the tab rather than left blank.

D5. Which channels reach each audience: owners, tenants, coordinators, vendors, and the broker?

Hint: Portal, email, phone, text, chat, per audience. Owner preference is per-owner and lives in the Owner Snapshot; broker-only escalations use the channel named in A3.

Answer: OWNERS - email, with per-owner preference recorded in the Owner Snapshot. TENANTS - resident
  portal plus SMS for scheduling and status; formal legal notices by email and certified mail
  only, and only after Dana Wren releases them. COORDINATORS - Ridgeline internal chat. VENDORS -
  portal plus email, owned by the maintenance seat's D4 answer and not re-specified here. BROKER -
  SMS to Sloane Karr with a mirror into the broker escalation channel, same day, per A3.

D6. By what day of the month does the owner report pack go out, on which channels, and do high-touch owners get a follow-up call?

Hint: Common defaults: portal plus email by day 15, owner draws around day 10, and the financial review signed off on days 8 to 12 before anything sends. The all-clear version goes out even when nothing happened.

Answer: Day 15, on the resident-owner portal plus email. High-touch owners get a follow-up call from
  Dana Wren, never from the assistant. Owner draws go out around day 10. The financial review is
  signed off between day 8 and day 12 and nothing sends before that sign-off. The all-clear
  version goes out on day 15 even in a month where nothing happened.

D7. Where do the durable records live: the decision log, owner files, tenant files, proof of notice service, and the compliance calendar?

Hint: The judgment guide requires owner communication saved in the portal or PM software, not just email. Every scenario ends with a write-it-down step; name the one place those entries land.

Answer: DECISION LOG - the decision-log tab of the Ridgeline PM Operating Board workbook, mirrored to
  the WorkTrail owner record so owner communication is saved in the PM software and not only in
  email. OWNER FILES and TENANT FILES - WorkTrail. PROOF OF NOTICE SERVICE - the WorkTrail unit
  document folder, with the certified-mail record attached to the same entry. COMPLIANCE CALENDAR
  - a tab on the operating board workbook. Every scenario's write-it-down step lands in the
  decision-log tab.

D8. Where do your attorney-reviewed notice templates live, and who owns keeping them current?

Hint: The PM maintains the templates and flags when they need updating; the assistant can track review dates once a home and an owner are named.

Answer: The attorney-reviewed notice template library lives in the Notice Templates folder of the
  Ridgeline Operations shared drive, reviewed by Merritt and Cole. Dana Wren owns keeping them
  current. The assistant tracks review dates and flags a template that has gone stale; it never
  edits one and never drafts outside the library.

D9. What is your CMA source for renewal pricing, and who runs it?

Hint: The renewal recommendation memo is drafted from CMA data; name the tool or data source and whether the PM runs the CMA or reviews one pulled by the assistant.

Answer: WorkTrail comparables plus the fictional RentBasin market report. Wren Calloway pulls the CMA;
  Dana Wren reviews it and sets the rate. The renewal recommendation memo is drafted by the
  assistant with the rate line left blank for Dana Wren to fill.

### What Happens Next
Your answers do three things, in order:

- The operating board gets your values. The PM Operating Board is built from your Group B and Group D answers: every population rule on the Daily Pulse, every aging flag on the Approval Queue, and every threshold on the Alert Rules tab reads from this configuration, and the generic documents themselves are never edited.
- The assistant boots in shadow mode. For about the first week the assistant reads the lane boards silently and sends a daily calibration digest to the PM: what it would have flagged, filed, and drafted. Nothing outbound, no board writes. Shadow mode ends when a week of digests matches reality.
- Delegation widens row by row. The rows you marked "now" in C1 go live first; every outbound draft is PM-released until its message class proves clean; rows marked "later" graduate one at a time, lowest consequence first. The golden rule never graduates at any setting: if it requires a relationship, a risk assessment, a legal judgment, or an unhappy conversation, it stays with the PM; and the broker-only decisions stay with the broker.

Keep the answers current. When a threshold, a person, an owner, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the three Property Manager library documents: The Property Manager Seat, The PM Operating Board, and the PM Judgment and Lookup Guide. Nothing in this document is legal advice; confirm every state-law answer with your attorney and broker of record.

