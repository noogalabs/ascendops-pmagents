# System Context

**Organization:** {{org}} <!-- cover sheet: Org short-name -->
**Company:** {{company_name}} <!-- cover sheet: Company name -->
**Timezone:** {{timezone}} <!-- cover sheet: Timezone -->
**Framework:** cortextOS Node.js

---

## Accounting Platform
**Platform:** {{accounting_platform}} <!-- D1 -->
<!-- Note at onboarding whether the platform includes a built-in trust reconciliation module
     and platform 1099 filing; both change the month-end and year-end mechanics. -->

## Bank and Account Inventory
<!-- Filled at onboarding from D2. List every account: bank, account purpose (operating trust,
     security deposit trust, reserve, company operating), and which reports or feeds expose it.
     No account numbers in this file. -->

**Security deposit trust separate from operating trust:** {{deposit_trust_separate}} <!-- D3 -->
**Positive pay enrolled on trust accounts:** {{positive_pay_enrolled}} <!-- D4 -->
**Suspense / clearing account for unidentified payments:** {{suspense_account}} <!-- D5 -->

## Board and Decision Log
**Tracking board location:** {{board_location}} <!-- D6 -->
**PM decision log location:** {{decision_log_location}} <!-- D6 -->
<!-- If either does not exist yet, bootstrapping both is a phase-zero task before this
     agent watches anything. -->

## Read-Only Access Paths
<!-- Filled at onboarding from D7. Name every report export and statement source this agent
     can see. A statement drop into a shared folder is a valid day-one answer.
     This agent is read-only by construction. -->

## Escalation Channels
**Money escalations to the property manager:** {{money_escalation_channel}} <!-- D8 -->
**Urgent / after-hours, including suspected fraud:** {{after_hours_escalation_channel}} <!-- D8 -->

## W-9 and 1099
**W-9 storage location:** {{w9_storage_location}} <!-- D9 -->
<!-- If no 1099 tracker exists, building one is a phase-zero task ahead of year-end. -->

## Jurisdictions
<!-- Filled at onboarding from A17. Which landlord-tenant statute applies in each county or
     jurisdiction in the portfolio. Notice and deposit rules change with it. -->

---

This file contains static org context only. For the live agent roster, run:
```bash
cortextos bus list-agents
```

For agent health (last heartbeat per agent), run:
```bash
cortextos bus read-all-heartbeats
```
