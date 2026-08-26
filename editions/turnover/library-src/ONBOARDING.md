# Onboarding — Turnover Coordinator Agent

The guided configurator has already collected and rendered the operating answers. This first-boot procedure verifies that configured custody, connects deploy-time messaging, and activates the documented schedules. Do not re-ask questionnaire answers or edit rendered values by hand; `turnover-config.json` is the source of truth.

---

## Step 1: Verify the configured package

Read `turnover-config.json`, `config.json`, `IDENTITY.md`, `USER.md`, `GUARDRAILS.md`, and `AGENTS.md`. Confirm that the structured configuration agrees with the rendered operating surfaces, including the turn target, inspection and scope SLAs, stale-stage threshold, approval threshold, timezone, and permanent human-release gates.

If any configured value is wrong or unresolved, STOP and rerun `python3 setup.py` from the PMAgents repository root. Do not continue by patching a rendered file.

---

## Step 2: Connect Telegram

The only new values collected at first boot are deployment credentials.

1. Message @BotFather, run `/newbot`, and copy the bot token.
2. Send `/start` to the new bot.
3. Put `BOT_TOKEN` and `CHAT_ID` in the agent `.env` before starting the agent, or detect the chat ID after the token is present:

   ```bash
   cortextos detect-chat-id --agent "$CTX_AGENT_NAME" --org "$CTX_ORG"
   ```

4. Verify the configured channel:

   ```bash
   cortextos bus send-telegram "$CTX_TELEGRAM_CHAT_ID" "Bot is live — completing turnover onboarding."
   ```

---

## Step 3 (FINAL): Activate the documented schedules

Run this block only after the configured-package and Telegram checks pass. It is idempotent and keeps the durable `.onboarded` marker as the completion boundary. Heartbeat registration happens only after that marker exists, so an interrupted pre-marker run cannot create a state-writing heartbeat for an incomplete agent.

```bash
# FINAL GATE: configured output must contain no unresolved template field or
# first-boot name marker. Do not add crons or write .onboarded while either exists.
if grep -rlE '\{\{[^{}]+\}\}|<!-- Set during onboarding' . --include='*.md' --include='*.json' 2>/dev/null | grep -vE 'ONBOARDING\.md|README\.md|skills/onboarding/|node_modules'; then
  echo "STOP: configured files still contain an unresolved template field or name marker. Rerun python3 setup.py; no crons were added and .onboarded was not written."
else
  # Idempotent restart: clear the documented turnover cron set from a prior
  # partial attempt before recreating it.
  for c in heartbeat pipeline-review certify-check; do cortextos bus remove-cron "$CTX_AGENT_NAME" "$c" 2>/dev/null; done
  if cortextos bus add-cron "$CTX_AGENT_NAME" pipeline-review "0 8 * * 1-5" "Run a morning pipeline review: list all active unit turns with current stage, day count versus target, and stale or at-risk items. Draft escalations for operator approval." \
    && cortextos bus add-cron "$CTX_AGENT_NAME" certify-check "0 17 * * 1-5" "Check all turns in Stage 4 for completion: verify every must-fix item has evidence and re-key is last. Draft a certify summary or deficiency list for operator approval." \
    && cortextos bus list-crons "$CTX_AGENT_NAME" \
    && mkdir -p "$CTX_ROOT/state/$CTX_AGENT_NAME" \
    && touch "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"; then
      cortextos bus add-cron "$CTX_AGENT_NAME" heartbeat "4h" "Read HEARTBEAT.md and follow its instructions. Update heartbeat, check inbox, check stale stages and pending QC items, and continue the highest-priority turnover task." \
        && echo "onboarding complete: configured, crons added, online" \
        || echo "STOP: onboarding is durably marked complete but heartbeat registration failed. Re-run this block; it removes and recreates the cron set idempotently."
  else
    # ROLLBACK: pre-marker failure removes only role crons created in this attempt.
    rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"
    for c in pipeline-review certify-check; do cortextos bus remove-cron "$CTX_AGENT_NAME" "$c" 2>/dev/null; done
    echo "STOP: onboarding completion failed before the durable marker. Role crons were removed and .onboarded was not written; fix the error and re-run this block."
  fi
fi
```

The five completion properties are load-bearing: unresolved fields stop activation; the role-cron set is recreated idempotently; role-cron failure rolls back before the marker; `.onboarded` is the durable completion boundary; and heartbeat is registered only after that boundary.

---

## Step 4: Confirm copilot posture

Send the operator a short completion message naming the configured turn target, SLAs, approval threshold, and schedules. State plainly that vendor dispatch, external messages, spend approval, and rent-ready certification remain human-release decisions.

If a restart interrupts onboarding, begin again at Step 1. The activation block is safe to rerun: it removes and recreates only the documented turnover cron set.
