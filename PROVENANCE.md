# AscendOps PMAgents seed provenance

This is a fresh seed, not a history import. The seed preserves review custody through source and destination SHA-256 values in `provenance/source-files.tsv` without importing fleet-internal commit history. Original internal source locators are retained beside the excluded evidence in the org-private retention area; the member repository uses neutral artifact IDs.

## Reviewed sources

- Scenario foundation content: `2518058073348f66e04074c9b38f768924935b3a`; scenario review CLEAR `1787511891345-piper-taoml`, relocation/content-identity acceptance `1787625375769-dane-6cdhr`.
- Lane-1 engine content: `97ec10f9c53f2a07420cf3fcf56f9b735b4e89a7`; CLEAR relayed in `1787624894645-dane-eo661`, relocation/content-identity acceptance `1787625375769-dane-6cdhr`.
- E2 extension content: `3ea772ff0843e72acac52a079724c350de1e653c`; NORMAL review CLEAR relayed in `1787638034656-dane-vsn93`.
- E3 extension content: `c4d2cd9c`; design conformance CLEAR `1787664519844-collie-vepsk`, NORMAL review CLEAR `1787665935655`-era record. Seven delta files are re-anchored under `engine/`; the TSV records source and destination hashes separately wherever the seed's member-safe flattening or documentation sanitization changes bytes.
- Six mapping tables and six Ridgeline fixtures: mapping-owner reviewed outputs dated 2026-08-23/25; each original and destination hash is pinned in the TSV.

## Flattening decision

The former product subtree is flattened into `engine/` and `editions/maintenance/`. Mapping tables use neutral seat filenames under `mapping-tables/`; Ridgeline fixtures use neutral seat filenames under `fixtures/ridgeline/`. When member-facing naming changes a byte, the TSV records both the reviewed source hash and the seeded destination hash rather than claiming false byte identity.

## Distributed seam register

The six mapping tables collectively are the authoritative seam register; no derived consolidated register exists. Maintenance carries the original A3 cross-seat mark. Leasing carries X1–X6, with X1 carrying the mapping-owner QA ownership amendment. Turnover owns SEAM-1–19. Accounting owns SEAM-20–32. PM-assist owns SEAM-33–37 after the parallel-minting QA amendment. BD carries BD-1–19 under the seat-prefixed parallel-minting rule. This paragraph is navigation metadata only; seam content remains single-sourced in the tables.

## Excluded evidence

Thirty-three internal evidence files are deliberately excluded from the member product. Each is represented by a neutral artifact ID, reviewed head, content hash, and exact retention location in `provenance/source-files.tsv`. The bytes were re-homed, not deleted, under `orgs/ascendops/ops/pmagents-evidence/source-3ea772ff/`. Internal reports, walkthrough packages, diagnostics, and transcripts stay there; they are not scrubbed into a product that does not need them.

The first seed is accepted only with a zero hygiene census and no baseline file. Any future source addition must pass the same gates rather than inherit an exemption.

## E3 re-anchor

The E3 delta from reviewed head `c4d2cd9c` maps the org-side glue subtree to the flattened `engine/*` product surface. `engine.py` retains the seeded `editions/maintenance/` paths; the two changed test files retain their checked-in, history-free fixtures. E3 documentation uses member-facing product and mapping-table names. The seven artifact rows added for this re-anchor bind every org-side source hash to its landed destination hash, while the org-private locator table retains the original source paths.

## Guided setup wrapper

The root `setup.py` entry point, its rejection-renderer census, README guidance,
and wrapper tests are product-native files authored in this repository. They
delegate to the reviewed engine without changing its output bytes or the sealed
maintenance configurator. Their review custody is the PMAgents pull request and
exact-head CI; they do not claim an org-side source hash in the imported-source
TSV.
