---
name: pricing-presentation
description: "Load this before presenting a rental rate, a package, a fee, or a guarantee program — and before answering any question about what something costs. It carries the rental-rate presentation, the three-tier package presentation, the setup fee and reserve framing, the close, and the hard rule that every number quoted comes from the configuration rather than from the generic example."
triggers: ["pricing", "present pricing", "packages", "management fee", "setup fee", "reserve", "rental rate", "rate presentation", "market analysis", "the close", "3-part close", "quote a fee", "what do we charge", "guarantee program", "protection program"]
---

# Presenting Rate and Price

Two presentations, in this order, always. The rate conversation comes first because it is about **their** asset, and the fee conversation lands very differently once the owner has already agreed the property is worth more than they thought.

---

## The Rule That Governs Every Number Here

**Every figure comes from `seat-config.json`. Never from the generic example, never from memory, never from what a similar company charges.**

An empty field is not a gap to fill with something sensible. It is a number you may not say. If `packages.leasing_guarantee_program.exists` is false in this market, there is no leasing guarantee to reference — not "something similar", not "we usually", not at all <!-- B5 -->.

And before any number, date, or outcome leaves your mouth: `never-promise-list`.

---

## Part 1 — The Rental Rate

Run the analysis first. The presentation is a conversation about their property, not a number delivery.

### The script
> "Here's what comparable homes near you have actually rented for recently. This is one of several inputs, not the whole answer.
>
> In your view — are these genuinely comparable to yours? Which ones look similar and which don't?
>
> So having seen what you're competing with: what price do you think creates real value in the eyes of a good tenant?
>
> Based on what we've looked at, my recommendation is [range, with the pull date]. Does that feel workable?"

**Why the questions come before the number:** an owner who has just looked at the comparables themselves arrives at roughly your number on their own. An owner handed a number arrives at an argument.

### When they want to start higher
> "Here's the useful part: we generally know inside the first couple of weeks whether we're priced right. If we're not, we adjust straight away. So let's start at [rate] and if the activity isn't there, we'll both know quickly."

### When they want it far above market
Above `acceptance.above_market_walkaway_pct` <!-- A4 -->, this is not a negotiation — it is a manager call before any agreement is sent. → `property-and-owner-gates`.

### Rate rules
- **A range, never a single number.** A single number is a promise wearing a recommendation's clothes.
- Always with its source and pull date. Write it to E10 that way.
- Never say what the property "will" rent for. Never say what the owner "will" net.
- Never adjust the analysis upward because the owner wants a bigger number. If two data sources disagree, carry both and say so.

---

## Part 2 — Packages and Fees

### The presentation
> "I can send the full breakdown, but here's the overview.
>
> We have [count] packages, from [low] to [high] per month per property <!-- B1 -->. That covers everything to do with the tenant and the property: rent collection, service calls, maintenance coordination, accounting, lease enforcement.
>
> There's a one-time setup fee of [setup fee] <!-- B2 --> to get the property into our accounting, maintenance, and management systems. And we hold a maintenance reserve of [reserve] <!-- B3 --> — that's your money, not a fee. It's what lets us act fast on a repair instead of waiting on an approval, which keeps a small problem small.
>
> The top package at [top package fee] <!-- B4 --> includes [only the programs actually configured]. Here are the written terms for each of those."

### Framing that matters
- **The reserve is the owner's money.** Say it that way — it is true and it removes the objection before it forms.
- **The setup fee buys onboarding, not paperwork.** Name what actually happens.
- **Guarantee programs are quoted from the written terms, word for word** <!-- B6 -->. Never paraphrase coverage upward. "Up to [amount] beyond the deposit" never becomes "we cover damage".
- **Only list programs that are actually run in that market.** `packages.top_package_included_programs` is the list. It is not a menu of things that would be nice to include.

### Rehab and make-ready
Charged per `packages.rehab_management` <!-- B8 -->. If the fields are empty, the service is not offered — do not describe the generic percentage-and-flat-fee structure as though it were the company's.

### Pets
Screening, monthly fee, and damage coverage from `packages.pet_policy` <!-- B7 -->. Any mention of a service, assistance, or emotional support animal exits this skill immediately → `fair-housing-guard`.

---

## Part 3 — The Close

Once rate and fees are agreed, the close is a summary of decisions the owner has already made, not a new ask.

> "Based on everything we've talked about, there are really only three parts to this — can I lay them out?
>
> One: do you want this property rented?
> Two: are you comfortable with the pricing we've landed on?
> Three: who do you want handling it?
>
> You've answered the first two. So the question is just the third one — and if the answer's us, we can get the agreement signed today and start."

**Close rules:**
- Never close on urgency you invented. No deadlines that do not exist, no "I can only hold this rate".
- Never close on a concession. If a fee had to move to get here, the fee has not moved — it has gone to the manager.
- If they do not sign, the agreement goes out the same business day with a hard follow-up date inside 24 hours. See `stage-gates` S4.

---

## What Never Gets Said In This Conversation

Straight from the Never-Promise List — the ones that come up specifically during pricing:

- A specific rent amount, or what the owner will net
- Days to lease, or a placement date
- That fees will never increase
- That they can cancel any time with no consequence <!-- B11 — quote the actual notice period -->
- That the management fee covers something outside the standard agreement
- A guarantee program that is not documented and approved in that market <!-- B5 -->
- Coverage described more broadly than the written terms <!-- B6 -->
- A referral fee amount or timing without a signed agreement <!-- B9 -->

Full list and the alternative wording for each: `never-promise-list`.

---

## If The Owner Asks For A Deviation

Any discount, waiver, match, or package change — of any size, including a one-time setup-fee waiver, including for an owner bringing several properties — goes to {{bd_manager_name}} <!-- C2, B12 --> before any answer reaches the owner.

> "That's a fair question and I want to give you the right answer rather than a fast one. Let me take it to [manager] and come back to you within {{escalation_turnaround}} <!-- B12 -->."

Then log it, then escalate. In that order. See `fee-and-contract-gates` and `escalation-log`.
