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

Company name: ________________________________________
Org short-name: ________________________________________
Forward email: ________________________________________
Timezone: ________________________________________

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

An answer or cover value may begin with exactly one provenance tag: `[documented]`,
`[inferred]`, or `[NEEDS-DAVID]`. The configurator preserves the tagged source text in
`seat-config.json`, strips `[documented]` and `[inferred]` before derived or executable
use, and keeps `[NEEDS-DAVID]` on the named-skip path. Any other leading bracketed tag
fails shut for human confirmation; provenance annotations never become runtime values.

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

Answer: ________________________________________

A2. Who holds the Property Manager seat, and which coordinator lanes exist in your company: leasing, maintenance, turnover, bookkeeping?

Hint: The assistant assists a hired human PM; it never replaces the seat. Name the PM, and for any lane with no coordinator, name who covers that board so the assistant knows where each lane flag routes.

Answer: ________________________________________

A3. Who is the principal broker or company owner, and on what channel do broker-only escalations travel?

Hint: Twelve decision classes never sit with the PM: Fair Housing responses, trust account variances, management agreement terminations, staff discipline, fee concessions, and the rest of the broker-only table in the PM Judgment and Lookup Guide. Pick a channel that gets read the same day.

Answer: ________________________________________

A4. Who is your eviction attorney, and who is your property or general counsel?

Hint: The eviction attorney handles filings and pre-filing reviews; any legal demand letter or attorney contact goes to the broker and counsel the same day it arrives.

Answer: ________________________________________

A5. What are your state's late-rent and eviction notice rules: what day does the late notice go out, what notice type and cure period applies, and what must happen before a filing?

Hint: Common working default: late notice on day 1 or 2 per the lease, then Pay-or-Quit per your state's notice requirements. State law governs; confirm with counsel.

Answer: ________________________________________

A6. What notice does your state require for non-renewal, and what notice for entry?

Hint: Both carry a state-set clock. The renewal pipeline and the compliance calendar read these values. Confirm with counsel.

Answer: ________________________________________

A7. How must security deposits be held in your state, and what is the disposition deadline after move-out?

Hint: Deposits are trust funds: never spent early, disbursed only after the tenancy ends and within the state deadline. Many states use 30 days; confirm with counsel.

Answer: ________________________________________

A8. What are the habitability standards in your state, and what response timeframes do they set?

Hint: A heating failure in winter is the canonical trigger. Common working default: a written owner deadline of 24 to 48 hours on a habitability approval, and PM emergency repair authority when the owner is unreachable. Confirm with counsel.

Answer: ________________________________________

A9. What inspection cadence do your state law and your management agreement set for routine and mid-lease inspections, and how long must tenant files be retained?

Hint: Retention is typically 3 to 7 years. Pre-move-out inspections are scheduled 1 to 2 weeks before move-out; move-in inspections are completed and uploaded on or before move-in day.

Answer: ________________________________________

A10. What state-required landlord filings, registrations, or inspection deadlines belong on your compliance calendar?

Hint: These fill the compliance rows on the Month-End Pack and the compliance alert rules. Anything with a government deadline goes here.

Answer: ________________________________________

### Group B: Thresholds, KPI Targets, and Clocks
B1. What is your owner pre-approval spend threshold, and which owners have a different number in their management agreement?

Hint: The cost above which a repair needs written owner approval before work proceeds. List every per-owner override; the Approval Queue and the maintenance alert rules read this value.

Answer: ________________________________________

B2. What is the coordinator spend authority: the repair cost above which a work order escalates to the PM?

Hint: Common working default: $300. Anything above it lands in the Approval Queue for a PM decision.

Answer: ________________________________________

B3. What is the PM's emergency spend authority when the owner is unreachable, and at what cost does even an emergency loop in the broker?

Hint: On a genuine habitability emergency the PM authorizes the repair, documents every contact attempt, and never waits more than 2 to 4 hours for an owner callback. Common extraordinary threshold: above $5,000 the broker is looped in even for an emergency.

Answer: ________________________________________

B4. What is your owner non-response ladder on approval requests?

Hint: Common defaults: follow-up call or text at 24 hours, second follow-up with documented attempts at 48, PM decides if urgent at 72 and logs it in the decision log, and non-urgent items at 72 hours escalate to the broker and get flagged in the owner file.

Answer: ________________________________________

B5. What is your minimum owner reserve per unit?

Hint: Typical range: $300 to $500 per unit. The financial alert fires when an owner falls below it; the reserve conversation itself always belongs to the PM.

Answer: ________________________________________

