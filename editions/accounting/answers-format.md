---
title: "Bookkeeping Agent Setup Questionnaire"
source: "Owner-reviewed bookkeeping and accounting configuration contract"
converted: 2026-08-21
audience: all agents
status: reference
---

# Bookkeeping Agent Setup Questionnaire

# Configuration Cover Sheet

Company name: ________________________________________
Org short-name: ________________________________________
Forward email: ________________________________________
Timezone: ________________________________________

Answer format: Put each response on its `Answer:` line. For a multi-line response,
indent every continuation line by two spaces; indented lines belong to the preceding
answer until the next questionnaire heading or question begins.

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

Hint: This edition currently supports one jurisdiction-wide grace clock. Begin the answer with an exact line `Late fee grace days: NN` and confirm it with counsel. If your portfolio has different grace clocks by jurisdiction, setup rejects that answer and directs you to wait for the tracked per-jurisdiction capability rather than choosing one clock.

Answer: ________________________________________

A2. What is your state's late fee cap: a flat amount, a daily rate, or a total percentage of past-due rent?

Hint: Many states cap late fees as a percentage of the past-due amount. Confirm with counsel.

Answer: ________________________________________

A3. What notice period does your state require for nonpayment before an eviction can be filed?

Hint: The number of days from service of the notice, and what counts as service. Confirm with counsel. Begin the answer with an exact line `Nonpayment notice days: NN`.

Answer: ________________________________________

A4. For nonpayment, does your state use a pay-or-quit notice where the resident can cure, or an unconditional quit notice?

Hint: This controls the wording of every notice the agent tracks. Confirm with counsel.

Answer: ________________________________________

A5. Does accepting a partial payment after a nonpayment notice void the notice in your state?

Hint: A counsel question, and the answer varies. Safe working rule until it is answered: every payment on a noticed account is flagged to the PM before it is applied. Confirm with counsel.

Answer: ________________________________________

A6. What is the security deposit return deadline in your state, and what date starts the clock?

Hint: Many states use 30 days. The trigger date matters as much as the count: move-out, termination of tenancy, and key return are different days. Confirm with counsel. Begin the answer with an exact line `Deposit return days: NN`.

Answer: ________________________________________

A7. Does your state require security deposits to be held in a separate account, and must the resident be told where they are held?

Hint: Some states require a deposit-only account and disclosure of the bank name. Confirm with counsel.

Answer: ________________________________________

A8. Does your state require interest to be paid on security deposits?

Hint: Confirm with counsel.

Answer: ________________________________________

A9. Does your state cap the security deposit amount?

Hint: Confirm with counsel.

Answer: ________________________________________

A10. What is your state's cap on NSF or returned payment fees, and does it apply to ACH returns as well as checks?

Hint: Many states cap the fee and require it to appear in the lease before it can be charged. Confirm with counsel.

Answer: ________________________________________

A11. Once the nonpayment notice period runs, how soon may an eviction be filed, and what is your file-or-hold decision window?

Hint: Common working shape: the PM makes the file-or-hold decision within a few days of the notice expiring, so accounts never age without a decision. Confirm the filing rules with counsel. Begin the answer with an exact line `File-or-hold decision days: NN`.

Answer: ________________________________________

A12. Does your state set a statutory deadline for owner disbursements?

Hint: Many states set none, in which case the management agreement governs. Confirm with counsel.

Answer: ________________________________________

A13. What are your state's trust account reconciliation requirements: how often, who signs, how long records are retained, and which regulator can audit?

Hint: The common shape is monthly reconciliation signed by the responsible broker, with a multi-year retention period and audit rights held by the state real estate regulator. Confirm with counsel. Begin the answer with an exact line `Trust record retention years: NN`.

Answer: ________________________________________

A14. Does your state require state-level 1099 filing in addition to the federal filing?

Hint: Federal 1099-NEC is due January 31 regardless. Have your CPA confirm the state answer annually. Confirm with counsel.

Answer: ________________________________________

A15. At what invoice or project amount does your state's contractor licensing law require a flag, and which trades require a licensed contractor at any amount?

Hint: Many states set a dollar threshold for general work and require licenses for electrical, plumbing, HVAC, and gas work at any amount. Confirm with counsel.

