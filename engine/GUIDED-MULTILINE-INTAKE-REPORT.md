# Guided multiline intake fix-forward

PR19 closes the first-consumer failure exposed by Accounting B8: the guided
setup path previously accepted exactly one terminal input line, while mapping
rows may require multiple separately labeled lines from one answer.

The shared setup wrapper now collects every guided answer until a blank line,
preserves continuation lines in the questionnaire, and reads only the answer
line plus indented continuations when deciding whether a field is complete.
Single-line answers use the same protocol with an immediate blank terminator.
Correction prompts use the identical collector, so the retry path cannot
reintroduce the one-line limitation.

The production-grain casualty registers a synthetic B8-shaped consumer on the
real leasing mapping path, enters `Owner draw deadline day: 15` and
`Owner draw target day: 10` as separate lines, and proves both typed values
reach generated `config.json`. Existing maintenance and leasing guided paths
remain byte-equal to direct configuration with explicit single-line
terminators; the synthetic E-block and extra-cover consumers remain green.

No seat content changes in this PR. Accounting consumes the capability in its
rebased PR9 head after this shared fix-forward merges.
