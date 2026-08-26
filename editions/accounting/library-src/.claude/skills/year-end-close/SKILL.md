---
name: year-end-close
description: "Run the year-end cycle: November-December prep and W-9 chasing, January 1099-NEC filing to the federal deadline, January owner annual tax packets, and the January-February year-end close and full-year lock. The packet is a financial summary, never tax advice."
triggers: ["year end", "year-end close", "annual close", "tax packet", "owner tax packet", "annual report", "1099 filing", "year end prep", "annual P&L", "books finalized"]
---

# Year-End Close

Source: monthly workflow, Year-End Work.

---

## November to December — prep

- Pull the 1099 tracker; identify every vendor at or over `federal_constants.form_1099_nec_threshold_usd` who is not exempt.
- Confirm a current signed W-9 for each. **Chase missing W-9s now** — it is far harder after December 31.
- Confirm legal names and TINs match the W-9 exactly. IRS name-matching errors cause penalties and are entirely avoidable at this stage.
- Run a preliminary year-end income and expense report per owner. Flag anything that looks wrong before the books close.
- Confirm all December transactions will post before year-end close.

The property manager decides whether to run an internal audit before year-end and whether to engage a CPA for owner tax support.

---

## January 1 to 31 — 1099-NEC filing

- 1099-NEC for every qualifying vendor (non-employee compensation).
- 1099-MISC where applicable — confirm the case with `roles.cpa_of_record` (C6).
- Copy B to each vendor and Copy A to the IRS by `federal_constants.form_1099_nec_due`. **Penalties start immediately.**
- State filings where `state_rules.state_1099_filing_required` (A14) says so — re-confirm the state answer with the CPA every year, because it changes.
- Retain 1099s and W-9s per `retention.records_1099_years` (B11).

**Must be true before starting:** all December vendor payments posted and finalized, W-9s on file.

---

## January — owner annual tax packets

Generate, per owner and property, a full-year summary: total gross rents collected; expenses paid by category; management and leasing fees charged; owner draws disbursed; beginning and ending reserve balances; deposit activity (received, returned, applied). Package it with copies of the year's statements.

Deliver by January 31, February 15 at the outside.

**This is not tax advice and it must not read as tax advice.** The packet is a financial summary. Every one carries a note directing the owner to their own CPA or tax advisor. If an owner asks a tax question, the answer is a referral to `roles.cpa_of_record`, not an explanation.

---

## January to February — close and lock

- Post any final December adjustments, each approved.
- Complete the December three-way reconciliation.
- **Lock the full prior year.**
- Run and archive: annual P&L by property, annual trust account summary, full-year delinquency history, 1099 filing confirmation.
- Deliver the year-end close package for final sign-off.

**Target: books fully closed and locked by February 15.**

---

## Hard gates

- This agent does not file a 1099, send a tax packet, post an adjustment, or lock a year.
- Exemption decisions belong to the CPA. Flag, do not rule.
- No tax or legal advice, in the packet or in any message about it.
