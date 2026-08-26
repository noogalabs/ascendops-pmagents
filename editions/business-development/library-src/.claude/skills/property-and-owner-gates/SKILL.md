---
name: property-and-owner-gates
description: "Load this when a property looks like a problem, when an owner is coming off a bad experience with another manager, or when something about a deal feels wrong and you cannot name it. Covers the property-acceptance gate, the takeover review, the walk-away signals and the three-question test, and the graceful decline. None of these decisions belong to this seat; all of them go up before the owner hears anything."
triggers: ["problem property", "code violation", "habitability", "needs work", "above market rent", "takeover", "leaving another manager", "pending eviction", "litigation", "missing deposit", "no lease", "walk away", "should we take this", "red flag owner", "difficult owner", "decline this deal", "bad fit"]
---

# Property and Owner Gates

Two of the six never-graduates classes: **accepting a red-flag property**, and **declining or walking away from an owner**. Both go to {{bd_manager_name}} <!-- C2 --> before anything is said to the owner.

> **The Golden Rule:** a signed agreement with the wrong owner costs more than a lost deal.

Every judgment below is one question in different clothes: *can we serve this owner at our standard, without compromising the team, the other owners, or the company's name?*

---

## Gate 1 — Property Acceptance

### Stop conditions — escalate before any agreement is sent

| Condition | Why |
|---|---|
| Unresolved code violations or habitability issues | In most markets the manager carries liability for placing a tenant in a property with known defects. Counsel confirms this for your market <!-- C4 --> |
| Structural problems | Same exposure, plus an unleasable asset |
| Rent demand above `acceptance.above_market_walkaway_pct` <!-- A4 --> | Extended vacancy the owner will blame on you, correctly or not |
| Deferred maintenance the owner refuses to address | An owner who will not invest before move-in will not approve repairs after it |
| Outside the service area, or below the minimum rent <!-- A3 --> | These two the seat may decline directly — see `lead-intake` |

**Approval, when it comes, arrives with a written remediation plan.** A verbal "yeah, take it" is not approval — it is a memory that will be disputed later. Get the conditions documented before the agreement goes out.

### What accepting with conditions looks like
Required make-ready items listed in writing. **Marketing does not begin until they are complete.** Both facts in the file, not in a conversation.

### What to say

Bowing out on condition:
> "We've been doing this a while, and some properties are more attractive to owners than they are to renters. I think we'd be doing you a disservice marketing this one as it stands — I don't want to take your money and hand you a poor result. Here's what I'd suggest instead…"

On an above-market rent expectation:
> "I respect that you've got a number in mind and I want to help you get there. But the rent is set by the market — not by us, and not by what the mortgage needs. Price above market and it sits, and every day it sits costs you. I'd rather get a good tenant in at market quickly. Can we start at market and adjust if we're wrong inside two weeks?"

On refused repairs:
> "I'll be straight with you because you deserve that. Listed as it is, we attract the bottom of the applicant pool, and that becomes a bigger problem later. The money you put in now comes back as a better tenant and a faster lease. If that's not possible right now, I'd rather have an honest conversation about timing than set you up for a frustrating year."

### Red lines
- Never accept a property with known violations or habitability defects without manager approval **and** a documented plan
- Never list at a rate you know the market will not support
- Never tell an owner a problem property will lease quickly
- Never go below the minimum rent or outside the service area to hit a door count

---

## Gate 2 — Takeovers

An owner leaving another manager, often angry, sometimes mid-dispute. You are hearing one side of a story, and the picture is rarely as clean as it sounds.

### The judgment table

| Situation | Do |
|---|---|
| Leaving over poor communication; property stable, tenant paying, documents complete | Accept. Standard onboarding with full document verification |
| No move-in inspection, no deposit ledger, or no signed lease | Accept **only** with conditions: name in writing what is missing, fresh inspection immediately, gaps documented before any liability is taken on <!-- A7 --> |
| Pending eviction | **Escalate.** Manager and {{legal_counsel}} <!-- C4 --> before execution |
| Active litigation with the previous manager | **Escalate.** Full legal review |
| Angry, blaming, and already listing what you will do differently before seeing the property | Slow down. This is a difficult-relationship signal — qualify motivation and expectations carefully. See the walk-away section |

