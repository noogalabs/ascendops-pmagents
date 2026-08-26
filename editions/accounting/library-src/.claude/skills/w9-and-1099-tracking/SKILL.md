---
name: w9-and-1099-tracking
description: "Keep the W-9 file and the 1099 tracker current all year so January is filing, not archaeology. W-9 before first payment, cumulative payments tracked per vendor per calendar year, name and TIN matched to the W-9 exactly, and every vendor at or over the federal threshold identified in November rather than January."
triggers: ["1099", "W-9", "W9", "1099-NEC", "1099 tracker", "TIN", "vendor tax", "year end tax", "IRS filing", "contractor tax form", "vendor W-9 missing"]
---

# W-9 and 1099 Tracking

Source: monthly workflow Step 5 (1099 tracking) and the year-end section.

Federal constants live in `accounting-config.json` → `federal_constants`. The state answer lives in `state_rules.state_1099_filing_required` (A14) and gets re-confirmed with `roles.cpa_of_record` (C6) every year, because state rules change.

---

## The one rule that prevents everything else

**No W-9 on file, no first payment.** Not "we'll get it before year-end." The moment a vendor is paid without one, the company has taken on a filing obligation it may not be able to satisfy, and chasing a W-9 from a vendor who has already been paid is materially harder than chasing one from a vendor who wants to be.

---

## Per-payment discipline

Every vendor payment updates the tracker. The tracker carries, per vendor per calendar year:

- legal name exactly as it appears on the W-9
- TIN
- entity type, and whether it is 1099-exempt
- W-9 on file: yes / no / requested / exempt
- cumulative paid year to date
- flag once cumulative paid reaches the federal threshold in `federal_constants.form_1099_nec_threshold_usd`

Any unincorporated vendor — sole proprietor, LLC taxed as a sole proprietorship or partnership — paid at or above that threshold in a calendar year needs a 1099-NEC. Corporations are generally exempt, but "generally" is doing work in that sentence: flag them for the CPA rather than deciding exemption on your own.

---

## November to December — prep

- Pull the tracker and identify every vendor at or over the threshold who is not exempt.
- Confirm a current signed W-9 is on file for every one of them.
- Chase missing W-9s **now**. After December 31 it gets much harder.
- Confirm legal names and TINs match the W-9 exactly. IRS name-matching mismatches cause penalties, and they are entirely avoidable in November.
- Run a preliminary year-end income and expense report per owner and flag anything that looks wrong before the books close.

---

## January — filing

- 1099-NEC for every qualifying vendor.
- 1099-MISC where applicable — confirm with the CPA.
- Copy B to each vendor and Copy A to the IRS by `federal_constants.form_1099_nec_due`. Penalties start immediately; there is no grace here.
- State copies where `state_rules.state_1099_filing_required` (A14) says so.
- Retain copies of all 1099s and W-9s per `retention.records_1099_years` (B11).

---

## The weekly check

On the weekly sweep, one question: has any vendor been paid this week without a W-9 on file? If yes, that payment should not have gone out, and the next one is held until the W-9 lands.

---

## Hard gates

- This agent does not file. It prepares the list, the amounts, and the exceptions, and routes them to the CPA and the property manager.
- Exemption is never decided here. Flag it, let the CPA rule.
- A vendor's legal name on the tracker is what the W-9 says, not what the invoice letterhead says.
