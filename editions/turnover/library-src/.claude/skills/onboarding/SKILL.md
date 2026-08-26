---
name: onboarding
description: "Verify a Turnover Coordinator configured by repository setup.py, connect its private Telegram deployment wiring, and complete the approval-gated first boot. Never run a second turnover configuration interview."
triggers: ["onboarding", "/onboarding", "first boot", "run onboarding", "not onboarded", "onboarding interrupted"]
---

# Turnover Coordinator Onboarding

Repository `setup.py` is the single configuration interview. This skill verifies
the configured result and completes deployment wiring. It never asks the
operator to re-enter identity, company, turnover policy, targets, goals, or
software answers and never rewrites those values from conversation.

## 1. Check completion state

```bash
[[ -f "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.onboarded" ]] && echo "ONBOARDED" || echo "NEEDS_ONBOARDING"
```

If already onboarded, return to normal startup unless the operator explicitly
asked to repair onboarding.

## 2. Verify configured custody

Read `ONBOARDING.md`, then read `turnover-config.json` in full. Verify:

- the structured artifact says `seat: turnover-coordinator`;
- `IDENTITY.md`, `SOUL.md`, `GUARDRAILS.md`, and `config.json` agree with the
  configured answers;
- the `## Name` marker in `IDENTITY.md` is replaced unconditionally, using
  `$CTX_AGENT_NAME` as the default display value;
- no rendered `{{...}}` placeholder remains outside documentation examples.

If any configured value is wrong or incomplete, stop and rerun
`python3 setup.py` from the repository root. Do not correct, recollect, or silently substitute turnover answers during first boot.

## 3. Add deployment-only wiring

The only values first boot may collect are the Telegram bot token, chat id, and
allowed sender id. Store all three as `BOT_TOKEN`, `CHAT_ID`, and
`ALLOWED_USER` in the agent's private environment file, never a tracked file.
If new credentials were loaded in the current process, restart so the daemon
reads them before continuing.

Do not ask for property-management platform credentials or API keys. Live
platform connections are separate, approval-gated work.

## 4. Complete through the single authority

Run the final completion Bash block in `ONBOARDING.md`. That block is the only
completion authority. It performs the final placeholder-and-marker gate,
registers the turnover role crons, writes the durable `.onboarded` marker, and
registers heartbeat only after the marker.

Never write `.onboarded` directly. Never add role crons before the final gate.
If the block stops, fix the named condition and rerun the same idempotent block.

Only after the block succeeds may the agent report that it is online and begin
normal turnover work. The permanent posture remains copilot-first: draft,
verify, and flag; all external messages, scope changes, vendor pricing, deposit
deductions, and damage-charge notices require human approval.
