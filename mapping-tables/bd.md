# AscendOps PMAgents glue: BDM questionnaire → BD/BDM seat MAPPING TABLE (draft for mapping QA reviewer QA, then orchestrator reviewer eyeball)

Worker: m-bd (sixth seat). Contract:
`outputs/mapping-contracts-accounting-pmassist-2026-08-25.md`, section **M-BD** + its
**M-BD ADDENDUM (~1300Z)** + the inherited L2 shared rules block
(`outputs/glue-lane2-contracts-2026-08-24.md`) + the **PARALLEL-MINTING RULE**.
Status: **DRAFT** — mapping QA reviewer QA seat, then orchestrator reviewer eyeball, then the table feeds the engine.
**Mapping schema: v2**, consuming surface = the **E3 extension**
(`outputs/glue-e3-extension-contract-2026-08-25.md`), whose **capability 6**
(quoted-promise severity + fill-exempt blocks) was cut *from* this seat's assembly pass and
is discharged by name in §11.

**Sources read TODAY, and what each was used for**

| Source | Used for |
|---|---|
| `private source-questionnaire archive` (42 Q, groups A–D) | The source side. **FROZEN — opened read-only, zero bytes written.** |
| `outputs/templates-drafts/bd-seat/` (67 files, 19 root, 40 SKILL.md) | The destination side. Census re-derived **fresh by grep**, then diffed against the assembly report (§2). Re-derived a **second** time after the mid-pass banned sales acronym clean (§7). |
| `outputs/sa-bd-assembly-report.md` | Pre-seeded work list: §4 census, §5 NO-SOURCE (N1–N16), §6 mapping-forward table, §8 seams BD-1…BD-15, §9 findings, §11 open items. **Verified before consumption, not trusted as counts.** |
| `mapping-tables/maintenance.md` | Pattern authority: structure, destination taxonomy, cover-sheet precedent. |
| `mapping-tables/leasing.md` (incl. the **X1 QA amendment**), `mapping-tables/turnover.md`, `mapping-tables/pm-assist.md` (incl. both QA appendices), `mapping-tables/accounting.md` | Seam-register reconciliation by question id (§8), and the settled id ranges (accounting 20–32, pm-assist 33–37). |
| The five Ridgeline fixtures on disk (maintenance, leasing, turnover, pm-assist, accounting) | Established entities for fixture coherence, and the **SEAM-11 six-way verification** and **BD-1 / BD-2 delivering-seat values** — read, not remembered (§8.1, §9.2). |
| `outputs/glue-e3-extension-contract-2026-08-25.md` | The consuming surface. Rows cite its six capabilities (§11). |

**Rule (two-direction, from the maintenance pattern, non-negotiable):** every question gets a
destination or an explicit UNMAPPED-AND-WHY; every template placeholder gets a source or an
explicit NO-SOURCE flag. Both directions proven in §12. The census is the deliverable.

**Read-only bindings honoured:** kit docs frozen; draft tree read-only — **every defect found in
the draft is FLAGGED in §10, never corrected**. No build, no configurator run, no `add-agent`,
no writes outside the two deliverable paths.

**Elevated PII bar (this seat's contract):** the fixture contains **fictional prospects ONLY**.
Verified in §9.4 with a named search surface, not asserted.

---

## 1. Destination taxonomy

Reused verbatim from the maintenance table. No new codes invented.

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct `{{...}}` substitution at configure time |
| K | config key by path | `config.json` / `seat-config.json` key set to the derived value (E2 capability 2) |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board tab | The BDM Pipeline Board workbook tab — SECONDARY, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behaviour (not just a value) |

---

## 2. Placeholder census — FRESH, and diffed against the assembly report

Derived today by `grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}'` over the whole draft tree, twice: once
before and once after the mid-pass banned sales acronym clean (§7). **Both runs identical.**

**Fresh totals: 20 types / 108 sites.**
**Assembly report §4 claim: 20 types / 108 sites. → MATCH on both totals. Two instruments agree.**

Tree shape also re-derived and matching: **67 files, 19 root, 40 `SKILL.md`.**

### 2.1 The one mismatch, at sub-total grain — and why it is two defects, not one

The report's §4 sub-heading reads *"Question-sourced (14 types, 92 sites)"*. Its own table under
that heading lists **14 rows summing to 93 sites**. Two separate problems:

1. **An arithmetic slip.** 43+15+11+5+4+2+2+2+2+2+1+1+1+2 = **93**, not 92. Same defect family as
   the pm-assist table's **F-PM-6**. → **F-BD-6** in §10.
2. **A classification error inside the same table.** The 14th row is `{{company_name}}` (2 sites)
   and its own Question column reads *"cover sheet"* — a cover-sheet field filed under
   *question-sourced*. **No BDM question asks the company name.**

**This table reclassifies.** Question-sourced is **13 types / 91 sites**; `{{company_name}}` moves
to the cover-sheet class where it belongs. Every downstream total in the report is correct, and
the tree is unaffected: 91 + 2 + 8 + 7 = **108**.

### 2.2 Site distribution by surface — the sharpest number in this pass

| Surface | Sites |
|---|---|
| Root files (`*.md`, `*.json`) | **37** |
| `.claude/skills/**/SKILL.md` (16 of 40 skills) | **71** |
| Total | 108 |

**65.7% of this seat's placeholder sites live inside skills files** — the highest share of any
seat mapped so far (pm-assist 43.5%). A root-files-only applier substitutes **37 of 108**.

**Zero sites in `ONBOARDING.md`.** Unlike pm-assist (32 interview-instruction sites), this seat's
onboarding names no placeholder by token. That removes the interview-instruction class entirely —
all 108 sites are **operating sites** — and it removes the one mitigation pm-assist had. See
**F-BD-2**, which is this seat's most consequential finding and is a direct consequence of this row.

### 2.3 Three types with ZERO root sites — the named test for E2 capability 1

| Placeholder | Sites | Every site | Consequence of a root-only applier |
|---|---|---|---|
| `{{esignature_tool}}` | 1 | `.claude/skills/pma-and-handoff/SKILL.md` | The agreement-send skill names a raw `{{esignature_tool}}` to the BDM |
| `{{pma_signer}}` | 1 | same file | Same |
| `{{owner_intake_form_link}}` | 1 | same file | The post-agreement email ships a raw token **to an owner** |

`{{owner_intake_form_link}}` is the strongest named test in any seat table so far: it has **one
site, in a skills file, on an owner-facing send path.** A root-only applier does not fail — it
emails a prospect the literal string `{{owner_intake_form_link}}`.

Three more types are 1-root + 1-skill (`{{onboarding_specialist}}`, `{{handoff_channel}}`,
`{{property_access_coordinator}}`, all root site = `CLAUDE.md`): a root-only applier substitutes
the routing table and leaves the skill that does the work raw.

### 2.4 The 20 types, with sites and source

**Question-sourced (13 types, 91 sites)**

| Placeholder (sites) | Source | Note |
|---|---|---|
| `{{bd_manager_name}}` (43) | **C2** | 4 root files + 12 skills. The seat's anchor value at 2.9× the next. `delegation-matrix/SKILL.md` alone carries 10 |
| `{{legal_counsel}}` (15) | **C4** | 4 root + 6 skills |
| `{{broker_of_record}}` (11) | **C3** | 4 root + 6 skills |
| `{{escalation_turnaround}}` (5) | **B12** | The turnaround quoted to an owner while a gate is open — **a promise, see §11 cap 6** |
| `{{referral_fee_payer}}` (4) | **C7** | **BD-7**, accounting seam |
| `{{pipeline_board_platform}}` (2) | **D1** | |
| `{{pipeline_board_location}}` (2) | **D1** | |
| `{{onboarding_specialist}}` (2) | **C5** | |
| `{{handoff_channel}}` (2) | **C5** | |
| `{{property_access_coordinator}}` (2) | **C6** | |
| `{{esignature_tool}}` (1) | **D4** | **skills-only, zero root sites** (§2.3) |
| `{{pma_signer}}` (1) | **A6 + D4** | **skills-only.** Dual cite because the questionnaire asks it twice — **F9**, §5 |
| `{{owner_intake_form_link}}` (1) | **D3** | **skills-only, and owner-facing** (§2.3) |

**Cover sheet (1 type, 2 sites)**

| Placeholder (sites) | Field |
|---|---|
| `{{company_name}}` (2) | Company name — `IDENTITY.md`, `SOUL.md` |

**Org-seeded pointer, NOT a cover-sheet field (2 types, 8 sites)**

| Placeholder (sites) | Source |
|---|---|
| `{{day_mode_start}}` (3), `{{day_mode_end}}` (5) | `templates/org/context.json` seed + **cross-seat pointer to maintenance B8** (SEAM-19 / leasing X2 precedent). Sites: `SOUL.md`, `soul-philosophy/SKILL.md`, `heartbeat/SKILL.md` (4) |

**No BDM question asks the outreach window.** The assembly's rejected alternatives (D7 daily call
floor, D9 review cadence) were re-checked against those questions' actual text and re-affirmed:
both are narrower scheduled windows and either mapping would silently mute the seat outside them.

**Add-agent framework values (4 types, 7 sites), uncited by design**

`{{agent_name}}` (3: `config.json`, `copilot-thresholds.json`, `GOALS.md`), `{{org}}` (2:
`SYSTEM.md`, `GOALS.md`), `{{org_name}}` (1: `copilot-thresholds.json`), `{{current_timestamp}}`
(1: `GOALS.md`). Filled by `add-agent`, not by any questionnaire.

### 2.5 COVER SHEET — the assembly's open item 3, resolved as a mapping decision

The assembly pass declined to mint `{{timezone}}` and `{{forward_email}}` and asked whether
cross-seat coherence requires all four fields (§11 item 3). **Resolved here without touching the
tree:**

