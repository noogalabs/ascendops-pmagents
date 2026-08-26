# Leasing edition validation report

Contract: `pmagents-five-seat-editions-contract-2026-08-25.md`.

## Edition census

- Questionnaire: 39 question IDs, A1-A14, B1-B9, C1-C6, D1-D10.
- Cover: four shared fields plus five leasing-only setup values.
- Declared artifact: `leasing-config.json`.
- Library source: fictional leasing coordinator template, 28 files.
- Shared-file touches: the leasing registry row in `engine/engine.py`, the leasing
  provenance rows, `PROVENANCE.md`, and the generated `MANIFEST.sha256` only.

## Five-law resweep

| Law | Result | Evidence |
|---|---|---|
| No private company/customer identity | PASS | member census test over every non-test edition file |
| No private people/contact data | PASS | same zero-hit census; Ridgeline identities are fictional |
| No credentials or secret material | PASS | Leak Guard plus the production-entry credential-scan casualties parameterized over `SUPPORTED`, including leasing at both scan timings |
| No internal evidence paths/codenames | PASS | member hygiene scan and product-relative provenance |
| No allowlist expansion to excuse a hit | PASS | no hygiene allowlist row changed |

`SOUL.md` and each shipped leasing skill preserve the same housing-decision boundary:
the agent prepares and routes work; a human decides approval, denial, rates, holds,
criminal-history assessment, legal notice, lease send/execution, and renewal offers.

## Cross-seat dispositions

- Deposit disposition deadline points to maintenance A3. Absent owner: held, never guessed.
- Move-out inspection ownership points to turnover D2 per turnover `SEAM-2`. Absent owner: held, never guessed.
- The communications-window pointer is absent until maintenance B8 is present; leasing C5 is explicitly rejected as a fallback by leasing table `X2`.
- The unrelated prose-valued notice `ORDERING` row is absent; neither leasing table `X2` nor turnover `SEAM-2` mandates it.
- The former escalation `POLICY_DIVERGE` row is absent. Leasing D10 combines
  channels and recipients, while maintenance D6 names channels only; comparing
  those differently shaped prose answers would manufacture contradictions.
- The former platform `FACT_MATCH` row is absent. The sealed maintenance payload
  exposes only raw `/answers/D1`, not a normalized platform field, while declared
  measures are validated but not applied by the current shared engine. Comparing
  the two prose answers would report a false contradiction. Shared measure
  application is therefore owned by the canonical-engine successor; the normalized
  leasing platform and escalation rows return only after that capability lands.

## Armed validation

The edition suite prints `ARMED` before each casualty and covers production configure,
create-then-reconfigure, declared filename, member census, the declared seam-check type,
and leasing zero-touch tree equality plus human question labels. The full engine,
maintenance frozen-baseline, setup, member-hygiene, manifest, and leak-guard suites are
run before packaging; exact command results belong in the frozen PR body.

The validation table was audited against tests that actually execute. Each claimed
edition behavior above is exercised through `engine.configure()` or the guided
`setup.run_setup()` production entry; no `ARMED` marker stands in for a mutation.

## Leasing and renewal content check

The leasing library carries renewals as leasing content, not as a separate seat.
`test_named_configured_output_carries_leasing_renewal_library` runs the production
configuration entry and pins the configured `Renewal and Rent-Increase Workflow.md`,
the renewal-offer section of `Leasing Message Template Library.md`, and the
`renewals-coordinator` skill by filename and distinctive content line.

## Declared configuration consumers

The mapping renders the canonical `leasing-coordinator` seat identity into every
`{{agent_name}}` carrier rather than substituting the organization slug. A2 and A3
render into both `IDENTITY.md` and the applicant-screening skill, so the configured
screening criteria live on operational surfaces outside setup prose. All five
leasing-only cover values land as typed integer keys in generated `config.json`:
prospect and application SLAs, approval threshold, renewal lead, and renewal response
window. `test_named_declared_leasing_configuration_reaches_runtime_consumers` drives
the production entry and pins all three wiring families.

## Compliance promise gates

Three questionnaire promises now reach value-bound instruction surfaces and typed
runtime configuration instead of remaining raw answers:

- A1 lands at `/screening_criteria_established`, in the applicant-screening hard
  gate, and in the onboarding pre-boot blocker. An A1=`No` production variant keeps
  screening, decision preparation, cron registration, and `.onboarded` behind STOP.
- D2 lands at `/screening_visibility_policy` and at the applicant-screening Inputs
  boundary. A summary-only configuration accepts only summary flags/pass-fail and
  refuses report contents, score narratives, and underlying screening records.
- B8 lands at `/pre_1978_properties` and in the lease-abstraction hard gate. Any
  configured pre-1978 property requires the lead-based-paint disclosure before a
  listing or lease packet can be marked complete.

`test_named_compliance_promises_reach_value_bound_runtime_gates` drives the normal
fixture plus A1-no and D2-summary-only variants through production configuration.
Removing each gate independently kills that named test.

## Boot configuration and renewal cadence

`AGENTS.md` reads the mapping-declared `leasing-config.json` as a first-class Session
Start input before applying any seat policy. The named bootstrap test derives that
filename through `cross_seat.structured_answers_filename()` from the mapping, so a
declared-name change cannot silently strand the instruction.

The same boot surface carries a value-bound **RENEWAL CADENCE STOP**. It names
`/renewal_offer_lead_days`, `/renewal_response_window_days`, and the configured B3
non-renewal notice floor, and stops renewal work when lead minus response is below
that floor. The fixture values are 60, 10, and 30; a production-configured variant
with lead 35 renders 35, 10, and 30 into the stop. Configure-time declarative
cross-field rejection is booked separately as `task_1787714841791_24557986` after
the shared PR13 capability work; the member seat does not invent engine machinery.

