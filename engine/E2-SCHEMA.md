# AscendOps PMAgents Glue E2 Mapping and Cross-Seat Schema

Schema v1 mappings remain readable and preserve the frozen L1 behavior. Schema v2 mappings must declare exactly one `config_keys` row for `/timezone`, sourced from `cover.timezone` with the `identity` extractor and string type.

## P-row site integrity

A placeholder row may declare exact load-bearing sites:

```json
{"placeholder":"turn_target_days","source":"B2","extractor":"integer","sites":[{"file":".claude/skills/make-ready-pipeline/SKILL.md","count":1}]}
```

The global template census still rejects unknown tokens and P-rows absent everywhere. A declared site adds a file-and-count assertion, so an occurrence elsewhere cannot hide a missing skill destination.

## Config-key rows

```json
{"path":"/timezone","source":"cover.timezone","extractor":"identity","value_type":"string","mode":"replace"}
```

`path` is an RFC6901 pointer into `config.json`. `mode` is `replace` unless the mapping explicitly owns creation. Values are typed as `string`, `integer`, `number`, or `boolean`. Every write is recorded in `configuration_engine.managed_surfaces` with `row_type=config_key`, pointer, question provenance, and typed value. Reruns use that manifest pointer and reject a hand edit or missing mapping row.

## Graduated cross-seat doctrine

Schema-v2 seam mappings declare `cross_seat.pointers`, `checks`, `appends`, and `never_graduate`.

- FACT pointer with owner present: holder stores owner seat/question and no copied value.
- FACT pointer with owner absent: holder stores one value under `cross_seat.held`, including `held_pending_seat`.
- POLICY/SPLIT check: values stay owned by their seats; a disagreement becomes an `EYEBALL` item in the contradiction report and is never unified.
- Owner append: the appender atomically persists a stable plan in `cross_seat.append_plans`. `apply_append.py` performs a separate atomic transaction on the owner directory and records the plan ID in the owner's `cross_seat.appends` ledger. An unapplied plan is visible as `PENDING`; replay is a no-op.

Seam-enabled configuration requires an explicit seat registry. Owner paths are never inferred from cwd. A v2 seat includes a compatibility guard in its managed-surface manifest, which makes the actual L1 engine reject a reverse read rather than silently deleting the new schema.

## Operator apply

```text
python3 engine/apply_append.py APPENDER_AGENT_DIR OWNER_AGENT_DIR PLAN_ID
```

Exit 0 prints `applied` or `already-applied`. Invalid identities, missing plans, future engine/schema versions, and moved owner paths fail loud.
