# Explicit re-run merge policy

Reconfiguration is an operator-invoked action. It is never scheduled and never runs from an update cron.

| File class | Re-run policy |
|---|---|
| `config.json` owned keys | Replace through the sealed configurator's key census; unowned keys must remain byte-equivalent |
| Template placeholders | First run substitutes from the reviewed mapping-table rows. Markdown values receive per-placeholder delimiters; JSON values receive recorded JSON pointers. Reruns use only the prior `managed_surfaces` manifest and fail shut if a locator changed. |
| `IDENTITY.md`, `SOUL.md`, `GUARDRAILS.md` | Replace only the managed configuration block recorded by the manifest |
| `seat-config.json` | Replace durable raw/derived answers and record engine + library versions |
| Config-key K rows | Schema-v2 mappings overwrite only declared RFC6901 paths, record typed manifest rows, and rerun only through those rows. Missing or hand-edited paths reject. |
| Cross-seat FACT/POLICY seams | FACT values resolve through owner pointers or remain visibly held pending an absent owner. POLICY/SPLIT values stay local and disagreements surface for eyeball; they are never unified. |
| Cross-seat owner append | Appender commit persists a replayable plan. A separate atomic owner apply records the same plan ID and grows the owner structure; pending and already-applied states are explicit. |
| `memory/`, `tasks/`, `.env` variants, `logs/`, `daily-logs/`, dated top-level logs | Never touch; census and copy byte-for-byte from the existing agent into the atomic candidate |
| Existing agent prose outside engine delimiters | Preserve |

The complete candidate is built beside the destination under a destination lock. A durable, fsynced transaction journal makes death between renames recoverable on the next invocation. Only after validation, sealed-core execution, protected-state restoration, and version stamping succeed is the directory swapped into place. A failed intake leaves the destination untouched. Existing-output reruns require source and destination to be the same directory so accumulated state can never come from the wrong tree.
