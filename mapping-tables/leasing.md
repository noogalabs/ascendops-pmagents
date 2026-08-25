# AscendOps PMAgents Lane 2: leasing questionnaire → agent-config MAPPING TABLE (worker draft for mapping QA reviewer QA)

Author: Lane 2 mapping-pass worker (L2-LEASING), 2026-08-25. Status: DRAFT — the mapping QA reviewer's
mapping-table QA seat first, orchestrator reviewer eyeballs after (same gate shape as the maintenance table).
Contract: glue-lane2-contracts-2026-08-24.md § CONTRACT L2-LEASING, executed verbatim.
Sources read TODAY:
- `private source-questionnaire archive` — all 39 Q,
  the source side. Counted fresh: 39 `Answer:` slots, 39 question headers, IDs A1-A14,
  B1-B9, C1-C6, D1-D10.
- `templates/leasing-coordinator/` — the destination side, censused BY FRESH GREP over
  IDENTITY / SOUL / GOALS / GUARDRAILS / SYSTEM / ONBOARDING / config.json. No prior count
  was trusted or consulted.
- `mapping-tables/maintenance.md` — the pattern: structure, taxonomy,
  cover-sheet precedent, the A3 cross-seat mark this pass reconciles.
- `engine/E2-SCHEMA.md` § 1 — the engine surface this mapping feeds
  (answers parser → mapping applier → gates → seat-config.json; seat cost = table +
  template + fixture, not new machinery).

Rule: every question gets a destination or an explicit UNMAPPED-AND-WHY; every template
placeholder gets a source or an explicit NO-SOURCE flag. Two directions, both proven below.

## Destination taxonomy

Reused verbatim from the maintenance table. No codes invented.

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct {{...}} substitution at configure time |
| K | config.json key | Merged into the agent's config.json |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board LOOKUP tab | The spreadsheet config block (questionnaire's own stated Group-D destination) — SECONDARY for the demo, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behavior (not just a value) |

Note on G for this seat: `templates/leasing-coordinator/GUARDRAILS.md` contains **zero
placeholders** (verified by grep). Every G destination in this table is therefore an
*appended generated block*, never an in-place substitution — the managed configuration
marker-block shape from scenario-1 contract 2, opened by the precedence sentence.

## Placeholder census (the template side, both directions)

**15 distinct placeholder types across 37 sites** in the seven contract-named files.
Per-placeholder site counts, derived fresh:

| Placeholder (sites) | Source |
|---|---|
| {{agent_name}} (4), {{org}} (2), {{current_timestamp}} (1) | add-agent substitutes already — 7 sites |
| {{income_multiplier}} (2) | **A2** — base ratio (Class B) to the placeholder, per-class map to S |
| {{credit_min_score}} (2) | **A3** — base floor (Class B) to the placeholder, per-class map to S |
| {{property_manager_name}} (2) | **D7** — the PM-of-record name only; the owner-approval seat above has no placeholder and goes S + I |
| {{day_mode_start}} (1), {{day_mode_end}} (1) | **NO LEASING QUESTION.** Org-seeded from `context.json` (verified: `templates/org/context.json` carries `day_mode_start`/`day_mode_end`/`timezone`) + CROSS-SEAT pointer to maintenance **B8**, which is the only question in the whole kit that asks the external-comms window. NOT a new cover-sheet field — see reconciliation X2. |
| {{company_name}} (3), {{timezone}} (2) | **NO SOURCE QUESTION** → cover sheet (shared 4-field header, maintenance precedent) |
| {{prospect_sla_minutes}} (2) | **NO SOURCE QUESTION** → cover sheet. The questionnaire names the speed-to-lead clock in D5's hint but never asks its value. |
| {{application_sla_hours}} (3) | **NO SOURCE QUESTION** → cover sheet. A12 is the post-*approval* hold window and A14 is the *incomplete*-file deadline; neither is the decision turnaround on a complete packet. |
| {{leasing_approval_threshold}} (2) | **NO SOURCE QUESTION** → cover sheet. A8 bounds the conditional-approval *menu* and D7 names *who* decides; no question asks the dollar figure the template escalates above. |
| {{renewal_lead_days}} (7), {{renewal_response_days}} (3) | **NO SOURCE QUESTION** → cover sheet. B3 gives the non-renewal notice period, which is a **floor constraint** on these values, not their source — see the CADENCE FLOOR finding. |

