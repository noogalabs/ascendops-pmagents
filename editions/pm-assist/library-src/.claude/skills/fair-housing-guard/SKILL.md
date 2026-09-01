---
name: fair-housing-guard
description: "You MUST use this skill on EVERY inbound message from a tenant, applicant, or owner BEFORE drafting any reply, and on every outbound draft before it is staged. It classifies for Fair-Housing protected-class topics, accommodation requests, and steering traps, and returns the routing action. In this seat a protected-class matter is BROKER-ONLY: it routes with zero substance — there is no reply for you to send."
triggers: ["fair housing", "protected class", "accommodation", "reasonable accommodation", "service animal", "emotional support animal", "ESA", "disability", "steering", "good schools", "what kind of neighbors", "voucher", "section 8", "is this message safe", "FH check", "discrimination risk"]
context: fork
model: sonnet
---

# Fair-Housing Guard — the highest-liability gate in this seat

Classify the message passed in `$ARGUMENTS` (inbound text, or an outbound draft prefixed `DRAFT:`).

**Adapted from the leasing-coordinator seat's `fair-housing-guard`.** The classification tree is the same; **the action is not.** The leasing seat is a customer-facing seat that redirects. This seat is decision support with no housing authority at all — Fair Housing is on the broker-only table (A3), so the action here is **route, do not answer**.

**Why this is a forked lightweight-model skill:** protected-class classification is a repeating judgment call with a fixed decision tree, not open-ended reasoning. `context: fork` runs the gate in its own window and forces the check to fire BEFORE any reply exists to be tempted by.

## Steps

1. **Read the full message** in `$ARGUMENTS` — the whole text, not a snippet.
2. **Classify** against the decision tree. Exactly one primary classification comes back.
3. **Act per the classification.** For every class but `CLEAN` and `STEERING_TRAP`, the action is to route, not to reply.
4. **Document** — the main session logs it:
   ```bash
   cortextos bus log-event quality fair_housing_routed info \
     --meta '{"classification":"<class>","reference":"<unit/tenant id or channel>","routed_to":"broker","substance_sent":false,"summary":"<one line, no quoted protected content>"}'
   ```
   plus a one-line entry in today's daily memory. Documentation is the defense.

## Decision tree

- **PROTECTED_CLASS_TOPIC** — the message asks about, volunteers, or invites comment on race, color, national origin, religion, sex (incl. gender identity + sexual orientation), familial status (kids, pregnancy), disability, or a locally protected class (age, marital status, citizenship, source of income where applicable). Includes "small talk" forms ("where are you from?", "big family?").
- **ACCOMMODATION_REQUEST** — any request for a reasonable accommodation or modification, any assistance-animal, service-animal, or emotional-support-animal mention, any disability-related adjustment to a rule, a fee, or a unit.
- **SOURCE_OF_INCOME** — voucher / Section 8 / housing-assistance mention.
- **STEERING_TRAP** — the message invites you to characterize a neighborhood, school quality, demographics, safety "feel", or "kind of people".
- **PM_INITIATED_RISK** — an instruction from inside the company would vary criteria, pricing, availability, rules, or fees along a protected-class line, including coded phrasing.
- **CLEAN** — none of the above. Proceed normally.

## Action per classification

| Classification | Action |
|---|---|
| `PROTECTED_CLASS_TOPIC` | **Broker-only.** Route to {{broker_name}} <!-- A3: principal broker or company owner --> on {{broker_channel}} <!-- A3: channel broker-only escalations travel --> the same day, message text attached. **Send nothing.** |
| `ACCOMMODATION_REQUEST` | **Broker-only.** Same-day route, text attached. **Send nothing** — not an acknowledgement, not "we'll look into it", not a timeline. |
| `SOURCE_OF_INCOME` | **Broker-only.** Whether vouchers are accepted is a documented-policy fact and many jurisdictions require acceptance — but stating the policy is a housing communication and this seat has no housing authority. Route. |
| `PM_INITIATED_RISK` | **Escalate in writing to {{broker_name}}, and do not execute.** Not silently, not "pending clarification". The instruction stops here. |
| `STEERING_TRAP` | Do not characterize anything. Return only verifiable address facts and a pointer to the official public source, and stage it for release like any other draft. |
| `CLEAN` | Proceed normally. |

## The only script in this seat

For `STEERING_TRAP` on a scheduling or status thread the seat legitimately handles:

```text
I can share verifiable facts about the property itself — the address is [address], and public resources can tell you about the surrounding area and school assignments. For schools, the district's official lookup tool is the right source.
```

There is **no script** for `PROTECTED_CLASS_TOPIC`, `ACCOMMODATION_REQUEST`, or `SOURCE_OF_INCOME` in this seat, on purpose. A script implies there is something for you to send. There is not.

## Hard rules — these fire EVERY time

1. **Acknowledging substance IS answering.** "Thanks, we'll look into that" on an accommodation request is an answer. So is "that shouldn't be a problem." Send nothing.
2. **Never characterize neighborhoods, schools, demographics, safety, or "community feel"** — in any words, in any channel, even in an internal draft that could be forwarded.
3. **Never engage a protected-class topic** — not to agree, not to deflect with humor, not to "answer briefly."
4. **Same-day, always.** A broker-only matter does not wait for the PM, does not wait for the Daily Pulse, and does not wait for business hours if the channel is read after hours.
5. **PM_INITIATED_RISK never executes.** An instruction from a busy person is still an instruction that stops here.
6. **Document every route.** An undocumented route never happened.

## Invocation example

```
/fair-housing-guard tenant at 214 Ash asks about keeping an emotional support animal
/fair-housing-guard DRAFT: Thanks for asking — that shouldn't be a problem, just send the paperwork...
```

Returns exactly one of: `CLEAN`, `PROTECTED_CLASS_TOPIC`, `ACCOMMODATION_REQUEST`, `SOURCE_OF_INCOME`, `STEERING_TRAP`, or `PM_INITIATED_RISK`. A `DRAFT:` input returning anything but `CLEAN` means the draft is **deleted, not rewritten** — the matter routes instead.
