---
title: "Occupied Unit Maintenance Board"
source: "PMAgents source library, owner-reviewed"
converted: 2026-08-19
google_doc_id: 1Ltgw3M8n0_IEiol85Y0g9bp81iCdvdi7CxdFhRfrkdI
google_doc_url: https://docs.google.com/document/d/1Ltgw3M8n0_IEiol85Y0g9bp81iCdvdi7CxdFhRfrkdI/edit
library_folder: 1QDyp_rF5syRtdM_XR3TAhT4CbXhdSoOg
audience: all agents
status: reference
---

# Occupied Unit Maintenance Board

## Occupied Unit Maintenance Board
Stages, columns, SLA clocks, automations, views and the weekly KPI dashboard, [Company Name]
The board that runs the occupied unit maintenance workflow. Part 1 is the card path and what the board adds at each stage. Part 2 is every column and status with its color. Part 3 is the priority based SLA clocks and how they run. Part 4 is the six automation groups. Part 5 is the three role based views. Part 6 is the weekly leadership KPI dashboard and how to run the Monday review. The closing Tool Notes collect the platform specific notes in one place.
---
Tool-agnostic by design (owner-reviewed, 2026-08-19): the body assumes a generic maintenance platform and a generic accounting system; vendor-specific notes are collected in the closing Tool Notes section. The current installation mapping (the maintenance platform as the operating system, the accounting system as the money record) is a separate short note in the library.
### Part 1: Stages (Card Path)
---
Standard path: Intake, then Triage, then Owner Hold (conditional), then Dispatched, then In Progress, then Pending Inspection, then Closed.
After-Hours Fork (from Intake): Intake, then After-Hours Emergency, then Dispatched, then In Progress, then Pending Inspection, then Closed.
Owner Hold only fires when the cost exceeds the pre-approved threshold (typically $500).
#### What the Board Adds at Each Stage
#### 1. Intake
- Intake timestamp (SLA clock starts here)
- Priority tag auto-applied: Emergency / Urgent / Routine
- Tenant acknowledgment auto-sent (portal or SMS)
- Photo/video attachment field required before card advances
#### 2. Triage
- Phone troubleshoot checklist (breaker? user error? tenant-caused?), prevents unnecessary dispatch
- Tenant responsibility flag (issues under $25: tenant handles per lease)
- Scope-of-work field locked until complete
- Route decision: standard path vs. After-Hours Emergency fork
#### 3. Owner Hold (conditional)
- Auto-notification to owner with bid/estimate attached
- 24-hour approval timer with escalation reminder
- Card is blocked from advancing until approval is logged
- Denial path: card moves to Closed, Declined
#### 4. After-Hours Emergency (fork)
- Emergency vendor list auto-surfaced (on-call, pre-approved)
- Bypass owner approval for life-safety issues (flooding, no heat, gas)
- Auto-log of after-hours dispatch cost for owner morning summary
- Tenant safety confirmation field required
#### 5. Dispatched
- Vendor assigned from pre-approved list (by trade plus availability)
- Access instructions pushed to vendor (tenant contact, lockbox code)
- Tenant notified: vendor name, appointment window
- Scope of work plus deadline locked to card
#### 6. In Progress
- Vendor check-in timestamp
- Mid-point status update sent to tenant if job exceeds 1 day
- Vendor access log (entered/exited unit)
- Completion photo upload required before card can advance
#### 7. Pending Inspection
- PM spot-check checklist (photos reviewed, scope confirmed complete)
- Tenant satisfaction survey auto-sent (24 hrs post-completion)
- Invoice matched to work order, flags mismatches before payment
- Dissatisfaction response: card re-opens to In Progress
#### 8. Closed
- Invoice posted to owner statement (accounting system handles payment)
- Satisfaction score logged to tenant record
- Work order archived with full photo/doc trail
- Monthly audit flag if pattern detected (same unit, same issue)
### Part 2: Columns and Statuses
#### Card Columns (Every Field)
Eight column groups. Every card carries every field; the views in Part 5 decide who sees which.
#### Unit and Property Identity

| Column | Values / Format | Notes |
|---|---|---|
| Unit ID | Text, e.g. 123 Oak St #4B | Primary card title |
| Property Class | Single-Family / Multi-Family / Condo / Commercial | Drives vendor routing rules |
| Owner Name | Linked record | Pulls approval threshold plus contact |
| Tenant Name | Linked record | Pulls lease status plus contact |

#### Classification

| Column | Values / Format | Notes |
|---|---|---|
| Priority | Emergency / Urgent / Routine | Sets SLA clock on intake |
| Category | Plumbing / HVAC / Electrical / Appliance / Structural / Pest / Cosmetic / Other | Drives vendor trade match |
| Source | Tenant Portal / Phone / After-Hours Line / Inspection / Owner | Audit trail |
| After-Hours Flag | Yes / No | Triggers after-hours fork |
| Recurring Flag | Yes / No | Set if same issue on same unit within 90 days |
| Callback Flag | Yes / No | Set if tenant reports issue unresolved post-close |

