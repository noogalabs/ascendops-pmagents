---
name: framework-upstream-auto-update
effort: low
description: "Daily owner-elected framework update check. One agent touches the shared canonical tree, reports findings to the member, and applies only in a separately confirmed attended action."
triggers: ["upstream check", "framework update", "check upstream", "upstream auto-update", "framework upstream", "apply upstream", "sync upstream"]
---

# Framework Upstream Auto-Update

## Trigger
- Daily cron (see `config.json` crons entry `daily-framework-upstream-auto-update`).
- Ad hoc if the member asks for an upstream check.

## Owner
Exactly one enabled agent owns the shared canonical-tree check. The enabled runtime orchestrator owns it when present; otherwise the lexicographically-first enabled agent in the org owns it. This election is computed from `enabled-agents.json`; there is no override variable.

## Member-install mode (cron boundary)

on member installs the update cron is check-and-notify only; applying an update is always the member's explicit action (D4 ruling, 2026-08-24).

For a cron-triggered member run, execute Steps 0-3 to inspect and classify, notify the member through the owner agent's normal Telegram channel, then continue only to Steps 7-8 for recording. Stop before Step 4. The cron path must never set `CORTEXTOS_CONFIRM_UPSTREAM_MERGE`, invoke `check-upstream --apply`, merge, or push. Step 4 is available only when the member explicitly requests an update in a separate attended action. Never notify specialist agents; a non-owner acts on nothing.

## Procedure

### Step 0 — Prove ownership before any repository access

For the `daily-framework-upstream-auto-update` cron injection, run this as the first command:

```bash
RESULT=$(cortextos bus check-upstream --owner-only --cron-invocation) || exit $?
```

If `RESULT.status` is `skipped`, print the named owner and stop successfully. Do not resolve or `cd` to `$CTX_FRAMEWORK_ROOT`, and do not run any git command.

For an attended manual request, omit `--cron-invocation`:

```bash
RESULT=$(cortextos bus check-upstream --owner-only) || exit $?
```

A non-owner manual run fails loudly and names the owner to ask. There is no environment-variable override. Only the elected owner receives a check result and may continue.

## Inputs
- Framework repo: the cortextos workspace root at `$CTX_FRAMEWORK_ROOT` (the canonical git repo, not the state dir, never a per-agent worktree)
- Upstream: `upstream/main` (verify with `git remote -v` if unsure)
- Current local state: local main can run ahead of upstream (your local fixes may flow upstream). Do NOT try to "sync" ahead-commits downward.

## Scope (worktree-aware)

This skill operates EXCLUSIVELY at the canonical framework root (`$CTX_FRAMEWORK_ROOT`). The `upstream` git remote is only tracked at canonical — not in per-agent worktrees. Step 0 deliberately runs before resolving or entering that root. Every repository command block after ownership is proven starts with `cd "${CTX_FRAMEWORK_ROOT:?CTX_FRAMEWORK_ROOT must be set}"` to guarantee correct cwd; each shell invocation in an agent session is a fresh shell.

### Step 1 — Read the owner-gated check result

Read `RESULT` from Step 0. The owner-only command performed the fetch and comparison after proving ownership. If it reports no new commits, skip to Step 7 (log noop and stop). Do not run a second check.

If there are new commits, list them:
```bash
cd "${CTX_FRAMEWORK_ROOT:?CTX_FRAMEWORK_ROOT must be set}"
git log --oneline HEAD..upstream/main
```

### Step 2 — Classify each commit
For each new commit, read the subject and the diff:
```bash
cd "${CTX_FRAMEWORK_ROOT:?CTX_FRAMEWORK_ROOT must be set}"
git show --stat <sha>
git show <sha>
```

Classification buckets:

| Bucket | Subject patterns | Action |
|---|---|---|
| **bugfix** | `fix(...)`, `hotfix(...)`, `fix:`, `BUG-###`, `closes BUG-###` | Auto-apply if safe paths |
| **docs/chore** | `docs:`, `chore:`, `test:`, `refactor:`, `ci:`, `build:` | Auto-apply if safe paths |
| **feature** | `feat(...)`, `feat:`, `new:` | Do NOT apply. Report it to the member for approval. |
| **mixed** | Any commit that contains multiple fix/feat changes or that is ambiguous | Report it to the member. |

### Step 3 — Check touched paths (HARD GUARDRAIL)
For EVERY new commit, scan the diff for touched paths. If ANY of the new commits touch any of these paths, **do NOT auto-apply anything**, report the whole batch to the member, and stop:

