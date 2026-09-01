---
title: "Occupied Unit Maintenance Workflow"
source: "PMAgents source library, owner-reviewed"
converted: 2026-08-19
google_doc_id: 1fwKqbKkUpAejNo0rEPCwSdNZ5vkEXkWat0Kx-TmyxsY
google_doc_url: https://docs.google.com/document/d/1fwKqbKkUpAejNo0rEPCwSdNZ5vkEXkWat0Kx-TmyxsY/edit
library_folder: 1QDyp_rF5syRtdM_XR3TAhT4CbXhdSoOg
audience: all agents
status: reference
---

# Occupied Unit Maintenance Workflow

## Occupied Unit Maintenance Workflow
Report to Intake to Triage to Dispatch to Visit to Close to Owner Notification, 420 Doors, Class B to D, [Company Name]
The full occupied unit maintenance process for a remote coordinator running in-house techs, vendors and an after-hours line on the maintenance platform plus the accounting system. Ten steps from resident report to owner notification, each with an owner, a gate, the working tables, a handoff and a time target. Then the after-hours and emergency path, the callback and recurring issue path, the warranty path, the tenant-caused damage path, the coordinator daily update checklist, how the maintenance platform and the accounting system connect, and the master SLA summary.
### Process Map at a Glance
---
Resident reports issue, then:
1. Step 1 Intake: the maintenance platform auto-captures
2. Step 2 Triage and Priority: Coordinator classifies
3. Step 3 Phone Troubleshoot: Coordinator calls before dispatch
4. Step 4 Tech vs. Vendor Assignment: Dispatch Decision Matrix
5. Step 5 Scheduling and Resident Access: Coordinator plus the maintenance platform
6. Step 6 Owner Approval (if over threshold): PM owns
7. Step 7 The Visit and Completion Proof: Tech or Vendor executes
8. Step 8 Resident Follow-Up: the maintenance platform auto plus Coordinator confirms
9. Step 9 Invoice and Closeout: Coordinator plus Bookkeeper
10. Step 10 Owner Notification: Coordinator logs, PM sends if needed
### The Ten Steps
#### Step 1: Intake
Who Owns It: the maintenance platform (automated), then Maintenance Coordinator reviews
What Must Be True Before It Starts:
- Resident is active in the accounting system with a current lease
- the maintenance platform is connected to the accounting system and synced to the unit
- Resident has portal access or the after-hours line number
How It Comes In, All 4 Channels:

| Channel | What Happens Automatically | Coordinator Action |
|---|---|---|
| the maintenance platform portal (preferred) | Work order created, resident gets confirmation, Coordinator notified | Review by 9am daily |
| the accounting system tenant portal | Work order created in the accounting system, syncs to the maintenance platform | Coordinator converts to Work order |
| Phone call to office | Coordinator or admin creates Work order manually | Enter all details, attach photos if provided |
| After-hours line | After-hours dispatcher triages (see After-Hours and Emergency Path) | Coordinator reviews at open of business |

Required Fields at Intake (the maintenance platform):
- Unit address plus resident name
- Category (plumbing, HVAC, electrical, appliance, structural, pest, other)
- Description of issue: what, when it started, how bad
- Photos or video (required for anything not clearly described)
- Is anyone in the home during business hours? (access note)
- Permission to enter without resident present? (yes/no)
Handoff: Coordinator receives the maintenance platform notification, then moves to Step 2
---
Time Target: Intake acknowledged to resident within 1 hour during business hours via the maintenance platform auto-message. Coordinator reviews all new Work orders by 9:00 AM daily.
#### Step 2: Triage and Priority Classification
Who Owns It: Maintenance Coordinator
What Must Be True Before It Starts:
- Work order is created with enough information to classify
- If information is missing, Coordinator contacts resident before classifying
Priority Matrix:

| Priority | Definition | Examples | Response Target |
|---|---|---|---|
| EMERGENCY | Immediate health, safety, or property damage risk | Active water leak/flooding, no heat below 55°F, gas smell, no hot water (Class C/D), sewage backup, fire damage, electrical sparking, lockout | Same day, within 2 to 4 hours |
| URGENT | Habitability impacted, not immediately dangerous | No A/C above 85°F, refrigerator out, water heater not working, toilet not flushing (only one in unit), broken exterior door/lock | Within 24 to 48 hours |
| ROUTINE | Quality of life, non-habitability | Dripping faucet, slow drain, broken blinds, minor appliance issue, cosmetic damage, pest (non-infestation) | Within 5 to 7 business days |
| SCHEDULED | Preventive or non-urgent owner-requested | HVAC filter change, gutter cleaning, annual servicing | Scheduled in advance, 10 to 14 days |

