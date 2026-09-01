---
title: "Bookkeeping Agent Setup Questionnaire"
source: "Owner-reviewed bookkeeping and accounting configuration contract"
converted: 2026-08-21
audience: all agents
status: reference
---

# Configuration Cover Sheet

Company name: Ridgeline Residential Management
Org short-name: ridgeline
Forward email: accounting@ridgeline.example
Timezone: America/Denver
Autonomy mode: [documented] copilot
Unlock window: [documented] last_10
Qualifying accuracy: [documented] null
Resident messaging autonomy: [documented] no

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

Fixture provenance: golden fixture for the accounting-seat mapping pass, 2026-08-25.
Every company, person, bank, platform, and jurisdiction below is FICTIONAL. Identity
reused from the sealed scenario-1 Ridgeline maintenance fixture and the turnover and
leasing sibling fixtures so cross-seat fixtures cohere.

# Bookkeeping Agent Setup Questionnaire

## Bookkeeping Agent Setup Questionnaire
Residential Property Management, Platform-Agnostic. The setup interview that turns the generic bookkeeping and accounting agent into your company's agent.

No separate companion documents ship in this edition. The configured bootstrap library and its accounting skills are the complete shipped surface.

### What This Is and How To Use It
The bookkeeping agent ships as a generic, approval-gated baseline. Nothing company-specific is baked in. This questionnaire is the one door your company's specifics enter through. Your answers become the agent's configuration file; every check, deadline clock, and alert reads from that file.

There are 46 questions in four groups: state rules, company thresholds and policy, roles and people, and platform, banking, and wiring. Most answers take a minute. Group A leans heavily on your attorney or your state's landlord-tenant statute; those questions are marked in the hint, and it is fine to write "confirm with counsel" as a first answer and come back. Expect 60 to 90 minutes for a complete first pass, plus the counsel round trip on Group A.

---
Where a question offers a common default, the default is a starting point, not legal advice. This questionnaire touches trust accounting, statutory deadlines, and eviction notices; every state-law answer should be confirmed with your attorney before the agent relies on it.

### Group A: State Rules
A1. How many days must rent be late before a late fee may be posted?

Hint: Grace periods are set by state law in most jurisdictions; the agent will not flag a missing late fee before this day. Confirm with counsel.

Answer: Late fee grace days: 5
  Rent is due on the 1st; a late fee may not post before the 6th in either fictional
  jurisdiction. Counsel confirmed one shared clock for this fixture. CONFIRMED=true.

A2. What is your state's late fee cap: a flat amount, a daily rate, or a total percentage of past-due rent?

Hint: Many states cap late fees as a percentage of the past-due amount. Confirm with counsel.

Answer: 10 percent of the past-due rent balance, as a total cap rather than a flat amount or a daily
  rate. Counsel confirmed for both fictional jurisdictions. CONFIRMED=true.

A3. What notice period does your state require for nonpayment before an eviction can be filed?

Hint: The number of days from service of the notice, and what counts as service. Confirm with counsel.

Answer: Nonpayment notice days: 14
  Service means personal delivery to an adult occupant, or
  posting on the unit door plus first-class mail the same day. Counsel confirmed for both
  fictional jurisdictions. CONFIRMED=true.

A4. For nonpayment, does your state use a pay-or-quit notice where the resident can cure, or an unconditional quit notice?

Hint: This controls the wording of every notice the agent tracks. Confirm with counsel.

Answer: Pay-or-quit; the resident may cure by paying the full past-due amount within the notice
  period. Counsel confirmed for both fictional jurisdictions. CONFIRMED=true.

A5. Does accepting a partial payment after a nonpayment notice void the notice in your state?

Hint: A counsel question, and the answer varies. Safe working rule until it is answered: every payment on a noticed account is flagged to the PM before it is applied. Confirm with counsel.

