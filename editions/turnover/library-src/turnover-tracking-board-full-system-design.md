---
title: "Turnover Tracking Board Full System Design"
source: "Reviewed generic turnover library"
converted: 2026-08-18
audience: all agents
status: reference
---

# Turnover Tracking Board Full System Design

## Turnover Tracking Board: Full System Design
420 Doors | Class B to D | Remote Coordinator + In-House Techs + Vendors, [Company Name]
Built to be consistent with the Make-Ready Checklist, Owner Communication Templates, Dispatch Decision Matrix, Class-Based Benchmarks, Turnover Grading Framework, and Monthly Performance Report. Every unit in turnover is one row on the board; every stage, date, cost, grade, and document is one column; every reminder, owner email, and escalation is an automation tied to those columns.
Platform note: this design is platform-agnostic. the setup library's reference build targets Monday.com; the Monday.com steps in Part 8 are kept as reference mechanics. [Company Name] has not chosen an implementation.
### Part 1: Board Architecture Overview
---
Recommended Platform

| Platform | Why It Works for This |
|---|---|
| Monday.com (recommended) | Best automation engine, multiple views, color-coded status, formula columns, email integrations, dashboard widgets; purpose-built for exactly this |
| ClickUp | Strong alternative; more flexible but steeper learning curve |
| Airtable | Great for data-heavy teams; less intuitive for coordinators doing daily updates |
| AppFolio / Buildium | Use as your data source; feed dates and financials into the board. Don't try to run the tracking board inside your PM software |

Recommendation: build the board in a workflow tool. Pull key data from your PM software (AppFolio/Buildium) manually or via Zapier integration. Your PM software tracks leases and financials; your tracking board tracks workflow and performance.
### Part 2: The Stages

---
Every unit moves left to right through these 8 stages, no skipping:
1 Notice Received then 2 Pre-Move-Out Inspection then 3 Move-Out Inspection then 4 Make-Ready In Progress then 5 Final Inspection Passed then 6 Photos and Marketing Ready then 7 Owner Approved then 8 Listed
#### Stage 1: Notice Received
Trigger: Tenant submits notice to vacate OR lease non-renewal confirmed
Owner: Coordinator
Target Duration: Same day as notice received

| Action | Who | Timing |
|---|---|---|
| Log notice in PM software | Coordinator | Same day |
| Create unit row on tracking board | Coordinator | Same day |
| Send tenant move-out packet (checklist, key return instructions, forwarding address request) | Coordinator | Within 24 hours |
| Notify owner: Notice Received email (Template 1) | Coordinator | Within 24 hours |
| Schedule pre-move-out inspection | Coordinator | Within 48 hours; target 1 to 2 weeks before move-out date |
| Flag unit for pre-marketing review | Coordinator | Within 48 hours |

#### Stage 2: Pre-Move-Out Inspection
Trigger: Scheduled 10 to 14 days before move-out date
Owner: Coordinator (remote) + In-House Tech (on-site)
Target Duration: Completed and reported within 48 hours of inspection

| Action | Who | Timing |
|---|---|---|
| Conduct pre-move-out inspection with tenant present if possible | In-House Tech | Per scheduled date |
| Document condition with photos; upload to PM software | In-House Tech | Same day as inspection |
| Identify likely make-ready scope; preliminary task list | Coordinator | Within 24 hours of inspection |
| Send owner: Pre-Move-Out Inspection Summary (Template 2) | Coordinator | Within 48 hours of inspection |
| Begin preliminary vendor scheduling for anticipated work | Coordinator | Within 48 hours of inspection |
| Begin pre-marketing; draft listing, order photos slot | Coordinator | Within 48 hours of inspection |

#### Stage 3: Move-Out Inspection
Trigger: Tenant vacates; keys returned or confirmed gone
Owner: Coordinator (remote) + In-House Tech (on-site)
Target Duration: Inspection completed within 24 hours of vacancy; report within 48 hours

| Action | Who | Timing |
|---|---|---|
| Confirm tenant has fully vacated; keys returned | Coordinator | Move-out date |
| Conduct move-out inspection; full documentation with photos | In-House Tech | Within 24 hours of vacancy |
| Complete move-out inspection report; upload to PM software | In-House Tech | Same day as inspection |
| Identify and document all damage vs. normal wear and tear | Coordinator | Within 24 hours of inspection |
| Calculate damage chargeback amount; initiate security deposit disposition | Coordinator | Within 48 hours |
| Send owner: Move-Out Inspection Report (Template 3) | Coordinator | Within 48 hours |
| Finalize make-ready scope and budget estimate | Coordinator | Within 48 hours |
| Get owner approval if make-ready estimate exceeds threshold | Coordinator | Before dispatching any work |
| Dispatch vendors and in-house techs per Dispatch Decision Matrix | Coordinator | Within 48 hours of owner approval |