**FINDING → COVER SHEET:** the leasing answers-file header is **9 fields**: the shared
4-field maintenance header (company name, org short-name, forward email, timezone) kept
verbatim so cross-seat fixtures cohere, plus **5 leasing-specific** fields the questionnaire
never asks — prospect response SLA (minutes), application decision SLA (business hours),
leasing approval threshold (USD), renewal offer lead (days), renewal response window (days).
This is an answers-FILE addition. **The kit docs stay frozen**; no questionnaire edit is
proposed here, and the fixture proves the body is byte-verbatim (validation V2 below).

**FINDING → CADENCE FLOOR (new derived validation rule).** `IDENTITY.md:38` and
`SOUL.md:112` spend `{{renewal_lead_days}}` as an arithmetic cadence: chase at
`renewal_lead_days ÷ 2` and again with `renewal_lead_days ÷ 4` days left. Two consequences
the configurator must enforce, neither visible from either document alone:
1. `(renewal_lead_days − renewal_response_days) ≥ B3 non-renewal notice days`, or the
   renewal decision lands too late to legally serve non-renewal. **Hard fail.**
2. `renewal_lead_days` divisible by 4, or the two chase dates are non-integer days.
   **Warn.**
Fixture values satisfy both: 60 − 10 = 50 ≥ 30 ✓; 60 ÷ 4 = 15 ✓.

**VOCABULARY CLASS → RUNTIME-PRESERVED (additive, from the L1 lane).** A `{{TOKEN}}`
that holds a **runtime-environment value** rather than an answer-mappable one is classified
**RUNTIME-PRESERVED** with its `file:line` — never NO-SOURCE, never omitted. The known
instance is in the *sibling* template: `templates/maintenance-coordinator/ONBOARDING.md:127`
(`{{CTX_ROOT}}/state/{{agent_name}}/inbox/work-orders/`) — verified by reading that line, not
assumed from the addendum.

**For this seat the class is EMPTY, and here is exactly what was searched to say so:**
- `grep -nE '\{\{[A-Z][A-Z0-9_]*\}\}'` over the seven contract-census files
  (IDENTITY / SOUL / GOALS / GUARDRAILS / SYSTEM / ONBOARDING / config.json) → **zero hits**,
  including `ONBOARDING.md`, which is the file the maintenance instance lives in.
- The same pattern over the addendum files (`copilot-thresholds.json`, `goals.json`, all
  `.claude/skills/*/SKILL.md`) → **zero hits**.
- `grep -rhoE '\{\{[^}]*\}\}'` over the **entire** template, uniq'd, returns exactly the 15
  censused types plus `{{org_name}}` (addendum) plus the literal `{{...}}` doc-mention at
  `ONBOARDING.md:239`. Nothing else exists to classify.

**Divergence worth flagging to the L1 lane:** the leasing template *does* reference the same
runtime values — `$CTX_ROOT`, `$CTX_AGENT_NAME` and siblings appear in shell form across
`ONBOARDING.md`, `AGENTS.md`, `CLAUDE.md`, `TOOLS.md`, `HEARTBEAT.md` and 20 skill files —
but **never in placeholder syntax**. So the two sibling templates document identical runtime
values in two different notations, and only maintenance's notation collides with the
placeholder census. Shell-form `$CTX_*` is not census-eligible and needs no classification;
the risk is the reverse direction — a configurator that substitutes `{{...}}` blindly would
corrupt maintenance ONBOARDING.md:127 while leaving leasing untouched, so the two templates
would fail differently on the same code path. Recorded here, not acted on: template edits
are outside this contract.

