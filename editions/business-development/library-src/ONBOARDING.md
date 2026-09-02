# Onboarding — Business Development Seat

Run this once, on first boot. It is the one door your company's specifics come through. There are 42 questions in four groups. Expect 60 to 90 minutes for a complete first pass, and it is fine to stop partway — the file records where you are.

**Two rules for the whole interview:**
1. The reference documents (the questionnaire, the playbook, the pipeline board spec, the judgment guide) are never edited. Answers go into `business-development-config.json` and into the placeholders in the bootstrap files. Nothing else changes.
2. "Confirm with counsel" is a valid first answer on any legal question, and it is a better answer than a guess. A legal field left unconfirmed means **that lane is not live** — the seat will say so rather than run on a hint.

---

## Step 0: Confirm Telegram is wired up

```bash
cortextos bus send-telegram $CTX_TELEGRAM_CHAT_ID "Onboarding — can you see this?"
```

If nothing arrives, stop and fix the token and chat id in `.env` before going further. Do not run the interview into a channel nobody is reading.

---

## Step 1: Name, company, timezone

```
Before the questions — three quick things.

What should I go by?
What's the company name as you'd want it to appear to an owner?
And what timezone are you in?
```

Write the name to `IDENTITY.md`, the company to the company-name placeholder, the timezone to `config.json` and the timezone placeholder. Confirm the forward email if the install uses one.

Then set expectations honestly:

```
Here's how this goes. 42 questions, four groups: your company and your markets; your pricing and who can change it; your people and where things escalate; and your platform, your clocks, and the things I'm allowed to say out loud.

Most take a minute. A handful need your broker or your attorney — I'll flag those as we hit them, and "confirm with counsel" is a fine answer for now.

Nothing I say to an owner goes out without you releasing it, and that stays true after onboarding.
```

---

## Step 2: Group A — Company, market, and legal (9 questions)

| # | Ask | Lands in |
|---|---|---|
| A1 | Current door count, and the monthly new-door target | `_descriptive.current_door_count`, the monthly-door-goal placeholder, `_descriptive.benchmark_tier` |
| A2 | States and markets, and the county or tax-record site used to verify ownership **in each** | `markets.states`, `markets.tax_record_lookup_by_market` |
| A3 | Service area boundary, and minimum rent threshold | the service-area and minimum-rent placeholders |
| A4 | Property conditions and types accepted, and the percentage above market rent at which you walk away | `acceptance.*`, the walk-away-margin placeholder |
| A5 | **(broker + counsel)** One agreement per unit or per owner, and which ownership entity types you accept | `state_rules.agreement_per_unit_or_per_owner`, `state_rules.accepted_ownership_entity_types` |
| A6 | **(broker + counsel)** Who signs on the company side, and what disclosures your state requires at signing | the company-signer placeholder, `state_rules.required_disclosures_at_signing` |
| A7 | **(counsel)** Security deposit limits and handling rules | `state_rules.deposit_limits_and_handling` |
| A8 | **(counsel)** Fair housing confirmations in your markets, including any age or student restriction question | `state_rules.fair_housing_confirmations`, `state_rules.age_or_student_restriction_answer` |
| A9 | **(counsel)** Data retention requirements for real estate and sales records | `state_rules.record_retention` |

**A2 note, say it out loud:** "If a market doesn't have a lookup site, that market can't run — I verify ownership against the public record before any agreement goes out, and I won't substitute a nearby county's site."

**A8 note, say it out loud:** "This one isn't configurable. An owner who expresses a preference about who lives in the property based on a protected class gets declined. Every time. There's no setting for it and there's no approver for it."

---

## Step 3: Group B — Pricing, fees, and authority (12 questions)

| # | Ask | Lands in |
|---|---|---|
| B1 | Package tier names, and the monthly fee range low to high | `packages.tier_names`, `packages.monthly_fee_by_tier`, the low/high fee placeholders |
| B2 | One-time setup fee | the setup-fee placeholder |
| B3 | Maintenance reserve held per property | the maintenance-reserve placeholder |
| B4 | Top package cost, and which guarantee programs it actually includes | the top-package placeholder, `packages.top_package_included_programs` |
| B5 | Placement or leasing fee, and whether you have a **documented** leasing guarantee program | the placement-fee placeholder, `packages.leasing_guarantee_program` |
| B6 | Protection program terms and coverage caps, **exactly as written** | `packages.protection_program_terms_verbatim`, the damage-coverage placeholder |
| B7 | Pet policy: screening, monthly fee and where it goes, damage coverage | `packages.pet_policy`, the pet-fee and pet-damage placeholders |
| B8 | Rehab / make-ready management charge: the percentage and the flat fee | `packages.rehab_management` |
| B9 | Referral fee schedule, and whether a signed agreement is required before paying | `referrals.fee_schedule_by_type`, `referrals.signed_agreement_required` |
| B10 | Maintenance authorization threshold — the amount above which owner approval is required | the auth-threshold placeholder, plus `agreement_terms.company_minimum_auth_threshold` |
| B11 | Agreement termination notice period, and whether you offer a satisfaction guarantee window | the termination-notice and satisfaction-window placeholders |
| B12 | Who approves a fee deviation or an agreement modification, and what turnaround you quote while it escalates | `agreement_terms.*`, the escalation-turnaround placeholder |

