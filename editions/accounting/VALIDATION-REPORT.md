# Accounting edition validation report

Contract: `pmagents-five-seat-editions-contract-2026-08-25.md`.

## Edition and custody census

- Questionnaire: 46 IDs, A1-A17, B1-B13, C1-C7, D1-D9.
- Structured artifact: `accounting-config.json`, declared by the mapping.
- Member library: the owner-reviewed 28-file classroom accounting package plus
  the reviewed byte-identical PM-assist approval workflow required by the
  classroom rent-posting skill.
- Fixture: fictional Ridgeline Residential Management.
- Mapping authority: `mapping-tables/accounting.md`, source SHA-256 pinned in
  `engine/mappings/accounting.json`.

Artifacts 167-194 in `provenance/source-files.tsv` form the complete classroom
file census. Every row carries source and destination SHA-256. The four changed
destinations are narrowly authorized platform-conformance adaptations:
placeholder spelling, session-start structured-config custody, guided-only
setup, and verify-not-reenter first boot. The mapping-owned `seat-config.json`
baseline and edition tests are product-native, not falsely attributed to the
classroom source. The larger in-fan draft is not shipped.
Artifact 195 records the separately reviewed, byte-identical approval workflow
import. It closes the classroom rent-posting skill's dangling money-gate
reference without inventing a new approval procedure.

The QAd mapping table targeted that draft tree. Its semantic question-to-value
rows survive; destination anchors were retargeted to the classroom package.
Production configuration, the declared-consumer sweep, and the named runtime
retarget casualty prove those values reach the actual shipped tree.

The nine shipped skills are dispositioned exhaustively: `ap-vendor-payments`,
`approvals`,
`ar-rent-posting`, `owner-draws`, `owner-statement-drafting`,
`security-deposit-accounting`, `trust-compliance`, and `trust-reconciliation`
remain byte-identical to classroom custody; `onboarding` is the one adapted
skill. Its platform delta is verify-not-reenter, private Telegram deployment
wiring, and completion only through `ONBOARDING.md`'s final gate. It contains no
second identity, company, goals, policy, or software interview.
The deployment-only step collects and validates the complete private Telegram
wiring triple: `BOT_TOKEN`, `CHAT_ID`, and `ALLOWED_USER`.

## Cross-seat row dispositions

The table below is exhaustive for SEAM-20 through SEAM-32. `Expressible now`
means the current engine can represent the row without guessing. Prose
comparison and holderless-pointer rows stay absent with an explicit return
vehicle rather than shipping a confident wrong result.

| Seam | Table authority | Shipped disposition |
|---|---|---|
| SEAM-20 | Turnover C7 owns the deposit chargeback fact; accounting B13 is the real local holder | Pointer lands now with owner `turnover-coordinator/C7`, holder B13. AF-2's draft POLICY typing is rejected. The prose two-number equality check is absent and returns after PR13b measure support. |
| SEAM-21 | Accounting B5/B6 own the decomposed trust-variance rule | No local pointer needed; accounting remains the single owner. PM-assist consumer migration is a follow-up, never a second local copy. |
| SEAM-22 | Accounting C3 owns the day-to-day financial-board worker identity | No local pointer needed; accounting remains the single owner. |
| SEAM-23 | Accounting C2 owns principal-broker identity; channels remain per-seat policy | No local pointer needed; the accounting identity remains authoritative. |
| SEAM-24 | PM-assist A4 owns eviction attorney inventory; accounting C5 is the real local holder | Pointer lands now with owner `pm-assist/A4`, holder C5. |
| SEAM-25 | Maintenance A7 owns licensed trades; accounting A15 owns its dollar threshold | Pointer lands now for the trades list with owner `maintenance-coordinator/A7`, holder A15. The accounting threshold remains local. |
| SEAM-26 | Accounting B3 owns the owner reserve floor | No local pointer needed; turnover C1 is explicitly not the same subject. |
| SEAM-27 | Accounting B10 statement release precedes PM-assist D6 report-pack day | Raw prose ORDERING is absent. It returns only through typed/labeled numeric paths after the shared comparison vehicle exists and the contract still mandates it. |
| SEAM-28 | Accounting A17 owns the jurisdiction inventory; per-seat statute values stay local | No local pointer needed; accounting remains the single owner. |
| SEAM-29 | PM-assist D7 owns decision-log location; accounting D6 is the real local holder | Pointer lands now with owner `pm-assist/D7`, holder D6. The bookkeeping-board location stays accounting-owned. |
| SEAM-30 | Retention facts are disjoint by record class | No equality row: prose disjointness is not expressible safely at current grain. The report records the classes instead of collapsing them. |
| SEAM-31 | Accounting owns the decomposed late-rent and eviction clocks | No local pointer needed. Existing sibling rows must point here only in a reviewed consuming follow-up; no second owner is minted in this PR. |
| SEAM-32 | Accounting owns the decomposed security-deposit holding rules | No local pointer needed. Existing sibling consumers migrate only through reviewed pointer rows. |

