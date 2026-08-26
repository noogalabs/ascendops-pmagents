# Turnover make-ready safety successor

This successor closes the five findings from the first live automated review of
the merged turnover edition. The reviewed subject is the shipped
`.claude/skills/make-ready-pipeline/make_ready.py` production helper.

## Closed findings

1. **Evidence-backed certification:** a verified must-fix or re-key item with a
   blank evidence reference remains open and names the affected task. Evidence
   is gate-consumed reference data: only a genuine nonblank string is valid;
   present non-string values remain aggregated as `INVALID EVIDENCE` items
   naming the task, Python type, and raw value. This deliberately preserves the
   pre-round-6 fail-closed behavior that Piper proved differentially between
   `5e7c8844` and `0f5c513e`, without weakening None-only coalescing for IDs,
   dates, or descriptive fields.
2. **Re-key finality:** certification requires re-key to begin only after every
   other scheduled task ends, regardless of classification. Independent early
   re-key, must-fix work after re-key, and cosmetic work after re-key all fail
   closed by task name. The member-facing skill contract carries the same
   all-scheduled-task language and bans the narrower must-fix-only form.
3. **Declared dependency graph:** task IDs must be unique and nonblank, and every
   `depends_on` value must name a declared task before topological sorting begins.
   IDs and dependencies are stripped once at ingestion and the canonical values
   flow through adjacency, scheduling, critical-path analysis, and certification;
   duplicates are detected after normalization. None-only coalescing preserves
   present falsy values such as numeric ID `0`; dependency lists accept only
   absent, list, or tuple forms, and an AST census bans user-input `.get()` values
   from regaining value-or-default `or` expressions outside one documented
   logical re-key exclusion.
4. **True critical path:** a forward schedule plus backward latest-start pass
   reports zero-slack work only. At an unequal two-branch join, the short branch
   is no longer mislabeled critical. Scheduling is the single duration-parsing
   boundary: blank duration keeps the documented one-day default, while
   malformed, zero, and negative durations reject by task and field before date
   math. The stored canonical integer flows into CPM without reparsing.
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
   A shared strict task-date parser distinguishes a genuinely blank optional
   progress date from any present-but-malformed value; required stage and
   certification dates reject missing or malformed values with named fields and
   raw inputs. An AST census pins every remaining direct `parse_date` consumer
   to the existing loud critical-path or CLI paths.

## Running guards

`editions.turnover.tests.test_make_ready` carries thirty named casualties covering
the five original review directions, four live-review recut directions, both
future-anchor directions, the missing-stage-entry rejection, and configured CLI default. The turnover
configurator suite remains unchanged and green; the source template and sealed
maintenance core remain outside this patch.
