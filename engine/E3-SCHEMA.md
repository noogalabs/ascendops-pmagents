# AscendOps PMAgents engine schema E3

E3 extends the wrapper schema without changing the sealed scenario-1 core.

## Structured answers artifact

Mappings may declare `structured_answers_file` as one safe JSON basename. An omitted declaration retains the v2-compatible `seat-config.json` default. A declared file that is absent rejects configuration. A second `*-config.json` artifact not named by the mapping is surfaced in the contradiction report rather than silently ignored.

## Cross-seat assertions

`cross_seat.checks[]` uses a closed `type` vocabulary:

- `FACT_MATCH`: equal values pass; mismatch reports or rejects when `severity: error`. Promise-class rows report `UNBACKED` when the delivering seat is absent. When measures are declared, both sides must name the same measure.
- `POLICY_DIVERGE`: differing values are preserved and surfaced for human review; agreement is clean. Legacy `POLICY` and `SPLIT` rows retain this behavior until their mapping is re-declared.
- `ORDERING`: evaluates a closed comparison operator (`gte`, `gt`, `lte`, or `lt`, including symbolic spellings) and surfaces a violation.

Unknown assertion types, operators, severity values, and inconsistent measures reject at load. `cross_seat.all_pairs[]` evaluates every pair in its declared participant population. `cross_seat.cross_seat_lane[]` records routing lanes separately from comparable values.

## Pointer states and config keys

A pointer may declare `migration_pending`, `migration_trigger`, and `migrates_to`. Presence of the trigger seat emits a pending migration record but never flips ownership automatically.

A config-key row may use `value_from: pointer` plus `pointer_name`. Owner presence resolves the owner's value. Owner absence uses only an explicitly declared `fallback`, records `held_fallback` in the managed-surface manifest, and rejects when no fallback exists.

Typed numeric config-key rows may declare numeric `minimum` and `maximum` bounds. Bounds are valid only for `integer` and `number` rows, `minimum` cannot exceed `maximum`, and the engine applies the domain after coercion for both questionnaire-backed and pointer-backed values. Domain failure names the config-key path and blocks all output.

## Executable intake values

Any questionnaire or cover value consumed by a placeholder or non-pointer config-key row must be resolved before configuration. A `NEEDS-*` confirmation marker blocks activation with the source field and the resolution path; an unresolved string cannot silently deactivate a rendered policy gate, and an unresolved numeric value cannot escape as a coercion traceback. Unconsumed answers retain their prior held/provenance behavior.

The `labeled_integer` extractor requires a nonblank `label` declaration and reads only a full `Label: NN` line. Earlier unrelated numerals are ignored. Absence of the declared anchor rejects through the production entry instead of guessing from prose.

## Promise fill policy

`cross_seat.fill_exempt` is a closed set of promise-bearing derived fields. Fields in the set never consume `fill_hints`; absence remains absence and gets a named report item. Removing any member makes its hint eligible, which is pinned as a mutation casualty.

All E3 state is deterministic JSON and remains inside the wrapper-managed transaction.