**ADDENDUM — placeholders OUTSIDE the contract's census set** (recorded so the count above
is not mistaken for the whole template; these are NOT in the 15/37 totals):
`copilot-thresholds.json` — {{agent_name}} (1), **{{org_name}} (1)**; four skill files —
`application-screening-pipeline` {{application_sla_hours}} (1), `showing-coordination`
{{application_sla_hours}} (1), `lead-intake-triage` {{prospect_sla_minutes}} (1),
`renewal-execution` {{renewal_lead_days}} (5) + {{renewal_response_days}} (1).
**{{org_name}} is a 16th distinct type that appears ONLY outside the contract file set** —
it is sourced by the cover sheet's org short-name field, which is why the shared 4-field
header is kept whole for this seat rather than trimmed to what the 7 files need.

## Per-question mapping (39/39)

Grouped as the questionnaire groups them.

### Group A — Published Application Criteria and Policy (14)
| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 written published criteria exist per class | S, G, **C!** | Questionnaire's own stated pre-boot blocker: "the agent cannot check files against criteria that do not exist". CRITERIA-PUBLISHED flag; false → criteria-check and application-decision-prep classes DISABLED, PHASE-ZERO flag set |
| A2 income-to-rent ratio per class | **P {{income_multiplier}}**, S, G | Base ratio (Class B) → placeholder (2 sites); full per-class map → S (no placeholder exists for the map); published-criteria block → G |
| A3 credit score floor per class | **P {{credit_min_score}}**, S, G | Same shape as A2 — base floor to the placeholder (2 sites), per-class map to S. B1-override precedent from the maintenance table cited: scalar placeholder + structured map beside it |
| A4 eviction lookback per class | S, G | Per-class map; GUARDRAILS: inside-lookback routes to the PM, never an automatic denial |
| A5 individualized criminal assessment + who performs it | S, G | Names the assessor. **NEVER-GRADUATES gate** (questionnaire: "the agent never touches this") — the gate text ships in GUARDRAILS regardless of the answer, so this is G, not C!. Answer supplies the routing target |
| A6 application fee + refund by outcome + backup-fee rule | S, G | Fee, per-outcome refund matrix, and the backup-not-charged-until-primary-denied rule |
| A7 co-signer policy: which properties, what criteria | S, G | Per-class allowance + the independent-full-income condition |
| A8 conditional approval menu | S, G | Ordered menu the PM may draw from + the state cap note. Bounds, but does not source, {{leasing_approval_threshold}} |
| A9 backup application policy + tie-break rule | S, G | Tie-break written verbatim into GUARDRAILS: "applied identically every time" is the questionnaire's own consistency requirement |
| A10 pet policy/fee schedule/screening service + ESA owner | S, G, **C!** | Pet terms structured. ESA/service-animal path is armed by the named accommodation owner; unnamed → accommodation routing DISABLED and PHASE-ZERO flag. No pet fee, no pet rent, no pet screening on that path — ever |
| A11 Section 8 / voucher position per property | S, G, **C!** | Per-property confirmed map. The agent answers ONLY from a confirmed entry and never improvises; unconfirmed property → voucher-answer class DISABLED for that property, question routes to the PM. Forks on B6 |
| A12 hold policy: approval-hold window, showings-during-processing, holding fee | S, G, K | Three values. Approval-hold window is a clock → heartbeat/board prompt summary in config.json |
| A13 occupancy limit standard | S, G | Standard + the HUD-guidance basis |
| A14 incomplete-file response deadline | S, G, K | Value + the questionnaire's own requirement that the deadline is stated in writing when the request is sent |

