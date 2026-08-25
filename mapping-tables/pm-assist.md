# Betty glue: PM questionnaire → PM-assist seat MAPPING TABLE (draft for collie QA, then dane eyeball)

Worker: m-pm-assist. Contract: `outputs/mapping-contracts-accounting-pmassist-2026-08-25.md`,
section **M-PM-ASSIST** + the inherited L2 shared rules block
(`outputs/glue-lane2-contracts-2026-08-24.md`). Status: **DRAFT** — collie QA seat, then dane
eyeball, then the table feeds the engine. **Mapping schema: v2** (the E2 extension's K-row +
`cross_seat{}` machinery is the consuming surface; rows are cited for it in §10).

**Sources read TODAY, and what each was used for**

| Source | Used for |
|---|---|
| `agents/dane/outputs/ascend-doc-kit/pm-questionnaire/pm-questionnaire.md` (41 Q, groups A–D) | The source side. **FROZEN — opened read-only, zero bytes written.** |
| `outputs/templates-drafts/pm-assist-seat/` (67 files, 19 root, 40 SKILL.md) | The destination side. Census re-derived **fresh by grep**, then diffed against the assembly report's census (§2). |
| `outputs/sa-pm-assist-assembly-report.md` | Pre-seeded work list: §4 NO-SOURCE defaults, §5 mapping-forward table, §8 seam list. Verified before consumption, not trusted as counts. |
| `outputs/betty-maintenance-mapping-table-2026-08-23.md` | Pattern authority: structure, destination taxonomy, cover-sheet precedent. |
| `outputs/betty-leasing-mapping-table-2026-08-25.md` (incl. the **X1 QA amendment**) + `outputs/betty-turnover-mapping-table-2026-08-25.md` | Seam register reconciliation by question id (§7). |
| `outputs/betty-c1-accepted/ridgeline-maintenance-answers.md`, `outputs/ridgeline-leasing-answers-2026-08-25.md`, `outputs/ridgeline-turnover-answers-2026-08-25.md` | Established Ridgeline entities for fixture coherence, and the **four-way SEAM-11 verification** (§7.1) — the actual names, read, not remembered. |
| `outputs/glue-engine-extension-contract-2026-08-25.md` (schema v2 / E2) | The consuming surface. Rows cite its four capabilities. |

**Rule (two-direction, from the maintenance pattern, non-negotiable):** every question gets a
destination or an explicit UNMAPPED-AND-WHY; every template placeholder gets a source or an
explicit NO-SOURCE flag. Both directions proven below. The census is the deliverable.

**Read-only bindings honoured:** kit docs frozen; draft tree read-only — **every defect found in
the draft is FLAGGED in §9, never corrected**. No build, no configurator run, no `add-agent`,
no writes outside the two deliverable paths.

---

## 1. Destination taxonomy

