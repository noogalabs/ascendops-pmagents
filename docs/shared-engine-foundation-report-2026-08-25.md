# Shared mapping-engine foundation report

Base: `ee28dceca93d5c6ee87f9086de098c1081cf6a98` (`origin/main`).

## Fan divergence census

PR5 through PR9 each independently changed `engine/engine.py`, `engine/intake.py`,
and `setup.py`. The five heads carried four incompatible registry/validation
signatures and multiple mapping runners. The canonical blend is:

- PR5's mapping materialization flow;
- PR7's explicit runner/structural-intake registry contract;
- PR9's registry-derived `SEAT_LABELS` setup list;
- no PR8 `generic_configurator.py` fork.

Edition PRs must rebase and retain only edition content, mapping data, one
registry row, provenance, and their edition tests/reports. Engine machinery is
owned here once.

## Credential boundary

`engine/credential_scan.py` is the shared scanner. `configure()` invokes it at
both production timings for every runner:

1. after the safe source copy and before placeholder/template rendering;
2. after all structured, seam, and stamp writes and before atomic replacement.

The maintenance sealed core remains byte-identical at
`0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551`
and retains its internal scans. The wrapper-level calls make the same boundary
explicit for sealed and mapping paths without modifying the sealed file.

## Armed casualties

- `ARMED: every mapping registry seat rejects an AKIA answer with zero output`
  parameterizes over every `SUPPORTED` mapping runner and is guarded against an
  empty population. It proves both a pre-template source secret and a
  post-template answer secret reject through production `configure()` with no
  destination.
- `ARMED: sealed production entry retains AKIA rejection with zero output`
  proves the sealed path remains fail-closed.
- Disabling both shared scan calls kills the mapping casualty by name while the
  sealed twin remains green, proving the twin is independent rather than a
  duplicate assertion.

## Manifest custody

`ci/generate-manifest.py` derives `MANIFEST.sha256` exclusively from
`git ls-files`. `tests/test_manifest_generation.py` plants an untracked
`__pycache__/planted.pyc` and proves it can never enter the manifest. Generation
fails if any tracked input is missing; `--check` compares the tracked census to
the committed manifest.

## Validation

- Engine: 77/77.
- Repository tests: 26/26.
- Tracked manifest check: green.
- Sealed core SHA-256: unchanged.
- `git diff --check`: clean.
