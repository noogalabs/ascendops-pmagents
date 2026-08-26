---
name: lead-intake
description: "Use this the moment any lead arrives — an inbound form fill, a call, a referral, or an outbound prospect you just found. It covers the speed-to-lead response, the board row, source tagging, the property-management-versus-redirect decision, duplicate handling, and the graceful decline for anything outside the model. Every lead enters through here; nothing skips straight to discovery."
triggers: ["new lead", "inbound", "lead came in", "speed to lead", "first response", "log a lead", "prospect found", "referral came in", "is this a PM lead", "redirect", "decline", "not a fit", "duplicate lead", "disqualify"]
---

# Lead Intake

Every lead enters here. Nothing goes straight to discovery, and nothing sits in an inbox as "I'll log it later" — a lead that is not on the board does not exist, and the speed-to-lead clock starts when it arrives, not when you notice it.

---

## Step 1: Respond, Then Log — In That Order

On inbound, the response goes out inside the speed-to-lead window. This is the single largest conversion lever in the seat and the difference is not marginal.

**In shadow mode or with the class locked, "respond" means stage the response and flag it for immediate release** — say so explicitly rather than letting it sit in a queue. A staged speed-to-lead response that waits four hours for a routine release is the same as no response. If the release is not going to be immediate, tell {{bd_manager_name}} <!-- C2 --> so a human can pick up the phone.

On outbound, log the attempt the same minute you make it.

---

## Step 2: The Row

Minimum fields to exist in S0: A2 date created, B1–B4 contact, C1 address, D1 lead source, D5 inbound or outbound.

**D1 comes from the list, never typed.** Source attribution is the input to every ROI decision the company makes about where to spend. A row tagged "other" because the exact source was not in the dropdown is a row that silently argues against the channel that produced it. If the source is genuinely new, add it to `platform.company_specific_lead_sources` <!-- D2 --> and regenerate the list.

---

## Step 3: Duplicate Check — Before Anything Else

Same owner plus same property already on the board? Then this is not a new deal.

Merge the new information into the surviving record, note the merge in G10, and archive the duplicate <!-- D5 -->. A duplicate that survives inflates the pipeline count, splits the touch history so both rows look cold, and produces two people calling the same owner.

Same owner, **different** property is a genuinely new row. That is the one-row-per-owner-per-property rule doing its job.

---

## Step 4: Is This Even A Property Management Deal?

Set E6 before doing anything else with it.

| E6 | What it means | Where it goes |
|---|---|---|
| PM Lead | Owner wants a property managed | Continue to discovery |
| Brokerage Redirect | They want to buy or sell | Warm handoff to the brokerage recipient <!-- C8 --> |
| Investment Redirect | They want investment services | Warm handoff to the investment recipient <!-- C8 --> |
| Disqualified | Fails the gates below | Graceful decline, then LOST |

**A redirect is a warm handoff, not a forward.** Introduce the person by name, say what the owner is looking for, and confirm the receiving side has it. Then REDIRECTED tab. If the company has no brokerage or investment arm, `people.redirect_recipients` names an outside partner or says "none" — and "none" means the decline script, not silence.

---

## Step 5: The Gates

Check before booking anything:

| Gate | Source | If it fails |
|---|---|---|
| Inside the service area | `markets.service_area_boundary` <!-- A3 --> | Decline gracefully, refer out |
| At or above the minimum rent | `acceptance.minimum_rent_threshold` <!-- A3 --> | Decline gracefully, refer out |
| An accepted property type and condition | `acceptance.*` <!-- A4 --> | Condition issues → `property-and-owner-gates`, not a self-service decline |
| Rent expectation within the walk-away margin | `acceptance.above_market_walkaway_pct` <!-- A4 --> | Manager call before any agreement — never yours alone |

**The split that matters:** service area and minimum rent are objective and the seat may decline on them directly. Condition, violations, and above-market rent demands are **judgment calls that belong to {{bd_manager_name}}** <!-- C2 -->. Never merge the two. "It's outside our area" is a fact. "This property is going to be a problem" is a decision.

---

## Step 6: The Graceful Decline

Where the seat may decline directly — area and minimum rent — the decline is warm, honest, and useful:

```
It looks like this one falls outside what we're set up for — [the specific,
factual reason]. I'd rather tell you that now than take it on and give you a
result that doesn't match what you're expecting.

I do know a couple of managers who might be a better fit for this property.
Want me to pass along their names?
```

Then: E7 disqualify reason, G4 lost reason, and the referral names from `people.decline_referral_partners` <!-- C9 -->.

**Rules for every decline:**
- Never say the reason is the person. Use the property or the model — this is true and it is also what keeps a declined owner referring people to you.
- Never decline a property on condition or rent expectation without the manager. That decision goes up first <!-- C2 -->.
- Never decline for anything protected-class-adjacent through this script. That is `fair-housing-guard`, and it routes to counsel the same day.
- Log every decline with its reason. A decline with no reason on the board is indistinguishable from a lead that was dropped.

---

## Step 7: Exit To S1

Live contact made and a discovery call on the calendar → move to S1, update A6, set F15 and F16. See `stage-gates` and then `discovery-call`.

If contact is not made, the attempt ladder runs to `clocks.max_contact_attempts` over `clocks.max_attempt_window_days` <!-- D5 -->, then the record archives as unresponsive. Every attempt is logged — the count is what makes "unresponsive" a fact instead of an impression.
