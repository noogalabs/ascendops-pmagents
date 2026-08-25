# Setup rejection renderer census

The guided wrapper always shows the engine's raw structured row and reason, then
adds the member-language question, explanation, and example below. Unknown rows
remain visible with support guidance. The renderer never converts, suppresses,
or replaces an engine rejection.

| Structured row family | Member question | Valid-answer example |
|---|---|---|
| `mapping.config_keys` / `config_keys` | Configuration question named by the row | `America/Denver` for a timezone |
| `mapping` | Installed edition mapping | Reinstall or update the PMAgents checkout |
| `template` / `protected_state` | Template or existing agent directory | Choose a clean template; retain memory/tasks |
| `structured_answers_file` | Configured-answer artifact | Restore the edition mapping and rerun |
| `sealed_core.<stage>` | Questionnaire answer named by the stage | Plain operational content with no credentials |
| `cross_seat` | Connected-seat question named by the row | Configure the named owner seat first |
| `append-plan` / `appender.*` / `owner.*` | Cross-seat handoff | Rerun setup for both named seats |
| `file` | Completed answers file | Choose a UTF-8 edition answers file |
| `output` | Configured agent destination | New directory or same configured agent |
| `seat` | Setup edition | Choose an edition listed by setup |
| `A1`–`D10` | Full questionnaire prompt with its row ID; raw ID if the prompt cannot be loaded | Confirmed answer or `unsure` |
| `cover.*` | Exact cover-sheet field | Requested company value |
| unknown row | Raw row plus support guidance | Share the displayed row with support |

This table is the auditable family census. Every row is bound to a named wrapper
test, including the unknown-row fail-open path.