### Group B — State Rules (9)
| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 deposit disposition deadline + what date starts the clock | S, G | **CROSS-SEAT (A3-class).** The *deadline value* is owned by the turnover seat; leasing holds a pointer. B1's **trigger-date component is unique to leasing** — maintenance A3 does not ask it — so leasing contributes that half. See reconciliation X1 |
| B2 tenant notice-to-vacate + month-to-month notice each direction | S, G | **Leasing OWNS.** Turnover reads it as the move-out trigger clock (pointer, not duplicate) |
| B3 non-renewal notice period + delivery method | S, G | **NEVER-GRADUATES gate**: PM or attorney serves, never the agent — text ships regardless of answer, so G not C!. Also the FLOOR input to the CADENCE FLOOR rule above |
| B4 state application fee refund requirements | S, G | Statutory position + the company's abandonment stance |
| B5 application/screening records retention | S, G, K | Retention clock → purge/retain prompt in config.json |
| B6 source of income a protected class per jurisdiction | S, G, **C!** | Per-jurisdiction map. Questionnaire's own words: "The entire Section 8 conversation script forks on this answer." Arms which A11 script branch is live per property |
| B7 consequences of insufficient notice + what may be said | S, G | **NEVER-GRADUATES gate**: agent flags only, never states consequences to a tenant. Answer supplies what the PM may say, not what the agent may say |
| B8 properties built before 1978 | S, G, **C!** | Lead-based-paint disclosure list. Arms disclosure attachment on every lease and listing for those units. **Present-and-empty ≠ absent** (maintenance C8 precedent) — an empty list is still written |
| B9 pre-move-out walkthrough Y/N + who conducts | S, **C!** | Y/N forks which library checklist the company uses. **CROSS-SEAT**: inspection ownership belongs to the turnover seat; leasing schedules and hands off. See reconciliation X3 |

### Group C — Showing Rules (6)
| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 showing method per property or class | S, G, **C!** | Per-class/per-property method map arms self-show vs agent-led; higher-risk override preserved |
| C2 self-show platform + ID verification protocol | S, G, **C!** | Questionnaire's own stated pre-boot blocker for self-show: "a code never releases without completed ID verification, no exceptions". ID-VERIFICATION-PROTOCOL flag; false → self-show and code-release classes DISABLED and PHASE-ZERO flag, even where C1 says self-show |
| C3 showing agent roster + where calendars live | S, I, G | Roster structured + calendar location; GUARDRAILS carries the questionnaire's rule that a showing time is never promised before the resource is confirmed. Empty roster → PHASE-ZERO flag |
| C4 lockbox conventions: rotation + time-limited codes | S, G | Rotation schedule + time-limited-code policy. Distinct from maintenance D8 (which asks code *storage*) — the two are complementary, not duplicates; seam noted in X4 |
| C5 showing windows and hours | S, G | **Explicitly NOT the day-mode source.** A showing window is when showings are *booked*; day mode is when the agent may *communicate*. Mapping them together would silently narrow the comms window. GUARDRAILS carries "outside the window is offered the next available slot, not an exception" |
| C6 properties with video tour assets | S | Asset inventory + location. Empty is a valid answer, not a blocker |

### Group D — Platform, People, and Wiring (10)
| Q | Destination(s) | Mapping detail |
|---|---|---|
| D1 property management software | S | No {{platform}} placeholder exists in this template (unlike maintenance) — S-only. **CROSS-SEAT consistency check** against maintenance D1, see X5 |
| D2 screening service + what the agent may see | S, G, **C!** | Arms the screening-visibility scope. FCRA block into GUARDRAILS: summary flags and pass/fail against a documented criterion only, never report contents, never reaches an owner |
| D3 e-signature tool + does it auto-file into PM software | S, G, **C!** | AUTO-FILE flag. False → the named filer + location becomes the clock source; if neither is named, lease-follow-up clocks have no record to read → those classes DISABLED and PHASE-ZERO flag |
| D4 syndication set + credential holders | S, I | Auto-syndicated set vs manual sites; per-site credential owner. Manual sites flagged as human-step |
| D5 where rental inquiries land today | S, I | Lead-source inventory. Questionnaire's own test: "Every lead source must land somewhere the agent can read, or the speed-to-lead clock is fiction" — any unreadable source → PHASE-ZERO flag. Note this question does NOT supply {{prospect_sla_minutes}} |
| D6 outbound identity: SMS number, email identity, sender persona | S, G, K | Identity triple → seat-config + config.json sender keys; the pre-send-review-until-graduation rule → GUARDRAILS |
| D7 PM seat deciding approvals/denials/rates/renewals/holds + owner-approval seat above | **P {{property_manager_name}}**, S, I, G | PM name → placeholder (2 sites). The owner-approval seat above has **no placeholder** — S + IDENTITY routing prose. GUARDRAILS: every housing decision belongs to the named person |
| D8 where the leasing board lives | S, **B** | Spreadsheet-vs-in-platform decision. B destination listed for completeness; board wiring is a stated non-goal |
| D9 calendar carrying showings and move-ins | S, I, K | Calendar ID + visibility list. **CROSS-SEAT**: the move-in half seams with turnover, see X6 |
| D10 escalation channels + to whom | S, K, I | Channel-per-audience map; escalation prompts in config.json reference them. **CROSS-SEAT consistency** with maintenance D6, see X5 |

