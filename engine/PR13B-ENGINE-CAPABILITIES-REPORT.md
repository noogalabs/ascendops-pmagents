# PR13b-i engine capability report

This shard adds only shared engine capabilities. It does not activate new
edition consumers, change cross-seat ownership, or ship the gated business-
development day-mode row.

The resolver now supports an explicit live holding-answer fallback for a
pointer-backed config row. When its owner seat is absent,
`fallback_from: holding_answer` rereads the pointer's declared holding path on
every configuration run and records `held_holding_answer`; it never substitutes
a frozen mapping literal. After either owner or holding resolution, a pointer
row may select `window_start` or `window_end` before the ordinary config type
and domain checks run.

FACT_MATCH now applies the declared `maintenance_platform` measure before
comparison. Equivalent platform facts written as different questionnaire prose
therefore compare at platform grain, while a different platform still surfaces
the existing contradiction result. Unsupported measures reject rather than
quietly reverting to raw-text equality.

The shared platform extractor deliberately retains the pre-existing
single-token grammar in this engine-only shard. A multi-word name such as
`Rent Manager for maintenance` currently extracts `Manager`; successor task
`task_1787757982072_93367381` owns a fail-closed multi-word identity grammar.
That inherited bound is recorded here rather than expanded inside this PR.

The David-locked Gap Rule passes at the content-origin leg: this shard contains
only structural resolution, extraction, validation, and comparison plumbing.
It introduces no property-management numbers, thresholds, scripts, workflows,
or judgment calls and therefore requires no invented domain-practice content.

The named casualties cover both owner and absent-owner pointer resolution, a
production configuration from a changed live communications-window answer,
same-platform/different-prose equality, different-platform disagreement, and
mapping-load rejection for unsupported pointer extractor and fallback shapes.
Each of the three capability branches was independently removed during review;
its named casualty failed before the exact bytes were restored.
