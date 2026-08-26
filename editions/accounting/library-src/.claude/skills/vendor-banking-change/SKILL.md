---
name: vendor-banking-change
description: "Run the vendor banking change verification protocol end to end: receive and freeze, independent verbal verification at the number already on file, written property-manager authorization, update, second-person spot-check, and release. Business email compromise is the number-one fraud vector in property management payments and the callback is the only control that stops it. An email is never verification."
triggers: ["vendor banking change", "change bank details", "update ACH", "new account number", "direct deposit change", "banking update", "BEC", "business email compromise", "vendor payment info", "routing number change", "vendor bank request"]
---

# Vendor Banking Change Verification

Source: the Vendor Banking Change Verification Protocol, which is judgment scenario 5 in expanded form.

> A vendor's banking details change exactly once: after independent verbal verification with a known contact, followed by written property-manager authorization. Every other step exists to protect that moment.

This is a **never-graduates** gate. No accuracy record shortens it. No vendor relationship exempts a vendor from it.

---

## What counts as independent verification

Confirmation with a real, known human at the vendor, using contact information that **existed in your records before the change request arrived**.

| Method | Counts | Condition |
|---|---|---|
| Phone call to the number already in the vendor master | Yes | Must reach a live person. Voicemail does not count. |
| Video call with a known contact whose face you recognize | Yes | You initiate, not the vendor |
| In-person at the vendor's known business address | Yes | Rare, valid for high-value vendors |
| Callback to a number on the vendor's official website, navigated to independently | Yes, with PM approval | You navigate there yourself. Never click a link in the request. |

## What never counts

- Replying to the email that carried the request — the fraudster controls that inbox
- Calling a number provided in the request, or in any follow-up on the same thread
- A text from an unknown or new number claiming to be the vendor
- A second email from a different address "confirming" the first
- A signed PDF or form attached to the request
- A portal message where the account was just created or accessed from a new device
- "I've worked with them for years, I know it's them" — familiarity is not verification, and fraud works precisely because it exploits it

---

## Phase 1 — Receive and freeze (immediate)

1. **Do not act on the request.** Do not update anything. Do not reply confirming. Do not forward it to anyone who might act on it. Note the exact time and method of receipt and capture the request exactly as received, unaltered.
2. **Pull the vendor master record.** Legal name, primary contact, **the phone number on file — the only number you will call**, email on file, current banking details by last four only, date last verified. Use nothing from the request itself. No phone number on file means escalate before any callback attempt.
3. **Freeze every pending and scheduled payment** to this vendor: `HOLD — BANKING CHANGE PENDING VERIFICATION`. If a payment is due within 24 hours, escalate immediately; the property manager decides whether to delay or expedite. Never pay to old or new details without that direction.
4. **Log the escalation** in the PM decision log as scenario S5, with the total held, a plain description, and the action taken. Notify the property manager in writing **within 15 minutes**, with the log ID in the subject line.

---

## Phase 2 — Independent verification

5. **Tell the property manager the call is happening** before making it. Do not wait for a reply — time matters — but they must know.
6. **Call the number on file.** Ask to speak to the contact on file. Confirm verbally: did you or someone authorized submit this request; what is the name on the new account; what is the name of the new bank; what are the last four of the new account number. **Let them supply the details — do not read the request's details to them first.** Document date, time, duration, who you spoke to, their role, and every answer. Never leave banking details in a voicemail.
7. **Evaluate the outcome.**

| Outcome | Meaning | Next |
|---|---|---|
| Confirmed, details match | Live person confirmed and the details match exactly | Phase 3 |
| Confirmed, details do not match | A request was made but the details differ | Escalate immediately — possible fraud or an error at the vendor. Change nothing. |
| Denied | The vendor made no such request | Escalate immediately — active fraud attempt. Change nothing. |
| No answer | Could not reach a live person | Step 7A |

**7A — no answer.** Retry after 30 minutes. Retry once more at a different time of day. After three failed attempts across one business day, escalate; the property manager decides whether to delay payment or attempt a secondary route (the vendor's official website contact form, never a link from the request). The hold stays in force.

---

## Phase 3 — Property manager authorization

8. Report the verification result in writing: log ID, what was received and when, who was called at what number, who answered, what they confirmed, and whether the details match.
9. The property manager reviews and decides. **No record changes before this decision.**
10. The property manager signs the written authorization. A verbal is not authorization here.

---

## Phase 4 — Update and confirm

11. Update the vendor master record, noting the authorization reference and the verification date.
12. **Second-person spot-check** by `roles.second_person_verifier` (C7) — someone other than whoever processed the change — before the next payment releases.
13. Notify the vendor, at the contact on file, that the change is complete.
14. Release the payment hold and process the first payment under the new details.
15. Close the decision-log entry.

---

## The holding state

Between step 1 and step 14: banking details unchanged, payments held, **operations continue** — new work orders may still be assigned, the hold is financial only. Communication with the vendor goes only to contact information already on file. Never reply to the request itself.

**Maximum hold: three business days without an active property-manager decision.** Holding indefinitely is not a strategy. If the hold makes a payment late, the property manager tells the vendor payment is held pending a routine verification. Do not describe the steps or the timing of the protocol to the vendor, and do not apologize in a way that implies the vendor did something wrong. The hold is a standard control, not an accusation.

---

## Pushback

Vendors push back. Stay calm, stay firm, and use one line: *"This applies to every vendor, every time. It protects you too. Can I call you right now?"*

The one thing you never say: anything that suggests the protocol is negotiable, or that this particular vendor might be exempt from it.

---

## Hard gates

- The agent does not change a vendor record. It runs the protocol, produces the evidence, and routes the authorization.
- No email, no attachment, no second email, and no familiarity substitutes for the callback.
- The freeze goes on at minute zero, before anyone has decided anything.
