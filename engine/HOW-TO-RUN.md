# AscendOps PMAgents glue engine — operator runbook (v1, we-run-and-hand-back)

1. Receive the filled questionnaire as a Markdown file. Do not run against a live member directory; begin with a provisioning copy.
2. Run:

   `python3 engine.py SOURCE_AGENT FILLED_ANSWERS OUTPUT_AGENT --seat maintenance-coordinator`

3. If a `REJECT LIST` is printed, correct every named item and rerun. A rejection writes no agent files.
4. Inspect `OUTPUT_AGENT/seat-config.json`, `key-census.json`, and `contradiction-report.md`. Confirm the version stamp and named skips.
5. Run the configured agent's normal boot smoke and human QA before hand-back.
6. To apply changed answers later, invoke the same command explicitly with the existing configured agent as `SOURCE_AGENT` and its path as `OUTPUT_AGENT`. Memory, tasks, `.env`, daily logs, and prose outside engine delimiters remain unchanged.

Only `maintenance-coordinator` is currently mapped. Any other seat rejects until Lane 2 installs its reviewed mapping and library. Drive retrieval is intentionally parked; file intake is the v1 path.

Schema-v2 mappings may emit cross-seat owner-append plans. After the appender transaction succeeds, inspect its `seat-config.json` for `cross_seat.append_plans` and run `python3 apply_append.py APPENDER_AGENT_DIR OWNER_AGENT_DIR PLAN_ID`. The owner apply is a separate atomic operation: a crash between operations leaves the plan persisted and visibly `PENDING`, and replay is safe.

If either seat mapping declares a structured filename other than `seat-config.json`, pass the reviewed mapping files with `--appender-mapping APPENDER_MAPPING.json` and `--owner-mapping OWNER_MAPPING.json`. The append operation resolves each participant artifact from its own declaration; it never guesses a structured filename from directory contents.