B3 now requires the first answer line to use the labeled form `Notice days: NN`.
The fixture begins `Notice days: 30`, and the named production test proves the
configured `non_renewal_notice_days` value is 30. A repository census finds exactly
zero live mapping declarations of `first_integer`: leasing B3 now consumes PR13a's
`labeled_integer` extractor with the exact `Notice days` label. The adversarial
round-7 phrase `Use 2 delivery methods at least 60 days before lease end` is rejected
loudly because it lacks the labeled line; it can never silently configure `2` as the
legal notice floor.

All five typed leasing cover values declare `minimum: 1`: prospect-response minutes,
application-decision hours, approval-threshold USD, renewal-offer lead days, and
renewal-response days. A named production-entry test derives the five rows from the
mapping and drives a zero-valued fixture variant for each through `configure()`. Each
rejects before the output tree exists, while the normal fixture remains the configured
positive-value regression.

## Supported member setup

The README names `python3 setup.py` as the supported member path and identifies
`leasing-config.json` as the generated source of truth. The former four-placeholder
manual instructions were incapable of satisfying the final completeness sweep and
are removed. The shared engine CLI is deliberately not advertised until PR13a fixes
its empty-seat-registry default.

## Companion-document truth

The questionnaire and filled fixture now name only the two companion documents the
edition actually ships: `Leasing Message Template Library.md` and
`Renewal and Rent-Increase Workflow.md`. The introductory and next-step prose was
narrowed at the same time so no board, process, or judgment-guide artifact is implied.
Whether to ship the eight absent documents—including the two inspection checklists—is held as the contract decision
`task_1787718258364_71764421`; no sanitization or authoring begins without a GO. If
approved, the work requires its own owner-source hygiene bar. The
companion-claim test pins both current carriers and asserts all six absent names stay
absent until that successor deliberately ships them.

## Onboarding failure-path custody

The completion chain registers the heartbeat cron only after the durable `.onboarded`
marker. A kill or power loss before the marker therefore leaves no state-writing cron;
a termination after the marker but before heartbeat registration is benign and a rerun
recreates the cron set idempotently. Pre-marker failures remove the five role crons and
the marker, while post-marker heartbeat failure preserves the marker and loudly asks for
a rerun. `test_named_onboarding_failure_cannot_leave_heartbeat_live` pins marker-before-
heartbeat ordering and both failure scopes. A Bash execution harness for an instruction file is
outside this content-only edition boundary; textual ordering plus the documented
retro-write invariant is the enforcement grain for member prose.

## Promise truth at questionnaire boundaries

B9 now asks the operator to record the approved inspection process and checklist
location without claiming this edition ships either inspection checklist. The two
checklists join the six companion artifacts in the owner-authorization decision lane.
The post-shadow text now states the shipped permanent copilot posture: a human approves
every external message, and any future message-class change requires an explicit policy
and runtime change. The first week is likewise described as operator-supervised review,
with no automated calibration digest or automatic shadow exit. The named test bans all
former automation and graduation promises.

The onboarding name-marker step is unconditional: it writes `$CTX_AGENT_NAME` as the
default display value and substitutes a different human-facing value only when requested.
Keeping the canonical display name therefore cannot strand the marker that the final
completeness sweep rejects.

The round-9 A2/A3 unresolved-threshold row is owned by PR13a
(`task_1787719172740_06204033`), whose generalized executable-
value gate rather than duplicated here. Its explicit casualty list now includes unresolved
`income_multiplier` and `credit_min_score`, alongside string-gate and integer variants;
every mapping-consumed sentinel must reject configuration with the field and resolution path.

## Embedded Bash parser custody

The finalization command chain is a real nested `if` and parses before any textual
ordering property is asserted. `test_named_every_onboarding_bash_block_parses`
enumerates all five indentation-aware `bash` fences in `ONBOARDING.md` and runs each
through the real `bash -n` parser. Removing the opening `if` kills that named test on
the finalization block. PR13c generalizes the same parser-first casualty across every
shipped edition onboarding file.

## CI edition-suite census

At the pre-fix head, three edition test suites existed—maintenance, PM-assist, and
leasing—but the workflow hardcoded maintenance alone. PM-assist and leasing were not
CI subjects; earlier green jobs therefore did not certify their named casualties.
Local independent peer runs remain valid evidence, but the merged PM-assist bar had a
hollow CI leg and is recorded honestly here.

The workflow now derives `editions/*/tests` from the filesystem and invokes each suite
in a separate Python process, avoiding the duplicate `test_configurator` module-name
collision. It also executes `tests.test_manifest_generation`, whose custody test pins
the glob, the separate-process command, the absence of hardcoded edition paths, and
the current three-directory census. A future edition test directory enters CI without
another workflow edit.

The engine CLI omission of an explicit empty seat registry is a real pre-existing
shared-runtime defect that already affects the merged PM-assist edition. It is not
caused or repaired by this content-only PR. PR13 owns the one-line CLI default and
real-entry casualties for both a cross-seat mapping and the maintenance default.

## Import sanitation successor

The frozen-head audit at `deab6c4` found two source-attribution lines naming an
internal operator. Both now use the maintenance-precedent `owner-reviewed`
attribution. A fresh recursive audit of the full leasing import surface—edition,
mapping table, and canonical Ridgeline fixture—finds zero internal operator names,
zero internal codenames, and zero banned sales tokens. No allowlist row was added.
