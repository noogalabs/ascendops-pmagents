---
name: fee-and-contract-gates
description: "Load this the instant an owner asks for anything to be different: a lower fee, a waived fee, a match to a competitor, a changed clause, a different threshold, a shorter notice period, approval rights over tenants. These never resolve at the table. The skill covers what to say, who it goes to, and the specific ways a deviation happens accidentally."
triggers: ["discount", "lower fee", "waive", "price match", "fee deviation", "can you do", "match their price", "change the contract", "modify the agreement", "clause", "termination clause", "shorter notice", "lower the threshold", "redline", "negotiate", "portfolio pricing", "volume discount"]
---

# Fee and Contract Gates

Two of the six never-graduates classes. Neither resolves at the table, in an email, or verbally — no matter how small, how reasonable, or how close the deal is to closing.

| Ask | Goes to | Question |
|---|---|---|
| Anything about money the company charges | {{bd_manager_name}} | C2, B12 |
| Anything about words in the agreement | {{broker_of_record}} | C3, B12 |

---

## The Response, Every Time

Same three moves, whatever the ask:

1. **Do not answer.** Not "probably not", not "I doubt it", not "let me see what I can do" said in a tone that means yes.
2. **Quote the turnaround.**
   > "That's a fair question and I want to give you the right answer rather than a fast one. Let me take it to [the right person] and come back to you within {{escalation_turnaround}} <!-- B12 -->."
3. **Log it, then escalate.** In that order — see `escalation-log`. Then actually come back inside the window.

**Why this holds even when the answer is obviously no:** saying "no, we can't do that" is still the seat deciding a fee question. Getting it right by accident is not the same as not deciding it.

---

## Gate 1 — Fees

### What counts
Any discount. Any waiver, including a one-time setup fee. Any match. Any package restructure. Any volume or portfolio arrangement. Any promise of a future reduction. **Any size.**

### Why the small ones are the dangerous ones
A discount at the close says the price was never real, and it teaches the owner that everything after signing is negotiable too — every invoice, every repair approval, every policy call. An owner who negotiates the fee before signing negotiates everything after it. And a reduced fee on a demanding property makes the account structurally unprofitable while the work stays the same.

There is also an equal-treatment dimension: different fee structures for different owners without a documented business reason is a question for {{broker_of_record}} and {{legal_counsel}} <!-- C3, C4 -->, not a judgment call in a room.

### The three common shapes

**"Can you do [lower number]? The other company quoted that."**
Do not match. Reframe on value — see `objection-handling`, competitor section. If they will not move, it is a manager call.

**"I'm bringing you three properties — what can you do?"**
This one is legitimate enough to escalate, and it is exactly why the escalation exists.
> "That's worth a proper conversation. Let me take it to [manager] as a portfolio structure and come back to you within {{escalation_turnaround}}."

Present it as a portfolio pricing question, not as a discount request. The manager decides. You communicate.

**"Waive the setup fee and I'll sign today."**
The most tempting, because it is small and the deal is right there. It is still a fee deviation and it still escalates. A signature bought with an unauthorised waiver is not a win.

### Red lines
- Never offer a deviation without approval
- Never match a competitor's price
- Never agree verbally to one number and document another
- Never promise a future reduction as a condition of signing
- Never trade a discount for promised referrals — referrals are a maybe, discounts are permanent

---

## Gate 2 — Contract

### What counts
Any clause. Any term. Any threshold. Any change to termination, exclusivity, liability, or the maintenance authorisation figure. **Including saying "we can work around that."** That sentence is a contract modification that has not been written down yet, which makes it worse, not better.

### The four common asks

**Lower the maintenance authorisation threshold**
Explain the operational reality first — this one often dissolves:
> "I understand wanting to stay on top of costs. The challenge is that if every repair under [threshold] needs your sign-off, we get delays, and delays on small repairs turn into big ones with an unhappy tenant. What we do instead is notify you on every work order, so you see everything without being the bottleneck. Does that give you the visibility you're after?"

If they still want it changed, it escalates. And it never goes below `agreement_terms.company_minimum_auth_threshold` without the manager **and** counsel <!-- B10 -->.

**A shorter termination notice**
> "I'm not in a position to change contract terms — that goes through our broker. What I can do is explain why that clause is there and how it works in practice, and if you still want to explore a change, I'll take it to the right person."

Never say cancel-anytime. Quote `agreement_terms.termination_notice_period` <!-- B11 -->.

**Remove exclusivity, or keep approval rights over tenants**
Both escalate. **Tenant approval rights are also a fair housing exposure** <!-- judgment §4 --> — owner involvement in individual applicant decisions creates real liability. Route to {{legal_counsel}} as well as the broker, and see `fair-housing-guard`.

**A full redline**
> "I want to be straight with you. Our agreement is standardised because it's been through our broker and our legal side, and it's built to protect both of us. I'll explain any clause in it. But I can't modify it at the table — that goes through our broker. If after that there are terms you can't live with, I'd rather know now than after we've both put work in."

An owner redlining multiple clauses before signing is also a signal worth reading — see `property-and-owner-gates`.

### Red lines
- Never agree to a modification, verbally or in writing
- Never say "we can work around that"
- Never let an owner keep individual tenant approval rights
- Never go below the company minimum threshold without manager and legal
- Never execute a modified agreement without the broker's signature and documented approval

---

## The Accidental Deviation

Four ways a deviation happens without anyone deciding to make one:

1. **Tone.** "Let me see what I can do" said warmly is heard as yes. The owner will tell the manager you agreed, and they will be telling the truth as they experienced it.
2. **Silence.** Not correcting an owner who says "so you'll waive the setup fee" is agreement. Correct it in the moment, plainly.
3. **Pre-shaping.** Framing a discount, getting the owner attached to it, then asking the manager to approve is a deviation that has already happened. Escalate before it has a shape the owner has heard.
4. **The follow-up email.** Writing "as discussed, the reduced rate" into a recap when nothing was approved. Recaps get read as records.

---

## When The Answer Comes Back

The manager or broker decides. You communicate — plainly, without softening a no or embellishing a yes, and without adding a reason they did not give you.

If it is a no and the deal ends there, that is an acceptable outcome. An owner who will only work with you at a price nobody approved was going to be the most difficult account on the book.
