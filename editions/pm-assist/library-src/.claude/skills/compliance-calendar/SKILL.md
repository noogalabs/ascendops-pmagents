---
name: compliance-calendar
effort: low
description: "Every government deadline, notice clock, retention action, and template review date, with its lead time and its named owner. Use on the alert pass, at month-end, and whenever a filing or a legal clock comes up."
triggers: ["compliance", "compliance calendar", "filing", "registration", "inspection deadline", "retention", "notice period", "entry notice", "template review", "state requirement", "deadline"]
---

# Compliance Calendar

Anything with a government deadline lives here, plus the clocks the state sets and the templates the company relies on.

## What is on it

**Filings and registrations (A10)** — every state-required landlord filing, registration, or inspection deadline. Each row: what, to whom, due date, lead time, named owner, evidence of filing.

**State-set clocks (A5, A6, A7, A8)** — late notice and cure period, non-renewal notice, entry notice, deposit disposition deadline, habitability response timeframes. These are read by the other skills; this is where they live.

**Inspections and retention (A9)** — routine and mid-lease inspection cadence from state law and the management agreement; tenant-file retention period with the actions it triggers.

**Template review (D8)** — the attorney-reviewed notice library at `seat-config.platform.notice_template_location`, its owner, and the review dates. You may track review dates once both a home and an owner are named (D8); you never author a notice outside the library.

## The unconfirmed rule

A state-law answer that is blank or reads "confirm with counsel" makes that lane **not live**. On every surface it reads:

> `NOT LIVE — <which answer> unconfirmed. Clocks derived from it are not running.`

Never `compliant`. Never a hint default in its place. Never a clock quietly computed from an assumption. The questionnaire's own hints say to confirm with counsel and broker of record, and this seat holds that line even when the default looks obviously right.

## The pass

Every heartbeat alert pass and every month-end:

1. Anything inside its lead time → Escalation Triage with the named owner
2. Anything past due → red, top of the Daily Pulse
3. Anything with no named owner → `UNRESOLVED`
4. Template review dates coming due → to the D8 owner
5. Retention actions due → to whoever owns the file system
6. Everything unconfirmed → listed as not live, every time, so nobody reads silence as compliance

## Evidence closes a row

A filing is done when there is proof of filing — a receipt, a confirmation number, a stamped copy — recorded in `seat-config.platform.durable_record_locations`. **Never close a compliance row on inference**, on "it was submitted", or on someone's recollection.

## Never

- Never decide whether a deadline applies. That is a legal judgment
- Never serve, or decide to serve, anything
- Never mark a row compliant that you did not see evidence for
- Never let an unconfirmed answer age into an assumed one