Answer: ________________________________________

A16. What retention period will you apply to the PM decision log?

Hint: Matching your trust-record retention period is the common choice, so the log survives as long as the records it explains. Confirm with counsel. Begin the answer with an exact line `Decision log retention years: NN`.

Answer: ________________________________________

A17. Which landlord-tenant statute applies in each county or jurisdiction in your portfolio?

Hint: In some states the applicable statute varies by county, for example URLTA counties versus common-law counties, and the notice and deposit rules change with it. Confirm every county with counsel.

Answer: ________________________________________

### Group B: Company Thresholds and Policy
B1. At what amount does a vendor bill require PM approval before payment?

Hint: Common range: $300 to $500. Below it the bookkeeper pays on a matched work order; at or above it the PM approves first.

Answer: ________________________________________

B2. At what amount does a payment require dual authorization?

Hint: Common range: $1,000 to $2,500. A second person signs off before the payment is released.

Answer: ________________________________________

B3. What reserve floor do you hold per property or per owner, and which owners have a different number in their management agreement?

Hint: Lead with `Base reserve: NN` on its own line. Common range: $300 to $500. The management agreement governs; list every per-owner override after that line.

Answer: ________________________________________

B4. At what amount does an unidentified payment escalate the same day instead of sitting in research?

Hint: Suggested: $500. Below it the payment sits in suspense while research continues; at or above it the PM hears about it same day.

Answer: ________________________________________

B5. What variance amount splits a small reconciliation difference from a large one?

Hint: Example: $25. Small variances get researched on a clock; large ones escalate immediately and can hold statements.

Answer: ________________________________________

B6. At what variance amount and age does an unreconciled item fire an alert?

Hint: Example: any variance of $5 or more that stays open 3 or more days fires an alert to the PM. Begin the answer with an exact line `Variance alert days: NN`.

Answer: ________________________________________

B7. What payment application order is set in your platform when a resident pays less than everything owed?

Hint: Common baseline: fees first, then past-due rent, then current rent. Confirm what your platform is actually configured to do, not what you assume it does.

Answer: ________________________________________

B8. What is your owner draw window and target date?

Hint: Common baseline: draws out by the 15th with a goal of the 10th. The dates must match what your management agreements promise. Begin with exact lines `Owner draw deadline day: NN` and `Owner draw target day: NN`.

Answer: ________________________________________

B9. On which dates do vendor bill payment runs go out?

Hint: Fixed run dates make the invoice-aging alerts meaningful; name the days of the month.

Answer: ________________________________________

B10. On what date are owner statements released?

Hint: Statements should not release while the trust account is unreconciled; the release date and the reconciliation date need to agree. Begin the answer with an exact line `Owner statement release day: NN`.

Answer: ________________________________________

B11. What archive retention period applies to each item type: rent records, vendor bills, deposit dispositions, reconciliations, 1099 records?

Hint: Where a range is offered, default to the long end until your counsel and CPA set the final numbers.

Answer: ________________________________________

B12. Who may authorize a fee waiver or a write-off, and in what form?

Hint: Common baseline: the PM, in writing. No waiver or write-off happens on a verbal.

Answer: ________________________________________

B13. What deposit-chargeback threshold does Bookkeeping enforce at the Deposit Packet, per line item and per unit total?

Hint: Do not set a new number here. This is the same per-line and per-unit chargeback threshold configured in the turnover coordinator setup (its Group C). Bookkeeping enforces that one configured number as the review gate on the Deposit Packet: at or above either number, or on any dispute or missing documentation, the disposition goes to the PM before it is sent. Both seats read the same number, so record it here only to confirm the two match. This is distinct from the vendor-bill PM-approval threshold in B1; that gates repair-spend authority, this gates deposit-deduction authority. Begin with exact lines `Per-line chargeback: NN` and `Per-unit chargeback: NN`.

Answer: ________________________________________

### Group C: Roles and People
C1. Who is the property manager of record for owner-money decisions?

Hint: This person owns every escalation the agent raises: noticed-account payments, overdraws, deposit deadlines, reconciliation variances. Name them.

Answer: ________________________________________

