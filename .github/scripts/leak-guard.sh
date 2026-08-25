#!/usr/bin/env bash
#
# leak-guard.sh — server-side operational-leak scanner for the PUBLIC repo.
#
# Catches the class of leak where internal fleet operational detail (agent
# roster + cron schedules, operator home paths, real org content, secrets) gets
# committed to the public framework repo. This is the server-side backstop that
# a local pre-push hook cannot provide: it runs in CI on every pull_request and
# push to main, so it covers fork PRs and GitHub UI-merges too.
#
# SECURITY (F1): on pull_request events the WORKFLOW executes the copy of this
# script from the PROTECTED BASE BRANCH, never the PR's own copy — a PR that
# edits this file cannot weaken its own enforcement run. Changes to this file
# and the workflow also require CODEOWNERS review.
#
# DESIGN: block on the LEAK SHAPE, not on framework convention. The framework
# legitimately uses agent names (boris/paul/...) as doc placeholders and `lifeos`
# as a test-fixture org name in hundreds of lines — those are NOT leaks and must
# NOT trip this guard. We match only high-signal shapes that never appear in
# legitimate framework code.
#
# Usage:
#   leak-guard.sh <file>...        scan the given files
#   leak-guard.sh --tree [ref]     scan every tracked file at ref (default HEAD)
# Exit 0 = clean, exit 1 = leak(s) found, exit 2 = requested scan subject
# could not be evaluated (details on stderr).

set -uo pipefail

fail=0
report() { printf '::error file=%s::LEAK-GUARD: %s\n' "$1" "$2" >&2; printf '  %s: %s\n' "$1" "$2" >&2; fail=1; }
GUARD_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
PRIVATE_FIRST_NAME_BASELINE="$GUARD_DIR/leak-guard-bare-first-name-baseline.tsv"

# ---- Patterns (each is high-signal for a real leak, low false-positive) ----

# 1. Operator home paths — the real operator's machine paths never belong in
#    the public framework. Match the KNOWN operator identities specifically so
#    generic example paths (/Users/foo, /home/victim, /Users/.../) do not FP.
#    BOTH historical operator usernames are covered (F5); known synthetic test
#    fixtures are exempted by EXACT line below, never by weakening this set.
#    The name must be followed by a non-name character or end-of-line (F6), so
#    a bare `/Users/davidhunter` at EOL or before a quote/space/paren is caught;
#    a following name-character means a different user (e.g. /Users/davidhunter2).
OPERATOR_USERS='davidhunter|cortextos'
HOME_PATH_RE="(/Users|/home)/(${OPERATOR_USERS})([^A-Za-z0-9_-]|\$)"

# Exact-line allowlist for the operator-path check: known SYNTHETIC fixtures
# that intentionally carry an operator-shaped path. Both the file path AND the
# full line must match EXACTLY — any edit to these lines re-triggers the guard.
allowlisted_line() {
  case "$1" in
    tests/sprint7-environment.test.ts)
      case "$2" in
        "      const liveAgentDir = '/Users/cortextos/cortextos/orgs/testorg/agents/cortext-designer';") return 0 ;;
        "        projectRoot: '/Users/cortextos/cortextos',") return 0 ;;
      esac ;;
    tests/unit/cli/send-telegram-normalize.test.ts)
      case "$2" in
        "    // Verbatim shape from /Users/cortextos/.cortextos/default/logs/codex-research/") return 0 ;;
      esac ;;
  esac
  return 1
}

