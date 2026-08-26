# Accounting Agent Template

This package is a classroom-ready accounting copilot agent template for property managers.

The agent is intentionally copilot-first:
- It reads source data.
- It verifies and reconciles.
- It drafts financial artifacts.
- It flags discrepancies.
- It never moves money, posts ledger corrections, sends owner draws, returns deposits, releases vendor payments, or sends external financial documents without human approval.

## Guided setup

Run `python3 setup.py` from the repository root and select the Accounting
edition. The guided configurator is the only supported configuration path; do
not replace placeholders by hand. The generated `accounting-config.json` is the
source of truth for configured answers. If an answer changes, rerun
`python3 setup.py`.

At first boot, `ONBOARDING.md` verifies the configured files and collects only
deployment credentials that could not exist during repository configuration.

The agent boots in copilot mode: it reads, verifies, and drafts, and never takes an external or money action without your approval. Review the approval guardrails before you connect any live financial system.

## Recommended crons (add after setup)

This template ships with NO active crons on purpose: a fresh template should not run scheduled work before it is configured. Once the agent is set up, add the ones you want. Each is added with `cortextos bus add-cron <your-agent-name> <name> "<schedule>" "<prompt>"`, where `<schedule>` is an interval like `2h`/`30m`/`1d` or a 5-field cron expression like `0 8 * * 1-5`:

- `heartbeat`, schedule `2h`: Read HEARTBEAT.
- `ar-digest`, schedule `0 8 * * 1-5`: Run the ar-rent-posting skill in digest mode: read ledgers, verify payment application, and prepa....
- `bank-rec-am`, schedule `0 8 * * 1-5`: Run trust-reconciliation in morning verify-and-flag mode.
- `bank-rec-pm`, schedule `0 17 * * 1-5`: Run trust-reconciliation in evening verify-and-flag mode.
- `owner-statements-monthly`, schedule `0 9 1 * *`: Run owner-statement-drafting for the prior month: draft explainable statements and owner-draw rec....
- `deposit-deadline-watch`, schedule `30 8 * * *`: Run security-deposit-accounting deadline review.
