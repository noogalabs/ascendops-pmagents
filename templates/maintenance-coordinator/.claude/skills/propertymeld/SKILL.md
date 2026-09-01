---
name: propertymeld
description: "CLI for Property Meld work order management. The `pm` CLI (package: cli-anything-pm) is the primary tool for ALL Property Meld operations, reads AND writes — plain HTTP with a captured session cookie, no browser automation. The Nexus API (client-credential) path is secondary for bulk reads. Manual UI is last resort only."
triggers: ["property meld", "work order", "meld", "pm work-orders", "pm assign-tech", "meld triage", "assign vendor", "schedule meld", "complete meld"]
---

# Property Meld CLI

## Tool Hierarchy — Follow This Order

1. **`pm` CLI (plain HTTP)** — primary for ALL operations: reads, assignment, scheduling, messaging, completion. Authenticates with a captured session cookie. No Playwright, no browser, no MFA login for day-to-day operations.
2. **Nexus API** (client credentials) — secondary. Good for bulk reads (`properties list`, `vendors list`) and `maintenance_notes` updates. It cannot do assignment, merge, or chat writes.
3. **Manual PM UI** — last resort, only if the `pm` CLI itself is broken (expired cookies AND recapture failing, or a site layout change). Do NOT fall back here just because one API call returned 404.

> **History lesson — do not re-learn this the hard way.** An earlier version of this skill taught tech assignment and comment reads as browser/Playwright automation. That stale claim caused a phantom "login blocker" in a live deployment: the agent believed it was blocked on an MFA login it never needed. Assignment is and always was plain HTTP via the `pm` CLI. The only place a browser appears is the optional one-time session-cookie capture helper.

## Setup

```bash
# Install via pipx from your platform operator's cli-anything-pm source (a checkout path or git URL):
pipx install <path-or-git-url-to-cli-anything-pm>
pm --version
```

Required env vars (in the agent `.env`):

```
PM_CLIENT_ID=<Nexus client id>          # Meld: Settings > Integrations > API
PM_CLIENT_SECRET=<Nexus client secret>
PM_MULTITENANT_ID=<company id>          # the number in your Meld URL after app.propertymeld.com/
# Optional — defaults to ~/.claude/credentials/property-meld.json:
# PM_CREDS_PATH=<path to captured session-cookie JSON>
```

Session cookie: the plain-HTTP backend reads a `sessionid` cookie from `PM_CREDS_PATH`. Capture or refresh it with the recapture helper bundled in the cli-anything-pm package (it reads `PM_WEB_EMAIL` / `PM_WEB_PASSWORD`; see the package README). That helper is the ONLY step that opens a browser. If a write command starts returning 401, the session expired — re-run the recapture helper, then retry once.

Health check: `pm probe --json` (verifies credentials and connectivity).

## Commands

### Work orders — read
```bash
pm work-orders list --status open --json           # open work orders (also: pending / completed / canceled)
pm work-orders list --stuck-hours 48 --limit 500 --json   # silent >48h in current status
pm work-orders get <meld_id> --json                # single work order detail
pm work-orders comments <meld_id> --json           # message thread / notes
pm work-orders files <meld_id> --json              # attached files (manager + tenant + vendor uploads)
pm work-orders inspect <meld_id> --json            # detail + photos + thread in one call
```

### Work orders — write
```bash
pm work-orders create --brief-description "<title>" --description "<detail>" \
  --work-category "<category>" --work-type "<type>" --due-date <ISO8601> --unit-id <id> --json
pm work-orders assign-tech --work-order-id <meld_id> --tech "<tech name>" --json     # in-house; partial name match
pm work-orders assign-vendor --work-order-id <meld_id> --vendor "<vendor name>" --json  # external; partial name match -> PENDING_VENDOR
pm work-orders schedule --meld-id <meld_id> --dtstart 2026-04-27T14:00:00-04:00 --hours 2 --json          # in-house appointment window
pm work-orders schedule-vendor --meld-id <meld_id> --vendor-id <id> --dtstart <ISO8601> --hours 2 --json  # vendor appointment window
pm work-orders send-message --meld-id <meld_id> --text "<message>" --json            # post to the meld thread
pm work-orders send-message --meld-id <meld_id> --text "<internal note>" --hide-tenant --hide-vendor --json
pm work-orders complete --meld-id <meld_id> --notes "<completion notes>" --json      # meld must be PENDING_COMPLETION
pm work-orders cancel --meld-id <meld_id> --reason "<why>" --json
pm work-orders clone --meld-id <meld_id> --json                                      # new meld, same unit/tenant metadata
pm work-orders merge --destination <dst> --source <src> --json                       # dst absorbs src; src ends MANAGER_CANCELED (Merged); same unit required
pm work-orders update-notes <meld_id> --maintenance "<text>" --json                  # maintenance_notes PATCH (meld id is positional)
pm work-orders upload-file <meld_id> <file_path> --json                              # attach a photo/doc (meld id + path are positional)
```

### Tenants, properties, vendors
```bash
pm tenants list --search "<name / email / phone substring>" --json
pm tenants get <tenant_id> --json
pm properties list --json
pm vendors list --json
```

## Backend Notes

| Command | Backend | Auth |
|---------|---------|------|
| work-orders (all read + write subcommands) | pm CLI, plain HTTP | PM_CREDS_PATH session cookie |
| tenants list/get | pm CLI, plain HTTP | PM_CREDS_PATH session cookie |
| properties list / vendors list | Nexus API | PM_CLIENT_ID / PM_CLIENT_SECRET |
| maintenance_notes update | Nexus API | PM_CLIENT_ID / PM_CLIENT_SECRET |

## Behavior Notes

- `complete` requires the meld to be in `PENDING_COMPLETION` status.
- `merge` requires both melds at the same unit; the source meld ends `MANAGER_CANCELED` with a "(Merged)" prefix.
- A closed meld cannot be reopened. Clone it, assign the same vendor/tech, and note in the new thread that it replaces the closed one (see GUARDRAILS.md PropertyMeld rules).
- `assign-vendor` / `assign-tech` accept partial name matches against the roster; on no match the CLI returns the available names — surface them, do not guess.
- `tenants list --search` filters client-side; expect the full list to be fetched.
- Vendor assignment requests and appointments are different objects with different IDs — when scheduling a vendor, use the vendor id from `pm vendors list`, not the assignment-request id.