#### Stage 4: Make-Ready In Progress
Trigger: Owner approval received; work orders dispatched
Owner: Coordinator (remote); In-House Techs + Vendors (on-site)
Target Duration: Per class benchmark (see Part 4)

| Action | Who | Timing |
|---|---|---|
| Confirm all vendors and techs scheduled and confirmed | Coordinator | Day 1 of stage |
| Track work order completion in PM software | Coordinator | Daily |
| Send owner: Make-Ready Kickoff Update (Template 4) | Coordinator | Day 1 of stage |
| Monitor stage age; flag Yellow/Red per class benchmark | Board Automation | Daily |
| Send mid-point owner update if stage exceeds 50% of benchmark | Coordinator | Per automation trigger |
| Collect and upload all vendor invoices | Coordinator | As received |
| Confirm in-house tech task completions | In-House Tech | Per work order |
| Escalate to leadership if stage hits Red threshold | Automation | Per class benchmark |

#### Stage 5: Final Inspection
Trigger: All work orders marked complete by coordinator
Owner: Coordinator (remote) + In-House Tech (on-site)
Target Duration: Completed within 24 hours of work order completion

| Action | Who | Timing |
|---|---|---|
| Schedule final inspection immediately upon work completion | Coordinator | Same day work is confirmed complete |
| Conduct final inspection; verify all make-ready checklist items | In-House Tech | Within 24 hours |
| Document final condition with photos; upload to PM software | In-House Tech | Same day as inspection |
| Pass or Fail determination | Coordinator | Within 2 hours of inspection report |
| If Pass: advance to Stage 6 | Coordinator | Immediately |
| If Fail: create punch list, re-dispatch, re-inspect | Coordinator | Within 24 hours |
| Send owner: Final Inspection Complete (Template 5) | Coordinator | Within 24 hours of pass |

#### Stage 6: Photos and Marketing Ready
Trigger: Final inspection passed
Owner: Coordinator
Target Duration: Photos completed and listing drafted within 48 hours of final inspection pass

| Action | Who | Timing |
|---|---|---|
| Schedule professional photographer | Coordinator | Same day as final inspection pass |
| Confirm unit is clean, staged, and showing-ready before shoot | In-House Tech | Before photo appointment |
| Conduct photo shoot | Photographer / Vendor | Per scheduled date |
| Review and approve photos | Coordinator | Within 24 hours of shoot |
| Draft listing: description, rent rate, availability date | Coordinator | Within 24 hours of photo approval |
| Submit listing and photos to leadership/owner for approval | Coordinator | Within 24 hours of draft completion |

#### Stage 7: Owner Approved
Trigger: Owner approves listing details and rent rate
Owner: Coordinator
Target Duration: Same day as approval received

| Action | Who | Timing |
|---|---|---|
| Confirm owner approval of rent rate and listing | Coordinator | Per owner response |
| Finalize listing on all platforms | Coordinator | Same day as approval |
| Place lockbox; confirm showing access | In-House Tech | Same day as listing goes live |
| Send owner: Unit Listed Confirmation (Template 6) | Coordinator | Same day |
| Notify leasing team: unit active and showing-ready | Coordinator | Same day |

#### Stage 8: Listed
Trigger: Listing confirmed live on all platforms
Owner: Leasing Team
Target Duration: This is the finish line for the turnover board; the unit hands off to the leasing pipeline

| Action | Who | Timing |
|---|---|---|
| Confirm listing live on all platforms | Coordinator | Day of listing |
| Log final turn-time (move-out date to listed date) | Coordinator | Same day |
| Log final make-ready cost (total actual vs. budget) | Coordinator | Same day |
| Calculate and log turnover grade | Coordinator | Same day |
| Archive completed row to Monthly Report | Coordinator | End of month |
| Begin weekly leasing updates to owner | Leasing Team | Weekly until leased |

### Part 3: Board Columns

---
Every row = one unit in turnover. Every column = one data point.
#### Core Identifier Columns

| Column Name | Type | What Goes Here |
|---|---|---|
| Property Address | Text | Full street address |
| Unit # | Text | Unit number if multifamily |
| Property Class | Dropdown | B / C / D |
| Owner Name | Text | Owner of record |
| Coordinator | Person | Assigned coordinator |
| In-House Tech | Person | Assigned tech |

#### Key Date Columns

