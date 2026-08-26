---
name: trust-reconciliation
description: "Run the monthly three-way trust reconciliation: bank leg, owner ledger leg, resident deposit leg, agreeing to the penny. Verify and flag only — never move funds, never auto-correct a trust ledger, never post a plug entry to force balance. Covers judgment scenario 9 in both its small and large forms."
triggers: ["reconciliation", "three-way", "trust reconciliation", "bank rec", "out of balance", "variance", "does not reconcile", "trust balance", "reconcile to bank", "ledger total", "unreconciled"]
---

# Three-Way Trust Reconciliation

Source: monthly workflow Step 10, plus judgment scenario 9. This is the most important financial control in property management and it runs every month without exception.

---

## The three legs

| Leg | What it confirms |
|---|---|
| **Bank** | The trust bank statement reconciles to the platform's bank register. Every deposit and every payment matches. |
| **Owner ledgers** | The sum of all owner ledger balances — what the platform says is owed to owners. |
| **Resident deposits** | The sum of all resident security deposit balances and any resident credit balances held in trust. |

## The test

```
reconciled bank balance
  = sum of owner ledgers
  + sum of resident deposit balances
  + any other trust liabilities
```

**To the penny.** If these do not agree, there is an error or a trust violation. Stop and find it before the month closes.

---

## Preflight

- the bank statement for the period is available
- all transactions for the month are posted
- all draws and deposits have cleared
- the period is not already locked

Where `platform.has_builtin_trust_reconciliation` (D1) is true, the platform's module runs the ledger side. It does not replace reconciling to the actual bank statement; that leg is still done against the statement itself, every month.

---

## Scenario 9A — small variance (under `thresholds.reconciliation_variance_threshold`, B5)

**Do right now.** Do not force it. Trace every transaction for the period: bank fees, rounding, timing differences, a transposed digit. Give it one full business day.

**Never.** Never post a reconciliation adjustment to make it balance without knowing what caused it. Small unexplained variances are how embezzlement starts and stays undetected.

**Escalate when.** You cannot find the source within one business day.

**Write down.** Amount off, period, every step taken, resolution or escalation.

## Scenario 9B — large variance (at or above B5, or any amount you cannot explain)

**Do right now.** Stop all non-essential disbursements. Notify the property manager immediately. Do not send owner statements. Pull every transaction for the period.

**Never.** Never send statements over an account that does not reconcile. Never post an adjustment to force a balance. Never assume it will work itself out.

**Escalate when.** Immediately, the same hour. The property manager decides whether to notify the broker, pause disbursements, or bring in legal or outside accounting.

**Write down.** Amount, period, every transaction reviewed, time the PM was notified, resolution.

---

## The alert thresholds

- Any variance at or above `thresholds.variance_alert_amount` (B6) open for `thresholds.variance_alert_age_days` (B6) or more → bookkeeper alert.
- Any leg open more than 7 days → property-manager escalation.

An open variance blocks statement release. That is not a soft coupling.

---

## Sign-off and retention

`roles.principal_or_managing_broker` (C2), or whoever `state_rules.trust_reconciliation_signer` (A13) names, reviews and signs. **This agent does not sign a reconciliation** — `reconciliation_signoff` is in the `never_graduate` set. Signing is a licensed act and it is the point of the control.

Cadence comes from `state_rules.trust_reconciliation_cadence` (A13); retention from `state_rules.trust_record_retention_years` (A13); the regulator that can audit from `state_rules.trust_audit_regulator` (A13). The broker's license is what is at risk when a trust account is out of balance.

**Target: completed within 5 business days of month end.**

---

## Hard gates

- Verify and flag. Never move funds, never correct a ledger, never clear a variance on judgment.
- A plug entry is never the answer, at any amount.
- If a source document is missing, that is a stated blind spot in the report, not a leg quietly skipped.