Reused verbatim from the maintenance table. No new codes invented.

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct `{{...}}` substitution at configure time |
| K | config key by path | `config.json` / `seat-config.json` key set to the derived value (E2 capability 2 makes this mechanical) |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board tab | The PM Operating Board workbook tab (this seat's D2 board) — SECONDARY, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behaviour (not just a value) |

---

## 2. Placeholder census — FRESH, and diffed against the assembly report

Derived today by `grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}'` over the whole draft tree.

**Fresh totals: 32 types / 232 sites.**
**Assembly report §3 claim: 32 types / 232 sites. → MATCH on both totals. Two instruments agree.**

One mismatch found inside the report, at sub-total grain — see **F-PM-6** in §9: the report's
§3 sub-heading reads *"Question-sourced (20 types, 165 sites)"* while its own table under that
heading lists **23 rows summing to 190 sites**. The table body is correct and matches this fresh
census; the sub-heading is a stale count. The tree is not affected.

### 2.1 New measurement this pass adds — operating sites vs interview-instruction sites

Not in the assembly report. 32 of the 232 sites live in `ONBOARDING.md`, and **all 32 are
instruction-form** (a `→ {{x}}` directive, a mapping-table cell, or the Step-10 verify list) —
the interview naming the placeholder it fills, not a value the running agent reads. Verified by
inspecting all 32.

| Class | Sites |
|---|---|
| **Operating sites** (bootstrap prose + skills + JSON the agent reads at runtime) | **200** |
| Interview-instruction sites (`ONBOARDING.md`) | 32 |
| Total | 232 |

### 2.2 Site distribution by surface — load-bearing for the engine

| Surface | Sites |
|---|---|
| Root files (`*.md`, `*.json`) | 131 |
| `.claude/skills/**/SKILL.md` (28 of 40 skills) | **101** |

**43.5% of this seat's placeholder sites are inside skills files.** A root-files-only applier
substitutes 131 of 232. This is E2 capability 1 (P-rows targeting skills files) stated as a
number rather than a principle. `{{followthrough_sweep_day}}` is the sharpest case: **both** of
its sites are in `monday-board/SKILL.md` and **zero** are in any root file — a root-only applier
never substitutes it at all, and the seat ships with a raw `{{followthrough_sweep_day}}` in a
live skill. Recommended as the **named test** for capability 1.

### 2.3 The 32 types, with sites and source

**Question-sourced (23 types, 190 sites)**

| Placeholder (sites) | Source | Note |
|---|---|---|
| `{{property_manager_name}}` (59) | **A2** | 7 root files + 16 skills. The seat's most-substituted value by 2.5× |
| `{{broker_name}}` (23) | **A3** | |
| `{{broker_channel}}` (12) | **A3** | |
| `{{owner_reserve_minimum}}` (11) | **B5** | |
| `{{owner_report_day}}` (8) | **D6** | also drives two crons created at configure time (K6) |
| `{{owner_escalate_hours}}` (8) | **B4** | third rung |
| `{{decision_log_location}}` (8) | **D7** | |
| `{{trust_variance_broker_threshold}}` (6) | **B14** | |
| `{{promise_overdue_hours}}` (6) | **C8** | |
| `{{owner_approval_threshold}}` (6) | **B1** | |
| `{{pm_platform}}` (5) | **D1** | |
| `{{owner_followup_2_hours}}` (5) | **B4** | second rung |
| `{{backup_decision_maker}}` (5) | **C5** | |
| `{{renewal_lookahead_days}}` (4) | **B9** | |
| `{{owner_followup_1_hours}}` (4) | **B4** | first rung |
| `{{owner_decision_days}}` (3) | **B9** | |
| `{{operating_board_location}}` (3) | **D2** | |
| `{{delinquency_alert_day}}` (3) | **B6** | |
| `{{coordinator_spend_authority}}` (3) | **B2** | |
| `{{broker_emergency_threshold}}` (3) | **B3** | |
| `{{pm_emergency_authority}}` (2) | **B3** | |
| `{{followthrough_sweep_day}}` (2) | **C8** | **skills-only, zero root sites** — see §2.2 |
| `{{deposit_disposition_days}}` (1) | **A7** | **its only site is the ONBOARDING instruction line naming it — zero operating consumers. See F-PM-1** |

Three rungs of the B4 ladder are three separate types on purpose (a four-rung ladder in one
scalar is a bad shape) — the turnover precedent for "no placeholder exists for a map".

**Cover sheet — the shared 4-field header (4 types, 21 sites)**

Kept whole and verbatim, per the maintenance precedent and the leasing pass's reconciliation, so
cross-seat fixtures cohere. No fifth field minted.

| Placeholder (sites) | Field |
|---|---|
| `{{timezone}}` (11) | Timezone — **plus the mandatory K1 config-key row, see §10** |
| `{{company_name}}` (5) | Company name |
| `{{org_name}}` (4) | Org short-name |
| `{{forward_email}}` (1) | Forward email — ONBOARDING-only site, see F-PM-2 |

**Org-seeded pointer, NOT a cover-sheet field (2 types, 12 sites)**

| Placeholder (sites) | Source |
|---|---|
| `{{day_mode_start}}` (6), `{{day_mode_end}}` (6) | `templates/org/context.json` seed + **cross-seat pointer to maintenance B8** (SEAM-19 / leasing X2 precedent) |

**No PM question asks the external-comms window.** Rejected alternatives recorded by the
assembly pass and re-affirmed here: mapping **D6** (report day) or **C7** (broker check-in
cadence) → day mode. Both are narrower scheduled windows; either would have silently muted the
seat outside them. Verified against C7's actual text before re-affirming.

**Add-agent framework values (3 types, 9 sites), uncited by design**

`{{agent_name}}` (6), `{{org}}` (2), `{{current_timestamp}}` (1). Filled by `add-agent`.

### 2.4 FINDING → COVER SHEET

The 4-field header is the maintenance table's, unchanged. **This questionnaire asks company
identity nowhere** — it opens with portfolio (A1) and never asks the company's name, short name,
forward email, or timezone. So all four fields are genuine gaps and all four stay
answers-FILE additions. **Kit docs stay frozen; zero questionnaire edits proposed.**

---

## 3. Per-question mapping — Group A: Company, Portfolio, and State Rules (10/10)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 portfolio size / markets / classes | S (`_descriptive`), I | Portfolio profile prose into IDENTITY; weights every Group-B KPI target. **Pointer, not a second number:** the door count of record is turnover **B6** and the unit→class map is turnover **B1** (SEAM-6, SEAM-7). This seat stores the profile and resolves grain through those pointers |
| A2 who holds the PM seat + which coordinator lanes exist | **P `{{property_manager_name}}`** (59), S (`people.property_manager`, `coordinator_lanes{}`), I | The seat's anchor value. Per-lane record is `{exists, covered_by}` — **a lane with no coordinator still gets a named human**, because "an alert with no owner does not exist" (D4). **SEAM-11, now four-way — verified in §7.1** |
| A3 principal broker + broker-only escalation channel | **P `{{broker_name}}`** (23), **P `{{broker_channel}}`** (12), S, I, G | The broker-only routing destination for the 12 never-graduates decision classes. G carries the same-day requirement as a rule, not a value |
| A4 eviction attorney + property/general counsel | S (`people.eviction_attorney`, `people.counsel`), G | No placeholder minted (two names, consumed by skill prose). G rule: any legal demand letter or attorney contact goes to broker **and** counsel the same day it arrives |
| A5 late-rent + eviction notice rules | S (`state_rules.late_notice_day/type/cure_period_days/pre_filing_requirements`), G, **C!** | **GATE: unconfirmed state law → the delinquency lane is not live.** `state_rules._status` ships as `not_live_until_confirmed_with_counsel`; a hint default may never stand in for a legal answer. The gate is per-jurisdiction, not per-seat |
| A6 non-renewal notice + entry notice | S (`state_rules.nonrenewal_notice_days`, `entry_notice_hours`), G, **C!** | Same not-live gate. **Entry notice is a FACT pointer** — the per-jurisdiction entry-notice map is owned by maintenance **A2** (SEAM-33, new this pass). Non-renewal notice has no counterpart in any shipped seat and is **PM-assist-owned** |
| A7 deposit holding rule + disposition deadline | **P `{{deposit_disposition_days}}`** (1, see F-PM-1), S (`state_rules.deposit_holding_rule`, `deposit_disposition_days`), G | **SPLIT.** The *holding rule* (separate account, resident notified) is PM-assist-owned. The *deadline value* is a FACT pointer, owner = maintenance **A3** (SEAM-1). **This pass does NOT rule on the SEAM-1 migration** — the contract assigns that decision to M-ACCOUNTING; this row records the pointer and names the accounting pass as the deciding seat |
| A8 habitability standards + response timeframes | S (`state_rules.habitability_standards`, `habitability_response_hours`), G, **C!** | **GATE, and it is an anti-authority gate:** the PM's emergency repair authority is recorded here and the seat is told, in GUARDRAILS, that it is the PM's and never the seat's. Recording an authority is not acquiring it |
| A9 inspection cadence + tenant file retention | S (`state_rules.inspection_cadence`, `tenant_file_retention_years`), G | Cadence feeds the compliance calendar. **Pointer:** whether a pre-move-out inspection is legally required (turnover **A2**) and who conducts each type (turnover **D2**) are turnover-owned — SEAM-2. This seat carries cadence only |
| A10 state filings / registrations / inspection deadlines | S (`state_rules.required_filings[]`), G, **C!** | **GATE is per-filing, not per-answer.** A partially-confirmed answer arms the confirmed jurisdictions and leaves the rest NOT LIVE, said out loud on the compliance tab rather than left blank. The fixture exercises exactly this (Pine Basin confirmed, Cedar Mesa not) |

---

## 4. Per-question mapping — Group B: Thresholds, KPI Targets, and Clocks (14/14)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 owner pre-approval threshold + per-owner overrides | **P `{{owner_approval_threshold}}`** (6), S (`thresholds.owner_approval_threshold`, `owner_threshold_overrides{}`), B | Base number → placeholder; overrides → seat-config map (no placeholder exists for a map). **SEAM-8, POLICY, per-seat owned — do NOT collapse** with maintenance B1 or turnover C1 |
| B2 coordinator spend authority | **P `{{coordinator_spend_authority}}`** (3), S | **THE THREE-MONEY-GATE TRAP, gate 2 of 3.** This is the coordinator→PM escalation line. It is not B1's owner line and not B14's variance line. **Exercised deliberately in the golden fixture** (§8.2), turnover-C7 precedent |
| B3 PM emergency authority + broker loop-in cost | **P `{{pm_emergency_authority}}`** (2), **P `{{broker_emergency_threshold}}`** (3), S, G | Two distinct values, two placeholders. G carries the "documents every contact attempt, never waits more than 2–4 h" behaviour, which is a rule not a number |
| B4 owner non-response ladder | **P `{{owner_followup_1_hours}}`** (4), **P `{{owner_followup_2_hours}}`** (5), **P `{{owner_escalate_hours}}`** (8), S (`clocks.owner_nonresponse_ladder_hours[3]`) | Three rungs, three placeholders, plus the ordered array in seat-config. GUARDRAILS: no rung passes unfired |
| B5 minimum owner reserve per unit | **P `{{owner_reserve_minimum}}`** (11), S (`thresholds.owner_reserve_minimum`) | The reserve *conversation* is never the seat's — value only. **New seam with bookkeeping B3** (reserve floor per property/owner) — SEAM-35, §7 |
| B6 delinquency clocks | **P `{{delinquency_alert_day}}`** (3), S (`clocks.delinquency_late_notice_day`, `delinquency_alert_day`, `delinquency_target_pct`), G | Late-notice day is the *operational* echo of the A5 *legal* clock and is stored separately on purpose — `delinquency-clock/SKILL.md` keeps the two clocks apart, and merging them is how a legal deadline gets computed from an operational habit |
| B7 days vacant + days to make-ready targets | S (`kpi_targets.days_vacant`, `days_to_make_ready`) | Both ship `null`, so no literal-overwrite hazard. **Pointer:** turnover's B-group owns the per-class make-ready grain; this seat holds the portfolio scalar. Days-vacant has **no counterpart in any shipped seat — PM-assist-owned** |
| B8 KPI benchmark overrides | S (`kpi_targets.*`) + **K3** | **LITERAL-OVERWRITE ROW (E2 capability 2).** `seat-config.kpi_targets` ships pre-filled with the standard set (95/90/60/90/25, NO-SOURCE default N8, sourced from B8's own hint). B8 asks only for *overrides*, so an applier that writes nothing when there are no overrides is correct, and one that writes only the answered keys must not blank the rest. Without a K-row the overrides land in prose and the literals stay — split-brain with no marker |
| B9 renewal clocks | **P `{{renewal_lookahead_days}}`** (4), **P `{{owner_decision_days}}`** (3), S + **K4** | Two scalars → placeholders. The tenant follow-up schedule is a **list**, so it is `clocks.renewal_tenant_followup_days`, shipping as the literal `[30, 60]` (N9) — **K4 overwrite row** for the same reason as B8. Seam with the leasing seat's own renewal offer lead / response window (§7, SEAM-34) |
| B10 leasing alert thresholds (five) | S (`clocks.leasing_*`, `application_decision_hours`) | Five values, no placeholder (a five-value matrix in a scalar is the shape B4 was split to avoid). **Pointer:** the application-decision SLA is leasing-owned; this seat watches it as an alert threshold, it does not set a second standard (SEAM-36) |
| B11 turnover escalation days + over-budget rule | S (`clocks.turnover_escalation_days`), G | Value + the two-tier over-budget rule into GUARDRAILS (PM approval; above the owner threshold → owner). **Pointer:** turnover owns escalation on its own board; this seat owns the escalation *landing* on the PM board (SEAM-37) |
| B12 maintenance SLA windows + invoice queue limit | S (`clocks.maintenance_sla{}`, `invoice_queue_alert_days`), G | **The questionnaire's own explicit cross-seat pointer**, quoted: *"If you run the maintenance agent, use the same values as its configuration."* Owner = maintenance **B5**. A difference is an `unresolved` flag, **never an average** — that rule goes to G because it is a behaviour. The 5-day invoice-queue limit has **no maintenance counterpart and is PM-assist-owned** |
| B13 multi-bid project cost | S (`thresholds.multi_bid_threshold`) | S-only; consumer is the approval-queue completeness check. Adjacent to bookkeeping **A15** (contractor-licensing flag amount) — different gates, recorded so a later pass does not collapse them |
| B14 trust variance rule | **P `{{trust_variance_broker_threshold}}`** (6), S (`thresholds.trust_variance_resolution_hours`), G | **THE THREE-MONEY-GATE TRAP, gate 3 of 3**, and the accounting seam. This seat owns *surfacing* + the broker threshold; the accounting seat owns *resolution*. **Whether the commission must be notified is the broker's call** — that sentence is quoted into G verbatim because it is a limit on both this seat and the bookkeeper |

---

## 5. Per-question mapping — Group C: Delegation and People (8/8)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 the 20-row Assistant Can Own table, now / later / never | S (`delegation.rows{}`), **C!** | **POSTURE-BOUND ROW.** Each row is stored as its **execution half only**. The gate this arms is *which drafts get built first*, never *who decides*. **A `now` on a row whose subject is a housing, money, legal, or relationship matter is INVALID INPUT → `flags.unresolved[]` + surfaced to the PM. It is never written as a delegation row.** No combination of `now` rows sums to authority. See §6 |
| C2 which drafted comms may send without PM review | S (`owner_comms.assistant_may_send_without_review[]`) — **and nothing else** | **THE SHARPEST POSTURE ROW.** This answer records **intent**, and **MUST NOT** write `status` in `copilot-thresholds.json`. Every class ships `locked`; unlocking is an explicit runtime PM action after shadow mode and a tracked record (`draft-release-gate`). **An applier that flips a category to `unlocked` at configure time is a defect in the applier, not a configuration option.** Additionally the answer is validated against the **closed 7-class vocabulary**; an out-of-vocabulary value is rejected to `flags.unresolved[]` and **never mints a new category**, because a category invented here is exactly the never-graduates entry the file's own `_note` calls a bug |
| C3 the owner-contact line | S (`owner_comms.assistant_may_send_to_owners[]`, `always_pm_review[]`), G | `always_pm_review` ships **present and non-empty** with the seat rule (judgment/framing, any concern, any difficult month). An answer may *add* to it; an answer may **not** empty it |
| C4 owner tags + where the tag lives | S (`owner_comms.owner_tags`) | **Closed vocabulary from N13** (silent investor / collaborative / high touch) — it comes from C4's hint, not from an answer, so the vocabulary is a literal and only the per-owner assignment and the tag location are answered |
| C5 backup decision-maker | **P `{{backup_decision_maker}}`** (5), S (`people.backup_decision_maker`), I | **SEAM-12, POLICY, per-seat owned.** Empty → `flags.phase_zero[]`, per the questionnaire's own hint that a deadline with no available decision-maker is a company-structure problem. Saying so is in the seat's job description (GUARDRAILS) |
| C6 who works the financial board | S (`people.financial_board_owner`), I | **The accounting seam, other half.** Pairs with bookkeeping **C3** (who executes the human bookkeeper role). Ownership proposal in §7.2 |
| C7 PM ↔ broker check-in cadence | S (`people.broker_checkin_cadence`) | S-only. **Explicitly NOT a day-mode source** — see §2.3's rejected alternative. The cadence is a meeting, not a comms window, and the answer's own escalation clause ("go up as they arise, not held for the meeting") goes to G |
| C8 how decisions reach the log + Follow-Through sweep | **P `{{promise_overdue_hours}}`** (6), **P `{{followthrough_sweep_day}}`** (2, skills-only), S + **K5 (+K2)** | Two placeholders. **The C8 answer has two config targets (K5 and K2):** `seat-config.clocks.followthrough_sweep_day` ships the literal `"Monday"` **and** `config.json crons[monday-board].interval` is the literal `0 8 * * 1`. Both must move when the answer is not Monday — today only the prose moves. **See F-PM-3** |

---

## 6. POSTURE BINDING discharge — decision-authority answers configure ROUTING, never autonomy

The contract binds: *"any mapping row that would let an answer graduate a never-graduates gate is
a defect in the row, not a configuration option."* Discharged by construction, and audited row by
row rather than asserted.

**Every question in this questionnaire that names a decider was checked against the never-graduates
set** (Housing / Housing–protected-class / Money / Legal / Relationship, per
`GUARDRAILS.md` HARD RULE and `SOUL.md` "Decision Authority Is Routing, Not Autonomy").

| Question | What it names | Where it lands | Why that is routing, not autonomy |
|---|---|---|---|
| A2 | The PM seat | `{{property_manager_name}}` + `people.property_manager` | Names the **destination** every gated matter routes to. Changing it changes where the item goes, never whether it goes |
| A3 | The broker + channel | `{{broker_name}}`, `{{broker_channel}}` | Same, for the 12 broker-only classes |
| A4 | Attorney + counsel | `people.*` | Destination for demand letters. The seat never answers one |
| A8 | PM emergency spend authority | `state_rules.habitability_response_hours` + G | Records **the PM's** authority. GUARDRAILS carries the matching red-flag row ("I'll authorize the emergency repair, that's what the PM would do" → *You never authorize*) |
| B1–B3, B13, B14 | Money thresholds | placeholders + `thresholds.*` | A threshold decides **who is asked**, never **whether to spend**. Money is a never-graduates class at every value |
| **C1** | Delegated rows | `delegation.rows{}` | **Execution half only.** A `now` on a judgment row is rejected as invalid input (§5) |
| **C2** | Send-without-review list | `owner_comms.*` **only** | **Never writes `copilot-thresholds.json` status.** Recorded intent ≠ unlock (§5) |
| C3 | Owner-contact line | `owner_comms.*` | `always_pm_review` may be extended, never emptied |
| C5 | Backup decision-maker | `{{backup_decision_maker}}` | A second **destination**, not a second authority |
| C6 | Financial board worker | `people.financial_board_owner` | Names who *works* the board. Money still moves on the money side; this seat surfaces and drafts |
| D4 | Alert ownership | `manual_alert_flags{}` | Names the human per alert. An alert with no owner → UNRESOLVED, never held by the agent |

**Zero rows in this table arm a never-graduates gate.** Two rows (C1, C2) could have, and both
carry an explicit rejection clause instead of a value path. The remaining risk is not in the
table but in the applier — stated as an engine requirement in §10.

---

## 7. Cross-seat seam register — reconciled by question id against three tables

Reconciled against `betty-maintenance-mapping-table-2026-08-23.md`,
`betty-turnover-mapping-table-2026-08-25.md` (SEAM-1…19) and
`betty-leasing-mapping-table-2026-08-25.md` (X1…X6, incl. the **X1 QA amendment**). Existing ids
are reused; only genuinely new pairs get a new id, continuing the turnover numbering.

| Seam | Value | This seat's Q ↔ other side | Type | Resolution |
|---|---|---|---|---|
| **SEAM-1** | Deposit disposition deadline | **A7** ↔ maintenance A3, turnover A1, leasing B1 | FACT | **Owner = maintenance A3**, per turnover's SEAM-1 and the leasing **X1 QA amendment** (which resolved the two passes' opposite rulings *for* maintenance). This seat holds a **pointer**. **This pass does not touch the migration ruling** — the contract assigns SEAM-1's migration-readiness decision to **M-ACCOUNTING**, whose questionnaire asks it at bookkeeping **A6**. Recorded, not decided |
| **SEAM-8** | Owner spend pre-approval threshold | **B1** ↔ maintenance B1, turnover C1 | **POLICY** | Per-seat owned, do NOT collapse. Three seats, three legitimate numbers. Cross-check on difference |
| **SEAM-11** | Property manager of record | **A2** ↔ maintenance C1, turnover D3, leasing D7 | **POLICY** | **Now FOUR-WAY. Verified against the actual fixtures — §7.1** |
| **SEAM-12** | Backup decision-maker | **C5** ↔ maintenance C9, turnover D7 | **POLICY** | Per-seat owned. Empty → PHASE-ZERO here |
| **SEAM-15** | Platform of record | **D1** ↔ maintenance D1, turnover E3, leasing D1 | FACT | Owner = maintenance D1 for the inventory. Each seat records which platform carries its own work |
| **SEAM-16** | Channels + sender identity | **D5** ↔ maintenance D5, turnover E5 | **SPLIT** | Channel = FACT (owner maintenance D5); sender identity = POLICY, per-seat |
| **SEAM-17** | Escalation channels + hours | **A3 / C7** ↔ maintenance D6, turnover E8, leasing D10 | **POLICY** | Per-seat owned. The broker channel is this seat's and is same-day **by requirement**, not by preference |
| **SEAM-19** | Timezone + day-mode window | **cover sheet** ↔ maintenance B8 | FACT | Timezone is install-level, one value per install. Day mode: owner = maintenance B8; this seat has no question and takes the org seed + pointer (leasing X2). **Timezone must reach `config.json`, not just prose — K1, §10** |
| **SEAM-33** *(new)* | Entry-notice period per jurisdiction | **A6** ↔ maintenance A2 | FACT | **Owner = maintenance A2** (richer grain: it asks the per-jurisdiction map explicitly). This seat holds a pointer so the compliance calendar and renewal pipeline read one map. The **non-renewal** notice half of A6 has no counterpart anywhere — **PM-assist-owned** |
| **SEAM-34** *(new)* | Renewal clocks | **B9** ↔ leasing renewal cover-sheet values, renewals-coordinator seat | **SPLIT** | The PM **pipeline look-ahead** and **owner decision window** are PM-assist-owned (no other seat asks them). The **offer lead** and **tenant response window** are leasing-owned execution clocks that sit *inside* this window. Not a duplicate; a nesting. Cross-check fires only if a leasing clock exceeds the PM window |
| **SEAM-35** *(new)* | Owner reserve floor | **B5** ↔ bookkeeping **B3** | FACT | Unowned pending accounting-seat promotion. Bookkeeping B3 asks reserve floor per property *or* per owner with contract overrides — richer grain. **Proposed owner = bookkeeping B3 at promotion; PM-assist holds today** (`held_pending_seat: accounting`). Flagged for the collie QA cross-check |
| **SEAM-36** *(new)* | Leasing alert thresholds | **B10** ↔ leasing B-group | FACT | Owner = leasing for the application-decision SLA and the listing clocks it executes. This seat watches them as alert thresholds. Cross-check on difference |
| **SEAM-37** *(new)* | Turnover escalation + over-budget | **B11** ↔ turnover C-group | FACT | Owner = turnover for the board mechanics; PM-assist owns the escalation landing. Cross-check on the escalation-days number |
| **B12 pointer** *(no new id)* | Maintenance SLA windows | **B12** ↔ maintenance B5 | FACT | The questionnaire itself names the pointer. Owner = maintenance B5. Difference → `unresolved`, never an average |
| **B14 / C6** | Trust variance + financial-board worker | **B14, C6** ↔ bookkeeping B5/B6, C3 | FACT/POLICY split | **§7.2** |

**Tally for this seat: 15 seams touched — 8 FACT, 4 POLICY, 2 SPLIT, 1 FACT/POLICY split.
5 new ids contributed (SEAM-33…24).** `SEAM-n` register total across the four tables: **24 (SEAM-1…24)**; the leasing pass's X1–X6 marks are a parallel numbering and are unchanged by this pass.

### 7.1 Four-way SEAM-11 verification — done against the fixtures, not from memory

The contract requires the four-way seam be *verified*, not merely noted. Read from the three
existing golden fixtures plus this pass's:

| Seat | Question | Name in the Ridgeline fixture |
|---|---|---|
| maintenance | C1 | **Morgan Vale**, Maintenance Supervisor |
| turnover | D3 | **Ellis Shore**, Portfolio Director |
| leasing | D7 | **Dana Wren**, Property Manager |
| **pm-assist** | **A2** | **Dana Wren**, Property Manager |

**Result: four seats, three distinct names, one match (leasing D7 = pm-assist A2).** This is the
correct outcome for a POLICY seam and it exercises the cross-check in both directions at once —
a configured install must surface the three-way *difference* as an eyeball item **and** must not
treat the leasing/pm-assist *match* as evidence that the other two should be unified. A four-way
POLICY check is 6 pairs, not 3; the register previously described a 3-pair surface. Named as an
engine requirement in §10.

Secondary check, same method: **SEAM-12** — maintenance C9 = Ellis Shore, turnover D7 = Morgan
Vale, pm-assist C5 = Ellis Shore. Two distinct names across three seats, one match. Consistent
with per-seat ownership; nothing to unify.

### 7.2 B14 / C6 — the accounting seam, resolved by question id

Both mapping passes run in parallel, so this resolves **by question id only** and expects the
collie QA cross-check. Proposal from this side:

| Half | Owner proposed | Question ids |
|---|---|---|
| Variance **resolution** — the window the bookkeeper gets, the amount that splits small from large, the age that fires an alert | **ACCOUNTING** | bookkeeping **B5** (variance size split), **B6** (variance amount + age → alert), **A13** (trust reconciliation requirements) |
| Variance **surfacing** on the PM board + the **broker notification threshold** | **PM-ASSIST** | pm-assist **B14** → `{{trust_variance_broker_threshold}}` + `thresholds.trust_variance_resolution_hours` (held as a pointer once accounting ships) |
| The **commission-notification call** | **NEITHER SEAT — the broker** | pm-assist B14 text + bookkeeping **C2** (licensee accountable for the trust account) |
| Who **executes** the bookkeeper role | **ACCOUNTING** | bookkeeping **C3** ↔ pm-assist **C6** (this seat holds `people.financial_board_owner` as the board-facing name; a difference between the two is a contradiction to surface) |

**Note for QA, stated because the leasing and turnover passes reached opposite conclusions on
SEAM-1 and needed resolution:** this side proposes accounting ownership of *resolution* and
PM-assist ownership of *surfacing*, with `trust_variance_resolution_hours` degrading from an
owned value to a pointer at accounting promotion. If the accounting pass claims the broker
threshold as well, that is the collision to resolve — this seat's claim rests on the threshold
being a **PM-board escalation rung**, which is the same argument SEAM-8 uses.

**Also flagged:** bookkeeping **C1** (PM of record for owner-money decisions) becomes a **fifth**
arm of SEAM-11 at accounting promotion. Today SEAM-11 is four-way and this table records it as
four-way; the fifth arm is named by id so the register does not have to rediscover it.

### 7.3 Fixture-merge risks, flagged not resolved (turnover SEAM-13 precedent)

- **C6 / bookkeeping C3:** this pass's fixture names **Avery Moss, Accounts Payable** (an entity
  already established in the maintenance fixture's C7). If the accounting pass's fixture names a
  different bookkeeper for Ridgeline, that is a **fixture-merge conflict for the QA seat, not a
  defect in either table.**
- **A3 / bookkeeping C2:** this pass mints **Sloane Karr, Principal Broker** — a new fictional
  person, because no prior fixture has a broker. If the accounting pass mints a different broker
  name for the same company, same call: merge conflict, not defect.
- **B5 / bookkeeping B3 (SEAM-35):** this pass sets $400 per unit. A different accounting number
  is the expected shape of the seam, not a contradiction — but the *owner* must be one seat.

---

## 8. Golden fixture + validation record

**File:** `outputs/ridgeline-pmassist-answers-2026-08-25.md`
**Company:** Ridgeline Residential Management (`ridgeline`, America/Denver) — the **same fictional
company** as the maintenance, leasing, and turnover fixtures, so cross-seat fixtures cohere.
Reused established entities where roles overlap: 186 doors (112 Class B / 74 Class C), Pine Basin
and Cedar Mesa markets, WorkTrail (PM platform) and LedgerPeak (accounting), Dana Wren, Ellis
Shore, Morgan Vale, Wren Calloway, Avery Moss, and the owners Juniper Holdings and Northstar
Homes. **Minted new for roles no prior fixture had:** Sloane Karr (principal broker), Tobin
Merritt of Merritt and Cole LLP (eviction attorney), Harlan Voss of Voss Legal Group (counsel),
Basin State Bank (deposit trust), RentBasin market report (CMA source).

**V9 rule honoured:** the leasing/turnover golden **unit** names are not reused, and neither are
the draft tree's own example units.

### 8.1 Gate states deliberately mixed (scenario-1 fixture-B precedent)

| Gate | State in the fixture | What it exercises |
|---|---|---|
| A5 late-rent / eviction rules | CONFIRMED-WITH-COUNSEL=true, both markets | Delinquency lane live |
| A6 notice periods | CONFIRMED=true, both markets | Renewal + compliance lanes live |
| A10 required filings | **Pine Basin confirmed; Cedar Mesa UNCONFIRMED** | **Per-jurisdiction not-live gate** — the compliance lane runs for one market and is explicitly dark for the other, said out loud rather than defaulted |
| C2 send-without-review | **None at go-live**, all 7 classes locked | The POSTURE row: an answer that records intent and unlocks nothing |
| C1 delegation | 9 now / 7 later / 1 never | The never row is `sending renewal offers even after terms are set` — a class the *template* permits and this company declines. Proves the answer can only narrow, never widen |
| C5 backup decision-maker | Named (Ellis Shore) | PHASE-ZERO path not exercised here — it is exercised in the maintenance fixture |

### 8.2 The three-money-gate trap, exercised deliberately

Per the contract's explicit instruction (turnover-C7 precedent). The fixture carries **two
number collisions on purpose**:

| Value | Number | Gate |
|---|---|---|
| B1 owner pre-approval, Northstar Homes override | **$300** | One owner's contract threshold, that owner's properties only |
| **B2 coordinator spend authority** | **$300** | Coordinator→PM escalation, **portfolio-wide** |
| B14 broker notification on trust variance | **$500** | Variance escalation to the broker |
| **turnover C1 base make-ready reserve** (other seat, same company) | **$500** | Owner pre-approved make-ready reserve |

A configurator that pattern-matches on "threshold" or on the value collapses `$300` into one gate
and grants coordinator-level spend authority across the whole portfolio at one owner's number.
The fixture's B2 answer states the trap in prose so the failure is legible when it happens.
Third distinct gate in the same family: B3's `$1,200` PM emergency authority and `$5,000` broker
loop-in — six distinct money numbers across five gates in one seat.

### 8.3 Validation record

| # | Check | Method | Result |
|---|---|---|---|
| V1 | 41/41 questions answered | Count of filled `Answer:` lines vs blank slots in the source | **PASS** — 41 blank slots consumed, 41 answers written |
| V2 | Kit docs stay FROZEN | `diff` blank questionnaire vs fixture | **PASS** — removed lines: exactly the 41 blank `Answer:` slots, nothing else. Added lines: only filled `Answer:` lines, their 2-space continuations, and the cover-sheet block. **Questionnaire body byte-verbatim** |
| V3 | Fresh census matches the tree | `grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}'` over all 67 files | **PASS** — 32 types / 232 sites |
| V4 | Census diffed against the second instrument | Compared to assembly report §3 | **PASS on totals** (32/232). One sub-heading mismatch found → **F-PM-6** |
| V5 | Fictional-only | Regex scan **restricted to answer text** over fleet agent names, operator first names, org strings, and real PM platforms (AppFolio / Buildium / Rent Manager / Propertyware / Yardi / PropertyMeld) | **PASS — zero hits across all 41 answer blocks.** Matches elsewhere in the file are frozen kit text preserved byte-verbatim by V2, not answers |
| V6 | V9 rule — no reuse of leasing/turnover golden unit names | Regex scan of answer text for those names and the draft tree's example units | **PASS — zero hits** |
| V7 | Two-direction proof | §11 count lines | **PASS** — 41/41 questions, 32/32 placeholders, zero bare flags |
| V8 | Read-only surfaces genuinely untouched | **Not by `git status` — the draft tree is gitignored** (`.gitignore:164` `orgs/ascendops/agents/collie/*`), so a clean status there proves nothing. Verified by **mtime** instead: `find outputs/templates-drafts/pm-assist-seat -type f -newermt '2026-08-25 02:04'` → **0 files**. Kit files last written 2026-08-21 14:31 | **PASS** |
| V9 | Fixture parses through the scenario-1 parser | — | **NOT RUN — and not claimed.** Same honest position the leasing pass took: the parser lives in contract-2's reconfigurator, which this worker does not run (contract: no build, no configurator run). The fixture is built to the identical format spec the maintenance, leasing, and turnover fixtures use, so it should pass unchanged, but **that is an expectation, not evidence.** Re-run V9 against the parser when the engine consumes this table |

---

## 9. FINDINGS in the draft tree — FLAGGED, NOT FIXED

The authority-defect rule binds: a defect found in the draft is flagged here, never silently
corrected. **Zero bytes of the draft tree were modified by this pass.**

| # | Finding | Where | Verified by | Severity |
|---|---|---|---|---|
| **F-PM-1** | **`{{deposit_disposition_days}}` has exactly one site, and it is the ONBOARDING instruction line that names the placeholder itself.** Zero operating consumers: no bootstrap file, no skill, no JSON reads it. A configurator that substitutes it changes nothing observable, and a configurator that *fails* to substitute it is invisible. The value's real machine home is `seat-config.state_rules.deposit_disposition_days` (which exists and is correct) | `ONBOARDING.md:83` is the only site | `grep -rn 'deposit_disposition_days'` over the whole tree — 3 hits: seat-config key, ONBOARDING line, and the census | **MEDIUM** — a placeholder type with no consumer is a type that can never fail loudly |
| **F-PM-2** | `{{forward_email}}` has the same shape: 1 site, ONBOARDING-only, zero operating consumers | `ONBOARDING.md:63` | same method | **LOW** — matches the maintenance template's own treatment of this cover-sheet field, so it is parity rather than divergence, but it is still an uncensused dead type |
| **F-PM-3** | **Sweep-day split-brain.** C8's sweep day is configurable three ways — `{{followthrough_sweep_day}}` (2 prose sites), `seat-config.clocks.followthrough_sweep_day` (literal `"Monday"`) — **but the `monday-board` cron in `config.json` is the hard literal `0 8 * * 1`, and ONBOARDING contains no instruction to rewrite it.** A member answering "Tuesday" gets Tuesday in every prose surface and a job that still fires Monday, with no error | `config.json` crons[1]; `ONBOARDING.md` Step 5 adds month-end/owner-report crons but not this one | Read both files; grepped ONBOARDING for any `monday-board` cron edit — none | **MEDIUM** — exactly E2 capability 2's silent-failure class (literal default contradicting substituted prose, no marker) |
| **F-PM-4** | **`"timezone": ""` in `config.json`** — the turnover pass's **FINDING E2** holds verbatim in this tree. The daemon's resolver then supplies a host/org value and every clock in the seat runs in a timezone nobody chose. Also: **no `day_mode_*` keys exist in `config.json`**, so the day-mode window lives only in prose | `config.json:9`; no `day_mode` key anywhere in `config.json` | `grep -n '"timezone"\|day_mode' config.json` | **INHERITED, not new** — present identically in `templates/{maintenance,leasing}-coordinator/config.json`. Claiming a new number for it would overstate. Fixed by K1 in §10 |
| **F-PM-5** | **A cron seeded for a tab that may not be live.** `config.json` unconditionally seeds the `monday-board` cron, while D2 lets the member choose which of the nine tabs go live on day one. The fixture exercises this: Monday Board is a *later* tab, and the cron fires anyway from day one | `config.json` crons[1] ↔ `seat-config.platform.live_tabs_day_one[]` | Surfaced by writing the D2 fixture answer | **MEDIUM** — the seat writes/stages against a tab that does not exist yet; shadow mode masks it for the first week only |
| **F-PM-6** | **Assembly report internal count mismatch** (report defect, tree unaffected). §3's sub-heading reads *"Question-sourced (20 types, 165 sites)"*; the table beneath it lists **23 rows summing to 190 sites**, and the parenthetical two lines later says *"(23 rows…)"*. The tree and the fresh census both agree with the table body | `outputs/sa-pm-assist-assembly-report.md` §3 | Two-instrument diff (this pass's fresh grep vs the report) | **LOW** — stale sub-heading only; every downstream total in the report is correct |
| **F-PM-7** | **ONBOARDING Step 10's verify list is narrower than the tree.** The enumerated file list names 8 files carrying **98 of the 232 sites**. **102 operating sites are outside it — 101 in `.claude/skills/**` and 1 in `SYSTEM.md`.** Mitigated, not broken: the very next line runs a recursive `grep -rn '{{' .` that does catch them. But a human working the enumerated list and skipping the grep ships a seat with raw placeholders in 28 skill files | `ONBOARDING.md:234-236` | Per-file site census (§2.2) compared against the enumerated list | **MEDIUM** — same shape as the turnover pass's "a human following the shipped onboarding misses the same 6 sites", at 102 sites instead of 6 |

**Not findings, checked and clean:** notation discipline (zero `{{CTX_*}}`); all 41 question ids
present in ONBOARDING; all 7 copilot categories ship `locked` with the never-graduates `_note`
present; `seat-config.json` contains zero `{{...}}` (it is written by the interview, not
substituted); root file inventory 19/19 and skill count 40/40 as the assembly report claims;
every line count in the report's §2 table matches the tree exactly (re-derived by `wc -l`).

---

## 10. Requirements this table places on the engine (schema v2 / the E2 extension)

Cited against `outputs/glue-engine-extension-contract-2026-08-25.md`, by capability.

**K-ROWS this mapping declares** (E2 capability 2 — config keys by path, recorded in the
managed-surface manifest with question-id provenance):

| K | Target | Source | Why it must be a K-row |
|---|---|---|---|
| **K1** | `config.json` → `timezone` | cover-sheet Timezone | **MANDATORY.** A v2 seat mapping without this row is rejected at load, fail-closed (E2 capability 3, as amended 2026-08-25 ~0537Z). This seat has the cover sheet, so the row exists and is not optional. Closes F-PM-4's sourcing half |
| **K2** | `config.json` → `crons[name=monday-board].interval` | **C8** sweep day | Closes **F-PM-3**. Without it the prose and the job disagree silently |
| **K3** | `seat-config.json` → `kpi_targets.*` | **B8** overrides | Literal `95/90/60/90/25` must be overwritten per answered key and left intact per unanswered key |
| **K4** | `seat-config.json` → `clocks.renewal_tenant_followup_days` | **B9** | Literal `[30, 60]` |
| **K5** | `seat-config.json` → `clocks.followthrough_sweep_day` | **C8** | Literal `"Monday"` — the same answer as K2, two targets |
| **K6** | `config.json` → two new crons (month-end, owner-report) | **D6** `{{owner_report_day}}` | ONBOARDING Step 5 does this by hand today; a K-row makes it mechanical and manifest-recorded |
| — | `config.json` → `crons[name=daily-pulse].interval` | **NO SOURCE (N3)** | Declared explicitly as a retained literal, **not** a K-row. No question asks when the PM's day starts. Recorded so its absence reads as a decision, not an omission |
| — | `config.json` → `day_mode_start` / `day_mode_end` | maintenance B8 pointer | **No such key exists in any template `config.json`.** The applier must either create the keys or accept that the window lives only in prose. Same open item the turnover table raised; unchanged here |

**`cross_seat{}` records this mapping declares** (E2 capability 4a):

```
cross_seat: {
  deposit_disposition_days:  {owner_seat: maintenance, owner_question_id: A3},   # SEAM-1
  entry_notice_hours:        {owner_seat: maintenance, owner_question_id: A2},   # SEAM-33
  maintenance_sla:           {owner_seat: maintenance, owner_question_id: B5},   # B12 pointer
  platform_of_record:        {owner_seat: maintenance, owner_question_id: D1},   # SEAM-15
  owner_channel:             {owner_seat: maintenance, owner_question_id: D5},   # SEAM-16 (channel half)
  day_mode_window:           {owner_seat: maintenance, owner_question_id: B8},   # SEAM-19
  door_count_of_record:      {owner_seat: turnover,    owner_question_id: B6},   # SEAM-7
  unit_class_map:            {owner_seat: turnover,    owner_question_id: B1},   # SEAM-6
  make_ready_target_by_class:{owner_seat: turnover,    owner_question_id: B-grp},# B7 grain
  turnover_escalation:       {owner_seat: turnover,    owner_question_id: C-grp},# SEAM-37
  inspection_ownership:      {owner_seat: turnover,    owner_question_id: A2/D2},# SEAM-2
  application_decision_sla:  {owner_seat: leasing,     owner_question_id: B-grp},# SEAM-36
  renewal_offer_lead:        {owner_seat: leasing,     owner_question_id: cover},# SEAM-34
}
held_pending_seat: {
  owner_reserve_minimum:            accounting,  # SEAM-35, bookkeeping B3
  trust_variance_resolution_hours:  accounting,  # SEAM B14, bookkeeping B5/B6
  financial_board_owner:            accounting,  # C6 ↔ bookkeeping C3
}
cross_seat_checks: [
  {POLICY, property_manager_of_record, [maintenance C1, turnover D3, leasing D7, pm-assist A2]},
  {POLICY, backup_decision_maker,      [maintenance C9, turnover D7, pm-assist C5]},
  {POLICY, owner_approval_threshold,   [maintenance B1, turnover C1, pm-assist B1]},
  {POLICY, escalation_channels_hours,  [maintenance D6, turnover E8, leasing D10, pm-assist A3/C7]},
  {SPLIT,  channel_vs_sender_identity, [maintenance D5, turnover E5, pm-assist D5]},
  {SPLIT,  renewal_clock_nesting,      [leasing cover, pm-assist B9]},
]
never_graduate: [housing, housing_protected_class, money, legal, relationship]
```

**Four requirements stated as tests, not as prose:**

1. **Skills-file P-rows (capability 1).** 101 of 232 sites are in `.claude/skills/`.
   **Named test:** `{{followthrough_sweep_day}}` — a type with **zero root sites** — substitutes
   in `monday-board/SKILL.md`. Mutation removing the skills walk leaves the raw token and kills
   the test by name.
2. **Four-way POLICY check is 6 pairs, not 3 (capability 4d).** SEAM-11 now spans four seats,
   and §7.1 shows the real fixture set produces three distinct names **plus one match**. A check
   that stops at the first agreeing pair reports clean. **Named test:** four configured seats,
   three distinct PM names, one matching pair → the contradiction report lists **all three
   disagreeing pairs** and does not treat the match as resolution.
3. **C2 must not reach `copilot-thresholds.json` (POSTURE).** **Named test:** a fixture whose C2
   answer names a class produces `copilot-thresholds.json` with that category still
   `"status": "locked"`, and `owner_comms.assistant_may_send_without_review` carrying the intent.
   A mutation that writes `"unlocked"` at configure time must fail this test. Second named test:
   a C2 answer naming a value **outside the closed 7-class vocabulary** lands in
   `flags.unresolved[]` and creates **no new category** — a closed vocabulary needs a named test
   that reaches it through the production entry point, not an assertion in a comment.
4. **C1 rejects an invalid `now`.** **Named test:** a fixture C1 answer marking a
   judgment-subject row `now` writes `flags.unresolved[]` and **no** `delegation.rows` entry.

**Open item, not a requirement:** `seat-config.json` has no applier. This seat's structured half
is the largest of any seat so far — 13 top-level objects, 12 of the 41 questions land in it with
no placeholder at all. The assembly report's §11.6 is correct that this seat makes the gap
load-bearing; this table quantifies it rather than repeating it.

---

## 11. Coverage proof — both directions

**Direction 1 — questions → destinations: 41/41 mapped. Zero UNMAPPED.**

- Group A: 10/10 · Group B: 14/14 · Group C: 8/8 · Group D: 9/9
- 17 questions produce **23 placeholders**; 24 questions are S/K/G/I/B/C!-only.
- Weakest mappings, flagged honestly rather than dressed up: **B13** (S-only; consumer is the
  approval-queue completeness check, which is prose today), **C7** (S-only; consumer is a
  calendar habit, not a clock the agent runs), **A1** (descriptive — it weights targets, it sets
  none), **B10** (five values, one seat-config object, no bootstrap consumer beyond `alert-rules`).
- Zero bare flags: every pointer names an owner **seat and question id**; every gate names the
  behaviour it arms or disarms; every not-live state names the lane it darkens.

**Direction 2 — placeholders → sources: 32/32 sourced. Zero NO-SOURCE.**

| Source class | Types | Sites |
|---|---|---|
| Questionnaire answers (17 questions) | 23 | 190 |
| Cover sheet (4-field header) | 4 | 21 |
| Org-seeded + maintenance B8 pointer | 2 | 12 |
| add-agent framework values | 3 | 9 |
| **Total** | **32** | **232** |

**Direction 2b — values with no placeholder, sourced anyway.** The assembly report's §4
NO-SOURCE table (N1–N15) was verified, not assumed: all 15 are real literals in the files named,
and all 15 are correctly classed as unasked. Six of them are literal defaults that an answer can
legitimately override — N8 (KPI set), N9 (follow-up days), and the sweep-day/cron pair — and
those are the K-rows in §10. The other nine (shadow duration, digest time, pulse time, heartbeat
interval, PM re-ping, class taxonomy, three row schemas, pull-record convention, month-end lead,
owner-tag vocabulary) are **structural, not configurable**, and are recorded here as deliberate
literals so a later pass does not mistake them for gaps.

**Conditional gates preserved from the questionnaire's own text: 6** — A5/A6/A10 (unconfirmed
state law → lane not live, per jurisdiction), A8 (PM emergency authority recorded, never
acquired), C1 (execution-half-only delegation), C2 (recorded intent, zero unlock), D4 (alert with
no owner → UNRESOLVED). Every one arms or disarms behaviour; none of them moves a
never-graduates line, and two of them exist specifically to refuse to.

---

## 12. seat-config.json shape — as-shipped, with the v2 additions this table requires

Shipped shape (verified by reading the file, 121 lines): `{_note, seat, cover_sheet{},
people{}, coordinator_lanes{}, state_rules{_status, …}, thresholds{}, clocks{}, kpi_targets{},
delegation{rows{}}, owner_comms{}, platform{}, owner_reporting{}, flags{phase_zero[], unresolved[]}}`.

Raw answers are **not** preserved beside derived values in this seat's shipped shape — the
maintenance table's `answers: {A1..D9 raw text}` block has no counterpart here. That is a real
divergence from the pattern authority and it costs the property the maintenance table named:
re-mapping without re-asking. **Recommended addition (not made — draft tree is read-only):**
`answers: {A1..D9 raw text}` and `provenance: {questionnaire_version, filled_by, date}`.

**Required v2 additions** (E2 capability 4a, doctrine adopted verbatim from the turnover table):
`cross_seat{}`, `held_pending_seat`, `cross_seat_checks[]`, `never_graduate[]` — populated as
listed in §10.

---

## Worker stop line

Table + fixture, per contract. No build, no configurator run, no `add-agent`, no writes to
`templates/`, `outputs/templates-drafts/`, or the kit. Draft-tree defects flagged in §9 and left
in place. SEAM-1's migration ruling left to M-ACCOUNTING as the contract assigns.

---
## QA CROSS-CHECK RESOLUTION (collie QA seat, 2026-08-25 ~0700Z) — B14/C6 seam, both passes now on disk

RESOLVED, NO COLLISION: pm-assist B14 (trust_variance_broker_threshold) stays
pm-assist-owned as its own placeholder — POLICY per the SEAM-8 precedent (an escalation
rung and an internal split are different ladder steps that may legitimately differ).
Accounting's SEAM-21 decomposition STANDS as the semantic map (B14 dollar-component ↔
accounting B5 reconciliation_variance_threshold; B14 age-component ↔ B6
variance_alert_age_days) — it maps meaning, it does not transfer ownership. The seam
gains an ORDERING assertion (m-accounting's own new assertion type):
trust_variance_broker_threshold >= reconciliation_variance_threshold — a reversed
ladder would notify the broker before the bookkeeper's internal escalation fires.
Fixtures verified coherent: B5 = $40, B14 = $500, ordering holds; both fixtures carry
inline disambiguation notes against the turnover C1 $500; Avery Moss consistent across
maintenance C7 / turnover D6 / accounting C3, Sloane Karr consistent across pm-assist
A3 / accounting B14-answer. SEAM-22 (pm-assist C6 ↔ accounting C3 financial-board desk)
accepted as accounting-decomposed; accounting C6 (CPA of record) confirmed seamless by
id sweep. SEAM-11 five-way-at-promotion noted by both passes consistently.

## QA REGISTER AMENDMENT (collie, 2026-08-25 ~0710Z, per dane cross-table finding 1787639205649)

REGISTER ID COLLISION RESOLVED: this pass and the parallel accounting pass both continued
the turnover register and independently minted SEAM-20..24 with different meanings.
Ruling: the ACCOUNTING assignments keep 20..32; THIS table's five contributions are
renumbered to SEAM-33..37 (33 entry-notice, 34 renewal-clock nesting, 35 owner-reserve
floor, 36 leasing alert thresholds, 37 turnover escalation) - applied consistently
through this table's body (17 sites). The QA cross-check appendix above cites SEAM-21/22
in the ACCOUNTING sense, which is now the unambiguous assignment. FIXTURE NOTE (dane
LOW finding, documented not yet fixed): $400 appears as both turnover C7 per-unit
chargeback and the B5/B3 reserve floor (workers could not see each other; both values
seam-forced) - so the specific B3-to-per-unit-chargeback mis-route would produce a
silently equal number. Queued fixture edit: nudge reserve floor to $425 at the next
fixture-touching pass; until then this note IS the hole's documentation.