| Column Name | Type | What Goes Here |
|---|---|---|
| Notice Received Date | Date | Date notice to vacate was confirmed |
| Move-Out Date | Date | Tenant's confirmed move-out date |
| Pre-Move-Out Inspection Date | Date | Date pre-move-out inspection was completed |
| Move-Out Inspection Date | Date | Date final move-out inspection was completed |
| Make-Ready Start Date | Date | Date work orders were dispatched |
| Make-Ready Complete Date | Date | Date all work orders confirmed complete |
| Final Inspection Date | Date | Date final inspection was completed |
| Final Inspection Result | Dropdown | Pass / Fail / Re-Inspect |
| Photos Completed Date | Date | Date professional photos were approved |
| Listed Date | Date | Date unit went live on all platforms |

#### Turn-Time Columns

| Column Name | Type | Formula / What Goes Here |
|---|---|---|
| Turn-Time (Days) | Formula | Listed Date minus Move-Out Date |
| Class Benchmark (Days) | Formula | Auto-populate based on Class: B=12, C=14, D=21 |
| Days Over/Under Benchmark | Formula | Turn-Time minus Class Benchmark (negative = under = good) |
| Stage Age (Days) | Formula | Today minus Stage Start Date (resets at each stage) |
| Turn-Time Status | Status | Green / Yellow / Red (auto per benchmark) |

#### Budget Columns

| Column Name | Type | What Goes Here |
|---|---|---|
| Make-Ready Budget (Estimated) | Currency | Estimated cost at scope approval |
| Make-Ready Actual (Total) | Currency | Sum of all invoices; updated as received |
| Cleaning Cost | Currency | Actual cleaning invoice |
| Paint Cost | Currency | Actual paint invoice |
| Repair Cost | Currency | Actual repair invoices |
| Flooring Cost | Currency | Actual flooring invoice |
| HVAC / Mechanical | Currency | Actual HVAC invoice |
| Other Costs | Currency | Any additional costs |
| Damage Chargeback Amount | Currency | Amount charged to tenant / deducted from deposit |
| Chargeback Status | Dropdown | Pending / Collected / Disputed / Written Off |
| Net Make-Ready Cost to Owner | Formula | Make-Ready Actual minus Damage Chargeback |
| Budget Variance | Formula | Make-Ready Actual minus Make-Ready Budget |
| Budget Status | Status | Green On Budget / Yellow Watch / Red Over Budget |

#### Grading Columns

| Column Name | Type | What Goes Here |
|---|---|---|
| Turn-Time Grade | Dropdown | A / B / C / D |
| Budget Grade | Dropdown | A / B / C / D |
| Inspection Grade | Dropdown | A / B / C / D |
| Owner Comms Grade | Dropdown | A / B / C / D |
| Documentation Grade | Dropdown | A / B / C / D |
| Overall Turnover Grade | Formula | Weighted average per grading framework |
| Root Cause Notes | Long Text | Required for any grade below B |

#### Documentation Columns

| Column Name | Type | What Goes Here |
|---|---|---|
| Move-Out Inspection Report | File / Link | Link to report in PM software or uploaded PDF |
| Make-Ready Photo Set | File / Link | Link to before/after photo folder |
| Vendor Invoices | File / Link | Link to invoice folder in PM software |
| Owner Approval Confirmation | File / Link | Email thread or portal approval screenshot |
| Listing Link | URL | Live listing URL once posted |
| Notes / Flags | Long Text | Any open issues, delays, or escalations |

### Part 4: Status Values and Color Logic
---
Stage Status

| Status | Color | Meaning |
|---|---|---|
| Not Started | Gray | Stage not yet reached |
| In Progress | assigned coordinator | Stage actively being worked |
| Awaiting Owner | Purple | Waiting on owner approval or response |
| Awaiting Vendor | Orange | Waiting on vendor scheduling or completion |
| Complete | Green | Stage finished; ready to advance |
| Stalled | Red | Stage has exceeded time threshold; escalate |
| Failed, Re-Inspect | Red | Final inspection failed; punch list issued |
| Cancelled | Black | Turnover cancelled; owner pulling unit |

#### Turn-Time Status (Auto-Calculated by Class)

| Class | Green | Yellow | Red |
|---|---|---|---|
| B | <=12 days | 13 to 18 days | 19+ days |
| C | <=14 days | 15 to 21 days | 22+ days |
| D | <=21 days | 22 to 30 days | 31+ days |

#### Budget Status (Auto-Calculated by Class)

| Class | Green | Yellow | Red |
|---|---|---|---|
| B | <=$1,000 | $1,001 to $1,800 | $1,801+ |
| C | <=$800 | $801 to $1,400 | $1,401+ |
| D | <=$1,200 | $1,201 to $2,500 | $2,501+ |

