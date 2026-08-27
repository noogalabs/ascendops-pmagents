# AscendOps PMAgents

AscendOps PMAgents is the private, paid-edition configuration engine for property-management agent seats. It turns reviewed questionnaires, mapping tables, and edition libraries into configured agents through a fail-closed, atomic workflow.

The repository starts with the reviewed maintenance edition and the six-seat mapping/fixture set. Run the engine only against a provisioning copy, inspect every generated artifact, and complete human QA before hand-back.

## Layout

- `engine/` — intake, validation, substitution, cross-seat, and atomic-transaction code.
- `editions/maintenance/` — sealed maintenance configurator, answer format, and source library.
- `editions/pm-assist/` — mapping-driven property-manager assistant edition.
- `editions/leasing/` — mapping-driven leasing and renewals edition.
- `editions/turnover/` — mapping-driven turnover questionnaire, fictional fixture, tests, and make-ready library.
- `editions/accounting/` — mapping-driven accounting questionnaire, fictional fixture, tests, and reviewed accounting library.
- `mapping-tables/` — the six authoritative mapping tables; collectively they are the cross-seat seam register.
- `fixtures/ridgeline/` — fictional integration fixtures.
- `provenance/` — source and destination hashes plus excluded-evidence custody.
- `ci/` and `.github/` — hygiene and regression gates.

See `engine/HOW-TO-RUN.md` for the operator flow. This repository contains product files only; internal walkthrough transcripts and build evidence remain in the org-private retention area named in `PROVENANCE.md`.

## Guided member setup

Each block below is self-contained: prerequisites, then the exact command to
run. Pick the block matching your platform; the setup interview itself is
identical everywhere after that point.

### macOS / Linux

Requires git and Python 3 (already present on most macOS and Linux installs).

```sh
git clone https://github.com/noogalabs/ascendops-pmagents.git
cd ascendops-pmagents
python3 setup.py
```

### Windows 10/11 (native)

Requires git for Windows and Python from python.org, installed natively (no
WSL/Linux subsystem needed).

1. Install git: https://git-scm.com/download/win (default options are fine).
2. Install Python 3.11 or newer from https://www.python.org/downloads/. On the
   first installer screen, check **"Add python.exe to PATH"** before clicking
   Install.
3. Install Claude Code: `npm install -g @anthropic-ai/claude-code` (requires
   Node.js from https://nodejs.org if `npm` is not recognized), then
   `claude auth login`.
4. Run:

```
git clone https://github.com/noogalabs/ascendops-pmagents.git
cd ascendops-pmagents
python setup.py
```

Note the last command is `python`, not `python3`. The stock python.org
installer for Windows registers `python.exe`, not a `python3` command.

**Crash-durability note (Windows only)**: if the computer loses power in the
narrow instant right after setup completes a step but before the next write,
POSIX systems (macOS/Linux/VPS) are guaranteed to recover cleanly on the next
run; on native Windows, that specific guarantee is weaker (the file content
itself is always safe either way, this is only about a rename landing durably
on disk before an actual power loss). This is a known, declared tradeoff, not
a bug, and does not affect normal use (it only matters for the rare case of
losing power mid-setup).

### VPS / headless server

Follow the macOS/Linux steps above exactly; a VPS is Linux underneath. The one
difference is authentication: with no browser on the server, run
`claude auth login` and follow the printed URL from another device to finish
sign-in.

### After cloning, for every platform

The setup interview offers the installed edition, asks where the clean template
and configured agent should live, and then walks the questionnaire in plain
language. Enter `unsure` to mark an answer for later confirmation; the generated
agent skips features that depend on it. If setup stops, run the same command and
choose the same answers file to resume. Existing configured agents are safely
reconfigured through the same flow rather than overwritten as new installs.

On success, setup prints the configured agent directory and the next review
step. On rejection, it shows the engine's exact row plus a plain-language fix;
unknown rows remain visible for support. See [the renderer census](docs/rejection-renderer.md).
