# AscendOps PMAgents

AscendOps PMAgents is the private, paid-edition configuration engine for property-management agent seats. It turns reviewed questionnaires, mapping tables, and edition libraries into configured agents through a fail-closed, atomic workflow.

The repository starts with the reviewed maintenance edition and the six-seat mapping/fixture set. Run the engine only against a provisioning copy, inspect every generated artifact, and complete human QA before hand-back.

## Layout

- `engine/` — intake, validation, substitution, cross-seat, and atomic-transaction code.
- `editions/maintenance/` — sealed maintenance configurator, answer format, and source library.
- `editions/pm-assist/` — mapping-driven property-manager assistant edition, questionnaire, fixture, and source library.
- `mapping-tables/` — the six authoritative mapping tables; collectively they are the cross-seat seam register.
- `fixtures/ridgeline/` — fictional integration fixtures.
- `provenance/` — source and destination hashes plus excluded-evidence custody.
- `ci/` and `.github/` — hygiene and regression gates.

See `engine/HOW-TO-RUN.md` for the operator flow. This repository contains product files only; internal walkthrough transcripts and build evidence remain in the org-private retention area named in `PROVENANCE.md`.

## Guided member setup

From the repository root, run this one command:

```sh
python3 setup.py
```

The setup interview offers the installed edition, asks where the clean template
and configured agent should live, and then walks the questionnaire in plain
language. Enter `unsure` to mark an answer for later confirmation; the generated
agent skips features that depend on it. If setup stops, run the same command and
choose the same answers file to resume. Existing configured agents are safely
reconfigured through the same flow rather than overwritten as new installs.

On success, setup prints the configured agent directory and the next review
step. On rejection, it shows the engine's exact row plus a plain-language fix;
unknown rows remain visible for support. See [the renderer census](docs/rejection-renderer.md).

Supported today: macOS and Linux with Python 3. Windows is not yet a supported
runner platform.

Choose `Property manager assistant` in the guided setup to configure the PM-assist
edition. Its cross-seat pointers remain inert and visibly held when their owner seat
is not installed; setup never invents a peer value.