Answer: PER-JURISDICTION, and only half of it is confirmed. Pine Basin: accepting a partial payment
  after a nonpayment notice VOIDS the notice and the ladder restarts; counsel confirmed,
  CONFIRMED=true. Cedar Mesa: UNRESOLVED, counsel has not answered, CONFIRMED=false. The
  questionnaire's safe working rule stays in force for Cedar Mesa accounts: every payment on a
  noticed Cedar Mesa account is flagged to the property manager before it is applied.

A6. What is the security deposit return deadline in your state, and what date starts the clock?

Hint: Many states use 30 days. The trigger date matters as much as the count: move-out, termination of tenancy, and key return are different days. Confirm with counsel.

Answer: Deposit return days: 30
  The clock starts at termination of the tenancy. (CROSS-SEAT: the
  deadline is the same fact the maintenance seat's A3 answer carries; recorded here as a
  pointer, not a second copy. The date that starts the clock is owned by the leasing seat's B1
  answer; pointer as well.) MIGRATION-READY: when this bookkeeper seat ships into templates/
  through a reviewed PR, ownership of the deadline migrates here and maintenance A3 drops to a
  pointer. Today it is still a pointer. CONFIRMED=true.

A7. Does your state require security deposits to be held in a separate account, and must the resident be told where they are held?

Hint: Some states require a deposit-only account and disclosure of the bank name. Confirm with counsel.

Answer: Yes to both. A deposit-only trust account is required, and the resident must be told the name
  of the bank holding the deposit; the bank name goes in the lease and in the move-in packet.
  Counsel confirmed for both fictional jurisdictions. CONFIRMED=true.

A8. Does your state require interest to be paid on security deposits?

Hint: Confirm with counsel.

Answer: No. Neither fictional jurisdiction requires interest to be paid on security deposits. Counsel
  confirmed. CONFIRMED=true.

A9. Does your state cap the security deposit amount?

Hint: Confirm with counsel.

Answer: Yes: 1.5 months' rent, inclusive of any pet deposit. Counsel confirmed for both fictional
  jurisdictions. CONFIRMED=true.

A10. What is your state's cap on NSF or returned payment fees, and does it apply to ACH returns as well as checks?

Hint: Many states cap the fee and require it to appear in the lease before it can be charged. Confirm with counsel.

Answer: $30, and it applies to ACH returns as well as to checks. The fee must appear in the lease
  before it can be charged; fictional lease section 7.4 carries it. Counsel confirmed.
  CONFIRMED=true.

A11. Once the nonpayment notice period runs, how soon may an eviction be filed, and what is your file-or-hold decision window?

Hint: Common working shape: the PM makes the file-or-hold decision within a few days of the notice expiring, so accounts never age without a decision. Confirm the filing rules with counsel.

Answer: File-or-hold decision days: 3
  An eviction may be filed the first business day after the 14-day notice period expires.
  Ridgeline's decision window runs from expiry, so no noticed account
  ages without a recorded decision. Counsel confirmed the filing rules. CONFIRMED=true.

A12. Does your state set a statutory deadline for owner disbursements?

Hint: Many states set none, in which case the management agreement governs. Confirm with counsel.

Answer: None. Neither fictional jurisdiction sets a statutory owner-disbursement deadline, so the
  management agreement governs; the Ridgeline standard agreement promises owner funds out by the
  15th. Counsel confirmed. CONFIRMED=true.

A13. What are your state's trust account reconciliation requirements: how often, who signs, how long records are retained, and which regulator can audit?

Hint: The common shape is monthly reconciliation signed by the responsible broker, with a multi-year retention period and audit rights held by the state real estate regulator. Confirm with counsel.

Answer: Trust record retention years: 7
  Monthly three-way reconciliation, signed by the principal broker, Harlan Beck. The fictional Basin State Real Estate Commission holds audit rights over
  both trust accounts. Counsel confirmed. CONFIRMED=true.

A14. Does your state require state-level 1099 filing in addition to the federal filing?

Hint: Federal 1099-NEC is due January 31 regardless. Have your CPA confirm the state answer annually. Confirm with counsel.

Answer: UNANSWERED PENDING CPA. Devin Marsh has not yet confirmed whether the fictional Basin state
  requires a state-level 1099 filing on top of the federal 1099-NEC. CONFIRMED=false; the
  state-1099 year-end check is DISABLED and reported as disabled until Devin answers. The
  federal January 31 filing is unaffected and proceeds regardless.

