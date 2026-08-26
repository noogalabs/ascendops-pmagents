# PR16 canonical question-ID surface

## Finding

Turnover is the first edition with an `E` question group. The shared production intake,
guided setup, rejection renderer, and promise-ledger sectioner each carried an `A`-through-`D`
regular expression. A content-only turnover registration could therefore never collect or
parse `E1` through `E8`, and its promise rows would be attributed to the preceding `D` subject.

## Fix

`engine/intake.py` now owns the canonical question-ID spelling: one uppercase letter followed
by one or more digits. Production intake, guided setup, rejection rendering, and the promise
sectioner all consume that surface. The parser accepts the broad spelling but fails closed when
an observed ID is not in the edition's declared `question_ids`; broad syntax does not broaden
edition authority.

## Casualties

- a declared `E1` parses through production intake while the same row rejects loudly when it
  is absent from the declared set;
- production `guided_answers` discovers, asks, and writes a synthetic edition's `E1` answer;
- the promise sectioner attributes an `E1` promise to `E1`, never the preceding subject;
- a git-tracked repo-wide custody sweep bans question-ID range regex definitions outside
  canonical intake, with explicit historical exceptions only for the byte-sealed maintenance
  configurator and its direct test helper;
- the existing maintenance, PM-assist, and leasing suites remain the regression bar.

The sealed maintenance configurator remains byte-identical.
