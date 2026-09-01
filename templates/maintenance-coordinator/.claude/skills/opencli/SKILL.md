---
name: opencli
effort: medium
description: "Turn any website into a CLI command by driving Chrome's live session. Use when you need structured data from a site that has no API or where the API is inadequate — reads the browser's actual session (logged-in state, cookies) to extract data. Requires Chrome + Browser Bridge extension setup (one-time)."
triggers: ["opencli", "browser automation", "website cli", "scrape", "browser adapter", "web adapter", "generate adapter", "opencli explore", "opencli generate", "property work order adapter", "browser control"]
---

# OpenCLI — Turn Websites Into CLI Commands

> Converts any website into a deterministic CLI by driving Chrome's live session. No credentials stored — reuses whatever Chrome is already logged into.

---

## Prerequisites (One-Time Setup)

OpenCLI requires a Chrome extension to bridge between the CLI and the browser.

### 1. Install the Browser Bridge extension

```bash
# Check if already set up
opencli doctor
```

If not connected:
1. Download the extension from: https://github.com/jackwener/opencli/releases (look for `browser-bridge-extension.zip`)
2. Open Chrome → `chrome://extensions` → enable **Developer Mode**
3. Click **Load unpacked** → select the extracted extension folder
4. Run `opencli doctor` — should show `[OK] Extension: connected`

### 2. Log into target sites in Chrome

OpenCLI uses Chrome's existing session. Navigate to the target site in Chrome and log in before running any command.

### 3. Verify

```bash
opencli doctor
# Expected:
# [OK] Daemon: running on port 19825
# [OK] Extension: connected
# [OK] Connectivity: ok
```

---

## Core Commands

| Command | What it does |
|---------|-------------|
| `opencli doctor` | Diagnose extension connectivity |
| `opencli explore <url>` | Discover APIs, data stores, and recommended strategies |
| `opencli generate <url>` | One-shot: explore → synthesize → verify → register adapter |
| `opencli cascade <url>` | Probe public endpoints before committing to session-based approach |
| `opencli browser` | Direct page control — navigate, click, type, extract |
| `opencli record <url>` | Capture API calls from live session → generate YAML candidates |
| `opencli list` | List all available adapters (87+ built-in) |

---

## Adapter Generation Workflow

Use this to build a new adapter for any site:

```bash
# Step 1: Explore — discover what the site exposes
opencli explore https://app.example.com \
  --goal "read maintenance work orders and their comments"

# Step 2: Generate — build and register the adapter
opencli generate https://app.example.com \
  --goal "list open work orders with latest comment"

# Step 3: Use it
opencli <adapter-name> list-orders
opencli <adapter-name> get-comments --work-order-id 12345
```

### Record-then-synthesize (alternative for complex auth flows)

```bash
# Record API calls from your live session
opencli record https://app.example.com

# Perform the actions manually in Chrome while recording
# Stop recording — synthesize converts captured calls to adapter

opencli synthesize platform-adapter
```

---

## the {{platform}} platform Adapter Blueprint

**Goal:** Read work order comments (replacing `pm-get-comments.py` Playwright script)

**Status:** Blueprint ready. Requires Chrome extension setup + the {{platform}} platform login in Chrome to complete.

### When extension is connected, run:

```bash
# Explore what the {{platform}} platform exposes
opencli explore https://app.example.com \
  --goal "read work order work orders and associated comments/notes"

# Generate the adapter
opencli generate https://app.example.com \
  --goal "list open work orders with latest comment for triage"
```

### Expected adapter commands (once generated):

```bash
# List open work orders
opencli platform-adapter list-work-orders --status open

# Get comments on a specific work order
opencli platform-adapter get-comments --work-order-id 12345

# Triage summary (all open work orders with latest comment)
opencli platform-adapter triage --format json
```

### the {{platform}} platform API endpoints to target during recording

Based on existing Playwright scripts, these endpoints carry the relevant data:

| Endpoint | Data |
|----------|------|
| `/api/v2/work-orders/` | Work order list, status, assignee, property |
| `/api/v2/work-orders/{id}/comments/` | Work order comments and notes |
| `/api/v2/work-orders/{id}/` | Single work order detail |

**Tip:** Use `opencli record` while navigating the Work orders page and opening a work order — it captures the actual API calls Chrome makes, which is more reliable than guessing endpoints.

---

## Browser Control (no adapter needed)

For one-off browser interactions without building an adapter:

```bash
# Open a session
opencli browser

# Navigate
> navigate https://app.example.com/work orders/

# Extract text from current page
> extract .work order-list-item

# Click a button
> click "View Details"

# Wait for element
> wait .comments-panel

# Get structured data
> extract table --format json
```

---

## Using Built-In Adapters

87+ adapters ship out of the box:

```bash
opencli list              # see all
opencli gh pr list        # GitHub (wraps gh CLI)
opencli obsidian list     # Obsidian vault
```

---

## Output Formats

All commands support structured output:

```bash
opencli platform-adapter list-work-orders --format json
opencli platform-adapter list-work-orders --format csv
opencli platform-adapter list-work-orders --format table   # default
```

---

## Notes

- Session-backed: if Chrome logs out, commands return empty data
- Zero LLM cost at runtime — adapters are pre-compiled YAML + JS
- Additive: does not replace existing Playwright scripts; use alongside them
- `opencli cascade` first if unsure whether the site has public API endpoints (no extension needed for public routes)

---

*OpenCLI v1.7.3. Daemon runs on port 19825. `opencli doctor` is the first debugging step for any connectivity issue.*