| Field | Spend in this tree | Mapping resolution |
|---|---|---|
| Company name | `{{company_name}}`, 2 P-sites | P-row. Normal |
| **Timezone** | **zero P-sites** | **K-row K1, MANDATORY** (E2 capability 3 as amended 2026-08-25 ~0537Z). The value is a real `config.json` field and the seat's "local, never raw UTC" rule reads it there. **A cover-sheet field does not need a placeholder to be load-bearing** — it needs a destination, and K1 is it |
| **Forward email** | **zero P-sites, zero K-rows, zero consumers** | **NO SPEND, and that is correct.** This seat has no email-forwarding intake path: leads arrive by the board platform (D1) and the configured sources (D2). Carried in the answers-file header for install coherence only, marked as unspent |
| Org short-name | `{{org_name}}`, 1 site, `copilot-thresholds.json` | Inherited as an add-agent value in this tree, not as a cover-sheet field. Recorded so the difference from the pm-assist classification is deliberate, not drift |

**The header stays whole in the answers file** (maintenance precedent, four fields) while the tree
mints one placeholder. Fields two and three are answered by a K-row and by a documented
no-consumer note respectively. **Kit docs stay frozen; zero questionnaire edits proposed.**

And the ONBOARDING text that instructs filling two of them does not match the tree — **F-BD-3**.

### 2.6 A NO-SOURCE **value** the assembly's NO-SOURCE table does not contain

**"The speed-to-lead window" is referenced in 13 places across 10 files and has no number
anywhere.** `goals.json` (2), `IDENTITY.md`, the `heartbeat` cron prompt in `config.json` (as a
Critical alert class), `lead-intake/SKILL.md` (2), `stage-gates`, `delegation-matrix`,
`draft-release-gate` (2), `shadow-mode-calibration`, `TOOLS.md`.

- **No BDM question asks it.**
- **No `seat-config.json` key holds it** (`clocks{}` has 11 keys; none is this).
- **It is not in the assembly report's N1–N16 NO-SOURCE table.**

The seat is instructed to enforce, alert on, and escalate a clock whose value exists nowhere. The
leasing seat hit the identical gap on the tenant side and minted the cover-sheet field
`{{prospect_sla_minutes}}`. → **F-BD-1 (HIGH)** in §10, and the fixture carries the value as a
**seat-specific fifth cover-sheet field under the leasing precedent, with nowhere in the tree to
land it today** — stated as the gap it is, not papered over.

---

## 3. Per-question mapping — Group A: Company, Market, and Legal (9/9)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 door count + monthly new-door growth target | S (`_descriptive.current_door_count`, `benchmark_tier`; `activity_targets.monthly_door_goal`), I | **Pointer, not a second number:** the door count of record is turnover **B6** (SEAM-7); this seat records the profile that selects the benchmark tier. `benchmark_tier` is derived from the count, not asked — the closed vocabulary is `under_150 \| 150_to_400 \| 400_plus`. **The growth-target half is the same number D8 asks — F9**, resolved in §5 |
| A2 states + tax-record lookup **per market** | S (`markets.states[]`, `markets.tax_record_lookup_by_market{}`), **C!** | The map is per market, and the seat's own note is the gate: *a market with no lookup site is a lane that cannot run — flag it, never substitute a nearby market's site*. **C! arms/disarms ownership verification per market.** Also **BD-12** (state law, narrower than pm-assist A5–A10) |
| A3 service area boundary + minimum rent | S (`markets.service_area_boundary`, `acceptance.minimum_rent_threshold`), G, **C!** | Two gates: outside-area and under-minimum both route to `{{bd_manager_name}}` before any agreement (GUARDRAILS never-graduates row 5). Neither is ever taken without manager approval |
| A4 accepted conditions/types + above-market walk-away % | S (`acceptance.accepted_property_types[]`, `accepted_conditions[]`, `above_market_walkaway_pct`), G, **C!** | The walk-away percentage is a **threshold that arms an escalation**, not a filter the agent applies alone. `code_violation_rule` ships as a literal (never accepted without manager approval + written remediation plan) and an answer may narrow it, never widen it |
| A5 one agreement per unit or per owner + accepted entity types | S (`state_rules.agreement_per_unit_or_per_owner`, `accepted_ownership_entity_types[]`), G, **C!** | Legal. Empty or "confirm with counsel" ⇒ **lane not live** per `state_rules._unconfirmed_rule`. The entity must match the tax record; a mismatch stops execution (GUARDRAILS red-flag row 8) |
| A6 company signer + required disclosures | **P `{{pma_signer}}`** (1), S (`state_rules.company_signer_requirements`, `required_disclosures_at_signing[]`, `fee_disclosure_rules`), G | **Asked twice — A6 and D4 — F9.** The tree already carries the dual cite `<!-- A6, D4 -->`. Mapping rule stated in §5: **ask once, surface a difference, never average or silently pick** |
| A7 deposit limits + handling | S (`state_rules.deposit_limits_and_handling`) as a **POINTER**, G | **BD-3 / SEAM-1. Owner = maintenance A3** today. BD's own angle is takeover-specific and is BD-owned: *never accept liability for a deposit not collected and not verifiable*. See §8 for the migration-pending state the accounting pass set |
| A8 fair housing confirmations + age/student | S (`state_rules.fair_housing_confirmations`, `age_or_student_restriction_answer`; `compliance._cite`), **G**, **C!** | **BD-11 — the one seam where all seats must agree, and the check is for a *weaker* statement, not for difference.** The rule with no approver: an owner expressing a protected-class preference is declined, always. **An answer here can only narrow the screening-criteria script; it can never unlock a preference** |
| A9 data retention requirements | S (`state_rules.record_retention{}`), **C!** | Board defaults ship as literals (won permanent / lost 12 months / duplicates 30 days — **N12**). K-row K9 overwrites **per answered key** and leaves unanswered keys intact **plus the unconfirmed mark**. Unconfirmed ⇒ the archive/delete automation is **not live** |

---