#### Assignment

| Column | Values / Format | Notes |
|---|---|---|
| Assigned Tech / Vendor | Linked record from vendor roster | Filtered by trade plus availability |
| Vendor Trade | Plumber / Electrician / HVAC Tech / Handyman / Specialist | Auto-suggested from Category |
| Internal Coordinator | Staff member | Owns the card from intake to close |

#### Key Timestamps

| Column | Format | Set By |
|---|---|---|
| Intake Date/Time | Date plus Time | Auto on card creation |
| Triage Completed | Date plus Time | Manual or stage trigger |
| Owner Notified | Date plus Time | Auto when Owner Hold stage entered |
| Owner Approved | Date plus Time | Manual when approval logged |
| Dispatched | Date plus Time | Auto when vendor assigned |
| Work Started | Date plus Time | Vendor check-in log |
| Work Completed | Date plus Time | Vendor completion plus photo upload |
| Closed | Date plus Time | Auto when card moves to Closed |

#### SLA Clocks
See Part 3 for the full SLA table and color logic.

| Column | Format | Notes |
|---|---|---|
| SLA Deadline | Calculated Date/Time | Intake plus SLA window by priority |
| Time to Dispatch | Duration (hrs) | Intake to Dispatched |
| Time to Complete | Duration (hrs/days) | Intake to Work Completed |
| SLA Status | On Track / At Risk / Breached | Auto-calculated, color-coded Green / Yellow / Red |
| SLA Breach Reason | Text | Required if card closes in Red (Breached) |

#### Owner Approval State

| Column | Values | Notes |
|---|---|---|
| Approval Required | Yes / No | Auto-set when estimated cost is over $500 |
| Estimated Cost | Currency | Entered at Triage |
| Approval State | Pending / Approved / Declined / Escalated | Drives Owner Hold stage |
| Approval Deadline | Date plus Time | Intake plus 24 hrs; auto-reminder fires at 12 hrs |

#### Special Flags

| Column | Values | Notes |
|---|---|---|
| Warranty Flag | In Warranty / No | Blocks standard vendor; routes to warranty contact |
| Warranty Expiry | Date | Pulled from appliance/system record |
| Tenant Damage Flag | Yes / No | Triggers cost recovery plus security deposit note |
| Tenant Responsibility | Yes / No | Set at Triage if issue is under $25 or tenant-caused |

#### Cost and Invoice

| Column | Values / Format | Notes |
|---|---|---|
| Estimated Cost | Currency | Set at Triage |
| Actual Cost | Currency | Entered on invoice receipt |
| Cost Variance | Auto-calculated | Flags if actual exceeds estimated by more than 15% |
| Charged To | Owner / Tenant / Warranty / Insurance | Determines accounting routing |
| Invoice State | Not Received / Received / Matched / Mismatch / Posted | See Invoice State Colors below |
| Invoice Number | Text | Vendor invoice reference |
| Posted to Statement | Yes / No | Confirmed by accounting system |

#### Status Values with Colors

| Status | Color | Meaning |
|---|---|---|
| New | White | Card created, not yet triaged |
| In Triage | Blue | Coordinator reviewing, troubleshooting with tenant |
| Owner Hold | Orange | Awaiting owner approval to proceed |
| Approval Declined | Dark Gray | Owner declined; card moving to close |
| Dispatched | Purple | Vendor assigned, appointment set |
| In Progress | Yellow | Vendor on site or work underway |
| Pending Inspection | Teal | Work done; PM review plus tenant survey pending |
| Callback Open | Red | Tenant reported issue unresolved after close |
| Closed, Resolved | Green | Fully complete, invoice posted |
| Closed, Declined | Dark Gray | Owner declined or tenant responsible |
| Closed, Duplicate | Light Gray | Merged into another card |

#### Invoice State Colors
Sub-status on the cost section.

| Invoice State | Color |
|---|---|
| Not Received | Gray |
| Received | Blue |
| Matched | Green |
| Mismatch | Orange |
| Posted | Teal |

### Part 3: Priority Based SLA Clocks with Color Triggers
#### SLA Table

| Priority | Definition | Acknowledge | Dispatch | Complete | Yellow Warning | Red Breach |
|---|---|---|---|---|---|---|
| Emergency | Flooding, gas leak, no heat in winter, no AC in extreme heat, security breach | Immediate (auto-reply fires) | Within 2 hrs | Within 4 hrs | 75% of window elapsed | Deadline hit |
| Urgent | Broken appliance, no hot water, HVAC not cooling (mild weather) | Within 1 hr | Within 4 hrs | Within 24 to 48 hrs | 60% of window elapsed | Deadline hit |
| Routine | Cosmetic, dripping faucet, minor repairs | Within 24 hrs | Within 48 hrs | 7 to 10 days | 50% of window elapsed | Deadline hit |