---
Class B to D Adjustment: Class C and D properties carry higher habitability risk. Apply one tier up in urgency when in doubt. A broken A/C in a Class D unit in summer is an Emergency, not Urgent.
Recurring Issue Flag: before classifying, Coordinator checks the maintenance platform and the accounting system history on the unit.
- Same issue within 90 days = flag as Recurring (see Callback and Recurring Issue Path)
- Same issue within 30 days = flag as Callback. Do not dispatch a new vendor without reviewing prior work
Handoff: Priority assigned in the maintenance platform, then moves to Step 3 (troubleshoot) or Step 4 (emergency: skip to dispatch)
---
Time Target: All Work orders classified within 2 hours of receipt during business hours
#### Step 3: Phone Troubleshoot Before Dispatch
Who Owns It: Maintenance Coordinator
What Must Be True Before It Starts:
- Priority is Urgent or Routine (Emergencies skip to Step 4)
- Coordinator has reviewed the Work order and photos
- Resident phone number is confirmed in the accounting system
Purpose: prevent unnecessary dispatch. A dispatched tech or vendor costs $75 to $200 or more before a wrench is turned. Troubleshooting over the phone resolves an estimated 15 to 25% of Routine and some Urgent calls.
Troubleshoot Script by Category:

| Issue Type | Phone Troubleshoot Steps |
|---|---|
| No power / outlets not working | Check breaker panel and reset tripped breakers. Check GFCI outlets in bathroom/kitchen and press the reset button. |
| Garbage disposal not working | Press reset button on bottom of unit. Check if unit is jammed; use the hex key. |
| No heat / A/C not working | Check thermostat batteries. Confirm thermostat is set correctly. Check air filter: is it blocked? Check breaker. |
| Refrigerator not cooling | Check if plugged in. Check thermostat dial inside fridge. Check if coils are blocked. |
| Toilet running / not flushing | Check flapper: is it seated? Check water supply valve: is it open? |
| Slow drain | Try plunger. Check for visible blockage. |
| No hot water | Check water heater pilot light (gas). Check breaker (electric). Check thermostat on unit. |
| Leaking faucet | Confirm location and severity: is it a drip or active flow? Can resident place a bucket temporarily? |
| Pest | Confirm type, quantity, location. Is this isolated or widespread? |

Outcomes of Troubleshoot Call:

| Outcome | Action |
|---|---|
| Resident resolves it | Close Work order. Log resolution notes. No dispatch. |
| Resident caused it (user error confirmed) | Proceed to dispatch. Flag as Tenant Caused (see Tenant-Caused Damage Path) |
| Confirmed repair needed | Proceed to Step 4, dispatch |
| No answer from resident | Leave voicemail plus send the maintenance platform message. Attempt 2x. If no response in 4 hours (Urgent) or 24 hours (Routine), proceed to dispatch with permission-to-enter note. |

Log in the maintenance platform: Date/time of call, who was reached, what was discussed, outcome
Handoff: Coordinator confirms dispatch needed, then moves to Step 4
---
Time Target: Troubleshoot call attempted within 2 hours of Work order classification for Urgent; within 4 hours for Routine
#### Step 4: Tech vs. Vendor Assignment (Dispatch Decision Matrix)
Who Owns It: Maintenance Coordinator
What Must Be True Before It Starts:
- Troubleshoot complete (or skipped for Emergency)
- Issue confirmed as requiring physical dispatch
- Recurring/Callback flag checked
Dispatch Decision Matrix:

| Criteria | Send In-House Tech | Send Vendor |
|---|---|---|
| Scope | General repairs, minor plumbing, appliance diagnosis, drywall patches, door hardware, locks, filters | Licensed trade work (HVAC, electrical panel, gas, major plumbing), roofing, pest control, appliance replacement |
| License required? | No | Yes: always send licensed vendor |
| Estimated cost | Under $300 and within tech skill set | Any amount if specialized trade |
| Time sensitivity | Available same day or next day | Emergency vendors available 24/7 |
| Warranty situation | Do NOT send tech; send warranty vendor (see Warranty Path) | Warranty vendor required |
| Tenant-caused damage | Tech can assess and document | Vendor if repair is specialized |
| Recurring issue | Do NOT send same tech; escalate to senior tech or specialist vendor | Escalate to vendor if tech has already attempted |