## Cross-seat reconciliation (contract step d)

Every shared value resolves to **ONE owner seat with a pointer, never duplicated**. Seams
reference by QUESTION ID only — the sibling turnover pass runs in parallel, so no line
numbers from another table are cited.

| # | Shared value | Owner seat | Pointer holders | Resolution |
|---|---|---|---|---|
| X1 | Security deposit disposition **deadline** | **MAINTENANCE (A3)** ~~TURNOVER~~ | turnover A1, leasing B1 | **QA-AMENDED (mapping QA reviewer, 2026-08-25 ~0330Z): the parallel turnover pass ruled the same seam the OPPOSITE way (its SEAM-1: owner = maintenance A3, with a named bookkeeper-seat migration trigger and the holding order maintenance → turnover → leasing). QA resolves the collision FOR maintenance ownership:** maintenance is the only seat with a sealed accepted configuration today, so an install configured seat-by-seat always has the owner present first, and the turnover pass — this row's proposed owner — itself declined ownership with the richer analysis. Original lifecycle argument (disposition executes at move-out) preserved for the record but does not outweigh install-order reality. **Unchanged and agreed by both passes:** leasing B1's *what-date-starts-the-clock* sub-value is leasing-owned and pointed at by the others. One number, one owner (maintenance A3); one trigger, one owner (leasing B1). |
| X2 | External communications window → {{day_mode_start}}/{{day_mode_end}} | **MAINTENANCE (B8)** | leasing template placeholders | Leasing has no question asking the comms window. Rather than mint a cover-sheet field that would duplicate maintenance B8, the leasing seat takes the org `context.json` seed and points at B8 when the maintenance seat is configured for the same company. **Rejected alternative recorded:** mapping leasing C5 (showing hours) → day mode. C5 is a booking window, typically narrower than the comms window; that mapping would have silently muted the agent outside showing hours. |
| X3 | Pre-move-out walkthrough + move-out inspection ownership | **TURNOVER** | leasing B9 | Leasing B9 asks Y/N and who conducts. Leasing's own role is scheduling + handoff; the inspection itself is turnover's. Leasing stores the Y/N fork (it decides which library checklist the company uses) and a pointer to the conducting seat. **Turnover's explicit three-way seam note is expected to cite leasing B9 by ID.** |
| X4 | Access/lockbox codes | **SPLIT — not a duplicate** | maintenance D8, leasing C4 | Maintenance D8 asks where codes are *stored* and how they reach an assigned vendor/tech. Leasing C4 asks *rotation cadence* and time-limited-code policy for showings. Different values, one shared security rule (codes never reach a resident-facing or owner-facing surface). Recorded as a seam so a later pass does not collapse them into one field. |
| X5 | Platform identity (D1) and escalation channels (D10) | **PER-SEAT, consistency-checked** | maintenance D1/D6, leasing D1/D10 | Each questionnaire asks these independently and the configurator writes them per seat, so ownership does not transfer. What is required is a **cross-seat consistency assertion**: if two seats are configured for the same company and their platform strings or escalation-channel targets disagree, that is a contradiction for the scenario-1 contradiction report, not a silent last-writer-wins. |
| X6 | Move-in appointments on the showings calendar (D9) | **LEASING** | turnover | The calendar is leasing-owned (showings dominate it). The move-in appointment and key handoff are the leasing→turnover handoff point; turnover holds a read pointer. |

**New cross-seat marks this pass contributes** (X2, X4, X5, X6 did not exist before this
table): recorded here so the turnover pass and the mapping QA reviewer's QA seat can reconcile against them
by ID rather than rediscovering them.

## Coverage proof (two-direction census — the deliverable)

