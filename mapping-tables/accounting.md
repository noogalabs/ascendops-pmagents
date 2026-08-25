# AscendOps PMAgents glue: bookkeeping questionnaire → accounting-seat MAPPING TABLE (draft for mapping QA reviewer QA, then orchestrator reviewer)

Author: mapping-pass worker `m-accounting`, 2026-08-25. Status: DRAFT — the mapping QA reviewer's mapping-table
QA seat first, orchestrator reviewer eyeballs after (same gate shape as the maintenance table).
Contract: `outputs/mapping-contracts-accounting-pmassist-2026-08-25.md` § M-ACCOUNTING, executed
as written; the L2 shared-rules block it inherits
(`outputs/glue-lane2-contracts-2026-08-24.md`) binds verbatim.

Sources read for this pass:

- `private source-questionnaire archive` — all 46 Q,
  frozen kit doc, source side. Counted fresh today: 46 question headers, 46 blank `Answer:` slots,
  ids A1-A17, B1-B13, C1-C7, D1-D9.
- `outputs/templates-drafts/accounting-seat/` — the DESTINATION side (post-normalization draft
  tree, per the contract; **not** `templates/`). Census derived FRESH by grep today; no prior count
  was trusted or consulted before deriving it. Commands and raw counts recorded below.
- `outputs/sa-accounting-assembly-report.md` — the assembly pass's own census and mapping-forward
  table. Read AFTER the fresh census, and DIFFED against it rather than adopted (two instruments).
- `mapping-tables/maintenance.md` — pattern, taxonomy, cover-sheet precedent.
- `mapping-tables/turnover.md` and
  `mapping-tables/leasing.md` — the FACT/POLICY/SPLIT doctrine, the
  RUNTIME-PRESERVED census class, the seam register this table extends, and the X1 QA amendment.
- `outputs/glue-engine-extension-contract-2026-08-25.md` (§§ 1-4) — the schema-v2 consuming
  surface: K-rows, the fail-closed timezone K-row, cross_seat pointer resolution, owner-append.
- `private source-questionnaire archive,turnover,leasing,pm}-questionnaire/` — read for
  QUESTION IDS ONLY, to reference seams by id against frozen kit docs.

Rule (non-negotiable, from the shared block): every question gets a destination or an explicit
UNMAPPED-AND-WHY; every destination slot gets a source or an explicit NO-SOURCE flag. Both
directions proven by count in this file. **The census is the deliverable.**

**Authority-defect rule applied:** defects found in the draft tree are FLAGGED in § 11 and never
silently corrected. Nothing under `outputs/templates-drafts/` was written by this pass.

---

## 1. Destination taxonomy

