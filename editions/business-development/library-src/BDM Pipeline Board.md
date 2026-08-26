---
title: "BDM Pipeline Board (Generic Baseline)"
source: "Owner-reviewed generic operating library"
converted: 2026-08-21
audience: all agents
status: reference
---

# BDM Pipeline Board (Generic Baseline)

## BDM Pipeline Board (Generic Baseline)
Source: Owner-reviewed generic operating library (verify with your broker and counsel). Generic baseline; companion to the BDM Owner-Acquisition Playbook.
Property Management | Spreadsheet-First | Platform-Agnostic
---
How to use this document: Every table below maps directly to a tab or view in your spreadsheet (Google Sheets, Excel, Airtable, Notion, or any CRM). Fill-in markers are written as [FILL: description]. Legal markers are written as [LEGAL: note].
### Part 1: The Master Pipeline Sheet
Tab Name: PIPELINE - ACTIVE
This is the single source of truth. Every active deal lives here. One row = one deal (one owner + one property address). If an owner has three properties, they get three rows.
#### 1A: Complete Column Schema
Every column below includes: Column Name | Data Type | Allowed Values / Format | Notes
#### Block A: Record Identification
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| A1 | Deal ID | Auto-number | PM-0001, PM-0002… | Auto-generate; never edit manually |
| A2 | Date Lead Created | Date | MM/DD/YYYY | Date first entered into pipeline |
| A3 | BDM Owner | Dropdown | [FILL: list of BDM names on your team] | Who owns this deal |
| A4 | Pipeline Stage | Dropdown | See Stage list in Part 2 | The ONE stage this deal is currently in |
| A5 | Days in Current Stage | Formula | =TODAY()-Date Entered Stage | Auto-calculates; drives alert logic |
| A6 | Date Entered Current Stage | Date | MM/DD/YYYY | Update every time stage changes |
#### Block B: Owner / Contact Information
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| B1 | Owner First Name | Text | Free text | Primary decision-maker |
| B2 | Owner Last Name | Text | Free text |  |
| B3 | Co-Owner / Spouse Name | Text | Free text | Leave blank if N/A |
| B4 | Owner Mobile | Phone | (XXX) XXX-XXXX | Primary contact number |
| B5 | Co-Owner Mobile | Phone | (XXX) XXX-XXXX |  |
| B6 | Owner Email | Email | name@domain.com |  |
| B7 | Co-Owner Email | Email | name@domain.com |  |
| B8 | Ownership Entity | Dropdown | Individual / LLC / Trust / Corporation / Partnership / [LEGAL: add state-specific entity types] | Verify via public tax records before PMA signing |
| B9 | Entity Name (if not individual) | Text | Free text | LLC name, trust name, etc. |
| B10 | Ownership Verified? | Checkbox / Dropdown | Yes / No / Pending | Must be Yes before PMA is sent |
| B11 | All Decision-Makers Identified? | Checkbox / Dropdown | Yes / No | Must be Yes before listing appointment |
| B12 | Preferred Contact Method | Dropdown | Call / Text / Email / Any |  |
#### Block C: Property Information
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| C1 | Property Address | Text | Full street address |  |
| C2 | City | Text | Free text |  |
| C3 | State | Dropdown | [FILL: states you operate in] |  |
| C4 | Zip Code | Text | XXXXX |  |
| C5 | Property Type | Dropdown | Single-Family / Condo / Townhome / Multi-Family (2 to 4 units) / Other |  |
| C6 | Bedrooms | Number | 1 / 2 / 3 / 4 / 5+ |  |
| C7 | Bathrooms | Number | 1 / 1.5 / 2 / 2.5 / 3 / 3+ |  |
| C8 | Square Footage | Number | Whole number |  |
| C9 | Stories | Number | 1 / 2 / 3+ |  |
| C10 | Pool? | Dropdown | Yes / No |  |
| C11 | HOA? | Dropdown | Yes / No |  |
| C12 | HOA Monthly Fee | Currency | $0.00 | Leave $0 if no HOA |
| C13 | Property Condition | Dropdown | Rent-Ready / Needs Minor Work / Needs Major Rehab / Unknown |  |
| C14 | Currently Occupied? | Dropdown | Vacant / Owner-Occupied / Tenant in Place |  |
| C15 | Number of Units (if multi) | Number | 1 to 4 | Default 1 for SFR |
| C16 | Doors This Deal Represents | Number | Whole number | Key for pipeline value calc |
#### Block D: Lead Intelligence
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| D1 | Lead Source | Dropdown | Inbound Web / FRBO-Active / FRBO-Stale / Realtor Referral / Owner Referral / Vendor Referral / Direct Mail / Social Media / Cold Call / Investor Network / REI Club / [FILL: any company-specific sources] | Critical for ROI tracking |
| D2 | Referring Person / Company | Text | Free text | Name of agent, owner, or vendor who referred |
| D3 | Referral Fee Owed? | Dropdown | Yes / No / TBD | Flag for accounting |
| D4 | Referral Fee Amount | Currency | $0.00 | [FILL: your referral fee schedule] |
| D5 | Inbound or Outbound? | Dropdown | Inbound / Outbound | Did they come to you or did you find them? |
| D6 | Competing PM Companies Mentioned | Text | Free text | Who else are they talking to? |
| D7 | Previous PM Company? | Dropdown | Yes / No | If yes, why are they leaving? |
| D8 | Previous PM - Reason for Leaving | Text | Free text |  |
| D9 | Self-Managing Before? | Dropdown | Yes / No |  |
#### Block E: Motivation & Qualification
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| E1 | Owner's Primary Goal | Dropdown | Generate Income / Cover Mortgage / Can't Sell / Relocating / Inherited Property / Growing Portfolio / Other |  |
| E2 | Short-Term Goal (notes) | Text | Free text | From discovery call |
| E3 | Long-Term Goal (notes) | Text | Free text |  |
| E4 | Timeline to Rent | Dropdown | ASAP (0 to 30 days) / 30 to 60 days / 60 to 90 days / 90+ days / Unknown |  |
| E5 | Motivation Level | Dropdown | Hot / Warm / Cold | BDM's gut-read after discovery call |
| E6 | Property Type Fit | Dropdown | PM Lead / Brokerage Redirect / Investment Redirect / Disqualified | Determines which department owns it |
| E7 | Disqualify Reason | Dropdown | Property Below Minimum Rent / Outside Service Area / Condition Too Poor / Owner Not Ready / Duplicate / Other | Only fill if E6 = Disqualified |
| E8 | Carrying Costs (monthly) | Currency | $0.00 | Mortgage + insurance + taxes + HOA |
| E9 | Owner's Target Rent | Currency | $0.00 | What they want |
| E10 | BDM Recommended Rent Range | Text | $X,XXX to $X,XXX | From rental market analysis |
| E11 | Other Properties Owned? | Dropdown | Yes / No | Expansion opportunity flag |
| E12 | Number of Other Properties | Number | Whole number |  |
#### Block F: Sales Activity & Timing
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| F1 | Discovery Call Date | Date | MM/DD/YYYY |  |
| F2 | Discovery Call Completed? | Dropdown | Yes / No / No-Show / Rescheduled |  |
| F3 | Listing Appointment Date | Date | MM/DD/YYYY |  |
| F4 | Listing Appointment Status | Dropdown | Scheduled / Held / No-Show / Cancelled / Rescheduled |  |
| F5 | All Decision-Makers on Appt? | Dropdown | Yes / No / Unknown | Must be Yes before appointment is "held" |
| F6 | Rental Analysis Sent? | Checkbox | Yes / No |  |
| F7 | Rental Analysis Sent Date | Date | MM/DD/YYYY |  |
| F8 | PMA Sent? | Checkbox | Yes / No |  |
| F9 | PMA Sent Date | Date | MM/DD/YYYY |  |
| F10 | PMA Signed? | Checkbox | Yes / No |  |
| F11 | PMA Signed Date | Date | MM/DD/YYYY |  |
| F12 | Package Selected | Dropdown | [FILL: your tier names, e.g., Basic / Standard / Premium] |  |
| F13 | Monthly Management Fee | Currency | $0.00 |  |
| F14 | Setup Fee Collected? | Dropdown | Yes / No / Invoiced |  |
| F15 | Next Action | Text | Free text | What is the BDM doing next on this deal? |
| F16 | Next Action Due Date | Date | MM/DD/YYYY | Must always be populated for active deals |
| F17 | Last Touch Date | Date | MM/DD/YYYY | Last time BDM contacted owner (any channel) |
| F18 | Days Since Last Touch | Formula | =TODAY()-F17 | Drives stale alert logic |
| F19 | Total Touches Made | Number | Whole number | Running count of all contacts |
| F20 | Follow-Up Sequence Active? | Dropdown | Yes / No | Is an automated or manual nurture running? |
#### Block G: Deal Outcome
| # | Column Name | Type | Allowed Values / Format | Notes |
|---|---|---|---|---|
| G1 | Deal Status | Dropdown | Active / Won / Lost / Redirected / Archived / Nurture |  |
| G2 | Won Date | Date | MM/DD/YYYY | Date PMA fully executed |
| G3 | Lost Date | Date | MM/DD/YYYY |  |
| G4 | Lost Reason | Dropdown | Price / Fees Too High / Chose Competitor / Chose Self-Manage / Not Ready / Property Disqualified / No Response / Friend/Family PM / Other |  |
| G5 | Lost to Competitor Name | Text | Free text | [FILL: track which competitors you lose to most] |
| G6 | Redirected To | Dropdown | Brokerage / Investment / Other Department | Only if E6 = Redirect |
| G7 | Handoff to Ops Complete? | Dropdown | Yes / No / In Progress |  |
| G8 | Handoff Date | Date | MM/DD/YYYY |  |
| G9 | Referral Fee Paid? | Dropdown | Yes / No / N/A |  |
| G10 | Notes / CRM Log | Text | Free text | Running notes; most recent entry at top |
### Part 2: Pipeline Stages: Full Gate Specifications
Stage Dropdown Allowed Values (in order): S0 - New Lead → S1 - Discovery Call Scheduled → S2 - Discovery Call Completed → S3 - Listing Appointment Scheduled → S4 - Listing Appointment Held → S5 - Proposal / PMA Sent → S6 - PMA Signed - Handoff → WON - Closed Won → LOST - Closed Lost → REDIRECT - Sent to Other Dept → NURTURE - Long-Term Follow Up → ARCHIVE
#### S0: New Lead
Description: Lead has entered the pipeline but BDM has not yet made live contact.
| Gate | Criteria |
|---|---|
| Entry | Lead submits inbound inquiry OR BDM logs outbound prospect (FRBO, referral, cold call, etc.) |
| Required Fields to Enter | A2 Date Created, B1 to B4 Owner Contact, C1 Property Address, D1 Lead Source, D5 Inbound/Outbound |
| BDM Action | Respond inside the configured {{speed_to_lead_minutes}}-minute window on inbound; log outbound attempt in CRM immediately |
| Exit to S1 | BDM makes live contact AND schedules discovery call |
| Exit to LOST/ARCHIVE | No response after [FILL: your max attempts, e.g., 6 touches over 10 days]; log as unresponsive |
| Max Days in Stage | 3 days; alert fires if no live contact after 3 days |
#### S1: Discovery Call Scheduled
Description: Live contact made; discovery call booked on calendar.
| Gate | Criteria |
|---|---|
| Entry | BDM spoke with owner; discovery call date/time confirmed |
| Required Fields to Enter | F1 Discovery Call Date, F16 Next Action Due Date |
| BDM Action | Send post-contact email within 5 min; send text within 15 min; add all CRM notes |
| Exit to S2 | Discovery call held; qualification complete |
| Exit to S0 | Owner no-shows or reschedules; reset and re-schedule |
| Exit to LOST | Owner cancels and declines to reschedule |
| Max Days in Stage | 5 days; alert fires if call not held within 5 days of scheduling |
#### S2: Discovery Call Completed
Description: Discovery call held; BDM has gathered property details, motivation, timeline, and qualification data.
| Gate | Criteria |
|---|---|
| Entry | Discovery call completed; F2 = Yes; all Block E fields populated |
| Required Fields to Enter | E1 to E6 (motivation/qualification), C1 to C16 (property), D1 (lead source), E10 (rent range initiated) |
| BDM Action | Begin rental market analysis; identify all decision-makers; determine PM vs. Brokerage vs. Investment redirect; schedule listing appointment |
| Exit to S3 | Listing appointment scheduled; rental analysis in progress |
| Exit to REDIRECT | Lead is better fit for Brokerage or Investment department |
| Exit to NURTURE | Owner not ready; timeline 90+ days; re-engage later |
| Exit to LOST | Owner disqualified (property below minimum, outside area, condition too poor) |
| Max Days in Stage | 3 days; listing appointment should be scheduled within 3 days of discovery call |
#### S3: Listing Appointment Scheduled
Description: Listing appointment booked; rental analysis being prepared; pre-appointment nurture sequence running.
| Gate | Criteria |
|---|---|
| Entry | F3 Listing Appointment Date populated; all decision-makers confirmed to attend |
| Required Fields to Enter | F3, F5 (all DMs confirmed), E10 (rent range), F6 (rental analysis sent or in progress) |
| BDM Action | Complete rental analysis; send pre-appointment email; execute 24-hr call and morning-of text; verify ownership entity |
| Exit to S4 | Listing appointment held as scheduled |
| Exit to S3 | Appointment rescheduled; update F3, reset nurture sequence |
| Exit to NURTURE | Owner postpones indefinitely |
| Max Days in Stage | 7 days; alert fires if appointment not held within 7 days of scheduling |
#### S4: Listing Appointment Held
Description: Listing appointment completed; pricing presented; PMA close attempted.
| Gate | Criteria |
|---|---|
| Entry | F4 = Held; BDM presented rental analysis, services, pricing, and attempted close |
| Required Fields to Enter | F4, E10 (recommended rent), F12 (package discussed), F13 (fee discussed), G10 (notes from appointment) |
| BDM Action | If signed on call → move to S6 immediately. If not signed → send PMA within same business day; set hard follow-up task within 24 hours |
| Exit to S5 | PMA sent but not yet signed |
| Exit to S6 | PMA signed on the call (best case) |
| Exit to LOST | Owner declines and closes conversation |
| Exit to NURTURE | Owner interested but timeline pushed significantly |
| Max Days in Stage | 1 day; PMA must be sent same day as appointment; alert fires at 24 hours |
#### S5: Proposal / PMA Sent (Unsigned)
Description: PMA has been sent; owner has not yet signed. This is the highest-risk stage; deals go cold here.
| Gate | Criteria |
|---|---|
| Entry | F8 = Yes; F9 (PMA Sent Date) populated |
| Required Fields to Enter | F8, F9, F15 (next action), F16 (next action due date; must be within 24 hours) |
| BDM Action | Follow up within 24 hours by call; address any remaining objections; re-close using 3-Part Close; escalate to manager if stalled beyond [FILL: your threshold, e.g., 5 days] |
| Exit to S6 | PMA signed |
| Exit to LOST | Owner declines after follow-up |
| Exit to NURTURE | Owner wants to wait; set long-term follow-up |
| Max Days in Stage | 5 days; RED ALERT fires at 48 hours unsigned; escalation alert fires at 5 days |
#### S6: PMA Signed, Handoff in Progress
Description: PMA fully executed. BDM initiating handoff to Operations/Onboarding.
| Gate | Criteria |
|---|---|
| Entry | F10 = Yes; F11 (PMA Signed Date) populated; ownership entity verified |
| Required Fields to Enter | F10, F11, F12 (package), F13 (fee), G7 (handoff status), G8 (handoff date) |
| BDM Action | Send thank-you + next steps email immediately; send Owner Intake Form link; notify onboarding specialist via CRM task; schedule onboarding call within 48 hours; flag referral fee if applicable |
| Exit to WON | Owner Intake Form received; onboarding specialist has made first contact; G7 = Yes |
| Exit flag | If handoff not confirmed within 48 hours, alert fires to BDM AND manager |
| Max Days in Stage | 2 days; this stage should close fast; stale alert at 48 hours |
#### WON: Closed Won
Description: Handoff to Operations complete. Deal is fully transferred. BDM's job on this record is done.
| Gate | Criteria |
|---|---|
| Entry | G7 Handoff Complete = Yes; onboarding specialist confirmed receipt |
| Required Fields | G2 Won Date, F11 PMA Signed Date, F12 Package, F13 Fee, D3 Referral Fee Owed, G9 Referral Fee Paid |
| BDM Action | Log final notes; confirm referral fee flagged for accounting; move row to CLOSED WON tab; update conversion metrics tab |
| Retention | Keep in CLOSED WON tab permanently; feeds all conversion and lead source reporting |
#### LOST: Closed Lost
Description: Owner chose not to proceed: chose competitor, self-manage, friend/family PM, or disqualified.
| Gate | Criteria |
|---|---|
| Entry | Owner confirmed they are not moving forward |
| Required Fields | G3 Lost Date, G4 Lost Reason, G5 Lost to Competitor (if applicable) |
| BDM Action | Log lost reason; send graceful close email; add to 90-day re-engagement nurture if appropriate; move to CLOSED LOST tab |
| Retention | Keep in CLOSED LOST tab for 12 months; feeds lost-reason analysis; eligible for re-entry if owner re-engages |
#### REDIRECT: Sent to Other Department
Description: Lead is a better fit for Brokerage or Investment; not a PM deal.
| Gate | Criteria |
|---|---|
| Entry | E6 = Brokerage Redirect or Investment Redirect |
| Required Fields | G6 Redirected To, G10 Notes |
| BDM Action | Warm handoff to correct department; log in CRM; move to REDIRECTED tab |
| Retention | Keep 6 months; track if redirect converts to PM deal later |
#### NURTURE: Long-Term Follow Up
Description: Owner is interested but not ready. Timeline is 60 to 180+ days out.
| Gate | Criteria |
|---|---|
| Entry | Owner engaged but timeline pushed; not lost, not active |
| Required Fields | F16 Next Action Due Date (must be set; no open-ended nurture), F20 Follow-Up Sequence Active = Yes |
| BDM Action | Enroll in nurture sequence; set a hard re-engagement date; touch at 30 / 60 / 90 days minimum |
| Exit to Active | Owner re-engages and is ready to move forward; re-enter at appropriate stage |
| Exit to ARCHIVE | No response after [FILL: e.g., 180 days and 8+ touches] |
| Max Days Without Touch | 30 days; alert fires if no touch logged in 30 days on any nurture record |
#### ARCHIVE
Description: Record is permanently inactive. No further action expected.
| Gate | Criteria |
|---|---|
| Entry | See Part 7: Archive Rules |
| Action | Move to ARCHIVE tab; lock row from editing; retain per your data retention policy |
### Part 3: The Spreadsheet Tab Structure
Build these as separate tabs in one workbook. Color-code the tabs for fast navigation.
| Tab Name | Color Code | Purpose |
|---|---|---|
| PIPELINE - ACTIVE | Blue | All active deals S0 to S6 + Nurture |
| CLOSED WON | Green | All won deals; permanent record |
| CLOSED LOST | Red | All lost deals; 12-month retention |
| REDIRECTED | Orange | Brokerage/Investment redirects |
| NURTURE | Yellow | Long-term follow-up deals |
| ARCHIVE | Gray | Fully inactive records |
| CONVERSION METRICS | Purple | Auto-calculated funnel + lead source stats |
| ALERTS DASHBOARD | Red | All stale/overdue flags in one view |
| BDM DAILY VIEW | Blue | Filtered view: today's tasks only |
| WEEKLY REVIEW VIEW | Green | Filtered view: full pipeline for owner/broker meeting |
| LOOKUP TABLES | Gray | Dropdown source lists; do not edit without admin |
### Part 4: The Three Working Views
#### View 1: BDM Daily View
Tab: BDM DAILY VIEW
Purpose: What the BDM opens every morning. Shows only what needs attention today.
Filter Logic: Pull from PIPELINE - ACTIVE where ANY of the following are true:
| Filter Condition | What It Catches |
|---|---|
| F16 Next Action Due Date = TODAY or PAST | Tasks due today or overdue |
| F18 Days Since Last Touch ≥ [FILL: e.g., 3] | Leads going cold |
| A5 Days in Current Stage ≥ stage max (see Part 2) | Stale stage alerts |
| F3 Listing Appointment Date = TODAY | Appointments happening today |
| F9 PMA Sent Date ≤ TODAY-2 AND F10 = No | Unsigned PMAs past 48 hours |
| G1 = Active AND F16 is blank | Deals with no next action set; data quality flag |
Columns to Show in This View (hide all others):
| Column | Why |
|---|---|
| Deal ID | Reference |
| Owner Full Name | Who to call |
| Owner Mobile | Click-to-call |
| Property Address | Context |
| Pipeline Stage | Where they are |
| Days in Current Stage | Urgency signal |
| Motivation Level | Hot / Warm / Cold; prioritize hot first |
| Next Action | What to do |
| Next Action Due Date | When |
| Days Since Last Touch | Stale signal |
| Last Touch Date | Context |
| PMA Sent? | Flag unsigned proposals |
| Notes / CRM Log | Quick context before calling |
Sort Order:
1. Motivation = Hot → first
2. Next Action Due Date → oldest first
3. Days in Stage → highest first
BDM Morning Routine with This View:
1. Open view; scan for any red alerts (overdue, unsigned PMAs)
2. Work top-to-bottom: hot leads first, then warm, then cold
3. After every call/touch → update F17 Last Touch Date, F15 Next Action, F16 Next Action Due Date
4. Never close the day with F16 blank on any active deal
#### View 2: Weekly Pipeline Review View
Tab: WEEKLY REVIEW VIEW
Purpose: The view the BDM and owner/broker look at together every week. Full pipeline visibility; no filters hidden.
Pull From: PIPELINE - ACTIVE + summary rows from CLOSED WON and CLOSED LOST for the current week
Columns to Show:
| Column | Why |
|---|---|
| Deal ID | Reference |
| Owner Full Name |  |
| Property Address |  |
| Doors This Deal Represents | Pipeline value |
| Pipeline Stage |  |
| Days in Current Stage | Stale flag |
| Motivation Level |  |
| Lead Source | ROI discussion |
| Listing Appointment Date | Upcoming or past |
| PMA Sent? |  |
| PMA Signed? |  |
| Next Action |  |
| Next Action Due Date |  |
| Lost Reason | For lost deals reviewed |
| Notes / CRM Log |  |
Sort Order:
1. Pipeline Stage (S5 first; highest risk of going cold)
2. Days in Current Stage (highest first within each stage)
3. Motivation Level (Hot first)
Weekly Review Meeting Agenda (30 to 45 min):
| # | Agenda Item | Time | Who Talks |
|---|---|---|---|
| 1 | Wins this week: PMAs signed, doors added | 3 min | BDM |
| 2 | New leads added: source, quality, first impression | 5 min | BDM |
| 3 | Stage-by-stage walk: every active deal, one sentence each | 15 min | BDM leads, owner/broker asks |
| 4 | Alerts review: stale deals, unsigned PMAs, overdue follow-ups | 5 min | Both |
| 5 | Lost deals this week: reason, what could have changed | 3 min | Both |
| 6 | Redirects: any brokerage/investment leads handed off | 2 min | BDM |
| 7 | Next week's priorities: top 3 deals to close, top 3 leads to pursue | 5 min | BDM commits |
Questions the Owner/Broker Should Ask at Every Review:
1. What is the next action on every deal in S4 and S5, and when exactly does it happen?
2. Are all decision-makers engaged on every listing appointment?
3. Which deals have been in the same stage for more than [FILL: your threshold] days; what's the plan?
4. What lead source produced the most wins this month; are we investing more there?
5. What objection killed the most deals this week; do we need to work on that script?
6. Is the pipeline 3 to 5x our monthly door goal? If not, what's the prospecting plan?
#### View 3: Conversion Metrics View
Tab: CONVERSION METRICS
Purpose: Auto-calculated funnel performance and lead source ROI. Updated in real time from PIPELINE - ACTIVE, CLOSED WON, and CLOSED LOST tabs. The full metric tables are in Part 5.
### Part 5: Conversion Metrics by Stage and Lead Source
#### 5A: Funnel Conversion Table
(Auto-calculate using COUNTIF formulas across tabs)
| Metric | Formula Logic | Benchmark | Your Number |
|---|---|---|---|
| Total Leads Created (period) | COUNT all Deal IDs created in date range |  | [auto] |
| Discovery Calls Completed | COUNT where F2 = Yes | 50 to 60% of leads | [auto] |
| Lead → Discovery Call % | Discovery Calls ÷ Total Leads | 50 to 60% | [auto] |
| Listing Appointments Held | COUNT where F4 = Held | 60 to 70% of discovery calls | [auto] |
| Discovery → Appointment % | Appts Held ÷ Discovery Calls | 60 to 70% | [auto] |
| PMAs Signed | COUNT where F10 = Yes | 40 to 60% of appts held | [auto] |
| Appointment → Close % | PMAs Signed ÷ Appts Held | 40 to 60% | [auto] |
| Overall Lead → Close % | PMAs Signed ÷ Total Leads | 20 to 30% | [auto] |
| Total Doors Added | SUM of C16 where G1 = Won |  | [auto] |
| Avg Doors Per Deal Won | Total Doors ÷ PMAs Signed | 1.3 to 1.8 | [auto] |
| Avg Days Lead to Close | AVG of (F11 PMA Date - A2 Lead Created Date) | [FILL: set your target] | [auto] |
| Avg Days in S5 (PMA Unsigned) | AVG days in S5 for all won deals | Under 3 days | [auto] |
| Lost Deal Rate | Lost ÷ (Won + Lost) | Under 70% | [auto] |
| Redirect Rate | Redirected ÷ Total Leads | [FILL: track yours] | [auto] |
#### 5B: Lead Source Performance Table
(One row per lead source; auto-calculated)
| Lead Source | Leads | Discovery Calls | Appts Held | PMAs Signed | Doors Added | Close % | Avg Days to Close | Notes |
|---|---|---|---|---|---|---|---|---|
| Inbound Web | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| FRBO - Active | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| FRBO - Stale | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Realtor Referral | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Owner Referral | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Vendor Referral | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Direct Mail | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Social Media | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Cold Call | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| Investor Network | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| REI Club | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
| [FILL: add yours] |  |  |  |  |  |  |  |  |
| TOTAL | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |  |
#### 5C: Lost Reason Analysis Table
(Auto-calculated from G4 Lost Reason field)
| Lost Reason | Count | % of All Lost | Trend vs. Last Month |
|---|---|---|---|
| Fees Too High | [auto] | [auto] | ↑ ↓ → |
| Chose Competitor | [auto] | [auto] |  |
| Chose Self-Manage | [auto] | [auto] |  |
| Not Ready / Timing | [auto] | [auto] |  |
| Friend / Family PM | [auto] | [auto] |  |
| Property Disqualified | [auto] | [auto] |  |
| No Response | [auto] | [auto] |  |
| Other | [auto] | [auto] |  |
| TOTAL LOST | [auto] | 100% |  |
---
How to use this table: If "Fees Too High" is your #1 lost reason, your pricing presentation needs work. If "No Response" is #1, your speed-to-lead or follow-up cadence is broken. If "Chose Competitor" is #1, you need better differentiation scripts. The data tells you exactly where to coach.
#### 5D: Monthly Pipeline Health Scorecard
(One row per month; BDM fills actuals; formulas calculate the rest)
| Month | Door Goal | Doors Won | % to Goal | Leads In | Close % | Top Source | Top Lost Reason | Avg Days to Close | Pipeline Value (Doors) |
|---|---|---|---|---|---|---|---|---|---|
| [FILL] | [FILL] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] | [auto] |
### Part 6: Alerts Dashboard
Tab: ALERTS DASHBOARD
Purpose: Every alert condition in one place. BDM checks this tab first every morning. Manager/broker checks it at the weekly review. Color-code rows: Red = act today, Yellow = act this week.
#### Alert Definitions Table
| Alert Name | Trigger Condition | Severity | Who Gets It | Action Required |
|---|---|---|---|---|
| Speed-to-Lead Breach | S0 deal with A2 Date Created = today and F17 Last Touch Date is blank | Critical | BDM | Contact the lead inside the configured {{speed_to_lead_minutes}}-minute window; every minute costs conversion rate |
| Unsigned PMA - 48 Hours | F8 = Yes AND F10 = No AND F9 PMA Sent Date ≤ TODAY-2 | Critical | BDM + Manager | Call owner immediately; re-close; identify objection |
| Unsigned PMA - 5 Days | F8 = Yes AND F10 = No AND F9 PMA Sent Date ≤ TODAY-5 | Critical | BDM + Manager | Escalate to manager; consider in-person or video call; last-chance close |
| Overdue Follow-Up | F16 Next Action Due Date < TODAY | Critical | BDM | Complete the action today; no exceptions |
| No Next Action Set | G1 = Active AND F16 is blank | Critical | BDM | Every active deal must have a next action and date; fix immediately |
| Handoff Not Confirmed | F10 = Yes AND G7 ≠ Yes AND F11 PMA Signed Date ≤ TODAY-2 | Critical | BDM + Ops | Confirm ops received handoff; owner intake form must be in motion |
| Stale Lead - S0 | A5 Days in Stage ≥ 3 AND G1 = Active | Warning | BDM | Make live contact today or move to Nurture/Lost |
| Stale Lead - S1 | A5 Days in Stage ≥ 5 | Warning | BDM | Discovery call hasn't happened; reschedule or disqualify |
| Stale Lead - S2 | A5 Days in Stage ≥ 3 | Warning | BDM | Listing appointment not yet scheduled; act today |
| Stale Lead - S3 | A5 Days in Stage ≥ 7 | Warning | BDM | Appointment not held; reschedule or move to Nurture |
| Stale Lead - S4 | A5 Days in Stage ≥ 1 | Warning | BDM | PMA must be sent same day as appointment; if not, send now |
| Cold Lead - No Touch | F18 Days Since Last Touch ≥ [FILL: e.g., 3] on any S0 to S4 deal | Warning | BDM | Log a touch today; call, text, or email |
| Nurture - No Touch in 30 Days | G1 = Nurture AND F18 Days Since Last Touch ≥ 30 | Warning | BDM | Re-engage or move to Archive |
| Listing Appointment - No DMs Confirmed | F3 Listing Appt Date within 48 hours AND F5 = No | Warning | BDM | Confirm all decision-makers will attend; reschedule if needed |
| Appointment No-Show | F3 Listing Appt Date = yesterday AND F4 = No-Show | Warning | BDM | Call within 1 hour of missed appointment; reschedule same day |
| Discovery Call No-Show | F1 Discovery Call Date = yesterday AND F2 = No-Show | Warning | BDM | Call within 1 hour; reschedule or move to Lost |
| Referral Fee Not Paid | G1 = Won AND D3 = Yes AND G9 = No AND G2 Won Date ≤ TODAY-7 | Warning | BDM + Accounting | Flag for accounting; referral partner relationships depend on timely payment |
| Pipeline Below Minimum | Total active pipeline doors < [FILL: 3x your monthly door goal] | Warning | BDM + Manager | Increase prospecting volume immediately; add lead source |
| No New Leads This Week | COUNT of A2 Date Created in last 7 days = 0 | Warning | BDM + Manager | Prospecting has stopped; identify why and restart |
| Ownership Not Verified Pre-Appt | F3 Listing Appt Date within 48 hours AND B10 = No or Pending | Warning | BDM | Verify ownership entity before appointment; [LEGAL: required for valid PMA] |
| Archive Eligible | See Part 7 Archive Rules | Info | BDM + Manager | Review and move to Archive tab |
#### Alerts Dashboard: Tab Layout
Build this tab as a live filtered pull from the master pipeline. No manual entry here; it auto-populates based on the trigger conditions above.
Columns to show in Alerts Dashboard:
| Column | Purpose |
|---|---|
| Alert Type | Which alert fired |
| Severity | Critical / Warning |
| Deal ID | Link back to master row |
| Owner Full Name | Who to contact |
| Owner Mobile | Click-to-call |
| Pipeline Stage | Context |
| Days in Stage | How long it's been sitting |
| Days Since Last Touch | Staleness signal |
| Next Action Due Date | What was supposed to happen |
| PMA Sent Date | For unsigned PMA alerts |
| Notes | Last CRM note for context |
Sort Order: Critical first → Warning second → oldest dates first within each group
Daily BDM Protocol with Alerts Tab:
1. Open ALERTS DASHBOARD first; before email, before anything else
2. Work every Critical alert before 10:00 AM
3. Work every Warning alert before end of day
4. No alert should carry over two consecutive days without a logged action and updated next action date
5. At end of day: alerts tab should be empty or have a documented reason for each remaining item
### Part 7: Archive Rules
Tab: ARCHIVE
Purpose: Clean, permanent, searchable record of all inactive deals. Never delete; archive instead.
#### 7A: What Gets Archived and When
| Record Type | Archive Trigger | Timing | Who Approves |
|---|---|---|---|
| Unresponsive New Lead | No live contact after [FILL: e.g., 6 attempts over 10 days] | After final attempt logged | BDM self-approves |
| Lost Deal - No Re-Engage Potential | G1 = Lost AND no re-engagement expected within 12 months | After 12 months in CLOSED LOST tab | BDM + Manager |
| Lost Deal - Hard No | Owner explicitly said never contact again | Immediately | BDM self-approves |
| Nurture - Exhausted | G1 = Nurture AND no response after [FILL: e.g., 8 touches over 180 days] | After final nurture touch logged | BDM + Manager |
| Disqualified Lead | E6 = Disqualified AND no redirect opportunity | Immediately upon disqualification | BDM self-approves |
| Duplicate Record | Same owner + same property exists as another Deal ID | Immediately upon discovery | BDM self-approves; merge notes into surviving record |
| Redirect - Confirmed Handled | G6 = Redirected AND receiving department confirmed receipt | After 30 days with no PM re-engagement | BDM self-approves |
| Won Deal - Ops Fully Onboarded | G1 = Won AND G7 = Yes AND owner is active in PM software | After 90 days post-handoff | Ops confirms; BDM archives |
#### 7B: What Must Be Complete Before Archiving
Every record must have these fields populated before it moves to Archive; no exceptions:
| Required Field | Why |
|---|---|
| G1 Deal Status | Final status must be set |
| G3 Lost Date OR G2 Won Date | Date of final outcome |
| G4 Lost Reason | Required for all Lost records; feeds lost reason analysis |
| G5 Lost to Competitor | Required if G4 = Chose Competitor |
| G10 Notes / CRM Log | Final note explaining why archived |
| D1 Lead Source | Required for all records; feeds lead source ROI |
| D3 Referral Fee Owed | Must be resolved before archiving |
| G9 Referral Fee Paid | Must = Yes or N/A before archiving |
| B10 Ownership Verified | Log whatever was determined |
#### 7C: Archive Tab Structure
The Archive tab is read-only after a record is moved there. Lock rows from editing in your spreadsheet settings.
Additional columns added only in Archive tab:
| Column | Type | Purpose |
|---|---|---|
| Date Archived | Date | MM/DD/YYYY; when moved to archive |
| Archived By | Text | BDM name who archived |
| Archive Reason | Dropdown | Unresponsive / Hard No / Exhausted Nurture / Disqualified / Duplicate / Redirect Complete / Won-Onboarded / Other |
| Re-Engage Eligible? | Dropdown | Yes - [Date] / No / Unknown |
| Re-Engage Date | Date | MM/DD/YYYY; if Yes, when to try again |
#### 7D: Data Retention Policy
| Record Type | Minimum Retention | Recommended Retention | Notes |
|---|---|---|---|
| Won Deals | Permanent | Permanent | Feeds all conversion metrics forever |
| Lost Deals | 12 months active in CLOSED LOST | Permanent in Archive | Re-engagement opportunity; competitive intel |
| Unresponsive / No Contact | 6 months | 12 months | May re-engage organically |
| Disqualified | 6 months | 12 months | Property conditions change |
| Nurture Exhausted | 12 months | 24 months | Timing changes; owners come back |
| Duplicates | 30 days | 30 days then delete | No value after merge |
---
[LEGAL: check your state's data retention requirements for real estate records]
#### 7E: Quarterly Archive Audit
Every quarter, BDM and manager run a 30-minute audit of the Archive tab:
| Audit Question | Action |
|---|---|
| Any archived records with Re-Engage Date = this quarter? | Pull back into Nurture tab; restart sequence |
| Any lost deals where the competitor they chose has a bad reputation now? | Re-engage with updated value proposition |
| Any disqualified properties that may now meet your criteria? | Re-qualify and re-enter pipeline |
| Any records missing required fields? | Complete before next audit |
| Is the archive growing faster than wins? | Investigate; prospecting quality or close rate issue |
### Part 8: Quick-Reference Master Summary
#### 8A: Stage Max Days Cheat Sheet
| Stage | Max Days Before Alert Fires | Alert Severity |
|---|---|---|
| S0 - New Lead | 3 days | Critical |
| S1 - Discovery Call Scheduled | 5 days | Warning |
| S2 - Discovery Call Completed | 3 days | Warning |
| S3 - Listing Appt Scheduled | 7 days | Warning |
| S4 - Listing Appt Held | 1 day | Critical |
| S5 - PMA Sent Unsigned | 2 days (warning) / 5 days (escalate) | Critical |
| S6 - Handoff in Progress | 2 days | Critical |
| Nurture - No Touch | 30 days | Warning |
#### 8B: Fill-In Markers Master List
Every [FILL] and [LEGAL] marker in this document, consolidated:
| Marker | Location | What to Fill In |
|---|---|---|
| [FILL: BDM names] | A3 | Names of all BDMs on your team |
| [FILL: states you operate in] | C3 | Your active markets |
| [FILL: lead sources] | D1 | Any company-specific sources not listed |
| [FILL: your tier names] | F12 | Your management package names |
| [FILL: max attempts before archive] | S0 exit / Archive rules | Your policy, e.g., 6 attempts over 10 days |
| [FILL: days since last touch threshold] | Alert table | Your standard, e.g., 3 days for active, 30 for nurture |
| [FILL: your referral fee schedule] | D4 | Dollar amount or % per referral type |
| [FILL: your monthly door goal] | Pipeline health alert | Your current growth target |
| [FILL: nurture exhaustion threshold] | Nurture exit / Archive | e.g., 8 touches over 180 days |
| [FILL: re-engagement window] | Archive rules | How long before you try a lost lead again |
| [LEGAL: one PMA per unit requirement] | S6 / B8 | Confirm with broker of record by state |
| [LEGAL: ownership entity types by state] | B8 | Confirm valid entity types in your markets |
| [LEGAL: data retention requirements] | Part 7D | Check state real estate record retention laws |
| [LEGAL: fair housing — age/student restrictions] | E7 disqualify reasons | Confirm applicable law before using as disqualify reason |
| [LEGAL: broker signature requirements on PMA] | S6 entry | Confirm who must co-sign in your state |
#### 8C: One-Page Pipeline Board Summary
---
TABS: PIPELINE ACTIVE | CLOSED WON | CLOSED LOST | REDIRECTED | NURTURE | ARCHIVE | CONVERSION METRICS | ALERTS DASHBOARD | BDM DAILY VIEW | WEEKLY REVIEW VIEW | LOOKUP TABLES
STAGES: S0 New Lead → S1 Discovery Scheduled → S2 Discovery Done → S3 Appt Scheduled → S4 Appt Held → S5 PMA Sent → S6 Handoff → WON / LOST / REDIRECT / NURTURE / ARCHIVE
CRITICAL ALERTS: Unsigned PMA > 48 hrs | Overdue follow-up | No next action set | Speed-to-lead breach | Handoff not confirmed > 48 hrs
WARNING ALERTS: Cold lead > 3 days no touch | Nurture > 30 days no touch | No DMs confirmed before appt | Pipeline below 3x monthly goal | No new leads in 7 days
METRICS: Lead→Discovery % | Discovery→Appt % | Appt→Close % | Overall Close % | Doors/Deal | Days to Close | By Lead Source | By Lost Reason | Monthly Scorecard
ARCHIVE TRIGGERS: Hard No (immediate) | Unresponsive (10 days) | Nurture Exhausted (180 days) | Disqualified (immediate) | Won + Onboarded (90 days post-handoff) | Duplicate (immediate)
Ascend Operations Library, owner-reviewed generic baseline document; verify with your broker of record and legal counsel. Companion to the BDM Owner-Acquisition Playbook; second document in the Business Development folder.
