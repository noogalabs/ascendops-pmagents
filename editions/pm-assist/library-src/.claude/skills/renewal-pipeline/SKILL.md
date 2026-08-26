---
name: renewal-pipeline
effort: medium
description: "Track leases into the renewal window, request the CMA, draft the recommendation memo with the rate line blank, run the owner decision clock, and schedule tenant follow-ups. Use on the weekly sweep and whenever a lease crosses the look-ahead window."
triggers: ["renewal", "renewal pipeline", "lease expiring", "renewal memo", "cma", "renewal rate", "non-renewal", "renewal offer", "lease expiration", "renewal window"]
---

# Renewal Pipeline

Leases move through this pipeline on a clock. **The rate is never yours.**

## The clocks (B9)

| Stage | Clock |
|---|---|
| Pipeline pull | Leases inside {{renewal_lookahead_days}} <!-- B9: renewal pipeline look-ahead window --> days of expiration |
| Owner decision | Within {{owner_decision_days}} <!-- B9: owner decision window on a renewal recommendation --> days of the recommendation |
| Tenant follow-ups | `seat-config.clocks.renewal_tenant_followup_days`, default 30 and 60 |
| Red flag | Any lease inside the window with **no action started** |

## The pass

1. **Pull the pipeline** from the lease board. Every lease crossing into the window this week onto the Monday Board.
2. **Request the CMA** from `seat-config.platform.cma_source`. Whether {{property_manager_name}} <!-- A2: who holds the Property Manager seat --> runs it or reviews one you pulled is `cma_run_by` (D9) — follow it, do not assume.
3. **Draft the recommendation memo** with the rate line **blank**. Include: current rent, CMA range with its source and date, tenancy length, payment history, work-order history, market context from the CMA data only.
4. **Route to the PM.** The rate, the terms, and the renew/non-renew call are all housing decisions — they never come to you at any setting.
5. **On terms set**, prepare the offer. Sending it is `renewal_offer_send_after_terms_set` in `copilot-thresholds.json` and starts locked.
6. **Run the owner decision clock** at {{owner_decision_days}} days. A silent owner runs the B4 ladder — see `approval-queue`.
7. **Run tenant follow-ups** on schedule after the offer goes out.
8. **File the outcome** in {{decision_log_location}} <!-- D7: where the decision log lives -->, with the decider named.

## The non-renewal constraint

If the company decides not to renew, the state's non-renewal notice period (A6) has to be servable from the date of the decision. **A decision made too late to serve legal notice is a problem you surface, not one you solve.**

Every week, check: for each lease in the window, does `days_to_expiration − owner_decision_days` still leave the notice period? When it does not, that lease goes red on the Daily Pulse with the arithmetic shown. When the A6 answer is unconfirmed, say the check cannot run rather than using a hint default.

## Never

- Never suggest a rate, a range, or "in line with the CMA." Present the CMA and stop
- Never characterize a tenant as one you would or would not renew
- Never send an offer before the terms are set by a human, and never adjust terms after
- Never let a lease sit inside the window with no action started — that is a red flag, every day, until it moves
- Never derive a renewal rate from last year's plus a percentage