#### SLA Clock Color Logic (Per Card)

| SLA Status | Color | Condition | Action |
|---|---|---|---|
| On Track | Green | Card is within the green window | No action required |
| At Risk | Yellow | Emergency: more than 3 hrs elapsed with no dispatch. Urgent: more than 29 hrs elapsed with no completion. Routine: more than 5 days elapsed with no completion | Auto-alert fires to coordinator |
| Breached | Red | Emergency: more than 4 hrs with no completion. Urgent: more than 48 hrs with no completion. Routine: more than 10 days with no completion | Auto-escalation fires to PM or Ops Manager. Card header turns red on board view. SLA Breach Reason field becomes required before close |

#### How the Clock Runs

| Event | Rule |
|---|---|
| Clock starts | Intake Date/Time (auto) |
| Clock pauses | When card enters Owner Hold (owner response time does not burn your SLA) |
| Clock resumes | When Approval State = Approved or Declined |
| Clock stops | When Work Completed timestamp is logged |
| Breach logged | If clock stops AFTER SLA Deadline |

---
Pause rule: the SLA clock pauses the moment a card enters Owner Hold and resumes when the owner approves or declines. Owner response time never counts against the coordinator or the vendor.
### Part 4: Automations (Six Groups)
Six automation groups: R (resident acknowledgements), V (vendor and tech nudges), O (owner approval reminders), E (escalations to the PM), T (stage transitions), C (30 day callback watch). Each row is a trigger, the action, who receives it, and when it fires. Message copy is the starting wording; the platform templates carry the final text.
#### Group 1: Resident Acknowledgements (R1 to R10)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| R1 | Card created (any priority) | Send SMS plus portal message: "We received your request for [Unit]. Your work order # is [ID]. We will be in touch shortly." | Tenant | Immediately on intake |
| R2 | Card created, Priority = Emergency | Send SMS: "This is being treated as an emergency. Our team is on it now." | Tenant | Immediately on intake |
| R3 | Card created, After-Hours Flag = Yes | Send SMS: "We have received your after-hours request. An on-call vendor is being contacted. Expect a follow-up by [time]." | Tenant | Immediately on intake |
| R4 | Tenant Responsibility Flag set = Yes | Send portal message plus email: "After reviewing your request, this falls under resident responsibility per your lease (items under $25). Here is how to resolve it: [link]." | Tenant | Immediately on flag set |
| R5 | Stage moves to Dispatched | Send SMS plus portal: "Good news, your repair is scheduled. A vendor will arrive [date/window]. You do not need to be present." | Tenant | Immediately on stage change |
| R6 | Vendor check-in timestamp logged (Work Started) | Send SMS: "Your vendor has arrived at the property and work has begun." | Tenant | Immediately on timestamp |
| R7 | Work Completed timestamp logged | Send SMS plus portal: "Work on your request is complete. We will follow up shortly to make sure everything looks good." | Tenant | Immediately on timestamp |
| R8 | Card moves to Pending Inspection | Send satisfaction survey via portal/email: "How did we do? Rate your recent maintenance experience." | Tenant | 24 hrs after Work Completed |
| R9 | Survey score = low (below threshold) | Send email: "We are sorry the experience fell short. A team member will reach out within 24 hours." Plus flag card for Callback | Tenant plus Coordinator | Immediately on survey submit |
| R10 | Card moves to Closed, Resolved | Send portal message: "Your work order [ID] is officially closed. Thank you for your patience." | Tenant | Immediately on stage change |

#### Group 2: Vendor and Tech Nudges (V1 to V9)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| V1 | Vendor assigned (Dispatched stage entered) | Send work order details via email/SMS: scope of work, unit address, tenant contact, access instructions, deadline | Assigned Vendor / Tech | Immediately on assignment |
| V2 | Priority = Emergency plus no vendor check-in logged | Send SMS nudge: "Emergency WO [ID]: please confirm you are en route to [Unit]." | Assigned Vendor / Tech | 30 mins after dispatch |
| V3 | Priority = Emergency plus no vendor check-in logged | Send second SMS nudge plus alert Coordinator | Assigned Vendor / Tech plus Coordinator | 1 hr after dispatch |
| V4 | Priority = Urgent plus no vendor check-in logged | Send SMS nudge: "Reminder: WO [ID] is due within 24 to 48 hrs. Please confirm your scheduled time." | Assigned Vendor / Tech | 12 hrs after dispatch |
| V5 | Priority = Routine plus no vendor check-in logged | Send email nudge: "WO [ID] is scheduled. Please confirm your appointment window." | Assigned Vendor / Tech | 48 hrs after dispatch |
| V6 | SLA Status flips to At Risk plus no completion | Send SMS: "WO [ID] is approaching its deadline. Please update status or confirm ETA." | Assigned Vendor / Tech | Immediately on SLA flip |
| V7 | Work Completed timestamp logged plus no completion photos uploaded | Send SMS: "Please upload completion photos for WO [ID] before this order can be closed." | Assigned Vendor / Tech | 2 hrs after Work Completed logged |
| V8 | Invoice not received within window after Work Completed | Send email: "Please submit your invoice for WO [ID] to [billing contact]." | Assigned Vendor / Tech | 48 hrs after Work Completed |
| V9 | Invoice State = Mismatch | Send email: "Invoice for WO [ID] does not match the approved estimate. Please review and resubmit." | Assigned Vendor / Tech plus Coordinator | Immediately on mismatch flag |

