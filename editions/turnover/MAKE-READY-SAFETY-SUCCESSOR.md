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
   closed by task name. The member-facing skill contract carries the same
   all-scheduled-task language and bans the narrower must-fix-only form.
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
   Either anchor being in the future rejects loudly by task, field, and date
   before staleness age is computed. A progress date earlier than current-stage
   entry also rejects with both fields and dates; the tool never guesses which
   contradictory record to substitute. If real boards intentionally carry
   prior-stage progress forward, that requires an explicit reviewed state in a
   later contract decision rather than a silent default here.

## Running guards

`editions.turnover.tests.test_make_ready` carries thirteen named casualties covering
the five original review directions, four live-review recut directions, both
future-anchor directions, the missing-stage-entry rejection, and configured CLI default. The turnover
configurator suite remains unchanged and green; the source template and sealed
maintenance core remain outside this patch.
