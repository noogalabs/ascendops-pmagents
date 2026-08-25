# AscendOps PMAgents glue: turnover questionnaire → agent-config MAPPING TABLE (draft for mapping QA reviewer QA, then orchestrator reviewer)

Author: Lane 2 turnover mapping worker, 2026-08-25. Status: DRAFT — mapping QA reviewer QA seat first,
orchestrator reviewer eyeballs after (same gate shape as the maintenance table).
Contract: outputs/glue-lane2-contracts-2026-08-24.md § CONTRACT L2-TURNOVER (executed as
written; shared rules block binding).

Sources read for this pass:
- `private source-questionnaire archive` — all 34 Q,
  frozen kit doc, source side.
- `templates/turnover-coordinator/` — destination side, census derived FRESH by grep today
  (no prior count trusted). Commands and raw counts recorded in the census section.
- `mapping-tables/maintenance.md` — pattern, taxonomy, cover-sheet
  precedent, and the A3 cross-seat mark this pass reconciles.
- `engine/E2-SCHEMA.md` § 1 — the engine surface this feeds.
- `editions/maintenance/answers-format.md` + `ridgeline-maintenance-answers.md` — the
  sealed scenario-1 answers format and the fictional company identity reused here.

Rule (from the contract, non-negotiable): every question gets a destination or an explicit
UNMAPPED-AND-WHY; every destination slot gets a source or an explicit NO-SOURCE flag. Both
directions proven by count in this file. The census is the deliverable.

---

## Destination taxonomy

Reused VERBATIM from the maintenance table. No codes invented.

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct `{{...}}` substitution at configure time |
| K | config.json key | Merged into the agent's config.json |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board LOOKUP tab | The spreadsheet config block (the questionnaire's own stated Group-B/C destination) — SECONDARY, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behavior (not just a value) |

---

## Cross-seat reconciliation doctrine (LOAD-BEARING for this seat)

The contract requires every shared value to resolve to ONE owner seat plus a pointer, never
duplicated. Applying that needs a test, because two seats asking similar-sounding questions
are not always asking about the same thing. The test used throughout this table:

> **Is the answer a fact about the company, the portfolio, or the law — one truth that cannot
> differ by seat? Or is it a policy this seat sets — a truth that may legitimately differ from
> the neighbouring seat's?**

- **FACT** → exactly ONE seat's seat-config carries the value. Every other seat carries a
  pointer record (`{owner_seat, owner_question_id}`) and no copy. Changing it is a one-place edit.
- **POLICY** → each seat OWNS its own value. These are not duplicates and must not be
  collapsed. They get a CONTRADICTION CROSS-CHECK instead: the configurator surfaces the pair
  for human eyeball when the values differ, and never auto-unifies them.

Collapsing a POLICY pair into one "shared" value is the failure mode this doctrine exists to
prevent — it silently overwrites one seat's deliberate choice with another seat's. The
maintenance/turnover approval thresholds (SEAM-8) are the worked example: same shape, same
owners, different authorities, correctly different numbers.

**Single-state rule.** At any moment exactly one seat-config holds a FACT value; the others
hold pointer records only. Where the owner seat is not installed yet, ownership falls to the
next seat in a FIXED order named in the seam row, and the holding seat records
`held_pending_seat: <owner>`. There is never a moment when two seat-configs both carry the value.

---

## Destination census — the template side (derived fresh today)

Commands run (read-only, `templates/turnover-coordinator/`):

```
grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}' . | sort | uniq -c | sort -rn     # 13 types, 45 sites
grep -roE  '\{\{[a-zA-Z0-9_]+\}\}' . | sort | uniq -c                # per-file breakdown
grep -rlE  '\{\{[a-zA-Z0-9_]+\}\}' .                                 # 11 files
```

Negative-search note (a negative is only as good as its spelling): also swept for
`{{ spaced }}` / `{{a.b}}` forms, `${VAR}`, `<ALLCAPS>`, and `__TOKEN__`. Only hits were
`{{...}}` as literal prose in ONBOARDING Step 11, runtime env vars (`${CTX_ROOT}` etc., not
configure-time), and `<TOKEN>`/`<YOUR_TOKEN>` in `.env.example` instructions. None are
mapping destinations.

### RUNTIME-PRESERVED class (census vocabulary addendum from the L1 lane)

A double-brace token can carry a RUNTIME-environment value rather than an answer-mappable
one. Those are **RUNTIME-PRESERVED**: the applier leaves them for the runtime to resolve.
The class is neither NO-SOURCE (which would send it to the cover sheet and invent a question
for it) nor omitted (which would silently shrink the census).

Swept for it explicitly:

```
grep -rnoE '\{\{(CTX_[A-Za-z0-9_]+|[A-Z][A-Z0-9_]{2,})\}\}' .
```

**Result for `templates/turnover-coordinator/`: NO MATCH. Zero RUNTIME-PRESERVED tokens in
this seat**, so the 13-type / 45-site count above is unchanged and no line moves class.

