---
name: pma-and-handoff
description: "Load this when an agreement is going out, when one comes back signed, and through the whole handoff to onboarding. Covers the send package, the entity and disclosure checks that make the agreement valid, the signature chase, the document package operations needs, the post-signing sequence, the referral fee flag, and what to do when onboarding finds something the discovery call missed."
triggers: ["send agreement", "PMA", "management agreement", "e-signature", "W-9", "signature", "unsigned", "signed", "handoff", "onboarding", "post-signing", "intake form", "entity mismatch", "referral fee", "surprise at handoff", "ops found"]
---

# Agreement and Handoff

Two phases that share one rule: **the company is bound from the moment it is signed, so everything that determines whether it should be signed happens before, not after.**

---

## Phase 1 — Sending

### Before it goes out

| Check | Source | If it fails |
|---|---|---|
| Ownership verified, entity matches the tax record | `markets.tax_record_lookup_by_market` <!-- A2, A5 --> | **Stop.** Re-execute against the correct entity. An agreement signed by the wrong party may be unenforceable |
| Entity type is one the company accepts | `state_rules.accepted_ownership_entity_types` <!-- A5 --> | Route to {{broker_of_record}} <!-- C3 --> |
| One agreement per unit or per owner, as required | `state_rules.agreement_per_unit_or_per_owner` <!-- A5 --> | Split or combine before sending, never after |
| Required disclosures attached | `state_rules.required_disclosures_at_signing` <!-- A6 --> | Do not send without them |
| Company-side signer correct | <!-- A6, D4 --> | Route |
| No red-flag property condition unresolved | `property-and-owner-gates` <!-- A4 --> | Manager approval, in writing, before sending |
| Every prevention question asked | `discovery-call` <!-- judgment §7 --> | Ask them now. It is cheaper than finding out during onboarding |

**If any state-law field is unconfirmed, that lane is not live.** Do not send an agreement into a market whose rules the config does not carry. Say so, and get counsel's answer <!-- C4 -->.

### The send
- Through {{esignature_tool}} <!-- D4 -->
- **W-9 goes out attached to the send**, not separately and not later
- Executed on the company side by {{pma_signer}} <!-- A6, D4 -->
- **Same business day as the appointment** — no exceptions <!-- D6 -->
- F8, F9, and a next action inside 24 hours

### The signature chase (S5)

The highest-risk stage on the board. Deals die here without anyone deciding to kill them.

| When | Do |
|---|---|
| Inside 24 hours | Call — not email. Surface what is still unresolved. Re-close |
| `clocks.unsigned_agreement_alert_hours` <!-- D6 --> | Critical alert. Manager sees it too |
| `clocks.unsigned_agreement_escalate_days` <!-- D6 --> | Escalate to {{bd_manager_name}}. Log first. A live conversation, not a fourth email |

Never chase with a bare nudge. Every touch surfaces something or asks something.

---

## Phase 2 — Signed

Everything below happens on day one, not "this week".

### The document package for operations

| Document | Notes |
|---|---|
| Fully executed agreement | Entity matching the tax record <!-- A5 --> |
| W-9 | Sent with the agreement, returned with it |
| Proof of ownership / entity verification | The tax record itself |
| Proof of property insurance | |
| HOA documentation | Where applicable — including any rental restriction |
| Existing lease | If a tenant is in place |
| **Deposit ledger and move-in inspection** | If a tenant is in place. **Their absence is named in writing, not glossed over** <!-- A7 --> |
| Existing vendor contracts or warranties | |

### The board and CRM package
Every discovery note · lead source tagged · address, unit count, all decision-makers · agreed rate range with its pull date · package and fee · any owner preference or sensitivity worth the next seat knowing · referral source flagged.

### Financial
Setup fee collected or invoiced <!-- B2 --> · maintenance reserve collected or invoiced <!-- B3 --> · **referral fee flagged to {{referral_fee_payer}}** <!-- C7 --> with the amount from `referrals.fee_schedule_by_type` <!-- B9 -->.

> **Referral fees are never a verbal commitment.** No signed referral agreement means no payment and no promise of one <!-- B9 -->. Unpaid past the configured window fires an alert to accounting by name — referral relationships are built on this being boring and on time.

### The post-signing sequence

1. **Thank-you and next steps, immediately.** Three steps, plainly:
   - Complete the owner intake form at {{owner_intake_form_link}} <!-- D3 --> within the day, or do it together on a call
   - {{onboarding_specialist}} <!-- C5 --> will make contact and becomes the main point of contact
   - {{property_access_coordinator}} <!-- C6 --> will call about property access
2. **Notify onboarding** through {{handoff_channel}} <!-- C5 -->
3. **Schedule the onboarding call** inside the configured window <!-- C5 -->
4. **Confirm receipt.** Handoff unconfirmed past its window is a Critical alert to the seat *and* the manager.

Every one of these is a staged message until its class graduates — including the thank-you. See `draft-release-gate`.

### Exit to WON
Intake form received, onboarding has made contact, G7 = Yes. Then G2, referral fee confirmed flagged, row to CLOSED WON. See `stage-gates`.

---

## When Onboarding Finds Something You Missed

It happens. What determines whether it is a problem or a disaster is what happens in the next hour.

### The five steps, in order
1. **Own it.** Do not say the owner should have disclosed it. Asking the right question was the seat's job.
2. **Log it** with the date discovered and a full description.
3. **Escalate to {{bd_manager_name}} the same day** <!-- C2 -->. Do not leave onboarding holding it.
4. **Fix the process.** Which prevention question would have caught this? Add it to `discovery-call` today, not at the next review.
5. **Have the owner conversation yourself.** Not onboarding. You have the relationship, and handing this one over teaches the owner that bad news comes from strangers.

### What each surprise means

| Found | Do |
|---|---|
| HOA rental restriction | Manager immediately; counsel on whether the agreement can proceed <!-- C4 --> |
| Missing lease, deposit ledger, or move-in inspection | **Tenant onboarding does not proceed.** Notify the owner in writing of the gap and the risk. Fresh inspection immediately <!-- A7 --> |
| Deferred maintenance | Written notice to the owner; repair plan before marketing |
| Delinquent mortgage | Manager immediately; counsel — managing a property heading to foreclosure carries real exposure <!-- C4 --> |
| Entity mismatch | **Stop.** Re-execute against the correct entity <!-- A5 --> |
| Undisclosed insurance claim | Manager; document; assess condition and coverage impact |
| Code violations | Manager and counsel. **No tenant is placed until they are resolved** <!-- A4, C4 --> |

### What to say
> "I want to be upfront about something we found during onboarding. [The issue, factually.] We need to sort this before we go further because it affects [leasability / your legal protection / our ability to manage it properly]. Here's what I'd suggest…"

And where information was withheld:
> "Going forward, if anything about the property or the tenant situation changes, I need to know straight away. The more I know, the better I can protect you."

Not accusatory. Not a lecture. Once, then moving on.

---

## The Line

Repeated surprises are not bad luck. They are a discovery process with a hole in it, and they are visible in the metrics before anyone says anything. The prevention checklist exists so this stays rare — see `discovery-call`.
