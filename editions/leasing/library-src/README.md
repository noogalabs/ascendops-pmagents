# Leasing / Renewals Coordinator Agent Template

This package is a classroom-ready leasing and renewals copilot agent template for property managers.

The agent covers the lead-to-lease and renewals lifecycle: applicant screening, lease abstraction, renewal scoring and offer prep, and fair-housing-safe communications.

The agent is intentionally copilot-first:
- It reads source data (applications, leases, payment history).
- It screens, abstracts, and scores against written criteria.
- It drafts offers, decisions, and applicant/resident messages.
- It flags risk, missing data, and fair-housing exposure.
- It never sends an applicant a decision, executes or sends a lease, sends a renewal offer, or sends any applicant- or resident-facing message without human approval.

## Supported setup

From the PMAgents repository root, run `python3 setup.py`, choose **Leasing Coordinator**, and answer the guided prompts. Setup validates the complete answer set and writes the declared `leasing-config.json` source of truth alongside the configured library.

Do not install this edition by manually replacing a short placeholder list. The guided setup is the supported path because it collects and validates every value required before activation.

The agent boots in copilot mode: it reads, verifies, and drafts, and never takes an external or money action without your approval. Review the approval guardrails before you connect any live property-management system.

## Recommended crons (add after setup)

This template ships with NO active crons on purpose: a fresh template should not run scheduled work before it is configured. Once the agent is set up, add the ones you want. Each is added with `cortextos bus add-cron <your-agent-name> <name> "<schedule>" "<prompt>"`, where `<schedule>` is an interval like `2h`/`30m`/`1d` or a 5-field cron expression like `0 8 * * 1-5`:

- `heartbeat`, schedule `2h`: Read HEARTBEAT.
- `applicant-screening-digest`, schedule `0 8 * * 1-5`: Run the applicant-screening skill in digest mode: score new applications against the written rubr....
- `renewal-window-am`, schedule `0 8 * * 1-5`: Run renewals-coordinator in morning mode: detect leases entering the renewal window, score risk o....
- `renewal-window-pm`, schedule `0 17 * * 1-5`: Run renewals-coordinator in evening mode: surface changed renewal flags and deadline pressure only.
- `lease-abstraction-intake`, schedule `0 9 * * 1-5`: Run lease-abstraction on any newly received leases: extract terms into structured data and flag m....
- `fair-housing-presend-sweep`, schedule `30 8 * * *`: Run fair-housing-guard over any pending applicant- or resident-facing drafts and screening criteria.