#### Group 3: Owner Approval Reminders (O1 to O8)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| O1 | Estimated Cost over $500 plus card enters Triage | Set Approval Required = Yes and move card to Owner Hold | System (auto) | Immediately on cost entry |
| O2 | Card enters Owner Hold | Send email plus portal notification: "Your approval is needed for WO [ID] at [Unit]. Estimated cost: $[X]. Scope: [summary]. Please approve or decline by [deadline]." Plus attach photos/bid | Owner | Immediately on stage entry |
| O3 | Approval not received within 12 hrs | Send SMS reminder: "Reminder: WO [ID] awaiting your approval. Deadline: [time]. Reply or log in to approve." | Owner | 12 hrs after O2 |
| O4 | Approval not received within 24 hrs | Send final email plus SMS: "Final reminder: WO [ID] approval deadline has been reached. We will proceed per your management agreement." Plus alert Coordinator | Owner plus Coordinator | 24 hrs after O2 |
| O5 | Approval State = Approved | Move card to Dispatched plus notify Coordinator to assign vendor | System (auto) plus Coordinator | Immediately on approval |
| O6 | Approval State = Declined | Move card to Closed, Declined plus send email to owner confirming decline plus notify tenant of delay | System (auto) plus Owner plus Tenant | Immediately on decline |
| O7 | After-Hours Emergency dispatched (life-safety bypass) | Send owner morning summary email: "An after-hours emergency was handled overnight at [Unit]. Vendor: [name]. Issue: [summary]. Estimated cost: $[X]. Full report attached." | Owner | Next business day at 8:00 AM |
| O8 | Work Completed plus invoice posted to statement | Send email: "WO [ID] at [Unit] is complete and has been posted to your owner statement. Cost: $[X]." | Owner | Immediately on invoice posted |

#### Group 4: Escalations to the PM (E1 to E8)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| E1 | Priority = Emergency plus no dispatch within 2 hrs | Send chat/SMS alert: "Emergency WO [ID] at [Unit] has not been dispatched. Immediate action required." | Property Manager | 2 hrs after intake |
| E2 | SLA Status flips to Breached (any priority) | Send chat/SMS alert: "SLA Breached: WO [ID] at [Unit] ([Priority]). Breach reason required before close." Plus card header turns red on board | Property Manager plus Coordinator | Immediately on SLA breach |
| E3 | Owner unresponsive after 24 hrs (O4 fired, no response) | Alert PM: "Owner [name] has not approved WO [ID] after 24 hrs. Please intervene or proceed per management agreement." | Property Manager | Immediately after O4 fires |
| E4 | Tenant survey score = low AND Callback Flag = Yes | Alert PM: "Tenant at [Unit] reported dissatisfaction on WO [ID]. Callback flag is open. Please review within 24 hrs." | Property Manager | Immediately on flag combo |
| E5 | Recurring Flag = Yes (same issue, same unit, within 90 days) | Alert PM: "Recurring issue detected at [Unit]: [Category]. This is the [2nd/3rd] occurrence in 90 days. Review for root cause." | Property Manager | Immediately on flag set |
| E6 | Invoice State = Mismatch plus unresolved after 48 hrs | Alert PM: "Invoice mismatch on WO [ID] unresolved after 48 hrs. Vendor has been notified. Please review." | Property Manager | 48 hrs after V9 fires |
| E7 | Tenant Damage Flag = Yes plus card moves to Closed | Alert PM: "WO [ID] closed with Tenant Damage flag. Cost recovery and security deposit note required before final close." | Property Manager plus Accounting | Immediately on stage change |
| E8 | Warranty Flag = Yes plus standard vendor assigned in error | Alert PM plus Coordinator: "WO [ID] has an active warranty. Standard vendor assignment blocked. Route to warranty contact." | Property Manager plus Coordinator | Immediately on vendor assignment |

