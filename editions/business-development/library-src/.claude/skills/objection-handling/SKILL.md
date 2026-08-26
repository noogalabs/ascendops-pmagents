---
name: objection-handling
description: "Load this the moment an owner pushes back on anything — price, timing, a competitor's quote, needing to think, needing to ask a partner, a friend in the business, the contract, the property's condition. It carries the diffuse-never-rebut framework and the response for each common objection. Also carries the competitor-pricing conversation, which is the objection this seat gets most and handles worst when unprepared."
triggers: ["objection", "pushback", "too expensive", "fees too high", "need to think", "talk to my spouse", "just looking", "not ready", "competitor", "cheaper", "another company quoted", "friend is a property manager", "bring me a tenant first", "contract is complicated", "not interested", "what's your fee"]
---

# Objections

An objection is not an attack to win. It is a signal of unresolved concern, and it is usually the most useful thing the owner will say all call.

## The Framework: Diffuse, Never Rebut

1. **Acknowledge** neutrally. "Fair enough." "That's a reasonable thing to ask."
2. **Clarify as a question.** Reflect it back so they expand it. *"When you say it's more than you expected — more than what you had in mind, or more than someone else quoted?"*
3. **Let them resolve it.** Most objections dissolve when the owner hears themselves explain them. The ones that do not have now been made specific, which is the only form you can actually address.

**Never rebut. Never argue. Never win.** A rebutted objection goes underground; it does not disappear. It reappears as silence after the appointment.

---

## Before You Answer Any Of These

Ask one question first: **does answering this require a fee or a term to move?**

If yes, it is not an objection — it is a request, and it goes to `fee-and-contract-gates` before you say anything. Nothing below authorises a discount, a waiver, a match, or a clause change, and the responses are written specifically so they do not need one.

---

## The Responses

### "Your fees are higher than the competition"
> "I can see why that's a concern. What our owners tend to find is that it costs less over the life of the lease — the real costs in this business are vacancy, damage, evictions, and surprises. Managing those well is where the money actually goes. What part of the value are you still unsure about?"

Never match. See the competitor section below.

### "It's more than I expected to pay"
> "How were you thinking about it? What number did you have in mind?"

Then listen. This is information, not a negotiation opening — and it is not an invitation to move toward the number. If it turns into a real request, it goes to the manager.

### "I need to think about it"
> "Absolutely. What specifically do you want to think through — the pricing, the services, or something else? I'd rather answer it now than have you sitting on a question I could have handled."

### "I need to talk to my spouse / partner"
> "Of course. When's a good time for the three of us to get on a quick call together? I want to make sure their questions get answered directly rather than through you."

> This one is preventable. Identify every decision-maker in discovery and confirm attendance before the appointment. See `discovery-call`.

### "We're not ready yet"
> "Understood. What timeframe are you working toward? And when you are ready, what will matter most to you in a manager?"

Then nurture properly, with a hard date. See `followup-and-nurture`.

### "We're just looking right now"
> "That's smart — you should look properly before deciding. Out of curiosity, what are you looking for in a management company?"

### "A friend / family member is a property manager"
> "I understand — most people have someone they feel some obligation to. The only thing I'd ask is whether mixing it with a personal relationship might make it harder to have the difficult conversations. It can be tough to hold someone accountable when you care about them. Would you be open to at least comparing?"

### "Bring me a tenant first, then we'll talk"
> "We might well have someone, but we won't know until we've seen inside. When would be a good time to take a look?"

### "Your contract is too complicated"
> "Whoever manages this property is responsible for protecting the asset and keeping you out of legal trouble, and every clause in there exists for a reason. I'm happy to walk through any of them and explain what it does."

Explaining a clause is yours. Changing one is not — see `fee-and-contract-gates`.

### "We're taking it off the market"
> "I hear you. If I'd brought you a well-qualified tenant yesterday, would you still have rented it? Let's just take fifteen minutes. If the plan makes sense, great; if not, it was fifteen minutes."

### "What's your fee?" — asked too early
> "Good question, and I want to give you an answer that's actually useful. It depends on what you need. Can I ask a couple of quick things about the property first so I can give you the right number rather than a range?"

### "My property needs a lot of work"
> "Two ways to go. We can manage the rehab — we act as your point of contact with the vendor network and drive it. Or you handle the work and we pick up once it's rent-ready. Which fits your situation better?"

Rehab management pricing comes from `packages.rehab_management` <!-- B8 -->. Do not quote the generic structure; quote what is configured. If it is not configured, it is not offered.

### "We're not interested"
> "Of course you're not — I haven't given you enough to be interested in yet. Can I just ask you one thing…"

Then a situation question. One attempt, then let it go gracefully. A second attempt is pressure.

### "I don't want pets"
> "Common concern. Here's how we handle it: [the configured pet screening process], a monthly pet fee that goes to you, and the property protection program covers [the configured damage amount]."

Quote only from `packages.pet_policy` <!-- B7 -->. **If the conversation turns to a service animal, an assistance animal, or an emotional support animal, it is not a pet conversation** — stop and go to `fair-housing-guard`.

### "I don't want students"
Do not answer this one. It is not a preference conversation. → `fair-housing-guard`, same day, counsel and manager <!-- A8 -->.

---

## The Competitor-Pricing Conversation

The most common objection at the appointment, and the one that goes wrong most often.

**Why matching is the wrong move even when it wins:** an owner who chose you on price leaves the moment somebody cheaper appears. And a cheaper competitor is usually cheaper because they are doing less — fewer inspections, slower maintenance, weaker screening, no protection programs — which the owner discovers at the worst possible moment.

**The reframe:**
> "I get why the difference stands out. What our owners find is that it costs less over the life of the lease. The costs that hurt are vacancy, damage, evictions, and surprises — and if someone isn't charging for something, there's a decent chance they're not doing it."

**Making the comparison concrete** — ask questions about the other quote rather than making claims about the other company:
> "The thing I'd ask them: what's their average days to lease? What happens if the tenant stops paying? What's their maintenance markup? Do they do move-in and move-out inspections?"

Then state what your fee covers — **only from `quotable_standards` and `packages`** <!-- D10, B4, B6 -->. An empty field there is not a gap to fill with the generic example; it is a claim you may not make.

**When they still push:**
> "I respect you being thorough — that's the kind of owner we want. My honest answer is that I'm not going to match, because matching would mean delivering at their level, and that isn't what we do. What I can do is make sure you're confident about what you're getting. What part are you still unsure about?"

**The four hard rules:**
1. Never match. A match is a fee deviation → `fee-and-contract-gates`.
2. Never name a competitor disparagingly. Never say another company is bad, dishonest, or terrible — even when the owner says it first, even when you believe it.
3. Only ask what their fee *may not include*. Never assert what it does not.
4. Never let their price become the anchor. The conversation is about total cost, not about the gap between two percentages.

---

## When An Objection Is Actually A Signal To Stop

Some pushback is not an objection to handle. If the owner has now negotiated the fee, the terms, *and* the maintenance threshold and is still pushing, that is a pattern, not a question. → `property-and-owner-gates`, walk-away section.

---

## After Every Objection

Log it in G10 in the owner's own words, and log what actually resolved it. Objection data is the input to the lost-reason analysis, and it is how the company finds out that the pricing presentation needs work rather than that the market got harder. See `pipeline-metrics-and-review`.