**Direction 1 — questions covered: 39/39.**
A-group 14/14 (A1-A14) + B-group 9/9 (B1-B9) + C-group 6/6 (C1-C6) + D-group 10/10
(D1-D10) = **39**, which equals the censused total (39 `Answer:` slots and 39 question
headers, counted fresh from the kit file). **Zero UNMAPPED.**
Weakest mappings flagged honestly, S-only or near-it, no placeholder and no prose consumer
beyond seat-config today: **C6** (video asset inventory — consumer is message-composition
logic that is prose today), **D8** (board location — B destination is out of demo scope),
**D4** (syndication set — no machinery reads it yet). These are recorded as weak, not
dressed up.

**Direction 2 — placeholders covered: 15/15 distinct types across 37/37 sites.**
- 3 types / 7 sites — add-agent substitutes already: {{agent_name}}, {{org}}, {{current_timestamp}}
- 3 types / 6 sites — sourced from the questionnaire: {{income_multiplier}} (A2),
  {{credit_min_score}} (A3), {{property_manager_name}} (D7)
- 2 types / 2 sites — org-seeded + cross-seat pointer, NOT duplicated into a cover-sheet
  field: {{day_mode_start}}, {{day_mode_end}} (maintenance B8 owns — X2)
- 7 types / 22 sites — cover sheet: {{company_name}}, {{timezone}}, {{prospect_sla_minutes}},
  {{application_sla_hours}}, {{leasing_approval_threshold}}, {{renewal_lead_days}},
  {{renewal_response_days}}
- 0 types / 0 sites — **RUNTIME-PRESERVED**: the class is empty for this seat; the
  searches that establish that are named above, not asserted bare.
- Sum: 3+3+2+7 = **15 types**; 7+6+2+22 = **37 sites**. Both equal the censused totals.
**Zero bare NO-SOURCE flags** — every one of the 9 no-question placeholders carries the
reason it has no question, in the census table above.

**Conditional gates: 10**, each traceable to the questionnaire's own text, not invented —
A1 (criteria-exist pre-boot blocker), A10 (ESA accommodation owner), A11 (per-property
voucher confirmation), B6 (source-of-income fork), B8 (pre-1978 disclosure list), B9
(walkthrough Y/N fork), C1 (showing-method arming), C2 (ID-verification pre-boot blocker),
D2 (screening-visibility scope), D3 (auto-file clock source).
**Never-graduates gates preserved as prose regardless of answer: 3** — A5 (criminal
history), B3 (non-renewal service), B7 (insufficient-notice consequences). These match the
questionnaire's own "What Happens Next" list of gates that never graduate at any setting.
**PHASE-ZERO flag sites: 6** — A1, A10, C2, C3, D3, D5.

## Golden fixture + validation record (contract step e / § 3)

**File:** `outputs/ridgeline-leasing-answers-2026-08-25.md`
**Company:** Ridgeline Residential Management (`ridgeline`, America/Denver) — the **same
fictional company as scenario 1**, identity reused from `editions/maintenance/
ridgeline-maintenance-answers.md` so cross-seat fixtures cohere: 186 doors, Pine Basin and
Cedar Mesa markets, Class B and C, WorkTrail as system of record, LedgerPeak for
accounting, Ellis Shore as the Portfolio Director above the seat, the 30-calendar-day
deposit deadline carried consistently with X1, and the `@ridgeline.example` mail domain.
Leasing-only fictional entities added: Dana Wren (PM), Priya Sandoval and Colton Reyes
(showing agents), OpenDoorway (self-show), ClearFile (screening), InkPath (e-sign),
PawCheck (pet screening).

Gate states deliberately mixed, per the scenario-1 fixture-B precedent (one confirmed, one
unconfirmed, so both branches are exercised): CRITERIA-PUBLISHED=true, SOURCE-OF-INCOME-
CONFIRMED=true, ID-VERIFICATION-PROTOCOL=true, AUTO-FILE=true — and **VOUCHER-POSITION-
CONFIRMED=false for Cedar Mesa**, which leaves the A11 voucher-answer class disabled for
that market while it is live for Pine Basin.

