# PR13c review sweeps

## Scope

This change turns four review discoveries into registry-wide executable checks:

- mapping-driven declared values must have a runtime carrier or config-output landing;
- questionnaire promise candidates, using the declared wordlist, must have a reviewable
  gate, no-gate reason, or successor disposition in the edition review ledger;
- every claimed companion document must exist in the shipped edition library, with known
  false claims banned explicitly;
- every Bash fence in every shipped edition `ONBOARDING.md` must pass the real `bash -n`
  parser.

The ordering guard receives its missing casualty pair: prose operands reject and numeric
operands retain their comparison behavior. The shared engine production code is unchanged.

## Instance truth fixes

The maintenance questionnaire and filled fixture now name the six documents that actually
ship. The prior eight-document and board-spreadsheet claims are removed. PM-assist now says
plainly that no separate companion documents ship; its configured bootstrap library is the
complete shipped surface. Both answer-format and filled-fixture carriers are corrected.

Maintenance remains the sealed-core edition and is recorded as not mapping-driven in the
ledger. The declared-consumer sweep applies to mapping-driven editions; the companion,
promise, and Bash sweeps cover all three registered editions.

## Promise ledger boundary

The spelling boundary is explicit and reviewable: `must`, `blocker`, `never`, `each`,
`every`, `graduate`, `autonomous`, and `automatically`. Every candidate question or intro
section must appear in the ledger. Wrong-source consumption is not mechanically inferred;
that remains a contract-review responsibility. Successor dispositions are visible rather
than silent.

## CI custody

The workflow invokes `tests.test_review_sweeps` directly, and the manifest-custody suite
pins that invocation. Adding an edition test directory still requires no workflow edit;
the existing per-edition filesystem loop remains separate-process by construction.

## Mutation evidence

Each guard was independently armed before freeze and restored clean afterward:

- a prose ordering bypass killed the named numeric-ordering casualty;
- an unconsumed synthetic PM-assist placeholder killed the declared-consumer sweep;
- removing leasing D10 from the promise ledger killed the promise census;
- restoring a false PM-assist companion claim in the filled fixture killed the
  questionnaire-and-fixture truth sweep;
- removing an `if` from the leasing onboarding finalization block killed the
  registry-wide Bash parser sweep with the real `bash -n` syntax error.