## 4. Per-question mapping — Group B: Pricing, Fees, and Authority (12/12)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 tier names + monthly fee range | S (`packages.tier_names[]`, `monthly_fee_by_tier{}`), B | Tier names feed the board's Package dropdown. **BD-8** (what BD quotes must equal what accounting bills) |
| B2 one-time setup fee | S (`packages` — **no key exists**, see F-BD-4) | Quoted in the pricing presentation and collected at handoff. **The shipped `packages{}` object has no `setup_fee` key.** Flagged, not fixed |
| B3 maintenance reserve per property | S (`packages` — **no key exists**, F-BD-4) | Presented as "your money, not a fee". **BD-18 (new)**: grain seam against pm-assist B5 / bookkeeping B3 owner reserve floor — **per property here, per unit there.** Numerically comparable, semantically not |
| B4 top package cost + guarantee programs | S (`packages.top_package_included_programs[]`), **C!** | **Programs are a closed list of what the company actually runs.** A program absent from the answer is a program the agent never references, at any stage. The generic script's four examples are not defaults |
| B5 placement/leasing fee + leasing guarantee | S (`packages` fee — **no key exists**, F-BD-4; `packages.leasing_guarantee_program{exists, markets[], terms}`), **C!** | `exists: false` is a **hard mute**, per market: the agent never references a leasing guarantee in that market at any stage. A configurator that reads `false` as "unset" and back-fills the generic program manufactures a guarantee |
| B6 protection program terms **exactly as written** | S (`packages.protection_program_terms_verbatim`), **fill-exempt candidate** | Quoted to owners word for word; **coverage is never paraphrased upward.** The block's `_note` says so. **This value belongs to the fill-exempt class (§11 cap 6b) even though it is not inside `quotable_standards`** — see F-BD-5 |
| B7 pet policy: screening, monthly fee + where it goes, damage coverage | S (`packages.pet_policy{}`), **fill-exempt candidate** | **BD-19 (new)**: the pet fee an owner is quoted is the fee leasing administers — owner = leasing. `damage_coverage: null` means the seat may not quote a coverage number. Same class as B6 |
| B8 rehab/make-ready management charge | S (`packages.rehab_management{pct_under_threshold, flat_fee_above, invoice_threshold}`) | **The $3,000 boundary between the two is never asked (N8)** — it ships as the literal `invoice_threshold: 3000` from the playbook's generic structure. Declared as a retained literal in §11, not a K-row, so its absence reads as a decision |
| B9 referral fee schedule + signed-agreement requirement | S (`referrals.fee_schedule_by_type{}`, `signed_agreement_required`), **C!** | `signed_agreement_required: true` ships as a literal and an answer may not clear it below the company rule. The 7-day unpaid alert is **N9** (from B9's hint text, not an answer field) |
| B10 maintenance authorization threshold **+ company minimum** | S (`agreement_terms.maintenance_auth_threshold`, `company_minimum_auth_threshold`), **C!** | **BD-2 — the genuinely-one-number seam.** The threshold quoted to the owner at the sale **is** the threshold maintenance enforces afterwards (maintenance B1). The second value is a **floor on negotiation**, not an operating threshold. **Two numbers that pattern-match; do not collapse them.** Exercised deliberately in §9.2 |
| B11 termination notice + satisfaction window | S (`agreement_terms.termination_notice_period`, `satisfaction_guarantee_window`) | Quote the actual clause; **never "cancel anytime"** (Never-Promise List). A promise, and therefore in the §11 cap 6 severity class |
| B12 fee-deviation / agreement-modification approver + quoted turnaround | **P `{{escalation_turnaround}}`** (5), S (`agreement_terms.fee_deviation_approver`, `agreement_language_approver`, `quoted_escalation_turnaround`), G | **The approver half duplicates C2 and C3 — F10**, resolved in §5. Only the turnaround half is new, and it is **said to an owner**, so it is a quoted promise (§11 cap 6). The two approver keys ship as the role literals `bd_manager` / `broker_of_record`, which resolve through C2/C3 — **an answer here that names a third party is a defect in the answer, not a configuration** |

---

## 5. F9 / F10 discharge — the questionnaire asks two things twice, and this is where a configurator picks silently

The assembly flagged these in a **FROZEN** kit doc and did not edit it. The mapping pass is where
they bite, exactly as the assembly predicted (§11 item 7). Rule for all three:

| Pair | Same value? | Mapping rule |
|---|---|---|
| **A1** monthly new-door growth target ↔ **D8** monthly door goal | **Yes — one number** | One destination: `activity_targets.monthly_door_goal`. **Write once.** If the two answers differ, the value goes to `flags.unresolved[]` with **both** answers and both question ids. **Never average, never take the later question.** (The seat's own GUARDRAILS row: *two sources give different numbers — carry both, name both, flag the discrepancy*) |
| **A6** who signs on the company side ↔ **D4** who executes on the company side | **Yes — one person** | One destination pair: `{{pma_signer}}` + `platform.company_side_executor`. Same rule. The tree already carries the dual cite; ONBOARDING already tells the installer to ask once and surface a difference |
| **B12** approver ↔ **C2** BD manager / **C3** broker of record | **Soft overlap** | B12's approver half **resolves through** C2/C3 (the literals `bd_manager`, `broker_of_record`). Only B12's turnaround half is an independent value. A B12 answer naming someone who is neither C2 nor C3 is `flags.unresolved[]`, not a third approver |

**Named test this places on the engine:** a fixture whose A1 and D8 answers disagree produces
**one** `monthly_door_goal` key, unset, plus a `flags.unresolved[]` entry naming A1, D8, and both
values. A mutation that writes either answer silently must die by name. Same shape for A6/D4.

---

## 6. Per-question mapping — Group C: People, Escalation, and Handoff (9/9)

| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 the BDMs on your team | S (`people.bdms[]`), B, I | Feeds the board's BDM Owner dropdown. The hint's "the owner wearing the BDM hat" case must produce a **named person**, not an empty list |
| C2 the BD manager | **P `{{bd_manager_name}}`** (43), S (`people.bd_manager`), G, I, **C!** | **The seat's anchor. BD-4 / SEAM-11 — now six-way, verified in §8.1.** Escalation target for **five of the six** never-graduates classes. **An empty C2 is PHASE-ZERO: the seat refuses to run** (`people._note`: *a gate with no name is an unrouted gate, and the seat does not run one*). The applier must treat "seat declines to start" as a **valid configured outcome**, not a failure |
| C3 broker of record | **P `{{broker_of_record}}`** (11), S (`people.broker_of_record`), G | **BD-5 — FACT: one person company-wide, and a difference is an error, not a policy.** Two fixtures already on disk disagree — see §8.2, this pass's most useful cross-check result |
| C4 legal counsel | **P `{{legal_counsel}}`** (15), S (`people.legal_counsel`), G | **BD-6 — FACT/SPLIT.** pm-assist A4 splits eviction attorney from counsel; BD asks one question covering takeovers, code violations, and fair housing. **Owner unassigned; this table proposes the split survives** (§8) |
| C5 onboarding specialist + handoff channel | **P `{{onboarding_specialist}}`** (2) + **P `{{handoff_channel}}`** (2), S (`people.onboarding_specialist`, `handoff_channel`) | **BD-10.** Named to the owner in the post-agreement email as their new main point of contact. Both types are 1-root + 1-skill (§2.3) |
| C6 property access coordinator | **P `{{property_access_coordinator}}`** (2), S (`people.property_access_coordinator`) | **BD-10.** The owner is told to expect this person's call within 48 hours — **a commitment made on another seat's behalf**, so it is in the §11 cap 6 class |
| C7 who pays referral fees | **P `{{referral_fee_payer}}`** (4), S (`people.referral_fee_payer`, `referrals.paid_by`) | **BD-7 — the accounting seam. Resolved by question id in §8.3** against bookkeeping C3 |
| C8 brokerage / investment redirect recipients | S (`people.redirect_recipients{brokerage, investment}`), B, **C!** | The board's REDIRECT lane. **"none" is a legitimate answer and must not become an empty string that reads as unset** — the closed vocabulary is `named recipient \| outside partner \| none`. An empty value is an unrouted lane |
| C9 declined-owner referral partners | S (`people.decline_referral_partners[]`), **C!** | The graceful-decline script offers these names. **An empty list is valid and must mute the referral sentence** — the script may not invent a partner. Same class as B5's `exists: false` |

---

## 7. banned sales acronym ADDENDUM — discharged, with provenance

Two injections landed mid-pass and both are discharged here rather than left in prose:

1. **~1300Z, orchestrator reviewer 1787661045833** — hold: no member-facing destination carries the acronym;
   existing draft-tree occurrences flagged pending-the-ruling, not resolved.
2. **owner-direct ruling, same session** — **the hold upgraded to PERMANENT.** Acronym dropped
   everywhere member-facing; plain-language technique description is the permanent form. The
   draft tree was cleaned by mapping QA reviewer before this table was written.

**What this pass actually measured, both sides of the clean:**

| Instrument | Before the clean | After the clean |
|---|---|---|
| `grep -ric 'banned sales acronym'` over the tree | **10 hits across 7 files** — 2 spelled-out acronym (`SOUL.md:27`, the skill's own body) and 8 as the skill name `question-led-selling` (directory, frontmatter `name`, a `triggers` token, and 5 cross-references from `CLAUDE.md`, `AGENTS.md`, `TOOLS.md`, `discovery-call`, `pipeline-metrics-and-review`) | **0** |
| Skill directory | `.claude/skills/question-led-selling/` | `.claude/skills/question-led-selling/` |
| `SOUL.md` method paragraph | named the acronym | *"built on question-led, low-pressure selling"* — generic |
| Placeholder census | 20 types / 108 sites | **20 types / 108 sites — unchanged** |
| Dangling-skill sweep | — | **rename is complete: 7 references, all resolving to `question-led-selling`; zero `banned sales acronym` tokens remain.** Verified independently, not relayed |

**Provenance for the zero:** this table cites the owner ruling as delivered in the M-BD session
injection. **No mapping row and no fixture answer in either deliverable places the acronym in any
destination**, member-facing or otherwise; §4/§6/§8 describe the method generically. The
`{{...}}` census is unaffected because the acronym was never a placeholder.

**One residue worth a QA line, stated not resolved:** the SA-BD assembly report
(`outputs/sa-bd-assembly-report.md` §11 item 9 and §7a) still names the acronym as an open
attribution question. That report is a **mapping QA reviewer/orchestrator reviewer internal artifact, not a member-facing
surface**, so the ruling does not require editing it — but a reader who consumes the assembly
report without this table would re-open a closed question. **Recommend a one-line ruling stamp on
the assembly report at the QA seat.** Not done here: it is not this pass's deliverable.

---

## 8. Cross-seat seam register — BD-prefix, formalized by question id

**Numbering, stated because the register has already collided once.** The settled ranges are
accounting **SEAM-20…32** and pm-assist **SEAM-33…37**. The contract permits **"SEAM-38+ or
BD-prefix"**. This table uses the **BD- prefix** and **deliberately does not draw SEAM-38+**, for
one reason: **the E3 extension contract already cites `BD-1` and `BD-2` by name in capability 6.**
Renumbering an id that a sibling contract cites is precisely the defect the 2026-08-25 ~0710Z
register amendment had to repair. BD-1…BD-15 are the assembly's ids, kept; **BD-16…BD-19 are new
in this pass.** Each row carries its **SEAM-n cross-reference** so the shared register can absorb
them without re-deriving.

| ID | BD Q | Other side (by question id) | Type | Resolution this table records |
|---|---|---|---|---|
| **BD-1** | **D10, D11, D12** | leasing (days to lease, marketing reach), maintenance **B5** (SLA), turnover, pm-assist **B12** | **POLICY + FACT, severity: error** | **The promise/delivery seam. Formalized in §8.4 and exercised in §9.2.** FACT half: a quoted number must equal the delivering seat's value. POLICY half: whether the seat may quote it at all. **Mismatch = configure REJECTS**, not an eyeball row (E3 cap 6a) |
| **BD-2** | **B10** | maintenance **B1**, turnover **C1**, pm-assist **B1/B2** (**SEAM-8 family**) | **FACT_MATCH — genuinely one number** | Owner-facing quote = maintenance's enforced threshold. **Plain FACT_MATCH (report severity), NOT error** — E3 cap 6a is explicit. The companion `company_minimum_auth_threshold` is a negotiation floor and is **BD-owned, never compared** |
| **BD-3** | **A7** | maintenance **A3**, turnover **A1**, leasing **B1**, pm-assist **A7**, bookkeeping **A6** (**SEAM-1**) | FACT, pointer | **Owner = maintenance A3 today.** The accounting table set SEAM-1 to **MIGRATION-READY** (flips at accounting promotion). **This table inherits that state and adds nothing**: BD holds a pointer, carries no migration trigger of its own, and BD's takeover rule (never accept liability for an unverifiable deposit) is **BD-owned and not part of the shared value** |
| **BD-4** | **C2** | maintenance **C1**, turnover **D3**, leasing **D7**, pm-assist **A2**, bookkeeping **C1** (**SEAM-11**) | **POLICY** | **SEAM-11 is now SIX-WAY. Verified against the five fixtures on disk in §8.1 — 15 pairs, not 6.** Per-seat owned; cross-check on difference, never unify. **BD's empty C2 is PHASE-ZERO**, the only arm where emptiness refuses to run |
| **BD-5** | **C3** | pm-assist **A3**, bookkeeping **C2** | **FACT — a difference is an error** | **Three-way, and two fixtures on disk already disagree. §8.2** |
| **BD-6** | **C4** | pm-assist **A4** | FACT/SPLIT | pm-assist splits eviction attorney from counsel; BD asks one question spanning takeovers, violations, fair housing. **This table proposes the split survives**: BD's `legal_counsel` maps to pm-assist's *counsel* arm, and the eviction attorney stays pm-assist-owned with no BD counterpart. Unassigned pending QA |
| **BD-7** | **C7** | bookkeeping **C3**, pm-assist **C6** | FACT | **§8.3** |
| **BD-8** | **B1–B8** | accounting (AR, owner statements), pm-assist owner reporting | FACT | What BD quotes must equal what accounting bills. **Unassigned — and it is the seam with the most surface and the least specification.** Named as an open item, not resolved |
| **BD-9** | **D1** | maintenance **D1**, turnover **E3**, leasing **D1**, pm-assist **D1** (**SEAM-15**) | FACT | **Owner = maintenance D1 for the platform-of-record inventory.** BD's board may legitimately be a **different system** — this seat records which platform carries *its own* work and does not claim the inventory. Exercised in §9 (the fixture's board is not the PM platform) |
| **BD-10** | **C5, C6** | turnover + leasing onboarding entry points | FACT | The handoff lands on people another seat also names. **C6 resolves to an established entity in the fixture — see §9.3** |
| **BD-11** | **A8** | leasing `fair-housing-guard`, pm-assist housing never-graduates | **POLICY, non-negotiable in all three** | **The check is for a *weaker* statement anywhere, not for difference.** All three carry it as the rule with no approver |
| **BD-12** | **A2, A5, A6, A9** | pm-assist **A5–A10** | FACT | BD asks a narrower set. **Owner should be whichever seat asks the widest — this table proposes pm-assist**, with BD holding pointers for the overlap and owning `agreement_per_unit_or_per_owner` + `accepted_ownership_entity_types` (no counterpart anywhere) |
| **BD-13** | **D5** | leasing prospect follow-up clocks | FACT/POLICY | **BD's prospect is an owner; leasing's is a tenant applicant. Different populations, similar clocks. A pattern-matching configurator will collapse these.** Exercised in §9.2 |
| **BD-14** | **S6 handoff → WON** | **leasing** | **structural — a lane, not a value** | **Prospect-to-applicant handoff.** BD's WON is where a property *enters* the portfolio, which is where leasing's pipeline *begins*. **Neither questionnaire describes the join.** Formalized in §8.5 |
| **BD-15** | **cover sheet** | maintenance **B8** (**SEAM-19**) | FACT | Timezone install-level; day mode owner = maintenance B8, this seat takes org seed + pointer (leasing X2). **K-ROW-THROUGH-POINTER**, §11 cap 4 |
| **BD-16** *(new)* | **D2** | **leasing D5** | **FACT/POLICY — the collapse risk BD-13 names, applied to inventories** | The contract names this pairing. **BD D2 is the OWNER lead-source inventory; leasing D5 is the TENANT inquiry inventory.** Same words, disjoint populations, disjoint destinations. **Neither owns the other; the cross-check is a *non*-match assertion** — if a configurator writes one into the other's key, that is the failure |
| **BD-17** *(new)* | **D4** | leasing (e-signature tool) | FACT | One e-signature tool company-wide is the normal shape. **Owner unassigned; a difference is a finding, not a policy.** Exercised in §9.2 as a **passing** FACT_MATCH |
| **BD-18** *(new)* | **B3** | pm-assist **B5**, bookkeeping **B3** (**SEAM-35**) | **FACT with a GRAIN DIFFERENCE** | **BD's reserve is per PROPERTY; pm-assist/bookkeeping's floor is per UNIT.** Numerically comparable, semantically not. **A FACT_MATCH typed on these two keys produces a false error on a multi-unit property.** Proposed owner = bookkeeping B3 at promotion (inheriting SEAM-35's `held_pending_seat`), with BD holding a **grain-annotated** pointer |
| **BD-19** *(new)* | **B7** | leasing (pet fee + pet policy) | FACT | **The pet fee BD quotes an owner is the fee leasing administers to a tenant. Owner = leasing.** BD holds a pointer for the fee and owns only the *owner-facing framing* (where the fee goes). A BD-side number that differs from leasing's is a mis-sale, same family as BD-1 |

**Tally for this seat: 19 seams touched — 10 FACT, 3 POLICY, 2 FACT/POLICY or SPLIT, 1
FACT_MATCH-one-number, 1 structural lane, 1 grain-difference, 1 non-match assertion.
4 new ids contributed (BD-16…BD-19). Zero SEAM-n ids minted, deliberately.**

### 8.1 SEAM-11 is SIX-WAY — verified against the fixtures, not from memory

Read from the five Ridgeline fixtures on disk plus this pass's:

| Seat | Question | Name in the Ridgeline fixture | Source |
|---|---|---|---|
| maintenance | C1 | **Morgan Vale**, Maintenance Supervisor | `editions/maintenance/ridgeline-maintenance-answers.md:92` |
| turnover | D3 | **Ellis Shore**, Portfolio Director | `ridgeline-turnover-answers-2026-08-25.md:178` |
| leasing | D7 | **Dana Wren**, Property Manager | `ridgeline-leasing-answers-2026-08-25.md:344` |
| pm-assist | A2 | **Dana Wren**, Property Manager | `ridgeline-pmassist-answers-2026-08-25.md` |
| accounting | C1 | **Ellis Shore**, Portfolio Director | `ridgeline-accounting-answers-2026-08-25.md:298` |
| **BD** | **C2** | **Rhea Calder**, Business Development Manager | this pass's fixture |

**Result: six seats, four distinct names, two agreeing pairs**
(leasing D7 = pm-assist A2; turnover D3 = accounting C1).

**Pair arithmetic, which is the whole point:** C(6,2) = **15 pairs. 2 agree, 13 disagree.**

The E3 contract's capability 5 was written against *"four-way SEAM-11 today, five-way at
promotion"* and its named test specifies **5 failing pairs** from the pm-assist table's four-seat
case. **That case is now stale by two arms.** The requirement itself is unchanged — *all* C(N,2)
pairs, every failing pair listed — but the test fixture should be restated at N=6:
**a checker that stops at the first agreeing pair reports clean on a portfolio with four
different people in the seat.** Recommended as the capability-5 named test in its current form.

**Secondary check, same method — SEAM-12 backup decision-maker:** maintenance C9 = Ellis Shore,
turnover D7 = Morgan Vale, pm-assist C5 = Ellis Shore. **BD has no counterpart question** — this
seat's escalation ladder is C2 → C3/C4 by class, with no generic backup. Recorded as a
**deliberate non-arm**, so a later pass does not read the absence as an omission.

### 8.2 BD-5 — two fixtures on disk name different principal brokers

**This is the most useful thing this pass found in the seam register, and it was found by running
the check rather than by asserting it.**

| Seat | Question | Name |
|---|---|---|
| pm-assist | **A3** | **Sloane Karr**, Principal Broker and company owner |
| accounting | **C2** | **Harlan Beck**, principal broker |

BD-5's own rule: *"Should be one person company-wide. **A difference is an error, not a
policy.**"* Two Ridgeline fixtures, produced by parallel workers who could not see each other,
name two different principal brokers for the same fictional company.

**This pass's action, per the authority-defect rule: FLAG, DO NOT FIX.** Neither fixture is this
pass's deliverable. This table's fixture answers C3 = **Sloane Karr**, matching pm-assist A3 —
which makes BD-5 **pass** against pm-assist and **fail** against accounting, surfacing the
pre-existing contradiction instead of burying it under a third choice.

→ **F-BD-8** in §10. **Fixture-merge conflict for the QA seat, not a defect in any one table**
(turnover SEAM-13 / pm-assist §7.3 precedent). Same defect family as the SEAM-20…24 collision:
shared state written by workers who cannot see each other.

**A second, lower-severity instance of the same class, noted for legibility:** the fixture set now
contains **Harlan Voss** (pm-assist A4, counsel) and **Harlan Beck** (accounting C2, broker). Two
first-name-identical fictional people in adjacent roles is a merge hazard for a reader, not a
defect. Recorded, not resolved.

### 8.3 BD-7 — the referral-fee accounting seam, resolved by question id

| Half | Owner | Question ids |
|---|---|---|
| **Who pays** the referral fee | **ACCOUNTING** (the desk) | bookkeeping **C3** (the bookkeeper of record) |
| **The board flag** that a fee is owed, and its 7-day clock | **BD** | BD **C7** → `{{referral_fee_payer}}` + `referrals.unpaid_alert_days_after_won` |
| **The fee schedule itself** | **BD** | BD **B9** — no accounting counterpart asks it |

**Resolution: no collision.** BD names the person the flag *lands on*; accounting names the desk
that *executes payment*. The value is one name and it must match — **FACT_MATCH, report
severity**. The fixture answers C7 with the entity already established across maintenance C7 /
turnover D6 / accounting C3, so the check **passes** (§9.3).

**Difference from the pm-assist B14/C6 resolution, stated so QA does not have to re-derive it:**
that seam split *resolution* from *surfacing* because two seats each owned a real half. Here there
is only one half — a name — so there is nothing to split. BD holds it as a pointer once the
accounting seat is promoted; today both seats hold it and must agree.

### 8.4 BD-1 formalized — three sub-shapes, not one

The assembly named the class. Mapping it revealed that "BD quotes what another seat delivers"
covers **three structurally different failures**, and an engine that handles only the first
produces false errors on the other two.

| Sub-shape | What it looks like | Engine behaviour required |
|---|---|---|
| **(a) Differs** | BD quotes a number; the delivering seat's config holds a different number of the **same measure** | `FACT_MATCH, severity: error` → **configure REJECTS** (E3 cap 6a) |
| **(b) No delivering owner at all** | BD quotes a standard **no seat delivers** — the counterpart key does not exist in any configured seat | **Must NOT pass as "nothing to compare".** An absent counterpart on a `severity: error` row is the *worst* case, not the empty one: the company is selling something with no operational owner. Requires an explicit `owner_absent` outcome distinct from `match` |
| **(c) Same word, different measure** | BD quotes a **response** SLA; the delivering seat holds a **completion** SLA | **Must not be typed FACT_MATCH at all.** A row that compares unlike measures manufactures an error. The mapping declares the measure, and a measure mismatch is a **mapping defect**, not a config contradiction |

All three are exercised in the golden fixture — §9.2. **Sub-shape (b) is the one the E3 contract's
capability 6 does not currently name**, and it is the one this fixture fires.

### 8.5 BD-14 formalized — the prospect-to-applicant lane

**It is not a config key, and this table does not pretend it is one.** What can be recorded:

- **The join point by stage id:** BD stage **S6 handoff → WON** is the moment a property enters
  the portfolio; leasing's pipeline begins at the same moment for a *different subject* (the
  property's units, not the owner).
- **The carried record:** the BD board's WON row and the handoff package (C5 channel, C6 access
  coordinator, D3 intake form) are the only artifacts crossing the line.
- **Neither questionnaire describes the join.** BD's D-group ends at the handoff; leasing's
  A-group begins with a unit already in the portfolio.
- **What this table asserts:** the lane needs a **named owner and a specified payload** before any
  automation spans it. Proposing one here would be inventing a workflow neither kit doc defines.

**Recorded as `cross_seat_lane`, an entry shape the schema does not yet have** — §11.

### 8.6 Money-gate family — every number in this fixture, and which gate it arms

Per the contract's explicit instruction (turnover-C7 / pm-assist B1/B2/B14 precedent), the fixture
carries **deliberate numeric collisions with inline disambiguation**. Enumerated here so a reader
can see they are designed, not accidental:

| Number | Gate | Seat | Deliberate collision with |
|---|---|---|---|
| **$450** | BD B10 maintenance auth threshold quoted to the owner | BD | **maintenance B1 base threshold — a REQUIRED match (BD-2)** |
| **$300** | BD B10 **company minimum** auth threshold (a negotiation floor) | BD | maintenance B1 **Northstar Homes override**; pm-assist B1 **Northstar override**; pm-assist **B2 coordinator spend authority** — **four gates, one number, no two of them the same thing** |
| **$500** | BD B3 maintenance reserve held **per property** | BD | turnover **C1 base make-ready reserve**; pm-assist **B14 broker trust-variance threshold** — three gates, one number |
| $295 | BD B2 one-time setup fee | BD | none |
| 50% of one month's rent | BD B5 placement fee | BD | none |
| $250 / $500 | BD B9 referral fee schedule | BD | the $500 tier collides with the $500 row above — **a fourth meaning** |

**The trap this exercises:** a configurator that pattern-matches on the word *threshold*, on the
word *reserve*, or on the value **$300** collapses a negotiation floor into a portfolio-wide
coordinator spend authority. Every colliding answer in the fixture states the trap in prose on its
own `Answer:` line, so the failure is legible the moment it happens.

**Honesty note, carried forward from the pm-assist QA amendment:** deliberate collisions are only
safe while the inline notes exist. If a later pass edits a fixture answer and drops the note, the
collision becomes indistinguishable from the accidental `$400` case that amendment recorded.
**The notes are load-bearing.**

---

## 9. Golden fixture + validation record

**File:** `outputs/ridgeline-bd-answers-2026-08-25.md`
**Company:** Ridgeline Residential Management (`ridgeline`, America/Denver) — the **same fictional
company** as the other five fixtures.

**Reused established entities where roles overlap** (read from the fixtures, not remembered):
Ellis Shore (Portfolio Director), Morgan Vale (Maintenance Supervisor), Avery Moss (Accounts
Payable), Sloane Karr (Principal Broker), Harlan Voss / Voss Legal Group (counsel), Tobin Merritt
/ Merritt and Cole LLP (eviction attorney), the Pine Basin and Cedar Mesa markets, the fictional
Basin state, WorkTrail (PM platform of record), InkPath (e-signature), the RentBasin / HomeSeeker
/ ListingHub syndication set, and the owners Juniper Holdings and Northstar Homes.

**Minted new for roles no prior fixture had:** **Rhea Calder** (BD manager), **Nika Ansell** and
**Bram Teller** (BDMs), **Tam Ruiz** (owner onboarding specialist), **Basin Ridge Realty**
(outside brokerage partner), **Cedar Ridge Property Group** and **Foothill Rentals LLC** (decline
referral partners), **PetCheck** (pet screening).

**V9 rule honoured:** the leasing/turnover golden **unit** names (Elm Court, Foster Row, Alder
Street) are not reused, and neither are the draft tree's own example strings.

### 9.1 Gate states deliberately mixed

| Gate | State in the fixture | What it exercises |
|---|---|---|
| A2 tax-record lookup per market | **Both markets named** | The map is complete, so the ownership-verification lane runs for both. The not-live path is exercised elsewhere rather than twice |
| A5, A6, A8 state law | **CONFIRMED with counsel** | Agreement-execution and fair-housing lanes live |
| **A9 retention** | **UNCONFIRMED — counsel has not answered** | **Board defaults carried as a starting point AND explicitly marked unconfirmed ⇒ the archive/delete automation is NOT LIVE.** The literal is present; the behaviour is dark |
| **B5 leasing guarantee** | **`exists: false`, both markets** | **A hard mute.** The agent never references a leasing guarantee at any stage. Proves `false` ≠ unset |
| B7 pet damage coverage | **None — Ridgeline runs no such program** | The seat may not quote a coverage number even though the generic script has one |
| C2 BD manager | **Named (Rhea Calder)** | PHASE-ZERO path **not** exercised here — it is exercised in the maintenance fixture, and re-exercising it would cost this fixture every other gate |
| C8 brokerage redirect | **Outside partner named; investment = "none"** | Both branches of the closed vocabulary in one answer |
| C9 decline partners | **Two named** | The non-empty branch; the empty-list mute is stated in the answer prose |
| **D12 eviction range** | **UNANSWERED PENDING COUNSEL** | **Fill-exempt proof #2** — §9.2 |

### 9.2 BD-1 and BD-2 exercised deliberately, with the quoted-promise severity semantics

**BD-2 — plain FACT_MATCH, and it PASSES.**

| Value | Fixture | Delivering side |
|---|---|---|
| BD **B10** maintenance auth threshold quoted to the owner | **$450** | maintenance **B1** base threshold = **$450** (`ridgeline-maintenance-answers.md:92`) |

Equality is the **correct** state for BD-2 and the fixture ships it that way, because a fixture
that only ever fires checks cannot prove a check does not false-positive. The **companion**
`company_minimum_auth_threshold` = **$300** is BD-owned and **must not be compared to anything** —
it is the four-way numeric collision enumerated in §8.6.

**Named test (E3 cap 6a):** the same pair typed `FACT_MATCH, severity: report` and mutated to
$500 on the BD side surfaces a contradiction-report row and **configures successfully**. Typed
`severity: error`, the same mutation **rejects**. Same fixture pair, two severities, two outcomes.

**BD-1 — all three sub-shapes, from real cross-fixture values.**

| Sub-shape | Fixture answer | Delivering seat's actual value | Outcome |
|---|---|---|---|
| **(a) differs — the error probe** | **D10 marketing reach: 3 syndication sites** (RentBasin, HomeSeeker, ListingHub) | leasing's syndication set = **exactly those 3** (`ridgeline-leasing-answers-2026-08-25.md:320`) | **MATCHES → passes.** Mutating the fixture's single token `3` → `90` (the generic script's "90 plus websites") makes BD quote 30× the reach the company delivers. **`severity: error` ⇒ configure REJECTS.** This is the capability-6a named test, and its input is one token |
| **(b) no delivering owner at all** | **D11 inspection schedule: move-in, 60 days, 10 months, move-out** | **No seat delivers a 60-day or 10-month inspection.** Verified by grep for `inspection` across all five fixtures: maintenance has none, turnover has only the optional pre-move-out walkthrough 1–2 weeks prior, leasing has move-in/move-out only | **FIRES.** Two of the four quoted inspections have **no operational owner anywhere in the portfolio.** A checker that treats an absent counterpart as "nothing to compare" reports clean on a promise nobody keeps |
| **(c) same word, different measure** | **D12 non-emergency response SLA: acknowledged the same business day** | maintenance **B5** holds Routine **completion** 8 days, Urgent **completion** 36 hours (`ridgeline-maintenance-answers.md:116`) | **Must NOT be typed FACT_MATCH.** *Acknowledgement* and *completion* are different measures; comparing them manufactures an error. The mapping declares the measure and the rows stay uncompared |

**Fill-exempt proof — `quotable_standards` stays empty when unanswered (E3 cap 6b).**

The contract requires this block be proven exempt. The fixture carries **three empty values, each
empty for a different reason**, so the exemption is proven against three distinct causes rather
than one:

| Key | Fixture state | Why empty | What back-fill would produce |
|---|---|---|---|
| `typical_days_to_lease` | **`""`** | **No leasing-side number exists.** The leasing fixture holds screening criteria, hold windows, and notice periods — **no days-to-lease figure anywhere.** Verified by grep | The generic hint's number becomes a days-to-lease **promise** to an owner, sourced from nothing |
| `screening_point_count` | **`null`** | Leasing runs **documented written criteria per property class**, not a point count. The company has no such number | The script's "14-point screening process" becomes a claim about a process Ridgeline does not run |
| `eviction_timeline_range` | **`""`** | **UNANSWERED PENDING COUNSEL** — the answer says so out loud | A market range quoted as fact, unconfirmed, on the topic the Never-Promise List names explicitly |

The seat's own text already enforces this in prose — `never-promise-list/SKILL.md:85-91`: *"An
empty field is not a gap to fill with the generic example. It is a claim the seat may not make."*
and the scripted line for the empty case. **`objection-handling/SKILL.md:106` says the same for
`packages`.** The engine requirement is that the applier not contradict the template it is filling.

**Named test (E3 cap 6b):** configure the golden fixture; assert all three keys are still
empty/null in the produced `seat-config.json` **and** that a named report line exists for each. A
mutation removing `fill_exempt: true` back-fills at least `typical_days_to_lease` from the hint
and **dies by name**.

### 9.3 Cross-seat checks the fixture makes PASS, on purpose

A fixture that only fires checks cannot distinguish a working checker from a stuck one.

| Check | BD value | Other side | Result |
|---|---|---|---|
| **BD-7** referral fee payer | Avery Moss, Accounts Payable | maintenance C7 / turnover D6 / accounting C3 — same entity | **PASS** |
| **BD-17** e-signature tool | InkPath | leasing's executed-lease tool = InkPath | **PASS** |
| **BD-2** auth threshold | $450 | maintenance B1 = $450 | **PASS** |
| **BD-1(a)** marketing reach | 3 sites | leasing syndication = 3 sites | **PASS** |
| **BD-10** access coordinator | Morgan Vale | maintenance C1 | **PASS** (deliberately an established entity) |
| **BD-5** broker of record | Sloane Karr | pm-assist A3 **PASS** / accounting C2 **FAIL** | **Surfaces the pre-existing contradiction — §8.2** |
| **BD-4** SEAM-11 | Rhea Calder | five other seats, four distinct names | **13 of 15 pairs disagree — §8.1** |

### 9.4 Validation record

| # | Check | Method | Result |
|---|---|---|---|
| V1 | 42/42 questions answered | `grep -c '^Answer: '` on the fixture vs blank-slot count in the frozen source | **PASS** — **42 blank slots consumed, 42 answers written.** Built by script from the frozen file so the body cannot drift by hand |
| V2 | Kit docs stay FROZEN | `diff` blank questionnaire vs fixture, then **classify every diff line** | **PASS, proven by class.** Removed lines: **42, all matching `^< Answer: ___`, zero others** (the unexpected-removal filter printed nothing). Added lines: only filled `Answer:` lines, their 2-space continuations, and the 33-line cover-sheet block. **Questionnaire body byte-verbatim** |
| V3 | Fresh census matches the tree | `grep -rhoE '\{\{[a-zA-Z0-9_]+\}\}'` over all 67 files | **PASS** — 20 types / 108 sites |
| V4 | Census diffed against the second instrument | Compared to assembly report §4 | **PASS on totals** (20/108). One sub-total mismatch + one classification error → **F-BD-6**, §2.1 |
| V5 | Census re-run after the mid-pass banned sales acronym clean | Same command, after the tree was cleaned | **PASS — identical.** §7 |
| V6 | **Elevated PII bar — fictional prospects ONLY** | Regex scan over the **255 lines of extracted answer text only** (`Answer:` lines plus their 2-space continuations, split out first so frozen kit text cannot mask a hit) over: private fleet roster names; the operator first name; org strings (`ascendops`, `AscendOps`, `Ascend Property`, `dbhconstruction`); real PM/CRM platforms (`AppFolio, Buildium, Rent Manager, Propertyware, Yardi, PropertyMeld, Salesforce, HubSpot, Follow Up Boss, Podio`); real e-sign tools (`DocuSign, Dropbox Sign, HelloSign, Adobe Sign, PandaDoc`); real listing sites (`Zillow, Trulia, Apartments.com, Realtor.com, HotPads, Zumper`); the banned sales acronym acronym; and any `@` address not ending `.example` | **PASS — zero hits, all classes.** Two further scans on the same extracted text: **zero non-`.example` email addresses** and **zero non-`.example` URLs**. Matches elsewhere in the file are frozen kit text preserved byte-verbatim by V2 (the D1 and D2 hints name spreadsheet products and generic source types), not answers |
| V7 | **Prospect names are fictional and marked** | Proper-noun-pair extraction over the answer text alone, then every result checked against the fixture roster in §9 | **PASS — 31 distinct pairs, and every one is either a role title, a defined term, or a roster entity.** Persons named: Avery Moss, Bram Teller, Dana Wren, Ellis Shore, Harlan Voss, Morgan Vale, Nika Ansell, Rhea Calder, Sloane Karr, Tam Ruiz, Tobin Merritt — 7 new fictional entities, all enumerated in §9. **Zero prospect-shaped strings that could be a real owner:** the fixture names no prospect at all, because no question asks for one. Stated rather than assumed — this seat's PII exposure is in its *runtime data*, not its *config* |
| V8 | V9 rule — no reuse of leasing/turnover golden unit names | Case-insensitive scan of the extracted answer text for `Elm Court`, `Foster Row`, `Alder Street` and the draft tree's example strings | **PASS — zero hits** |
| V9 | Two-direction proof | §12 count lines | **PASS** — 42/42 questions, 20/20 placeholders, zero bare flags |
| V10 | Read-only surfaces genuinely untouched | **Not by `git status` — the draft tree is gitignored** (`.gitignore` `private mapping workspace`), so a clean status there proves nothing. Verified by **mtime**: `find … -newermt '2026-08-25 08:29'` returns **exactly 7 files** — `SOUL.md`, `AGENTS.md`, `CLAUDE.md`, `TOOLS.md`, `question-led-selling/SKILL.md`, `pipeline-metrics-and-review/SKILL.md`, `discovery-call/SKILL.md`, all stamped 08:32–08:33. **Those are precisely the 7 files that carried the acronym (§7), rewritten by mapping QA reviewer, none by this worker.** Kit docs stamped 2026-08-20 22:41 / 23:01 / 23:16 and 2026-08-21 14:31 — none touched | **PASS** |
| V11 | Dangling-skill sweep, independently re-derived | Extracted every `.claude/skills/<name>/` reference across all files, compared against the present skill list | **ONE DANGLE — `memory`, referenced twice from `HEARTBEAT.md`.** This is the assembly's **F5, copied faithfully under the authority-defect rule.** Zero others; the `question-led-selling` rename resolves cleanly across all 7 references. **Two instruments agree with assembly V7** |
| V12 | Fixture parses through the scenario-1 parser | — | **NOT RUN — and not claimed.** Same honest position the leasing, turnover, pm-assist, and accounting passes took: the parser lives in contract-2's reconfigurator, which this worker does not run (contract: no build, no configurator run). The fixture is built to the identical format spec the five sibling fixtures use, so it should pass unchanged, but **that is an expectation, not evidence.** Re-run V12 when the engine consumes this table |

---

## 10. FINDINGS in the draft tree — FLAGGED, NOT FIXED

The authority-defect rule binds. **Zero bytes of the draft tree were modified by this pass.**

| # | Finding | Where | Verified by | Severity |
|---|---|---|---|---|
| **F-BD-1** | **A clock the seat enforces has no value anywhere.** "The speed-to-lead window" appears in **13 places across 10 files** — `goals.json` (2), `IDENTITY.md`, the `heartbeat` cron prompt as a **Critical alert class**, `lead-intake` (2), `stage-gates`, `delegation-matrix`, `draft-release-gate` (2), `shadow-mode-calibration`, `TOOLS.md`. **No BDM question asks it. No `seat-config.json` key holds it** (`clocks{}` has 11 keys; none is this). **It is not in the assembly report's N1–N16 NO-SOURCE table.** The seat alerts and escalates on a window whose number exists nowhere in the system | `grep -rn 'speed-to-lead\|speed_to_lead'` over the tree; `clocks{}` read in full; assembly §5 read in full | Three instruments: tree grep, config read, report read | **HIGH** — the leasing seat hit the identical gap on the tenant side and minted `{{prospect_sla_minutes}}`. Fix is a cover-sheet field + a `clocks` key; kit stays frozen |
| **F-BD-2** | **The shipped onboarding cannot fill 66% of this seat's placeholders, and has no fallback.** Step 9 item 1 reads *"fill every placeholder in the **bootstrap files**"* — **71 of 108 sites are in `.claude/skills/**`, in 16 files.** And unlike the pm-assist template, **`ONBOARDING.md` contains no recursive `grep` verify step at all** — zero occurrences of `grep` and zero occurrences of `{{` in the entire file. A human or agent following the shipped onboarding literally ships a configured seat with raw placeholders in 16 live skill files, including **`{{owner_intake_form_link}}` on an owner-facing send path** (§2.3) | `ONBOARDING.md:190-196`; `grep -c 'grep\|{{' ONBOARDING.md` → 0; per-file site census §2.2 | Site census + full read of ONBOARDING | **HIGH** — pm-assist's equivalent (F-PM-7) was MEDIUM *because the recursive grep mitigated it*. Here the mitigation does not exist |
| **F-BD-3** | **ONBOARDING instructs filling two placeholders that do not exist.** `ONBOARDING.md:31`: *"the timezone to `config.json` and **the timezone placeholder**. Confirm **the forward email** if the install uses one."* **`{{timezone}}` and `{{forward_email}}` appear zero times in the tree** — the assembly deliberately did not mint them (§11 item 3) but the onboarding text was not reconciled | `grep -rn '{{timezone}}\|{{forward_email}}'` → 0 hits; `ONBOARDING.md:31` | Two greps + read | **MEDIUM** — a step that cannot be completed as written teaches the installer to skip verification steps |
| **F-BD-4** | **Three answered fee values have no `seat-config.json` key to land in.** **B2** (one-time setup fee), **B3** (maintenance reserve per property), and **B5** (placement/leasing fee) are all asked, all quoted to owners, and all mapped by the assembly's §6 to `packages.*` — but the shipped `packages{}` object has **no `setup_fee`, no `maintenance_reserve`, and no `placement_fee` key.** It holds `tier_names`, `monthly_fee_by_tier`, `top_package_included_programs`, `leasing_guarantee_program`, `protection_program_terms_verbatim`, `pet_policy`, `rehab_management` — and nothing else | `seat-config.json` `packages{}` read key-by-key against Group B | Full read of the object vs the 12 B-questions | **MEDIUM–HIGH** — three prices an owner is quoted have no machine home. The applier writes them nowhere and errors nowhere |
| **F-BD-5** | **`fill_exempt` is a class, not one block.** The `quotable_standards._note` correctly says every value in it is a claim the seat may say out loud — but **`packages.protection_program_terms_verbatim`** ("quoted word for word, never paraphrased upward"), **`packages.pet_policy.damage_coverage`**, and **`packages.leasing_guarantee_program`** are the same kind of value and sit **outside** the exempt block. `objection-handling/SKILL.md:106` explicitly tells the agent to draw from **`quotable_standards` *and* `packages`** | `seat-config.json` `_note` texts; `objection-handling/SKILL.md:106`; `never-promise-list/SKILL.md:85-91` | Cross-read of the block notes against the consuming skills | **MEDIUM** — a per-block exemption that covers one of the two blocks the agent quotes from is a half-guard |
| **F-BD-6** | **Assembly report sub-total mismatch + a classification error** (report defect, tree unaffected). §4's sub-heading reads *"Question-sourced (14 types, 92 sites)"*; the table beneath lists **14 rows summing to 93**, and its 14th row is `{{company_name}}`, whose own Question column reads *"cover sheet"*. Reclassified in §2.1 to 13 types / 91 sites | `outputs/sa-bd-assembly-report.md` §4 | Two-instrument diff (fresh grep vs report) | **LOW** — stale sub-heading + misfiled row; every downstream total in the report is correct |
| **F-BD-7** | **`"timezone": ""` in `config.json`, and no `day_mode_*` key anywhere.** The turnover pass's FINDING E2 and pm-assist's F-PM-4 hold verbatim in this tree: the daemon's resolver supplies a host/org value and every clock runs in a timezone nobody chose; the day-mode window lives only in prose across 8 placeholder sites | `config.json` `"timezone": ""`; `grep -n 'day_mode' config.json` → 0 | Read + grep | **INHERITED, not new** — identical in `templates/{maintenance,leasing}-coordinator/config.json`. Claiming a new number for it would overstate. Closed by K1 + K10 in §11 |
| **F-BD-8** | **Two Ridgeline fixtures on disk name different principal brokers** — pm-assist A3 = Sloane Karr, accounting C2 = Harlan Beck. BD-5's rule is that a difference here **is an error, not a policy**. Neither fixture is this pass's deliverable, so it is flagged, not fixed | `ridgeline-pmassist-answers-2026-08-25.md`, `ridgeline-accounting-answers-2026-08-25.md:308` | Direct read of both answer blocks | **MEDIUM** — fixture-merge conflict for the QA seat (turnover SEAM-13 precedent). Same defect family as the SEAM-20…24 collision |
| **F-BD-9** | **A cron literal contradicts the answer it is supposed to carry, and the file says so itself.** `config.json` seeds `weekly-review-prep` at `0 8 * * 1` (Monday 08:00) while **D9 asks when the weekly pipeline review happens**. The file's own `_cron_note` admits the literals *"are seat defaults, not answers"* and says to re-point them at install — **but ONBOARDING contains no step that does it.** A member answering "Tuesday 09:00" gets Tuesday in every prose surface and a job that still fires Monday 08:00, with no error | `config.json` crons[1] + `_cron_note`; `ONBOARDING.md` Step 5 and Step 9 read in full — no cron re-point step | Read of both files | **MEDIUM** — exactly E2 capability 2's silent-failure class. Closed by K2 in §11 |
| **F-BD-10** | **The banned sales acronym residue in the assembly report** (report artifact, tree clean). `outputs/sa-bd-assembly-report.md` §7a and §11 item 9 still carry the acronym and describe the attribution question as **open**. The tree is clean and the ruling is permanent (§7). This is an internal artifact, not member-facing, so the ruling does not require the edit — but a reader consuming the report without this table re-opens a settled question | `outputs/sa-bd-assembly-report.md` §11 item 9 | Read | **LOW** — recommend a one-line ruling stamp at the QA seat |

**Not findings, checked and clean:** notation discipline (**zero** `{{CTX_*}}` and zero `${{...}}`;
148 shell-form runtime refs); all 42 question ids present in `ONBOARDING.md`; all **9** copilot
categories ship `"status": "locked"` with the never-graduates `_note` present and **none of the
six never-graduates classes present as a category**; `seat-config.json` contains zero `{{...}}`
(written by the interview, not substituted); root inventory 19/19, skills 40/40, files 67/67 as
the assembly claims; the `question-led-selling` rename is complete across all 7 references.

---

## 11. Requirements this table places on the engine

Cited against `outputs/glue-e3-extension-contract-2026-08-25.md` by capability, plus the E2
capabilities it builds on.

**Capability 1 (P-rows targeting skills files) — the strongest named test in any seat.**
**71 of 108 sites (65.7%) are in `.claude/skills/`.** Named test: **`{{owner_intake_form_link}}`**
— one site, in `pma-and-handoff/SKILL.md`, **on an owner-facing send path, with zero root sites.**
A root-only applier does not fail; it emails a prospect the literal token. Mutation removing the
skills walk leaves the raw token and kills the test by name. Two companion types with the same
shape: `{{esignature_tool}}`, `{{pma_signer}}`.

**Capability 1 of E3 (per-seat config filename resolution).** This seat's structured-answers
artifact is **`seat-config.json`** — the pm-assist name, not the accounting `accounting-config.json`
name. **Declared here explicitly** so the declared-name resolver has a value for this seat and the
present-but-undeclared branch cannot fire.

**K-ROWS this mapping declares** (E2 capability 2):

| K | Target | Source | Why it must be a K-row |
|---|---|---|---|
| **K1** | `config.json` → `timezone` | cover-sheet Timezone | **MANDATORY.** A v2 seat mapping without this row is rejected at load, fail-closed (E2 cap 3 as amended 2026-08-25 ~0537Z). This seat mints no `{{timezone}}` placeholder, so **K1 is the field's only destination.** Closes F-BD-7's sourcing half |
| **K2** | `config.json` → `crons[name=weekly-review-prep].interval` | **D9** | Closes **F-BD-9**. Without it the prose and the job disagree silently, and the file's own `_cron_note` becomes an unexecuted instruction |
| **K3** | `seat-config.json` → `clocks.stage_max_days.{S0…S4}` | **D6** | **Per answered key only.** `S5_warning`, `S5_escalate`, `S6` stay `null` (**N13** — D6 asks only S0–S4). An applier that defaults the unasked keys invents stage gates |
| **K4** | `seat-config.json` → `state_rules.record_retention.*` | **A9** | Board defaults (**N12**) overwritten per answered key, unanswered keys left intact **plus the unconfirmed mark that keeps the archive/delete lane dark** |
| **K5** | `seat-config.json` → `quotable_standards.*` | **D10, D11, D12** | **`fill_exempt: true`** — E3 cap 6b. See below |
| **K6** | `seat-config.json` → `packages.{setup_fee, maintenance_reserve, placement_fee}` | **B2, B3, B5** | **THESE KEYS DO NOT EXIST YET — F-BD-4.** Declared as required K-rows so the gap is a schema item, not a silent write-to-nowhere |
| **K7** | `seat-config.json` → `clocks.speed_to_lead_minutes` | **NO QUESTION — F-BD-1** | **The key does not exist and no question sources it.** Declared so the gap is visible to the engine rather than only to a reader |
| **K8** | `config.json` → `day_mode_start` / `day_mode_end` | maintenance **B8** pointer | **`value_from: pointer`** — E3 capability 4. **No such key exists in any template `config.json`** (F-BD-7). Owner-present resolves the owner value; owner-absent takes the org `context.json` seed as the **declared fallback** and records held state |
| — | `config.json` → `crons[name=daily-pipeline-run].interval` | **NO SOURCE (N5)** | **Declared as a retained literal, NOT a K-row.** D7 asks the daily call floor, not the hour. Recorded so its absence reads as a decision |
| — | `seat-config.json` → `packages.rehab_management.invoice_threshold` (3000) | **NO SOURCE (N8)** | Retained literal. **B8 asks the percentage and the flat fee; the boundary between them is never asked.** An answer may override it; nothing sources it |
| — | `referrals.unpaid_alert_days_after_won` (7), `clocks.nurture_no_touch_alert_days` (30), `activity_targets.pipeline_minimum_multiple` (3) | **N9, N10, N11** | Retained literals from hint text and board defaults. Overridable, unsourced. Declared so a later pass does not mistake them for gaps |

**`cross_seat{}` records this mapping declares** (E2 capability 4a / E3 capability 3):

```
config_artifact: "seat-config.json"          # E3 cap 1 declaration

cross_seat: {
  deposit_disposition_days: {owner_seat: maintenance, owner_question_id: A3,
                             migration_pending: true,
                             migration_trigger: "accounting seat promoted to templates/",
                             migrates_to: {seat: accounting, question_id: A6}},   # BD-3 / SEAM-1
  day_mode_window:          {owner_seat: maintenance, owner_question_id: B8},     # BD-15 / SEAM-19
  platform_of_record:       {owner_seat: maintenance, owner_question_id: D1},     # BD-9  / SEAM-15
  entry_notice_hours:       {owner_seat: maintenance, owner_question_id: A2},     # BD-12 overlap
  pet_fee_and_policy:       {owner_seat: leasing,     owner_question_id: B-grp},  # BD-19
  esignature_tool:          {owner_seat: unassigned,  seats: [bd D4, leasing D-grp]}, # BD-17
}

held_pending_seat: {
  referral_fee_payer:        accounting,   # BD-7,  bookkeeping C3
  fee_schedule_billing:      accounting,   # BD-8,  unspecified counterpart
  maintenance_reserve:       accounting,   # BD-18, bookkeeping B3 — GRAIN-ANNOTATED
}

cross_seat_checks: [
  {POLICY_DIVERGE, bd_manager_vs_pm_of_record,
     [maintenance C1, turnover D3, leasing D7, pm-assist A2, accounting C1, bd C2]},  # BD-4, 15 pairs
  {FACT_MATCH, broker_of_record, severity: report,
     [bd C3, pm-assist A3, accounting C2]},                                          # BD-5
  {FACT_MATCH, referral_fee_payer, severity: report, [bd C7, accounting C3]},        # BD-7
  {FACT_MATCH, maintenance_auth_threshold, severity: report,
     [bd B10, maintenance B1]},                                                      # BD-2
  {FACT_MATCH, esignature_tool, severity: report, [bd D4, leasing D-grp]},           # BD-17
  {FACT_MATCH, quoted_marketing_reach,  severity: ERROR, [bd D10, leasing D-grp]},   # BD-1(a)
  {FACT_MATCH, quoted_inspection_schedule, severity: ERROR,
     [bd D11, owner: NONE]},                                                         # BD-1(b)
  {POLICY_DIVERGE, fair_housing_statement, weaker_than_check: true,
     [bd A8, leasing fair-housing-guard, pm-assist housing]},                        # BD-11
  {NON_MATCH, lead_source_inventory, [bd D2, leasing D5]},                           # BD-16
  {ORDERING, company_minimum <= maintenance_auth_threshold, [bd B10 both halves]},   # BD-2 companion
]

cross_seat_lane: [
  {id: BD-14, from: {seat: bd, stage: "S6 handoff -> WON"},
              to: {seat: leasing, entry: "property enters portfolio"},
              payload: [won_row, handoff_package],
              owner: UNASSIGNED, specified_by: NEITHER_QUESTIONNAIRE}
]

fill_exempt_blocks: [ quotable_standards ]            # E3 cap 6b, and see the class finding below

never_graduate: [fee_or_package_deviation, agreement_language_or_threshold,
                 never_promise_list, legal_or_fair_housing, red_flag_property_acceptance,
                 decline_or_walk_away]
```

**Six requirements stated as tests, not as prose:**

1. **Skills-file P-rows (E2 cap 1).** `{{owner_intake_form_link}}` substitutes in
   `pma-and-handoff/SKILL.md`. Mutation removing the skills walk leaves the raw token on an
   owner-facing send path and dies by name.
2. **Quoted-promise severity (E3 cap 6a).** BD-1(a): the **same** fixture pair
   (`bd D10` = 3, `leasing` = 3) mutated to 90 **rejects** under `severity: error` and
   **surfaces-and-configures** under `severity: report`. BD-2 stays plain `FACT_MATCH` and
   **passes** — proving error-severity is not applied by pattern-matching the word *threshold*.
3. **NEW — `owner_absent` is not `match` (E3 cap 6a, sub-shape (b), §8.4).** BD-1(b): a
   `severity: error` row whose counterpart key exists in **no** configured seat must produce an
   **`owner_absent` outcome**, distinct from both `match` and `mismatch`. **Named test:** configure
   the golden fixture with D11 answered and no seat delivering a periodic inspection → the
   contradiction report names the standard, the quoting seat, and *the absence of an owner*. A
   mutation that treats an absent counterpart as "nothing to compare" reports clean and dies.
4. **Fill-exempt (E3 cap 6b), proven against three causes.** All three `quotable_standards` keys in
   §9.2 stay empty after configure and each produces a named report line. A mutation removing
   `fill_exempt: true` back-fills `typical_days_to_lease` from the hint and dies by name.
   **AND — F-BD-5: the exemption must be declarable on `packages` sub-keys**
   (`protection_program_terms_verbatim`, `pet_policy.damage_coverage`, `leasing_guarantee_program`),
   because `objection-handling/SKILL.md:106` sends the agent to quote from **both** blocks. A
   per-block exemption that covers one of the two blocks the agent quotes from is a half-guard.
5. **N-way POLICY is ALL PAIRS, restated at N=6 (E3 cap 5).** SEAM-11 now spans six seats with
   **four distinct names and two agreeing pairs — 15 pairs, 13 failing** (§8.1). The capability's
   named test currently specifies the four-seat / five-failing-pairs case; **that fixture is stale
   by two arms.** Restate at N=6. A checker that stops at the first agreeing pair reports clean on
   a portfolio with four different people in the seat.
6. **PHASE-ZERO is a valid configured outcome (BD-4).** An empty **C2** must produce a seat that
   **declines to start** — not a warning, not a default. **Named test:** a fixture with C2 blank
   configures to `flags.phase_zero[]` containing the BD-manager entry and **no** `{{bd_manager_name}}`
   substitution across all 43 sites. A mutation that substitutes an empty string writes 43 blanks
   into live prose and dies by name.

**Two schema shapes this table needs that do not exist yet, stated as gaps rather than assumed:**
`cross_seat_lane[]` (BD-14 is a lane, not a value — §8.5) and a **measure declaration** on
`FACT_MATCH` rows so BD-1 sub-shape (c) cannot be typed at all (§8.4).

**Open item, not a requirement:** `seat-config.json` still has no applier, and this seat's
structured half carries **13 top-level objects** while **29 of the 42 questions produce no
placeholder at all**. Quantified here rather than repeated.

---

## 12. Coverage proof — both directions

**Direction 1 — questions → destinations: 42/42 mapped. Zero UNMAPPED.**

- Group A: 9/9 · Group B: 12/12 · Group C: 9/9 · Group D: 12/12
- **11 questions produce 13 placeholder types.** Recounted by hand rather than carried: A6, B12,
  C2, C3, C4, C5, C6, C7, D1, D3, D4 — where **C5 and D1 each produce two** types, and
  `{{pma_signer}}` is **dual-sourced from A6 *and* D4** (F9). **31 questions are
  S/K/G/I/B/C!-only.** 11 + 31 = 42.
- Weakest mappings, flagged honestly rather than dressed up: **B2 / B3 / B5** (answered, quoted to
  owners, **no config key exists** — F-BD-4), **C1** (S+B only; the board dropdown is its whole
  consumer), **A1** (descriptive — it selects a benchmark tier and weights D7/D8 targets, it sets
  no threshold), **D2** (a list whose only consumers are a board dropdown and a compliance check).
- Zero bare flags: every pointer names an owner **seat and question id**; every gate names the
  behaviour it arms or disarms; every not-live state names the lane it darkens.

**Direction 2 — placeholders → sources: 20/20 sourced. Zero NO-SOURCE placeholders.**

| Source class | Types | Sites |
|---|---|---|
| Questionnaire answers (11 questions; C5 and D1 produce two each, `{{pma_signer}}` dual-cited) | 13 | 91 |
| Cover sheet (Company name) | 1 | 2 |
| Org-seeded + maintenance B8 pointer | 2 | 8 |
| add-agent framework values | 4 | 7 |
| **Total** | **20** | **108** |

**Direction 2b — values with no placeholder, sourced or declared anyway.** The assembly's N1–N16
table was **verified, not assumed**: all 16 are real literals in the files named and all 16 are
correctly classed as unasked. Six are literals an answer can legitimately override — **N5** (daily
run hour), **N8** (rehab invoice boundary), **N9** (referral unpaid window), **N10** (nurture
no-touch alert), **N11** (pipeline minimum multiple), **N12** (retention defaults) — and those are
the K-rows and declared literals in §11. The other ten (**N1–N4** class taxonomy / graduation order
/ shadow duration / shadow exceptions, **N6–N7** cron times and heartbeat interval, **N13** S5–S6
nulls, **N14** log schema, **N15** board write rules, **N16** pre-stage checks) are **structural,
not configurable**.

**And one the table does not contain: F-BD-1**, the speed-to-lead window — 13 references, no
question, no key, no N-row. **The two-instrument rule is what found it**: the assembly's list was
verified against the tree rather than consumed, and the tree had one more.

**Conditional gates preserved from the questionnaire's own text: 9** — A2 (a market with no
lookup site is a lane that cannot run), A3 + A4 (outside-area / under-minimum / above-market
walk-away route to the manager before any agreement), A5 + A9 (unconfirmed legal ⇒ lane not live),
A8 (protected-class preference declined, **no approver, not configurable**), B4 (programs are a
closed list of what the company runs), B5 (`exists: false` is a hard mute per market), B9 (signed
referral agreement required, an answer may not clear it), C8 (`none` is a routed answer, empty is
not), C9 (an empty partner list mutes the referral sentence).
**Every one arms or disarms behaviour; none of them moves a never-graduates line, and A8 exists
specifically to refuse to.**

---

## 13. seat-config.json shape — as-shipped, with the v2 additions this table requires

Shipped shape (verified by reading the file, 167 lines): `{_about, _frozen_docs, _descriptive{},
markets{}, acceptance{}, state_rules{…, record_retention{}, _unconfirmed_rule}, packages{…,
leasing_guarantee_program{}, pet_policy{}, rehab_management{}}, agreement_terms{}, referrals{},
people{…, redirect_recipients{}, _note}, platform{}, clocks{…, stage_max_days{}},
activity_targets{weekly{}}, cadence{}, quotable_standards{…, _note}, compliance{}, shadow_mode{}}`.

**13 top-level objects. Every one carries a `_cite` naming its questions** — the strongest
provenance discipline of any seat's config so far, and worth preserving as the pattern.

Raw answers are **not** preserved beside derived values. Same divergence from the maintenance
pattern the pm-assist table recorded, same cost: re-mapping requires re-asking.
**Recommended additions (not made — draft tree is read-only):** `answers: {A1..D12 raw text}` and
`provenance: {questionnaire_version, filled_by, date}`.

**Required v2 additions** (E2 cap 4a / E3 caps 1, 3, 6): `config_artifact`, `cross_seat{}` with
the **migration-pending** record on BD-3, `held_pending_seat{}`, `cross_seat_checks[]` with
**typed assertions and per-row severity**, `cross_seat_lane[]` (new shape, BD-14),
`fill_exempt_blocks[]`, `never_graduate[]` — populated as listed in §11.

**Missing keys this table declares as required** (F-BD-4, F-BD-1): `packages.setup_fee`,
`packages.maintenance_reserve`, `packages.placement_fee`, `clocks.speed_to_lead_minutes`.

---

## Worker stop line

Table + fixture, per contract. No build, no configurator run, no `add-agent`, no writes to
`templates/`, `outputs/templates-drafts/`, or the kit. Draft-tree defects flagged in §10 and left
in place. The banned sales acronym ruling is discharged in §7 with its provenance; **no destination in either
deliverable carries the acronym.** SEAM-38+ deliberately not drawn; BD-16…BD-19 minted under the
BD prefix per the parallel-minting rule.

---
## QA AMENDMENT (mapping QA reviewer, 2026-08-25 ~1325Z, per orchestrator reviewer eyeball finding 1787662301649)
F-BD-7's closure cite "K1 + K10" is a LABEL SLIP: section 11 defines K1-K8 only and the
day-mode row is K8 - read the cite as "K1 + K8". K10 does not exist. Same family as
F-BD-6 (label vs table-body drift); the table body and K-row definitions are correct,
only the cross-reference label erred. No other K-row cites affected (verified by grep).
