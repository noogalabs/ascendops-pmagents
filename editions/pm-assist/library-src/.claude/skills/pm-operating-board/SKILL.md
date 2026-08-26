---
name: pm-operating-board
effort: medium
description: "The PM Operating Board workbook: nine tabs, where each lives, how each is populated, and the pull rules that keep it true. Use whenever you build, refresh, reconcile, or answer a question from the board — and before writing any row."
triggers: ["operating board", "the board", "nine tabs", "board pull", "refresh the board", "board row", "which tab", "pull the lane boards", "board is stale", "reconcile the board", "workbook"]
---

# PM Operating Board

One workbook at {{operating_board_location}} <!-- D2: where the PM Operating Board workbook lives -->, nine tabs. Some tabs may map to native views in {{pm_platform}} <!-- D1: property management platform --> instead of the workbook — `seat-config.platform.live_tabs_day_one` says which.

## The one rule

**Coordinators update the lane boards. The operating board pulls from them and never replaces them.**

You do not write to a lane board. You do not correct a lane board. You do not hold a value the lane board should hold. If a lane board is stale, that is an Escalation Triage row with the coordinator's name on it — not a number you supply.

## The nine tabs

| Tab | Owner of the content | Refresh | Skill |
|---|---|---|---|
| Daily Pulse | you (assembled) | every weekday morning | `daily-pulse` |
| Monday Board | you (assembled) | Monday morning | `monday-board` |
| Month-End Pack | you (assembled) | month-end | `month-end-pack` |
| Approval Queue | you (rows), PM (decisions) | continuous + every heartbeat aging pass | `approval-queue` |
| Escalation Triage | anyone can flag in; you triage | continuous | `escalation-triage` |
| Owner Snapshot | you (maintained) | on change + monthly | `owner-snapshot` |
| Owner Report Pack | you (assembled), PM (released) | monthly, by day {{owner_report_day}} <!-- D6: day of the month the owner report pack goes out --> | `owner-report-pack` |
| Alert Rules | configured at onboarding | on config change only | `alert-rules` |
| Follow-Through Log | you (rows), PM (promises) | continuous + Monday sweep | `monday-board` |

## Pull discipline

Every pull records three things. A row missing any of them is not a row.

1. **Value** — exactly as the source gave it. No rounding, ever, and never toward a threshold.
2. **Source** — which lane board, which report, which platform view.
3. **Pull time** — local time ({{timezone}} <!-- cover sheet: timezone -->), not UTC, on the row itself.

Pull method per lane is in `seat-config.platform.lane_pull_method`: linked sheet, export, or manual update, and who does it. A manual-update lane whose person has not updated is a stale-source row, not a missing number.

## The never-reconcile-silently rule

When two sources disagree about the same fact:

- Show **both** values with **both** pull times, side by side, on the tab where the question lives
- Mark the row `DISCREPANCY`
- Route it to {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> with both sources named
- Do **not** pick one, average them, prefer the fresher one, or footnote the difference away

Picking the "obviously right" one is the failure this rule exists to prevent. The PM resolves it; you carry the pair until they do.

## Derived numbers

A number you computed is labeled `derived` and names its inputs on the row. "Delinquency 2.4%" is incomplete. "Delinquency 2.4% (derived: $9,840 past due ÷ $410,000 rent roll, both pulled 7:04 AM)" is complete.

An input you could not pull makes the derived number **unavailable**, not estimated. Say what is missing and whose board it lives on.

## Missing values

A missing number is reported missing. No estimate, no interpolation, no carry-forward from last week. The row reads `NOT AVAILABLE — <source> last updated <when>` and lands in Escalation Triage with the source owner's name.

## Board writes and shadow mode

While shadow mode is active there are **no board writes of record** — you compute the tabs and report them in the calibration digest instead. See `shadow-mode-calibration`. After shadow mode, board writes are still a graduated category (`board_row_write` in `copilot-thresholds.json`) and start locked.

## When a tab does not exist yet

If a tab has no home — no workbook sheet and no mapped platform view — the seat cannot run that tab. Set `flags.phase_zero` in `seat-config.json`, raise a `[HUMAN]` task, and say plainly which alerts are dark until it exists. Do not invent a substitute location.
