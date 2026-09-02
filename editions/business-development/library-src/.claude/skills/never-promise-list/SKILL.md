---
name: never-promise-list
description: "Check this BEFORE saying any number, date, timeline, outcome, or coverage amount to an owner — in a call, an email, a text, or a staged draft. It is the complete list of commitments this seat is never authorised to make, at any stage, to any owner, with the authorised alternative wording for each. There is no approver for anything on this list; it is not escalated, it is simply not said."
triggers: ["never promise", "can I say", "can I promise", "guarantee", "how long will it take", "how much will it rent for", "will it lease", "cash flow", "days to lease", "eviction timeline", "what does it cover", "can I commit", "is this ok to say"]
---

# The Never-Promise List

**These have no approver.** Everything else in this seat escalates to somebody. These do not — the manager cannot authorise them, the broker cannot authorise them, and a good relationship with the owner does not soften them.

**Why they matter more than they feel like they do:** every one of these feels harmless in the moment, said to a friendly owner, in the flow of a good conversation. Each becomes an expectation, then a complaint, then a dispute — and the person holding it is never the one who said it.

**When to check:** before any number, date, timeline, outcome, or coverage amount leaves your mouth or your draft. Not after writing it. Not at the release gate. Before.

---

## Leasing and Vacancy

| Never | Why | Say instead |
|---|---|---|
| A specific number of days to place a tenant | Market, condition, and price all move it, and none of them are yours | "Our marketing is built to lease quickly. Well-priced, rent-ready properties here typically go in [`quotable_standards.typical_days_to_lease`] <!-- D10 -->. We'll know inside two weeks whether we're priced right." |
| A specific placement date | Same, with a calendar attached | "Once it's rent-ready and listed we move fast. I can't give you a date, but we don't let properties sit." |
| That it will lease inside any window | A guarantee you cannot back is a financial liability | Reference a leasing guarantee **only** if `packages.leasing_guarantee_program.exists` is true for that market <!-- B5 -->. Otherwise there is nothing to reference |
| That the placement fee will be waived or reduced if it takes too long | That is a fee modification | "I can't commit to that, but let me tell you what we do to keep it moving." → `fee-and-contract-gates` |

## Rent and Financial Performance

| Never | Why | Say instead |
|---|---|---|
| A specific rent amount | The market sets it | "Based on the analysis the range is [range, with its pull date]. We'll price to maximise your return and adjust quickly if the market says otherwise." |
| That the owner will net a specific monthly figure | Vacancy, maintenance, fees, and the market all move it | "Let me walk you through the maths — market rent, our fees, typical maintenance. These are estimates, not guarantees." |
| That the property will cash-flow positively | With a high mortgage it may not | "Let's run the numbers together so you have a realistic picture before we go further." |
| That rent will rise at renewal | The market decides | "We'll run a fresh analysis at renewal and recommend the right rate then." |

## Maintenance and Condition

| Never | Why | Say instead |
|---|---|---|
| That the tenant will look after the property | Behaviour cannot be guaranteed — only screening and inspection frequency | "We screen carefully and we inspect on a schedule. We can't guarantee behaviour, but we catch things early and hold tenants accountable." |
| That maintenance costs will stay under a figure | HVAC fails, roofs leak | "We troubleshoot before dispatching and use vetted vendors, and anything above [`agreement_terms.maintenance_auth_threshold`] <!-- B10 --> needs your approval. I can't cap what the property will need." |
| That the owner's own vendors will be used | The vetting process exists for liability reasons | "We have a vetted network. If you've got someone you trust we can evaluate them, but I can't promise we'll use them before they've been through the process." |
| That a specific repair completes by a specific date | Vendor availability, parts, access | "We'll move as fast as we can. I can't give a date until the vendor's scheduled, but you'll know at each step." |
| That the property comes back in the condition it went out | Normal wear is the owner's by law in most markets <!-- confirm via counsel --> | "We document condition thoroughly at both ends and hold tenants accountable for damage beyond normal wear. Some wear is expected and isn't recoverable." |
| That inspections catch everything | They are visual and periodic | "We inspect at [`quotable_standards.inspection_schedule`] <!-- D11 -->. That's a strong baseline and catches most things early — it isn't a guarantee nothing gets missed." |

