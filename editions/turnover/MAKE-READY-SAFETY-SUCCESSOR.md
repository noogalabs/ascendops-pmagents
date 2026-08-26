# Turnover make-ready safety successor

This successor closes the five findings from the first live automated review of
the merged turnover edition. The reviewed subject is the shipped
`.claude/skills/make-ready-pipeline/make_ready.py` production helper.

## Closed findings

1. **Evidence-backed certification:** a verified must-fix or re-key item with a
   blank evidence reference remains open and names the affected task.
2. **Re-key finality:** certification requires re-key to begin only after every
   other scheduled task ends, regardless of classification. Independent early
   re-key, must-fix work after re-key, and cosmetic work after re-key all fail
   closed by task name.
3. **Declared dependency graph:** task IDs must be unique and nonblank, and every
   `depends_on` value must name a declared task before topological sorting begins.
   IDs and dependencies are stripped once at ingestion and the canonical values
   flow through adjacency, scheduling, critical-path analysis, and certification;
   duplicates are detected after normalization.
4. **True critical path:** a forward schedule plus backward latest-start pass
   reports zero-slack work only. At an unequal two-branch join, the short branch
   is no longer mislabeled critical.
5. **Configured progress staleness:** the CLI reads the configured
   `stale_stage_alert_days` unless explicitly overridden. Unfinished must-fix
   work measures staleness from `last_progress_date`, or visibly from required
   `stage_entered_date` when no progress exists. It never substitutes planned end.

## Running guards

`editions.turnover.tests.test_make_ready` carries nine named casualties covering
the five original review directions, the two live-review recut directions, the
missing-stage-entry rejection, and configured CLI default. The turnover
configurator suite remains unchanged and green; the source template and sealed
maintenance core remain outside this patch.
