# Turnover Coordinator Agent Template

This package is a classroom-ready turnover coordinator copilot agent template for property managers.

The agent owns the make-ready pipeline from the moment a unit goes vacant through rent-ready certification: move-out possession intake, inspection findings, scope and punch list, multi-trade coordination, QC with photo evidence, re-key, and a signed certify gate before handing off to leasing.

The agent is intentionally copilot-first:
- It reads possession confirmations, inspection reports, and move-out media.
- It builds a structured scope (must-fix vs nice-to-fix) and a trade dependency schedule.
- It drafts every vendor dispatch and approval request — never sends without your sign-off.
- It tracks SLA clocks on each stage and alerts you when a stage goes stale.
- It runs a hard certify gate: all must-fix items verified done, re-key last, before any rent-ready signal leaves.
- It never certifies, dispatches a vendor, or approves a spend without human approval.

## Guided setup

From the PMAgents repository root, run `python3 setup.py`, choose **Turnover Coordinator**, and answer the guided prompts. Setup validates the complete answer set and writes the declared `turnover-config.json` source of truth alongside the configured library.

Do not replace template fields by hand. If an operating answer changes, rerun the guided setup so the structured source of truth and every rendered surface remain aligned. After setup, follow `ONBOARDING.md` only to verify the configured files, connect the Telegram bot, and register the documented crons.

The agent boots in copilot mode: it reads, triages, and drafts, and never takes an external or money action without your approval. Review the approval guardrails and certify gate rules before you connect any live inspection or work-order system.

## Recommended crons (add after setup)

This template ships with NO active crons on purpose: a fresh template should not run scheduled work before it is configured. Once the agent is set up, add the ones you want. Each is added with `cortextos bus add-cron <your-agent-name> <name> "<schedule>" "<prompt>"`, where `<schedule>` is an interval like `4h`/`1d` or a 5-field cron expression like `0 8 * * 1-5`:

- `heartbeat`, schedule `4h`: Read HEARTBEAT.md and follow its instructions. Update heartbeat, check inbox, check for stale stages, check pending QC items, and continue the highest-priority turnover task.
- `pipeline-review`, schedule `0 8 * * 1-5`: Run a morning pipeline review: list all active unit turns with current stage, day count vs target, and any stale or at-risk items. Draft escalations for any stale stages.
- `certify-check`, schedule `0 17 * * 1-5`: Check all turns in Stage 4 (QC) for completion: verify every must-fix item has evidence and re-key is last. Draft a certify summary or a deficiency list for any that need attention.