The negative is a proven one, not a hollow one: the identical sweep run against
`templates/maintenance-coordinator/` returns the known instance,
**`{{CTX_ROOT}}` at `maintenance-coordinator/ONBOARDING.md:127`** — so the pattern does detect
the class it claims to rule out. That instance sits inside a message the agent speaks to the
member, displaying the inbox path `{{CTX_ROOT}}/state/{{agent_name}}/inbox/work-orders/`. Note
the line mixes two classes: `{{CTX_ROOT}}` is RUNTIME-PRESERVED, `{{agent_name}}` on the same
line is an add-agent substitution — so a per-line classification is wrong; classification is
per token.

Why this seat is clean: turnover writes the same variable in shell form,
`${CTX_ROOT}` at `turnover-coordinator/ONBOARDING.md:214`, which never enters a double-brace
census in the first place. That is a template-authoring difference between the two seats, not
a difference in what the two agents need at runtime — so a future turnover template edit could
introduce the class here, and the sweep above is the check to re-run.

### 13 placeholder types / 45 sites, across 11 files

| Placeholder (sites) | Source |
|---|---|
| `{{agent_name}}` (8), `{{org}}` (2), `{{current_timestamp}}` (1) | add-agent substitutes already |
| `{{approval_threshold}}` (3) | **C1** (base reserve number only — see the C7 trap below) |
| `{{turn_target_days}}` (6) | **B2** (per-class map reduced to the modal-class scalar — weak mapping, see B2 row) |
| `{{property_manager_name}}` (2) | **D3** |
| `{{inspection_sla_hours}}` (5) | **NO QUESTION ASKS THIS** → cover sheet |
| `{{scope_sla_hours}}` (4) | **NO QUESTION ASKS THIS** → cover sheet |
| `{{stale_stage_alert_days}}` (7) | **NO QUESTION ASKS THIS** → cover sheet |
| `{{company_name}}` (3) | **NO QUESTION ASKS THIS** → cover sheet |
| `{{timezone}}` (2) | **NO QUESTION ASKS THIS** → cover sheet |
| `{{day_mode_start}}` (1), `{{day_mode_end}}` (1) | **NO QUESTION ASKS THIS** → cover sheet |

Site split: **11 add-agent + 11 questionnaire + 23 cover-sheet = 45.**

### 5 config.json keys that are literal defaults, NOT placeholders

A placeholder-only census misses these, and missing them is a silent-wrong-value bug rather
than a visible unsubstituted `{{...}}`:

| config.json key | Shipped literal | Source | Same value as |
|---|---|---|---|
| `"timezone"` | `""` (empty string) | cover sheet | `{{timezone}}` |
| `"turn_target_days"` | `10` | B2 | `{{turn_target_days}}` |
| `"inspection_sla_hours"` | `48` | cover sheet | `{{inspection_sla_hours}}` |
| `"scope_sla_hours"` | `24` | cover sheet | `{{scope_sla_hours}}` |
| `"stale_stage_alert_days"` | `2` | cover sheet | `{{stale_stage_alert_days}}` |

These are K-homes of five placeholder types already counted, so they add **0 new values** but
**5 new destination slots**. Total destination slots: **13 placeholder types + 5 K keys = 18**.

**Two-direction total: 18/18 destination slots sourced, 0 bare NO-SOURCE flags.**

---

## Two engine-shape findings the maintenance seat could not have surfaced

Both compare the turnover template against `templates/maintenance-coordinator/`, which is the
only template the sealed scenario-1 applier has ever run against.

**FINDING E1 — placeholders live inside `.claude/skills/`, which maintenance has zero of.**

| Template | Placeholder-bearing files | Any under `.claude/skills/`? |
|---|---|---|
| maintenance-coordinator | 8 (bootstrap + config.json + copilot-thresholds.json) | **none** |
| turnover-coordinator | 11 (bootstrap + config.json + **4 skill files**) | **yes — 10 sites** |