#### Group 5: Stage Transitions (T1 to T11)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| T1 | Card created | Auto-set: Priority tag, SLA Deadline, SLA clock starts, Intake timestamp logged | System (auto) | Immediately on creation |
| T2 | Triage checklist complete plus no approval required | Auto-move card to Dispatched | System (auto) | Immediately on checklist complete |
| T3 | Triage checklist complete plus Estimated Cost over $500 | Auto-move card to Owner Hold plus set Approval Required = Yes | System (auto) | Immediately on cost entry |
| T4 | Approval State = Approved | Auto-move card to Dispatched plus SLA clock resumes | System (auto) | Immediately on approval |
| T5 | Approval State = Declined | Auto-move card to Closed, Declined plus SLA clock stops | System (auto) | Immediately on decline |
| T6 | Vendor assigned plus appointment confirmed | Auto-move card to Dispatched (if not already) plus log Dispatched timestamp | System (auto) | Immediately on vendor assignment |
| T7 | Vendor check-in timestamp logged | Auto-move card to In Progress plus log Work Started timestamp | System (auto) | Immediately on check-in |
| T8 | Completion photos uploaded plus Work Completed timestamp logged | Auto-move card to Pending Inspection | System (auto) | Immediately on both conditions met |
| T9 | PM inspection confirmed plus survey sent | Hold card in Pending Inspection until survey response OR 72 hrs elapsed | System (auto) | 72-hr timeout if no survey response |
| T10 | Survey received (any score) plus invoice = Matched plus PM inspection = Yes | Auto-move card to Closed, Resolved plus log Closed timestamp plus stop SLA clock | System (auto) | Immediately on all three conditions met |
| T11 | Callback Flag set = Yes on a Closed card | Auto-reopen card to Callback Open status plus notify Coordinator plus PM | System (auto) | Immediately on flag set |

#### Group 6: 30 Day Callback Watch (C1 to C7)

| # | Trigger | Action | Recipient | Timing |
|---|---|---|---|---|
| C1 | Card moves to Closed, Resolved | Start 30-day callback watch timer on unit | System (auto) | Immediately on close |
| C2 | 30-day timer active plus new card created for same unit plus same Category | Auto-set Recurring Flag = Yes on new card plus alert Coordinator: "This is a repeat issue at [Unit] within 30 days." | Coordinator | Immediately on new card creation |
| C3 | 30-day timer active plus tenant contacts office about same issue | Coordinator manually sets Callback Flag = Yes on closed card, which auto-reopens to Callback Open | Coordinator (manual trigger) | On tenant contact |
| C4 | Card status = Callback Open for more than 24 hrs with no action | Alert PM: "Callback WO [ID] at [Unit] has been open 24 hrs with no coordinator action." | Property Manager | 24 hrs after C3 |
| C5 | Callback resolved plus Work Completed re-logged | Auto-move card to Pending Inspection (second pass) plus send new satisfaction survey to tenant | Tenant | Immediately on re-completion |
| C6 | 30-day timer expires with no callback or recurring flag | Clear watch timer plus log "No callback, 30-day watch closed clean" to card record | System (auto) | 30 days after original close |
| C7 | Same unit triggers Recurring Flag 3 or more times in 90 days | Alert PM plus flag unit for root cause inspection: "[Unit] has had [3] recurring [Category] issues in 90 days. Recommend full inspection." | Property Manager | Immediately on 3rd flag |

### Part 5: Three Role Based Views
The same board, three lenses. The coordinator view is the working queue, the leadership view is oversight, and the owner view is read-only and limited to the owner's own properties.
#### View 1: Coordinator View
The working board. Everything needed to triage, dispatch, track, and close, nothing extra.
Default filters (on load)

| Filter | Setting |
|---|---|
| Assigned Coordinator | = Current user (me) |
| Status | Not Closed, Resolved / Closed, Declined / Closed, Duplicate |
| Date Range | Rolling 60 days |

Coordinator sees only their own open queue by default. Can manually remove the coordinator filter to view the team queue if needed.
Columns visible in this view

| Column | Why It Is Here |
|---|---|
| Unit ID | Primary identifier |
| Tenant Name | Direct contact reference |
| Priority | Emergency / Urgent / Routine, drives daily triage order |
| Category | Trade routing reference |
| Status | Current stage at a glance |
| SLA Status | On Track / At Risk / Breached, the coordinator's daily health check |
| SLA Deadline | Exact deadline visible at all times |
| Assigned Vendor / Tech | Who owns the field work |
| Intake Date/Time | Age of card |
| After-Hours Flag | Flags cards that bypassed normal intake |
| Recurring Flag | Flags repeat issues needing extra attention |
| Callback Flag | Flags reopened cards |
| Approval Required | Quick check before dispatching |
| Approval State | Pending / Approved / Declined, unblocks dispatch |
| Work Completed | Confirms field work done |
| Invoice State | Not Received / Received / Matched / Mismatch / Posted, tracks billing close-out |
| Internal Notes | Coordinator working notes |

Grouped by, default sort
1. Callback Open
2. Emergency (by SLA Deadline ascending)
3. Urgent (by SLA Deadline ascending)
4. Owner Hold (by Approval Deadline ascending)
5. Dispatched (by SLA Deadline ascending)
6. In Progress (by Work Started ascending)
7. Pending Inspection (by Work Completed ascending)
8. Routine (by Intake Date ascending)
Saved filter shortcuts (coordinator quick views)

