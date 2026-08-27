# AscendOps PMAgents glue engine — operator runbook (v1, we-run-and-hand-back)

Commands below use `python3` (macOS/Linux/VPS). On native Windows, use `python`
instead; see the README's "Setup by platform" section for the full Windows flow.

1. Receive the filled questionnaire as a Markdown file. Do not run against a live member directory; begin with a provisioning copy.
2. Run:

   `python3 engine.py SOURCE_AGENT FILLED_ANSWERS OUTPUT_AGENT --seat maintenance-coordinator`

   Installed mapping seats use the same command with `--seat pm-assist`,
   `--seat leasing-coordinator`, or `--seat turnover-coordinator`. Turnover's
   declared structured artifact is `turnover-config.json`.

3. If a `REJECT LIST` is printed, correct every named item and rerun. A rejection writes no agent files.
4. Inspect `OUTPUT_AGENT/seat-config.json`, `key-census.json`, and `contradiction-report.md`. Confirm the version stamp and named skips.
5. Run the configured agent's normal boot smoke and human QA before hand-back.
6. To apply changed answers later, invoke the same command explicitly with the existing configured agent as `SOURCE_AGENT` and its path as `OUTPUT_AGENT`. Memory, tasks, `.env`, daily logs, and prose outside engine delimiters remain unchanged.

The four listed seats are currently installed. Any other seat rejects until its
reviewed mapping and library are registered. Drive retrieval is intentionally
parked; file intake is the v1 path.

Schema-v2 mappings may emit cross-seat owner-append plans. After the appender transaction succeeds, inspect its `seat-config.json` for `cross_seat.append_plans` and run `python3 apply_append.py APPENDER_AGENT_DIR OWNER_AGENT_DIR PLAN_ID`. The owner apply is a separate atomic operation: a crash between operations leaves the plan persisted and visibly `PENDING`, and replay is safe.

If either seat mapping declares a structured filename other than `seat-config.json`, pass the reviewed mapping files with `--appender-mapping APPENDER_MAPPING.json` and `--owner-mapping OWNER_MAPPING.json`. The append operation resolves each participant artifact from its own declaration; it never guesses a structured filename from directory contents.