### Part 5: Stage Ownership Map

---

| Stage | Primary Owner | Secondary / On-Site | Escalate To |
|---|---|---|---|
| 1: Notice Received | Coordinator | None | PM Lead |
| 2: Pre-Move-Out Inspection | Coordinator | In-House Tech | PM Lead |
| 3: Move-Out Inspection | Coordinator | In-House Tech | PM Lead |
| 4: Make-Ready In Progress | Coordinator | In-House Techs + Vendors | PM Lead |
| 5: Final Inspection | Coordinator | In-House Tech | PM Lead |
| 6: Photos and Marketing Ready | Coordinator | Photographer | PM Lead |
| 7: Owner Approved | Coordinator | Owner | PM Lead |
| 8: Listed | Leasing Team | Coordinator | PM Lead |

### Part 6: Automations
---
Reminder Automations

| Trigger | Action | Recipient | Timing |
|---|---|---|---|
| Stage 1 created | Remind to schedule pre-move-out inspection | Coordinator | 24 hours after creation |
| Pre-Move-Out Inspection Date set | Remind to confirm tech is scheduled | Coordinator | 48 hours before inspection date |
| Move-Out Date arrives | Remind to confirm tenant has vacated and schedule move-out inspection | Coordinator | Day of move-out |
| Move-Out Inspection Date set | Remind to complete and upload inspection report | In-House Tech | Day of inspection |
| Make-Ready Start Date set | Remind to confirm all vendors and techs are scheduled | Coordinator | 24 hours after start date |
| Make-Ready In Progress, Day 3 | Remind to check work order status and update board | Coordinator | Day 3 of Stage 4 |
| Final Inspection Date set | Remind to confirm tech is scheduled and unit is ready | Coordinator | 24 hours before inspection |
| Photos Completed Date set | Remind to review and approve photos | Coordinator | 24 hours after photo date |
| Stage 7, Owner Approval pending 48 hours | Remind to follow up with owner | Coordinator | 48 hours after entering Stage 7 |

#### Owner Email Automations
Tied directly to the Owner Communication Templates.

| Trigger | Email Sent | Template |
|---|---|---|
| Stage 1: Notice Received logged | Owner: Notice Confirmed + Move-Out Timeline | Template 1 |
| Stage 2: Pre-Move-Out Inspection complete | Owner: Pre-Move-Out Inspection Summary | Template 2 |
| Stage 3: Move-Out Inspection complete | Owner: Move-Out Inspection Report + Make-Ready Scope | Template 3 |
| Stage 4: Make-Ready Start Date set | Owner: Make-Ready Kickoff + Budget Estimate | Template 4 |
| Stage 4: Stage Age hits 50% of class benchmark | Owner: Make-Ready Mid-Point Update | Template 4b |
| Stage 5: Final Inspection Passed | Owner: Final Inspection Complete + Unit Status | Template 5 |
| Stage 8: Listed Date set | Owner: Unit Listed Confirmation + Listing Link | Template 6 |

In Monday.com: set these as automation recipes: "When [Stage Status] changes to [Complete], send email to [Owner Email column] using [Template]". Use Monday's Email and Activities integration or connect via Zapier to Gmail/Outlook.
#### Escalation Automations
These are your safety net; they catch stalls before they become expensive.

| Trigger | Action | Recipient | Timing |
|---|---|---|---|
| Stage 4: Stage Age hits Yellow threshold for class | Change Turn-Time Status to Yellow + notify coordinator | Coordinator | Per class: B=Day 13, C=Day 15, D=Day 22 |
| Stage 4: Stage Age hits Red threshold for class | Change Turn-Time Status to Red + notify coordinator AND PM Lead | Coordinator + PM Lead | Per class: B=Day 19, C=Day 22, D=Day 31 |
| Any stage: no status update for 3 consecutive days | Flag row as Red Stalled + notify coordinator | Coordinator | 72 hours of no update |
| Any stage: no status update for 5 consecutive days | Escalate to PM Lead + flag for leadership review | PM Lead | 120 hours of no update |
| Stage 7: Owner Approval pending 48+ hours | Remind coordinator to follow up with owner | Coordinator | 48 hours after entering Stage 7 |
| Stage 7: Owner Approval pending 72+ hours | Escalate to PM Lead; owner may need direct outreach | PM Lead | 72 hours after entering Stage 7 |
| Final Inspection: Result = Fail | Notify coordinator + create punch list task + reset Stage 5 clock | Coordinator | Immediately on Fail status |
| Final Inspection: 2nd consecutive Fail | Escalate to PM Lead + flag for root cause review | PM Lead | Immediately on 2nd Fail |
| Make-Ready Actual exceeds Budget by 10% | Notify coordinator + flag Budget Status Yellow | Coordinator | As invoices are entered |
| Make-Ready Actual exceeds Budget by 25%+ | Notify coordinator AND PM Lead + flag Budget Status Red | Coordinator + PM Lead | As invoices are entered |
| Unit reaches Stage 8 Listed | Auto-calculate Turn-Time Grade + Budget Grade + trigger Overall Grade formula | Board | Immediately on Listed Date entry |
| Unit reaches Stage 8 Listed with Grade C or D | Create Root Cause Notes task + assign to coordinator | Coordinator | Immediately on grade calculation |