| Filter Name | Logic |
|---|---|
| Needs Action Now | SLA Status = Breached OR Priority = Emergency AND Status = New/In Triage |
| Awaiting Owner | Status = Owner Hold AND Approval Deadline is less than 4 hrs from now |
| Needs Dispatch | Status = In Triage AND Approval Required = No AND Vendor = Blank |
| Missing Photos | Work Completed is not blank AND Completion Photos = Not Uploaded |
| Invoice Queue | Invoice State = Not Received AND Work Completed more than 48 hrs ago |
| Callbacks and Recurring | Callback Flag = Yes OR Recurring Flag = Yes |
| Today's Appointments | Dispatched AND Vendor Appointment Date = Today |

Columns hidden in this view: Owner Name financial details beyond Estimated Cost, Actual Cost variance reporting, portfolio-level aggregates, coordinator performance metrics. Those live in the Leadership View only.
#### View 2: Leadership View
The oversight board. Portfolio-wide visibility, SLA health, team performance, vendor accountability, and cost control, no card-level noise.
Default filters (on load)

| Filter | Setting |
|---|---|
| Assigned Coordinator | All (no filter) |
| Status | All active statuses (excludes Closed, Duplicate) |
| Date Range | Rolling 30 days |

Columns visible in this view

| Column | Why It Is Here |
|---|---|
| Unit ID | Property reference |
| Owner Name | Owner accountability layer |
| Priority | Portfolio-wide priority distribution |
| Category | Identifies systemic trade issues |
| Status | Stage distribution across portfolio |
| SLA Status | On Track / At Risk / Breached, portfolio health at a glance |
| SLA Deadline | Breach risk identification |
| SLA Breach Reason | Required on all Breached closed cards, pattern analysis |
| Assigned Coordinator | Team workload distribution |
| Assigned Vendor / Tech | Vendor performance tracking |
| Intake Date/Time | Card age / aging queue |
| Work Completed | Completion tracking |
| Time to Dispatch | Speed metric (hrs) |
| Time to Complete | Resolution metric (hrs/days) |
| Estimated Cost | Budget visibility |
| Actual Cost | Spend tracking |
| Cost Variance | Flags budget overruns |
| Charged To | Owner / Tenant / Warranty / Insurance split |
| Invoice State | Portfolio-wide billing close-out health |
| Recurring Flag | Systemic property issues |
| Callback Flag | Quality control signal |
| Tenant Damage Flag | Cost recovery tracking |
| Warranty Flag | Warranty utilization tracking |

Grouped by, default sort
- Primary group: SLA Status (Breached, then At Risk, then On Track)
- Secondary sort: Priority (Emergency, then Urgent, then Routine)
- Tertiary sort: Intake Date ascending (oldest first within each group)
Saved filter shortcuts (leadership quick views)

| Filter Name | Logic |
|---|---|
| Breach Report | SLA Status = Breached, all open plus closed this week |
| Cost Overruns | Cost Variance over 15% AND Actual Cost is not blank |
| Recurring Issues | Recurring Flag = Yes, grouped by Unit ID |
| Vendor Performance | Group by Assigned Vendor, sort by Callback Flag count plus SLA Breach count |
| Owner Hold Aging | Status = Owner Hold AND Approval Deadline more than 24 hrs ago |
| Invoice Backlog | Invoice State = Not Received OR Mismatch AND Work Completed more than 72 hrs ago |
| Coordinator Workload | Group by Assigned Coordinator, count of open cards by SLA Status |
| Property Deep Dive | Filter by Unit ID or Owner Name, full card history rolling 90 days |

Columns hidden in this view: Tenant contact details, access instructions, lockbox codes, internal coordinator working notes. Operational detail that belongs in the Coordinator View only.
#### View 3: Owner View
Read-only. Their properties only. Transparent, professional, no internal operational detail.
Default filters (on load, locked, cannot be changed by owner)

| Filter | Setting |
|---|---|
| Owner Name | = Logged-in owner (hard-locked) |
| Status | All (including closed, rolling 12 months) |
| Date Range | Rolling 12 months |

Columns visible in this view

| Column | What the Owner Sees |
|---|---|
| Unit ID | Their property address / unit |
| Issue Summary | Plain-language description of the work order |
| Priority | Emergency / Urgent / Routine |
| Status | Current stage in plain language (no internal jargon) |
| Submitted Date | When the request came in |
| Vendor / Trade | Who is doing the work (trade name only, no contact info) |
| Scheduled Date | When vendor is going out |
| Work Completed Date | When work was finished |
| Estimated Cost | Pre-approved estimate |
| Actual Cost | Final cost (visible only after invoice posted) |
| Charged To | Owner / Tenant / Warranty / Insurance |
| Approval Required | Yes / No |
| Approval State | Pending / Approved / Declined |
| Approve / Decline Button | One-click action (visible only when Approval State = Pending) |
| Invoice / Receipt | Downloadable attachment (visible after invoice posted) |
| Before / After Photos | Downloadable (visible after Work Completed) |
| Completion Notes | Brief summary of work done |