A15. At what invoice or project amount does your state's contractor licensing law require a flag, and which trades require a licensed contractor at any amount?

Hint: Many states set a dollar threshold for general work and require licenses for electrical, plumbing, HVAC, and gas work at any amount. Confirm with counsel.

Answer: $2,500 for general work: at or above that project amount the invoice is flagged for a
  contractor-license check before payment. (CROSS-SEAT: the list of trades requiring a licensed
  contractor at any amount is owned by the maintenance seat's A7 answer, which carries the full
  ten-trade list; pointer, not a second copy. The dollar threshold has no maintenance
  counterpart and is owned here.) Counsel confirmed. CONFIRMED=true.

A16. What retention period will you apply to the PM decision log?

Hint: Matching your trust-record retention period is the common choice, so the log survives as long as the records it explains. Confirm with counsel.

Answer: Decision log retention years: 7
  This matches the trust-record retention period in A13, so the log survives as long as the
  records it explains. Counsel confirmed. CONFIRMED=true.

A17. Which landlord-tenant statute applies in each county or jurisdiction in your portfolio?

Hint: In some states the applicable statute varies by county, for example URLTA counties versus common-law counties, and the notice and deposit rules change with it. Confirm every county with counsel.

Answer: Two fictional jurisdictions, and they do not carry the same statute. Pine Basin County: the
  fictional Basin Residential Landlord and Tenant Act, a URLTA-style statute. Cedar Mesa County:
  fictional common-law county rules, not under the Act. The A5 partial-payment rule already
  differs between them, which is why every Group A clock in this config is per-jurisdiction and
  not per-company. CONFIRMED=true for the mapping itself; the Cedar Mesa A5 value inside it
  remains CONFIRMED=false.

### Group B: Company Thresholds and Policy
B1. At what amount does a vendor bill require PM approval before payment?

Hint: Common range: $300 to $500. Below it the bookkeeper pays on a matched work order; at or above it the PM approves first.

Answer: $375. Below it the bookkeeper pays on a matched work order; at or above it the property
  manager approves before payment. Deliberately not equal to the maintenance seat's B1 owner
  pre-approval threshold ($450) or the turnover seat's C1 make-ready reserve threshold ($500) -
  three different authorities, three numbers, and the difference is intentional rather than a
  contradiction.

B2. At what amount does a payment require dual authorization?

Hint: Common range: $1,000 to $2,500. A second person signs off before the payment is released.

Answer: $1,500. At or above it a second person signs off before the payment is released; the second
  signer is Harlan Beck when the payment is prepared by Avery Moss.

B3. What reserve floor do you hold per property or per owner, and which owners have a different number in their management agreement?

Hint: Lead with `Base reserve: NN` on its own line. Common range: $300 to $500. The management agreement governs; list every per-owner override after that line.

Answer: Base reserve: 400
  Fictional owner overrides written into their management agreements: Juniper Holdings $650,
  Northstar Homes $250. This is a cash floor that must remain
  in the owner's ledger, not a spend-approval threshold; it is not the same number as, and must
  not be reconciled against, the maintenance B1 overrides ($700 / $300) or the turnover C1
  overrides ($750 / $350).

B4. At what amount does an unidentified payment escalate the same day instead of sitting in research?

Hint: Suggested: $500. Below it the payment sits in suspense while research continues; at or above it the PM hears about it same day.

Answer: $550. Below it the payment sits in suspense while research continues; at or above it the
  property manager hears about it the same day. Set above the questionnaire's suggested $500 so
  the number is distinguishable from the turnover seat's C1 threshold at a glance.

B5. What variance amount splits a small reconciliation difference from a large one?

Hint: Example: $25. Small variances get researched on a clock; large ones escalate immediately and can hold statements.

Answer: $40. At or below $40 a reconciliation difference is researched on the clock; above $40 it
  escalates immediately and can hold owner statements.