#### Stage Transition Automations

| Trigger | Action |
|---|---|
| Stage 3: Move-Out Inspection marked Complete | Auto-advance status to Stage 4; prompt coordinator to confirm work orders dispatched |
| Stage 4: All work orders marked Complete | Auto-advance status to Stage 5; prompt coordinator to schedule final inspection |
| Stage 5: Final Inspection marked Pass | Auto-advance status to Stage 6; prompt coordinator to schedule photographer |
| Stage 6: Photos marked Approved | Auto-advance status to Stage 7; prompt coordinator to submit listing for owner approval |
| Stage 7: Owner Approval marked Received | Auto-advance status to Stage 8; prompt coordinator to confirm listing is live |
| Stage 8: Listed Date entered | Auto-calculate all grade columns + auto-populate Monthly Report group |

### Part 7: The Three Views
---
View 1: Coordinator View
"What do I need to do today and what's at risk?"
Type: Kanban Board (grouped by Stage) + My Work filter
What they see:
Only rows assigned to them as Coordinator
Units organized in columns by Stage; drag left to right as work progresses
Each card shows: Address | Class | Stage Age | Turn-Time Status color | Next Action needed
Red and Yellow cards float to the top automatically
My Tasks panel on the right: all open action items assigned to them
Filters active: Coordinator = [Me]; Status is not Listed (completed units hidden from daily view); sorted by Turn-Time Status (Red first, Yellow second, Green third).
Key columns visible on each card: Property Address, Class, Current Stage, Stage Age (Days), Turn-Time Status (Green/Yellow/Red), Next Action / Notes, In-House Tech assigned, Move-Out Date, Target Listed Date.
Why it works for a remote coordinator: they open the board every morning and immediately see every unit they own, what stage it's in, what's stalled, and what needs action today, without digging through a spreadsheet.
#### View 2: Leadership View
"How is the whole portfolio performing right now?"
Type: Table View + Dashboard with widgets
Table View, what leadership sees: all active turnovers across all coordinators; grouped by Coordinator (so you can see each person's workload at a glance); sorted by Turn-Time Status (Red first); all columns visible including grades, budget variance, and stage age.
Dashboard widgets, built alongside the board:

| Widget | What It Shows |
|---|---|
| Active Turnovers by Stage | Bar chart: how many units are in each stage right now |
| Turn-Time Status Breakdown | Pie chart: % Green / Yellow / Red across all active units |
| Average Turn-Time by Class | Number widgets: B / C / D vs. benchmark |
| Average Make-Ready Cost by Class | Number widgets: B / C / D vs. benchmark |
| Units in Red Status | Count widget: number of units currently flagged Red |
| Coordinator Workload | Bar chart: units per coordinator by stage |
| Budget Variance, This Month | Sum widget: total over/under budget across all active turnovers |
| Estimated Vacancy Cost, This Month | Formula widget: sum of excess vacancy days x daily rent rates |
| Turnovers Completed This Month | Count widget: feeds directly into Monthly Performance Report |
| Grade Distribution, This Month | Pie chart: A / B / C / D grades on completed turnovers |

Why it works for leadership: one dashboard, real-time, no manual pulling. You walk into your Monday morning meeting and the whole portfolio is on one screen. Any Red unit gets discussed. Any coordinator with a heavy Red load gets support.
#### View 3: Owner View
"What's happening with my property right now?"
Important: owners do not get direct access to the board. This view is what you use to generate their updates, either as a portal report, a PDF export, or the owner email templates triggered automatically.
What owners see, via portal or email:

| Information | Delivery Method | Timing |
|---|---|---|
| Notice confirmed + move-out timeline | Automated email, Template 1 | Day notice received |
| Pre-move-out inspection summary + photos | Automated email, Template 2 | Within 48 hrs of inspection |
| Move-out inspection report + make-ready scope + budget estimate | Automated email, Template 3 | Within 48 hrs of move-out inspection |
| Make-ready kickoff + estimated completion date | Automated email, Template 4 | Day work orders dispatched |
| Make-ready mid-point update | Automated email, Template 4b | At 50% of class benchmark |
| Final inspection passed + unit status | Automated email, Template 5 | Within 24 hrs of pass |
| Unit listed + listing link + rent rate | Automated email, Template 6 | Day unit goes live |
| Weekly leasing update | Automated email, Leasing Template | Weekly until leased |

For multi-property owners: generate a Portfolio Summary PDF from the Leadership Dashboard at month-end; pull their properties only, export the table, attach to the Monthly Performance Report email.
What owners never see: coordinator names or performance grades; vendor names or vendor scorecards; internal escalation flags or root cause notes; other owners' properties.
### Part 8: Reference build (Monday.com)

---
the setup library's step-by-step guide for building this in Monday.com from scratch, kept as reference mechanics. Five phases, sixteen steps.
#### Phase 1: Board Setup (Day 1, 2 hours)
Step 1: Create the Board
Log into Monday.com, click + New, then New Board
Name it: Turnover Tracking Board, [Company Name]
Set type to: Main Board (not a private board; leadership needs access)
Set permissions: Team members can edit / Guests view only (for any external access)
Step 2: Set Up Groups (groups = your active pipeline stages; create one group per stage)
Stage 1: Notice Received
Stage 2: Pre-Move-Out Inspection
Stage 3: Move-Out Inspection
Stage 4: Make-Ready In Progress
Stage 5: Final Inspection
Stage 6: Photos and Marketing Ready
Stage 7: Owner Approved
Stage 8: Listed
Completed, Archive (for closed turnovers; feeds monthly report)
Cancelled (for pulled units)
Step 3: Add All Columns (add columns in this order; match exactly to Part 3 of this document)

| Group | Column | Monday.com type / formula |
|---|---|---|
| Core Identifiers | Property Address | Text |
|  | Unit # | Text |
|  | Property Class | Dropdown (options: B / C / D) |
|  | Owner Name | Text |
|  | Coordinator | People |
|  | In-House Tech | People |
| Key Dates | Notice Received Date | Date |
|  | Move-Out Date | Date |
|  | Pre-Move-Out Inspection Date | Date |
|  | Move-Out Inspection Date | Date |
|  | Make-Ready Start Date | Date |
|  | Make-Ready Complete Date | Date |
|  | Final Inspection Date | Date |
|  | Final Inspection Result | Dropdown (Pass / Fail / Re-Inspect) |
|  | Photos Completed Date | Date |
|  | Listed Date | Date |
| Turn-Time | Turn-Time (Days) | Formula: {Listed Date} - {Move-Out Date} |
|  | Class Benchmark (Days) | Formula: IF({Property Class}="B", 12, IF({Property Class}="C", 14, 21)) |
|  | Days Over/Under | Formula: {Turn-Time (Days)} - {Class Benchmark (Days)} |
|  | Stage Age (Days) | Formula: TODAY() - {Make-Ready Start Date} (adjust per stage as needed) |
|  | Turn-Time Status | Status (configure colors per benchmark thresholds) |
| Budget | Make-Ready Budget | Numbers (set as currency) |
|  | Make-Ready Actual | Numbers (set as currency) |
|  | Cleaning Cost, Paint Cost, Repair Cost, Flooring Cost, HVAC / Mechanical, Other Costs | Numbers (one column each) |
|  | Damage Chargeback Amount | Numbers |
|  | Chargeback Status | Dropdown (Pending / Collected / Disputed / Written Off) |
|  | Net Make-Ready Cost | Formula: {Make-Ready Actual} - {Damage Chargeback Amount} |
|  | Budget Variance | Formula: {Make-Ready Actual} - {Make-Ready Budget} |
|  | Budget Status | Status (configure colors per benchmark thresholds) |
| Grades | Turn-Time Grade, Budget Grade, Inspection Grade, Owner Comms Grade, Documentation Grade | Dropdown (A / B / C / D), one column each |
|  | Overall Turnover Grade | Formula (weighted average; see grading framework) |
|  | Root Cause Notes | Long Text |
| Documentation | Move-Out Inspection Report, Make-Ready Photo Set, Vendor Invoices, Owner Approval Confirmation, Listing Link | Link (one column each) |
|  | Notes / Flags | Long Text |

#### Phase 2: Status Configuration (Day 1, 30 minutes)
Step 4: Configure Turn-Time Status Colors. Click the Turn-Time Status column, then Edit Labels. Add: Green / Yellow / Red / Not Yet Calculated. These will be set manually by coordinator OR triggered by automation.
Step 5: Configure Budget Status Colors. Same process: Green On Budget / Yellow Watch / Red Over Budget.
Step 6: Configure Stage Status Colors (per the status values in Part 4): Not Started / In Progress / Awaiting Owner / Awaiting Vendor / Complete / Stalled / Failed, Re-Inspect / Cancelled.
#### Phase 3: Automations (Day 2, 2 to 3 hours)
Step 7: Build Reminder Automations. Go to Automate, then Custom Automation. Build each reminder from the Reminder Automations table in Part 6. Example recipe: "When Move-Out Date arrives, notify Coordinator: 'Confirm tenant has vacated and schedule move-out inspection for [Property Address]'".
Step 8: Build Escalation Automations. Build each escalation from the Escalation Automations table in Part 6. Example recipe: "When Stage Age (Days) changes, if Stage Age > 19 AND Property Class = B, change Turn-Time Status to Red, then notify Coordinator AND PM Lead". For the 3-day stall automation: "When last activity on item was more than 3 days ago AND status is not Complete, change status to Stalled, then notify Coordinator".
Step 9: Build Stage Transition Automations. Example recipe: "When Final Inspection Result changes to Pass, move item to Stage 6 group, then notify Coordinator: 'Final inspection passed; schedule photographer for [Property Address]'".
Step 10: Build Owner Email Automations. Connect Monday.com to Gmail or Outlook via Monday Email Integration or Zapier. Build one automation per owner email trigger from the Owner Email Automations table. Use the Owner Email column as the recipient. Paste your owner communication templates as the email body. Use column variables to auto-populate: {Property Address}, {Move-Out Date}, {Make-Ready Budget}, {Listed Date}, etc.
#### Phase 4: Views (Day 2, 1 hour)
Step 11: Build Coordinator View. Click + Add View, then Kanban. Group by: Stage Group. Filter: Coordinator = Me. Sort: Turn-Time Status (Red first). Save as: "My Turnovers, Coordinator View".
Step 12: Build Leadership View. Click + Add View, then Table. Show all columns. Group by: Coordinator. Sort by: Turn-Time Status (Red first). Save as: "Portfolio Overview, Leadership".
Step 13: Build Leadership Dashboard. Click + Add, then Dashboard. Add widgets per the Leadership View widget list in Part 7. Connect each widget to the Turnover Tracking Board as its data source. Save as: "Turnover Performance Dashboard".
#### Phase 5: Test and Launch (Day 3, 2 hours)
Step 14: Run a Test Turnover. Create one fake row and walk it through all 8 stages manually. Confirm every automation fires correctly at the right trigger, all formula columns calculate correctly, all status colors change as expected, and owner email templates send with correct variable population.
Step 15: Train Your Team. Coordinator training: 30-minute walkthrough focused on daily use, how to update stages, how to log costs. In-house tech training: show them how to view their assigned tasks; they don't need to manage the board, just confirm completions. Leadership training: 20-minute dashboard walkthrough focused on Red flags and the weekly review rhythm.
Step 16: Go Live. Enter all currently active turnovers into the board at their correct current stage. Set the board as the single source of truth for all turnover status; retire any spreadsheets.
### Part 9: Data To Feed From Your PM Software

---
The rule: your PM software (AppFolio / Buildium / Rentvine) is your financial and lease record system. Your tracking board is your workflow and performance system. They work together: your PM software feeds the board, the board drives the work.
#### Data You Pull Into the Board From Your PM Software

| Data Point | Where It Lives in PM Software | How Often | Manual or Automated |
|---|---|---|---|
| Property Address | Property record | Once at row creation | Manual |
| Property Class | Property record / custom field | Once at row creation | Manual |
| Owner Name | Owner record | Once at row creation | Manual |
| Owner Email | Owner record | Once at row creation | Manual |
| Notice to Vacate Date | Tenant record / lease record | When received | Manual; coordinator enters same day |
| Move-Out Date | Lease record | When confirmed | Manual; coordinator updates if date changes |
| Monthly Rent Amount | Lease record | Once at row creation | Manual; used for vacancy cost calculation |
| Security Deposit Amount | Tenant ledger | Once at row creation | Manual; used for chargeback reconciliation |
| Work Order Costs | Work order / maintenance ledger | As invoices are posted | Manual; coordinator enters per line item as vendors invoice |
| Vendor Invoice Totals | Accounts payable / maintenance ledger | As invoices are approved | Manual, or via Zapier if your PM software supports it |
| Damage Chargeback Amount | Tenant ledger / security deposit disposition | After move-out inspection | Manual; coordinator enters after disposition is calculated |
| Chargeback Collection Status | Tenant ledger | As updated | Manual; coordinator updates when collected or disputed |
| Listing Go-Live Date | Vacancy / marketing module | When listing is confirmed live | Manual; coordinator enters same day |

#### Data You Push From the Board Back to Your PM Software

| Data Point | Where It Goes in PM Software | When | How |
|---|---|---|---|
| Make-Ready Completion Date | Property record / vacancy record | When Stage 5 passes | Manual; coordinator updates vacancy record |
| Rent-Ready / Available Date | Vacancy / marketing record | When Stage 8 is reached | Manual; coordinator updates listing record |
| Total Make-Ready Cost | Owner statement / property ledger | When all invoices are entered | Manual; coordinator confirms total matches PM software ledger |
| Turnover Grade | Custom field in property record (if available) | When grade is calculated | Manual; optional but recommended for trend tracking |
| Listed Date | Vacancy / marketing record | When listing goes live | Manual; coordinator confirms in both systems |

#### Zapier Automation Options (If You Want to Reduce Manual Entry)
If you're on AppFolio, Buildium, or Rentvine, some of these syncs can be automated via Zapier, reducing double-entry and human error.

| Zap | Trigger | Action |
|---|---|---|
| New Notice to Vacate | New notice logged in PM software | Auto-create row on the board at Stage 1 with address, owner, move-out date pre-filled |
| Work Order Closed | Work order marked complete in PM software | Notify coordinator on the board that work order is done; prompt to confirm Stage 4 progress |
| Invoice Posted | Vendor invoice approved in PM software | Update Make-Ready Actual cost column on the board |
| Listing Goes Live | Unit marked available/listed in PM software | Update Listed Date on the board; trigger grade calculation |

Reality check: not all PM software has full Zapier support for every trigger. AppFolio has the strongest integration options. Buildium is more limited. Check your PM software's Zapier integration page before building these, but even 1 to 2 automated syncs will save your coordinator significant time across 420 doors.
#### The Data Rhythm: What Gets Updated When

| Timing | Who | What They Update |
|---|---|---|
| Same day notice received | Coordinator | Create row; enter address, class, owner, move-out date, monthly rent |
| After pre-move-out inspection | Coordinator | Log inspection date; enter preliminary scope notes |
| After move-out inspection | Coordinator | Log inspection date; enter damage chargeback amount; enter make-ready budget estimate |
| As vendor invoices come in | Coordinator | Enter each cost line item; update Make-Ready Actual total |
| After final inspection | Coordinator | Log inspection date and result; update stage |
| After photos approved | Coordinator | Log photos completed date; paste listing link |
| When unit goes live | Coordinator | Enter Listed Date; board auto-calculates turn-time and grade |
| End of month | Coordinator / PM Lead | Move all Stage 8 completed rows to Archive group; export for Monthly Performance Report |

### Complete System Summary

---
Everything the design covers, consistent across every companion document:

| Component | Status |
|---|---|
| 8 Turnover Stages, Notice to Listed | Done |
| Full Column Set: identifiers, dates, turn-time, budget, grades, docs | Done |
| Status Values and Color Logic: stage, turn-time, budget | Done |
| Stage Ownership Map: coordinator, tech, vendor, PM Lead | Done |
| Class-Based Turn-Time Targets: B/C/D with Green/Yellow/Red thresholds | Done |
| Automations: reminders, owner emails, escalations, stage transitions | Done |
| Coordinator View: Kanban, filtered to their units, Red/Yellow first | Done |
| Leadership View: full portfolio table + dashboard with 10 widgets | Done |
| Owner View: automated email sequence tied to stage completions | Done |
| Reference Build Guide: 5 phases, 16 steps, Monday.com specific | Done |
| PM Software Data Feed: what to pull, what to push, Zapier options | Done |

### Manager Notes

---
Build the board before you enter a single real unit. Run a full fake test turnover through all 8 stages first; confirm every automation fires, every formula calculates, every email sends correctly. Fix issues in test before they affect a real owner.
Your coordinator is the engine of this board. The system only works if stage updates happen same-day. Set the expectation on Day 1: the board is updated in real time, not at the end of the week. A stale board is worse than no board.
Start with the 3-day stall automation as your most important escalation. At 420 doors, things will fall through cracks. A unit that hasn't been touched in 3 days is a vacancy cost problem waiting to happen. That automation is your net.
The Leadership Dashboard is your Monday morning meeting. Pull it up, look at every Red unit, assign an action item, move on. 15 minutes. That's the cadence.
Don't try to replace your PM software with this board. They do different jobs. PM software = leases, money, compliance. Tracking board = workflow, performance, accountability. Keep them separate and connected.
[Company Name] - internal operations document. Use only the companion files that ship in this turnover library.
