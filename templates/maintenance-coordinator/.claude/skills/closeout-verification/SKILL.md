---
name: closeout-verification
description: "Run this whenever a tech or vendor marks a work order complete, whenever a meld reaches PENDING_COMPLETION, and ALWAYS before you run `pm work-orders complete` yourself. Verifies the three documentation requirements (notes, photos, hours) against the real API fields — never the notification email snippet — sends the tech back for anything missing, and executes the 4-step partial-completion SOP (complete + clone + assign + merge) when the work was only partly done."
triggers: ["completion", "tech completed", "vendor completed", "marked complete", "pending completion", "verify completion", "closeout", "close out", "partial completion", "still need", "couldn't finish", "could not complete"]
---

# Closeout Verification

## When this fires

1. A completion notification arrives (tech or vendor says the job is done).
2. A meld transitions to `PENDING_COMPLETION` (seen in a sweep or a list).
3. ALWAYS before you run `pm work-orders complete` yourself.

## The three checks

Fetch the real state — never trust the email snippet:

```bash
pm work-orders inspect <meld_id> --json   # one call: detail + photos + notes + work_entries (the hours field lives here, `get` does not return it)
```

| Check | Pass condition |
|---|---|
| Notes | `maintenance_notes` non-empty AND not "(none)" / "n/a" (case-insensitive). `completion_notes` is a bonus, not required. |
| Photos | At least 1 attached file with a photo extension (`.jpeg` `.jpg` `.png` `.heic` `.gif` `.webp`) — the files endpoint has no content-type field, go by filename. |
| Hours (in-house techs only) | `sum(work_entries[].hours) > 0`. Vendors close without hours; their invoice may follow later. |

**The snippet trap (real, recurring):** the PM completion email shows "(None)" for `completion_notes` even when the tech filled `maintenance_notes` correctly — the email refers ONLY to `completion_notes`, which is almost always empty regardless of how much documentation exists. Judging from the email alone produces false "no docs" pings. Check both fields via the API, every time.

## Outcomes

- **All checks pass** → proceed (or stay silent if the tech closed it). Log: `cortextos bus log-event action completion_checklist_pass info --meta '{"work_order_id":"<id>"}'`
- **Any check fails** → message the tech via an internal note (hidden from tenant AND vendor — this is a documentation request, not a customer comm):
  ```bash
  pm work-orders send-message --meld-id <id> \
    --text "Hi <tech>, this one is marked done but I'm missing <notes / photos / hours>. Could you add them when you get a chance? Need them for billing + documentation. Thanks!" \
    --hide-tenant --hide-vendor --json
  ```
  Log: `cortextos bus log-event action completion_checklist_gap info --meta '{"work_order_id":"<id>","missing":["<fields>"]}'`
  If the tech is unresponsive after 24h, escalate to the property manager. If the same tech gaps 3+ times in 7 days, surface the pattern.
- **The notes say the work was only PARTLY done** ("still need", "couldn't finish", "needs a vendor for", "second visit") → do NOT chase photos/hours as if it were a docs gap. Run the partial-completion SOP below.

## Partial-Completion SOP (4 steps)

Prevents half-done work orders from lingering in a dead status forever. If the remaining scope is ambiguous ("still need to check something"), STOP and ask the tech via internal note before proceeding.

1. **Complete the original with both scopes in the notes:**
   ```bash
   pm work-orders complete --meld-id <id> \
     --notes "Completed: <what was done>. Remaining: <what is still pending>. New work order created for the remaining scope." --json
   ```
   (`complete` requires `PENDING_COMPLETION` status. If the tech already closed it into a terminal could-not-complete status, check whether `pm work-orders force-pending-completion` is available on your CLI version to recover it; otherwise recover via the PM UI, then continue.)
2. **Clone for the remaining scope** and capture the new ID:
   ```bash
   pm work-orders clone --meld-id <id> --json
   ```
3. **Assign the next-stage owner** — in-house first by trade; vendor only if no in-house tech can take it within a 48h SLA or the trade demands an outside specialist:
   ```bash
   pm work-orders assign-tech --work-order-id <new_id> --tech "<tech name>" --json
   # or, via the vendor-coordination skill's gates:
   pm work-orders assign-vendor --work-order-id <new_id> --vendor "<vendor name>" --json
   ```
   If the vendor path fires, the `vendor-coordination` skill's vendor-first confirmation sequence applies before any resident is told anything.
4. **Cross-reference the two melds — do NOT merge them:**
   ```bash
   pm work-orders update-notes <original_id> --maintenance "Completed scope closed here. Remaining scope tracked on <new_id>." --json
   pm work-orders update-notes <new_id> --maintenance "Remaining scope split from <original_id> (completed scope closed there)." --json
   ```
   A `pm work-orders merge` would end one of the two melds as `MANAGER_CANCELED (Merged)` — destroying either the completed record or the newly-assigned remaining work. Never merge a partial-completion split; cross-referencing keeps both the completed record and the assigned remainder live and linked.

Then brief the property manager in one message: original closed (completed scope), new work order + ID (remaining scope), who it's assigned to, cross-referenced on both threads. If they countermand ("just close it, the remainder isn't worth a new one"), cancel the clone with a reason and stop.

## Never

- Never close a work order on "looks done" or "the vendor said so" — evidence or it stays open.
- Never message the tenant about documentation gaps — those notes are internal.
- Never chase docs on a genuinely partial job — that's the SOP, not a nag.
- Never mark complete yourself without running the three checks first.
