---
name: fraud-and-unauthorized-transactions
description: "Drop-everything protocol for a transaction in the trust account that nobody initiated: a wire, an ACH pull, an unrecognized check, a disbursement to an unknown payee. Do not touch it, capture everything, notify the property manager immediately verbally then in writing, and preserve every record unaltered. Judgment scenario 14."
triggers: ["fraud", "suspected fraud", "unauthorized transaction", "unknown payee", "unrecognized wire", "ACH pull", "did not initiate", "missing funds", "bank fraud", "embezzlement", "compromised account"]
---

# Suspected Fraud or Unauthorized Transaction

Source: judgment scenario 14. This is the one situation where everything else stops.

---

## Do right now

1. **Do not touch the transaction.** Do not attempt to reverse it, dispute it, delete it, or "clean up" the ledger around it.
2. **Capture everything.** Screenshot the bank entry, the ledger view, the timestamps, and anything adjacent that might matter. Capture more than seems necessary.
3. **Notify the property manager immediately** — verbally first, then in writing. Use `platform.after_hours_escalation_channel` (D8) if it is outside business hours. This is exactly what that channel exists for.
4. **Do not discuss it with other staff** until the property manager directs you to. Not because anyone is suspected, but because an investigation with a controlled information boundary is worth more than one without.
5. **Contact the bank's fraud line to place a hold only if the property manager authorizes it.**
6. **Preserve every record. Alter no document.** Not a note, not a category, not a typo.

---

## Never

- Never attempt to reverse or delete the transaction yourself.
- Never assume it is a bank error and wait for it to resolve.
- Never tell a resident, an owner, or a vendor before the property manager and counsel have been notified.
- Never continue normal disbursements out of that account while the question is open, unless the property manager explicitly directs it.

---

## Escalate when

Immediately. Same minute. This is a drop-everything situation and there is no threshold on it — a small unrecognized transaction is treated exactly like a large one, because the size of the first one says nothing about the size of the next.

The property manager notifies the broker, contacts legal counsel, and determines whether law enforcement or the state real estate regulator (`state_rules.trust_audit_regulator`, A13) has to be notified.

---

## Write down

Everything, timestamped, from the moment of discovery:

- what was seen, where, and at what time
- the exact transaction detail: date, amount, payee, method, account
- what was captured and where the captures are stored
- who was notified, by what channel, at what time
- every instruction received and from whom
- every action taken, in sequence

Open a decision-log entry as scenario S14 at the moment of discovery, not at the end of the day.

---

## The adjacent tells

Some of these arrive before the transaction does. Treat each as a fraud signal, not an administrative oddity:

- a vendor banking change request, especially one with urgency attached (`vendor-banking-change`)
- a change request arriving right before a scheduled payment run
- an email thread where the reply-to differs from the sender
- a payment instruction that arrives outside the normal channel
- a reconciliation variance with no traceable cause, however small

A small unexplained variance is the classic first symptom. That is why the penny-off discipline in `trust-reconciliation` is not pedantry.

---

## Hard gates

- The agent takes no corrective action here, at all, of any kind.
- Speed of notification is the entire contribution. Certainty is not required to escalate; suspicion is the trigger.
- Nothing about the situation goes into a shared-scope knowledge base, an activity feed, or any channel beyond the escalation path.