| # | Check | Method | Result |
|---|---|---|---|
| V1 | Two-direction counts | Counted fresh from kit file and from grep census; both restated above | 39/39 questions, 15/15 types, 37/37 sites — **PASS** |
| V2 | Kit docs stay frozen | `diff` blank questionnaire vs fixture | Removed lines: exactly the 39 blank `Answer:` slots, nothing else. Added lines: only filled `Answer:` lines, their 2-space continuations, and the 12-line cover-sheet/format header. **Questionnaire body byte-verbatim — PASS** |
| V3 | Fixture parses clean | See PARSER NOTE below | 9/9 cover fields, 39/39 answers, 0 missing, 0 extra, 0 blank, continuation-join clean — **PARSE RESULT: CLEAN**, exit 0 |
| V4 | No bare flags | Every UNMAPPED/NO-SOURCE entry carries a reason | 0 UNMAPPED; 9 NO-SOURCE, each with its reason in the census table — **PASS** |
| V5 | Fictional-only (scenario-1 fixture-B rule) | Regex scan restricted to answer text for real org/person/platform strings | **ZERO hits across all 39 answer blocks.** The three matches elsewhere in the file (`orchestrator reviewer` in the frontmatter provenance line, the `AppFolio, Buildium, Rent Manager, Propertyware` example in D1's hint, the `Ascend Operations Library` footer) are frozen kit text preserved byte-verbatim by V2, not answers — **PASS** |
| V6 | Cadence floor | Fixture values against the derived rule | 60 − 10 = 50 ≥ 30 (B3) ✓; 60 ÷ 4 = 15, integer ✓ — **PASS** |

**PARSER NOTE — read this before accepting V3.** The contract asks that the fixture parse
clean through *the scenario-1 parser*. **That parser is not present in this tree.** Only
scenario-1 contract-1 artifacts landed (`editions/maintenance/` = `answers-format.md`
plus the two maintenance fixtures); contract-2's reconfigurator, which contains the parser,
is not on disk anywhere under `cortextos/` and no internal build branch or commit carries it
(searched by filename, by content signature, and by git log). Rather than claim a check
that could not be run, V3 was executed against a parser written **to the rules stated
verbatim in `answers-format.md`** — `Answer:` line per question, two-space continuation
lines belonging to the preceding answer until the next question or heading, cover-sheet
key/value header. It asserts the 39+9 counts by name. **This is a stand-in, not the real
gate.** When contract-2's parser exists, re-run V3 against it; the fixture is built to the
same format spec the maintenance fixtures use, so it should pass unchanged, but that
remains unproven until it actually runs.

## seat-config.json shape (leasing seat)

Same top-level shape orchestrator reviewer already blessed for maintenance, so one engine reads both:
`{seat: "leasing", company: {…9-field cover sheet…}, answers: {A1..D10 raw text},
derived: {criteria{per_class{income_multiplier, credit_min_score, eviction_lookback}},
fees{}, holds{}, clocks{}, notices{}, people{}, roster{}, showing{}, channels{},
gates{confirmed_flags}, disclosure_lists{pre_1978[]}, phase_zero[]},
cross_seat: {owned:[], pointers:[{value, owner_seat, owner_question_id}]},
provenance: {questionnaire_version, filled_by, date}}`

Two leasing-specific additions to the maintenance shape, both load-bearing:
- **`cross_seat`** — makes X1-X6 machine-readable. Without it, "owner seat + pointer" is
  prose that the next seat's configurator cannot check, and the duplication the rule
  forbids reappears silently at configure time.
- **`derived.criteria.per_class`** — A2/A3/A4 are all per-class, and the template
  placeholders are scalars. The scalar goes to the placeholder, the map lives here; a
  configurator that wrote only the scalar would lose the Class C policy entirely.

Raw answers are ALWAYS preserved verbatim beside derived values — re-mapping is possible
without re-asking.

## Handoff

Worker stops here per contract: table + fixture, no build, no configurator run, no
`add-agent`, `templates/` untouched, kit untouched. Next: the mapping QA reviewer's mapping-table QA seat,
then orchestrator reviewer eyeball, then this table feeds Lane 1's configurator work.
