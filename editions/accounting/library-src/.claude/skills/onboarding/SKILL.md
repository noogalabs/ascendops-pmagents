---
name: onboarding
description: "This agent has not been onboarded yet, or the user asked to run onboarding. Run the bookkeeping seat setup interview: the shared 4-field cover sheet plus the 46-question Bookkeeping Agent Setup Questionnaire (Group A state rules, Group B company thresholds, Group C roles and people, Group D platform, banking, and wiring). Write every answer into accounting-config.json with its question id, start the agent in shadow mode, and create the .onboarded marker only at the end."
triggers: ["onboarding", "run onboarding", "/onboarding", "first boot", "not onboarded", "setup", "set me up", "configure the agent", "questionnaire", "bookkeeping questionnaire", "resume onboarding", "finish setup"]
---

# Onboarding

The full script lives in `ONBOARDING.md` at the agent root. Read it and follow it top to bottom.

## Before you start

```bash
[[ -f "${CTX_ROOT}/state/${CTX_AGENT_NAME}/.onboarded" ]] && echo "ONBOARDED" || echo "NEEDS_ONBOARDING"
```

If the marker exists, do not re-run the interview unless the user explicitly asks for it. If they do, resume from the first unanswered value rather than re-asking everything.

## What onboarding actually produces

| Artifact | What lands in it |
|---|---|
| `accounting-config.json` | Every threshold, state marker, clock, and named role, each carrying its question id |
| `SYSTEM.md` | Platform, account inventory (no account numbers), read paths, board and log locations, jurisdictions |
| `USER.md` | Who the user is, how they want to be reached, what counts as urgent to them |
| `SOUL.md` → `## Custom Rules` | Anything standing the customer asked for |
| `config.json` | Timezone, day-mode hours, crons |
| `.onboarded` marker | Created last, and only last |

## The three rules that matter most

1. **An unanswered value is not a defaulted value.** It stays as its placeholder, its dependent check is DISABLED, and it goes in `unanswered[]`. A confidently wrong deposit deadline is worse than a missing one.
2. **A Group A answer that has not been through counsel is written `"confirmed": false`.** The agent flags on unconfirmed legal values; it never acts on them. "Confirm with counsel" is a legitimate answer to leave in place.
3. **Shadow mode is on when onboarding ends.** Checks run silently, a calibration digest goes to the human bookkeeper, nothing goes outbound. Only the property manager ends shadow mode, and only after two consecutive weeks of digests matching reality.

## Phase-zero flags

Some answers are not configuration, they are findings. Raise each one plainly, create a `[HUMAN]` task, and say which checks stay dark until it clears:

- No separate security-deposit trust account in a state that requires one (D3 vs A7)
- No suspense or clearing account (D5) — there is nowhere legitimate to park an unidentified payment
- No tracking board and no PM decision log (D6)
- No 1099 tracker (D9)
- No named backup decision-maker (C4) — a statutory deadline with nobody available to decide it is a company structure problem

## If the customer already filled in the questionnaire

Read their answers, transcribe them into `accounting-config.json` with question ids intact, and use the interview only for gaps and for the four cover-sheet fields. Do not re-ask what they already answered.
