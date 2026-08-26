---
name: broker-escalation
effort: low
description: "The broker-only decision classes: what they are, how they route, and the same-day channel rule. Use the moment a matter looks like it might be broker-only — the check is cheap and the miss is expensive."
triggers: ["broker", "broker only", "escalate to broker", "principal broker", "trust variance", "management agreement", "fee concession", "staff discipline", "legal demand", "attorney contact", "commission", "does this go to the broker"]
---

# Broker Escalation

Twelve decision classes never sit with the Property Manager. They go to {{broker_name}} <!-- A3: principal broker or company owner --> on {{broker_channel}} <!-- A3: channel broker-only escalations travel -->, **the same day**, and they never wait for the PM.

## The classes

The authoritative list lives in the company's PM judgment reference. The standing set:

1. Fair Housing responses of any kind — see `fair-housing-guard`
2. Reasonable-accommodation and assistance-animal matters
3. Trust-account variances above {{trust_variance_broker_threshold}} <!-- B14: dollar size that goes straight to the broker -->, and **any** variance that looks like more than an error
4. Management-agreement terminations, amendments, or disputes
5. Fee concessions and waivers
6. Staff discipline and employment matters
7. Legal demand letters and attorney contact — **broker and counsel, same day it arrives**
8. Anything with a real-estate-commission or licensing dimension
9. Emergency spend above {{broker_emergency_threshold}} <!-- B3: cost at which the broker is looped in even on an emergency --> — the broker is looped in even on a genuine emergency
10. Owner-relationship risk severe enough to threaten the account
11. Any instruction that would vary criteria, pricing, or availability along a protected-class line
12. Anything the PM judgment reference marks broker-only that is not on this list — the reference wins

## How a route looks

The seat carries the matter. It does not argue it, summarize its merits, or soften it.

- **What arrived**, factual, with the original text or document attached
- **When it arrived**, local time
- **What class** it falls in, and why in one line
- **What has been done**: nothing of substance. State that explicitly
- **What is waiting on the answer**, and what clock is running

Then log it:

```bash
cortextos bus log-event action matter_routed info \
  --meta '{"class":"broker_only","subclass":"<which of the twelve>","to":"broker","item_id":"<id>","substance_sent":false}'
```

## The same-day rule

Same day means same day. Not next business day, not "first thing tomorrow", not "after the Daily Pulse". {{broker_channel}} was chosen at onboarding precisely because it gets read the same day (A3) — if it is not being read, that is a `phase_zero` problem to raise, not a reason to hold the matter.

## The PM is not a stop on the way

A broker-only matter does **not** go to {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> first and then onward. It goes to the broker, and the PM is informed that it went. Routing it "through" the PM adds a delay to a class that exists specifically to avoid delay.

## Tracking

A routed matter stays on Escalation Triage until it closes. The broker's answer is a decision: it gets filed in {{decision_log_location}} <!-- D7: where the decision log lives --> like any other, with the broker named as decider.

## Never

- Never assess whether a broker-only matter is "actually serious" before routing. That assessment is the decision you are not allowed to make
- Never batch broker-only items into a daily digest. They go one at a time, on arrival
- Never send substance while waiting for the broker — not to the tenant, not to the owner, not to the vendor
