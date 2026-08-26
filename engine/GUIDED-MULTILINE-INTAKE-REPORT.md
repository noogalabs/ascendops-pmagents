# Guided multiline intake fix-forward

PR19 closes the first-consumer failure exposed by Accounting B8: the guided
setup path previously accepted exactly one terminal input line, while mapping
rows may require multiple separately labeled lines from one answer.

The shared setup wrapper now collects every guided answer until a blank line,
preserves continuation lines in the questionnaire, and reads only the answer
line plus indented continuations when deciding whether a field is complete.
Replacement is bounded to that same answer span, so the next section heading
and final questionnaire guidance remain byte-present.
Cover fields use the same indented-continuation representation and the shared
intake parser preserves those continuations instead of silently truncating them.
The read and write consumers now share `indented_value`, `CONTINUATION_LINE`,
and `INTAKE_VALUE_SPAN` from `engine.intake`; `setup.py` no longer carries a
private single-line or continuation grammar. Dane requested the class census
before PR19 merged, but the request arrived through the delayed queue after the
merge; PR21 therefore closes that review debt on the same intake boundary. Its
named AST census discovers the answer and cover collection sites in `setup.py`
and `engine/intake.py`, accepts shared multiline readers, writers, and guided
collectors, and carries reasoned exemptions only for cover-label and
question-heading framing. A future intake consumer that forks the value grammar
therefore fails the census instead of waiting for another instance report.
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
