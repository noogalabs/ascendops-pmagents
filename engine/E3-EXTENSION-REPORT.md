# E3 engine extension report

Subject parent: `3ea772ff0843e72acac52a079724c350de1e653c` (frozen PR296 head).

Semantic source rows were consumed from the reviewed accounting and business-development mapping tables now published as `mapping-tables/accounting.md` (AF-1) and `mapping-tables/bd.md` (BD-1/2/14/18/19, SEAM-11, pointer K-row, fill-exempt, measures, and lanes), rather than re-derived from memory.

## Loud replacements

- AF-1: mapping-declared structured filename resolution rejects a missing declaration target and reports an undeclared structured artifact.
- Assertions: FACT_MATCH, POLICY_DIVERGE, and ORDERING are closed, typed, independently fired and passed; severity-error is fail-closed; measure mismatch rejects.
- Migration: trigger presence produces a named pending record and never changes the pointer automatically.
- Pointer K-row: owner value and explicit fallback are manifested distinctly; missing owner plus missing fallback rejects.
- N-way: the six-seat fixture evaluates all 15 pairs and reports exactly 13 failures.
- Promise safety: fill-exempt members stay absent and visible; removing a member makes the mutation observable. Promise rows cannot pass vacuously when their delivering owner is absent. Lane records have their own schema.

## Compatibility and non-disturbance

Legacy structured artifacts still resolve as `seat-config.json`. Legacy POLICY/SPLIT rows preserve their prior divergence-report semantics. E2 append-plan, timezone-K-row, and frozen-baseline tests remain green. The scenario-1 sealed core is untouched.

## Armed evidence

Named E3 rows exercise every fire/pass direction, the owner/fallback/no-fallback triad, trigger present/absent, unknown-type rejection, measure rejection, severity error/report, and the N=6 all-pairs casualty. Two identical applications of the same fixture are required to serialize byte-identically.

Four isolated mutations were executed before packaging and each died by its named row: truncating the all-pairs loop produced 3 rather than 13 failures; disabling severity-error made the rejection row fail; allowing hints to fill exempt members exposed the forbidden values; and ignoring the declared structured filename broke the declared-name row. These are subject-killing casualties, not neighboring assertions.

Deliverable paths: `engine/cross_seat.py`; `engine/placeholders.py`; `engine/engine.py`; `engine/E3-SCHEMA.md`; `engine/E3-EXTENSION-REPORT.md`; `engine/tests/test_cross_seat.py`; `engine/tests/test_extension_applier.py`.

Completion claim: the E3 wrapper replaces each named silent failure with a typed, fail-closed or explicitly surfaced outcome while leaving the sealed core and frozen E2 behavior intact.

## Post-review production-entry fix-forward

All four review findings were verified at the landed artifact. The rerun path attempted to extract pointer-backed K-rows as questionnaire rows instead of deferring to the cross-seat resolver. A mapping-declared structured filename was enforced before the sealed core's default `seat-config.json` output was materialized under that name. `all_pairs` read peer payloads without the pairwise path's version guard. The config commit helper always created absent targets, even for replace-mode rows.

The wrapper now uses the same pointer resolver on initial and rerun paths; materializes the sealed-core output under the declared safe filename before enforcing its presence; validates every non-current all-pairs participant version; and rejects absent replace targets while allowing creation only for explicitly declared create-mode rows. The sealed core remains byte-unchanged.

Production-entry tests cover pointer-backed rerun determinism, a declared filename different from the sealed-core default, version skew inside an all-pairs population, and the replace-absent/create-declared pair. Each fix was removed or reversed in isolation after the test was written; every planted mutation killed its named row with `ARMED` printed before the result.

Test-gap classification: the original capability and integration tests exercised wrapper helpers directly or never drove the differing declaration through `configure()`. The new named rows bind the production configure/rerun paths so helper-level green cannot substitute for end-to-end reachability.