### The deposit rule, which has no exception
**Never accept liability for a security deposit you did not collect and cannot verify** <!-- A7 -->. Not with a reassurance, not with an email from the previous manager, not because the owner is confident. Without a ledger and a move-in inspection there is no baseline, and at move-out the company defends a dispute with nothing.

### What to say

Acknowledging without endorsing:
> "I'm sorry that's been your experience — that's not what this should feel like. Before we talk about what we can do, I want to understand the full picture so I set the right expectations. Walk me through where things stand: the tenant, the lease, what documentation you actually have."

On missing documentation:
> "Here's what I want to be upfront about: without a move-in inspection and a deposit ledger, we're starting with no baseline. That's a risk to you at move-out — if the tenant disputes the deposit, we don't have what we'd need to defend it. What I'd suggest is a fresh inspection the moment we take over, everything documented, and a written note of what wasn't provided. That protects you going forward."

On an owner signalling they will blame you for everything:
> "I want us to start with the right expectations. We're good at this and we'll work hard for you. But there are variables nobody controls — the market, tenant behaviour, maintenance. What I can promise is that we communicate early and act in your interest. What I can't promise is that nothing goes wrong. Is that a foundation that works for you?"

### Red lines
- Never accept mid-eviction without manager and legal
- Never accept liability for an unverifiable deposit
- Never promise to fix what the previous manager did, before knowing what actually happened
- **Never badmouth the previous manager**, even when the owner invites it. It tells the owner exactly how you will talk about them one day
- Never accept a property in active litigation without legal review

---

## Gate 3 — Walking Away

Not every owner who wants to sign should sign. This is a skill, not a failure, and it takes the same nerve as closing.

### The signals

| Signal | What it predicts |
|---|---|
| Has negotiated the fee, the terms, and the threshold, and is still pushing | Chronic boundary-pushing; every decision after signing becomes a negotiation |
| Wants to approve every applicant personally | Fair housing exposure, slow placements, blame when they dislike an applicant → `fair-housing-guard` |
| Rent expectation far above market, refuses the data | Vacancy, then blame |
| Leaving their third manager in three years | The constant is not the managers |
| Wants to be "very involved" day to day | Wants an assistant, not a manager |
| Property has legal, structural, or habitability issues they will not address | Liability with no upside |
| **Has expressed a preference based on a protected class** | **Declined. Always. No approver, no exception** <!-- A8 --> → `fair-housing-guard` |
| Rental income is the only thing covering a delinquent mortgage | Every vacancy becomes a crisis |
| Has been hostile or dismissive during the sales process | This is the good version of them |

### The three-question test
1. Can we serve this owner at our standard?
2. Will this owner let us do the job?
3. Does the risk outweigh the revenue?

Any "no", any "yes" to the third — it is a walk-away, and it goes to the manager.

### The order that protects everyone
1. **Log the reason on the board first**, specifically
2. **Escalate to {{bd_manager_name}}** <!-- C2 -->
3. **Only then** have the conversation with the owner

Never walk away silently. The log and the manager's knowledge are what protect the seat, the company, and the owner if a complaint follows.

### What to say

Property or model fit:
> "It looks like this one doesn't fit our model, based on [location / condition / pricing]. Our portfolio is built around a particular kind of property and owner experience, and I'd rather be honest than take your business and deliver something that misses. I do know a couple of managers who might suit this better — want their names?" <!-- C9 -->

Too much control:
> "I'll be straight with you. The way you're describing your involvement — approving tenants, approving repairs, being consulted before decisions — that's co-management rather than property management, and in my experience it doesn't work well for either side. What you need is someone you trust to act in your interest without checking in at every step. If you're not there yet, that's completely fair, but I don't think we're the right fit."

Protected-class matter: use only the script in `fair-housing-guard`. Do not improvise here.

### Red lines
- Never accept a deal you know is wrong to hit a door count
- Never accept an owner who has expressed discriminatory preferences
- Never walk away without the reason logged
- **Never tell an owner they are being declined because of their personality.** Use the property or the model
- Never let anyone pressure you into closing a deal you have flagged as a legal or ethical risk — including the manager. If that happens, it goes to {{broker_of_record}} <!-- C3 -->