B6. At what variance amount and age does an unreconciled item fire an alert?

Hint: Example: any variance of $5 or more that stays open 3 or more days fires an alert to the PM.

Answer: Variance alert days: 3
  Any variance of $10 or more that stays open that many business days fires an alert to the
  property manager.

B7. What payment application order is set in your platform when a resident pays less than everything owed?

Hint: Common baseline: fees first, then past-due rent, then current rent. Confirm what your platform is actually configured to do, not what you assume it does.

Answer: Fees first, then past-due rent, then current rent. VERIFIED in LedgerPeak's
  payment-application settings screen during setup, not assumed from the platform's
  documentation; the screen and the baseline agreed.

B8. What is your owner draw window and target date?

Hint: Common baseline: draws out by the 15th with a goal of the 10th. The dates must match what your management agreements promise.

Answer: Owner draw deadline day: 15
  Owner draw target day: 10
  The 15th is what the Ridgeline standard
  management agreement promises owners, so it is a commitment and not just an internal goal.

B9. On which dates do vendor bill payment runs go out?

Hint: Fixed run dates make the invoice-aging alerts meaningful; name the days of the month.

Answer: The 5th and the 20th of each month. Bills approved after a run date wait for the next run
  unless the property manager releases them early.

B10. On what date are owner statements released?

Hint: Statements should not release while the trust account is unreconciled; the release date and the reconciliation date need to agree.

Answer: Owner statement release day: 12
  Never release over an unreconciled trust account. The 12th sits after the monthly
  reconciliation completes and before the 15th draw deadline, so the sequence is reconcile,
  release statements, then draw.

B11. What archive retention period applies to each item type: rent records, vendor bills, deposit dispositions, reconciliations, 1099 records?

Hint: Where a range is offered, default to the long end until your counsel and CPA set the final numbers.

Answer: Rent records 7 years. Vendor bills 7 years. Deposit dispositions 7 years after the tenancy
  ends. Reconciliations 7 years, matching the A13 trust-record period. 1099 records 7 years. The
  long end of every range, pending final numbers from counsel and the CPA.

B12. Who may authorize a fee waiver or a write-off, and in what form?

Hint: Common baseline: the PM, in writing. No waiver or write-off happens on a verbal.

Answer: Ellis Shore, Portfolio Director, in writing, with the reason recorded in the PM decision log.
  No waiver and no write-off on a verbal. NOTE, DELIBERATE: the PM decision log does not exist
  yet (see D6), so this authority currently has no place to record its reason. That is a
  phase-zero dependency, not a policy gap, and it is written here so the gap is visible rather
  than discovered at the first waiver.

B13. What deposit-chargeback threshold does Bookkeeping enforce at the Deposit Packet, per line item and per unit total?

Hint: Do not set a new number here. This is the same per-line and per-unit chargeback threshold configured in the turnover coordinator setup (its Group C). Bookkeeping enforces that one configured number as the review gate on the Deposit Packet: at or above either number, or on any dispute or missing documentation, the disposition goes to the PM before it is sent. Both seats read the same number, so record it here only to confirm the two match. This is distinct from the vendor-bill PM-approval threshold in B1; that gates repair-spend authority, this gates deposit-deduction authority.

Answer: Per-line chargeback: 150
  Per-unit chargeback: 400
  CONFIRMED TO MATCH the turnover coordinator's C7
  configuration exactly; no new number was set here. (CROSS-SEAT: owned by the turnover seat's
  C7 answer; this seat holds a pointer and enforces the same number as the review gate on the
  Deposit Packet.) These gate deposit-deduction authority and are distinct from B1's $375, which
  gates repair-spend authority.

### Group C: Roles and People
C1. Who is the property manager of record for owner-money decisions?

Hint: This person owns every escalation the agent raises: noticed-account payments, overdraws, deposit deadlines, reconciliation variances. Name them.

Answer: Ellis Shore, Portfolio Director. Same person the turnover seat names at its D3, and
  deliberately NOT the same person the maintenance seat names at its C1 (Morgan Vale,
  Maintenance Supervisor). Owner-money decisions and maintenance dispatch decisions answer to
  different desks at Ridgeline, and that is the real org shape rather than a configuration
  error.