B6. What are your delinquency clocks: the day the late notice goes out, the day an account with no payment and no contact alerts the PM, and your portfolio delinquency target?

Hint: Common defaults: late notice on day 1 or 2, PM alert at day 3 to 5 with nothing logged, and a portfolio target under 2 percent of rent roll; above 2 percent alerts the PM and the broker.

Answer: ________________________________________

B7. What are your targets for days vacant and days to make-ready?

Hint: Both are fill-ins on the KPI scorecard: days vacant is usually set to your market average; days to make-ready is your company standard.

Answer: ________________________________________

B8. Do the standard KPI benchmarks hold for your company, or do any get overridden?

Hint: Standard set: occupancy 95 percent or higher, work order close rate 90 percent within SLA, renewal rate 60 to 70 percent or higher, owner retention 90 percent annually, and no more than 20 to 25 percent of leases expiring in any one month. Write only the overrides.

Answer: ________________________________________

B9. What are your renewal clocks: the pipeline look-ahead window, the owner decision window, and the tenant follow-up schedule?

Hint: Common defaults: pipeline pulled at 90 to 120 days out, owner decision within 7 to 10 days of the recommendation, tenant follow-ups at 30 and 60 days, and a flag on any lease inside 90 days with no action started.

Answer: ________________________________________

B10. What are your leasing alert thresholds: days to list after move-out, days on market with no showings, days with showings but no application, and the vacancy age that escalates to the PM?

Hint: Common defaults: listing live within 2 days of move-out, price review at 7 days with no showings, price decision at 14 days with showings but no application, escalation at 21 days with no application, and an application decision within 48 hours.

Answer: ________________________________________

B11. How many days past the target make-ready date does a turnover escalate, and what happens when scope exceeds the approved budget?

Hint: Common default: 3 days past target escalates. Any scope beyond the approved turnover budget is a PM approval, and above the owner threshold it goes to the owner.

Answer: ________________________________________

B12. What maintenance SLA windows does the PM board hold vendors and coordinators to, and how long may an invoice sit unapproved?

Hint: Common defaults: Emergency assigned within 2 hours and resolved same day, Urgent within 24 to 48 hours, Routine within 7 to 10 days, and invoices flagged after 5 days in queue. If you run the maintenance agent, use the same values as its configuration.

Answer: ________________________________________

B13. At what project cost do you require multiple bids?

Hint: The seat standard is 2 to 3 bids for larger projects; name the dollar line where that kicks in.

Answer: ________________________________________

B14. What is your trust account variance rule: how long does the bookkeeper get to resolve an unexplained variance, and what dollar size goes straight up?

Hint: Common defaults: 24 to 48 hours to resolve, and above $500 the broker is notified regardless. Any deposit-account variance, or any suspicion beyond error, goes up immediately; state trust law may require notifying the real estate commission, which is the broker's call.

Answer: ________________________________________

### Group C: Delegation and People
C1. Go through the 20-row Assistant Can Own table in The Property Manager Seat, Part 7: which rows does your company delegate to the assistant on day one, which later, and which never?

Hint: The rows cover pulling reports, drafting owner updates, scheduling, board updates, status tracking, sending renewal offers once terms are set, logging decisions, formatting inspection reports, drafting approval requests, deadline tracking, KPI dashboards, invoice logging, reserve flagging, turnover scheduling, vendor list upkeep, memo drafting, and tenant follow-ups. Mark each row: now, later, or never.

Answer: ________________________________________

C2. Which drafted communications, if any, may the assistant send without PM review?

Hint: Default: every draft is PM-reviewed before it sends. The templated all-clear owner update is the usual first graduate. Anything with judgment or framing in it is always reviewed, personalized, and sent by the PM.

Answer: ________________________________________

C3. Where is the line on owner contact: what may the assistant send to owners directly, and what must always carry the PM's review?

Hint: The seat rule: statements and templated updates can be prepped and sent by the assistant; any owner who responds with a concern goes to the PM, and a difficult month is always framed by the PM, never by a template.

Answer: ________________________________________

C4. How are your owners tagged by communication style, and where does that tag live?

Hint: Silent investor, collaborative, or high-touch, with a preferred contact method per owner. The Owner Snapshot and the report pack tone both read this tag.

Answer: ________________________________________

C5. Who is the backup decision-maker when the PM is unreachable and an SLA or legal clock is burning?

Hint: The default path is up: the broker or company owner. If there is no answer, that is the first thing to fix before the assistant goes live; a deadline with no available decision-maker is a company structure problem.

Answer: ________________________________________