# 2. Fleet-roster + cron-schedule TABLE shape — the phase-report leak. A line
#    naming an agent alongside a cron schedule expression. Framework SOURCE and
#    TEST fixtures legitimately build agent+cron structures, so this check is
#    scoped to non-test files only (see scan_file) — the leak was in docs/.
#    Matched case-insensitively (F5): `| Dane |` is the same leak as `| dane |`.
#    NOTE: `.*` (grep is line-oriented, so this cannot cross lines) — the previous
#    `[^\n]*` was an ERE bracket of literal `\` and `n`, so any leak line with an
#    `n` between the agent name and the cron keyword silently PASSED.
ROSTER_NAMES_RE='boris|paul|sentinel|donna|nick|dane|blue|collie|codie|aussie|lacey|cash'
# Roster names must match as STANDALONE WORDS: [A-Za-z0-9_-] are word
# characters, so `Blueprint`, `mundane`, `cashier`, `nickname`, `blue-green`
# are compounds, never roster hits. awk/grep ERE have no \b; the explicit
# classes are mawk/BSD-awk/grep -E portable. The name needs a non-word char
# AFTER it too — the cadence keyword follows via `.*`, so requiring one
# non-word char cannot miss a real `| dane | ... heartbeat(` row.
# The three BARE-NAME cadence markers below double as directory names: our
# skills live at agents/<roster-name>/.claude/skills/<marker>/SKILL.md, so ANY
# doc citing a skill file path carried a roster name and a marker on one line
# and was reported as a roster+schedule table. That is a path reference, not an
# ops table. They are therefore required NOT to be preceded by `/` (note the
# `/` added to the negated class), which is what distinguishes a path segment
# from a table cell.
#
# This NARROWS a false-positive surface; it does not widen what is allowed.
# The markers that cannot appear as a path segment — the parenthesized cadences
# and the bare five-field cron expression — keep matching anywhere on the line,
# so a real schedule sitting next to a path reference is still caught.
ROSTER_MARKERS_RE='morning-review|evening-review|human-task-sweep'
# The exemption requires a marker to be a GENUINE PATH SEGMENT: preceded by `/`
# AND followed by `/`. An earlier draft exempted anything merely slash-PREFIXED,
# which let an ops table launder a roster row by writing the cadence cell as
# `| dane | cadence | /morning-review |` — a leading slash, no trailing one, and
# not a path at all. So the rule still fires when the marker is preceded by a
# non-slash (a table cell) OR followed by a non-slash / end of line (a slash-
# prefixed token that is not a path segment). Only `/marker/` is exempt.
# NATURAL-LANGUAGE CADENCE. This is a WIDENING, and the only one here.
#
# The rule previously had NO natural-language schedule detection at all. A row
# reading `| dane | primary | daily at 9am |` was never caught, in any form. The
# gap surfaced when a reviewer showed a line the old pattern caught and the new
# one did not — and the reason the OLD pattern caught it was incidental: the
# line cited a skill path, so a marker token happened to appear. Detection by
# coincidence is not coverage, and once the path exemption above is correct that
# coincidence is gone, so the real hole has to be closed on purpose.
#
# Deliberately conservative: a frequency word AND a CLOCK TIME, on one line, no
# pipe between them (so it stays inside a single table cell or clause). Prose
# like "we review this daily" carries no time and does not match.
#
# CLOCK TIME IS NOT "at <digit>". An earlier draft used `at [0-9]`, which reads
# ordinary quantity and rate prose as a schedule:
#   "dane reviews daily occupancy at 9 properties."
#   "dane bills hourly labor at 125 dollars per visit."
# Those are sentences people write, not punctuation attacks, and the corpus was
# blind to them precisely because our written history happens not to contain
# that combination. A corpus bounds the false-positive cost against the PAST.
#
# So a clock time must carry actual clock evidence: an am/pm suffix, or an
# HH:MM minute component. A bare integer after "at" is a quantity, not a time.
#
# AND IT MUST BE A COMPLETE TOKEN, NOT A PREFIX. Requiring clock evidence was
# still not enough, because an unbounded pattern matches the START of a longer
# word or number:
#   "hourly electrical load at 9 amperes."   -> `9 am` is a prefix of `9 amperes`
#   "weekly batches at 09:171 records."      -> `09:17` is a prefix of `09:171`
#   "nightly output at 99:99 records."       -> unconstrained two-digit form
# The first is ordinary property-maintenance prose. So the hours and minutes are
# range-constrained to real clock values, and a trailing non-alphanumeric
# boundary (or end of line) is required, which is what stops prefix matching.
#
# Negative corpus BEFORE adoption, per the standing no-regex-without-a-corpus
# rule: run across all 2602 tracked files, this fires on 2, and both were opened
# and confirmed to be genuine roster+schedule content the guard was missing.
# Zero false positives. Both were sanitized rather than exempted.
# ---- RECURRENCE, stated as a finite class rather than a vocabulary list ----
#
# The previous version was `daily|nightly|weekly|hourly|weekdays?|every ...` — an
# examples list that stopped when the examples in hand passed. It missed six
# ordinary forms (`monthly`, `weekends`, `every Monday`, `each morning`,
# `every 4 hours`, `Mon-Fri`) that a reviewer produced in one message.
#
# The class: a RECURRENCE EXPRESSION is exactly one of four structures.
#
#   1. INTERVAL ADVERB      a single word naming a period: hourly ... annually
#   2. QUANTIFIED PERIOD    (every|each) + optional COUNT + a UNIT or a DAY
#   3. DAY-OF-WEEK RANGE    weekdays / weekends, or a DAY-to-DAY range
#   4. DAY SET              a plural weekday, or two+ DAYs joined by , / or "and"
#
# and three closed vocabularies it is built from:
#
#   UNIT   a period noun (hour, day, night, morning, ..., quarter, year)
#   DAY    a weekday name or its standard abbreviation
#   COUNT  a quantifier: a numeral, a number word one..twelve, or "other"
#
# A BARE SINGLE DAY IS DELIBERATELY NOT A RECURRENCE. `Monday at 9am` is as
# likely to be one meeting as a schedule, so a day counts only when quantified
# (`every Monday`), ranged (`Mon-Fri`), pluralised (`Mondays`), or listed
# (`Mon, Wed, Fri`). That is the one judgement call in the class, and it is made
# for false-positive reasons, not from an example.
#
# STRUCTURE 4 WAS MISSING FROM THE FIRST STATEMENT of this class, found in review:
# `Mondays at 9am`, `Mon, Wed, Fri at 9am` and `Monday and Friday at 9am` are all
# unambiguously recurring while being neither quantified nor a range. Recorded
# because it is the point of writing a class down — a missing STRUCTURE is a
# restatement, which is what this is, and not another alternation bolted onto the
# end, which is what the previous vocabulary list kept receiving.
#
# Explicitly SUPPORTED via COUNT, decided rather than left to accident:
#   `every other week`, `every two weeks` (number words), `every 4 hours`
# Explicitly supported already via structure 1: `twice daily` (matches `daily`).
#
# Structures 1-4 are exhaustive over "how English says a thing recurs" as far as
# I can state it. If a form shows up that is none of these, the class is wrong
# and needs restating — NOT another alternation bolted onto the end.
ROSTER_NL_UNIT_RE='(weekdays?|weekends?|hours?|days?|nights?|mornings?|afternoons?|evenings?|weeks?|months?|quarters?|years?)'
ROSTER_NL_DAY_RE='(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tues|tue|weds|wed|thurs|thur|thu|fri|sat|sun)'
ROSTER_NL_INTERVAL_RE='(hourly|daily|nightly|weekly|biweekly|fortnightly|semimonthly|monthly|quarterly|yearly|annually)'
ROSTER_NL_COUNT_RE='([0-9]+|other|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)'
ROSTER_NL_DAYFULL_RE='(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
# Structure 4. A plural weekday, or two+ DAYs joined by comma, slash or "and".
# Only FULL day names are pluralised: `suns`/`mons` are noise, not schedules.
ROSTER_NL_DAYSET_RE="${ROSTER_NL_DAYFULL_RE}s|${ROSTER_NL_DAY_RE} *[,/] *${ROSTER_NL_DAY_RE}|${ROSTER_NL_DAY_RE} +and +${ROSTER_NL_DAY_RE}"
ROSTER_NL_FREQ_RE="(^|[^a-z0-9-])(${ROSTER_NL_INTERVAL_RE}|(every|each) +(${ROSTER_NL_COUNT_RE} +)?(${ROSTER_NL_UNIT_RE}|${ROSTER_NL_DAY_RE})|weekdays?|weekends?|${ROSTER_NL_DAY_RE} *[-] *${ROSTER_NL_DAY_RE}|${ROSTER_NL_DAYSET_RE})[^a-z0-9-]"
# The 12-hour hour allows an optional leading zero: `daily at 09am` is a plausible
# way to write a schedule, and without the `0?` it was a BYPASS rather than a
# false positive. Found by probing the edges of the clock class rather than the
# examples in hand, after three consecutive bounds that each fit the examples in
# front of me and were short everywhere else.
ROSTER_NL_CLOCK_RE='((0?[1-9]|1[0-2])[ ]?(am|pm)|([01]?[0-9]|2[0-3]):[0-5][0-9]([ ]?(am|pm))?)([^A-Za-z0-9]|$)'
ROSTER_NL_CADENCE_RE="${ROSTER_NL_FREQ_RE}[^|]*at ${ROSTER_NL_CLOCK_RE}"
ROSTER_CADENCE_RE="heartbeat\\([0-9]|pr-monitor\\([0-9]|\\([0-9]+ [0-9*]+ \\* \\* |[^A-Za-z0-9_/-](${ROSTER_MARKERS_RE})|(${ROSTER_MARKERS_RE})([^/]|\$)|${ROSTER_NL_CADENCE_RE}"
# ORDER-INDEPENDENT. The thing being detected is a same-line ASSOCIATION between
# a roster name and a cadence; a table does not become safe because Schedule is
# the first column. The rule was forward-only (roster then `.*` then cadence), so
# every one of these passed clean:
#
#   | daily at 9am | dane |
#   | Schedule | daily at 9am | Agent | dane |
#   | morning-review | dane |
#
# The machine-cron forms were rescued by the windowed awk branch below, which is
# already order-independent — which is exactly why the gap was invisible: the
# shapes most likely to be probed were covered by a different branch.
#
# Both directions are therefore matched, for EVERY cadence form rather than only
# the natural-language one that was reported. The reverse arm was found to affect
# bare markers too, and fixing only the reported instance would have left the
# same bypass open one column over.
ROSTER_NAME_BOUNDED_RE="(^|[^A-Za-z0-9_-])(${ROSTER_NAMES_RE})[^A-Za-z0-9_-]"
ROSTER_CRON_RE="${ROSTER_NAME_BOUNDED_RE}.*(${ROSTER_CADENCE_RE})|(${ROSTER_CADENCE_RE}).*${ROSTER_NAME_BOUNDED_RE}"