C2. Who is the principal or managing broker, the licensee accountable for the trust account?

Hint: This one matters legally: reconciliation sign-off and regulator audits land on this person. Name them even if the answer feels obvious.

Answer: Harlan Beck, principal broker. The licensee accountable for both trust accounts;
  reconciliation sign-off and any Basin State Real Estate Commission audit land on him.

C3. Who executes the human bookkeeper role today, the person who posts, pays, and reconciles: a staff member, the principal, or an outside bookkeeper?

Hint: The agent watches and flags; a human executes. The daily digest needs a recipient who actually posts and pays.

Answer: Avery Moss, Accounts Payable, a staff member. She posts, pays, and reconciles today, and she
  is the recipient of the daily digest. Already named by the maintenance seat's C7 as the
  invoice-payment executor and by the turnover seat's D6 as the deposit-disposition executor, so
  all three seats hand money work to the same desk.

C4. Who is the backup decision-maker when the PM is unavailable and a statutory deadline is imminent?

Hint: If there is no answer, that is the first thing to fix: a statutory deadline with no available decision-maker is a company structure problem.

Answer: Morgan Vale, Maintenance Supervisor, is the backup when Ellis Shore is unreachable and a
  statutory deadline is imminent. Deliberately different from the maintenance seat's C9 backup
  (Ellis Shore) - each seat's backup is the other seat's primary, which is coherent and not a
  contradiction.

C5. Who is your eviction attorney of record?

Hint: Name and channel. The nonpayment ladder ends at this desk.

Answer: Marisol Quill of the fictional firm Quill and Associates; reached at evictions@quill.example
  and on her direct line. The nonpayment ladder ends at her desk.

C6. Who is your CPA of record for 1099 filing and year-end?

Hint: Name and channel. The CPA also confirms the state 1099 answer from Group A each year.

Answer: Devin Marsh of the fictional firm Marsh Tax Partners; reached at devin@marshtax.example. He
  also owes the annual confirmation on the A14 state 1099 question, which is why A14 is
  currently CONFIRMED=false.

C7. Who performs the second-person spot-check in the vendor banking change verification protocol?

Hint: The protocol requires a second person, not the one who processed the change, to verify the update before the next payment releases. Name them.

Answer: Harlan Beck, principal broker, performs the second-person spot-check on every vendor banking
  change. He is never the person who processed the change; Avery Moss processes, Harlan
  verifies, and the payment does not release until he has.

### Group D: Platform, Banking, and Wiring
D1. What property management accounting platform do you run?

Hint: Note whether it includes a built-in trust reconciliation module and platform 1099 filing; both change the month-end and year-end mechanics.

Answer: LedgerPeak, the fictional accounting platform. It has a built-in trust reconciliation module,
  which the month-end close uses. It does NOT offer platform 1099 filing, so year-end 1099-NEC
  filing runs through Devin Marsh at Marsh Tax Partners from an exported vendor-payment report.
  (CROSS-SEAT: LedgerPeak as the company's accounting system is the same fact the maintenance
  seat's D1 answer carries alongside WorkTrail; pointer for the platform identity, and the two
  sub-answers above are owned here.)

D2. What banks do you use, and what is the full account inventory: operating trust, security deposit trust, reserve account, company operating account?

Hint: The three-way reconciliation and the trust controls all run against this inventory. List every account, its bank, and its purpose.

Answer: Basin Trust Bank holds three accounts: Operating Trust, Security Deposit Trust, and the
  Reserve account. Cedar Mesa Community Bank holds the Ridgeline company operating account. Four
  accounts total, labelled by purpose only - no account or routing numbers are recorded here or
  in any tracked file.

D3. Is the security deposit trust account already separate from the operating trust?

Hint: In states that require a separate deposit account, a "no" here is a day-one flag to fix before anything else.

Answer: Yes. The Security Deposit Trust at Basin Trust Bank is already separate from the Operating
  Trust, so the A7 requirement is satisfied and no day-one fix is open.