Of those 10 skill sites, 4 are `{{agent_name}}` (add-agent's path) and **6 are mapping-owned**,
all in `.claude/skills/make-ready-pipeline/SKILL.md`: `{{turn_target_days}}`×1,
`{{inspection_sla_hours}}`×1, `{{scope_sla_hours}}`×1, `{{stale_stage_alert_days}}`×3.
An applier whose file set is a fixed bootstrap list leaves those 6 sites unsubstituted, in the
one skill that actually runs the make-ready pipeline. **The applier's file set must include
`.claude/skills/`.**

Corroborating defect in the template's own instructions (read-only observation, not this
worker's file to fix): `ONBOARDING.md:161` directs saving the five threshold values to
`IDENTITY.md`, `SOUL.md`, and `config.json` — it never mentions `make-ready-pipeline/SKILL.md`.
A human following the shipped onboarding misses the same 6 sites.

**FINDING E2 — `"timezone": ""` is an active wrong-clock hazard, not a benign blank.**

`src/daemon/agent-manager.ts:2196` on the live tree reads:

```
const tz = agentConfig.timezone || 'America/New_York';
```

A bare OR treats the shipped empty string as "unset" and silently runs the agent on Eastern.
For the golden fixture's company (America/Denver) that is a 2-hour cron shift with no error.
All four templates checked ship `"timezone": ""`, so this is fleet-shaped, not turnover-only.
Consequence for this mapping: the cover-sheet timezone **must** be written into `config.json`,
not only substituted into `SOUL.md` prose. A timezone-coercion fix was in flight tonight
(PR292); Lane 1 should re-read line 2196 before building rather than assuming either state.

---

## Cover sheet (the answers-FILE addition — kit docs stay FROZEN)

Maintenance precedent: a 4-field header the questionnaire never asks. Turnover needs those
four for cross-seat format parity plus five stage-clock fields this questionnaire never asks:

| Field | Fills | Note |
|---|---|---|
| Company name | `{{company_name}}` (3 sites) | |
| Org short-name | — | **UNUSED BY THIS SEAT**: no `{{org_name}}` in this template. Carried for answers-file format parity across seats. |
| Forward email | — | **UNUSED BY THIS SEAT**: no `{{forward_email}}` in this template. Carried for parity. |
| Timezone | `{{timezone}}` (2 sites) + `config.json:"timezone"` | See FINDING E2 |
| Day mode start | `{{day_mode_start}}` (1 site) | No `day_mode_*` key exists in any template config.json; the applier must CREATE the keys or accept that the window lives only in SOUL prose. ONBOARDING Step 8 instructs writing keys that are not there. |
| Day mode end | `{{day_mode_end}}` (1 site) | as above |
| Inspection SLA hours | `{{inspection_sla_hours}}` (5) + K | template default 48 |
| Scope SLA hours | `{{scope_sla_hours}}` (4) + K | template default 24 |
| Stale-stage alert days | `{{stale_stage_alert_days}}` (7) + K | template default 2 |

Why the three stage clocks are genuinely NO-SOURCE and not a lazy flag: the questionnaire's
Group B asks OUTCOME clocks (turn time, punch-list completion) but never the agent's INTERNAL
STAGE clocks. The template's own `ONBOARDING.md:150-161` interview asks five threshold
questions; three of them — inspection SLA, scope SLA, stale-stage alert — have no counterpart
anywhere in the 34. The gap is provable in both documents.

Adjacency traps refused, deliberately (a check whose subject is silently substituted is worse
than an honest flag):

- **A1's 48-hour SLA is NOT `{{inspection_sla_hours}}`.** A1 clocks the evidence package
  reaching the deposit process. The placeholder clocks inspection findings reaching the agent
  (`IDENTITY.md:43`, "escalate draft to PM if missing"). Different subjects, same number by
  coincidence. Mapping A1 onto it would be a substituted subject.
- **B4's punch-list deadline is NOT `{{scope_sla_hours}}`.** B4 is remediation after a FAILED
  final inspection (`turnover-tracking-board-source-2026-08-19.md:459,682` — punch list is
  created on final-inspection failure). `{{scope_sla_hours}}` is Stage-2 scope drafting.
- **E8's per-person escalation hours are NOT the agent's day-mode window.** Adjacent enough to
  seed the cover-sheet default, never enough to set it silently. Cover sheet, human confirms.

---

## Per-question mapping (34/34)

### Group A — Legal and Deposit Interlocks

| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 deposit disposition deadline + evidence-package SLA | S, G | **SPLIT.** The statutory deadline is a FACT → pointer only, owner = maintenance A3 (SEAM-1, three-way with leasing B1). The 48-hour evidence-package handoff SLA is turnover-OWNED and is the only new value this question contributes. GUARDRAILS carries the handoff clock, not the statute. |
| A2 pre-move-out inspection legally required | S, G, **C!** | Arms/disarms the pre-move-out walkthrough as a standard step. Gate records WHY it is armed: statute or company policy. A policy-armed step is disarmable by the member; a statute-armed step is not (SEAM-2). |
| A3 damage dispute window | S, G | FACT → pointer, owner = maintenance A5 (SEAM-3). Notice templates read the owner's value. |
| A4 certified-mail requirement | S, G, **C!** | FACT → pointer, owner = maintenance A4 (SEAM-4). The gate (delivery=certified-mail on the high-consequence notice classes) is armed locally from the pointed-at value; maintenance precedent preserved verbatim. |
| A5 lease sections list | S, G | FACT → pointer, owner = maintenance A6 (SEAM-5). GUARDRAILS: every damage notice cites one of these. |
| A6 lawn care / HVAC filter lease assignment | S, G | **Turnover-OWNED FACT** — no maintenance or leasing question asks it, and maintenance is a downstream consumer for occupied-unit wear calls (SEAM-9, reverse pointer). Drives the damage-versus-wear call on the two most common move-out findings. |

### Group B — Property Classes and Benchmarks

| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 per-unit class map | S, B | **Turnover-OWNED FACT** at the finest grain in the fleet (SEAM-6): maintenance A1 and leasing A1-A4 hold class LABELS, only B1 holds the unit→class MAP. S-only for machine use (no placeholder exists for a map) — maintenance B1-override precedent cited. If the answer says no map exists → PHASE-ZERO flag in seat-config, per the question's own hint. |
| B2 turn-time targets per class | **P `{{turn_target_days}}`** (6 sites), **K**, S, G, B | **WEAK MAPPING, flagged honestly.** The answer is a per-class map; the placeholder and the config key are scalars. Reduction rule: the scalar takes the value for the portfolio's MODAL class by door count, recorded as `turn_target_days.placeholder_source_class` in seat-config; the full map goes to S and to a GUARDRAILS precedence sentence — *the per-class map governs; the single number in IDENTITY/SOUL/config.json is the portfolio default for the modal class.* Without that sentence `SOUL.md:197` ("any deviation from the `{{turn_target_days}}`-day target that requires a PM decision") mis-gates every non-modal class. |
| B3 make-ready budget bands per class | S, G, B | No placeholder exists. Per-class map + warning/over bands structured. Candidate future placeholder; S-only today (maintenance B2 precedent). |
| B4 punch-list completion deadlines per class | S, G, B | No placeholder. Explicitly NOT `{{scope_sla_hours}}` — see the adjacency trap above. |
| B5 turnover grading scorecard weights | S, B | Five weights structured; consumer is the grading scorecard, prose today. Weak in the same sense as maintenance B11 — named, not hidden. |
| B6 turnover-rate baseline + door count of record | S, B | **Turnover-OWNED FACT** for the door count (SEAM-7): maintenance A1 holds portfolio size as descriptive prose; only B6 designates a denominator "of record". The monthly report header reads both numbers from here. |

### Group C — Scope and Owner-Approval Rules

| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 pre-approved reserve threshold per owner | **P `{{approval_threshold}}`** (3 sites), S, B | Base number → placeholder; per-owner overrides → seat-config map (no placeholder exists for overrides). Exact maintenance B1 shape. POLICY, not shared with maintenance B1 (SEAM-8). |
| C2 scope-change ladder | S, G, **C!** | Three rungs structured. Gate: the call rung is human-executed — the agent drafts and tracks, never places the call. The gate text ships in GUARDRAILS whether or not the member changes the ladder. |
| C3 safety fix-first cap | S, G, **C!** | Below cap: dispatch then notify. At or above: wake the on-call human first. Safety-item list preserved from the question's own hint unless overridden. |
| C4 silent-owner decision-maker | S, I, **C!** | Names the human who decides proceed-without-item versus hold. Gate: the agent chases the response and surfaces the burning clock but never makes this decision. If empty → UNRESOLVED flag surfaced in the calibration digest (maintenance C9 precedent). |
| C5 suggested-upgrades rule | S, G | Judgment prose → G, not forced into K. Upgrades are an owner option with their own line-item price, never dispatched on agent initiative. |
| C6 standing no-approval items | S, G, **C!** | Never skipped, never asked, never charged against the approval ladder. **Present-and-empty ≠ absent** — an empty list is still written (maintenance C8 precedent). |
| C7 chargeback PM-review thresholds (per-line + per-unit) | S, G, **C!** | **PLACEHOLDER-COLLISION TRAP — the sharpest trap in this seat.** C7 is a deposit-DEDUCTION authority; C1 is a repair-SPEND authority. They are different gates and the question's own hint says to keep the two numbers labeled separately. C7 must NEVER populate `{{approval_threshold}}`, and it needs two numbers where the placeholder holds one. S + G only. A configurator that pattern-matches "threshold → `{{approval_threshold}}`" silently grants deposit-deduction authority at the repair-approval line, which for the golden fixture would move it from $150/$400 to $500. |

### Group D — Roles and People

| Q | Destination(s) | Mapping detail |
|---|---|---|
| D1 in-house techs vs vendor-only | S, I, **C!** | Gate: vendor-only collapses the dispatch decision matrix to its vendor column. The ROSTER itself is a FACT owned by maintenance C3 (SEAM-10); D1 records only the yes/no shape and derives from the owner's roster when that seat exists. |
| D2 who conducts pre-move-out / move-out / final inspections | S, I | **Turnover-OWNED FACT** (SEAM-2 companion). Per-inspection-type person or role, structured — the three windows are tight and the assignments differ. Leasing B9 asks who conducts the pre-move-out walkthrough and points here. |
| D3 PM of record for scope escalation + damage notice gates | **P `{{property_manager_name}}`** (2 sites), S, I | POLICY, per-seat owned (SEAM-11). The turnover PM of record may legitimately differ from maintenance C1's maintenance supervisor and from leasing D7's approval seat — collapsing them would overwrite a real org distinction. Additional approvers → seat-config + IDENTITY routing prose. Contradiction cross-check when the names differ. |
| D4 photographer of record + turnaround SLA | S, I | Turnover-OWNED. Leasing is a downstream consumer (the listing cannot launch without photos); reverse-pointer note only, no leasing question asks it. |
| D5 leasing handoff recipient at rent-ready | S, I | **SEAM-13, the move-in handoff seam.** Turnover owns the RECIPIENT (it is the sending seat's routing config); the leasing seat owns its own intake. See the parallel-work note in the seam register. |
| D6 deposit disposition executor | S, I | Turnover-OWNED person + handoff location. Interlocks with A1: this seat delivers the evidence package and never makes the deduction decision. Adjacent to but distinct from maintenance C7's invoice-payment executor (SEAM-18) — different money paths. |
| D7 backup decision-maker | S, I | POLICY, per-seat owned (SEAM-12). If empty → UNRESOLVED flag in the calibration digest, per the question's own hint that a deadline with no available decision-maker is a company-structure problem. |

### Group E — Platform and Wiring

| Q | Destination(s) | Mapping detail |
|---|---|---|
| E1 turnover board of record | S, K, G, B | Turnover-OWNED. The question's own single-source rule ("a board of record that lives in two places is not a board of record") is quoted into GUARDRAILS — it is a rule, not just a value. |
| E2 inspection capture app | S, I | Turnover-OWNED. No maintenance or leasing question asks it. |
| E3 work-order system for turnover work | S, I | Which systems exist is a FACT owned by maintenance D1 (SEAM-15); E3 records which of them carries make-ready line items, which is this seat's own routing. If the answer names the board itself, that is recorded, not corrected. |
| E4 vendor roster + per-trade list | S, I | **SPLIT (SEAM-14).** The roster is a FACT owned by maintenance C5 — richer question (license, insurance, warranty, hands-off flags). Make-ready trades named here (paint, flooring, turn cleaning, landscaping) are APPENDED to the owner's roster, never forked into a second roster. Turnover-OWNED annotation: the tough-property-class vendor subset. If no roster exists → PHASE-ZERO flag before the agent schedules anything. |
| E5 owner channel + sender identity | S, G | **SPLIT (SEAM-16).** Channel = FACT, owner maintenance D5. Sender identity = POLICY, turnover-owned — turnover owner emails may legitimately go out under a different name than maintenance approvals. |
| E6 photo/document storage + naming convention | S, G | Turnover-OWNED. The convention goes to GUARDRAILS as an every-turn rule, because its purpose is findability at dispute time, which is a rule about behavior, not a value. |
| E7 messaging bot/channel + administrator | S | **DEPLOY-TIME INPUT, not a file-mapping value.** The bot token and chat ID land in `.env` at deploy, outside the applier's file set; the administrator name is a real seat-config value. No new taxonomy code invented — S plus this note. This worker does not run add-agent (contract). |
| E8 escalation channels + hours, per person | S, K | POLICY, per-seat owned (SEAM-17). Per-person channel + hours matrix structured; escalation prompts in config.json reference it. The "hours" component seeds — never sets — the cover-sheet day-mode window. |

---

## Cross-seat seam register (referenced by QUESTION ID only)

The leasing mapping pass runs in parallel with this one, so every leasing reference below is
to a QUESTION ID in the frozen kit doc
(`private source-questionnaire archive`, 39 Q verified
today), never to that worker's table or its line numbers.

| # | Value | Seats (by Q ID) | Class | Resolution |
|---|---|---|---|---|
| SEAM-1 | Security deposit disposition deadline | turnover **A1** ↔ maintenance **A3** ↔ leasing **B1** | FACT | **Owner = maintenance A3.** Three-way; this is the A3 cross-seat mark the maintenance table raised without assigning an owner, now resolved. Turnover and leasing hold pointer records. **Migration trigger named:** the questionnaire's own A1 hint says the statutory deadline is owned by the bookkeeping process; when the bookkeeper seat (Class B, no template yet) ships and asks it, ownership migrates there in one edit and maintenance drops to a pointer. Ownership order until then: maintenance → turnover → leasing. Leasing B1 additionally asks what date STARTS the clock — that sub-value has no maintenance or turnover counterpart and is leasing-owned. |
| SEAM-2 | Pre-move-out inspection: legal status + who conducts | turnover **A2** + **D2** ↔ leasing **B9** | FACT | **Owner = turnover** for both halves. A2 owns whether it is legally required or regulated; D2 owns the inspector per inspection type. Leasing B9 asks whether the company conducts one and who — it holds a pointer, not a second assignment. Two seats naming different inspectors for the same walkthrough is the failure this resolves. |
| SEAM-3 | Damage-charge dispute window | turnover **A3** ↔ maintenance **A5** | FACT | Owner = maintenance A5. |
| SEAM-4 | Certified-mail requirement | turnover **A4** ↔ maintenance **A4** | FACT | Owner = maintenance A4. Each seat arms its own delivery gate from the owner's value. |
| SEAM-5 | Lease sections for damage / wear / cost recovery / collections | turnover **A5** ↔ maintenance **A6** | FACT | Owner = maintenance A6. |
| SEAM-6 | Unit → property-class map | turnover **B1** ↔ maintenance **A1** ↔ leasing **A1-A4** | FACT | **Owner = turnover B1** — the only seat asking per-unit grain. The others hold class LABELS and consume the map. |
| SEAM-7 | Door count of record | turnover **B6** ↔ maintenance **A1** | FACT | **Owner = turnover B6** — the only seat designating a denominator "of record". Maintenance A1's portfolio size is descriptive prose and must not become a second denominator. |
| SEAM-8 | Owner spend pre-approval threshold | turnover **C1** ↔ maintenance **B1** | **POLICY** | **Per-seat owned. Do NOT collapse.** C1 gates make-ready reserve; B1 gates occupied-unit repair spend. Same owners may carry different numbers for each. Contradiction cross-check surfaces the pair for eyeball; it never unifies them. The golden fixture exercises this deliberately. |
| SEAM-9 | Lawn care / HVAC filter lease assignment | turnover **A6** → maintenance (consumer) | FACT | **Owner = turnover A6.** No maintenance question asks it, yet maintenance needs it for occupied-unit wear calls. Reverse pointer: maintenance reads turnover's value. |
| SEAM-10 | In-house tech roster (skills, areas, platform IDs) | turnover **D1** ↔ maintenance **C3** | FACT | Owner = maintenance C3 (richest grain). Turnover D1 records the yes/no shape and derives from the roster. Order if maintenance absent: turnover holds, `held_pending_seat: maintenance`. |
| SEAM-11 | Property manager of record | turnover **D3** ↔ maintenance **C1** ↔ leasing **D7** | **POLICY** | Per-seat owned. Three seats can legitimately answer to three different people; leasing D7 explicitly adds an owner-approval seat above its PM. Cross-check on difference, never auto-unify. |
| SEAM-12 | Backup decision-maker | turnover **D7** ↔ maintenance **C9** | **POLICY** | Per-seat owned. Cross-check on difference. Empty on either side → UNRESOLVED flag in that seat's calibration digest. |
| SEAM-13 | Rent-ready → leasing handoff recipient | turnover **D5** ↔ leasing intake (**D7** seat, **D9** calendar) | FACT | **Owner = turnover D5** — it is the sending seat's routing config. **Parallel-work note:** the golden fixture names this person (Wren Calloway, Leasing Coordinator). If the leasing pass's fixture names a different person for the same handoff, that is a fixture-merge conflict for the mapping QA reviewer QA seat to resolve, NOT a defect in either table. Flagged here so the QA pass looks for it. |
| SEAM-14 | Approved vendor roster | turnover **E4** ↔ maintenance **C5** | FACT | Owner = maintenance C5. Turnover's make-ready trades APPEND to the owner's roster. Turnover-owned annotation: the tough-class vendor subset. **This requires cross-seat append, which the engine does not have — see the Lane 1 requirements below.** |
| SEAM-15 | Platform of record | turnover **E3** ↔ maintenance **D1** ↔ leasing **D1** | FACT | Owner = maintenance D1 for the platform inventory. Each seat records which platform carries ITS work — that routing is the seat's own. |
| SEAM-16 | Owner channel / sender identity | turnover **E5** ↔ maintenance **D5** | **SPLIT** | Channel = FACT, owner maintenance D5. Sender identity = POLICY, per-seat owned. |
| SEAM-17 | Escalation channels + hours | turnover **E8** ↔ maintenance **D6** ↔ leasing **D10** | **POLICY** | Per-seat owned. Different seats wake different people at different hours by design. |
| SEAM-18 | Money-side executor | turnover **D6** (deposit disposition) ↔ maintenance **C7** (invoice payment) | **POLICY** | Adjacent, not shared — two different money paths. Per-seat owned; cross-check only to catch a member who meant one person and named two. |
| SEAM-19 | Clock context: timezone + day-mode window | turnover **cover sheet** ↔ maintenance **B8** + cover sheet | FACT | Timezone is install-level: ONE value per install, carried on every seat's cover sheet, and the install is the owner. Day-mode window: owner = maintenance B8, which is a real question; turnover has none, so its cover-sheet field is a pointer-seeded value the member confirms. See FINDING E2 — the timezone must reach `config.json`, not just prose. |

**Seam tally: 19 — 13 FACT (single owner + pointer), 5 POLICY (per-seat owned + cross-check), 1 SPLIT.**
Both three-way seams the contract names explicitly are resolved: SEAM-1 (maintenance A3 deposit
deadline) and SEAM-2 (move-out inspection ownership).

---

## Coverage proof

- **Source side: 34/34 questions mapped, zero UNMAPPED.** Group counts verified against the
  frozen kit doc: A=6, B=6, C=7, D=7, E=8.
- **Destination side: 18/18 slots sourced, zero bare NO-SOURCE flags.** 13 placeholder types
  (45 sites) + 5 config.json literal-default keys. Placeholder sites split 11 add-agent /
  11 questionnaire / 23 cover-sheet = 45.
- **RUNTIME-PRESERVED: 0 in this seat**, swept for explicitly and recorded as a proven
  negative (the same sweep finds the known `{{CTX_ROOT}}` instance in the maintenance
  template). Nothing was reclassified and no count moved; the class is carried here so a
  future template edit that introduces one is caught rather than mistaken for NO-SOURCE.
- **Questionnaire-sourced placeholders: 3** — `{{approval_threshold}}`←C1,
  `{{turn_target_days}}`←B2, `{{property_manager_name}}`←D3.
- **Cover-sheet fields: 9** — 4 carried from the maintenance precedent for cross-seat format
  parity (2 of them unused by this template, said so plainly) + 5 stage-clock fields this
  questionnaire never asks. Every NO-SOURCE flag carries its reason; three adjacency traps are
  refused explicitly rather than silently mapped.
- **Conditional gates (C!): 8** — A2 pre-move-out armed-by (statute vs policy), A4
  certified-mail delivery, C2 human-executes-the-call rung, C3 safety fix-first cap, C4
  silent-owner decision authority, C6 standing no-approval items (present-and-empty), C7
  deposit-deduction authority, D1 vendor-only matrix collapse. The configurator writes the
  flag; the gate text ships in GUARDRAILS either way.
- **Never-graduate gates: 4**, structural rather than answer-driven, taken from the
  questionnaire's own What Happens Next: make-ready scope and budget approval, security
  deposit deduction decisions, vendor pricing commitments, tenant damage charge notices. These
  are written to GUARDRAILS regardless of any answer and no autonomy setting graduates them.
- **Weakest mappings, flagged honestly rather than buried:** B2 (per-class map reduced to a
  scalar placeholder — needs the precedence sentence or it mis-gates non-modal classes), B3
  and B4 (S-only, no placeholder exists), B5 (S-only, consumer is scorecard logic that is
  prose today).
- **Board (B) destinations** listed for completeness. Board wiring remains out of scope for
  this pass, same as the maintenance table.

---

## Golden fixture + validation record

**File:** `outputs/ridgeline-turnover-answers-2026-08-25.md`

Company: **Ridgeline Residential Management** — the same fictional company as sealed scenario 1
(`editions/maintenance/ridgeline-maintenance-answers.md`), reused so cross-seat fixtures
cohere. Carried forward and verified consistent: 186 doors, Pine Basin and Cedar Mesa markets,
Class B and C, America/Denver, 30-day deposit deadline, 10-business-day dispute window,
certified-mail confirmed, lease sections 12.2/12.4/18.1/21.3, Morgan Vale, Ellis Shore,
Tessa Reed, Omar Flint, Avery Moss, Juniper Holdings, Northstar Homes, WorkTrail.

Built programmatically from the frozen kit doc — only the `Answer:` lines were written and the
cover-sheet block inserted — so question text is byte-identical by construction, not by care.

The fixture deliberately exercises three things a clean-looking fill would hide:
1. **SEAM-8** — Juniper Holdings and Northstar Homes carry different reserve numbers here
   ($750/$350) than their maintenance repair numbers ($700/$300). Correct, not a contradiction;
   the fixture says so inline so no reviewer "fixes" it.
2. **SEAM-11** — turnover's PM of record is Ellis Shore while maintenance's is Morgan Vale,
   with the roles swapping for the backup slot. Coherent, and it proves the seats are not
   blind copies of each other.
3. **C7's trap** — chargeback numbers ($150 per line, $400 per unit) sit below the C1 reserve
   ($500), so a configurator that wrongly routes C7 into `{{approval_threshold}}` produces a
   visibly wrong number rather than a silently equal one.

### Validation run (all read-only; the fixture is the only file written)

| # | Check | Result |
|---|---|---|
| V1 | Byte-drift: fixture minus answer lines minus cover-sheet block, diffed against the frozen kit doc | **PASS**, `diff` exit 0 — non-answer text byte-identical |
| V2 | All 9 cover-sheet fields present and filled (no residual underscores) | **PASS** 9/9 |
| V3 | 34 question IDs, 34 `Answer:` lines, none blank or unfilled | **PASS** 34/34 |
| V4 | Each question followed by exactly one answer before the next question | **PASS** 34/34 |
| V5 | Group counts A=6 B=6 C=7 D=7 E=8 | **PASS**, matches the kit doc |
| V6 | Multi-line continuation-indent path exercised | **NOT EXERCISED** — see gap below |

**Mutation proof that the checks have teeth** (planted against scratch copies; the deliverable
was never mutated). Each mutation was killed, and the real fixture still passes as a control:

| Mutation | Expected killer | Result |
|---|---|---|
| Blank C7's answer back to underscores | V3 | died, exit 1, named ordinal 18 |
| Delete a cover-sheet field (`Scope SLA hours`) | V2 | died, exit 1 |
| Delete the whole E8 question+answer pair | V3 + V5 | died, exit 1, counts 33/33 and E=7 |
| Drift one word of C7's question text | V1 | died, `diff` exit 1 |
| *(control)* unmutated deliverable | none | passes, exit 0 |

### Validation gaps — stated, not papered over

1. **The contract's "parses clean through the scenario-1 parser" could not be executed: the
   parser does not exist on disk yet.** Searched the whole repo for the reconfigurator and its
   parser section (managed-block reader, cover-sheet reader, any PMAgents-named script) — nothing.
   The scenario-1 contract-2 script is Lane 1's build. What was done instead: the fixture was
   validated against the sealed FORMAT contract (`editions/maintenance/answers-format.md`) with
   the six mechanical checks above, which are the checks a parser must perform. **This is a
   format-conformance proof, not a parse proof.** The parse proof is owed the moment Lane 1's
   parser lands, and it is a real remaining gate, not a formality.
2. **The continuation-line path is unexercised.** All 34 answers are single-line, matching the
   proven scenario-1 fixture shape. So neither fixture in the corpus tests the two-space
   continuation-indent rule that `answers-format.md` specifies. Lane 1 should add a
   multi-line variant to its parser tests; this fixture deliberately does not diverge from the
   shape scenario 1 proved.

---

## Requirements this pass surfaces for Lane 1 (do not assume these exist)

The sealed scenario-1 core was proven against one seat and one template. Four capabilities
this mapping table assumes are not in it, and each fails silently rather than loudly:

1. **Applier file set must include `.claude/skills/`** (FINDING E1). Otherwise 6 mapping-owned
   sites in `make-ready-pipeline/SKILL.md` stay unsubstituted in the skill that runs the pipeline.
2. **Literal-default config.json keys must be overwritten by value**, not only by `{{}}`
   substitution (5 keys). A placeholder-only applier leaves `turn_target_days: 10` next to an
   IDENTITY.md that says 12 — a split-brain config with no visible marker.
3. **Timezone must reach `config.json`** (FINDING E2). `agent-manager.ts:2196` bare-ORs an
   empty timezone to `America/New_York`; the fixture's company is `America/Denver`.
4. **Cross-seat pointer resolution and owner-append** (SEAM-14 especially). Today seat-config
   is per-seat and single-seat. This table's FACT/pointer doctrine needs the applier to (a)
   write a pointer record instead of a value, (b) resolve it at read time, and (c) append into
   the owner seat's roster rather than forking a second one. **This machinery does not exist in
   the scenario-1 core.** Until it does, a turnover-only install must hold FACT values locally
   with `held_pending_seat` set, and the QA seat must catch the migration at install time.

---

## seat-config.json shape — delta from the maintenance proposal

Same top-level shape (`{seat, company, answers: {A1..E8 raw text}, derived: {...}, provenance}`),
raw answers always preserved verbatim beside derived values so re-mapping never needs re-asking.

Turnover adds, under `derived`:

- `class_map{}` — unit → class, the SEAM-6 owned FACT, plus `phase_zero` when absent.
- `benchmarks{turn_time{}, budget_bands{}, punch_list{}}` — per-class maps, all three of them
  scalar-less by nature.
- `turn_target_days{value, placeholder_source_class}` — the B2 reduction made explicit rather
  than implicit, so a reviewer can see which class the scalar came from.
- `chargeback_gates{per_line, per_unit}` — deliberately NOT under `thresholds{}`, so no
  configurator can confuse C7 with C1 by key adjacency.
- `cross_seat{}` — pointer records `{value_name: {owner_seat, owner_question_id}}` for the 13
  FACT seams, and `held_pending_seat` where this seat is holding an absent owner's value.
- `cross_seat_checks[]` — the 5 POLICY pairs plus the 1 SPLIT, listed for the contradiction
  report to eyeball, never to auto-unify.
- `never_graduate[]` — the 4 structural gates, written regardless of answers.

---

## Contract compliance

Deliverables: this table + `outputs/ridgeline-turnover-answers-2026-08-25.md`. Two files
written, nothing else. `templates/` read-only (grep census only), `add-agent` not run, the kit
docs not edited — the cover sheet is an answers-FILE addition, exactly the maintenance
precedent. Every cross-seat reference is by question ID against frozen kit docs; the leasing
worker's in-flight table was neither read nor cited.
