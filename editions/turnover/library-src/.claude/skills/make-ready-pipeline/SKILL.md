---
name: make-ready-pipeline
description: "Run the full unit turn from move-out possession through rent-ready certification: build the day-count timeline and critical path, classify scope as cosmetic vs rent-ready-blocking, sequence trades with dependency ordering, QC every must-fix with evidence, and issue the completion record to leasing. Re-key is always last. Certify gate requires 100% must-fix verified plus re-key verified. Demo mode runs fully offline."
triggers: ["make-ready", "turnover", "unit turn", "rent-ready", "make ready pipeline", "possession", "punch list", "scope review", "QC", "certify", "stage 1", "stage 2", "stage 3", "stage 4", "stage 5", "critical path", "day count", "trade sequence"]
context: fork
model: sonnet
---

# Make-Ready Pipeline

This is the flagship skill for the turnover coordinator. It owns the full 5-stage pipeline from move-out possession to rent-ready certification. It plans, tracks, and certifies; it never repairs, dispatches vendors directly, or messages externally without approval.

---

## Hard Gate

This skill plans and certifies. It does not dispatch vendors, send messages, decide chargebacks, or commit spend. Trade dispatch routes through vendor-coordination (approval-gated). The wear-vs-damage split is a recommendation; the deposit/chargeback decision stays with the property manager. Rent-ready is certified only when every must-fix is verified with evidence AND re-key is verified.

---

## 5-Stage Pipeline

| Stage | Entry Condition | Exit Condition | Critical-Path Rule |
|-------|----------------|---------------|-------------------|
| 1. Move-out trigger + inspection | Possession confirmed (keys back); day-0 clock starts | Structured findings delivered within {{inspection_sla_hours}}h | Missing findings at deadline → PM escalation draft |
| 2. Scope + punch list | Findings received | PM-approved punch list | Scope completed within {{scope_sla_hours}}h; PM approval required before Stage 3; wear-vs-damage flags for PM decision |
| 3. Multi-trade coordination | PM-approved punch list | All must-fix tasks reported done with evidence | Dependency order: repairs → paint → floor/clean; dry/cure as own blocks; re-key LAST; stale alert at {{stale_stage_alert_days}} days |
| 4. Final walk + QC | All must-fix tasks reported done | Every must-fix verified with evidence; rework re-routed to Stage 3 | Verified-done beats reported-done; no shortcuts |
| 5. Rent-ready certification | Every must-fix verified + re-key verified | Completion record delivered to leasing; leasing ACK closes pipeline | 100% must-fix AND re-key gate; no partial certifications |

---

## Certify Gate (Non-Negotiable)

Before issuing any rent-ready certification, confirm ALL of the following:
1. Every must-fix item in the punch list has `verified_done = True`
2. Re-key is in the punch list, sequenced last, and has `verified_done = True`
3. A completion record exists with evidence references per must-fix item

If any condition is false: the unit is `UNVERIFIED` and cannot be certified. Surface the open items to the property manager.

---

## Day-Count Engine

Day 0 = possession date (keys back, confirmed).
- Target rent-ready: Day {{turn_target_days}}
- Stale stage threshold: {{stale_stage_alert_days}} days without progress
- Critical path = longest dependency chain from possession to re-key-done
- Each stage exit date is derived from task durations and dependency ordering

The helper script (`make_ready.py`) runs the day-count arithmetic and dependency ordering offline.

---

## Trade Dependency Ordering

Always enforce this sequence. Never run later-stage trades before earlier-stage predecessors complete:

1. Trash-out / demo (enables: repairs)
2. Structural and mechanical repairs (enables: paint, floor prep)
3. Paint (enables: floor/clean; dry time = its own block)
4. Flooring (enables: final clean; cure time = its own block where applicable)
5. Final deep clean
6. Re-key (ALWAYS last — never certify without this step complete)

Dry and cure times are modeled as separate tasks with zero-work duration but real elapsed time. They block downstream tasks.

---

## Scope Classification

For each finding from the inspection:
- **Must-fix (rent-ready blocker):** anything that makes the unit unhabitable, legally non-compliant, or materially different from what was advertised. Required before certification.
- **Cosmetic (can defer):** surface wear that does not block habitability or legal compliance. Document; PM decides whether to address in this turn.
- **Wear-vs-damage flag:** classify as normal wear (owner cost) or tenant-caused damage (chargeback candidate). Flag genuinely unclear cases as `UNCLEAR — PM decision`.

---

## Helper Script

The helper is pure Python 3 stdlib with no network or third-party dependencies.

Run synthetic demo data:

```bash
python3 .claude/skills/make-ready-pipeline/make_ready.py --demo
python3 .claude/skills/make-ready-pipeline/make_ready.py --demo --json
```

Run a real turn (JSON file with tasks):

```bash
python3 .claude/skills/make-ready-pipeline/make_ready.py \
  --tasks tasks.json \
  --possession-date 2026-07-01 \
  --target-days 10 \
  --json
```

---

## Output Contract

For each unit turn, produce:
- possession date, day-0 clock, and target rent-ready date
- punch list with must-fix vs cosmetic classification, wear-vs-damage flags, and PM-approval status
- dependency-ordered task list with trade, duration, dry/cure blocks, and assigned vendor slot
- critical path and soonest-possible ready date (vs target: on-track-with-slack or at-risk-with-gap)
- per-task verified_done status with evidence reference
- stale-stage flags (any stage over {{stale_stage_alert_days}} days without progress)
- CERTIFIABLE / UNVERIFIED verdict with open items enumerated

---

## Validation

- Day-count clock started on possession date, not inspection or scope date.
- Every must-fix item has a verified_done status and evidence reference before certification.
- Re-key is sequenced last and verified before certification.
- No vendor dispatch issued from this skill; routing went through vendor-coordination.
- No chargeback decided; no external message sent without approval.
- Demo mode made zero external calls.
