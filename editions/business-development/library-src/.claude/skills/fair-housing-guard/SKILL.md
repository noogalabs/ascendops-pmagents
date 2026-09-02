---
name: fair-housing-guard
description: "You MUST use this skill the moment an owner or prospect says anything touching who may live in a property — who they want, who they do not want, who they want to approve, who they want it marketed to. It classifies the statement, and where a class fires it stops the deal conversation and routes to counsel and the manager the same day. This seat has no fair housing authority: it never answers, never reassures, never steers around the subject. Pass the owner's exact words after the command."
triggers: ["fair housing", "protected class", "discrimination", "no students", "no kids", "no families", "no section 8", "voucher", "no pets service animal", "emotional support animal", "assistance animal", "I want to approve every tenant", "kind of tenant", "type of person", "who lives there", "steering", "accommodation request", "owner preference"]
context: fork
model: sonnet
---

# Fair-Housing Guard — the highest-liability gate on this seat

Classify the statement passed in `$ARGUMENTS` — an owner's words, a prospect's words, or an outbound draft prefixed `DRAFT:`.

**Adapted from the leasing seat's guard.** The classification tree carries. The *action* inverts. The leasing seat is customer-facing and holds screening authority, so it redirects with a script and keeps the conversation moving. **This seat has no housing authority at all.** Here, a fired class does not get a script that continues the conversation — it stops it and routes it. That difference is deliberate: a smooth reply from a seat with no authority is exactly how a company ends up bound to something it never agreed to.

**Why forked:** this is a repeating judgment call against a fixed tree, and it has to fire *before* a reply exists to be tempted by. A guard that runs after the draft is written is not a guard.

---

## Steps

1. **Read the full statement** in `$ARGUMENTS`. The whole thing, not a fragment. Context changes classification.
2. **Classify** against the tree below. Exactly one primary classification comes back.
3. **If any class fires**, return the classification, the exact words that triggered it, and the routing instruction. **Return no reply script for the deal conversation.** There is nothing for this seat to say about the substance.
4. **The main session then**: logs the owner's exact words verbatim on the board, routes to {{legal_counsel}} <!-- C4 --> and {{bd_manager_name}} <!-- C2 --> the same day, and says nothing further on the subject.

---

## Classification Tree

| Class | What it looks like | Fires? |
|---|---|---|
| `PROTECTED_CLASS_PREFERENCE` | The owner states a preference for or against occupants by race, color, national origin, religion, sex, familial status, disability, or any class protected in the market <!-- A8 -->. Includes the softened forms: "the right kind of family", "people who fit the neighborhood", "someone quiet, you know what I mean" | **YES** |
| `AGE_OR_STUDENT_RESTRICTION` | "No students", "no college kids", "nobody under thirty", or any age-bounded request | **YES** — and note that A8 asks specifically about this; even where a lawful exemption exists in a market, the answer comes from counsel, never from this seat |
| `FAMILIAL_STATUS` | "No children", "adults only", "not good for kids" | **YES** |
| `ASSISTANCE_ANIMAL` | Service animal, assistance animal, emotional support animal — including "my pet policy covers that, right?" | **YES**. This is never a pet-policy question, no matter how it is phrased, and the pet script in `pricing-presentation` does **not** apply |
| `ACCOMMODATION_REQUEST` | A request for a modification or accommodation, from either side | **YES** |
| `SOURCE_OF_INCOME` | Vouchers, housing assistance, subsidy programs — where the market protects it | **YES** |
| `TENANT_APPROVAL_RIGHTS` | The owner wants to personally approve or reject individual applicants <!-- judgment §4 --> | **YES** — this is a fair housing exposure wearing a contract-term costume. It is *also* a contract modification: route to counsel **and** to {{broker_of_record}} |
| `STEERING_ADJACENT` | Marketing questions about schools, "neighborhood character", "the kind of area", or targeting where marketing goes | **YES** |
| `SCREENING_CRITERIA_QUESTION` | A neutral question about the screening process itself: what is checked, what the criteria are | **NO** — answer from `quotable_standards` in `business-development-config.json` only, and only what is documented there. If nothing is documented, say nothing is documented. Never describe criteria you have not read |
| `CLEAR` | Nothing above fires | **NO** |

When two classes could apply, the more protective one fires. When you are genuinely unsure, it fires.

---

## What The Seat Says When A Class Fires

One line, then stop. Do not soften it, do not explain the law, do not offer a workaround, and do not say the word "policy" — this is not policy.

```
I have to be straight with you: that's not something we can do. Fair housing rules
mean every applicant gets evaluated on the same objective criteria, and that's not
something I'm able to work around. Let me get you a proper answer from the right
person rather than a fast one from me.
```

Then route. Same day.

**If the owner presses**, the answer does not change and does not expand. A second sentence explaining *why* is a legal opinion from a seat that has none.

**If it is clear this is a requirement of working together**, that is a walk-away — and like every walk-away, the reason is logged first and the decision goes to {{bd_manager_name}} before the final conversation <!-- C2 -->.

---

## Hard Rules

1. **There is no approver for the substance.** No manager, no broker, no config value makes a protected-class preference workable. This is the one gate with no override anywhere in the seat.
2. **Silence is not safe here.** Not routing a fair housing matter is its own liability. If the owner said it, it gets logged and routed — including when they laughed it off, including when they took it back, including when you are sure they did not mean it.
3. **Log the exact words.** Not your summary of them. The verbatim quote is what counsel needs and what protects everyone if it is ever disputed. This is the one place the board carries a direct quote of an owner.
4. **Never record it as a decline reason in the dropdown.** The board's lost-reason field is a business field. A protected-class matter is routed to counsel and referenced by escalation id, not categorised into a metrics tab.
5. **The prevention question stays neutral.** Never ask an owner what kind of tenant they are looking for. The question invites the answer that ends the deal.

---

## Documentation

The main session logs every fire:

```bash
cortextos bus log-event action fair_housing_gate_fired info \
  --meta '{"agent":"'$CTX_AGENT_NAME'","class":"<CLASS>","escalation_id":"<id>","routed_to":"counsel+manager"}'
```

Board row: escalation id, date and time, class, the verbatim words, who it was routed to, and when. No summary in place of the quote.