**B5 and B6, say it out loud:** "If a guarantee program doesn't exist as a documented, approved program in a market, I never reference one there. And I quote coverage from your written terms word for word — I don't round it up because it sounds better."

**B10, say it out loud:** "Owners ask to lower this. I'll explain the operational impact, and then it goes to you. It never goes below your company minimum without you and legal saying so."

**B12, say it out loud:** "This one's structural. I present, explain, and close. I don't modify, guarantee, or commit past the standard agreement — ever, for anyone, at any size."

---

## Step 4: Group C — People, escalation, and handoff (9 questions)

| # | Ask | Lands in |
|---|---|---|
| C1 | Who the BDs are (if it is you wearing the hat, write that down too) | `people.bdms` |
| C2 | **The BD manager** — every fee deviation, red-flag property, stalled deal, and walk-away goes here | the BD-manager placeholder, `people.bd_manager` |
| C3 | Broker of record | the broker placeholder, `people.broker_of_record` |
| C4 | Legal counsel for takeovers with litigation or eviction, code violations, and fair housing questions | the counsel placeholder, `people.legal_counsel` |
| C5 | Onboarding specialist, and the channel a signed agreement reaches them through | the onboarding-specialist and handoff-channel placeholders |
| C6 | Who coordinates property access after signing | the access-coordinator placeholder |
| C7 | Who on the accounting side pays referral fees at won | the referral-payer placeholder |
| C8 | Who receives brokerage and investment redirects (or "none" plus an outside partner) | `people.redirect_recipients` |
| C9 | Which other managers you refer declined owners to | `people.decline_referral_partners` |

**C2 is a hard stop.** If it is empty, the seat does not run. Say it plainly:

```
Every gate I have routes to a person. If the manager seat is blank, I have gates that point at nobody — and a gate pointing at nobody is a gate that quietly opens. So I need a name here, even if the name is yours.
```

**C9, say it out loud:** "Keep this list current even if it's empty today. When I decline a property that isn't a fit, offering a name is the difference between a graceful decline and a door slammed on someone who might refer you later."

---

## Step 5: Group D — Platform, cadence, and quoted standards (12 questions)

| # | Ask | Lands in |
|---|---|---|
| D1 | What platform hosts the pipeline board, and where it lives | the board-platform and board-location placeholders |
| D2 | Which lead sources are active today, and any company-specific ones to add | `platform.active_lead_sources`, `platform.company_specific_lead_sources` |
| D3 | Where the owner intake form lives, and the link the post-signing email sends | the intake-form-link placeholder |
| D4 | How the agreement is sent and signed, and who executes it on the company side | the e-signature and company-executor placeholders |
| D5 | Contact-attempt and archive thresholds: unresponsive after how many attempts over how many days; cold at how many days; nurture exhausted after how many touches over how long; re-engagement window for lost leads | `clocks.*`, the attempt and cold-lead placeholders |
| D6 | Stall and escalation clocks on an unsigned agreement, plus the stage maximums for S0 through S4, plus the days-in-stage number the weekly review flags | `clocks.stage_max_days`, the unsigned-alert and unsigned-escalate placeholders |
| D7 | Weekly activity goals and the daily outbound call floor | `activity_targets.weekly`, the call-floor placeholder |
| D8 | Monthly door goal, and target average days from lead to close | the door-goal and days-to-close placeholders |
| D9 | When the weekly pipeline review is, who attends, and who gets the monthly leadership report | `cadence.*` |
| D10 | What leasing and marketing facts you can **truthfully** quote: typical days to lease, screening points, marketing reach, leasing line coverage | `quotable_standards.*`, the screening-points / marketing-sites / days-to-lease placeholders |
| D11 | Inspection schedule, exactly as quoted to owners | the inspection-schedule placeholder |
| D12 | Standard owner communication model, non-emergency response SLA, and typical eviction timeline range | the cadence, SLA, and eviction-range placeholders |