C6. Who works the financial board day to day: who pulls reports, posts payments, generates statements, and flags anomalies?

Hint: Bookkeeper, assistant, or both. The PM reviews and signs off before statements go to owners; money itself always moves on the money side.

Answer: ________________________________________

C7. What is the PM's check-in cadence with the broker?

Hint: The seat recommends a weekly check-in, with legal escalations, owner relationship risk, and compliance questions going up as they arise, not held for the meeting.

Answer: ________________________________________

C8. How do the PM's decisions reach the assistant for the decision log, and when does the assistant sweep the Follow-Through Log?

Hint: Seat defaults: the PM dictates or notes the decision and the assistant formats and files it; the assistant reviews the Follow-Through Log every Monday morning and flags anything due that week; a promise overdue by 24 hours flags red and moves to the top of the Daily Pulse.

Answer: ________________________________________

### Group D: Platform and Wiring
D1. What property management platform and what accounting system do you run?

Hint: The PM documents are platform-agnostic; every board, tag, and alert has to be wired to a real system. Name both, and note whether they are the same product.

Answer: ________________________________________

D2. Where will the PM Operating Board workbook live, and which of its nine tabs go live on day one?

Hint: The board is designed spreadsheet-first: one workbook, nine tabs (Daily Pulse, Monday Board, Month-End Pack, Approval Queue, Escalation Triage, Owner Snapshot, Owner Report Pack, Alert Rules, Follow-Through Log). Some tabs may map to native platform views instead; say which.

Answer: ________________________________________

D3. Where does each lane board live (maintenance, leasing, turnover, bookkeeping, decision log), and how does the operating board pull from them?

Hint: Coordinators update the lane boards; the PM Operating Board pulls from them and never replaces them. Note whether each pull is a linked sheet, an export, or a manual update, and who does it.

Answer: ________________________________________

D4. Which alert rules fire automatically in your platform, and which are manual coordinator flags into Escalation Triage?

Hint: The Alert Rules tab lists thresholds across maintenance, leasing, delinquency, financial, and compliance. Anything your software cannot auto-flag becomes a named person's manual duty; an alert with no owner does not exist.

Answer: ________________________________________

D5. Which channels reach each audience: owners, tenants, coordinators, vendors, and the broker?

Hint: Portal, email, phone, text, chat, per audience. Owner preference is per-owner and lives in the Owner Snapshot; broker-only escalations use the channel named in A3.

Answer: ________________________________________

D6. By what day of the month does the owner report pack go out, on which channels, and do high-touch owners get a follow-up call?

Hint: Common defaults: portal plus email by day 15, owner draws around day 10, and the financial review signed off on days 8 to 12 before anything sends. The all-clear version goes out even when nothing happened.

Answer: ________________________________________

D7. Where do the durable records live: the decision log, owner files, tenant files, proof of notice service, and the compliance calendar?

Hint: The judgment guide requires owner communication saved in the portal or PM software, not just email. Every scenario ends with a write-it-down step; name the one place those entries land.

Answer: ________________________________________

D8. Where do your attorney-reviewed notice templates live, and who owns keeping them current?

Hint: The PM maintains the templates and flags when they need updating; the assistant can track review dates once a home and an owner are named.

Answer: ________________________________________

D9. What is your CMA source for renewal pricing, and who runs it?

Hint: The renewal recommendation memo is drafted from CMA data; name the tool or data source and whether the PM runs the CMA or reviews one pulled by the assistant.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The operating board gets your values. The PM Operating Board is built from your Group B and Group D answers: every population rule on the Daily Pulse, every aging flag on the Approval Queue, and every threshold on the Alert Rules tab reads from this configuration, and the generic documents themselves are never edited.
- The assistant boots in shadow mode. For about the first week the assistant reads the lane boards silently and sends a daily calibration digest to the PM: what it would have flagged, filed, and drafted. Nothing outbound, no board writes. Shadow mode ends when a week of digests matches reality.
- Delegation widens row by row. The rows you marked "now" in C1 go live first; every outbound draft is PM-released until its message class proves clean; rows marked "later" graduate one at a time, lowest consequence first. The golden rule never graduates at any setting: if it requires a relationship, a risk assessment, a legal judgment, or an unhappy conversation, it stays with the PM; and the broker-only decisions stay with the broker.

Keep the answers current. When a threshold, a person, an owner, or a platform changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Ascend Operations Library, generic baseline document. Derived from the three Property Manager library documents: The Property Manager Seat, The PM Operating Board, and the PM Judgment and Lookup Guide. Nothing in this document is legal advice; confirm every state-law answer with your attorney and broker of record.
