---
name: pipeline-metrics-and-review
description: "Load this for the weekly pipeline review, for the monthly leadership report, and any time a number about the pipeline is going to be reported to anyone. Carries the funnel conversion table, lead-source performance, lost-reason analysis, the healthy-pipeline benchmarks by portfolio size, the weekly review agenda, and the rules that keep reported numbers honest."
triggers: ["metrics", "conversion", "weekly review", "pipeline review", "monthly report", "leadership report", "close rate", "how are we doing", "pipeline health", "lost reasons", "lead source", "benchmarks", "scorecard", "doors added"]
---

# Metrics and Review

## The Rule That Comes Before Any Number

**Every reported number carries its source, its date range, and when it was pulled.** A conversion rate with no window behind it is not a measurement — it is an impression with a decimal point.

And when a computed column has stopped computing, say so. A stale formula reports a healthy zero, and a healthy zero on a stale-deal count is the most expensive number this seat produces.

---

## Funnel Conversion

| Metric | Computed from | Benchmark |
|---|---|---|
| Total leads created | Count of deal IDs in the window | — |
| Discovery calls completed | F2 = Yes | 50–60% of leads |
| Lead → discovery | calls ÷ leads | 50–60% |
| Appointments held | F4 = Held | 60–70% of discovery calls |
| Discovery → appointment | held ÷ calls | 60–70% |
| Agreements signed | F10 = Yes | 40–60% of appointments held |
| Appointment → close | signed ÷ held | 40–60% |
| Overall lead → close | signed ÷ leads | 20–30% |
| Doors added | Sum of C16 where won | — |
| Average doors per win | doors ÷ signed | 1.3–1.8 |
| Average days lead to close | Mean of (F11 − A2) | `activity_targets.target_days_lead_to_close` <!-- D8 --> |
| Average days unsigned (S5) | Mean days in S5 on won deals | Under 3 |
| Lost rate | lost ÷ (won + lost) | — |

**Reading the funnel:** roughly two to three signed agreements per ten qualified leads. Below that, the break is usually at the appointment — which points at the pricing presentation or the objection handling, not at lead volume. Adding leads to fix a close-rate problem is the most common wrong move available.

---

## Lead Source Performance

One row per source from `platform.active_lead_sources` <!-- D2 -->: leads, discovery calls, appointments held, signed, doors added, close rate, average days to close.

This table only works if D1 is picked from the list every time. A row tagged "other" argues silently against the channel that actually produced it. See `pipeline-board`.

**What healthy looks like:** three to five sources running simultaneously, with referrals at twenty to thirty percent. Single-source dependency is the risk nobody feels until the source dries up.

---

## Lost-Reason Analysis

From G4, one row per reason, with the trend against the previous month.

The diagnostic is direct:

| Top lost reason | What it actually says |
|---|---|
| Fees too high | The pricing presentation is not landing. → `pricing-presentation` |
| No response | Speed-to-lead or follow-up cadence is broken. → `daily-pipeline-run`, `followup-and-nurture` |
| Chose competitor | Differentiation is weak. → `objection-handling`, competitor section |
| Chose self-manage | The gap is not being surfaced in discovery. → `question-led-selling` |
| Property disqualified | Qualification is happening too late in the funnel. → `lead-intake` |

Every one of these points at a fixable thing. That is the whole value of the field being a dropdown rather than free text.

**G4 never carries a protected-class matter.** Those route by escalation id — see `fair-housing-guard`.

---

## Healthy Pipeline By Size

Selected by `_descriptive.benchmark_tier` <!-- A1 -->.

**Under 150 doors** — target 5–10 new doors/month. Active leads 20–35. Discovery calls 3–5/week. Appointments 2–3/week. Signed 3–6/month. Warning signs: fewer than 10 active leads at any time; a week with no appointments; a single lead source.

**150–400 doors** — target 10–20/month. Active leads 50–80. Discovery calls 6–10/week. Appointments 4–6/week. Signed 6–12/month. Sources 3–5. Warning signs: more than a fifth of time on non-sales work; one source dominating; appointment-to-close under 35%.

**400+ doors** — target 20–40+/month. Active leads 100–150+. Discovery calls 12–18/week. Appointments 8–12/week. Signed 12–20+/month. Sources 5–7+. Warning signs: close rate falling; onboarding overwhelmed; no nurture sequence for the 30–60 day cohort; a board that is not being updated.

**Universal:** a healthy pipeline holds `activity_targets.pipeline_minimum_multiple` × the monthly door goal in active opportunities <!-- D8 -->. Below it, the alert fires to the manager the same day — that one does not wait for the review.

---

## Weekly Review

When: `cadence.weekly_review_when` <!-- D9 -->. Who: `cadence.weekly_review_attendees`.

| # | Item | Time |
|---|---|---|
| 1 | Wins: signed, doors added | 3 min |
| 2 | New leads: source, quality | 5 min |
| 3 | **Stage-by-stage walk — every active deal, one sentence each** | 15 min |
| 4 | Alerts still open, and why | 5 min |
| 5 | Lost this week: reason, what would have changed it | 3 min |
| 6 | Redirects handed off | 2 min |
| 7 | Next week: top three to close, top three to pursue | 5 min |

Questions worth asking every time:
- What is the next action on every S4 and S5 deal, and exactly when?
- Are all decision-makers engaged on every booked appointment?
- Which deals have sat past `clocks.days_in_stage_review_flag` <!-- D6 -->, and what is the plan?
- Which source produced the wins this month — are we investing more there?
- Which objection killed the most deals — does a script need work?
- Is the pipeline at the minimum multiple? If not, what is the prospecting plan?

**Prepare the pack before the meeting, not in it.** The review is for decisions; assembling numbers live burns the fifteen minutes that matter.

---

## Monthly Leadership Report

To `cadence.monthly_report_recipients` <!-- D9 -->.

Leads by source · discovery calls, count and percentage · appointments held, count and percentage · agreements signed, count and percentage · doors added · average doors per owner · pipeline value in doors · lost deals with reasons · top source by return · new recurring revenue added.

**Three honesty rules:**
1. Report the number the board produces. Not the number with the awkward deal explained away.
2. Where a figure could not be computed, say so and say why. An asterisk beats a plausible estimate.
3. Pipeline value is doors in active opportunities, not doors you expect to win. The second number is a forecast and gets labelled as one.

A pipeline that reads healthy and is not is worse than a thin pipeline honestly reported, because somebody staffs against it.

---

## Quarterly

Alongside the archive audit in `stage-gates`: which sources produced over the quarter, whether close rate is trending, whether the lost-reason mix has shifted, and whether the benchmark tier still matches the portfolio.