The live bot re-raised AF-2 at the current consumer grain: a differing local B13
and owner C7 cannot yet be compared safely. This is successor-grade, not a
second PR9 mapping defect: pointer ownership is correct, but C7 is two-number
prose and the current engine has neither pointer-grain extraction nor measured
comparison for it. Task `task_1787735414502_98348643` owns the shared PR13b
capability and a consuming follow-up that returns this chargeback equality with
the leasing communications-window and BD day-mode rows. Its casualty must prove
151/401 rejects against owner 150/400; PR9 never guesses by raw prose equality.

The exact-head bot also identified a second owner/value split at SEAM-1.
Until PR13b can extract typed values at pointer grain, the local
`/deposit_return_days` row remains sourced from the pointer's declared holding
question A6. A structural casualty pins that equality so the local config and
held pointer cannot silently drift to different accounting answers. Task
`task_1787735414502_98348643` gains the consuming follow-up: maintenance A3
must become the typed runtime authority when present, with absent-peer and
divergent 31-vs-30 casualties. PR9 does not fabricate a prose-to-integer pointer
conversion the current engine cannot express.

The existing POLICY_DIVERGE rows SEAM-8, SEAM-11, SEAM-12, and SEAM-17
remain report-only comparisons and never auto-unify prose. SEAM-1 remains at
the table's current migration-ready ownership: maintenance A3 owns the deadline
today and accounting A6 holds it; leasing B1 owns the clock trigger. This avoids
two owner seats for one deposit fact.

AF-3 is closed by deletion, not a default: the false `08:00`/`17:00` day-mode
literals and their config keys do not ship. As with the leasing X2 and BD
day-mode dispositions, no holderless row is fabricated; holderless pointer state
and pointer-grain window extraction return through PR13b.

Twenty runtime accounting numbers land as typed integer config keys with a
strict minimum of 1. Semantically ambiguous prose is never parsed with
`first_integer`: multi-number answers lead with exact labeled lines and use
`labeled_integer`, while unambiguous money answers use `currency`. Percentage,
fractional-month, multi-date, and explicit-none answers remain in the structured
artifact rather than being coerced into a dishonest integer domain.

## Inherited platform laws

- `AGENTS.md` gates session start on `.onboarded` and reads the declared
  structured config before work.
- README routes only through repository `setup.py`; manual placeholder setup is
  banned.
- First boot verifies configured values, collects deployment credentials only,
  and uses the canonical role-crons -> durable marker -> heartbeat transaction.
- The executable final gate refuses both cron registration and `.onboarded`
  while any rendered placeholder or identity marker remains.
- Every embedded onboarding Bash fence passes `bash -n`.
- Companion claims match the shipped tree and promise-ledger rows are
  hash-anchored.
- The maintenance sealed core SHA-256 remains
  `0540ea08aa8d47ecb1aebbb7f51db85c5a67ab252172804e9ba24e56c2403551`.

## Armed validation

- Real classroom-tree production configure and stable rerun.
- Content-divergent maintenance fixture rejected before writes.
- Original accounting AKIA blast shape rejected before either config or
  onboarding output exists.
- Destination-retarget proof: configured semantic answers are present in the
  declared structured artifact, the boot read names it, and every classroom
  placeholder is consumed.
- Exact cross-seat pointer/check/gate sets and AF-2/AF-3 dispositions.
- Exact typed-config key set, fixture-to-config values, zero rejection for a
  labeled timeline and a money threshold, and unresolved B1 rejection before
  any output write.
- Provenance source/destination hashes recomputed for every classroom file.
- Accounting 23/23, engine 92/92, sibling editions 26/5/20/13, zero-touch
  28/28, review sweeps 6/6, plus manifest, hygiene, leak, and exact-head CI.

## Shared-file boundary

Shared touches are the accounting registry constant/row, setup label, root
edition/provenance documentation, mapping, review ledger, manifest census, and
manifest hashes. Shared production mechanics remain owned by foundation PRs;
the sealed maintenance core is byte-identical.