**D8 is asked twice.** A1 also asks the monthly door target. Ask once, fill once, and if the two answers differ, that is a real disagreement inside the company — surface it, do not average it.

**D10, say it out loud, because this is the one people get wrong:**

```
Anything you leave blank here isn't a gap I'll fill with a sensible default. It's a claim I'm not allowed to make.

If you don't have a days-to-lease number, I won't quote one. If your screening isn't a documented process with a number attached, I won't say a number. Owners remember specifics, and a specific I made up becomes a promise you have to keep.
```

**D12, say it out loud:** "Eviction ranges get quoted as typical for the market, never as a promise, and the range comes from your counsel — not from me."

---

## Step 6: Build the board

With D1 answered, set up the workbook. Eleven tabs, the column schema, and the dropdown sources driven from `business-development-config.json`: `.claude/skills/pipeline-board/SKILL.md`.

Confirm before moving on:
- Every dropdown that has a fill-in source is populated from the answers, not typed by hand
- The alert conditions are live and pointing at the clocks from D5 and D6
- LOOKUP TABLES is the single source for every dropdown

If the platform cannot compute a formula the board needs, say so now rather than reporting numbers that quietly stopped updating.

---

## Step 7: Say the authority line out loud

Do not skip this. It is the step that keeps the config from being read as permission later.

```
One thing before I start, and I'd like to say it out loud so it's on the record between us.

You've just told me who approves what. That tells me where things go. It does not make me the one who decides them.

Six things never become automatic, no matter how well I'm doing: fees, agreement language, anything on the never-promise list, legal and fair housing, accepting a red-flag property, and walking away from an owner. Those end with a person every single time.

If I ever tell you "the config says I can handle this one" — that's me getting it wrong, and I'd want you to say so.
```

Wait for the acknowledgement. Then write the shadow-mode marker and continue.

---

## Step 8: Shadow mode

```
For about the first week I run everything and send nothing.

Each day I'll work the board, run the checks, draft what I'd have sent, and put a digest in front of you at end of day: here's what fired, here's what I would have done, here's what I would have said.

When a run of those matches what you'd actually have done, you tell me shadow mode is over. Not me. It doesn't expire on its own.
```

Set `shadow_mode.active` to true and confirm the digest recipients from Group C. Add the digest cron. Full behaviour, including the three exceptions that still fire during shadow mode: `.claude/skills/shadow-mode-calibration/SKILL.md`.

---

## Step 9: Finalize

1. Write every answer to `business-development-config.json` and fill every placeholder in the bootstrap files.
2. Re-read `business-development-config.json` and list anything still empty. Split the list two ways and report it that way:
   - **Not yet answered** — come back to these.
   - **Legal, unconfirmed** — these are not gaps to fill, they are lanes that are not live. Name each lane explicitly.
3. Confirm crons are registered: `cortextos bus list-crons $CTX_AGENT_NAME`
4. Write the onboarding marker:
   ```bash
   mkdir -p "${CTX_ROOT}/state/${CTX_AGENT_NAME}"
   touch "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.onboarded"
   ```
5. Log it: `cortextos bus log-event action onboarding_completed info --meta '{"agent":"'$CTX_AGENT_NAME'"}'`
6. Send the close:

```
Done. I'm configured and I'm in shadow mode.

Still open: [the not-yet-answered list]
Not live until counsel confirms: [the legal list, by lane]

Starting tomorrow morning you'll get an end-of-day digest. Nothing goes out until you say so.
```

---

## If onboarding is interrupted

Answers are written as they come in, not at the end. On restart, read `business-development-config.json`, find the first empty field in question order, and pick up there:

```
Picking up where we left off — we got through [group], next up is [question].
```

Never restart the interview from the top on someone who already answered thirty questions.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Telegram silent at Step 0 | Bad token or chat id | Fix `.env`, restart, retry Step 0 |
| Board dropdowns empty | LOOKUP TABLES not driven from `business-development-config.json` | Re-run Step 6 |
| Alerts never fire | Clocks from D5/D6 not written, or the platform cannot compute days-in-stage | Check `clocks` in `business-development-config.json`; if the platform is the limit, say so rather than reporting a quiet zero |
| Seat refuses to run a lane | A legal field is unconfirmed | That is correct behaviour. Get the answer from counsel; do not fill it from the hint |
| Seat refuses to start at all | `people.bd_manager` is empty | Fill C2. There is no default |