C2. Who is the principal or managing broker, the licensee accountable for the trust account?

Hint: This one matters legally: reconciliation sign-off and regulator audits land on this person. Name them even if the answer feels obvious.

Answer: ________________________________________

C3. Who executes the human bookkeeper role today, the person who posts, pays, and reconciles: a staff member, the principal, or an outside bookkeeper?

Hint: The agent watches and flags; a human executes. The daily digest needs a recipient who actually posts and pays.

Answer: ________________________________________

C4. Who is the backup decision-maker when the PM is unavailable and a statutory deadline is imminent?

Hint: If there is no answer, that is the first thing to fix: a statutory deadline with no available decision-maker is a company structure problem.

Answer: ________________________________________

C5. Who is your eviction attorney of record?

Hint: Name and channel. The nonpayment ladder ends at this desk.

Answer: ________________________________________

C6. Who is your CPA of record for 1099 filing and year-end?

Hint: Name and channel. The CPA also confirms the state 1099 answer from Group A each year.

Answer: ________________________________________

C7. Who performs the second-person spot-check in the vendor banking change verification protocol?

Hint: The protocol requires a second person, not the one who processed the change, to verify the update before the next payment releases. Name them.

Answer: ________________________________________

### Group D: Platform, Banking, and Wiring
D1. What property management accounting platform do you run?

Hint: Note whether it includes a built-in trust reconciliation module and platform 1099 filing; both change the month-end and year-end mechanics.

Answer: ________________________________________

D2. What banks do you use, and what is the full account inventory: operating trust, security deposit trust, reserve account, company operating account?

Hint: The three-way reconciliation and the trust controls all run against this inventory. List every account, its bank, and its purpose.

Answer: ________________________________________

D3. Is the security deposit trust account already separate from the operating trust?

Hint: In states that require a separate deposit account, a "no" here is a day-one flag to fix before anything else.

Answer: ________________________________________

D4. Are your trust accounts enrolled in positive pay?

Hint: A standard check-fraud control: the bank pays only checks you have registered. Availability varies by bank and platform.

Answer: ________________________________________

D5. Does a suspense or clearing account exist for unidentified payments?

Hint: Needed for the unmatched-payment scenario: money you cannot yet attribute sits in suspense, never in an owner's ledger.

Answer: ________________________________________

D6. Where do the tracking board and the PM decision log live, and do they exist yet?

Hint: Name the existing systems of record. If either is absent, creating it is a phase-zero task before the agent watches anything; no board or decision-log template ships in this edition.

Answer: ________________________________________

D7. What read-only access paths exist for platform reports and bank statements or feeds?

Hint: The agent is read-only by construction. Name the report exports and statement sources it can see; a simple statement drop into a shared folder is a fine day-one answer.

Answer: ________________________________________

D8. Which channels carry money escalations to the PM and to the principal, and what hours apply to each?

Hint: Name the channel each person actually looks at quickly. Urgent money flags, above all suspected fraud, need a channel that works outside business hours.

Answer: ________________________________________

D9. Where are W-9s stored, and does a current 1099 tracker exist?

Hint: Every vendor should have a W-9 on file before their first payment. If no tracker exists, building one is a phase-zero task ahead of year-end.

Answer: ________________________________________

### What Happens Next
Your answers do three things, in order:

- The configured bootstrap and accounting skills receive your values. Group A supplies the state markers, Group B supplies the operating thresholds, and the structured config remains the authority for every clock and alert.
- The agent begins in operator-supervised copilot mode. A human reviews every draft and every flag; no automated calibration digest or automatic graduation mechanism is shipped.
- The agent never moves money, at any setting. It reads, reconciles, tracks deadlines, drafts, and flags. Posting a ledger entry, releasing a payment, approving a disbursement, signing off a reconciliation, changing a vendor record, and sending anything to an owner, resident, or vendor always end with a human, and read-only access is how the agent is wired, not just a policy it follows.

Keep the answers current. When a threshold, a person, a bank account, or a statute changes, the config changes the same day; the questionnaire is a living document, not a one-time form.

Generic baseline document derived from the owner-reviewed bookkeeping and accounting contract. Nothing in this document is legal advice; confirm every state-law answer with your attorney.
