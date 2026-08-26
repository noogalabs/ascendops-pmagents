# PR23 five-seat wiring report

All five production editions already conform to the registered mapping-driven
setup shape. This change therefore adds no edition content and changes no
mapping row. It closes the shared setup gap that previously passed an empty
seat registry on every member-run configuration.

Setup now discovers completed sibling installations beside the requested
output. A sibling enters the registry only when both `config.json` and its
mapping-declared structured-answer artifact exist, the artifact names the
registered seat, and the existing cross-seat version gate accepts it. Newer or
malformed completed peers are excluded with a visible reason. Incomplete peers
remain ordinary partial installs. Discovery reads sibling artifacts but never
writes their trees.

Two complete sibling directories claiming the same seat reject setup before
configuration and name both paths. There is deliberately no lexical, timestamp,
or first-found precedence: only the operator can resolve which installed peer
identity is current without risking stale cross-seat values.

Guided answers and completed-file answers converge before the registry is
constructed, so both member entry paths consume one shared discovery function
and one construction site. Completion output reports the doctrine state at its
currently shipped grain: each pointer is either `resolved` from an owner seat
or `held` pending an owner seat. The config-row resolution vocabulary remains
reserved for the PR13b-ii consumer shard.

Two receiver-side contract checks refined the original review spec before any
code was written. No shipped mapping currently contains a pointer-backed config
row, and resolved pointer records do not currently persist the peer value
digest that held records persist. PR23 therefore pins `state`, `owner_seat`,
and `owner_question_id` on resolution without inventing a new engine field.
Successor task `task_1787778610923_27846941` owns the symmetric resolved-value
digest at engine grain.

The named casualties cover a live turnover-to-accounting resolution, reverse
installation order followed by a dependent-seat rerun, an absent owner that
stays visibly held, a newer peer excluded loudly, an incomplete sibling that
never enters the registry, peer-tree byte stability, and an AST census proving
the registry has one construction site for both answer modes.
The duplicate-identity casualty additionally proves the ambiguous install stops
with zero dependent-seat output.

The David-locked Gap Rule passes at the content-origin leg. This is structural
discovery and reporting plumbing only: it introduces no property-management
numbers, thresholds, scripts, workflows, or judgment calls. Renewals remain
input-gated, business-development day mode remains PR18-gated, and all deferred
cross-seat mapping seams remain in PR13b-ii.

This freeze is held for the nighttime double-green review. Merge remains held
until the recorded morning GO before Jordan and Albie pull the member setup.
