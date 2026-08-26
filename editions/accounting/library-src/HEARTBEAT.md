# Heartbeat Checklist — EXECUTE EVERY STEP. SKIP NOTHING.

This runs on your heartbeat cron. Execute EVERY step in order. Skipping steps = broken system.

## Step 1: Update heartbeat (DO THIS FIRST)

```bash
cortextos bus update-heartbeat "<1-sentence summary of current work>"
```

If this fails, your agent shows as DEAD on the dashboard. Fix it before anything else.

## Step 2: Sweep inbox for un-ACK'd messages

Messages arrive in real time via the fast-checker daemon. This step is a safety sweep for anything that was not ACK'd (for example, a crash mid-processing).

Full reference: `.claude/skills/comms/SKILL.md`

```bash
cortextos bus check-inbox
cortextos bus ack-inbox "<message_id>"
```

Un-ACK'd messages redeliver after 5 minutes. Target: 0 un-ACK'd after this sweep.

## Step 3: Run the money-critical sweep

This is the accounting seat's version of the task-queue check, and it runs BEFORE the task queue because these items carry statutory and fraud exposure. Full reference: `.claude/skills/daily-money-review/SKILL.md`.

Check, in this order, and stop on the first red:

1. **Suspected fraud or unrecognized trust transaction** — anything in the bank feed nobody initiated. Drop everything; run `.claude/skills/fraud-and-unauthorized-transactions/SKILL.md`.
2. **Trust out of balance** — any open three-way variance. If statements are due, statements do not go out.
3. **Deposit deadlines** — any disposition inside its {{deposit_return_days}} <!-- A6 --> window or past it.
4. **Returned payments** — any NSF or ACH reject from the bank since the last cycle.
5. **Unidentified payments** — anything sitting in suspense; same-day escalation at or above {{unidentified_payment_escalation_threshold}} <!-- B4 -->.
6. **Vendor banking change requests** — any received since the last cycle; payments to that vendor freeze immediately.
7. **Reserve floors** — any owner ledger below {{reserve_floor}} <!-- B3 -->.
8. **Approvals aging** — any property-manager approval pending more than 24 hours (remind) or 48 hours (escalate).

Anything red gets a task and an escalation before you move on.

## Step 4: Check task queue + stale task detection

Full reference: `.claude/skills/tasks/SKILL.md`

```bash
cortextos bus list-tasks --agent $CTX_AGENT_NAME --status pending
cortextos bus list-tasks --agent $CTX_AGENT_NAME --status in_progress
```

- Pending tasks: pick the highest priority one.
- in_progress older than 2 hours: complete them now or update status with a note.
- No tasks: check GOALS.md, then ask the property manager.

## Step 5: Sweep approvals

Full reference: `.claude/skills/approvals/SKILL.md`

```bash
cortextos bus list-approvals --status pending
```

Every money-gated item you drafted should have a live approval with a blocked parent task. An approval with no blocked task, or a blocked task with no approval, is a bookkeeping error in your own queue — fix it this cycle.

## Step 6: Log heartbeat event

Full reference: `.claude/skills/event-logging/SKILL.md`

```bash
cortextos bus log-event heartbeat agent_heartbeat info --meta '{"agent":"'$CTX_AGENT_NAME'"}'
```

## Step 7: Write daily memory

Full reference: `.claude/skills/memory/SKILL.md`

```bash
TODAY=$(date -u +%Y-%m-%d)
LOCAL_TIME=$(date +'%-I:%M %p %Z' 2>/dev/null || date)
MEMORY_DIR="$(pwd)/memory"
mkdir -p "$MEMORY_DIR"
cat >> "$MEMORY_DIR/$TODAY.md" << MEMORY

## Heartbeat Update - $(date -u +'%H:%M UTC') / $LOCAL_TIME
- WORKING ON: <task_id or "none">
- Status: <healthy/working/blocked>
- Money-critical sweep: <clean | N reds, listed>
- Open trust variance: <none | amount + leg>
- Deposit clocks inside window: <none | unit + days remaining>
- Approvals pending: <N, oldest age>
- Inbox: <N messages processed>
- Next action: <what you will do next>
MEMORY
```

## Step 8: Check GOALS.md

Read GOALS.md. If goals are stale (more than 24h without update), ask for fresh ones. Do not idle.

## Step 9: Resume work

Full reference: `.claude/skills/tasks/SKILL.md`

```bash
cortextos bus update-task "<task_id>" in_progress
cortextos bus complete-task "<task_id>" --result "<summary of what was produced>"
```

If you are blocked, see `.claude/skills/human-tasks/SKILL.md`. If you need an approval before acting, see `.claude/skills/approvals/SKILL.md`.

## Step 10: Guardrail self-check

Full reference: `.claude/skills/guardrails-reference/SKILL.md`

Did you skip any procedure this cycle? Did you rationalize not doing something? Did you report a figure you did not re-derive from source?

```bash
cortextos bus log-event action guardrail_triggered info --meta '{"guardrail":"<which one>","context":"<what happened>"}'
```

If you discovered a new pattern that should be a guardrail, add it to GUARDRAILS.md now.

## Step 11: Update long-term memory (if applicable)

Full reference: `.claude/skills/memory/SKILL.md`

Append to MEMORY.md anything worth carrying across sessions: owner or management-agreement quirks, repeat NSF residents, vendors who invoice without work orders, recurring reconciliation timing items, and every correction received.

## Step 12: Re-ingest memory to knowledge base

Full reference: `.claude/skills/knowledge-base/SKILL.md`

```bash
cortextos bus kb-ingest ./MEMORY.md ./memory/$(date -u +%Y-%m-%d).md \
  --org $CTX_ORG --agent $CTX_AGENT_NAME --scope private --force
```

---

REMINDER: a heartbeat with 0 events logged and 0 memory updates means you did nothing visible.
Target: at least 2 events and at least 1 memory update per cycle.
A clean money-critical sweep is a result worth logging — say "clean," do not say nothing.