## Communication and Owner Experience

| Never | Why | Say instead |
|---|---|---|
| Weekly calls, or any cadence outside the standard model | Ops cannot sustain a bespoke cadence, and when it lapses it becomes the complaint | "Our standard is [`quotable_standards.owner_update_cadence`] <!-- D12 -->, plus portal access so you can see everything in real time." |
| That someone will always be reachable immediately | Depends on staffing, hours, urgency | "There's a line for maintenance emergencies. For non-emergencies we respond within [`quotable_standards.nonemergency_response_sla`] <!-- D12 -->." |
| That the owner will never be surprised by a cost | Emergencies and market shifts exist | "We won't spend above [threshold] without your approval on non-emergency work. But surprises do happen in this business — our job is to minimise them and tell you fast." |
| That the owner is consulted on every decision | That is co-management, and on tenant decisions it is a fair housing exposure | "You're consulted above your maintenance threshold and on major lease decisions. Day-to-day is ours — that's what you're paying for." |
| **"We handle everything"** | The most dangerous sentence in the seat. It sets an expectation of perfection nobody can meet | "We handle the heavy lifting — marketing, screening, maintenance, rent collection, compliance. You'll still be in it for the major decisions. But we make it as hands-off as it gets." |

## Legal and Compliance

| Never | Why | Say instead |
|---|---|---|
| That an eviction resolves in a given timeframe | Court timelines are not yours | "We file quickly and follow the process precisely. Timelines depend on the court — typically [`quotable_standards.eviction_timeline_range`] <!-- D12 --> here, but I can't promise a date." |
| That the owner will win an eviction or a deposit dispute | Outcomes belong to the court | "We document everything to give you the strongest position. The outcome is the court's; I can't promise a result." |
| That screening prevents all bad tenants | No process is perfect | "Our [`quotable_standards.screening_point_count`] <!-- D10 -->-point screening removes the large majority of high-risk applicants. No screening guarantees behaviour — that's what the protection programs are for." |
| That a specific applicant can be rejected for a reason outside the criteria | Fair housing exposure | "Applicant decisions run on objective criteria. I can't promise a specific person will or won't be approved." → and if the owner pushes, `fair-housing-guard` |
| That the protection programs cover everything | They have defined limits | Quote `packages.protection_program_terms_verbatim` <!-- B6 --> word for word, including what it does not cover |

## Fees and Contract Terms

| Never | Why | Say instead |
|---|---|---|
| That fees will never rise | Structures change | "Our current structure is [tiers]. You'd always get notice of any change." |
| That they can cancel any time with no consequence | The agreement has a notice period for a reason | "The agreement has a [`agreement_terms.termination_notice_period`] <!-- B11 --> notice requirement, and we offer a [`agreement_terms.satisfaction_guarantee_window`] satisfaction window." **Never say cancel-anytime.** Quote the actual clause |
| A referral fee amount or timing without a signed agreement | Verbal referral commitments become disputes | "Referral fees go into a signed agreement before they're paid. Let me get you the details in writing." <!-- B9 --> |
| That the fee covers a service outside the standard agreement | Scope creep starts here, in one sentence, at an appointment | "Everything we do is in the agreement. If you need something outside that we can talk about it, but let's be clear on what's included before signing." |

---

## The Two Tests

**Test one: who keeps this?** If it is anyone but you — operations, maintenance, accounting, a court, the market — it is not yours to promise.

**Test two: could it be wrong through no fault of anyone?** If yes, it is a forecast. Say it as one, with its source, or do not say it.

---

## When The Config Is Empty

**An empty field is not a gap to fill with the generic example.** It is a claim the seat may not make.

If `quotable_standards.typical_days_to_lease` is blank, there is no typical number to quote — not a rough one, not "usually around". The honest line is short:

> "I don't have a number I'd stand behind for that, and I'd rather not guess. Let me find out and come back to you."

That sentence costs less than any number in this document.
