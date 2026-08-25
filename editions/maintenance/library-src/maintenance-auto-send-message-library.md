---
title: "Maintenance Auto-Send Message Library"
source: "PMAgents source library, owner-reviewed"
converted: 2026-08-19
google_doc_id: 1-0d9Cx8i5HbOupRGEBu_28y7VpM21cgzXjdTg1D1XQw
google_doc_url: https://docs.google.com/document/d/1-0d9Cx8i5HbOupRGEBu_28y7VpM21cgzXjdTg1D1XQw/edit
library_folder: 1QDyp_rF5syRtdM_XR3TAhT4CbXhdSoOg
audience: all agents
status: reference
---

# Maintenance Auto-Send Message Library

## Maintenance Auto-Send Message Library
Resident, vendor, owner and PM alert copy for the occupied unit maintenance board, [Company Name]
The exact copy behind every automation on the occupied unit maintenance board. Part 1 is the resident series (R1 to R10, plus the R11 to R14 additions: entry notice, day-of reminder, delay notice and charge notice), Part 2 the vendor and tech series (V1 to V9), Part 3 the owner series (O2 to O8) and Part 4 the internal PM escalation alerts (E1 to E8). Each message carries its trigger, channel, timing and tone rule, then the SMS copy and the portal or email copy with merge fields, then the character-count and gating notes. Each part closes with a master reference table and the tool notes for that series. O1 on the board is a system action (set Approval Required and move the card to Owner Hold) with no outbound message, so the owner copy begins at O2.
---
Templates: bracketed merge fields are left exactly as written for the automation platform to fill. Tool-agnostic by design; vendor notes per series at the end of each part.
### Part 1: Resident Series (R1 to R10)
#### Global Tone Rules
Applied across all ten messages before individual rules.
- Warm but efficient. Never cold, never chatty.
- First name only in the greeting. Never "Dear Resident" or "Hello Tenant."
- Plain language. No property management jargon. No work order system terminology visible to the tenant.
- One clear next step per message. Never list multiple asks.
- Never give vendor contact info. All coordination stays in-house.
- Never state cost in resident-facing messages unless legally required.
- SMS: under 160 characters where possible. No emojis unless your brand uses them. No abbreviations.
- Signature block on all emails: company name, main phone, portal link. No individual staff names on auto-sends.
#### R1: Standard Intake Confirmation
| Field | Value |
|---|---|
| Trigger | Card created, any priority |
| Channel | SMS + Portal Message (dual send) |
| Timing | Immediately on intake |
| Tone rule | SMS: reassuring and instant. The tenant just submitted something; confirm it landed and give them a reference number. Nothing else. Portal: same reassurance, slightly more room to breathe. Confirms what they submitted and sets a realistic expectation without overpromising a timeline. |
---
SMS
[Company Name]: Hi [First Name], we got your maintenance request for [Unit Address]. Your request # is [WO ID]. We'll be in touch soon. Questions? Call us at [Main Phone].
Character count: ~155. Fits within 160. If your WO ID format is long, abbreviate Unit Address to unit number only.
---
Portal Message
Subject: We received your maintenance request, #[WO ID]
Hi [First Name],
We received your maintenance request for [Unit Address] and it's already in our queue. Your request number is [WO ID]. You can use this number if you need to follow up with us.
Here's what happens next: our team will review your request and reach out to schedule a repair. We'll keep you updated every step of the way right here in your portal.
Thank you for letting us know. We'll take it from here.
[Company Name]
[Main Phone Number]
[Portal Login Link]
#### R2: Emergency Priority Confirmation
| Field | Value |
|---|---|
| Trigger | Card created, Priority = Emergency |
| Channel | SMS (fires in addition to R1, not instead of it) |
| Timing | Immediately on intake, simultaneously with R1 |
| Tone rule | Urgent but calm. The tenant is likely stressed. Acknowledge the severity without amplifying panic. Short, direct, action-oriented. |
---
SMS
[Company Name]: [First Name], we're treating your request as an emergency. Our team is on it right now. We'll update you shortly.
Character count: ~142. Intentionally brief; this fires alongside R1. Do not repeat the WO number here; R1 already covered it.
#### R3: After-Hours Emergency Confirmation
| Field | Value |
|---|---|
| Trigger | Card created, After-Hours Flag = Yes |
| Channel | SMS (fires in addition to R1) |
| Timing | Immediately on intake |
| Tone rule | Calm and specific. The tenant submitted something outside business hours; they need to know a real person (or on-call system) is handling it, not that it is sitting in a queue until morning. Give a concrete follow-up window. |
---
SMS
[Company Name]: Hi [First Name], your after-hours request was received. An on-call vendor is being contacted. Expect an update by [Follow-Up Time, e.g., 7:00 AM]. Request # [WO ID].
Character count: ~158. [Follow-Up Time] should be a dynamic field: set to next morning at 7 or 8 AM if submitted between 9 PM and 6 AM, or within 2 hours if submitted during evening hours. Configure this in your automation platform.
#### R4: Tenant Responsibility Notice
| Field | Value |
|---|---|
| Trigger | Tenant Responsibility Flag set = Yes |
| Channel | Portal Message + Email (dual send) |
| Timing | Immediately on flag set |
| Tone rule | Gentle, not accusatory. The tenant may not know their lease terms. Explain the "why" briefly, give them a path forward, and keep the door open. Never use the word "denied" or "rejected." |
---
Portal Message + Email
Subject: About your recent maintenance request, #[WO ID]
Hi [First Name],
Thank you for reaching out about the issue at [Unit Address]. After reviewing your request, our team found that this type of repair falls under resident responsibility based on your lease agreement. This typically includes minor items like replacing light bulbs, resetting tripped breakers, or small fixes under $25.
We know that's not always the answer you're hoping for, and we want to make sure you're not left without help. Here's what you can do:
[Insert self-help resource link OR brief instruction, e.g., "If this is a tripped breaker, here's how to reset it: [Link]"]
If you believe this was reviewed in error, or if the issue is more serious than described, please reply to this message or call us at [Main Phone] and we'll take another look right away.
Thank you for understanding. We're always here if you need us.
[Company Name]
[Main Phone Number]
[Portal Login Link]
This is the only R-series message that requires a human review checkpoint before firing. The coordinator should confirm the Tenant Responsibility flag is correctly set before this sends. Build a 15-minute delay into the automation to allow for a coordinator review window.
#### R5: Vendor Scheduled Notification
| Field | Value |
|---|---|
| Trigger | Card stage moves to Dispatched |
| Channel | SMS + Portal Message (dual send) |
| Timing | Immediately on stage change |
| Tone rule | Good news delivery. Keep it positive and practical. Give the date and window clearly. Reassure them they don't need to be home unless noted. |
---
SMS
[Company Name]: Good news, [First Name]! Your repair is scheduled for [Appointment Date] between [Time Window]. You don't need to be home. Questions? Call [Main Phone].
Character count: ~155. If the tenant IS required to be present, swap "You don't need to be home" for "Please plan to be home during this window." This should be a conditional field in your automation.
---
Portal Message
Subject: Your repair is scheduled, #[WO ID]
Hi [First Name],
Great news: we've scheduled a repair for your request at [Unit Address]. Here are the details:
Date: [Appointment Date]
Time: [Appointment Window, e.g., 8:00 AM to 12:00 PM]
Work: [Brief Issue Description, e.g., "Kitchen faucet leak"]
You do not need to be present; our team will coordinate access. [CONDITIONAL: If presence required, replace with: "Please plan to be available during this window. Our team will reach out if anything changes."]
We'll send you another update once the work is complete.
Thank you for your patience. We're on it!
[Company Name]
[Main Phone Number]
[Portal Login Link]
#### R6: Vendor On-Site Notification
| Field | Value |
|---|---|
| Trigger | Vendor check-in timestamp logged (Work Started) |
| Channel | SMS |
| Timing | Immediately on timestamp |
| Tone rule | Quick and informative. The tenant doesn't need a long message here, just a heads-up that someone is at their home right now. Calm, matter-of-fact. |
---
SMS
[Company Name]: Hi [First Name], your vendor has arrived at [Unit Address] and work has started. We'll let you know when it's done.
Character count: ~138. This fires only if a check-in timestamp is logged by the vendor or coordinator. If your platform does not support vendor check-in timestamps natively, this trigger can be set manually by the coordinator when they confirm vendor arrival.
#### R7: Work Completed Notification
| Field | Value |
|---|---|
| Trigger | Work Completed timestamp logged |
| Channel | SMS + Portal Message (dual send) |
| Timing | Immediately on timestamp |
| Tone rule | Warm close. The job is done; acknowledge it simply and set up the survey that follows in R8 without pre-asking for it here. |
---
SMS
[Company Name]: Hi [First Name], the repair at [Unit Address] is complete. We'll follow up shortly to make sure everything looks good. Thank you for your patience!
Character count: ~152. Do not mention the survey in this message; R8 fires 24 hours later and handles that ask cleanly.
---
Portal Message
Subject: Your repair is complete, #[WO ID]
Hi [First Name],
We're happy to let you know that the repair at [Unit Address] has been completed.
Work completed: [Brief Description, e.g., "Kitchen faucet replaced and tested"]
Completed on: [Completion Date]
If everything looks good, no action is needed on your end. If something doesn't seem right or the issue isn't fully resolved, please don't hesitate to reach out. You can reply here or call us at [Main Phone] and we'll get someone back out right away.
Thank you for your patience. We appreciate you!
[Company Name]
[Main Phone Number]
[Portal Login Link]
#### R8: Satisfaction Survey Request
| Field | Value |
|---|---|
| Trigger | Card moves to Pending Inspection |
| Channel | Portal Message + Email (dual send) |
| Timing | 24 hours after Work Completed timestamp |
| Tone rule | Light ask, no pressure. Make it feel like a genuine check-in, not a corporate survey blast. Keep it short. One click should get them there. |
---
Portal Message + Email
Subject: How did we do? Quick question about your recent repair
Hi [First Name],
We recently completed a repair at [Unit Address] and we want to make sure it hit the mark. It would mean a lot to us if you'd take 60 seconds to let us know how we did:
[Survey Link, "Share Your Feedback"]
Your honest feedback helps us keep improving, and we read every response.
Thank you for being a great resident!
[Company Name]
[Main Phone Number]
[Portal Login Link]
The survey should be a simple 1 to 5 star rating with one optional open comment field. Do not send a long form. If your platform has a native survey module, link directly to it. If not, a single-question form works fine; just make sure responses feed back into your tracking system.
#### R9: Low Survey Score Response
| Field | Value |
|---|---|
| Trigger | Survey score returned below threshold (e.g., 1 to 2 out of 5) |
| Channel | Email |
| Timing | Immediately on survey submission |
| Tone rule | Humble, human, and fast. This is the most important message in the set. The tenant is unhappy. Do not be defensive, do not over-explain, do not use corporate language. Acknowledge, apologize briefly, and commit to a real follow-up. A person's name should appear here, not just the company. |
---
Email
Subject: We hear you, and we're going to make it right
Hi [First Name],
Thank you for taking the time to share your feedback about your recent repair at [Unit Address]. We're sorry to hear the experience didn't meet your expectations. That's not the standard we hold ourselves to, and we want to make it right.
A member of our team will reach out to you personally within 24 hours to talk through what happened and figure out the best next step. You don't need to do anything; we'll come to you.
Thank you for giving us the chance to do better.
[Company Name]
[Main Phone Number]
[Portal Login Link]
This email fires automatically, but the follow-up call or message it promises must be a real human action. The automation map (E4) simultaneously flags the card and alerts the PM. The 24-hour callback commitment in this message must be tracked; if no coordinator action is logged within 24 hours, E4 re-escalates to the PM. Do not send this message if you cannot guarantee the follow-up.
#### R10: Work Order Officially Closed
| Field | Value |
|---|---|
| Trigger | Card moves to Closed, Resolved |
| Channel | Portal Message |
| Timing | Immediately on stage change |
| Tone rule | Clean, confident close. Brief. The tenant doesn't need a long message, just confirmation that the loop is closed and a clear door left open if anything comes up later. |
---
Portal Message
Subject: Your request is closed, #[WO ID]
Hi [First Name],
Just a quick note to let you know that your maintenance request #[WO ID] for [Unit Address] has been officially closed.
If the issue comes back or something new comes up, just submit a new request through your portal anytime. We're always here.
Thanks again for your patience throughout this process. We appreciate you!
[Company Name]
[Main Phone Number]
[Portal Login Link]
This is a portal-only send, no SMS. The tenant has already received R7 (work complete) and R8 (survey). A third SMS at close creates notification fatigue. Portal message only keeps the record clean without over-communicating.
### Part 1 additions: entry notice, day-of reminder, delay notice, charge notice
Four messages from the the second resident-message source set, renumbered R11 to R14 so the resident series reads R1 to R14 in one voice. The second set overlapped Series A on confirmation, scheduled, complete and survey (those duplicates are dropped); it adds the entry notice, the day-of reminder, the delay notice and the tenant-caused charge notice. Tone ladder for the four: Entry Notice = professional + legally precise; Day-Of Reminder = friendly + action-oriented; Delay = empathetic + accountable; Charge Notice = factual + firm, never accusatory. These four carry the signature block supplied with that source set (PM name + title, company name, maintenance line, portal link). The master reference and tool notes for the whole resident series (R1 to R14) follow at the end of this section.
#### R11: Notice of Entry (Advance Notice of Vendor Access)
| Field | Value |
|---|---|
| Trigger | Appointment confirmed AND Tenant Present = Not Required (vendor entering without tenant) |
| Channel | Email + SMS (dual send) |
| Timing | Minimum 24 hours before appointment; recommend sending at scheduling + day-before reminder (R12 handles day-of) |
| Tone rule | Professional and legally precise. This message serves as the written notice of entry required by landlord-tenant law in most states. It must be clear, specific, and documented. Never casual. Never vague on timing. |
Legal note: entry notice requirements vary by state; most require 24 hours written notice, some require 48 hours. Confirm your state's requirement with legal counsel before deploying this automation. This template defaults to 24-hour notice language.
---
Email
Subject: Notice of Entry: [Unit Address] | [Appointment Date]
Hi [Resident First Name],
This is your official notice that an authorized vendor will be entering your unit to perform a scheduled repair.
NOTICE OF ENTRY
Property: [Unit Address]
Date of Entry: [Appointment Date]
Time Window: [e.g., 10:00 AM to 12:00 PM]
Purpose: Maintenance repair, [Brief description, e.g., "Kitchen faucet replacement"]
Authorized By: [Company Name] on behalf of property owner
YOUR RIGHTS
You are not required to be present. The vendor has been provided with authorized access instructions and will enter only for the purpose stated above. All vendors working on your property are vetted and authorized by [Company Name].
If you have concerns about this entry, please contact us immediately at [Maintenance Line].
WHAT TO EXPECT
• Vendor will arrive within the stated time window
• Work will be limited to the area described above
• You will receive a completion notice once work is done
• Before and after photos will be taken for your property file
QUESTIONS OR CONCERNS?
Phone: [Maintenance Line] | Email: reply to this email | Portal: [Portal Link]
[PM Name] | [PM Title]
[Maintenance Line]
[Company Name] | [Portal Link]
This notice is provided in accordance with your lease agreement and applicable state law.
---
SMS
[Company Name]: Notice of entry for [Unit Address] on [Date] between [Time Window] for maintenance repair. Vendor has authorized access. Questions? Call [Maintenance Line].
~155 chars. Fits in one segment. The email is the legal record; SMS is the delivery confirmation. Both must send. Log send timestamp in WO file.
Entry notice requirements by common state (confirm with your property management attorney before deploying the R11 automation):
| State | Entry notice requirement |
|---|---|
| California | 24 hours written notice required |
| Texas | Reasonable notice (24 hours standard) |
| Florida | 12 hours notice required |
| New York | Reasonable notice (24 hours standard) |
#### R12: Day-Of Appointment Reminder
| Field | Value |
|---|---|
| Trigger | Appointment Date = Today AND Work Completed = blank |
| Channel | SMS primary, Email secondary |
| Timing | 8:00 AM on appointment day (or 2 hours before window opens if window starts after 10 AM) |
| Tone rule | Friendly and action-oriented. Quick reminder, nothing heavy. Confirm the time, confirm what to do if they need to reach someone, and wish them a good day. This is the highest-open-rate message in the series; keep it tight. |
---
SMS
Hi [Resident First Name]! Reminder: your repair at [Unit Address] is TODAY between [Time Window]. [Must be home: Please be there! / Vendor has access, no need to be home.] Questions? Call [Maintenance Line].
~175 chars. Trim "Please be there!" to "Be home please." if needed to stay under 160.
---
Email
Subject: Today's Reminder: Repair Appointment at [Unit Address] | WO #[WO ID]
Hi [Resident First Name],
Just a quick reminder that your repair appointment is today!
TODAY'S APPOINTMENT
Work Order #: [WO ID]
Property: [Unit Address]
Time Window: [e.g., 10:00 AM to 12:00 PM]
Service: [Brief description]
[Select one:]
Option A: PLEASE BE HOME during the time window above. If something has come up, call us right away at [Maintenance Line] so we can reschedule.
OR
Option B: NO ACTION NEEDED. The vendor has authorized access and will handle everything. We'll let you know when it's done.
Questions? We're here. Phone: [Maintenance Line] | Email: reply to this email
[PM Name] | [PM Title]
[Maintenance Line]
[Company Name] | [Portal Link]
#### R13: Repair Delay Notification
| Field | Value |
|---|---|
| Trigger | SLA Status = Breached OR Vendor Rescheduled = true AND Work Completed = blank |
| Channel | SMS + Email (dual send) |
| Timing | Same day as delay confirmed; within 2 hours of E3 or rescheduled flag |
| Tone rule | Empathetic first, factual second. The resident is waiting on a repair; a delay is frustrating. Acknowledge it directly, explain briefly without over-explaining, give a revised timeline, and make it easy to reach a real person. Do not blame the vendor by name. Do not make promises you can't keep on the revised date. |
---
SMS
Hi [Resident First Name], [Company Name] here. We're sorry, but your repair at [Unit Address] (WO #[WO ID]) has been delayed. New estimated completion: [Revised Date]. We're on it. Questions? Call [Maintenance Line].
~196 chars, 2 segments. Acceptable for a delay notice. Residents need the revised date; don't cut it.
---
Email
Subject: Update on Your Repair: WO #[WO ID] | [Unit Address]
Hi [Resident First Name],
We want to keep you informed about your open maintenance request at [Unit Address]. We're sorry to let you know that your repair has been delayed past the original expected completion date. We understand this is inconvenient and we sincerely apologize for the wait.
DELAY UPDATE
Work Order #: [WO ID]
Property: [Unit Address]
Issue: [Brief description]
Original Timeline: [Original Expected Date]
Reason for Delay: [e.g., "Part on order, expected to arrive [Date]." / "Vendor rescheduled, new appointment confirmed." / "We are sourcing an alternate vendor to complete this faster."]
Revised Completion: [Revised Estimated Date]
WHAT WE ARE DOING
• We are actively managing this repair and monitoring progress daily
• You will receive an update if anything changes before [Revised Date]
• You will receive a completion notice as soon as the work is done
QUESTIONS OR CONCERNS?
We know waiting is frustrating. If you have questions or the delay is creating a hardship, please reach out directly; we want to help.
Phone: [Maintenance Line] | Email: reply to this email | Portal: [Portal Link]
Thank you for your patience, [Resident First Name]. We appreciate it.
[PM Name] | [PM Title]
[Maintenance Line]
[Company Name] | [Portal Link]
#### R14: Tenant-Caused Damage Charge Notice
| Field | Value |
|---|---|
| Trigger | Work Order Cost Recovery = Tenant Responsible AND Invoice Approved |
| Channel | Email only |
| Timing | Within 48 hours of work order completion and cost determination |
| Tone rule | Factual and firm, never accusatory or emotional. State what happened, what it cost, why the resident is responsible per their lease, and how to pay. Give them a deadline and a dispute path. This email is a financial and legal record; every word matters. |
SMS is intentionally omitted for R14. Charge notices must be delivered in writing via email for documentation purposes. Log send timestamp in the WO file and the resident's ledger immediately.
---
Email
Subject: Maintenance Charge Notice: WO #[WO ID] | [Unit Address]
Attachments: Itemized invoice (PDF) | Supporting photos (if applicable)
Hi [Resident First Name],
Following the completion of a recent maintenance repair at [Unit Address], we have determined that the cost of this repair is the responsibility of the resident per your lease agreement.
CHARGE DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Work Completed: [Completion Date]
Issue: [Description of damage, e.g., "Garbage disposal damaged due to foreign object obstruction."]
Determination: Resident-caused damage per Lease Section [X]
Charge Amount: $[Invoice Amount]
Itemized Invoice: Attached to this email and uploaded to your portal under: Documents, then Maintenance, then WO #[WO ID]
LEASE REFERENCE
Per Section [X] of your lease agreement: "[Insert relevant lease language, e.g., 'Resident is responsible for damages caused by misuse, negligence, or failure to report issues in a timely manner.']"
HOW TO PAY
This charge has been added to your resident ledger. Please submit payment by [Payment Deadline, recommend 10 to 14 business days]:
• Resident Portal (fastest): [Portal Link]
• Check payable to: [Company Name]. Mail to: [Mailing Address]
QUESTIONS OR DISPUTES?
If you believe this charge has been applied in error, you have the right to submit a written dispute within [X] days of this notice. To dispute, please reply to this email or submit through your portal with:
• A written explanation
• Any supporting documentation or photos
Disputes will be reviewed by our property management team within [X] business days.
If you have questions, please contact us directly: Phone: [Maintenance Line] | Email: reply to this email | Portal: [Portal Link]
[PM Name] | [PM Title]
[Maintenance Line]
[Company Name] | [Portal Link]
This notice is provided in accordance with your lease agreement dated [Lease Start Date].
---
R14 coordinator gate: R14 must never auto-send without a human review step. Build a required "PM Approved, Send R14" checkbox on your board card. The automation should queue R14 and hold it until that box is checked. A charge notice sent in error is a tenant relations crisis.
#### Master Reference: R-Series at a Glance (R1 to R14)
| # | Trigger | Channel | Subject Line | Timing |
|---|---|---|---|---|
| R1 | Card created (any priority) | SMS + Portal | We received your maintenance request, #[WO ID] | Immediate |
| R2 | Priority = Emergency | SMS only | (no subject, SMS) | Immediate + R1 |
| R3 | After-Hours Flag = Yes | SMS only | (no subject, SMS) | Immediate + R1 |
| R4 | Tenant Responsibility Flag = Yes | Portal + Email | About your recent maintenance request, #[WO ID] | Immediate on flag (15-min coordinator review delay) |
| R5 | Stage to Dispatched | SMS + Portal | Your repair is scheduled, #[WO ID] | Immediate on stage change |
| R6 | Vendor check-in timestamp logged | SMS only | (no subject, SMS) | Immediate on timestamp |
| R7 | Work Completed timestamp logged | SMS + Portal | Your repair is complete, #[WO ID] | Immediate on timestamp |
| R8 | Stage to Pending Inspection | Portal + Email | How did we do? Quick question about your recent repair | 24 hrs after Work Completed |
| R9 | Survey score below threshold | Email only | We hear you, and we're going to make it right | Immediate on survey submit |
| R10 | Stage to Closed, Resolved | Portal only | Your request is closed, #[WO ID] | Immediate on stage change |
| R11 | Appt confirmed + Tenant not required to be home | Email + SMS | Notice of Entry: [Unit Address] \| [Appointment Date] | Min. 24 hrs before appt |
| R12 | Appointment Date = Today + Work Completed = blank | SMS + Email | Today's Reminder: Repair Appointment at [Unit Address] \| WO #[WO ID] | 8:00 AM day of appt |
| R13 | SLA Breached OR Vendor Rescheduled + Work incomplete | SMS + Email | Update on Your Repair: WO #[WO ID] \| [Unit Address] | Within 2 hrs of delay confirmed |
| R14 | Cost Recovery = Tenant Responsible + Invoice Approved | Email only | Maintenance Charge Notice: WO #[WO ID] \| [Unit Address] | Within 48 hrs of completion |
#### Tool Notes: R-Series
- AppFolio: R1 portal message, R5, R7, R8, and R10 can be built natively in the Maintenance module using automated task notifications. R8 uses AppFolio's built-in survey feature. R2, R3, R6 SMS sends require a Twilio or similar SMS integration via Zapier/Make since AppFolio's native SMS is limited to manual sends.
- Buildium: portal messages for R1, R5, R7, R10 are supported natively. Email sends for R4, R8, R9 can be templated in the Communications module. SMS for R2, R3, R6 requires an external SMS tool bridged via Zapier.
- Rentvine: supports automated portal messages and email natively across all R-series. SMS automation requires Twilio integration.
- Latchel: handles R2 and R3 natively as part of its after-hours and emergency dispatch flow. If using Latchel for emergency intake, suppress R2/R3 from your PM software to avoid duplicate sends.
- Zapier / Make: use to bridge SMS sends (R2, R3, R6) from your PM software trigger to Twilio or another SMS provider. Set WO ID and First Name as dynamic fields passed through the Zap.
- Survey tools: if your PM software does not have a native survey module (AppFolio, Buildium, etc. have one), use Typeform or Google Forms for R8. Map the response score back to your board via Zapier to trigger R9 automatically when the score falls below threshold.
- AppFolio (R11 to R14): R11 entry notice, R12 day-of reminder and R13 delay notice require Zapier/Make bridges. R14 must be manually reviewed before sending; build a coordinator gate.
- Buildium (R11 to R14): all four require external automation. Buildium's tenant portal messaging can supplement but should not replace email + SMS for legal notice messages (R11, R14).
- Rentvine (R11 to R14): Rentvine's workflow engine can handle R12 with conditional logic built in. R11 entry notice and R14 charge notice should still be reviewed by a coordinator before sending regardless of platform.
- Twilio (resident SMS): route all resident SMS through a dedicated resident-facing Twilio number, separate from internal PM alert numbers. Label it "Resident Communications" in your Twilio console. Inbound replies from residents to this number should route to your maintenance coordinator inbox or Slack channel, not a dead inbox.
### Part 2: Vendor and Tech Series (V1 to V9)
#### Global Tone Rules
Applied across all nine messages before individual rules.
- Direct and operational. Vendors are professionals; no hand-holding, no filler. Every message has a job to do.
- WO number, unit address, scope, and deadline in every single message. No exceptions.
- No tenant last name in vendor-facing messages. First name only for access coordination; protects tenant privacy.
- No cost discussion in auto-sends beyond referencing the approved estimate already on file.
- Never give vendors the owner's name or contact info. All communication routes through the PM office.
- Tone shifts by message type: Dispatch = clear and welcoming. Reminder = firm but professional. Escalation = no ambiguity. Invoice/payment = factual and process-driven.
- Email is the primary channel for vendors; it creates a paper trail. SMS is used for time-critical triggers only (emergency dispatch, same-day appointment reminders).
- Signature block on all emails: coordinator name + title, company name, direct line, and invoice submission email/portal link.
#### V1: Work Order Assignment (Standard Dispatch)
| Field | Value |
|---|---|
| Trigger | Card stage moves to Dispatched (Priority = Routine or Urgent) |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on stage change |
| Tone rule | Clear, complete, and professional. This is the vendor's full briefing. Everything they need to show up prepared is in this one message: scope, access, deadline, and what to submit when done. No follow-up questions should be necessary after reading this. SMS: confirmation nudge only; the email has the full brief. SMS just makes sure they saw it. |
---
Email
Subject: New Work Order Assigned: #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
You've been assigned a new work order. Please review the details below and confirm your acceptance by replying to this email or logging into the vendor portal.
WORK ORDER DETAILS
Work Order #: [WO ID]
Property: [Unit Address, City, State, Zip]
Unit: [Unit Number, if applicable]
Category: [Trade Category, e.g., Plumbing]
Scope of Work: [Detailed description of issue and work required, e.g., "Kitchen faucet is leaking at the base. Inspect, diagnose, and repair or replace."]
Priority: [Routine / Urgent]
Complete By: [SLA Deadline Date and Time]
ACCESS INSTRUCTIONS
Tenant First Name: [Tenant First Name]
Access Method: [e.g., Lockbox / Tenant to be present / Key at office]
Lockbox Code: [Code, if applicable]
Entry Notes: [e.g., "Side gate code is 1234. Knock first, tenant may be home."]
SCHEDULING
Please schedule your appointment and reply with your confirmed date and time window so we can notify the tenant.
If you cannot complete this work by [SLA Deadline], contact us immediately at [Coordinator Direct Line] so we can make alternate arrangements.
COMPLETION REQUIREMENTS
Before leaving the property, please:
• Take before AND after photos of the work area
• Confirm the issue is fully resolved
• Submit your invoice to [Invoice Email / Portal Link]
• Include WO #[WO ID] on your invoice
Photos and invoice must be submitted within 48 hours of job completion. Payment is processed on Net 30 terms from invoice approval.
Questions? Contact your coordinator directly:
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
---
SMS
[Company Name]: New WO assigned, #[WO ID] at [Unit Address]. Priority: [Routine/Urgent]. Due by [SLA Deadline Date]. Full details sent to your email. Reply to confirm.
Character count: ~158. If unit address is long, use street number + street name only and drop city.
#### V2: Emergency Dispatch
| Field | Value |
|---|---|
| Trigger | Card created OR stage to Dispatched, Priority = Emergency |
| Channel | SMS first, Email simultaneously |
| Timing | Immediately; both fire at the same time |
| Tone rule | Urgent and unambiguous. No pleasantries, no padding. The vendor needs to know this is happening right now and what the response window is. Every word earns its place. |
---
SMS
[Company Name] EMERGENCY: WO #[WO ID] | [Unit Address]. Issue: [One-line description, e.g., "Active water leak, kitchen"]. Respond within 30 min. Call [Coordinator Direct Line] NOW.
Character count: ~158. "Respond within 30 min" is the standard; adjust to match your emergency SLA. The coordinator direct line must be a live number during the hours this fires.
---
Email
Subject: EMERGENCY Work Order: #[WO ID] | [Unit Address]. Respond Immediately
[Vendor/Tech First Name],
This is an emergency work order requiring immediate response.
EMERGENCY WORK ORDER
Work Order #: [WO ID]
Property: [Unit Address, City, State, Zip]
Category: [Trade Category]
Issue: [Detailed description, e.g., "Active water leak under kitchen sink. Tenant reports water on floor. Shut-off location unknown."]
Priority: EMERGENCY
On-Site By: [Required On-Site Time, e.g., "Within 2 hours, by [Time]"]
ACCESS
Tenant First Name: [Tenant First Name]
Access Method: [Lockbox / Tenant present / Key at office]
Lockbox Code: [Code, if applicable]
Entry Notes: [Any critical access detail]
Call your coordinator immediately to confirm you are responding: [Coordinator Name] | [Coordinator Direct Line]
If you cannot respond within the required window, call us NOW so we can dispatch an alternate vendor. Do not delay; a resident is affected.
COMPLETION REQUIREMENTS
• Before and after photos required
• Invoice to [Invoice Email / Portal Link] within 24 hours of completion
• Include WO #[WO ID] on invoice
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
#### V3: Appointment Confirmation Request
| Field | Value |
|---|---|
| Trigger | Card stage = Dispatched AND Vendor Appointment Date field is still blank after [X hours, recommend 4 hrs for Urgent, 24 hrs for Routine] |
| Channel | Email + SMS (dual send) |
| Timing | Per delay logic above |
| Tone rule | Friendly but firm. The vendor has the assignment; this is a nudge to lock in the date and time. Not a reprimand, but not optional either. Clear deadline for their response. |
---
Email
Subject: Action Needed: Please Confirm Your Appointment | WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
We haven't yet received a confirmed appointment date and time for the work order below. Please reply with your scheduled date and time window as soon as possible so we can notify the tenant.
WORK ORDER REMINDER
Work Order #: [WO ID]
Property: [Unit Address]
Scope of Work: [Brief description]
Priority: [Routine / Urgent]
Must Complete By: [SLA Deadline Date and Time]
Please reply to this email with:
• Your confirmed appointment date
• Your arrival time window (e.g., 9 AM to 12 PM)
If you are unable to complete this work by [SLA Deadline], let us know immediately at [Coordinator Direct Line] so we can make alternate arrangements before the deadline is affected.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
---
SMS
[Company Name]: WO #[WO ID] | [Unit Address]: we still need your confirmed appointment date. Due by [SLA Deadline]. Reply or call [Coordinator Direct Line].
Character count: ~152.
#### V4: Same-Day Appointment Reminder
| Field | Value |
|---|---|
| Trigger | Vendor Appointment Date = Today |
| Channel | SMS + Email (dual send) |
| Timing | Fires at 7:00 AM on the day of the appointment |
| Tone rule | Practical and precise. The vendor knows the job; this is a same-day confirmation of the key details they need in the field. Access code, time window, and what to do when done. No fluff. |
---
SMS
[Company Name]: Reminder, WO #[WO ID] at [Unit Address] today, [Time Window]. Access: [Lockbox Code / "Tenant present"]. Submit photos + invoice same day. Questions: [Coordinator Direct Line].
Character count: ~158. If lockbox code pushes over 160, drop the "Questions:" line; the coordinator number is in the email.
---
Email
Subject: Today's Appointment Reminder: WO #[WO ID] | [Unit Address] | [Time Window]
Hi [Vendor/Tech First Name],
This is your reminder for today's scheduled work order.
TODAY'S JOB DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Appointment: Today, [Date] | [Time Window]
Scope of Work: [Brief description]
Must Complete By: [SLA Deadline, same day or noted]
ACCESS
Access Method: [Lockbox / Tenant present / Key at office]
Lockbox Code: [Code, if applicable]
Entry Notes: [e.g., "Park on street. Side entrance. Knock before entering."]
WHEN YOU'RE DONE
• Before and after photos, required before leaving
• Invoice to [Invoice Email / Portal Link] within 48 hours
• WO #[WO ID] must appear on your invoice
Running late or need to reschedule? Call us immediately: [Coordinator Name] | [Coordinator Direct Line]
A tenant is expecting you today. Please do not no-show without calling first.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
#### V5: Completion Photo and Invoice Submission Reminder
| Field | Value |
|---|---|
| Trigger | Work Completed timestamp logged AND Completion Photos = Not Uploaded OR Invoice State = Not Received after 24 hours |
| Channel | Email + SMS (dual send) |
| Timing | 24 hours after Work Completed timestamp |
| Tone rule | Matter-of-fact and process-focused. The vendor did the work; this is a clean reminder that the job isn't closed until the paperwork is in. No accusatory language. Just clear steps and a hard deadline. |
---
Email
Subject: Action Required: Photos and Invoice Needed | WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
Thank you for completing the work at [Unit Address]. We're in the final step of closing out this work order and need the following from you to process payment.
OUTSTANDING ITEMS, WO #[WO ID]
Work Order #: [WO ID]
Property: [Unit Address]
Work Completed: [Completion Date]
Please submit the following by [Submission Deadline, recommend 48 hrs from Work Completed]:
• BEFORE and AFTER photos of the work area. Submit to: [Photo Upload Link / Email]
• INVOICE for completed work. Submit to: [Invoice Email / Portal Link]. Include WO #[WO ID] on the invoice. Itemize all labor and materials separately.
Important: payment cannot be processed until both photos and invoice are received and approved.
Already submitted? Please disregard this message; our team may still be processing your submission.
Questions? Contact us at [Coordinator Direct Line].
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
---
SMS
[Company Name]: WO #[WO ID] | [Unit Address]: we still need your before/after photos and invoice to process payment. Submit by [Deadline]. Email: [Invoice Email].
Character count: ~158. If invoice email address is long, replace with a short URL or "reply to this message."
#### V6: Invoice Mismatch / Correction Request
| Field | Value |
|---|---|
| Trigger | Invoice State flagged as Mismatch |
| Channel | Email |
| Timing | Immediately on flag set by coordinator |
| Tone rule | Professional and specific. This is a billing dispute; keep it factual, not confrontational. State exactly what doesn't match, what is needed, and by when. No vague language. No accusations. Give the vendor a clear path to resolution. |
---
Email
Subject: Invoice Review Needed: WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
Thank you for submitting your invoice for WO #[WO ID] at [Unit Address]. Our team has reviewed it and found a discrepancy that needs to be resolved before we can process payment.
INVOICE DISCREPANCY DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Invoice Submitted: [Invoice Date]
Invoice Amount: $[Submitted Amount]
Approved Estimate: $[Approved Estimate on File]
ISSUE IDENTIFIED
[Select / fill the applicable reason:]
☐ Invoice total exceeds the approved estimate by $[Variance Amount]. Any amount above the approved estimate requires prior authorization.
☐ Line item(s) not included in the original scope of work: [Describe specific line item(s)]
☐ Labor hours billed ([X hrs]) do not match the scope of work on file.
☐ Invoice is missing required itemization; labor and materials must be listed separately.
☐ WO #[WO ID] is missing from the invoice.
☐ Other: [Coordinator to specify]
ACTION REQUIRED BY [Correction Deadline, recommend 3 business days]
Please resubmit a corrected invoice to [Invoice Email / Portal Link] addressing the item(s) above.
If you believe there is an error in our review, or if additional work was required that was not in the original scope, please contact us directly to discuss before resubmitting.
Important: payment will be held until a corrected invoice is received and approved.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
The checkbox section should be pre-filled by the coordinator before this auto-send fires. Build a required "Mismatch Reason" field on the board card that populates the correct line in this template. Do not send a blank checklist.
#### V7: SLA Deadline Warning (Work Not Yet Complete)
| Field | Value |
|---|---|
| Trigger | SLA Status moves to At Risk AND Work Completed = blank |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on SLA status change |
| Tone rule | Firm and urgent. The deadline is approaching and the work isn't done. This is not a gentle nudge; it is a clear operational alert. Professional, but no softening. The vendor needs to act or communicate right now. |
---
Email
Subject: Urgent: Deadline Approaching | WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
This is an urgent notice regarding work order #[WO ID] at [Unit Address]. Our records show this work has not yet been marked complete, and the deadline is approaching.
WORK ORDER STATUS
Work Order #: [WO ID]
Property: [Unit Address]
Scope of Work: [Brief description]
Priority: [Routine / Urgent / Emergency]
SLA Deadline: [SLA Deadline Date and Time]
Time Remaining: [X hours / X days]
Current Status: Not yet complete
ACTION REQUIRED, IMMEDIATELY
• If work is scheduled and on track: reply with your confirmed completion date and time so we can update our records.
• If you are unable to meet the deadline: call [Coordinator Direct Line] immediately. Do not wait; we need time to arrange alternate coverage if necessary.
• If work has already been completed: submit your photos and invoice to [Invoice Email / Portal Link] and reply to this email so we can update the record.
Important: missing this deadline affects a resident and is tracked in your vendor performance record.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
---
SMS
[Company Name] URGENT: WO #[WO ID] | [Unit Address] deadline is [SLA Deadline]. Work not yet logged complete. Call [Coordinator Direct Line] NOW or reply with update.
Character count: ~157.
#### V8: SLA Breach Notification (Deadline Passed)
| Field | Value |
|---|---|
| Trigger | SLA Status moves to Breached AND Work Completed = blank |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on SLA status change |
| Tone rule | No ambiguity, no softening. The deadline has passed and a resident is affected. This message is direct, factual, and consequence-aware, but still professional. Not hostile. The vendor needs to understand the severity and respond within a defined window or risk reassignment. |
---
SMS
[Company Name]: WO #[WO ID] | [Unit Address] is past its deadline. Work not logged complete. Call [Coordinator Direct Line] immediately or this job will be reassigned.
Character count: ~155. "Reassigned" is intentional; it is the real consequence and vendors need to see it plainly.
---
Email
Subject: Past Due: Immediate Response Required | WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
Work order #[WO ID] at [Unit Address] has passed its required completion deadline and our records show it has not been marked complete.
PAST DUE WORK ORDER
Work Order #: [WO ID]
Property: [Unit Address]
Scope of Work: [Brief description]
Priority: [Routine / Urgent / Emergency]
SLA Deadline: [SLA Deadline Date and Time]
Status: PAST DUE, not complete
YOU MUST DO ONE OF THE FOLLOWING WITHIN THE NEXT [2 / 4] HOURS:
1. Call [Coordinator Direct Line] to confirm a same-day or next-business-day completion date and time.
2. If work is already done, submit your before/after photos and invoice to [Invoice Email / Portal Link] immediately and reply to this email.
3. If you cannot complete this work, call us NOW at [Coordinator Direct Line] so we can reassign to another vendor without further delay to the resident.
Important: this breach is logged in your vendor performance record. Repeated missed deadlines are reviewed quarterly and may affect future work order assignments.
A resident is waiting. Please respond immediately.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
The [2 / 4] hour response window should be set based on priority: 2 hours for Emergency/Urgent breaches, 4 hours for Routine. Make this a conditional field in your automation. This message simultaneously fires escalation alert E3 to the coordinator and E4 to the PM; do not suppress those internal alerts when V8 sends.
#### V9: Payment Processed Confirmation
| Field | Value |
|---|---|
| Trigger | Invoice State moves to Submitted to Accounting AND payment is queued |
| Channel | Email |
| Timing | Immediately on Invoice State change |
| Tone rule | Clean, positive, and transactional. The job is done, the paperwork cleared; confirm it professionally. Give the vendor exactly what they need for their records: WO number, amount, and expected payment date. No filler. Ends the relationship loop on a good note. |
---
Email
Subject: Payment Confirmed: WO #[WO ID] | [Unit Address]
Hi [Vendor/Tech First Name],
Your invoice for work order #[WO ID] has been reviewed, approved, and submitted for payment.
PAYMENT DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Scope Completed: [Brief description]
Invoice Amount: $[Approved Invoice Amount]
Invoice Approved: [Approval Date]
Expected Payment: On or before [Payment Date, Net 30 from Approval Date]
Payment Method: [Check / ACH / Portal, per your vendor agreement]
Please retain this email for your records along with your invoice copy. If you have not received payment by [Payment Date] or have questions about this transaction, contact us at [Coordinator Direct Line] or [Invoice Submission Email].
Thank you for your work on this one. We appreciate the partnership.
[Coordinator Name] | [Coordinator Title]
[Coordinator Direct Line]
[Company Name] | [Invoice Submission Email]
SMS is intentionally omitted for V9. Payment confirmation is a record-keeping document; email only ensures the vendor has a paper trail. If your accounting system generates its own payment confirmation, suppress V9 to avoid a duplicate send and use the accounting system's native notification instead.
#### Master Reference: V-Series at a Glance
| # | Trigger | Channel | Subject Line | Timing |
|---|---|---|---|---|
| V1 | Stage to Dispatched (Routine/Urgent) | Email + SMS | New Work Order Assigned: #[WO ID] \| [Unit Address] | Immediate |
| V2 | Priority = Emergency, any stage change | SMS + Email | EMERGENCY Work Order: #[WO ID] \| [Unit Address]. Respond Immediately | Immediate |
| V3 | Dispatched + Appointment Date blank after [4/24 hrs] | Email + SMS | Action Needed: Please Confirm Your Appointment \| WO #[WO ID] | Per delay logic |
| V4 | Appointment Date = Today | SMS + Email | Today's Appointment Reminder: WO #[WO ID] \| [Unit Address] \| [Time Window] | 7:00 AM day-of |
| V5 | Work Completed + photos/invoice missing after 24 hrs | Email + SMS | Action Required: Photos and Invoice Needed \| WO #[WO ID] | 24 hrs post-completion |
| V6 | Invoice State = Mismatch | Email only | Invoice Review Needed: WO #[WO ID] \| [Unit Address] | Immediate on flag |
| V7 | SLA Status to At Risk + Work Completed = blank | Email + SMS | Urgent: Deadline Approaching \| WO #[WO ID] \| [Unit Address] | Immediate on status change |
| V8 | SLA Status to Breached + Work Completed = blank | SMS + Email | Past Due: Immediate Response Required \| WO #[WO ID] \| [Unit Address] | Immediate on status change |
| V9 | Invoice State to Submitted to Accounting | Email only | Payment Confirmed: WO #[WO ID] \| [Unit Address] | Immediate on state change |
#### Tool Notes: V-Series
- AppFolio: V1 and V4 can be built using AppFolio's native vendor work order notifications. V2 emergency SMS requires Twilio via Zapier/Make. V5, V6, V9 are best handled outside AppFolio via your automation platform since AppFolio's native vendor messaging does not support conditional invoice-state triggers natively.
- Buildium: V1 email sends natively via the Maintenance module vendor assignment. V3, V5, V6, V7, V8 require Zapier/Make bridges since Buildium does not support conditional delay triggers or invoice-state automations natively.
- Rentvine: supports V1, V3, V4, and V9 natively with strong vendor portal messaging. V2 emergency SMS and V7/V8 SLA breach alerts require external automation bridges.
- Latchel: if using Latchel for vendor dispatch, V1 and V2 are handled natively by Latchel's dispatch system. Suppress your PM software's V1/V2 sends to avoid duplicates. V5 through V9 still need to fire from your PM software or automation platform since Latchel does not manage invoice or payment workflows.
- Zapier / Make: use multi-step Zaps/scenarios for V7 and V8: Step 1 watches for SLA status field change, then Step 2 checks Work Completed = blank, then Step 3 fires SMS via Twilio, then Step 4 fires email via Gmail/Outlook, then Step 5 triggers the internal escalation alert to the coordinator (E3/E4). All five steps must be in the same scenario to keep the timing tight.
- Twilio: recommended SMS provider for V2, V3, V7, V8 where speed is critical. Set sender ID to your company name or main number, not a random short code, so vendors recognize it immediately.
- Accounting system note: V9 should be coordinated with your accounting system's own payment notification. If your system (QuickBooks, AppFolio accounting, Buildium ledger) sends its own payment confirmation, suppress V9 or use V9 only as a backup if the accounting system notification fails. Never send both; vendors do not need two payment confirmations.
### Part 3: Owner Series (O2 to O8)
#### Global Tone Rules
- Professional, transparent, and reassuring. Owners are investors. Every message should reinforce that their asset is being managed with care, precision, and full accountability.
- Never alarm unnecessarily. State facts, give context, tell them what is already being handled, and tell them what, if anything, you need from them.
- Portal-first. All documents, photos, invoices, and receipts live in the portal. Every email references it.
- Approval requests have a hard deadline and a stated consequence, either "we will proceed" or "we will hold", so owners know exactly what happens if they don't respond.
- Never share tenant last name, screening data, or vendor pricing markups in owner-facing messages.
- Emergency messages lead with what is already being handled, not with the problem alone. Owners should feel managed, not panicked.
- Signature block on all emails: PM name + title, company name, direct line, and portal link.
#### O2: Approval Request (Above Threshold, Non-Emergency)
| Field | Value |
|---|---|
| Trigger | Work Order created OR stage to Awaiting Owner Approval AND Priority = Routine or Urgent AND Estimated Cost > [Owner Approval Threshold] |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on trigger |
| Tone rule | Informative and action-oriented. Give the owner everything they need to say yes or ask a question: issue description, photos, estimate, and a clear deadline. Make the approval path frictionless. State the consequence of non-response plainly but without pressure. |
---
Email
Subject: Your Approval Needed: Repair at [Unit Address] | WO #[WO ID]
Attachments: Vendor estimate (PDF) | Issue photos (attached or portal link)
Hi [Owner First Name],
A maintenance issue has been reported at [Unit Address] that requires your approval before we can proceed. Please review the details below and respond by the deadline noted.
WORK ORDER DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Issue Reported: [Detailed description, e.g., "HVAC unit is not producing cool air. Tenant reports indoor temp at 84°F. Vendor has inspected and recommends full compressor replacement."]
Priority: [Routine / Urgent]
Vendor Estimate: $[Estimated Amount] (Itemized estimate attached and uploaded to your portal)
PHOTOS
Issue photos are attached to this email and available in your owner portal under: Documents, then Maintenance, then WO #[WO ID]. [Portal Link]
YOUR APPROVAL DEADLINE
Please respond by: [Approval Deadline, recommend 48 hrs for Urgent, 72 hrs for Routine]
To approve, simply reply to this email with "Approved" or log into your portal and approve directly.
If we do not receive your response by [Approval Deadline], we will [hold the work order until we hear from you / proceed with the repair to protect the property and tenant, select per your PMA terms].
Questions? Call or email us directly; we're happy to walk through the estimate with you.
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
---
SMS
[Company Name]: Approval needed for WO #[WO ID] at [Unit Address]. Est. cost: $[Amount]. Deadline: [Approval Deadline]. Details + photos in your portal: [Portal Link]. Reply "Approved" or call [PM Direct Line].
Character count: ~195. Trim portal URL with a shortener. If estimate amount pushes over 160 chars, drop "Details + photos in your portal" and keep the link only.
#### O3: Emergency Repair Notification (Action Already Taken)
| Field | Value |
|---|---|
| Trigger | Work Order created AND Priority = Emergency |
| Channel | SMS first, Email simultaneously |
| Timing | Immediately; both fire at the same time |
| Tone rule | Lead with what is already being handled. Owners should read the first sentence and feel that their PM is in control. State the issue, state the action taken, state the cost range, and tell them what, if anything, they need to do. Keep it calm, factual, and complete. |
---
SMS
[Company Name]: Emergency at [Unit Address]: [One-line issue, e.g., "active water leak, kitchen"]. Vendor dispatched. Est. cost: $[Range]. Full details emailed. Call [PM Direct Line] with questions.
Character count: ~158. "Vendor dispatched" is the key phrase; it signals control immediately.
---
Email
Subject: Emergency Repair in Progress: [Unit Address] | WO #[WO ID]
Attachments: Issue photos (if available at time of send; note if pending)
Hi [Owner First Name],
We are writing to inform you of an emergency maintenance situation at [Unit Address]. Our team has already responded and a vendor is en route.
EMERGENCY DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Issue: [Detailed description, e.g., "Active water leak reported under the kitchen sink. Tenant reports water on the floor. Main water shut-off has been identified. Plumber dispatched."]
Priority: Emergency
Action Taken: Vendor dispatched, on-site by [ETA Time]
Estimated Cost: $[Low] to $[High] (final invoice to follow upon completion)
PHOTOS
[Photos attached / Photos will be uploaded to your portal upon vendor arrival, check portal for updates: [Portal Link]]
WHAT HAPPENS NEXT
• Vendor will assess and complete the repair
• Before and after photos will be uploaded to your portal
• Final invoice will be submitted for your records within 48 hours of completion
• Cost will be deducted from your reserve fund per your PMA authorization for emergency repairs
No action is required from you at this time. We will send a completion update once the work is done.
If you have questions or would like to speak with us directly, please call [PM Direct Line].
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
#### O4: Owner Unresponsive, Proceeding with Repair
| Field | Value |
|---|---|
| Trigger | Approval Deadline passed AND Owner Approval Status = No Response AND Priority = Urgent (or per PMA terms) |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on deadline expiration |
| Tone rule | Factual and firm, but not confrontational. The PM is doing their job per the PMA. State what was requested, when, that no response was received, and what action is now being taken. Document this message as part of the audit trail. |
---
Email
Subject: Update: Proceeding with Repair at [Unit Address] | WO #[WO ID]
Attachments: Original estimate (PDF) | Original approval request (reference)
Hi [Owner First Name],
We are following up on our approval request sent on [Original Request Date] regarding work order #[WO ID] at [Unit Address]. We have not received a response by the deadline of [Approval Deadline].
WORK ORDER RECAP
Work Order #: [WO ID]
Property: [Unit Address]
Issue: [Brief description]
Approved Estimate: $[Estimated Amount]
Original Request: [Date Sent]
Response Deadline: [Approval Deadline, passed]
ACTION BEING TAKEN
Per Section [X] of your Property Management Agreement, we are authorized to proceed with necessary repairs when owner approval is not received within the required timeframe and tenant habitability or property condition is at risk.
We are proceeding with the repair effective today. The vendor has been dispatched and work is expected to be completed by [Expected Completion Date]. The final invoice will be uploaded to your portal and deducted from your reserve fund upon completion.
If you have questions or concerns, please contact us immediately at [PM Direct Line].
This email serves as formal notice of action taken and is logged in your property file.
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
---
SMS
[Company Name]: No response received for WO #[WO ID] at [Unit Address] by [Deadline]. Per your PMA, we are proceeding with the repair. Est. $[Amount]. Full details emailed. Call [PM Direct Line] with questions.
#### O5: Owner Declined Repair, Risk Acknowledgment
| Field | Value |
|---|---|
| Trigger | Owner Approval Status = Declined |
| Channel | Email |
| Timing | Immediately on status change |
| Tone rule | Professional, measured, and protective of the PM company. This message documents the owner's decision and clearly states the potential consequences (habitability, tenant rights, liability) without being accusatory. This email is a legal record. Every word matters. |
---
Email
Subject: Repair Decision Logged: Action Required to Acknowledge | WO #[WO ID] | [Unit Address]
Hi [Owner First Name],
Thank you for responding to our repair request for work order #[WO ID] at [Unit Address]. We have logged your decision to decline the repair at this time.
DECLINED REPAIR, ON FILE
Work Order #: [WO ID]
Property: [Unit Address]
Issue: [Description of repair requested]
Estimated Cost: $[Estimated Amount]
Decision: Declined by owner on [Date]
IMPORTANT, PLEASE READ
We want to make sure you are fully informed of the potential implications of deferring this repair:
• Habitability: depending on the nature of the issue, deferred repairs may affect the property's habitability under [State] landlord-tenant law.
• Tenant Rights: tenants may have the right to request rent reduction, repair-and-deduct, or lease termination if habitability is affected.
• Property Condition: deferred maintenance may result in greater damage and higher repair costs over time.
• Liability: [Company Name] cannot be held responsible for damages, tenant claims, or legal actions arising from a repair that was recommended and declined by the owner.
ACKNOWLEDGMENT REQUIRED
Please reply to this email confirming that you have read and understood the above, and that you are choosing to defer this repair at this time. Your reply will be logged in your property file as formal acknowledgment.
If you would like to reconsider and approve the repair, simply reply "Approved" and we will dispatch the vendor immediately.
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
SMS is intentionally omitted for O5. This is a legal record: email only, and it must be logged in the PM software file immediately upon send. Do not auto-archive this one. Flag it for coordinator review.
#### O6: Work Order Completed, Closeout Notice
| Field | Value |
|---|---|
| Trigger | Work Order Stage to Completed AND Invoice State = Approved |
| Channel | Email |
| Timing | Within 48 hours of Work Completed timestamp; recommend immediate on stage change |
| Tone rule | Positive, complete, and tidy. The job is done; confirm it professionally. Give the owner the full picture: what was done, what it cost, what's in the portal, and what the reserve balance looks like. No loose ends. |
---
Email
Subject: Repair Complete: WO #[WO ID] | [Unit Address]
Attachments: Completed invoice (PDF) | Before and after photos (attached or portal link)
Hi [Owner First Name],
We're pleased to let you know that the maintenance work at [Unit Address] has been completed and the work order is now closed.
COMPLETION SUMMARY
Work Order #: [WO ID]
Property: [Unit Address]
Work Completed: [Completion Date]
Scope of Work: [Description of work performed, e.g., "Kitchen faucet replaced. New Moen cartridge installed. Leak confirmed resolved."]
Vendor: [Vendor Company Name]
Final Invoice: $[Final Invoice Amount] (Itemized invoice attached and uploaded to your portal)
PHOTOS
Before and after photos are attached to this email and available in your portal under: Documents, then Maintenance, then WO #[WO ID]. [Portal Link]
FINANCIAL SUMMARY
Invoice Amount: $[Final Invoice Amount]
Deducted From: Owner Reserve Fund
Reserve Balance After Deduction: $[Updated Reserve Balance]
[If reserve is below threshold:] Your reserve balance is now below the recommended minimum of $[Threshold]. A replenishment request will follow separately.
All documentation is available in your owner portal at any time: [Portal Link]
Thank you for your continued trust in [Company Name]. Please don't hesitate to reach out with any questions.
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
The reserve balance line is critical; pull this dynamically from your accounting system. If your PM software cannot populate this field automatically, flag it for manual coordinator review before the email sends. Never send a blank or incorrect reserve balance to an owner.
#### O7: Reserve Fund Replenishment Request
| Field | Value |
|---|---|
| Trigger | Reserve Balance < [Minimum Threshold] after invoice deduction OR Reserve Balance field updated below threshold |
| Channel | Email + SMS (dual send) |
| Timing | Immediately on threshold breach, or bundled with O6 if triggered by same invoice |
| Tone rule | Matter-of-fact and non-alarming. This is a routine financial housekeeping request, not a crisis. State the balance, state the minimum, state what is needed, and make the payment path easy. Owners who maintain healthy reserves have fewer surprises. |
---
Email
Subject: Reserve Fund Replenishment Needed: [Unit Address]
Hi [Owner First Name],
Following a recent maintenance expense at [Unit Address], your reserve fund balance has fallen below the minimum required level.
RESERVE FUND STATUS
Property: [Unit Address]
Current Balance: $[Current Reserve Balance]
Minimum Required: $[Minimum Threshold per PMA]
Replenishment Needed: $[Difference]
WHY THIS MATTERS
Your reserve fund ensures we can respond quickly to maintenance needs, including emergencies, without delays caused by waiting for fund transfers. A healthy reserve protects your property and your tenant relationship.
HOW TO REPLENISH
Please submit a payment of $[Replenishment Amount] via:
• Owner Portal (fastest): [Portal Link]
• ACH / Bank Transfer: [Banking Details]
• Check payable to: [Company Name]. Mail to: [Mailing Address]
Please replenish by: [Replenishment Deadline, recommend 10 business days]
If you have questions about this balance or would like to discuss your reserve strategy, please contact us at [PM Direct Line].
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
---
SMS
[Company Name]: Your reserve at [Unit Address] is now $[Balance], below the $[Threshold] minimum. Please replenish $[Amount] by [Deadline]. Pay via portal: [Portal Link] or call [PM Direct Line].
#### O8: SLA Breach Owner Notification
| Field | Value |
|---|---|
| Trigger | SLA Status = Breached AND Work Completed = blank AND Owner Notification Sent = false |
| Channel | Email |
| Timing | Same day as breach; within 2 hours of E3 firing internally |
| Tone rule | Transparent and accountable. The PM is informing the owner of a delay before the owner finds out another way. Own it, explain what is being done to resolve it, and give a revised timeline. Do not over-apologize; state facts and actions. |
---
Email
Subject: Repair Delay Update: WO #[WO ID] | [Unit Address]
Hi [Owner First Name],
We want to keep you informed of a delay affecting work order #[WO ID] at [Unit Address].
DELAY DETAILS
Work Order #: [WO ID]
Property: [Unit Address]
Issue: [Brief description]
Original Deadline: [SLA Deadline Date]
Current Status: Not yet complete
Reason for Delay: [e.g., "Vendor has not confirmed completion. We are actively following up and have issued a deadline warning to the vendor." / "Part on order, expected [Date]." / "Vendor rescheduled, new date confirmed as [Date]."]
WHAT WE ARE DOING
• Vendor has been formally notified of the breach and given a [X]-hour response window
• If vendor does not respond, we will reassign to an alternate vendor
• Revised estimated completion: [Revised Completion Date]
• Your tenant has been notified of the delay and updated timeline
NO ACTION REQUIRED FROM YOU
We are managing this actively. You will receive a completion notice with photos and invoice as soon as the work is done.
If you have questions or concerns, please contact us directly at [PM Direct Line].
[PM Name] | [PM Title]
[PM Direct Line]
[Company Name] | [Portal Link]
O8 fires AFTER E3 (internal PM alert), never before. The PM must know first, confirm the reason for delay, and populate the "Reason for Delay" field before this sends to the owner. Build a required coordinator-fill field into your board that gates this send. A blank reason field going to an owner is worse than no email at all.
#### Master Reference: O-Series at a Glance
| # | Trigger | Channel | Subject Line | Timing |
|---|---|---|---|---|
| O2 | Stage to Awaiting Approval + Cost > Threshold (Routine/Urgent) | Email + SMS | Your Approval Needed: Repair at [Unit Address] \| WO #[WO ID] | Immediate |
| O3 | Priority = Emergency, WO created | SMS + Email | Emergency Repair in Progress: [Unit Address] \| WO #[WO ID] | Immediate |
| O4 | Approval Deadline passed + No Response | Email + SMS | Update: Proceeding with Repair at [Unit Address] \| WO #[WO ID] | Immediate on deadline expiration |
| O5 | Owner Approval = Declined | Email only | Repair Decision Logged: Action Required to Acknowledge \| WO #[WO ID] | Immediate on status change |
| O6 | Stage to Completed + Invoice Approved | Email only | Repair Complete: WO #[WO ID] \| [Unit Address] | Immediate on stage change |
| O7 | Reserve Balance < Threshold | Email + SMS | Reserve Fund Replenishment Needed: [Unit Address] | Immediate on threshold breach |
| O8 | SLA = Breached + Work Completed = blank | Email only | Repair Delay Update: WO #[WO ID] \| [Unit Address] | Within 2 hrs of E3 firing |
### Part 4: PM Escalation Alerts (E1 to E8)
#### Global Tone Rules
- One line. Maximum two. PMs are moving fast; every alert must be scannable in under three seconds.
- Lead with the trigger, follow with the exact fields needed to act. No context, no explanation, just the data.
- Slack format: bold the trigger label. Use code style for WO ID, address, and amounts. A bracketed severity tag at the front signals severity at a glance.
- SMS format: all caps trigger label, then fields. No emoji; SMS rendering is inconsistent across devices.
- Every alert names the property, WO number, and the one action the PM must take. Nothing vague.
- E-series never goes to owners or tenants. Internal only: Slack channel or PM direct SMS.
#### E1: Emergency Work Order Created
| Field | Value |
|---|---|
| Trigger | WO created AND Priority = Emergency |
| Fires to | Maintenance Coordinator + Property Manager (both) |
| Channel | Slack + SMS simultaneously |
| Timing | Immediate |
---
Slack: [EMERGENCY] EMERGENCY WO CREATED: WO #[WO ID] | [Unit Address] | Issue: [One-line description] | Vendor dispatched: [Yes / No, confirm now] | Owner notified: [Yes / No] | Action: Confirm vendor ETA and verify O3 sent.
SMS: EMERGENCY WO #[WO ID] | [Unit Address] | [Issue]. Vendor dispatched? Confirm ETA + verify O3 sent to owner. Call [Coordinator Name] if not dispatched.
#### E2: Owner Approval Request Sent, Clock Running
| Field | Value |
|---|---|
| Trigger | O2 sent AND Approval Deadline set |
| Fires to | Assigned Coordinator |
| Channel | Slack |
| Timing | Immediate on O2 send |
---
Slack: [CLOCK] APPROVAL CLOCK RUNNING: WO #[WO ID] | [Unit Address] | Owner: [Owner First Name] | Estimate: $[Amount] | Deadline: [Approval Deadline Date/Time] | Action: Monitor for response; if no reply by [Deadline minus 4 hrs], call owner directly.
#### E3: SLA Breach, Work Not Complete
| Field | Value |
|---|---|
| Trigger | SLA Status to Breached AND Work Completed = blank |
| Fires to | Maintenance Coordinator + Property Manager |
| Channel | Slack + SMS simultaneously |
| Timing | Immediate on breach |
---
Slack: [BREACH] SLA BREACH: WO #[WO ID] | [Unit Address] | Vendor: [Vendor Name] | Deadline was: [SLA Deadline] | Status: Not complete | Action: Call vendor NOW; if no response in 2 hrs, reassign. Populate delay reason field to gate O8 to owner.
SMS: SLA BREACH: WO #[WO ID] | [Unit Address] | Vendor: [Vendor Name]. Call vendor NOW. 2-hr window before reassign. Fill delay reason to release O8.
#### E4: Vendor No-Show / Appointment Missed
| Field | Value |
|---|---|
| Trigger | Appointment Date = Today AND Vendor Confirmed Arrival = No by [Appointment End Time + 1 hr] |
| Fires to | Maintenance Coordinator |
| Channel | Slack + SMS simultaneously |
| Timing | 1 hour after scheduled appointment window closes |
---
Slack: [NO-SHOW] VENDOR NO-SHOW: WO #[WO ID] | [Unit Address] | Vendor: [Vendor Name] | Appt was: [Scheduled Time Window] | Tenant waiting: [Yes / Unknown] | Action: Call vendor immediately; if unreachable, reassign and notify tenant of new date. Log no-show in vendor performance record.
SMS: VENDOR NO-SHOW: WO #[WO ID] | [Unit Address] | [Vendor Name] missed [Time Window]. Call now; reassign if unreachable. Log in vendor record.
#### E5: Owner Unresponsive, Approval Deadline Expired
| Field | Value |
|---|---|
| Trigger | Approval Deadline passed AND Owner Approval Status = No Response |
| Fires to | Property Manager |
| Channel | Slack + SMS simultaneously |
| Timing | Immediate on deadline expiration; fires before O4 sends |
---
Slack: [WARNING] OWNER UNRESPONSIVE: WO #[WO ID] | [Unit Address] | Owner: [Owner First Name] | Request sent: [Original Request Date] | Deadline: [Approval Deadline, PASSED] | Estimate: $[Amount] | Action: Confirm PMA authorization to proceed, then release O4. Do NOT let O4 send without PM sign-off.
SMS: OWNER NO RESPONSE: WO #[WO ID] | [Unit Address] | [Owner First Name] | Deadline passed. Confirm PMA auth to proceed before O4 releases. Call PM now.
E5 must fire BEFORE O4 auto-sends. Build a PM confirmation step, a required checkbox or reply, that gates O4. O4 should never send without a human PM confirming the PMA clause applies. This is a liability checkpoint.
#### E6: Owner Declined Repair
| Field | Value |
|---|---|
| Trigger | Owner Approval Status = Declined |
| Fires to | Property Manager |
| Channel | Slack |
| Timing | Immediate on status change; fires before O5 sends |
---
Slack: [DECLINED] OWNER DECLINED REPAIR: WO #[WO ID] | [Unit Address] | Owner: [Owner First Name] | Issue: [Brief description] | Estimate: $[Amount] | Action: Review for habitability risk before O5 sends; if issue affects habitability, call owner directly before releasing decline acknowledgment. Log decision in property file.
E6 gates O5. If the PM flags the issue as a habitability risk, O5 should be held and the PM should call the owner directly before any written notice goes out. Build a "Habitability Risk" toggle on the board card that suppresses O5 until cleared.
#### E7: Invoice Mismatch Flagged
| Field | Value |
|---|---|
| Trigger | Invoice State = Mismatch |
| Fires to | Maintenance Coordinator |
| Channel | Slack |
| Timing | Immediate on flag |
---
Slack: [INVOICE] INVOICE MISMATCH: WO #[WO ID] | [Unit Address] | Vendor: [Vendor Name] | Submitted: $[Submitted Amount] | Approved Estimate: $[Approved Amount] | Variance: $[Difference] | Action: Select mismatch reason in board card to release V6 to vendor; do not send V6 with blank reason field.
#### E8: Reserve Fund Below Threshold
| Field | Value |
|---|---|
| Trigger | Reserve Balance < [Minimum Threshold] |
| Fires to | Assigned Coordinator + Property Manager |
| Channel | Slack |
| Timing | Immediate on threshold breach |
---
Slack: [RESERVE] RESERVE LOW: [Unit Address] | Owner: [Owner First Name] | Current Balance: $[Balance] | Minimum: $[Threshold] | Shortfall: $[Difference] | Action: Verify O7 queued to send; confirm replenishment deadline is set in board card before release.
#### Master Reference: E-Series at a Glance
| # | Trigger | Fires To | Channel | Action Required |
|---|---|---|---|---|
| E1 | Emergency WO created | Coordinator + PM | Slack + SMS | Confirm vendor dispatched + O3 sent to owner |
| E2 | O2 sent, approval clock running | Coordinator | Slack | Monitor; call owner if no reply by [Deadline minus 4 hrs] |
| E3 | SLA Breached + Work incomplete | Coordinator + PM | Slack + SMS | Call vendor; 2-hr window; fill delay reason to release O8 |
| E4 | Vendor no-show, 1 hr past window | Coordinator | Slack + SMS | Call vendor; reassign if unreachable; log in vendor record |
| E5 | Approval deadline passed, no owner response | PM | Slack + SMS | Confirm PMA auth; gates O4; PM sign-off required |
| E6 | Owner declined repair | PM | Slack | Review habitability risk; gates O5; call owner if risk present |
| E7 | Invoice mismatch flagged | Coordinator | Slack | Select mismatch reason in board; gates V6 |
| E8 | Reserve balance below threshold | Coordinator + PM | Slack | Verify O7 queued; confirm replenishment deadline set |
#### Tool Notes: O and E Series
- AppFolio: O2, O3, and O6 can be partially built using AppFolio's native owner notification settings under Maintenance, then Work Orders. However, AppFolio does not support conditional approval-deadline logic or reserve-threshold triggers natively. O4, O5, O7, O8, and all E-series alerts require Zapier or Make bridges pulling from AppFolio's API or webhook layer.
- Buildium: O2 and O6 can be triggered via Buildium's native maintenance notification emails, but merge field depth is limited; estimate amounts and reserve balances will need to be manually inserted or pulled via Zapier. E-series alerts are fully external and require a Zapier/Make + Slack integration since Buildium has no native internal alert system.
- Rentvine: strongest native support for O-series among current PM platforms. Rentvine's workflow engine can handle O2, O3, O6, and O7 with conditional logic built directly in the platform. E-series Slack alerts still require an external automation bridge via Zapier or Make + Twilio for SMS.
- Slack: create a dedicated #maintenance-alerts channel for E1, E3, E4 (high urgency) and a separate #maintenance-ops channel for E2, E5, E6, E7, E8 (action-required but not time-critical). Mixing all eight into one channel causes alert fatigue; coordinators start ignoring them within two weeks.
- Zapier / Make: E5 is the most critical scenario to build carefully. The automation must: (1) detect deadline expiration, (2) fire E5 to PM Slack + SMS, (3) pause O4, (4) wait for PM confirmation field = true, (5) then release O4. A linear Zap cannot do this; use Make's scenario branching or a Zapier multi-step Zap with a delay + conditional path. Test this scenario in staging before going live.
- Twilio: all E-series SMS alerts should route through a dedicated internal Twilio number, separate from the tenant and vendor-facing numbers. Label it clearly in your Twilio console (e.g., "PM Internal Alerts"). This prevents coordinators from confusing internal alerts with inbound tenant or vendor replies.
- Reserve Balance Field: O6 and O7 both require a live reserve balance pull. If your PM software does not expose this via API, build a manual "Reserve Balance After Deduction" field on your board card that the coordinator fills before O6 sends. Gate O6 on that field being populated; never let a reserve balance line go to an owner as $0.00 or blank.
### Complete Series Summary: All Tracks
| Series | Track | Messages | Primary Audience |
|---|---|---|---|
| R1 to R14 | Resident | 14 messages | Residents and tenants |
| V1 to V9 | Vendor / Tech | 9 messages | Vendors and technicians |
| O2 to O8 | Owner | 7 messages | Property owners |
| E1 to E8 | PM Escalation Alerts | 8 alerts | Internal PM team |
Total: 38 messages and alerts across all four tracks.
[Company Name] - internal operations document. Companion documents: Occupied Unit Maintenance Board, Occupied Unit Maintenance Workflow, Remote Maintenance Coordinator Roles and Responsibilities, Remote Maintenance Coordinator KPI Addendum A, In-House Tech vs. Vendor Dispatch Decision Matrix, Turnover Tracking Board (Full System Design), The Make Ready Deep Dive, Monthly Turnover Performance Report Template.
