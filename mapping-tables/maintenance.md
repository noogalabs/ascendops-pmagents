# AscendOps PMAgents demo: maintenance questionnaire → agent-config MAPPING TABLE (draft for orchestrator reviewer review)

Author: mapping QA reviewer, 2026-08-23. Status: DRAFT — orchestrator reviewer eyeballs before build (his gate, like item-2).
Sources read TODAY: ascend-doc-kit/maintenance-questionnaire/maintenance-questionnaire.md
(all 38 Q); templates/maintenance-coordinator placeholder census (grep, counts below).
Rule: every question gets a destination or an explicit UNMAPPED-AND-WHY; every template
placeholder gets a source or an explicit NO-SOURCE flag. Two directions, both proven.

## Destination taxonomy

| Code | Destination | What it means |
|---|---|---|
| P | Template placeholder | Direct {{...}} substitution at configure time |
| K | config.json key | Merged into the agent's config.json |
| S | seat-config.json | ALWAYS — every raw answer lands here structured; S-only means "config file is the sole machine home today" |
| G | Prose block → GUARDRAILS.md | Appended as a company-rules section |
| I | Prose block → IDENTITY.md / SOUL.md | Portfolio/people/role prose |
| B | Board LOOKUP tab | The spreadsheet config block (questionnaire's own stated Group-B destination) — SECONDARY for the demo, listed for completeness |
| C! | CONDITIONAL GATE | Answer arms/disarms an agent behavior (not just a value) |

## Placeholder census (the template side, both directions)

13 placeholder types in templates/maintenance-coordinator (files: IDENTITY, SOUL, GOALS,
GUARDRAILS, SYSTEM, ONBOARDING, config.json, copilot-thresholds.json):

| Placeholder (sites) | Source |
|---|---|
| {{agent_name}} (6), {{org}} (2), {{current_timestamp}} (1) | add-agent substitutes already |
| {{approval_threshold}} (6) | B1 |
| {{triage_sla_minutes}} (2) | B5 (emergency dispatch window, minutes component) |
| {{property_manager_name}} (2) | C1 |
| {{platform}} (8) | D1 |
| {{day_mode_start}} (2), {{day_mode_end}} (2) | B8 (external-comms window) — also org-seeded from context.json; B8 answer WINS for the seat, see note 1 |
| {{timezone}} (3) | **NO EXPLICIT QUESTION** → cover sheet (below) |
| {{company_name}} (4), {{org_name}} (1), {{forward_email}} (1) | **NO SOURCE QUESTION IN THE QUESTIONNAIRE** → cover sheet |

**FINDING → COVER SHEET:** the answers-file template gets a 4-field header block
(company name, org short-name, forward email, timezone) that the questionnaire never
asks. This is an answers-FILE addition, not a questionnaire edit — the kit docs stay
frozen. (the PMAgents PM questionnaire asks company identity; maintenance assumes it.)

## Per-question mapping (38/38)

### Group A — Portfolio and State Rules
| Q | Destination(s) | Mapping detail |
|---|---|---|
| A1 portfolio/markets/classes | S, I | Portfolio profile prose in IDENTITY; class C/D urgency-bump rule quoted into GUARDRAILS priority section (G) |
| A2 entry-notice per jurisdiction | S, G | Structured {jurisdiction: hours} map + GUARDRAILS notice-rules block |
| A3 deposit disposition deadline | S, G | Value + counsel-flag; NOTE: shared with turnover seat — seat-config marks it cross-seat |
| A4 certified-mail requirement | S, G, C! | If yes → the two high-consequence notice classes get delivery=certified-mail gate text |
| A5 damage dispute window | S, G | Value feeds notice templates' window phrase |
| A6 lease sections list | S, G | Structured list; GUARDRAILS: "every damage notice cites one of these" |
| A7 licensed-contractor trades | S, G | Always-vendor trade list (structured); replaces/extends the default 10-trade list |
| A8 habitability triggers | S, G | Structured triggers (e.g. heat<55F=emergency); tunes priority matrix prose |

### Group B — Thresholds, SLAs, Clocks
| Q | Destination(s) | Mapping detail |
|---|---|---|
| B1 owner pre-approval threshold + per-owner overrides | **P {{approval_threshold}}**, S, B | Base number → placeholder (6 sites incl. copilot-thresholds.json); per-owner overrides → seat-config map (no placeholder exists for overrides — S is their machine home) |
| B2 after-hours emergency spend cap | S, G, B | No placeholder exists; GUARDRAILS block: under-cap dispatch+notify, over-cap wake human. Candidate future placeholder; S-only for demo |
| B3 tenant responsibility floor | S, G, C! | Value + LEASE-CLAUSE-CONFIRMED flag; resident-responsibility message class DISABLED until flag true |
| B4 invoice variance % | S, B | One number, both consumers named (invoice review + board flag) |
| B5 SLA windows per priority + yellow % | **P {{triage_sla_minutes}}** (emergency-dispatch minutes), S, B | Full matrix → seat-config; heartbeat prompt in config.json carries the summary (K) |
| B6 owner approval timer + silence clause | S, G, C! | Timer value; proceed-on-silence message class DISABLED unless CLAUSE-CONFIRMED=true (human confirms signed agreement) — the questionnaire's own liability checkpoint, preserved verbatim |
| B7 callback/recurring windows + vendor warranty | S, G | Three windows structured; warranty-confirmed flag |
| B8 quiet hours / external comms window | **P {{day_mode_start}}/{{day_mode_end}}**, K, S | Note 1: org context.json seeds these too; the ANSWER wins for this agent, written to config.json day_mode keys |
| B9 on-call window + emergency response clock | S, I | Coverage prose + clock value |
| B10 escalation ages + closeout clock | S, K | Ages structured; closeout clock into heartbeat/board prompts |
| B11 survey low-score + target avg | S | Values; apology-message trigger threshold |
| B12 self-repair window | S, G | Value + lease-governs note |

### Group C — People and Roles
| Q | Destination(s) | Mapping detail |
|---|---|---|
| C1 PM of record + other approvers | **P {{property_manager_name}}**, S, I | Name → placeholder; approver list → seat-config + IDENTITY routing prose |
| C2 on-call human + channel | S, I | Escalation route prose + structured contact |
| C3 in-house techs: skills/areas/platform IDs | S, I | Structured roster (the dispatch decision reads this); DO/DO-NOT per tech preserved as free text per person |
| C4 region → people routing | S, G | REGION CHECK FIRST rule (region routing precedes trade lookup — same shape as our Nashville rule) |
| C5 vendor roster by trade | S, I | Structured roster; if answer says "no roster" → PHASE-ZERO flag in seat-config, dispatch prose says build-first |
| C6 after-hours line + call logging | S, I | Prose + structured |
| C7 invoice payment executor + handoff location | S, I | Prose; handoff location structured |
| C8 owner-managed exclusions | S, G, C! | NEVER-DISPATCH property list; empty list still written (present-and-empty ≠ absent) |
| C9 backup decision-maker | S, I | If answer empty → UNRESOLVED flag surfaced in the calibration digest, per the questionnaire's own hint |

### Group D — Platform and Wiring
| Q | Destination(s) | Mapping detail |
|---|---|---|
| D1 maintenance platform + accounting system | **P {{platform}}**, S | Platform name → placeholder; both systems structured |
| D2 platform write-paths + quirks | S, I | Quirks prose into TOOLS/skill notes (e.g. status-looks-like-assignment traps) |
| D3 resident channels per message class | S, G | Channel matrix structured; legal-notices=email-only default preserved unless answered otherwise |
| D4 vendor/tech channels | S | Channel matrix |
| D5 owner channel + approval sender name | S, G | Sender-identity rule into GUARDRAILS (whose name approvals go out under) |
| D6 escalation alert channels | S, K | Channels; escalation prompts in config reference them |
| D7 warranty records location | S, G | Pre-dispatch warranty check rule + location; if none → PHASE-ZERO flag |
| D8 lockbox/access code storage + routing | S, G | SECURITY block: codes only to assigned resource, never resident/owner-facing (matches our own lockbox rule shape) |
| D9 weekly report destinations | S, K | Two crons in config.json (Friday open-ticket summary, Monday KPI) with destinations from the answer |

## Coverage proof
- 38/38 questions mapped; zero UNMAPPED. Weakest mappings flagged honestly: B2 (S-only,
  no placeholder), B11 (S-only, consumer is message-trigger logic that is prose today).
- 13/13 placeholders sourced: 3 add-agent, 6 questionnaire (B1, B5, B8×2, C1, D1),
  4 cover-sheet (timezone, company_name, org_name, forward_email).
- 4 CONDITIONAL GATES preserved from the questionnaire's own text: A4 certified-mail,
  B3 lease-clause-confirmed, B6 silence-clause-confirmed, C8 never-dispatch list.
  These arm/disarm message classes — the configurator writes the flag, the gate text
  ships in GUARDRAILS either way.
- Board LOOKUP (B destinations) listed for completeness; demo scope writes seat-config
  + agent files only, board wiring is a stated non-goal for tomorrow.

## seat-config.json shape (proposed, orchestrator reviewer already blessed the artifact)
Top-level: {seat, company (cover sheet), answers: {A1..D9 raw text}, derived:
{thresholds{}, slas{}, windows{}, people{}, roster{}, channels{}, gates{confirmed_flags},
exclusions[], phase_zero[]}, provenance: {questionnaire_version, filled_by, date}}.
Raw answers ALWAYS preserved verbatim beside derived values — re-mapping is possible
without re-asking.