# Agent work queues legitimately name an owner and one of that owner's skills
# as a compact `agent/skill` reference (for example `dane/evening-review`). The
# roster/cadence co-occurrence rule used to read that ONE token as two facts:
# roster member `dane` plus bare cadence marker `evening-review`. That made a
# generated GOALS sentence fail the full-tree main scan even though it carried
# no schedule or roster table.
#
# Mask only the marker half of an ADJACENT, canonical roster-name/known-marker
# reference before applying ROSTER_CRON_RE. Keep the roster name in the stream:
# if the same line also says `daily at 9am`, carries a machine cron, or names a
# second bare marker, the real cadence evidence still combines with the owner
# and fails. A table cell such as `| dane | /morning-review |` is not adjacent
# and remains unchanged, preserving the slash-prefix positive that closed the
# earlier bypass.
mask_agent_skill_refs() {
  # Two fixed global passes are sufficient for compact lists. Each match consumes
  # its trailing delimiter, so one pass masks the odd-positioned references and
  # the second masks the even-positioned references that share those delimiters.
  # Unlike the retired restart loop, the number of whole-line passes is bounded.
  # Unlike the retired awk walk, ordinary punctuation is copied in bulk rather
  # than tested and printed one byte at a time.
  #
  # The prior sed-loop successor fixed overlap but made N adjacent references
  # quadratic; an untrusted 5,000-reference line took about 23s. The next awk
  # successor was linear on references but emitted non-token input byte by byte,
  # making large ordinary/minified files a separate stall surface. Two portable
  # GNU/BSD sed passes keep both input classes bounded and preserve case. A
  # cheap candidate-line address prevents the complex substitutions from
  # scanning large ordinary lines that contain no agent/marker pair at all.
  LC_ALL=C sed -E \
    -e "/(${ROSTER_NAMES_RE})\/(${ROSTER_MARKERS_RE})/I {" \
    -e "s#(^|[^A-Za-z0-9_-])(${ROSTER_NAMES_RE})/(${ROSTER_MARKERS_RE})([^A-Za-z0-9_/-]|$)#\\1\\2/__skill_ref__\\4#gI" \
    -e "s#(^|[^A-Za-z0-9_-])(${ROSTER_NAMES_RE})/(${ROSTER_MARKERS_RE})([^A-Za-z0-9_/-]|$)#\\1\\2/__skill_ref__\\4#gI" \
    -e '}'
}