Vendor Assignment Rules:
- Always assign from the pre-approved vendor list in the maintenance platform
- Match vendor to trade category (plumbing, HVAC, electrical, pest, general)
- For Class C/D properties: prioritize vendors who are familiar with the property type and have fast availability
- Never assign a vendor who has an open invoice dispute or unresolved callback on another unit
Log in the maintenance platform: Assigned tech or vendor name, trade category, reason for selection, estimated cost if known
Handoff: Assignment made in the maintenance platform, then vendor/tech receives automated notification, then moves to Step 5
---
Time Target: Assignment made within 1 hour of dispatch decision for Emergency/Urgent; same business day for Routine
#### Step 5: Scheduling and Resident Access
Who Owns It: Maintenance Coordinator (via the maintenance platform)
What Must Be True Before It Starts:
- Tech or vendor assigned in the maintenance platform
- Resident access preference confirmed (from intake)
- Entry notice requirements known for the state/jurisdiction
Scheduling Rules:

| Priority | Scheduling Target | Notice to Resident |
|---|---|---|
| EMERGENCY | Same day; no notice required for true emergency | Notify as soon as possible, even if entering |
| URGENT | Within 24 to 48 hours | Minimum 24-hour notice via the maintenance platform |
| ROUTINE | Within 5 to 7 business days | Minimum 24 to 48 hour notice via the maintenance platform |
| SCHEDULED | Agreed date in advance | 5 to 7 day advance notice |

Access Options (confirm at intake):
- Resident present during visit
- Permission to enter without resident (lockbox or key on file in the maintenance platform)
- Resident requests specific time window, then Coordinator confirms with tech/vendor
the maintenance platform Scheduling Actions:
- Send resident appointment confirmation via the maintenance platform (auto-message)
- Include: tech/vendor name, date, time window, what they will be working on
- Attach access instructions for tech/vendor (lockbox code, gate code, parking notes)
- Set reminder in the maintenance platform 24 hours before visit
If Resident Refuses Access:
- Document refusal in the maintenance platform
- Send written notice that failure to provide access may delay repairs and affect habitability claims
- Escalate to PM if refusal is repeated or if it is an Emergency
Handoff: Appointment confirmed in the maintenance platform, then tech/vendor has all access info, then moves to Step 6 (owner approval check) or Step 7 (visit) if under threshold
---
Time Target: Scheduling confirmed to resident within 4 hours of assignment for Urgent; same business day for Routine
#### Step 6: Owner Approval (When Cost Exceeds Threshold)
Who Owns It: PM (relationship plus decision) | Coordinator (triggers and tracks)
What Must Be True Before It Starts:
- Estimated cost is known or vendor has provided a quote
- Cost exceeds the owner's pre-authorized threshold (default: $500 unless otherwise noted in the PMA)
- Issue is non-emergency (Emergencies proceed without approval; notify after)
Approval Threshold Rules:

