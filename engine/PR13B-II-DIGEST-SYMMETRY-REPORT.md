# PR13b-ii resolved pointer digest report

Resolved cross-seat pointer records now persist `value_sha256` for the live
owner value they verified. Held pointer records already persisted the same
digest, so both states now carry artifact-custody evidence without copying the
owner's raw answer into the dependent seat. Changing the live owner answer
changes the resolved digest; the record continues to omit a raw `value` field.

The named casualty configures the same pointer against two live owner values,
asserts each canonical digest, asserts the digests differ, and asserts neither
record duplicates the raw value. Removing the single resolved-record digest
field kills that casualty.

## Daylight design deferrals

Five consumer groups were examined and deliberately not implemented because
their current artifacts do not uniquely define an executable consumer:

1. `/deposit_return_days`: maintenance A3 is unstructured prose, while the
   pointer extractor vocabulary has no safe integer-duration grammar. A
   daylight review must choose a structured owner line or a ruled extractor.
2. Leasing communications window: the mapping table names an org
   `context.json` fallback, but PMAgents has no transport for that framework
   artifact and no in-repo fallback value. Context-seed transport must land
   before the two endpoint rows.
3. Held-without-local pointers: the shipped mapping census contains no pointer
   row without `holding_question_id`. Mapping authority must name owner,
   consumer, and path before such a row exists.
4. Keyed jurisdiction carrier: A1 line grammar, A17 set grammar, key
   normalization, and the legacy scalar's fate require an explicit design
   ruling. The PR21 fail-closed guard and documented residual remain unchanged.
5. SEAM-20 and SEAM-27: their refs are cross-format money-pair prose and
   day-of-month prose. Existing `currency`/`days` measures are identity at this
   path, so safe shared measure grammars and golden fixtures must be designed
   before the checks can evaluate.

The David-locked Gap Rule passes at the content-origin leg. This shard adds one
structural custody digest and no property-management number, threshold, script,
workflow, questionnaire content, mapping row, or judgment call. Business-
development day mode remains PR18/David-gated and renewals remain input-gated.