# 3. Secret shapes — real credentials. Obvious placeholders (xxxx/1234567890/
#    example) are excluded per-line in scan_file so doc token examples do not FP.
SECRET_RE='(sk-ant-[A-Za-z0-9_-]{20}|sbp_[a-f0-9]{40}|[0-9]{8,}:AA[A-Za-z0-9_-]{30}|AIza[A-Za-z0-9_-]{35}|apify_api_[A-Za-z0-9]{30})'
SECRET_PLACEHOLDER='x{6,}|1234567890|123456789|EXAMPLE|example|YOUR_|<[a-z]|placeholder|xxxx'

# 4. Operational-artifact PATH shapes — dev reports that should never be public.
ARTIFACT_PATH_RE='(^|/)(docs/phase-reports/|[A-Za-z0-9_-]*INSTALL_REPORT\.md$|PHASE[0-9]+-[A-Z-]+-REPORT\.md$)'

# 5. Private operator first names in member-facing publish surfaces. A full-name
# scan missed the real F1 casualty because the shipped templates said only the
# operator's first name. Keep this closed vocabulary HERE, inside the protected
# CODEOWNERS gate: when the private operator roster changes, a gate maintainer
# adds the new lowercase first name to this alternation and adds a named positive
# to tests/leak-guard.test.sh. The test extracts this declaration and plants each
# listed value, so an inert addition cannot pass review unnoticed.
#
# Scope is deliberately templates/ + community/ only. Runtime agent outputs,
# scenario evidence, tests and fixtures may contain fictional people (Dana Wren,
# Morgan Vale, Wren Calloway); those are not publish-template leaks and never
# enter this check. Standalone-word boundaries avoid substrings such as
# compounds ending in "son" or "2".
#
# Betty is deliberately excluded: it is the public product codename and module
# name. Any future person-context use of that spelling requires review and a
# deliberate new classification; it must not enter this list silently.
# Follow this gate's existing split-literal convention: the protected values
# must not themselves appear as searchable plaintext in the public repository.
PRIVATE_FIRST_NAMES_RE='dav''id|britt''any|di''ego|car''los|ja''mes|hun''ter'
PUBLIC_UPSTREAM_MAINTAINER='Ja''mes'
PRODUCT_OR_PERSON_NAME_RE='bet''ty'