D4. Are your trust accounts enrolled in positive pay?

Hint: A standard check-fraud control: the bank pays only checks you have registered. Availability varies by bank and platform.

Answer: PARTIAL. Positive pay is enrolled on the Operating Trust at Basin Trust Bank and on the
  company operating account at Cedar Mesa Community Bank. Basin Trust Bank does not offer
  positive pay on deposit-only trust accounts, so the Security Deposit Trust is NOT enrolled and
  is covered by monthly reconciliation and dual authorization instead. The gap is recorded
  rather than smoothed over.

D5. Does a suspense or clearing account exist for unidentified payments?

Hint: Needed for the unmatched-payment scenario: money you cannot yet attribute sits in suspense, never in an owner's ledger.

Answer: Yes. A LedgerPeak clearing account named Suspense - Unidentified Receipts exists and is the
  only legitimate destination for money that cannot yet be attributed. It never touches an owner
  ledger.

D6. Where do the tracking board and the PM decision log live, and do they exist yet?

Hint: Name the existing systems of record. If either is absent, creating it is a phase-zero task before the agent watches anything; no board or decision-log template ships in this edition.

Answer: SPLIT ANSWER. The Ridgeline Bookkeeping Board exists as the company cloud-drive spreadsheet
  and is the single board of record. The PM decision log does NOT exist yet. PHASE-ZERO:
  creating and reviewing that log is a task before the agent watches anything that depends on
  it, and it is the dependency B12's waiver authority is currently missing.

D7. What read-only access paths exist for platform reports and bank statements or feeds?

Hint: The agent is read-only by construction. Name the report exports and statement sources it can see; a simple statement drop into a shared folder is a fine day-one answer.

Answer: LedgerPeak read-only reporting role for the agent, covering the rent roll, delinquency, vendor
  aging, owner ledger, and trust balance reports. Bank statements arrive as monthly PDF drops
  from both banks into the cloud drive Statements folder. No write path exists to either system;
  the agent is read-only by construction, not by policy.

D8. Which channels carry money escalations to the PM and to the principal, and what hours apply to each?

Hint: Name the channel each person actually looks at quickly. Urgent money flags, above all suspected fraud, need a channel that works outside business hours.

Answer: Money escalations to Ellis Shore, Portfolio Director: internal chat 08:00-18:00
  America/Denver, and SMS at any hour when a statutory clock is burning. Escalations to Harlan
  Beck, principal broker: email during business hours, and SMS at any hour for suspected fraud
  or a suspected trust shortfall. Both after-hours SMS routes are live, because a fraud flag
  that waits for morning is not a control.

D9. Where are W-9s stored, and does a current 1099 tracker exist?

Hint: Every vendor should have a W-9 on file before their first payment. If no tracker exists, building one is a phase-zero task ahead of year-end.

Answer: W-9s live in the cloud drive under Vendors, one folder per vendor. A current 1099 tracker does
  NOT exist. PHASE-ZERO: building the tracker is a task ahead of year-end, and until it exists
  the year-end readiness check is DISABLED and reported as disabled rather than reporting a
  clean year-end.

### What Happens Next
Your answers do three things, in order:

- The configured bootstrap and accounting skills receive your values. Group A supplies the state markers, Group B supplies the operating thresholds, and the structured config remains the authority for every clock and alert.
- The agent begins in operator-supervised copilot mode. A human reviews every draft and every flag; no automated calibration digest or automatic graduation mechanism is shipped.
- The agent never moves money, at any setting. It reads, reconciles, tracks deadlines, drafts, and flags. Posting a ledger entry, releasing a payment, approving a disbursement, signing off a reconciliation, changing a vendor record, and sending anything to an owner, resident, or vendor always end with a human, and read-only access is how the agent is wired, not just a policy it follows.

Keep the answers current. When a threshold, a person, a bank account, or a statute changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Generic baseline document derived from the owner-reviewed bookkeeping and accounting contract. Nothing in this document is legal advice; confirm every state-law answer with your attorney.
