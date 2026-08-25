# AscendOps PMAgents

AscendOps PMAgents is the private, paid-edition configuration engine for property-management agent seats. It turns reviewed questionnaires, mapping tables, and edition libraries into configured agents through a fail-closed, atomic workflow.

The repository starts with the reviewed maintenance edition and the six-seat mapping/fixture set. Run the engine only against a provisioning copy, inspect every generated artifact, and complete human QA before hand-back.

## Layout

- `engine/` — intake, validation, substitution, cross-seat, and atomic-transaction code.
- `editions/maintenance/` — sealed maintenance configurator, answer format, and source library.
- `mapping-tables/` — the six authoritative mapping tables; collectively they are the cross-seat seam register.
- `fixtures/ridgeline/` — fictional integration fixtures.
- `provenance/` — source and destination hashes plus excluded-evidence custody.
- `ci/` and `.github/` — hygiene and regression gates.

See `engine/HOW-TO-RUN.md` for the operator flow. This repository contains product files only; internal walkthrough transcripts and build evidence remain in the org-private retention area named in `PROVENANCE.md`.