is_publish_surface() {
  case "$1" in
    templates/*|*/templates/*|community/*|*/community/*) return 0 ;;
    *) return 1 ;;
  esac
}

is_person_context_surface() {
  case "$1" in
    templates/*/skills/comms/SKILL.md|*/templates/*/skills/comms/SKILL.md|community/skills/comms/SKILL.md|*/community/skills/comms/SKILL.md|community/*/skills/comms/SKILL.md|*/community/*/skills/comms/SKILL.md) return 0 ;;
    *) return 1 ;;
  esac
}

# Exact-line attribution exemptions for the public upstream maintainer. Public
# maintainer attribution is not a private-identity leak, but the same bare name
# outside these reviewed bytes remains blocked. Keep this exact-path + exact-line
# shape aligned with allowlisted_line() above; never replace it with context
# regexes. The split literal prevents the protected spelling from becoming a
# searchable plaintext pattern in the public guard source itself.
allowlisted_public_maintainer_line() {
  local f="$1" line="$2" m="$PUBLIC_UPSTREAM_MAINTAINER"
  case "$f" in
    community/agents/dev-agent/GUARDRAILS.md|*/community/agents/dev-agent/GUARDRAILS.md)
      [ "$line" = "Each upstream PR = one fresh branch off grandamenium/main, 1–5 files max. Never layer one unmerged PR on top of another. $m rejects monster branches." ] && return 0
      [ "$line" = "After filing an upstream PR, always merge to local main and run \`npm run build\`. The fleet uses your local main — don't make them wait for $m." ] && return 0
      ;;
    community/agents/dev-agent/SOUL.md|*/community/agents/dev-agent/SOUL.md)
      [ "$line" = "**Upstream everything.** Framework fixes go to grandamenium/cortextos, not just the local fork. $m decides what merges — your job is to file clean, isolated PRs (1–5 files max)." ] && return 0
      ;;
    community/agents/dev-agent/SYSTEM.md|*/community/agents/dev-agent/SYSTEM.md)
      [ "$line" = "4. Always merge to local main after filing — don't wait for $m" ] && return 0
      ;;
    templates/agent-codex/AGENTS.md|*/templates/agent-codex/AGENTS.md)
      [ "$line" = "**Reply-to threading**: when $m replies in-thread to one of your earlier messages, the inject ends with \`[in reply to: <up to 200 chars of your prior message>]\`. Use this to keep the conversation coherent — refer back to what you said before, don't pretend the message arrived in a vacuum." ] && return 0
      ;;
  esac
  return 1
}

canonical_publish_path() {
  case "$1" in
    templates/*|community/*) printf '%s' "$1" ;;
    */templates/*) printf 'templates/%s' "${1#*/templates/}" ;;
    */community/*) printf 'community/%s' "${1#*/community/}" ;;
    *) return 1 ;;
  esac
}

line_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | awk '{print $1}'
  else
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  fi
}

# Exact-site ratchet for the known pre-fix population. A row exempts only one
# repository-relative path, one 1-based line number, and one exact-line hash.
# Moving or editing the same leak makes the tuple miss and therefore fails.
# Absence means a zero baseline (the required final state after PR-B), never a
# pattern fallback.
baseline_has_private_first_name_site() {
  local f="$1" line_no="$2" content="$3" path hash
  [ -f "$PRIVATE_FIRST_NAME_BASELINE" ] || return 1
  path=$(canonical_publish_path "$f") || return 1
  hash=$(line_sha256 "$content")
  awk -F '\t' -v p="$path" -v n="$line_no" -v h="$hash" '
    $1 == p && $2 == n && $3 == h { found = 1 }
    END { exit(found ? 0 : 1) }
  ' "$PRIVATE_FIRST_NAME_BASELINE"
}