Grouped by, default sort
1. Awaiting Your Approval (Approval State = Pending)
2. Active, Emergency
3. Active, Urgent
4. Active, Routine
5. Completed (last 12 months, newest first)
Columns and data permanently hidden from the Owner View

| Hidden Item | Reason |
|---|---|
| Tenant Name / Contact | Tenant privacy |
| Access instructions / lockbox codes | Security |
| Internal coordinator notes | Operational, not owner-facing |
| SLA Status / SLA Deadline | Internal metric, not client-facing |
| Assigned Coordinator name | Internal staffing detail |
| Cost Variance | Internal accounting flag |
| Recurring / Callback / Damage flags | Internal quality control signals |
| Invoice State (internal stages) | Replaced by clean receipt download |
| Vendor contact info | All vendor comms stay in-house |

### Part 6: Weekly Leadership KPI Dashboard
Reviewed every Monday morning. Covers the prior 7-day rolling window unless noted. Each KPI has a target, a Watch band (Yellow) and an Act band (Red).
#### Section A: SLA and Response Performance

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Emergency Dispatch Rate | % of Emergency WOs dispatched within 2 hrs of intake | 95% or higher | 90 to 94% | Under 90% |
| Emergency Completion Rate | % of Emergency WOs completed within 4 hrs of intake | 90% or higher | 85 to 89% | Under 85% |
| Urgent Completion Rate | % of Urgent WOs completed within 48 hrs | 92% or higher | 87 to 91% | Under 87% |
| Routine Completion Rate | % of Routine WOs completed within 10 days | 95% or higher | 90 to 94% | Under 90% |
| Overall SLA Breach Rate | % of all WOs closed with SLA Status = Breached | 3% or lower | 4 to 6% | Over 6% |
| Avg. Time to Dispatch | Mean hrs from Intake to Dispatched timestamp (all priorities) | 3 hrs or less | 3 to 5 hrs | Over 5 hrs |
| Avg. Time to Complete | Mean days from Intake to Work Completed (Routine only) | 7 days or less | 7 to 9 days | Over 9 days |

#### Section B: Quality and Callback Control

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Callback Rate | % of closed WOs reopened via Callback Flag within 30 days | 5% or lower | 6 to 9% | Over 9% |
| Recurring Issue Rate | % of WOs with Recurring Flag = Yes (same unit, same category, 90 days) | 4% or lower | 5 to 7% | Over 7% |
| Tenant Satisfaction Score | Avg. post-completion survey score (1 to 5 scale) | 4.3 or higher | 4.0 to 4.2 | Under 4.0 |
| Survey Response Rate | % of closed WOs where tenant completed satisfaction survey | 60% or higher | 45 to 59% | Under 45% |
| Low Score Rate | % of surveys returned below threshold (under 3 out of 5) | 5% or lower | 6 to 9% | Over 9% |

#### Section C: Vendor Accountability

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Vendor On-Time Rate | % of vendor appointments where check-in logged within scheduled window | 90% or higher | 85 to 89% | Under 85% |
| Completion Photo Compliance | % of completed WOs with photos uploaded before close | 100% | 95 to 99% | Under 95% |
| Invoice Submission Rate | % of invoices received within 48 hrs of Work Completed | 90% or higher | 80 to 89% | Under 80% |
| Invoice Mismatch Rate | % of invoices flagged as Mismatch vs. total invoices received | 5% or lower | 6 to 9% | Over 9% |
| Vendor Callback Rate | % of WOs per vendor that triggered a Callback Flag (by vendor) | 5% or lower per vendor | 6 to 9% | Over 9%, vendor review triggered |

#### Section D: Cost Control

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Cost Variance Rate | % of WOs where Actual Cost exceeded Estimate by more than 15% | 8% or lower | 9 to 12% | Over 12% |
| Avg. Cost per WO, Routine | Mean actual cost of Routine WOs closed this week | Benchmark set at 90-day rolling avg | +10% over avg | +20% over avg |
| Avg. Cost per WO, Urgent | Mean actual cost of Urgent WOs closed this week | Benchmark set at 90-day rolling avg | +10% over avg | +20% over avg |
| Tenant Damage Recovery Rate | % of WOs with Tenant Damage Flag where cost recovery was initiated | 100% | None | Any miss = act |
| Warranty Utilization Rate | % of WOs with active warranty where warranty vendor was used (not standard vendor) | 100% | None | Any miss = act |
| Invoice Posting Lag | Avg. days from Work Completed to Invoice Posted to owner statement | 5 days or less | 6 to 8 days | Over 8 days |

