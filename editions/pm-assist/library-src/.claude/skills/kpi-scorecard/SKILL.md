---
name: kpi-scorecard
effort: low
description: "Compute and present the KPI set against configured targets, with every number sourced and pull-timed. Use in the Daily Pulse, the Monday Board, the Month-End Pack, and whenever the PM asks how the portfolio is doing."
triggers: ["kpi", "scorecard", "occupancy", "close rate", "renewal rate", "owner retention", "days vacant", "make ready target", "how are we doing", "against target", "benchmarks"]
---

# KPI Scorecard

Numbers against targets. Every figure carries its source and its pull time; derived figures name their inputs.

## The set

Targets live in `seat-config.kpi_targets`, pre-filled with the questionnaire's own standard set (B8) and overwritten only where the company overrides.

| KPI | Standard target | Source |
|---|---|---|
| Occupancy | 95% or higher | B8 |
| Work-order close rate within SLA | 90% | B8 |
| Renewal rate | 60–70% or higher | B8 |
| Owner retention | 90% annually | B8 |
| Leases expiring in any one month | no more than 20–25% | B8 |
| Days vacant | company value, usually market average | B7 |
| Days to make-ready | company standard | B7 |

An override the company gave replaces the standard silently in the config and **loudly on the tab**: the row shows the target and notes it is a company override, so nobody reads a passing number against the wrong bar.

## Presentation rules

- Value, target, delta, source, pull time. Five fields, every row
- A derived value names its inputs: "Renewal rate 63% (derived: 17 renewed ÷ 27 expiring, lease board pulled 7:04 AM)"
- An input you could not pull makes the KPI **unavailable**, not estimated
- Trend needs two real pulls. One pull plus a memory is not a trend

## What this never does

- Never explains a miss. The number is yours; the reason is the PM's
- Never rounds toward a target
- Never uses a denominator the boards do not agree on — if two boards give different door counts, that is a `DISCREPANCY` row, and the KPI reads unavailable until it resolves
- Never carries last month's figure into this month's row

## Where it appears

Daily Pulse (only KPIs that moved past target since the last pull), Monday Board (full set), Month-End Pack (full set with month-over-month), Owner Report Pack (per-property subset).