scan_file() {
  local f="$1" hit line_no
  # F4: skip ONLY the guard machinery itself, by EXACT path (it legitimately
  # contains the detection patterns). No prefix wildcards: tests/leak-guard.test.sh
  # and any tests/leak-guard-*.md ARE scanned like every other file.
  case "$f" in
    .github/scripts/leak-guard.sh|.github/workflows/leak-guard.yml) return ;;
  esac

  # F2: the PUBLIC orgs/ carve-outs that .gitignore re-includes as tracked
  # (!orgs/*/docs/durable/**, !orgs/*/knowledge.md, !orgs/*/research-artifacts/
  # .gitignore) ARE scanned — they ship publicly, so a leak there is a real leak.
  # A path that reaches the guard in CI is by definition TRACKED (git ls-tree /
  # diff --name-only). So a tracked path matching the private-runtime bucket
  # ships publicly yet claims to be private — that IS the leak signal, and it is
  # reported, not silently exempted. Genuinely-private runtime is gitignored and
  # never reaches CI. The workflow's filter_private() stays in lockstep.
  case "$f" in
    orgs/*/docs/durable/*|*/orgs/*/docs/durable/*) : ;;
    orgs/*/knowledge.md|*/orgs/*/knowledge.md) : ;;
    orgs/*/research-artifacts/.gitignore|*/orgs/*/research-artifacts/.gitignore) : ;;
    # graphify is a SHIPPED plugin skill that lives under orgs/; scan it like any public file (exact path, not a wildcard).
    orgs/ascendops/agents/codie/plugins/cortextos-agent-skills/skills/graphify/SKILL.md|*/orgs/ascendops/agents/codie/plugins/cortextos-agent-skills/skills/graphify/SKILL.md) : ;;
    # TEMPORARY CARVE-OUT — added 2026-08-07, owner dane, decision due at the
    # 2026-08-07 evening review (task tracked).
    #
    # This file is tracked runtime state and the bucket rule is RIGHT about it.
    # Untracking it is a policy decision with wide blast radius (many agent files
    # are tracked and live-modified) and may be exactly what the
    # wip/boot-slim-memory-migration branch already covers, so it goes through
    # David and design rather than a quiet fix here.
    #
    # The carve-out exists so main is not permanently red: a red main normalises
    # red and blinds the guard to NEW leaks, which costs more than this one known
    # file. It exempts the PATH-BUCKET rule only — the content scan below still
    # applies, so a secret or operator path inside it is still caught.
    #
    # REMOVE THIS once the untrack decision lands, in either direction.
    orgs/ascendops/agents/aussie/MEMORY.md|*/orgs/ascendops/agents/aussie/MEMORY.md) : ;;
    # Aussie's daily snapshot pair, added 2026-08-10. Same reasoning and same
    # shape as the MEMORY.md carve-out above: these are committed deliberately
    # for DURABILITY (unversioned live state is one `git checkout` from gone),
    # which collides with the private-runtime-path rule. Repo is private; the
    # config carries no secret values — tokens live in .env, never here.
    #
    # PATH-CLASS EXEMPTION ONLY. `: ;;` is a no-op, so execution falls through
    # past this case block into the operator-path, roster, artifact-path and
    # SECRET_RE content scans. These files stay fully content-scanned, so the
    # exemption cannot become a blind spot if config.json ever carries a value.
    # Do not convert these to a `return` — that would skip the content checks.
    orgs/ascendops/agents/aussie/GOALS.md|*/orgs/ascendops/agents/aussie/GOALS.md) : ;;
    orgs/ascendops/agents/aussie/config.json|*/orgs/ascendops/agents/aussie/config.json) : ;;
    orgs/*|.agent/*|agents/*/memory/*|agents/*/local/*|agents/*/telegram-images/*) \
      report "$f" "private runtime path is tracked in the public tree (untrack it or add an explicit carve-out)"; return ;;
  esac

  # Path-shape check (applies to any path).
  if printf '%s' "$f" | grep -qE "$ARTIFACT_PATH_RE"; then
    report "$f" "operational-artifact path (dev report — must not be in public repo)"
  fi

  # A tracked symlink can smuggle an operator path in its TARGET string (git
  # stores the symlink as its target text). Scan the link target itself, since
  # the [ -f ] check below either follows the link to unrelated content or, for
  # a dangling link, returns early — either way missing a leaking target.
  if [ -L "$f" ]; then
    tgt=$(readlink "$f" 2>/dev/null || echo "")
    if printf '%s' "$tgt" | grep -iqE "$HOME_PATH_RE"; then
      report "$f" "operator home path in symlink target: $tgt"
    fi
    return
  fi

  # Content checks only for existing, non-binary files.
  [ -f "$f" ] || return
  grep -Iq . "$f" 2>/dev/null || return   # skip binary

  # Bare private first name — only member-facing template/publish surfaces.
  # This is intentionally independent of the roster/cadence detector below:
  # a private human name is a leak without needing neighboring schedule syntax.
  if is_publish_surface "$f"; then
    while IFS= read -r line; do
      line_no=${line%%:*}
      hit=${line#*:}
      allowlisted_public_maintainer_line "$f" "$hit" && continue
      baseline_has_private_first_name_site "$f" "$line_no" "$hit" && continue
      report "$f" "private operator first name in publish surface: $(printf '%s' "$line" | tr -s ' ' | cut -c1-100)"
    done < <(grep -inE "(^|[^A-Za-z0-9_-])(${PRIVATE_FIRST_NAMES_RE})([^A-Za-z0-9_-]|$)" "$f" 2>/dev/null)
  fi

  # The public Betty product codename is not a private-person match. That
  # exclusion is bounded, not blanket: a standalone Betty inside the shipped
  # human-communications instruction surface is person-context and fails shut.
  # Legitimate future codename prose in that narrow surface needs exact review,
  # never a broader exemption.
  if is_person_context_surface "$f"; then
    while IFS= read -r line; do
      report "$f" "private person name in communications template: $(printf '%s' "$line" | tr -s ' ' | cut -c1-100)"
    done < <(grep -inE "(^|[^A-Za-z0-9_-])(${PRODUCT_OR_PERSON_NAME_RE})([^A-Za-z0-9_-]|$)" "$f" 2>/dev/null)
  fi

  # Operator home path — iterate matched lines so the exact-line fixture
  # allowlist can exempt known synthetic lines without weakening the pattern.
  while IFS= read -r line; do
    allowlisted_line "$f" "$line" && continue
    report "$f" "operator home path: $(printf '%s' "$line" | tr -s ' ' | cut -c1-100)"
  done < <(grep -iE "$HOME_PATH_RE" "$f" 2>/dev/null)

  # Roster+cron table — scope OUT test files/fixtures (they legitimately build
  # agent+cron structures); the leak class was operational docs, not tests.
  case "$f" in
    tests/*|*.test.*|*.spec.*|*/__tests__/*|*/fixtures/*) ;;
    *)
      local roster_hit=0
      # Do not use grep -q here: with pipefail, an early grep exit can SIGPIPE
      # the masking stage on a large file and turn a real match into a false
      # non-match. Consume the full stream and discard grep's ordinary output.
      if mask_agent_skill_refs < "$f" | grep -inE "$ROSTER_CRON_RE" > /dev/null 2>&1; then
        report "$f" "fleet roster + cron-schedule table (internal ops detail)"
        roster_hit=1
      fi
      # Multi-line ops tables can split the roster name and a real cadence
      # expression across adjacent rows. Pipe-row context plus cadence syntax
      # prevents ordinary prose and bare skill names from becoming matches.
      # The windowed branch originally recognised ONLY machine-cron cadence, so
      # a multi-line ops table using a bare marker or a natural-language time
      # slipped through in both row orders while the machine-cron form on the
      # very same table was caught. The two branches disagreeing about what
      # counts as a cadence is what hid the single-line ordering bug too, so the
      # classes are shared here rather than restated.
      #
      # Written for the padded, lowercased line the awk below builds (" " line
      # " "), so no ^ or $ anchors are needed: padding supplies the edges, which
      # keeps the dynamic regex portable across awk implementations.
      #
      # NATURAL-LANGUAGE CADENCE ONLY, deliberately — bare markers are NOT added
      # here even though they are a cadence form on a single line. Proximity is
      # weaker evidence than adjacency: within a 3-line window a bare skill name
      # near a roster name is usually a skill INVENTORY, not a schedule. Adding
      # markers here flagged worktree-hooks-audit-2026-05-23.md, whose table
      # lists skill names against a yes/no git-ops column and contains no cadence
      # at all. A natural-language time is self-evidencing in a way a bare name
      # is not, which is why the classes differ between the two branches.
      if [ "$roster_hit" -eq 0 ] && awk -v W=3 -v roster="$ROSTER_NAMES_RE" \
          -v cadence="${ROSTER_NL_FREQ_RE}[^|]*at ((0?[1-9]|1[0-2])[ ]?(am|pm)|([01]?[0-9]|2[0-3]):[0-5][0-9]([ ]?(am|pm))?)[^a-z0-9]" '
          # Word-bound the roster names (no \b in awk; anchors in a dynamic
          # regex vary by implementation, so pad the line with spaces instead
          # and require a non-word char on BOTH sides of the name).
          BEGIN { bounded = "[^a-z0-9_-](" roster ")[^a-z0-9_-]" }
          /^[ \t]*\|/ {
            line = tolower($0)
            padded = " " line " "
            if (padded ~ bounded) name_line = NR
            if (line ~ /(heartbeat\([0-9]|pr-monitor\([0-9]|\([0-9]+ [0-9*]+ \* \* |(^|[^0-9*,\/-])[0-9*][0-9*,\/-]* [0-9*][0-9*,\/-]* [0-9*][0-9*,\/-]* [0-9*][0-9*,\/-]* [0-9*][0-9*,\/-]*([^0-9*,\/-]|$))/ || padded ~ cadence) cron_line = NR
          }
          name_line && cron_line &&
            name_line - cron_line <= W && cron_line - name_line <= W {
              found = 1
              exit
            }
          END { exit(found ? 0 : 1) }
        ' "$f" 2>/dev/null; then
        report "$f" "fleet roster + cron-schedule within 3 lines (multi-line ops table)"
      fi ;;
  esac

  # Secret shapes — skip lines that are obvious placeholders/examples.
  while IFS= read -r line; do
    printf '%s' "$line" | grep -qE "$SECRET_PLACEHOLDER" && continue
    report "$f" "secret-shaped token: $(printf '%s' "$line" | cut -c1-60)"
  done < <(grep -nE "$SECRET_RE" "$f" 2>/dev/null)
}

scan_tree_ref() {
  local ref="$1"
  local tree_oid tree_tmp tree_dir tree_index tree_list original_dir

  # Resolve first so a ref beginning with '-' cannot be interpreted as an
  # option by read-tree. The resulting object ID is the exact selected tree.
  if ! tree_oid=$(git rev-parse --verify "$ref^{tree}" 2>/dev/null); then
    echo "leak-guard: unable to resolve tree ref: $ref" >&2
    exit 2
  fi

  if ! tree_tmp=$(mktemp -d "${TMPDIR:-/tmp}/leak-guard-tree.XXXXXX"); then
    echo "leak-guard: unable to create temporary tree workspace" >&2
    exit 2
  fi
  # Bounded cleanup hardening: consolidate EXIT/TERM/delivered-INT cleanup.
  # This does NOT fix the measured SIGKILL orphan, which survives by
  # construction because SIGKILL cannot be trapped.
  # Signal handlers must exit, not merely delete: resuming the scan after
  # cleanup would silently drop every remaining materialized subject.
  trap 'rm -rf "$tree_tmp"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  tree_dir="$tree_tmp/tree"
  tree_index="$tree_tmp/index"
  tree_list="$tree_tmp/list"
  mkdir "$tree_dir"

  # Materialize the selected tree through an isolated temporary index. This is
  # exact for regular blobs and symlink target blobs, requires no mutation of the
  # real index/worktree, and avoids one git process per tracked file.
  if ! GIT_INDEX_FILE="$tree_index" git read-tree "$tree_oid" \
      || ! GIT_INDEX_FILE="$tree_index" git checkout-index -a --prefix="$tree_dir/"; then
    echo "leak-guard: unable to materialize tree ref: $ref" >&2
    exit 2
  fi
  if ! git ls-tree -r -z --name-only "$tree_oid" > "$tree_list"; then
    echo "leak-guard: unable to enumerate tree ref: $ref" >&2
    exit 2
  fi

  original_dir=$PWD
  if ! cd "$tree_dir"; then
    echo "leak-guard: unable to enter materialized tree ref: $ref" >&2
    exit 2
  fi
  while IFS= read -r -d '' f; do scan_file "$f"; done < "$tree_list"
  if ! cd "$original_dir"; then
    echo "leak-guard: unable to leave materialized tree ref: $ref" >&2
    exit 2
  fi

  rm -rf "$tree_tmp"
  trap - EXIT INT TERM
}

if [ "${1:-}" = "--tree" ]; then
  if [ "$#" -gt 2 ]; then
    echo "leak-guard: unexpected argument(s) after optional --tree ref:" >&2
    for f in "${@:3}"; do echo "  $f" >&2; done
    echo "  usage: leak-guard.sh --tree [ref]" >&2
    exit 2
  fi
  ref="${2:-HEAD}"
  scan_tree_ref "$ref"
else
  # A scan with no subject must never be reportable as clean. Previously this
  # iterated an empty list and exited 0, so `leak-guard.sh` with no arguments
  # printed nothing, succeeded, and was quotable as proof a tree was clean —
  # which is exactly how it was misused on 2026-07-30 as a pre-push gate.
  # A security control that returns PASS when it inspected nothing is worse
  # than one that crashes: the crash gets noticed.
  #
  # Exit 2, distinct from the exit 1 that means "leak found", so a caller can
  # tell "misused" from "detected". Callers that may legitimately have an empty
  # set must not reach here: leak-guard.yml exits early on an empty scan-list
  # and invokes via `xargs -0 -r`, which does not run the command at all when
  # its input is empty.
  if [ "$#" -eq 0 ]; then
    echo "leak-guard: no files to scan — refusing to report clean on an empty scan." >&2
    echo "  usage: leak-guard.sh <file>... | leak-guard.sh --tree [ref]" >&2
    exit 2
  fi

  # Family boundary: a REQUESTED subject must never be silently dropped. A
  # population that is legitimately empty after full evaluation (a valid empty
  # tree, deletion-only diff, or all-exempt set) is genuinely clean.
  #
  # Validate the whole invocation before scanning any file. A partial report
  # under an error exit is ambiguous about which subjects it covers, so mixed
  # valid/invalid input is refused atomically.
  invalid_subjects=()
  for f in "$@"; do
    if [ ! -f "$f" ] && [ ! -L "$f" ]; then
      invalid_subjects+=("$f")
    elif [ -f "$f" ] && [ ! -r "$f" ]; then
      invalid_subjects+=("$f")
    fi
  done
  if [ "${#invalid_subjects[@]}" -ne 0 ]; then
    echo "leak-guard: refusing invalid scan subject(s):" >&2
    for f in "${invalid_subjects[@]}"; do
      if [ -d "$f" ]; then
        echo "  $f (directory: pass files explicitly, or use --tree)" >&2
      elif [ -f "$f" ] && [ ! -r "$f" ]; then
        echo "  $f (unreadable file)" >&2
      else
        echo "  $f (missing or not a file)" >&2
      fi
    done
    exit 2
  fi

  for f in "$@"; do scan_file "$f"; done
fi

if [ "$fail" -ne 0 ]; then
  echo "" >&2
  echo "leak-guard FAILED: operational leak(s) detected above. If a match is a" >&2
  echo "false positive on legitimate framework content, refine the pattern in" >&2
  echo ".github/scripts/leak-guard.sh — do NOT bypass the check." >&2
  exit 1
fi
echo "leak-guard: clean"
exit 0
