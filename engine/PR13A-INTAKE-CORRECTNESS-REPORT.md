# PR13a intake-correctness report

Task: `task_1787719172740_06204033`

Base: PMAgents main after the merged leasing seat (`4870b4bcb45f2e7754a89dd84d3bc8f19c6c30ce`).

## Production corrections

1. The real `engine.py` CLI supplies an explicit empty peer registry. Cross-seat mappings therefore configure with every absent peer held, matching the guided setup path, while the default maintenance invocation remains unchanged.
2. Before any output parent or transaction is created, the engine enumerates the sources consumed by placeholder and non-pointer config-key rows. Any unresolved confirmation marker blocks configuration with the source field and the instruction to confirm the answer and rerun setup. Pointer-backed typed values carry the same protection at coercion.
3. `labeled_integer` joins the closed extractor vocabulary. It requires a declared label and accepts only a full `Label: NN` line, so an earlier unrelated number can never substitute for a semantically bound value.
4. Numeric config-key rows may declare `minimum` and optional `maximum`. Schema validation rejects invalid domains; runtime validation applies after coercion on questionnaire and pointer paths.

The sealed maintenance core remains byte-identical at its pinned SHA-256 (`0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551`).

## Consumer census and boundary

The production mapping census contains exactly one `first_integer` declaration: leasing B3. Maintenance and pm-assist declare none. PR13a lands the shared `labeled_integer` and numeric-domain capabilities with synthetic production-entry casualties. The immediate leasing follow-up changes B3 to `labeled_integer` and declares strict-positive minimums on all five typed cover values: response SLA minutes, decision SLA hours, approval threshold USD, renewal lead days, and renewal response days. No prose-only substitute is accepted.

Unresolved-value production casualties cover leasing A2, A3, D2, B8, and the typed renewal response cover field. Each failure names its own source, prints the resolution path, and leaves zero output.

## Named running guards

- `test_named_real_cli_cross_seat_and_default_maintenance_paths_exit_zero`
- `test_named_mapping_consumed_unresolved_answers_block_all_types_before_output`
- `test_named_mapping_production_entry_supports_literal_first_and_labeled_integer`
- `test_named_labeled_integer_missing_anchor_rejects_through_production_entry`
- `test_named_typed_config_key_domains_reject_negative_and_zero_and_accept_valid`
- `test_named_pointer_numeric_domain_rejects_out_of_range_fallback`
- `test_named_numeric_domain_honors_zero_and_optional_maximum`
- `test_named_numeric_domain_schema_rejects_invalid_declarations`

The mutation bar independently disables each production correction and requires the corresponding named test to fail before restoration. Exact-head CI and both peer seats bind only after those arms, the complete repository gates, manifest custody, and the fresh paginated bot union are green.