| Situation | Action |
|---|---|
| Under $500 (or owner's threshold) | Coordinator approves and dispatches; no owner contact required |
| Over $500, non-emergency | PM contacts owner for approval BEFORE work begins |
| Emergency, any cost | Proceed immediately. PM notifies owner same day with cost estimate and photos |
| Over $500, tenant caused | PM contacts owner AND documents tenant liability before proceeding |
| Warranty repair, any cost | Route to warranty vendor. Owner notified but no approval needed for covered work |

Owner Approval Process:
1. Coordinator flags Work order as "Pending Owner Approval" in the maintenance platform
2. Coordinator sends PM a summary: issue, estimated cost, vendor, photos, recommendation
3. PM contacts owner via phone or owner portal; target within 4 business hours
4. Owner approves or declines (see outcomes below)

| Owner Response | What Happens Next |
|---|---|
| Approved | PM notifies Coordinator, then dispatch proceeds |
| Declined | PM documents decision. If habitability issue, PM advises owner of legal risk in writing. Coordinator logs in the maintenance platform. |
| Owner wants second opinion | Coordinator gets second quote, returns to PM |

Log in the maintenance platform plus the accounting system: date/time of owner contact, approval or denial, who authorized, estimated cost
Handoff: Approval received, then Coordinator updates Work order, then moves to Step 7
---
Time Target: Owner contacted within 4 business hours of quote receipt. Approval loop closed within 24 hours for Urgent; 48 hours for Routine.
#### Step 7: The Visit and Completion Proof
Who Owns It: In-House Tech or Vendor (executes) | Coordinator (monitors and confirms)
What Must Be True Before It Starts:
- Appointment confirmed with resident
- Access instructions provided to tech/vendor
- Owner approval received (if required)
- Work order status updated to "Scheduled" in the maintenance platform
During the Visit, Tech/Vendor Requirements:

| Requirement | Detail |
|---|---|
| Check in via the maintenance platform | Tech/vendor marks arrival in the maintenance platform; timestamps the visit |
| Photos, before | Required for every visit. Minimum 3 photos of the issue before work begins |
| Scope confirmation | If scope changes on-site (bigger issue found), tech/vendor contacts Coordinator BEFORE proceeding |
| Tenant-caused damage found on-site | Stop. Document with photos. Contact Coordinator before doing any work. |
| Warranty item found on-site | Stop. Identify warranty coverage. Contact Coordinator. Do not proceed without warranty vendor. |
| Photos, after | Required for every completed repair. Minimum 3 photos showing completed work |
| Check out via the maintenance platform | Tech/vendor marks completion in the maintenance platform |
| Resident sign-off | If resident is present, get verbal or written confirmation that issue is resolved |

Scope Change Protocol (On-Site Discovery):
1. Tech/vendor finds bigger issue on-site
2. STOP; do not proceed
3. Call Coordinator immediately
4. Coordinator gets new estimate
5. Is new cost over threshold? YES: PM gets owner approval (return to Step 6). NO: Coordinator approves, work proceeds
6. All changes documented in the maintenance platform
Handoff: Tech/vendor marks complete in the maintenance platform with photos, then Coordinator reviews, then moves to Step 8
---
Time Target: Coordinator reviews completion photos within 4 hours of work order marked complete
#### Step 8: Resident Follow-Up
Who Owns It: the maintenance platform (automated first touch) | Coordinator (confirms if needed)
What Must Be True Before It Starts:
- Work order marked complete in the maintenance platform
- Completion photos uploaded and reviewed by Coordinator
Follow-Up Sequence:

| Step | Who | When | Method |
|---|---|---|---|
| Auto satisfaction survey | the maintenance platform | Immediately upon completion | the maintenance platform automated message |
| Coordinator review of response | Coordinator | Within 24 hours | the maintenance platform dashboard |
| If resident is satisfied | Coordinator | Log and close | No further action needed |
| If resident is unsatisfied | Coordinator | Within 24 hours | Call resident, assess issue |
| If issue not resolved | Coordinator | Same day | Open a callback work order that references the closed one (closure is irreversible); see Callback and Recurring Issue Path |
| No response from resident | Coordinator | After 48 hours | One follow-up message via the maintenance platform, then close |

Log in the maintenance platform: Satisfaction rating, resident comments, any follow-up actions taken
Handoff: Resident confirmed satisfied, then Coordinator moves to Step 9
---
Time Target: Follow-up survey sent within 1 hour of completion. Coordinator reviews responses by end of business day.
#### Step 9: Invoice and Closeout
Who Owns It: Coordinator (receives and reviews invoice) | Bookkeeper (processes payment in the accounting system)
What Must Be True Before It Starts:
- Work confirmed complete with photos
- Resident follow-up complete
- Invoice received from vendor or tech time logged
Invoice Review Checklist (Coordinator):

| Check | Detail |
|---|---|
| Invoice matches approved scope | No surprise line items without prior approval |
| Invoice matches estimate | If over estimate by more than 10%, flag for PM review before paying |
| Photos attached to Work order | Before and after required; do not approve invoice without them |
| Tenant-caused damage flagged | Invoice coded as tenant chargeback in the accounting system |
| Warranty work coded correctly | Coded to warranty, not owner expense |
| Invoice uploaded to the accounting system | Attached to the work order and the unit ledger |

the accounting system plus the maintenance platform Closeout Steps:
1. Coordinator uploads invoice to the maintenance platform; attach to Work order
2. Coordinator creates bill in the accounting system, coded to correct unit, owner, and expense category
3. If tenant chargeback: Coordinator creates tenant charge in the accounting system ledger
4. Bookkeeper reviews and approves payment per vendor payment schedule
5. Work order marked "Closed" in the maintenance platform
6. Work order marked "Completed" in the accounting system
Handoff: Work order closed and work order completed, then moves to Step 10
---
Time Target: Invoice reviewed and entered in the accounting system within 48 hours of receipt. Work order closed same day as invoice approval.
#### Step 10: Owner Notification and Communication
Who Owns It: Coordinator (routine updates via portal) | PM (anything over threshold, recurring, or sensitive)
What Must Be True Before It Starts:
- Work order is closed in the maintenance platform and the accounting system
- Invoice is entered and coded correctly
- Completion photos are attached to the unit record
Owner Notification Rules by Situation:

| Situation | Who Notifies | Method | Timing |
|---|---|---|---|
| Routine repair under threshold | the accounting system auto-notifies via owner portal | Portal statement plus work order record | Upon invoice posting |
| Repair over threshold, pre-approved | PM confirms completion | Phone or email | Within 24 hours of close |
| Emergency, any cost | PM notifies same day | Phone call first, then portal note | Same day as dispatch |
| Tenant-caused damage | PM notifies with documentation | Email with photos plus chargeback notice | Within 48 hours of close |
| Recurring issue, same unit | PM notifies with pattern summary | Email with history plus recommendation | Within 48 hours of close |
| Scope change discovered on-site | PM notifies with revised cost | Phone plus portal note | Before work resumes |
| Owner declined repair, habitability risk | PM documents in writing | Certified email or portal message | Same day as refusal |

What Goes Into the accounting system Owner Portal (Every Work Order):
- Description of issue
- Work performed
- Vendor or tech name
- Before and after photos
- Invoice amount
- Tenant chargeback amount (if applicable)
- Date opened and date closed
---
Owner Portal = the paper trail. Every owner should be able to log in and see the full history of every repair on their property without calling you.
Handoff: Portal updated and PM notified where the situation calls for it; the work order is done
---
Time Target: Portal updated within 48 hours of work order close for all routine repairs. Same day for emergencies.
### After-Hours and Emergency Path
Who Owns It: After-Hours Line Dispatcher (initial), then On-Call Vendor, then Coordinator (next business day), then PM (if cost or sensitivity warrants)
What Must Be True Before It Starts:
- After-hours line is active and staffed or answered by service
- On-call vendor list is current in the maintenance platform and dispatcher has access
- PM on-call contact is established for true life-safety situations
After-Hours Flow: resident calls the after-hours line, then the dispatcher answers and asks three questions:
1. What is the problem?
2. Is anyone in immediate danger?
3. Is the property actively being damaged right now?
The answers place the call in one of four tiers:

| Tier | Actions |
|---|---|
| LIFE SAFETY (fire, gas, carbon monoxide, break-in) | Call 911 FIRST, then notify PM on-call immediately, then document everything |
| PROPERTY EMERGENCY (flooding, sewage, no heat below 55°F, electrical sparking) | Dispatcher contacts on-call vendor from approved list, then vendor dispatched immediately (no approval needed), then dispatcher creates Work order in the maintenance platform (or logs for Coordinator to create at open), then PM notified by text/call same night if cost likely over $500 |
| URGENT BUT NOT EMERGENCY (no A/C, broken appliance, minor leak) | Dispatcher advises resident of next-business-day response, then provides interim guidance (shut off water valve, use space heater, etc.), then creates Work order or logs for Coordinator, then Coordinator picks up at 9am and processes as Urgent |
| NON-EMERGENCY (cosmetic, routine) | Dispatcher advises resident to submit via portal, then logs the call for Coordinator awareness |

After-Hours Dispatcher Must Have Access To:
- On-call vendor list by trade (plumbing, HVAC, electrical, general), stored in the maintenance platform
- the maintenance platform login to create or log Work orders
- PM on-call cell number for life-safety events
- Basic troubleshoot script (same as Step 3 above)
- Lockbox/access codes for emergency entry (secured access)
Next Morning, Coordinator After-Hours Review:
- Review all after-hours Work orders created overnight
- Confirm vendor was dispatched and has checked in
- Get status update from vendor on any active emergency
- Notify PM of anything over threshold or sensitive
- Update owner same morning for any emergency dispatch
---
Time Target: Emergency vendor on-site within 2 hours of dispatch. Coordinator reviews all after-hours activity by 9:00 AM.
### Callback and Recurring Issue Path
#### Callback (Same Issue, Within 30 Days)
Definition: resident reports the same problem that was recently repaired; the repair did not hold.
1. Resident reports same issue within 30 days of prior close
2. Coordinator flags as CALLBACK in the maintenance platform
3. Do NOT dispatch a new vendor without reviewing prior work
4. Coordinator pulls prior Work order: who did the work? what was the scope? are photos on file?
5. Contact original vendor/tech: "This is a callback on work completed [date] at [address]. We need you to return at no charge to assess and correct."
6. Vendor/tech returns; no new charge for same scope
7. If vendor refuses callback: PM notified, vendor flagged in the maintenance platform, new vendor assigned, original vendor billed for cost
8. If callback reveals NEW or EXPANDED issue: treat as new work order, new estimate, new approval if over threshold
9. PM notifies owner of callback situation
---
Vendor Accountability Rule: all vendors in the approved network must warranty their labor for a minimum of 30 days. This is a condition of being on the approved list. Document it in the vendor agreements.
#### Recurring Issue (Same Unit, 31 to 90 Days, or 3 or More Times in 12 Months)
Definition: a pattern of the same or related issues on the same unit; signals a systemic problem.
1. Coordinator identifies recurring pattern in the maintenance platform history
2. Flag unit as RECURRING in the maintenance platform
3. Coordinator pulls full unit maintenance history from the accounting system
4. Coordinator prepares summary for PM: issue type, dates of prior work orders, vendors used, total cost to date, photos from prior visits
5. PM reviews and determines root cause category (table below)

| Root Cause Category | Actions |
|---|---|
| DEFERRED CAPITAL ISSUE (system at end of life) | PM recommends replacement to owner; owner approval required; Scope Playbook used for replacement scope |
| TENANT BEHAVIOR (resident causing recurring damage) | PM documents pattern; lease compliance notice issued if warranted; costs charged back to tenant |
| VENDOR QUALITY ISSUE (poor workmanship pattern) | Vendor removed from approved list; new vendor assigned for corrective work; PM reviews vendor roster |
| BUILDING/STRUCTURAL ISSUE (foundation, plumbing main, roof, etc.) | PM escalates to full property assessment; owner notified with capital plan recommendation |

### Warranty Path
Tech or Coordinator identifies an item that may be under warranty, then checks the accounting system unit record for warranty documentation (appliances, HVAC, roof, new construction, etc.). Is it under warranty?

| Answer | Actions |
|---|---|
| YES | Do NOT dispatch your own vendor; contact warranty provider directly; coordinate access between warranty vendor and resident; Coordinator tracks claim in the maintenance platform; invoice coded as warranty, not owner expense; owner notified that warranty is being used |
| NO / EXPIRED | Proceed with standard dispatch (Step 4); note in Work order that warranty was checked and expired |
| UNCLEAR | Coordinator researches: check appliance model/serial, purchase date, builder warranty docs. If still unclear, PM makes judgment call |

---
Best Practice: store all warranty documents, serial numbers, and expiration dates in the accounting system under the unit record at move-in or property onboarding. Coordinator checks this BEFORE dispatching on any appliance, HVAC, roof, or new construction issue.
### Tenant-Caused Damage Path
1. Damage identified as tenant-caused (confirmed on-site by tech/vendor, or via photos)
2. Tech/vendor STOPS work; documents with photos
3. Contacts Coordinator immediately
4. Coordinator reviews photos; agrees it is tenant-caused
5. Coordinator notifies PM
6. PM determines habitability risk or non-habitability (table below)
7. Owner notified by PM with photos and chargeback plan
8. All documentation saved in the accounting system unit record

| PM Determination | Actions |
|---|---|
| HABITABILITY RISK (must repair regardless) | Proceed with repair; code invoice as tenant chargeback in the accounting system; PM sends tenant written notice of charge; charge added to tenant ledger in the accounting system; document for security deposit use at move-out |
| NON-HABITABILITY (cosmetic, non-urgent) | PM sends tenant written notice; tenant given option to repair themselves (within lease terms and approved standards); if tenant does not repair within 14 days: dispatch vendor, charge tenant; document for security deposit use at move-out |

---
Fair Housing Note: apply tenant-caused damage standards consistently across all units and all residents. Document your decision criteria. Never apply different standards based on protected class characteristics.
### Coordinator Daily Update Checklist
Who Owns It: Maintenance Coordinator. When: every business day; morning review by 9:30 AM, afternoon sweep by 4:00 PM.
#### Morning Review (9:00 to 9:30 AM)

| Task | Tool | Action |
|---|---|---|
| Review all new Work orders submitted overnight or since yesterday close | the maintenance platform | Classify priority, assign, or troubleshoot |
| Review after-hours log | the maintenance platform / After-hours notes | Create Work orders for any logged calls, notify PM of emergencies |
| Check all Work orders in "Scheduled" status | the maintenance platform | Confirm today's appointments are on track |
| Check all Work orders in "Pending Owner Approval" | the maintenance platform | Follow up with PM on any approvals over 24 hours old |
| Check all Work orders in "Waiting on Vendor" | the maintenance platform | Contact any vendor not confirmed within SLA |
| Review any Callback or Recurring flags | the maintenance platform | Escalate to PM if not already actioned |
| Review open invoices not yet entered | the accounting system | Enter and code any received invoices |

#### Afternoon Sweep (3:30 to 4:00 PM)

| Task | Tool | Action |
|---|---|---|
| Confirm all today's scheduled visits completed | the maintenance platform | Follow up with any tech/vendor who has not checked out |
| Review completion photos on closed Work orders | the maintenance platform | Approve or flag for re-inspection |
| Send resident follow-up on any completed Work orders not yet surveyed | the maintenance platform | Trigger or manually send satisfaction message |
| Update PM on any open items needing decision | Slack / Email | Brief summary: unit, issue, status, what is needed |
| Check for any Work orders approaching SLA breach | the maintenance platform | Urgent past 48 hrs, Routine past 7 days: escalate |
| Log any tenant-caused damage or warranty items identified today | the accounting system plus the maintenance platform | Ensure PM is looped in |

#### Weekly (Every Monday Morning)
Pull the maintenance platform report: open Work orders by priority, average days to close, vendor performance
Flag any unit with 2 or more open Work orders simultaneously, then report to PM
Review vendor invoice aging in the accounting system, then flag any unpaid over 30 days
Send PM a one-page weekly maintenance summary
### How It All Connects: the maintenance platform plus the accounting system

| Action | Lives In | Syncs To |
|---|---|---|
| Work order created | the maintenance platform | the accounting system (via integration) |
| Resident communication | the maintenance platform | Logged in Work order record |
| Vendor assignment plus scheduling | the maintenance platform | Not synced |
| Completion photos | the maintenance platform | Attached to Work order |
| Invoice uploaded | the maintenance platform plus the accounting system | the accounting system unit ledger |
| Tenant chargeback | the accounting system | Tenant ledger |
| Owner notification | the accounting system owner portal | Owner sees in portal |
| Work order history | Both | Full audit trail |

---
Rule: the maintenance platform is the operational brain: every communication, photo, and status lives there. the accounting system is the financial and legal record: every invoice, charge, and owner statement lives there. Never close a Work order without the invoice in the accounting system. Never post an invoice in the accounting system without the Work order photos attached.
### Master SLA Summary

| Priority | First Response | Dispatch | On-Site | Close |
|---|---|---|---|---|
| EMERGENCY | Immediate | Within 1 hour | Within 2 to 4 hours | Same day or next day |
| URGENT | Within 2 hours | Same day | Within 24 to 48 hours | Within 5 business days |
| ROUTINE | Within 4 hours | Same business day | Within 5 to 7 business days | Within 10 business days |
| SCHEDULED | Confirmed in advance | Scheduled date | Scheduled date | Day of visit |

[Company Name] - internal operations document. Companion documents: Remote Maintenance Coordinator Roles and Responsibilities, Remote Maintenance Coordinator KPI Addendum A, In-House Tech vs. Vendor Dispatch Decision Matrix, The Coordinator's Scope Playbook, The Make Ready Deep Dive, Turnover Tracking Board (Full System Design), Owner Make-Ready Communication Templates.