#### Section E: Owner Approval Health

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Owner Response Rate | % of approval requests answered within 24 hrs | 90% or higher | 80 to 89% | Under 80% |
| Owner Hold Aging | Number of cards in Owner Hold status more than 24 hrs with no response | 0 | 1 to 2 | 3 or more |
| Approval Decline Rate | % of approval requests declined by owner | 10% or lower | 11 to 15% | Over 15%, review scope/estimate process |
| After-Hours Owner Summary Rate | % of after-hours emergency WOs where owner morning summary was sent by 8 AM | 100% | None | Any miss = act |

#### Section F: Team and Coordinator Performance

| KPI | Definition | Target | Watch (Yellow) | Act (Red) |
|---|---|---|---|---|
| Open Queue per Coordinator | Number of active (non-closed) WOs assigned per coordinator | 40 or fewer | 41 to 55 | Over 55, capacity review |
| Triage Completion Time | Avg. hrs from Intake to Triage Completed timestamp | 2 hrs or less | 2 to 4 hrs | Over 4 hrs |
| Cards Closed This Week | Total WOs moved to Closed, Resolved in rolling 7 days | Benchmark vs. prior 4-week avg | 10% below avg | 20% below avg |
| SLA Breach Reason Compliance | % of Breached closed cards with Breach Reason field completed | 100% | None | Any miss = act |
| Escalation Volume | Number of E-series escalation alerts fired to PM this week | 3 or fewer | 4 to 6 | Over 6, process review |

#### How to Run the Weekly Review
---
Monday morning, 15 minute leadership pull.
1. Step 1: Open Leadership View, then the Breach Report filter. Review all Breached cards from the prior week and confirm Breach Reason is logged on every one.
2. Step 2: Pull Section A plus B KPIs from the maintenance platform report. Flag any metric in Watch (Yellow) or Act (Red).
3. Step 3: Pull Section C, sort by Vendor Callback Rate. Any vendor over 9% goes on the watch list for quarterly review.
4. Step 4: Pull Section D, Cost Variance Rate. Any WO with more than 15% variance gets PM review before the invoice posts.
5. Step 5: Pull Section E, Owner Hold Aging filter. Any card more than 24 hrs unresponded gets a PM phone call the same day.
6. Step 6: Pull Section F, Open Queue per Coordinator. Rebalance assignments if any coordinator is over 55 open cards.
7. Step 7: Log the weekly KPI snapshot to the scorecard. Compare to the prior 4-week rolling average and flag trends (3 consecutive weeks in Watch = process review).
### Tool Notes
Platform specific notes collected from every part of the board. The body above stays tool-agnostic; these are the vendor fits identified in the source material.
#### Stages
- Your PM software (the work-order platform): best fit for portal intake, SLA timestamps, owner approval workflows, and invoice-to-statement posting.
- Latchel / Vendor on Call: purpose-built for the After-Hours Emergency fork; handles on-call dispatch and tenant triage calls so your team is not on the phone at 2am.
- Vendor management (e.g. Thumbtack Pro / internal roster): the pre-approved vendor list by trade should live on the board, not just in someone's head.
#### Columns, Statuses and SLA Clocks
- Your PM software (the work-order platform): native SLA timestamps, invoice matching, and owner portal approval notifications live here. The board columns map directly to their work order fields.
- Monday.com / ClickUp: if you want the visual color-coded SLA clock on a kanban board with automation rules, these sit on top of your PM software and pull via integration.
- Latchel: handles the After-Hours Flag trigger automatically; logs intake timestamp and dispatches on-call vendor without staff involvement.
- Zapier / Make: connects the SLA breach event in your PM software to a Slack or SMS alert to the coordinator and PM in real time.
#### Automations
- Your PM software (the work-order platform): handles R-series and O-series automations natively via work order workflows and owner portal notifications. Best starting point.
- Zapier / Make: bridges the gap between your PM software and external channels (Slack alerts for E-series, SMS via Twilio for V-series nudges).
- Latchel: executes V1 to V3 and the after-hours fork (R3, O7) automatically without staff involvement; logs timestamps back to your PM software.
- Monday.com / ClickUp: best platform for the T-series stage transition logic and the C-series 30-day watch timer if your PM software does not support conditional automation natively.
#### Weekly KPI Dashboard
- Your PM software (the work-order platform): Sections A, D, and E pull directly from native work order and owner portal reports.
- Monday.com / ClickUp: Sections B, C, and F are best tracked here with formula columns and dashboard widgets if your PM software does not surface them natively.
- Power BI / Google Looker Studio: connect to both sources for a single Monday morning leadership dashboard that auto-refreshes overnight Sunday.
[Company Name] - internal operations document. Companion documents: Occupied Unit Maintenance Workflow, Remote Maintenance Coordinator Roles and Responsibilities, Remote Maintenance Coordinator KPI Addendum A, In-House Tech vs. Vendor Dispatch Decision Matrix, Turnover Tracking Board (Full System Design), The Make Ready Deep Dive, Monthly Turnover Performance Report Template.