Reused VERBATIM from the maintenance table. No codes invented.

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct `{{...}}` substitution at configure time |
| K | config.json key | Merged into the agent's config.json (schema-v2 K-row, engine contract § 2) |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board LOOKUP tab | The Bookkeeping Tracking Board's State Rules reference tab and threshold-driven alerts (the questionnaire's own stated *What Happens Next* destination) — SECONDARY, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behaviour (not just a value) |

**S binding for this seat, and the divergence it exposes.** The taxonomy defines S as
`seat-config.json`. This seat's structured-answers artifact is named **`accounting-config.json`**,
and the tree contains **zero** references to `seat-config` (verified: `grep -rn 'seat-config' .`
returns nothing). Every S destination in this table therefore resolves to
`accounting-config.json`. That is how the tree is, not how it should be — see **AF-1** in § 11.
The taxonomy code is not changed to match, because changing the code would hide the divergence
instead of surfacing it.

---

## 2. Cross-seat reconciliation doctrine

Inherited verbatim from the turnover table's doctrine section and the leasing table's X-series;
restated here only in the two lines this table applies constantly, not re-derived:

> **FACT** — one truth that cannot differ by seat. Exactly ONE seat's config carries the value;
> every other seat carries a pointer record `{owner_seat, owner_question_id}` and no copy.
> **POLICY** — a truth this seat sets, which may legitimately differ from a neighbouring seat's.
> Each seat OWNS its own value; a divergence is surfaced for human eyeball and NEVER auto-unified.

Single-state rule holds: at any moment exactly one config holds a FACT value; the others hold
pointer records only. Where the owner seat is not installed, ownership falls to the next seat in
the FIXED order named in the seam row, and the holding seat records `held_pending_seat`.

**One addition this seat forces.** A pair that MUST MATCH is a FACT, not a POLICY. Typing a
must-match pair POLICY is not a harmless label: POLICY means *surfaced, never unified*, so a real
mismatch on a must-match value reads as an accepted divergence and no one resolves it. B13 is
exactly that pair, and the draft tree types it POLICY — **AF-2** in § 11.

---

## 3. Destination census — the template side, derived fresh today

Commands run (read-only, against `outputs/templates-drafts/accounting-seat/`):

```
grep -rhoE '\{\{[^}]+\}\}'            . | sort | uniq -c | sort -rn   # permissive: 60 types / 162 sites
grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}'    . | sort -u | wc -l             # strict:     59 types / 161 sites
grep -rlE  '\{\{[^}]+\}\}'            . | sort                        # 11 files
```

The permissive pattern was run FIRST and deliberately: a strict `[a-zA-Z0-9_]` pattern silently
drops any token whose spelling it does not anticipate, and a negative search is only as good as
its spelling. The two patterns differ by exactly one token, which is the point of running both.

**Two of the 60 permissive tokens are literal prose, not destinations:**

| Token | Site | Why it is not a destination |
|---|---|---|
| `{{...}}` | `ONBOARDING.md:247` | Step text: "Replace any remaining `{{...}}` placeholders across …". An instruction *about* placeholders. |
| `{{placeholder}}` | `accounting-config.json:3` | Inside `_doctrine`: "An entry whose `value` is still a {{placeholder}} is UNANSWERED …". A doctrine sentence, not a slot. |

**Net: 58 placeholder types across 160 sites, in 11 files.**

### Per-file site counts (58 types / 160 sites)

| File | Sites |
|---|---|
| `ONBOARDING.md` | 56 |
| `accounting-config.json` | 55 |
| `SYSTEM.md` | 12 |
| `IDENTITY.md` | 11 |
| `SOUL.md` | 8 |
| `GUARDRAILS.md` | 6 |
| `HEARTBEAT.md` | 3 |
| `GOALS.md` | 3 |
| `CLAUDE.md` | 2 |
| `config.json` | 2 |
| `copilot-thresholds.json` | 2 |
| **Total** | **160** |

### Site split by source class

| Class | Types | Sites |
|---|---|---|
| FRAMEWORK — filled by add-agent / the goals generator before the configurator runs (`{{agent_name}}`, `{{current_timestamp}}`) | 2 | 4 |
| COVER SHEET (`{{company_name}}`, `{{org}}`, `{{org_name}}`, `{{forward_email}}`, `{{timezone}}`) | 5 | 19 |
| QUESTIONNAIRE — sourced to one of the 46 ids | 51 | 137 |
| **Total** | **58** | **160** |

### RUNTIME-PRESERVED sweep — a proven negative, not a hollow one

A double-brace token can carry a RUNTIME-environment value rather than an answer-mappable one.
Those are RUNTIME-PRESERVED: neither NO-SOURCE (which would invent a question for them) nor
omitted (which would silently shrink the census). Census-vocabulary class inherited from the
turnover table; not a new taxonomy code.

```
grep -rnoE '\{\{(CTX_[A-Za-z0-9_]+|[A-Z][A-Z0-9_]{2,})\}\}' .
```

**Result for the accounting draft tree: NO MATCH. Zero RUNTIME-PRESERVED tokens.** The 58/160
count is unchanged and no line moves class.

The negative has teeth because the identical sweep, run against
`templates/maintenance-coordinator/`, returns the known instance
**`{{CTX_ROOT}}` at `maintenance-coordinator/ONBOARDING.md:127`**. The pattern detects the class it
rules out here. Why this seat is clean: it writes runtime values in shell form — 157 occurrences of
`$CTX_ROOT` / `$CTX_AGENT_NAME` / `$CTX_ORG` / `${CTX_TELEGRAM_CHAT_ID}`, which never enter a
double-brace census. That is a template-authoring difference, not a difference in what the agent
needs at runtime, so a future edit could introduce the class here and the sweep above is the
re-check.

Also swept and found clean as mapping destinations: `{{ spaced }}` and `{{a.b}}` forms (no hits),
`${VAR}` (runtime only), `__TOKEN__` (no hits), `<ALLCAPS>` — two hits, both instructional
(`ONBOARDING.md:25` `<YOUR_TOKEN>`, `agent-management/SKILL.md:69` `<TOKEN>`), neither a slot.

### Destination slots that are NOT placeholders

A placeholder-only census misses these, and missing them is a silent-wrong-value bug rather than a
visible unsubstituted `{{...}}`. Derived by walking every `{value, q}` entry in
`accounting-config.json` and every literal in `config.json`:

| Slot | Shape | q | Why no placeholder |
|---|---|---|---|
| `retention.rent_records_years` | `null` | B11 | five distinct periods; a scalar would collapse them |
| `retention.vendor_bills_years` | `null` | B11 | as above |
| `retention.deposit_dispositions_years` | `null` | B11 | as above |
| `retention.reconciliations_years` | `null` | B11 | as above |
| `retention.records_1099_years` | `null` | B11 | as above |
| `platform.has_builtin_trust_reconciliation` | `null` | D1 | sub-answer; consumed as a prose condition today |
| `platform.has_platform_1099_filing` | `null` | D1 | as above |
| `platform.tracker_1099_exists` | `null` | D9 | phase-zero flag, not a runtime value |
| `state_rules.jurisdiction_statute_map` | `[]` | A17 | a single value is wrong for any multi-jurisdiction portfolio |
| `thresholds.reserve_floor_owner_overrides` | `[]` | B3 | maintenance B1-override precedent |
| `platform.account_inventory` | `[]` | D2 | structured; barred from carrying account numbers |
| `platform.read_only_access_paths` | `[]` | D7 | free-form by design |
| `policy.waiver_and_writeoff_authority` | literal `"property manager, in writing"` | B12 | asked as a role, written as a value |
| `config.json:day_mode_start` | literal `"08:00"` | **NONE** | **NO-SOURCE.** See AF-3 — and the cross-seat owner it should point at |
| `config.json:day_mode_end` | literal `"17:00"` | **NONE** | **NO-SOURCE.** as above |

**Total destination slots: 58 placeholder types + 13 non-placeholder config entries + 2 literal
config.json keys = 73.**

**Two-direction total: 71 of 73 destination slots sourced to a question or the cover sheet; 2
NO-SOURCE, both named, both carrying their reason and a proposed cross-seat owner. Zero bare
flags.**

### Citation coverage, re-derived

Every placeholder occurrence should carry its provenance on the same line. Re-derived
independently of the assembly report by classifying each of the 160 occurrences:

| Citation form | Occurrences |
|---|---|
| Same-line HTML comment (`{{x}} <!-- A1 -->`) | 50 |
| Same-line question id / `"q"` field / `cover-sheet:` marker | 106 |
| **Same-line total** | **156** |
| No same-line citation | 4 |

The 4 uncited occurrences are exactly `config.json:2` (`agent_name`), `config.json:9`
(`timezone`), `copilot-thresholds.json:2` (`agent_name`), `copilot-thresholds.json:3`
(`org_name`) — JSON forbids comments, and both files carry a file-level `_placeholder_sources`
object naming each. None is questionnaire-driven. This independently reproduces assembly V5.

---

## 4. Census DIFF against the assembly report — two instruments

The contract requires the assembly report's censuses be re-derived and diffed, not trusted.

| Quantity | Assembly report | This pass, fresh | Verdict |
|---|---|---|---|
| Placeholder types | 58 | 58 | **MATCH** |
| Placeholder occurrences | 160 | 160 | **MATCH** |
| Files carrying placeholders | 11 | 11 | **MATCH** |
| Same-line citations | 156 / 160 | 156 / 160 | **MATCH**, same 4 exceptions, same files, same lines |
| `{{CTX_*}}` placeholders | 0 | 0 | **MATCH**, and the negative is proven against a control |
| Questions with a template surface | 46 / 46 | 46 / 46 | **MATCH**, re-derived two ways (below) |

The raw grep totals differ (60/162 permissive vs 58/160) and the difference is fully explained:
the two literal-prose tokens in § 3. Nothing else moved.

**Questions-with-a-surface, re-derived two ways rather than one.** (a) Walking every `{value, q}`
entry in `accounting-config.json` yields **68 q-carrying destination entries** across **50 distinct
`q` values** = the 46 question ids + the 4 cover-sheet fields, with no id missing and none
invented. (b) `ONBOARDING.md`'s per-question destination tables carry a row for all 46 ids —
A1-A17, B1-B13, C1-C7, D1-D9, zero gaps. Two instruments, same answer.

### The one place the report's own classification does not survive the diff

The report's § 3 is titled *NO-SOURCE defaults* and lists 13 rows. Re-classified against the
frozen kit docs and the tree, only **2** of those 13 are NO-SOURCE. The rest belong to four other
classes the single title conflates. This is a report-level finding (**AF-4**), not a tree defect —
the tree's literals are all correct and correctly placed.

| Re-classified as | Rows | Which |
|---|---|---|
| **NO-SOURCE** — no question, no cover-sheet field, no kit prose | 2 | day mode start `08:00`, day mode end `17:00` |
| **FEDERAL-CONSTANT** — not a company value at all; the report itself says so in its Why column | 3 | 1099-NEC threshold `$600`, 1099-NEC due `January 31`, W-9 required before first payment |
| **KIT-PROSE-SOURCED** — sourced to the frozen kit docs, just not to a *question* | 6 | shadow-mode exit rule; suspense aging clock; approval aging ladder; invoice aging bound; vendor payment hold ceiling; NSF notification window |
| **QUESTION-SOURCED, mis-listed** | 1 | waiver / write-off authority — B12 asks it, and `accounting-config.json` records it with `"q": "B12"` |
| **FRAMEWORK-INHERITED** | 1 | heartbeat interval `4h`, carried from the structure authority |
| | **13** | every row accounted for |

The six KIT-PROSE-SOURCED rows were verified against the frozen kit at line level rather than
taken from the report — the instrument was checked, and so were its readings:

| Value | Tree | Frozen kit source |
|---|---|---|
| Vendor payment hold ceiling, three business days | `vendor-banking-change/SKILL.md:88` | `accounting-vendor-banking.md:246` |
| NSF notification within two hours | `GUARDRAILS.md:53`, `returned-payments/SKILL.md:18` | `accounting-flow.md:84` |
| Approval aging 24h remind / 48h escalate | `daily-money-review/SKILL.md:28`, `accounting-board/SKILL.md:62` | `accounting-board.md:164-165` |
| Suspense: escalate at 1 business day, never past 3 | `suspense-and-unmatched-payments/SKILL.md:19,21` | `accounting-judgment.md:26-27` |
| Invoice aging past 5 business days | `trust-reconciliation/SKILL.md:82`, `vendor-bill-intake/SKILL.md:68` | `accounting-judgment.md:50` |
| Shadow-mode exit, two consecutive weeks | `accounting-config.json:shadow_mode_exit_rule` | questionnaire *What Happens Next* |

Search-completeness note: the first sweep for these used digit spellings (`3 business days`,
`2 hours`) and returned near-nothing, because the tree writes them in words
(`three business days`, `two hours`). The digit-spelling negative was wrong and was not reported
as a finding; the word-spelling sweep is what these line numbers come from.

---

## 5. Cover sheet (an answers-FILE addition — kit docs stay FROZEN)

The maintenance precedent's 4-field header, and unlike the turnover seat **all four are used by
this template**:

| Field | Fills | Sites |
|---|---|---|
| Company name | `{{company_name}}` | 5 |
| Org short-name | `{{org}}` (4) + `{{org_name}}` (2) | 6 |
| Forward email | `{{forward_email}}` | 2 |
| Timezone | `{{timezone}}` — incl. `config.json:9` | 6 |

**No fifth field is minted.** The turnover seat needed five stage-clock fields because its
questionnaire never asked its internal clocks; this questionnaire's Group B asks the seat's clocks
directly (B4-B6, B8-B10), so there is no gap to fill. The only unfilled destination pair is
day mode, and the correct resolution there is a **cross-seat pointer to maintenance B8**, not a
new cover-sheet field that would duplicate the one question in the whole kit that asks the
external-communications window (leasing X2 precedent, applied identically). See SEAM-19 and AF-3.

**Adjacency traps refused, deliberately.** A check whose subject is silently substituted is worse
than an honest flag:

- **D8's escalation hours are NOT the agent's day-mode window.** D8 asks which channel each person
  looks at quickly and what hours apply to *that person's reachability*. Day mode is the agent's
  own responsive/quiet posture. The assembly report refused this stretch too, and it was right to.
- **A13's trust-record retention is NOT B11's reconciliation retention, and A16's decision-log
  retention is neither.** Three separate questions, three separate record classes; the fixture
  happens to answer all three "7 years" and that coincidence must not become a mapping.
- **B3's reserve floor is NOT turnover C1's pre-approved reserve threshold.** Same word, opposite
  direction: B3 is cash that must REMAIN in the ledger; C1 is spend that may LEAVE it without
  asking. See SEAM-26.
- **B13's chargeback numbers are NOT B1's vendor-bill approval threshold.** Deposit-deduction
  authority versus repair-spend authority; the questionnaire's own B13 hint says so in its last
  sentence. Turnover C7 precedent, and the golden fixture exercises it below.

---

## 6. Per-question mapping (46/46)

### Group A — State Rules (17)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 late-fee grace days | **P** `{{late_fee_grace_days}}` (2), S, G, B | Statutory. Owner of the decomposed late/eviction clock family (SEAM-31); pm-assist A5 bundles this into one question and holds a pointer. |
| A2 late-fee cap (flat / daily / percentage) | **P** `{{late_fee_cap}}` (2), S, G, B | Accounting-OWNED FACT — no other seat in the kit asks it. Shape is a discriminated value (flat vs rate vs percent), which the scalar placeholder carries as text; the machine home is S. |
| A3 nonpayment notice period | **P** `{{nonpayment_notice_days}}` (2), S, G | SEAM-31. The answer must carry *what counts as service*, which the placeholder cannot hold — S carries the full text, G carries the service rule. |
| A4 pay-or-quit vs unconditional quit | **P** `{{nonpayment_notice_type}}` (2), S, G, **C!** | Arms the notice-wording class. `accounting-config.json` constrains it to `["pay-or-quit","unconditional-quit"]`; an answer outside the pair disarms rather than guesses. |
| A5 does partial payment void the notice | **P** `{{partial_payment_voids_notice}}` (2), S, G, **C!** | Accounting-OWNED. Gate runs the OTHER way from the usual: while unconfirmed, the questionnaire's own safe working rule is ARMED — every payment on a noticed account is flagged to the PM before it is applied. Unanswered is not permissive here, it is stricter. Per-jurisdiction (SEAM-28); the fixture answers it differently for the two jurisdictions on purpose. |
| A6 deposit return deadline + clock trigger | **P** `{{deposit_return_days}}` (4) + `{{deposit_clock_trigger}}` (3), S, G | **SEAM-1, and the decision this pass owns.** The deadline is a FACT whose owner today is **maintenance A3**; this seat holds a POINTER plus a **MIGRATION-PENDING** mark. The clock-trigger sub-value is owned by **leasing B1**; pointer as well. See the SEAM-1 row for the exact recorded state. |
| A7 separate deposit account + resident disclosure | **P** `{{separate_deposit_account_required}}` (2), S, G, **C!** | SEAM-32 owner. Two sub-answers (account requirement, disclosure duty); the placeholder carries the requirement, S carries both. Gate interlocks D3: A7 true + D3 false = day-one fix, and the deposit-holding compliance check goes dark rather than reporting clean. |
| A8 deposit interest required | **P** `{{deposit_interest_required}}` (2), S, G | SEAM-32. |
| A9 deposit amount cap | **P** `{{deposit_cap}}` (2), S, G, B | SEAM-32. |
| A10 NSF / returned-payment fee cap | **P** `{{nsf_fee_cap}}` (2), S, G, **C!** | Accounting-OWNED. Gate: the fee is chargeable only if the lease carries it AND the state allows it — two conditions, both required, and the ACH-vs-check scope rides in S because the placeholder is a single number. |
| A11 eviction filing window + file-or-hold decision window | **P** `{{eviction_filing_decision_days}}` (2), S, G | SEAM-31. Two clocks in one question; the placeholder holds the *decision* window (the company value), the statutory filing window rides in S with A3. |
| A12 statutory owner-disbursement deadline | **P** `{{owner_disbursement_statutory_deadline}}` (2), S, G | Accounting-OWNED. Interlocks B8: where the statute sets none, the management agreement governs and B8's date becomes the binding promise. Both are written; neither overwrites the other. |
| A13 trust reconciliation: cadence, signer, retention, regulator | **P** ×4 — `{{trust_reconciliation_cadence}}`, `{{trust_reconciliation_signer}}`, `{{trust_record_retention_years}}`, `{{trust_audit_regulator}}` (2 sites each), S, G | Accounting-OWNED FACT, and the only question in the kit that produces four placeholders. The signer value feeds a **never-graduate** gate (`reconciliation_signoff` is a licensed act) — the answer names WHO signs; no answer makes the agent a signer. |
| A14 state-level 1099 filing | **P** `{{state_1099_filing_required}}` (2), S, **C!** | Accounting-OWNED. Gate: `confirmed:false` disables the state-filing check and the seat reports it DISABLED. The federal January 31 obligation is a FEDERAL-CONSTANT and is unaffected — the two must not share a gate. |
| A15 contractor-license flag threshold + trades | **P** `{{contractor_license_threshold}}` (3) + `{{license_required_trades}}` (2), S, G | **SPLIT (SEAM-25).** The trades list is a FACT owned by **maintenance A7** (richer question, ten trades) → pointer. The dollar threshold has no counterpart anywhere in the kit and is accounting-OWNED. Two placeholders, two ownerships, one question. |
| A16 decision-log retention | **P** `{{decision_log_retention_years}}` (2), S | SEAM-30. Distinct record class from A13 and B11; see the refused adjacency in § 5. |
| A17 per-jurisdiction statute map | **S only** (`state_rules.jurisdiction_statute_map`, array) + I prose at `SYSTEM.md:44-45` | **UNMAPPED to any placeholder, and the weakest surface in this seat — flagged, not buried.** A scalar would be wrong for any multi-jurisdiction portfolio. The report says so; this pass agrees and goes further: **A17 is not merely a value, it is the SHAPE of Group A.** When the portfolio spans jurisdictions, A1-A16 are per-jurisdiction maps rather than scalars, and every one of those 16 has a scalar placeholder. Nothing in the tree enforces that today. The golden fixture makes the failure concrete rather than theoretical: A5 has one answer in Pine Basin and a different, unconfirmed answer in Cedar Mesa, and the single `{{partial_payment_voids_notice}}` placeholder cannot hold both. SEAM-28 owner. |

### Group B — Company Thresholds and Policy (13)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 vendor-bill PM approval threshold | **P** `{{vendor_bill_approval_threshold}}` (3), S, G, B | **POLICY (SEAM-8 family). Do NOT collapse** with maintenance B1 or turnover C1. Three seats, three authorities: owner pre-approval for repair spend (maintenance B1), make-ready reserve (turnover C1), bill-payment approval (accounting B1). The fixture carries three different numbers deliberately. |
| B2 dual-authorization threshold | **P** `{{dual_auth_threshold}}` (2), S, G, **C!** | Accounting-OWNED — no seat asks it. Gate: at or above, a second person signs before release, and the second person is constrained not to be the preparer (C7's constraint shape, applied to payments rather than to banking changes). Same numeric SHAPE as B1/B3/B4, which is the trap § 10 exercises. |
| B3 reserve floor + per-owner overrides | **P** `{{reserve_floor}}` (4), S, B; overrides **S-only** (`reserve_floor_owner_overrides`, array) | **SEAM-26 owner.** Base floor → placeholder; the override map has no placeholder and S is its machine home (maintenance B1-override precedent). Adjacency trap refused: this is a cash floor, not turnover C1's spend authority. |
| B4 unidentified-payment same-day escalation | **P** `{{unidentified_payment_escalation_threshold}}` (5), S, G | Accounting-OWNED. Interlocks D5: below the threshold the payment *sits in suspense*, so the value is meaningless if no suspense account exists — D5's gate governs whether B4's check runs at all. |
| B5 small-vs-large reconciliation variance split | **P** `{{reconciliation_variance_threshold}}` (2), S, G, **C!** | **SEAM-21.** Gate: above the split, a variance escalates immediately and MAY HOLD owner statements — it can arm B10's hold. pm-assist B14's "what dollar size goes straight up" resolves to THIS value, not to B6's. |
| B6 variance alert amount + age | **P** `{{variance_alert_amount}}` (3) + `{{variance_alert_age_days}}` (3), S, B | **SEAM-21.** Two placeholders. pm-assist B14's "how long does the bookkeeper get to resolve" resolves to `variance_alert_age_days`. B14 is one question over three accounting values; the decomposition is recorded in the seam so no one writes a third copy. |
| B7 payment application order | **P** `{{payment_application_order}}` (2), S, G | Accounting-OWNED, and it is a fact about the PLATFORM, not a company preference — the question's own hint says confirm what the platform is configured to do, not what you assume. The mapping preserves that: S carries a verified-vs-assumed note, and an unverified answer is recorded as unverified rather than promoted. |
| B8 owner draw window + target date | **P** `{{owner_draw_deadline_day}}` (3) + `{{owner_draw_target_day}}` (2), S, G | Two placeholders. Interlocks A12 (see above) and B10 (statements before draws). |
| B9 vendor payment run dates | **P** `{{vendor_payment_run_dates}}` (2), S, G, B | A list in a scalar placeholder — carried as text, structured in S. Fixed run dates are what make the invoice-aging alerts mean anything, so G carries the rule and not just the dates. |
| B10 owner statement release date | **P** `{{owner_statement_release_day}}` (3), S, G, **C!** | **SEAM-27.** Gate is a hard rule, not a threshold: statements NEVER release over an unreconciled trust account, and B5's large-variance branch can hold them. The date is a POLICY value; the hold is structural and ships regardless of any answer. |
| B11 per-item-type archive retention | **S only** — five `null` slots (`retention.*`) | **UNMAPPED to any placeholder, flagged.** Five distinct periods; a scalar collapses them. SEAM-30: the five classes are disjoint from leasing B5 and pm-assist A9, and must stay disjoint. |
| B12 waiver / write-off authority | **S only** (literal default), G | Asked as a ROLE, written as a value; resolves to C1 in practice. **Interlock the fixture exercises:** the authority requires the reason to be recorded in the PM decision log, and D6 can answer that the log does not exist yet — a policy whose recording surface is phase-zero. Written so the gap is visible before the first waiver, not after. |
| B13 deposit chargeback per-line + per-unit | **P** `{{deposit_chargeback_per_line}}` (2) + `{{deposit_chargeback_per_unit}}` (2), S (`chargeback_gates{}`), G, **C!** | **SEAM-20. FACT, owner = turnover C7.** B13's own text: "Do not set a new number here… record it here only to confirm the two match." This seat ENFORCES the number as the Deposit Packet review gate; it does not set it. Correctly kept out of `thresholds{}` in the tree so no configurator confuses it with B1 by key adjacency — that part of the draft is right. The `cross_seat_checks` TYPE is not (AF-2). |

### Group C — Roles and People (7)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 PM of record for owner-money decisions | **P** `{{property_manager_name}}` (4), S, I | **SEAM-11, now FIVE-WAY. POLICY, per-seat owned.** Owner-money decisions may legitimately answer to a different desk than maintenance dispatch. Cross-check on difference; never auto-unify. |
| C2 principal / managing broker | **P** `{{broker_name}}` (5), S, I | **SPLIT (SEAM-23).** Identity = FACT (one principal broker per company). Broker-escalation channel = POLICY per seat. This name is legally load-bearing: it is the licensee accountable for the trust account and the signer in A13. |
| C3 human bookkeeper (staff / principal / outside) | **P** `{{bookkeeper_name}}` (3), S, I | **SEAM-22 / SEAM-18 owner.** Finest grain in the fleet: the only question asking which of three shapes the role takes. The daily digest recipient derives from it. pm-assist C6 asks the same desk in narrative form and holds a pointer. |
| C4 backup decision-maker | **P** `{{backup_decision_maker}}` (4), S, I, **C!** | **SEAM-12, now FOUR-WAY. POLICY.** Gate: empty → UNRESOLVED flag surfaced in the calibration digest, per the question's own hint that a statutory deadline with no available decision-maker is a company-structure problem, not a config gap. Maintenance C9 precedent preserved verbatim. |
| C5 eviction attorney of record | **P** `{{eviction_attorney}}` (3), S, I | **SEAM-24.** FACT; owner = **pm-assist A4**, which holds the whole counsel inventory (eviction attorney AND general counsel) — putting the eviction attorney elsewhere forks that inventory. This seat holds a pointer plus the channel it actually uses. Holding order while pm-assist is absent: pm-assist → accounting, `held_pending_seat: pm-assist`. |
| C6 CPA of record | **P** `{{cpa_of_record}}` (3), S, I | **Accounting-OWNED FACT, and the only Group C role with NO counterpart in any other seat's questionnaire** — verified by id sweep across the maintenance, turnover, leasing, and pm-questionnaires. Stated explicitly because the contract names a "B14/C6" seam and *this* C6 is not half of it; the seam's C6 is pm-assist C6 (see SEAM-22). The CPA also owes the annual A14 confirmation, so C6 and A14 interlock. |
| C7 second-person verifier (vendor banking change) | **P** `{{second_person_verifier}}` (3), S, I, **C!** | Accounting-OWNED. Gate carries a CONSTRAINT, not just a name: the verifier must not be the person who processed the change, and the payment does not release until the spot-check is done. A configurator that accepts the same name for C3 and C7 has written a control that cannot fire; the constraint is recorded in S so that is checkable. |

### Group D — Platform, Banking, and Wiring (9)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| D1 accounting platform (+ 2 sub-booleans) | **P** `{{accounting_platform}}` (3), S, I; sub-booleans **S-only** (`null`) | **SEAM-15.** Platform identity is a FACT owned by **maintenance D1** (which names both the maintenance platform and the accounting system) → pointer. The two sub-booleans — built-in trust reconciliation, platform 1099 filing — are asked by no other seat and are accounting-OWNED. They change month-end and year-end mechanics, so they are conditions, not decoration. |
| D2 banks + full account inventory | **S only** (`account_inventory`, array) | **UNMAPPED to any placeholder, correctly.** Accounting-OWNED FACT. Carries a HARD RULE into G: account and routing numbers are never recorded here or in any tracked file — purpose, bank, and label only. A placeholder would invite exactly the wrong value. |
| D3 is the deposit trust already separate | **P** `{{deposit_trust_separate}}` (3), S, **C!** | Gate interlocks A7: `A7 == required && D3 == false` → day-one fix and the deposit-holding compliance check goes DARK. Two questions, one gate; neither alone arms it. |
| D4 positive pay enrolled | **P** `{{positive_pay_enrolled}}` (3), S | Accounting-OWNED. **WEAK MAPPING, flagged (AF-5):** the real answer is per-account, the placeholder is one boolean. The fixture answers honestly — enrolled on three of four accounts, because the bank does not offer it on deposit-only trust accounts — and the scalar cannot carry that. A boolean here reports a fraud control as present when it is partial. |
| D5 suspense / clearing account exists | **P** `{{suspense_account}}` (3), S, **C!** | Gate: false → unmatched-payment handling has no legitimate destination, the class goes dark, and B4's threshold has nothing to gate. Phase-zero. |
| D6 board + decision-log location, and do they exist | **P** `{{board_location}}` (3) + `{{decision_log_location}}` (3), S, **C!** | **SPLIT (SEAM-29).** The bookkeeping board's location is accounting-OWNED. The decision log's location is a FACT owned by **pm-assist D7** (the durable-records inventory) → pointer. The **exists-yet** flag for both is accounting-OWNED, because D6 is the only question in the kit that asks it. Gate: either missing → the agent watches nothing that depends on it, and B12's waiver authority loses its recording surface. Single-source rule quoted into G (turnover E1 precedent): a log of record that lives in two places is not a log of record. |
| D7 read-only access paths | **S only** (`read_only_access_paths`, array) | **UNMAPPED to any placeholder, correctly** — free-form by design; "a statement drop into a shared folder" is a valid day-one answer. Accounting-OWNED. G carries the standing rule: the agent is read-only by construction, not by policy. |
| D8 money-escalation channels + hours per person | **P** `{{money_escalation_channel}}` (3) + `{{after_hours_escalation_channel}}` (4), S, G | **SEAM-17. POLICY, per-seat owned** — different seats wake different people at different hours by design. Two placeholders because the after-hours route is a distinct control: a fraud flag that waits for morning is not a control, and the question's own hint says so. The "hours" component seeds nothing automatically — see the refused adjacency in § 5. |
| D9 W-9 storage + 1099 tracker exists | **P** `{{w9_storage_location}}` (3), S; tracker **S-only** (`null`), **C!** | Accounting-OWNED. Gate: no tracker → year-end readiness DISABLED and reported disabled, rather than reporting a clean year-end. Interlocks the FEDERAL-CONSTANT that a W-9 is required before a vendor's first payment. |

**46/46 mapped. Zero UNMAPPED.** Six questions have no placeholder and are S-only — A17, B11, B12, D2, D7, and the sub-slots of D1/D9 — each with its reason stated above rather than a bare flag.

---

## 7. Cross-seat seam register (referenced by QUESTION ID only)

The pm-assist mapping pass runs in parallel with this one, so every pm-assist reference below is
to a QUESTION ID in the frozen kit doc
(`private source-questionnaire archive`, 41 Q, ids A1-A10, B1-B14,
C1-C8, D1-D9, verified today), never to that worker's table or its line numbers. Same discipline
for maintenance (38 Q), turnover (34 Q), and leasing (39 Q).

Seam numbering continues the turnover series. Rows SEAM-1 … SEAM-19 already exist; this table
JOINS eight of them and mints thirteen new ones.

### Seams this seat joins

| # | Value | Seats (by Q ID) | Class | Resolution as amended by this pass |
|---|---|---|---|---|
| SEAM-1 | Security-deposit disposition deadline | maintenance **A3** ↔ turnover **A1** ↔ leasing **B1** ↔ pm-assist **A7** ↔ **accounting A6** | FACT | **FIVE-WAY now. Owner remains maintenance A3** — the X1 QA amendment stands and this pass does not reopen it. **This pass owns the migration decision, and records it as MIGRATION-READY:** SEAM-1's named migration trigger is "when the bookkeeper seat ships AND asks it." This questionnaire *does* ask it (A6), but the seat is a DRAFT tree, not shipped into `templates/` through a reviewed PR. Therefore: **maintenance A3 remains owner today; this table holds a POINTER plus a `migration_pending` mark that flips ownership to accounting A6 AT PROMOTION.** Not migrated early; the readiness is not omitted. Recorded state, exactly: `{owner_seat: "maintenance", owner_question_id: "A3", local_question_id: "A6", migration_pending: true, migration_trigger: "accounting seat lands in templates/ via reviewed PR", migrates_to: {owner_seat: "accounting", owner_question_id: "A6"}}`. The clock-TRIGGER sub-value stays leasing B1's, and A6 asks it too — same pointer discipline, no second copy. |
| SEAM-8 | Money-gate family: spend / approval thresholds | maintenance **B1** ↔ turnover **C1** ↔ pm-assist **B1**, **B2** ↔ **accounting B1** | **POLICY** | **Per-seat owned. Do NOT collapse.** Five questions of identical numeric shape gating five different authorities: owner pre-approval for repair spend, make-ready reserve, PM owner-pre-approval, coordinator spend authority, vendor-bill payment approval. Contradiction cross-check surfaces the set for eyeball and never unifies it. **This is the same-shape trap the contract names**; the golden fixture exercises it (§ 10). |
| SEAM-11 | Property manager of record | maintenance **C1** ↔ turnover **D3** ↔ leasing **D7** ↔ pm-assist **A2** ↔ **accounting C1** | **POLICY** | **FIVE-WAY now** (the contract's four-way, plus this seat). Verified four-way as given: maintenance C1 "PM or supervisor of record for maintenance", turnover D3 "PM of record for scope escalation and damage-notice gates", leasing D7 "who decides approvals, denials, rates, renewal terms, holds" plus its owner-approval seat above, pm-assist A2 "who holds the Property Manager seat". Accounting C1 adds a fifth distinct scope: owner-MONEY decisions. Five seats may name up to five different people and that is a real org shape. Cross-check on difference; never auto-unify. |
| SEAM-12 | Backup decision-maker | maintenance **C9** ↔ turnover **D7** ↔ pm-assist **C5** ↔ **accounting C4** | **POLICY** | FOUR-WAY. Per-seat owned; each seat's clock is different, so each seat's backup may be. Empty on any side → UNRESOLVED flag in that seat's calibration digest. |
| SEAM-15 | Platform of record | maintenance **D1** ↔ turnover **E3** ↔ leasing **D1** ↔ pm-assist **D1** ↔ **accounting D1** | FACT | Owner = **maintenance D1** for the platform inventory (it names both the maintenance platform and the accounting system). Each seat records which platform carries ITS work — that routing is the seat's own. Accounting adds two owned sub-booleans no other seat asks. |
| SEAM-17 | Escalation channels + hours | maintenance **D6** ↔ turnover **E8** ↔ leasing **D10** ↔ pm-assist **D5** ↔ **accounting D8** | **POLICY** | Per-seat owned. Accounting's addition to the class: a SECOND, after-hours route that is a control rather than a convenience (fraud, suspected trust shortfall). A cross-seat unifier that collapsed D8 into a single business-hours channel would delete a control without erroring. |
| SEAM-18 | Money-side executor | turnover **D6** (deposit disposition) ↔ maintenance **C7** (invoice payment) ↔ **accounting C3** (posts, pays, reconciles) | **SPLIT** | Previously "adjacent, not shared." With the accounting seat present it resolves: the EXECUTOR IDENTITY is a FACT owned by **accounting C3** (finest grain — the only question asking staff vs principal vs outside bookkeeper); the per-path HANDOFF LOCATIONS (maintenance C7's AP inbox, turnover D6's deposit-evidence inbox) stay per-seat POLICY. The cross-check that mattered — "did the member mean one person and name two?" — is now answerable against a single owner. |
| SEAM-19 | Clock context: timezone + day-mode window | maintenance **B8** + cover sheets ↔ **accounting cover sheet + `config.json` literals** | FACT | Timezone: install-level, one value per install, on every seat's cover sheet, and it MUST reach `config.json` (engine contract § 3 — satisfied here, `config.json:9` is `{{timezone}}`). Day-mode window: owner = **maintenance B8**, the only question in the whole kit that asks the external-communications window. This seat has neither a question nor a cover-sheet field for it and instead carries **literal 08:00 / 17:00** — see **AF-3**. Correct resolution is a pointer to maintenance B8 (leasing X2 precedent), not a new cover-sheet field. |

### Seams this pass mints

| # | Value | Seats (by Q ID) | Class | Resolution |
|---|---|---|---|---|
| SEAM-20 | Deposit-deduction chargeback threshold (per line + per unit) | **accounting B13** ↔ turnover **C7** | **FACT** | **Owner = turnover C7.** B13's own text forbids setting a new number and asks only that the two be confirmed to match. Accounting holds a pointer and ENFORCES the number as the Deposit Packet review gate. A mismatch is an ERROR to resolve at the owner, not an accepted divergence — which is precisely why the draft's POLICY typing is a defect (AF-2). Holding order while turnover is absent: turnover → accounting, `held_pending_seat: turnover`. |
| SEAM-21 | Trust-account variance rule | **accounting B5** + **B6** ↔ pm-assist **B14** | **FACT** | One operational rule about one bookkeeper, asked at two grains. **Owner = accounting** (finest: three values across two questions). pm-assist B14 bundles two of them into one question and holds POINTERS, never a third copy. Decomposition, recorded so no one re-derives it: B14's *"what dollar size goes straight up"* → `thresholds.reconciliation_variance_threshold` (**B5**); B14's *"how long does the bookkeeper get to resolve"* → `thresholds.variance_alert_age_days` (**B6**). `variance_alert_amount` (**B6**) has no B14 counterpart and is accounting-only. **This is the first half of the contract's named B14/C6 seam.** |
| SEAM-22 | Who works the financial board day to day | **accounting C3** ↔ pm-assist **C6** | **FACT** | **Owner = accounting C3.** pm-assist C6 asks who pulls reports, posts payments, generates statements, and flags anomalies — the same desk C3 names, in narrative form. C3 is finer (it forks staff / principal / outside bookkeeper, which changes the digest routing), so C3 owns and C6 points. **This is the second half of the contract's named B14/C6 seam.** Cross-references SEAM-18: same person, different question about them. **Note for the QA seat:** the contract's "B14/C6" is TWO pm-assist ids seaming into accounting, not one pair — SEAM-21 and SEAM-22 are addressed separately and by id so either reading is covered. Accounting's own C6 (CPA of record) is unrelated and has no counterpart in any seat (see the C6 mapping row). |
| SEAM-23 | Principal broker / company owner | **accounting C2** ↔ pm-assist **A3** | **SPLIT** | Identity = FACT; **owner = accounting C2**, which carries the legally load-bearing framing (the licensee accountable for the trust account, the A13 reconciliation signer). Broker-escalation CHANNEL = POLICY, per-seat owned. Collapsing the channel would route a trust-shortfall alert down a general-escalation path. |
| SEAM-24 | Eviction attorney of record | **accounting C5** ↔ pm-assist **A4** | **FACT** | **Owner = pm-assist A4** — it holds the whole counsel inventory (eviction attorney AND property/general counsel), so owning the eviction attorney elsewhere forks that inventory. Accounting C5 holds a pointer plus its own channel. Holding order while pm-assist is absent: pm-assist → accounting. |
| SEAM-25 | Contractor licensing | **accounting A15** ↔ maintenance **A7** | **SPLIT** | Trades-requiring-a-license list = FACT, **owner = maintenance A7** (richer, ten trades) → pointer. Dollar flag threshold = **accounting-OWNED**; no seat asks it. One question, two ownerships, two placeholders. |
| SEAM-26 | Owner reserve floor | **accounting B3** ↔ pm-assist **B5** | **FACT** | A number the management agreement sets — a document fact, not a per-seat policy. **Owner = accounting B3** (finest grain: per-owner overrides with the source agreement named). pm-assist B5 asks the per-unit minimum and holds a pointer. **Adjacency trap refused and recorded:** turnover **C1** shares the word "reserve" and is the opposite direction — cash that may LEAVE the ledger without asking, versus cash that must REMAIN. They must never be collapsed, and a configurator matching on the word "reserve" would collapse them. |
| SEAM-27 | Owner statement release vs owner report-pack day | **accounting B10** ↔ pm-assist **D6** | **POLICY, with an ORDERING assertion** | Per-seat owned — the two dates are genuinely different events. But the cross-check here is NOT an equality check, and this is the new shape this seam contributes: the report pack CONTAINS the statement, so `reconciliation_complete ≤ B10 ≤ pm-assist D6` must hold. Two dates that differ are fine; two dates in the wrong ORDER ship an owner a pack referencing a statement that does not exist. An equality-only cross-check passes that silently. |
| SEAM-28 | Jurisdiction inventory | **accounting A17** ↔ maintenance **A2** ↔ leasing **B6** | **SPLIT** | The LIST of jurisdictions is ONE FACT; **owner = accounting A17**, the only question asking which statute governs each one. Each seat owns its own per-jurisdiction VALUES (maintenance A2 entry-notice hours, leasing B6 source-of-income status, accounting A1-A16). Load-bearing because the statute determines which per-jurisdiction values may legitimately differ at all — a portfolio under one statute and a portfolio under two are different configuration shapes, not the same shape with different numbers. |
| SEAM-29 | Board and decision-log location | **accounting D6** ↔ pm-assist **D3**, **D7**, **C8** | **SPLIT** | Bookkeeping board location = accounting-OWNED. Decision-log location = FACT, **owner = pm-assist D7** (durable-records inventory); accounting D6 points. The **exists-yet** flag for both = accounting-OWNED, since D6 is the only question that asks it. pm-assist C8 asks the log's INTAKE MECHANISM, which is pm-assist-owned and not a duplicate of the location. Single-source rule applies (turnover E1): one decision log, or it is not a log of record. |
| SEAM-30 | Record retention periods | **accounting A13, A16, B11** ↔ leasing **B5** ↔ pm-assist **A9** | **FACT, disjoint by class** | No single owner and none needed: each seat names record classes the others do not (trust records, decision log, and five bookkeeping classes here; application/screening records at leasing B5; tenant files at pm-assist A9). Recorded as a seam so a later pass does not collapse "retention" into one number. Cross-check asserts DISJOINTNESS — an overlap means two seats claim the same record class, which is the actual failure mode. |
| SEAM-31 | Late-rent and eviction notice clocks | **accounting A1, A3, A4, A11** ↔ pm-assist **A5**, **B6** | **SPLIT** | Statutory clocks = FACT, **owner = accounting** (finest grain: four separate values, including the file-or-hold decision window no other seat asks). pm-assist A5 bundles day-of-notice, notice type, cure period, and pre-filing requirements into one question and holds pointers. pm-assist B6's OTHER two components — the no-payment-no-contact PM alert day and the portfolio delinquency target — are pm-assist-OWNED and have no accounting counterpart. |
| SEAM-32 | Security-deposit holding rules | **accounting A7, A8, A9, D3** ↔ pm-assist **A7** | **FACT** | **Owner = accounting** (finest grain: separate-account requirement plus disclosure duty, interest, cap, and the actual account state, as four questions). pm-assist A7 asks how deposits must be held *and* the disposition deadline in one question: its holding half points here, its deadline half points at SEAM-1. One question, two pointers, no copies. |

**Seam tally for this seat: 21 rows — 8 joined, 13 minted. By class: 9 FACT, 6 POLICY, 5 SPLIT,
1 FACT-disjoint (SEAM-30).** Both seams the contract names explicitly are addressed by id: the
four-way SEAM-11 is verified as four-way and extended to five, and the B14/C6 accounting↔pm-assist
seam is split into SEAM-21 (B14) and SEAM-22 (C6) so the QA cross-check has an addressable row for
each. The SEAM-1 pre-ruling is recorded as MIGRATION-READY, exactly as instructed.

**No append-class seam in this seat.** SEAM-14 (cross-seat owner-append, the vendor roster) has no
accounting analogue — this questionnaire asks for no roster, and D2's account inventory is
accounting-owned rather than appended. Stated because absence of an append is a fact the engine's
§ 4c machinery needs, not an omission.

---

## 8. Coverage proof

- **Source side: 46/46 questions mapped, zero UNMAPPED.** Group counts verified fresh against the
  frozen kit doc: A=17, B=13, C=7, D=9.
- **Destination side: 73 slots, 71 sourced, 2 NO-SOURCE — both named, both with a reason and a
  proposed cross-seat owner. Zero bare flags.** Slots = 58 placeholder types + 13 non-placeholder
  `accounting-config.json` entries + 2 `config.json` literal keys.
- **Placeholder split: 58 types / 160 sites = 2 framework (4 sites) + 5 cover sheet (19 sites) +
  51 questionnaire (137 sites).** Every arithmetic total re-derived, not carried.
- **RUNTIME-PRESERVED: 0**, swept for explicitly and recorded as a PROVEN negative — the identical
  sweep finds the known `{{CTX_ROOT}}` instance in the maintenance template. Nothing reclassified,
  no count moved.
- **Citation coverage: 156/160 same-line**, the 4 exceptions being comment-forbidding JSON with a
  file-level `_placeholder_sources` object. Re-derived independently; matches assembly V5 exactly.
- **Cover-sheet fields: 4**, all four USED by this template — no fifth field minted, and the one
  gap (day mode) is resolved as a cross-seat pointer rather than an invented question.
- **Conditional gates (C!): 12 answer-armed, plus 1 structural confirmation rule.** Answer-armed:
  A4 notice wording, A5 partial-payment working rule, A7×D3 deposit-holding compliance, A10
  NSF chargeability, A14 state-1099 check, B2 dual authorization, B5 statement-hold arming, B10
  statement release, B13 Deposit Packet review gate, C4 UNRESOLVED-backup flag, C7 verifier-≠-
  processor, D5 suspense destination, D6 board/log existence, D9 year-end readiness — grouped to
  12 by folding A7×D3 into one gate and D6's two surfaces into one. Structural rule: any Group A
  value with `confirmed:false` disables its dependent clock. The assembly report groups the same
  set into 6 rows; the difference is grouping, not disagreement.
- **Never-graduate gates: 7**, structural and answer-independent, verified present in
  `copilot-thresholds.json:never_graduate[]`: `money_movement`,
  `ledger_posting_or_adjustment`, `trust_transfer`, `reconciliation_signoff`,
  `deposit_disposition_send`, `vendor_banking_change`, `external_financial_send`. Plus three
  doctrinal prose rules — no commingling, no cross-owner borrowing, statements never release over
  an unreconciled trust account. **Verified by grep: no mapping row in this table, and no
  placeholder anywhere in the tree, targets `never_graduate[]`** — the only two placeholders in
  `copilot-thresholds.json` are `{{agent_name}}` and `{{org_name}}`. No answer can graduate a
  never-graduate gate in this seat, and a row that would is a defect in the row.
- **Phase-zero flag sites: 4** — D3 (deposit trust not separate while A7 requires it), D5 (no
  suspense account), D6 (no board and/or no decision log), D9 (no 1099 tracker).
- **Weakest mappings, flagged honestly rather than buried:** **A17** (S-only array, and it is the
  SHAPE of Group A rather than one value — nothing enforces per-jurisdiction clocks today);
  **D4** (a per-account reality in a scalar boolean — reports a fraud control as present when it is
  partial); **B11** (S-only, five nulls); **B12** (a role asked, a value written, and its recording
  surface can be phase-zero); **D2** and **D7** (S-only arrays, correctly so); **B3**'s override map
  (S-only, maintenance B1-override precedent).
- **Board (B) destinations** listed for completeness. Board wiring remains out of scope for this
  pass, same as every prior table.

---

## 9. seat-config shape — delta from the maintenance and turnover proposals

Same top-level shape (`{seat, company, answers: {A1..D9 raw text}, derived: {...}, provenance}`),
raw answers ALWAYS preserved verbatim beside derived values so re-mapping never needs re-asking.

The accounting draft already implements most of it, under the name `accounting-config.json`
(AF-1). Deltas this table requires:

- `state_rules{}` — per-value `confirmed` booleans. Already present and correct: **unanswered is
  not defaulted, and unconfirmed is not acted on.** This is the single most load-bearing convention
  in the tree and it should survive into every future seat.
- `state_rules.jurisdiction_statute_map[]` — must become the KEY the Group A values are indexed by,
  not a sibling array beside sixteen scalars. Today it is a sibling. See AF-7.
- `chargeback_gates{per_line, per_unit}` — deliberately NOT under `thresholds{}`, so no
  configurator confuses B13 with B1 by key adjacency. Already correct; keep it.
- `cross_seat{}` — pointer records `{value_name: {owner_seat, owner_question_id}}` for the FACT
  seams, `held_pending_seat` where this seat holds an absent owner's value, and — new here —
  `migration_pending` + `migration_trigger` + `migrates_to` for SEAM-1. A pointer that is *ready to
  become ownership* is a third state, and neither "pointer" nor "owner" records it.
- `cross_seat_checks[]` — POLICY and SPLIT pairs for the contradiction report, eyeball never
  auto-unify. **Must carry a TYPE that distinguishes must-match FACT assertions from
  may-differ POLICY pairs**, and SEAM-27 needs a third: an ORDERING assertion. Today the schema has
  one type and B13 is filed under the wrong one (AF-2).
- `never_graduate[]` — the 7 structural gates, written regardless of answers. Present and correct.
- `federal_constants{}` — a class of its own, correctly separated from company values so no skill
  hardcodes them and a change lands in one place. Worth graduating into the shared schema; every
  seat will accumulate some.

---

## 10. Golden fixture + validation record

**File:** `outputs/ridgeline-accounting-answers-2026-08-25.md` (447 lines).

Company: **Ridgeline Residential Management** — the same fictional company as sealed scenario 1
(`editions/maintenance/ridgeline-maintenance-answers.md`), reused so cross-seat fixtures
cohere. Carried forward and verified consistent: 186 doors, Pine Basin and Cedar Mesa markets,
Class B and C, `America/Denver`, 30-calendar-day deposit deadline, LedgerPeak as the accounting
system, WorkTrail as the maintenance platform, Morgan Vale (Maintenance Supervisor), Ellis Shore
(Portfolio Director), **Avery Moss (Accounts Payable)**, Juniper Holdings and Northstar Homes as
the two override owners, and the `@ridgeline.example` mail domain.

Avery Moss is the point of the carry-forward, not a decoration: maintenance C7 already names her
as the invoice-payment executor and turnover D6 as the deposit-disposition executor. Accounting C3
names the same desk, which is what makes SEAM-18 resolvable rather than merely adjacent.

New fictional people minted for roles no prior seat has: **Harlan Beck** (principal broker, C2 and
C7), **Marisol Quill** of Quill and Associates (eviction attorney, C5), **Devin Marsh** of Marsh
Tax Partners (CPA, C6). New fictional institutions: **Basin Trust Bank**, **Cedar Mesa Community
Bank**, the **Basin State Real Estate Commission**, and the **Basin Residential Landlord and Tenant
Act**.

**V9 rule honoured:** no leasing or turnover golden UNIT name is reused. Verified by grep for
`PB-[0-9]` / `CM-[0-9]` / `ALL-[0-9]` across the fixture — zero hits. This seat's answers are
portfolio- and account-level, so no unit names were needed at all.

Built PROGRAMMATICALLY from the frozen kit doc — only the `Answer:` lines were written and the
cover-sheet block inserted — so question text is byte-identical **by construction, not by care**.

### What the fixture deliberately exercises

Six things a clean-looking fill would hide:

1. **The B1 / B2 / B14 three-money-gates same-shape trap** (contract-named; turnover C7 precedent).
   Every money number in the fixture is DISTINCT, across every seat, so any mis-route produces a
   visibly wrong number rather than a silently equal one:
   B1 vendor-bill approval **$375** · B2 dual authorization **$1,500** · B3 reserve floor **$400**
   (overrides $650 / $250) · B4 unidentified-payment escalation **$550** · B5 variance split
   **$40** · B6 variance alert **$10** · B13 chargeback **$150 / $400**.
   Against the sibling fixtures: maintenance B1 $450 (overrides $700 / $300), maintenance B2
   $1,200, turnover C1 $500 (overrides $750 / $350). **Eleven money numbers, eleven distinct
   values.** B4 was set to $550 rather than the questionnaire's suggested $500 for exactly this
   reason, and the fixture says so inline so no reviewer "corrects" it back into a collision.
2. **SEAM-20's must-match discipline.** B13 records **$150 / $400** — the same numbers turnover C7
   carries — with an explicit confirm-match note and no new number set, which is what B13's own
   text demands. A configurator that mis-routes B13 into `{{vendor_bill_approval_threshold}}`
   produces $150 where $375 belongs: visibly wrong.
3. **SEAM-26's adjacency trap.** B3's overrides ($650 / $250) differ from BOTH maintenance B1's
   ($700 / $300) and turnover C1's ($750 / $350) for the same two owners. Correct, not a
   contradiction — a cash floor and two spend authorities — and the fixture says so inline.
4. **A17 as a shape, not a value.** A5 is answered **differently for the two jurisdictions**, and
   only one half is counsel-confirmed. Pine Basin: partial payment voids the notice,
   `CONFIRMED=true`. Cedar Mesa: `CONFIRMED=false`, so the questionnaire's own safe working rule
   stays armed there. One scalar placeholder cannot hold both, which is the A17 weakness made
   concrete instead of asserted.
5. **Unanswered is not defaulted.** A14 is left `CONFIRMED=false` pending the CPA, so the
   state-1099 check is DISABLED and reported disabled — while the federal January 31 obligation,
   a FEDERAL-CONSTANT, proceeds unaffected. Two branches of the same year-end, correctly split.
6. **Phase-zero interlocks that bite.** D6 answers that the board EXISTS but the PM decision log
   does NOT, and D9 that no 1099 tracker exists. That leaves B12's waiver authority with no
   recording surface — a policy whose dependency is phase-zero — and the fixture states the
   interlock inline rather than leaving it to be discovered at the first waiver. D4 additionally
   answers positive pay as PARTIAL (three of four accounts; the bank does not offer it on
   deposit-only trust accounts), which is the honest answer the scalar placeholder cannot hold.

### Validation run (all read-only; the fixture is the only file written)

| # | Check | Result |
|---|---|---|
| V1 | Byte-drift: fixture minus answer lines minus continuation lines, diffed against the frozen kit doc | **PASS**, real `diff` exit 0 — frontmatter and every line from the questionnaire title onward byte-identical; the only added content is the cover-sheet block between them |
| V2 | All 4 cover-sheet fields present and filled (no residual underscores) | **PASS** 4/4 |
| V3 | 46 question ids, 46 `Answer:` lines, none blank or unfilled | **PASS** 46/46 |
| V4 | Each question followed by exactly one answer before the next question | **PASS**, 92-element Q/A alternation |
| V5 | Group counts A=17 B=13 C=7 D=9 | **PASS**, matches the kit doc |
| V6 | Continuation-indent path exercised | **PASS — 46/46 answers are multi-line.** See the note below |
| V7 | Parse to `{id: answer}` by the `answers-format.md` rules; 46 non-empty joins | **PASS** 46/46, zero empty, continuation-join clean |
| V8 | Fictional-only scan restricted to answer text (real orgs, real people, real platforms, fleet names) | **PASS — ZERO hits** across 160 answer-text lines |

**V6 closes a stated gap in the corpus, deliberately.** The turnover table recorded, honestly, that
neither fixture in the corpus exercised the two-space continuation-indent rule that
`answers-format.md` specifies, because every answer was single-line. This fixture wraps every
answer at 94 columns, so all 46 exercise it and the join is asserted by V7. That gap is now closed
on the fixture side. It remains open on the parser side until the real parser exists (below).

### Mutation proof that the checks have teeth

Planted against scratch copies; the deliverable was never mutated. Each mutation was killed, and
the real fixture passes as a control:

| Mutation | Expected killer | Result |
|---|---|---|
| Blank B13's answer back to underscores | V3 | died, exit 1 |
| Delete a cover-sheet field (`Timezone`) | V2 | died, exit 1 |
| Delete the whole D9 question + answer pair | V3 + V5 | died, exit 1 |
| Drift one word of A6's question text (`return` → `refund`) | V1 | died, exit 1, named the drifted line |
| De-indent one continuation line | V1 | died, exit 1, line-count 169 vs 168 |
| *(control)* unmutated deliverable | none | passes, exit 0 |

Recorded because it is the honest shape of the run: the continuation mutation was planted
**badly the first time** — a `sed` pattern that matched no line — and the suite reported exit 0.
That exit 0 was a bad mutation, not a gap in the check. Re-planted correctly against a real
continuation line, V1 killed it. A mutation that does not mutate proves nothing, and reporting the
first result as a passing check would have been reporting a hollow negative.

### Validation gaps — stated, not papered over

1. **The contract's "parses clean through the scenario-1 parser" could not be executed: that parser
   is still not on disk.** Both sibling passes recorded the same finding today and searched for it
   by filename, content signature, and git log. What was done instead: V7 parses the fixture to the
   rules stated verbatim in `editions/maintenance/answers-format.md` and asserts the 46+4
   counts by name. **That is a format-conformance proof, not a parse proof.** The parse proof is
   owed the moment Lane 1's parser lands, and it is a real remaining gate, not a formality.
2. **No fixture in the corpus has been through the engine.** This fixture, the turnover fixture,
   and the leasing fixture are all validated against the format spec rather than against the
   applier. Three format-conformant fixtures are not evidence that the applier accepts any of them.

---

## 11. Draft-tree defects — FLAGGED, not fixed

Per the contract's authority-defect rule, and per the flag-and-copy discipline the accounting
assembly's own QA deviation note established. **Nothing under `outputs/templates-drafts/` was
modified by this pass.** Ordered by how silently each fails.

| # | Defect | Where | Why it is silent |
|---|---|---|---|
| **AF-1** | The structured-answers artifact is named **`accounting-config.json`**, not `seat-config.json`. Zero occurrences of `seat-config` anywhere in the tree; the sibling **pm-assist draft uses `seat-config.json`**, the L2 taxonomy defines the S code as `seat-config.json`, and the engine contract § 4a names `seat-config.json` as the file whose schema adopts the cross-seat doctrine. | tree-wide; the artifact at `accounting-seat/accounting-config.json` | **The sharpest defect in this seat.** An applier keyed on `seat-config.json` finds no such file, writes nothing, and errors nowhere — a configured accounting agent boots with 55 unsubstituted placeholders and a doctrine block explaining that unsubstituted means DISABLED, so every check reports itself correctly disabled and the install looks like a cautious success. Two sibling seats built the same night disagree on the filename, which is the tell. Resolution is an engine/naming decision above this pass: either the engine resolves a per-seat config filename, or the seats converge. Not fixed here. |
| **AF-2** | `cross_seat_checks[0]` types the **B13 ↔ turnover chargeback** pair as `"type": "POLICY"` with `"rule": "Must match."` | `accounting-config.json:118-122` | A must-match pair is a FACT. POLICY means *may legitimately differ, surface and never unify* — so a real B13/C7 mismatch is reported as an accepted divergence and nobody resolves it. Internally inconsistent too: the same value appears in `cross_seat{}` with a pointer and `held_pending_seat: true`, which is FACT shape. One value, two doctrines, and the looser one wins at read time. |
| **AF-3** | `config.json` carries **literal** `day_mode_start: "08:00"` / `day_mode_end: "17:00"` with no cross-seat pointer. `_placeholder_sources` documents them as NO-SOURCE but names no owner. | `config.json:10-11,41-42`; `SOUL.md:220` | Maintenance **B8** is the only question in the entire kit that asks the external-communications window (SEAM-19; leasing X2 resolved the identical situation with a pointer, explicitly refusing to mint a duplicate field). Two seats installed for one company will run different day-mode windows with no error and no marker. The literal is also a *correct-looking* value, which is worse than an empty one. |
| **AF-4** | The assembly report's § 3 table is titled *NO-SOURCE defaults* but conflates five classes across 13 rows; only 2 are NO-SOURCE. | `outputs/sa-accounting-assembly-report.md` § 3 | Report-level, not tree-level — every literal in the tree is correct and correctly placed. It matters because the mapping pass is told to consume that table as its work list: a reader who trusts the title schedules eleven questions that should not exist, including three federal statutes. Full re-classification in § 4. |
| **AF-5** | `{{positive_pay_enrolled}}` is a scalar boolean for a question whose real answer is per-account. | `ONBOARDING.md:159`, `SYSTEM.md:21`, `accounting-config.json:93` | Positive pay is a check-fraud control. A partial enrolment — common, since many banks do not offer it on deposit-only trust accounts — collapses to `true` and the seat reports a fraud control as present over an unprotected trust account. Same weak-mapping CLASS as turnover B2, but the consequence is a control, not a target. The golden fixture answers it honestly and the scalar cannot carry the answer. |
| **AF-6** | The B13 pointer records `"owner_question_id": "turnover:C-group deposit chargeback"` — a prose label, not a question id. The actual id is turnover **C7**. | `accounting-config.json:113-114` | Engine contract § 4b resolves pointers by `{owner_seat, owner_question_id}`. A prose label does not resolve; the lookup fails, and the documented fallback for an unresolvable owner is to hold locally with `held_pending_seat`, which is already `true` — so the failure is indistinguishable from the normal absent-owner path and the seat silently keeps holding a value whose owner is installed. |
| **AF-7** | `state_rules.jurisdiction_statute_map` (A17) is a sibling array beside sixteen scalar Group A values, not the key those values are indexed by. | `accounting-config.json:38` | The report already calls A17 the weakest surface; this is the mechanical reason. Sixteen statutory clocks are structurally per-company while the portfolio is per-jurisdiction, and nothing errors when a two-jurisdiction portfolio is configured — the first jurisdiction's answers simply become the company's answers. The golden fixture's A5 split makes it reproducible. |

Also observed and NOT flagged as defects, recorded so the QA seat does not re-derive them: the
`chargeback_gates{}` placement outside `thresholds{}` is deliberate and correct; the four uncited
placeholders in comment-forbidding JSON are correctly handled by `_placeholder_sources`; the
HEARTBEAT Step-3 money-critical sweep ahead of the task queue is a deliberate and defensible
divergence from the maintenance shape; and the `confirmed:false` default on Group A is the best
convention in the tree.

---

## 12. Requirements this pass surfaces for the engine

The engine extension contract (`glue-engine-extension-contract-2026-08-25.md`) already covers the
applier skills-walk (§ 1), K-rows for literal config keys (§ 2), the fail-closed timezone K-row
(§ 3), and cross-seat pointer/append machinery (§ 4). This seat is consistent with all four and
adds three requirements none of them covers. Each fails SILENTLY today.

1. **Per-seat config filename resolution, or a converged name (AF-1).** The engine's § 4a names
   `seat-config.json`. This seat's file is `accounting-config.json` and the sibling pm-assist seat's
   is `seat-config.json`. Two of the five seats disagree. Until this is decided, a mapping's S
   destinations are not addressable, and the failure mode is a clean-looking install.
2. **`cross_seat_checks[]` needs THREE assertion types, not one.** `FACT_MATCH` (must match; a
   mismatch is an error to resolve at the owner — B13/SEAM-20), `POLICY_DIVERGE` (may differ;
   surface, never unify — SEAM-8, SEAM-11, SEAM-12, SEAM-17), and `ORDERING` (a ≤ b constraint
   between two seats' dates — SEAM-27, where equality is wrong and difference is fine but reversal
   ships an owner a pack referencing a statement that does not exist). One type cannot express
   these, and today the one type is silently applied to a must-match pair.
3. **A pointer that is READY to become ownership is a third state (SEAM-1).** `{owner, pointer,
   held_pending_seat}` cannot record "maintenance A3 owns this today, accounting A6 owns it the
   moment this seat lands in `templates/`." Recording it as a plain pointer loses the readiness;
   recording it as ownership migrates early and produces two owners. Requirement:
   `migration_pending` + `migration_trigger` + `migrates_to` on the pointer record, and a
   promotion-time check that performs the flip in ONE edit rather than leaving both seats holding.
   The contract instructed this state be recorded; the schema has nowhere to put it.

Additionally, and specific to the K-row surface: this seat needs K-rows for
`config.json:day_mode_start` and `config.json:day_mode_end` **that resolve through a cross-seat
pointer to maintenance B8** rather than through a local answer — a K-row whose value comes from
another seat. § 2 defines K-rows as taking a derived local value; § 4b defines pointer resolution
for S values. The intersection is undefined, and AF-3 sits exactly in it.

---

## 13. Contract compliance

Deliverables, both on disk as produced:

- `mapping-tables/accounting.md` — this table
- `outputs/ridgeline-accounting-answers-2026-08-25.md` — the golden fixture, 447 lines

Two files written, nothing else. `outputs/templates-drafts/` read-only (grep and JSON walk only);
`templates/` read-only (the RUNTIME-PRESERVED control sweep only); the kit docs opened read-only
and byte-unchanged — the cover sheet is an answers-FILE addition, exactly the maintenance
precedent. No build, no configurator run, no `add-agent`. Every cross-seat reference is by question
id against a frozen kit doc; neither the pm-assist worker's in-flight table nor its draft
`seat-config.json` content was read or cited for mapping decisions (the filename was observed by
`ls`, which is what AF-1 rests on). Draft-tree defects are FLAGGED in § 11 and none was corrected.

Next: the mapping QA reviewer's mapping-table QA seat — including the B14/C6 cross-check (SEAM-21 + SEAM-22) and the
four-way SEAM-11 verification, which this pass verified and extended to five — then orchestrator reviewer eyeball,
then this table feeds the schema-v2 engine.
