---
name: pipeline-board
description: "Use this whenever you write to, read from, or set up the pipeline board — adding a deal, moving a stage, logging a touch, populating a dropdown, or answering 'where does this go'. It carries the tab structure, the full column schema, the dropdown sources, and the two write rules that make the board trustworthy. Load it before the first board write of any session."
triggers: ["pipeline board", "board", "add a deal", "new row", "which tab", "column schema", "dropdown", "lookup tables", "board setup", "where does this go", "log a touch", "update the board", "deal id"]
---

# Pipeline Board — The Record

One workbook on {{pipeline_board_platform}} <!-- D1 --> at {{pipeline_board_location}} <!-- D1 -->.

**One row = one owner + one property.** An owner with three properties has three rows. This is not a convenience; a deal that spans rows cannot be staged, aged, or counted.

---

## The Two Write Rules

1. **Every value carries its source and when it was pulled.** A rent range without the analysis date behind it is not a range, it is a number somebody will quote back to you in six weeks.
2. **Every active deal has a next action and a date.** Always. A blank one is an alert condition, not a scheduling gap.

When two sources disagree, that is a **discrepancy**: carry both, name both, flag it. Never average, never silently pick the newer one.

---

## Tabs

| Tab | Colour | Holds |
|---|---|---|
| PIPELINE - ACTIVE | Blue | Every live deal, S0–S6, plus nurture |
| CLOSED WON | Green | Won deals — retained permanently <!-- A9 --> |
| CLOSED LOST | Red | Lost deals — retained per the configured window <!-- A9 --> |
| REDIRECTED | Orange | Not property management deals <!-- C8 --> |
| NURTURE | Yellow | Interested, not ready — every row has a hard date |
| ARCHIVE | Grey | Permanently inactive, read-only, never deleted |
| CONVERSION METRICS | Purple | Auto-calculated funnel and lead-source performance |
| ALERTS DASHBOARD | Red | Every alert condition, auto-populated, no manual entry |
| BDM DAILY VIEW | Blue | Filtered: what needs attention today |
| WEEKLY REVIEW VIEW | Green | Filtered: the full walk |
| LOOKUP TABLES | Grey | Every dropdown source — driven from `business-development-config.json` |

---

## Column Schema

### Block A — Record identification
| # | Column | Type | Notes |
|---|---|---|---|
| A1 | Deal ID | auto | Never edited by hand |
| A2 | Date lead created | date | |
| A3 | BD owner | dropdown | Source: `people.bdms` <!-- C1 --> |
| A4 | Pipeline stage | dropdown | Exactly one. See `stage-gates` |
| A5 | Days in current stage | formula | Drives every stale alert |
| A6 | Date entered current stage | date | **Updated on every stage change.** A stale A6 makes A5 lie, and A5 is what the alerts read |

### Block B — Owner and contact
B1 owner first name · B2 owner last name · B3 co-owner name · B4 owner mobile · B5 co-owner mobile · B6 owner email · B7 co-owner email · B8 ownership entity (dropdown, source `state_rules.accepted_ownership_entity_types` <!-- A5 -->) · B9 entity name · B10 ownership verified (**must be Yes before an agreement is sent** <!-- A2 -->) · B11 all decision-makers identified (**must be Yes before an appointment counts as held**) · B12 preferred contact method

> Block B is the seat's PII concentration. It lives here and nowhere else. See `prospect-data-handling`.

### Block C — Property
C1 address · C2 city · C3 state (dropdown, source `markets.states` <!-- A2 -->) · C4 zip · C5 property type · C6 beds · C7 baths · C8 square footage · C9 stories · C10 pool · C11 HOA · C12 HOA fee · C13 condition · C14 occupancy · C15 unit count · C16 **doors this deal represents** (drives every pipeline-value number)

### Block D — Lead intelligence
D1 lead source (dropdown, source `platform.active_lead_sources` + `company_specific_lead_sources` <!-- D2 -->) · D2 referring person or company · D3 referral fee owed · D4 referral fee amount (source `referrals.fee_schedule_by_type` <!-- B9 -->) · D5 inbound or outbound · D6 competing companies mentioned · D7 previous manager · D8 reason for leaving · D9 self-managing before

### Block E — Motivation and qualification
E1 primary goal · E2 short-term goal · E3 long-term goal · E4 timeline · E5 motivation level · E6 **property type fit** (PM lead / brokerage redirect / investment redirect / disqualified — decides which department owns it <!-- C8 -->) · E7 disqualify reason · E8 carrying costs · E9 owner's target rent · E10 recommended rent range · E11 other properties owned · E12 how many

### Block F — Activity and timing
F1 discovery call date · F2 discovery call completed · F3 appointment date · F4 appointment status · F5 all decision-makers attending · F6/F7 analysis sent + date · F8/F9 agreement sent + date · F10/F11 agreement signed + date · F12 package selected (source `packages.tier_names` <!-- B1 -->) · F13 monthly fee · F14 setup fee collected · **F15 next action** · **F16 next action due date** · F17 last touch date · F18 days since last touch (formula) · F19 total touches · F20 follow-up sequence active

> F15 and F16 are the two fields the whole seat runs on. Blank F16 on an active deal is a Critical alert.

### Block G — Outcome
G1 deal status · G2 won date · G3 lost date · G4 lost reason · G5 lost to competitor · G6 redirected to · G7 handoff complete · G8 handoff date · G9 referral fee paid · G10 notes (newest entry at top)

---

## Dropdowns Come From The Config, Not From Typing

Every dropdown with a fill-in source reads from LOOKUP TABLES, and LOOKUP TABLES is driven from `business-development-config.json`:

| Dropdown | Config key | Question |
|---|---|---|
| BD owner | `people.bdms` | C1 |
| State | `markets.states` | A2 |
| Lead source | `platform.active_lead_sources` + `company_specific_lead_sources` | D2 |
| Package | `packages.tier_names` | B1 |
| Ownership entity | `state_rules.accepted_ownership_entity_types` | A5 |
| Referral fee amount | `referrals.fee_schedule_by_type` | B9 |

A value typed straight into a cell instead of picked from a list is a value the metrics tab cannot count. If a needed option is missing, add it to the config and regenerate — never to the cell.

---

## When The Platform Cannot Do Something

Some platforms cannot compute days-in-stage, or cannot drive a filtered view. **Say so.** A formula that silently stopped updating reads as a healthy zero, and a healthy zero on a stale-deal alert is the most expensive number on this board. If a computed column cannot be computed, mark the column as manual and say it out loud at the weekly review.

---

## Retention

Records are archived, never deleted, per the configured retention schedule <!-- A9 -->. Duplicates are the one exception — merged into the surviving record, then deleted per the schedule. See `stage-gates` for archive triggers.