- `orgs/` — multi-tenant configuration, never auto-merge
- `**/.env*` — credentials and secrets
- `**/memory/` (agent memory subfolders)
- `**/MEMORY.md` (agent-level long-term memory)
- `community/skills/` — community skill catalog changes that affect running agents
- `community/agents/` — community agent templates that affect running agents

When flagging: collect the commit SHAs, commit messages, and touched paths, and send them to the member through the owner agent's normal Telegram channel. Do not message specialist agents and do not apply.

### Step 4 — Apply safe bugfix / docs / chore commits
If all new commits are pure bugfix or docs/chore AND none touch the guardrail paths:
```bash
cd "${CTX_FRAMEWORK_ROOT:?CTX_FRAMEWORK_ROOT must be set}"
CORTEXTOS_CONFIRM_UPSTREAM_MERGE=yes cortextos bus check-upstream --apply
```
**The `CORTEXTOS_CONFIRM_UPSTREAM_MERGE=yes` env var is required.** Without it, `check-upstream --apply` returns `{"status": "error", "error": "Refusing to auto-merge upstream..."}` as a safety gate. The env var is the "I have reviewed the diff and I trust the changes" signal. Set it inline, not exported, so it does not leak into subsequent unrelated commands.

After applying:
```bash
cd "${CTX_FRAMEWORK_ROOT:?CTX_FRAMEWORK_ROOT must be set}"
npm run build
npm test
```
Both must succeed. If either fails, DO NOT revert silently — report the failure to the member with the full error output and wait for instructions. The framework remains in its applied state; the member decides whether to revert or patch.

### Step 5 — Handle feature or mixed batches (no apply)
If any new commit is feature or mixed but all paths are safe:
- Do NOT run `--apply`
- Send the member a summary through the owner agent's normal Telegram channel containing:
  - Commit list (SHA + subject)
  - Touched paths (de-duped)
  - Your recommendation: apply as-is, hold for user review, or request clarification
- Wait for the member. The cron exits after sending the message. Never fan the notice out to specialist agents.

### Step 6 — Report to the member on success
When a bugfix batch is successfully applied and the build + tests are green:
```bash
cortextos bus send-telegram "$CTX_TELEGRAM_CHAT_ID" 'Framework upstream auto-update YYYY-MM-DD: applied N commits. Build + test green. Details: ...'
```
Include the commit list and any interesting touched paths (e.g. dist/cli.js rebuilt, specific src/ modules touched).

### Step 7 — Log and record (run this step ALWAYS, even for noop)
```bash
cortextos bus create-task "framework-upstream-check $(date +%Y-%m-%d)" --desc "Daily upstream check. Result: <applied N / flagged M / skipped K / noop>"
cortextos bus log-event action framework_updated info --meta '{"applied":N,"flagged":M,"skipped":K,"noop":BOOL}'
```

Write a single-line entry to today's daily memory file describing the result.

### Step 8 — Morning briefing hook
Include whatever was applied or flagged overnight from Step 7's memory entry in the next morning brief. Users should see the result in their morning summary, not have to ask.

## Failure Modes
- **Network failure fetching upstream** → log a warning event, do not retry in-loop, wait for next day's run.
- **Merge conflict during apply** → do NOT force. Report to the member with the conflict details and stop. The member resolves it by hand.
- **Build or test failure after apply** → do NOT auto-revert. Report to the member with full error output. The member decides whether to revert, patch, or tolerate.
- **Unexpected touched path (new guardrail category)** → report it to the member, propose the new path for the guardrail list, and wait for confirmation before adding it to this SKILL.

## Deployment Config

Add to `config.json` crons:
```json
{
  "name": "daily-framework-upstream-auto-update",
  "type": "recurring",
  "cron": "{{upstream_update_minute}} 6 * * *",
  "prompt": "Read and follow .claude/skills/framework-upstream-auto-update/SKILL.md"
}
```

`check-upstream --owner-only` reads the runtime agent/org/orchestrator identity and the enabled registry. No ownership setting belongs in this skill or agent config.

## Notes
- Local main is allowed to run ahead of upstream. `check-upstream` handles this correctly.
- Never push to upstream as part of this flow. Push is a separate manual operation.
- Bug fix application authority belongs to the user and should be granted explicitly in your deployment config or MEMORY.md.
