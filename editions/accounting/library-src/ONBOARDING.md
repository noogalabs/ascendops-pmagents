# Accounting Agent Onboarding

The repository configurator has already collected the accounting answers. This
first boot verifies that configured custody and adds deployment wiring; it does
not run a second accounting interview.

## First Boot Gate

1. Read `accounting-config.json` in full and verify that its `seat` is
   `accounting`.
2. Verify the configured values rendered into `IDENTITY.md`, `SOUL.md`,
   `GUARDRAILS.md`, and `config.json` against the operator answers. Never
   re-enter or silently correct them here. If they are wrong, stop and rerun
   `python3 setup.py` from the repository root.
3. Verify that `## Name` in `IDENTITY.md` no longer carries the
   `<!-- Set during onboarding -->` marker. Always replace that marker with
   `$CTX_AGENT_NAME` as the default display value; an operator override changes
   only the value written, not whether the marker is removed.

The only new values collected at first boot are the Telegram bot token and chat
id. Store them in the agent's private environment file; never write them into a
tracked file. If they are not available, stop before registering crons or
writing the onboarding marker.

## Complete onboarding

The accounting cron names and prompts below are retained from the reviewed
template. The transaction shape is the repository's canonical first-boot form:
role crons register before the durable marker, pre-marker failures roll them
back, and the heartbeat cron registers only after completion.

```bash
# FINAL GATE: never register crons or write .onboarded while a rendered
# placeholder or the unfilled identity marker remains.
if grep -rlE '\{\{[^{}]+\}\}|<!-- Set during onboarding' . --include='*.md' --include='*.json' 2>/dev/null | grep -vE 'ONBOARDING\.md|README\.md|skills/onboarding/|node_modules'; then
  echo "STOP: configured files still contain a rendered placeholder or the unfilled identity marker. Re-run python3 setup.py or complete the default display-name replacement before onboarding."
else
  # Remove residue from an interrupted pre-marker attempt.
  for c in ar-digest bank-rec-am bank-rec-pm owner-statements-monthly deposit-deadline-watch; do
    cortextos bus remove-cron "$CTX_AGENT_NAME" "$c" 2>/dev/null
  done
  rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"

  if cortextos bus add-cron "$CTX_AGENT_NAME" ar-digest "0 8 * * 1-5" "Run the ar-rent-posting skill in digest mode: read ledgers, verify payment application, prepare the delinquency feed as data, and flag unapplied or unexplained items. No ledger writes." \
  && cortextos bus add-cron "$CTX_AGENT_NAME" bank-rec-am "0 8 * * 1-5" "Run trust-reconciliation in morning verify-and-flag mode. Compute bank = book = liability, surface changed breaks only, and stop before any correction." \
  && cortextos bus add-cron "$CTX_AGENT_NAME" bank-rec-pm "0 17 * * 1-5" "Run trust-reconciliation in evening verify-and-flag mode. Compute bank = book = liability, surface changed breaks only, and stop before any correction." \
  && cortextos bus add-cron "$CTX_AGENT_NAME" owner-statements-monthly "0 9 1 * *" "Run owner-statement-drafting for the prior month: draft explainable statements and owner-draw recommendations, draft-only, route any external send or draw through approval." \
  && cortextos bus add-cron "$CTX_AGENT_NAME" deposit-deadline-watch "30 8 * * *" "Run security-deposit-accounting deadline review: tie deposits held to ledgers, check statutory deadlines, and alert on any return inside the deadline window. No money moves." \
  && cortextos bus list-crons "$CTX_AGENT_NAME" \
  && touch "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"; then
  if cortextos bus add-cron "$CTX_AGENT_NAME" heartbeat "2h" "Read HEARTBEAT and update your status."; then
    echo "onboarding complete: configured, crons added, online"
  else
    echo "STOP: onboarding is durably marked complete but heartbeat registration failed. Re-run this block; the role-cron and marker steps are idempotent."
  fi
else
  # ROLLBACK: no pre-marker failure may leave role crons or a marker behind.
  for c in ar-digest bank-rec-am bank-rec-pm owner-statements-monthly deposit-deadline-watch; do
    cortextos bus remove-cron "$CTX_AGENT_NAME" "$c" 2>/dev/null
  done
  rm -f "$CTX_ROOT/state/$CTX_AGENT_NAME/.onboarded"
    echo "STOP: onboarding did not complete. Fix the reported error and re-run this block."
  fi
fi
```

After the block succeeds, re-enter normal startup through `AGENTS.md`.
