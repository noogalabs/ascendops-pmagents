# Heartbeat Checklist - EXECUTE EVERY STEP. SKIP NOTHING.

This runs on your heartbeat cron (every 4 hours). Execute EVERY step in order.
Skipping steps = broken system. The dashboard monitors your compliance.

## Step 1: Update heartbeat (DO THIS FIRST)

```bash
cortextos bus update-heartbeat "<1-sentence summary of current work>"
```

If this fails, your agent shows as DEAD on the dashboard. Fix it before anything else.

## Step 2: Sweep inbox for un-ACK'd messages

Messages arrive in real time via the fast-checker daemon — you don't need to poll for them. This step is a safety sweep for anything that wasn't ACK'd (e.g. a crash mid-processing).

Full reference: `.claude/skills/comms/SKILL.md`

```bash
cortextos bus check-inbox
```

For any messages returned: process and ACK each one:

```bash
cortextos bus ack-inbox "<message_id>"
```

Un-ACK'd messages are re-delivered after 5 minutes. Target: 0 un-ACK'd after this sweep.

## Step 3: Check task queue + stale task detection

Full reference: `.claude/skills/tasks/SKILL.md`

```bash
cortextos bus list-tasks --agent $CTX_AGENT_NAME --status pending
cortextos bus list-tasks --agent $CTX_AGENT_NAME --status in_progress
```

- If you have pending tasks: pick the highest priority one
- If you have in_progress tasks older than 2 hours: either complete them NOW or update their status with a note
- If you have NO tasks: check GOALS.md for objectives, then work the open alerts on the board. A BD seat is never out of work while an alert is open.

Stale tasks are visible on the dashboard. They make you look broken.

## Step 3b: Sweep the board alerts

Full reference: `.claude/skills/daily-pipeline-run/SKILL.md`

The alert register is this seat's real task queue. On every heartbeat, check for:

| Severity | Condition | Do |
|---|---|---|
| Critical | Speed-to-lead breach — an inbound lead created today with no touch logged | Touch it now. Every minute of delay is measurable conversion loss. |
| Critical | Unsigned agreement past the alert window <!-- D6 --> | Call. Find the objection. Re-close. |
| Critical | Unsigned agreement past the escalation window <!-- D6 --> | Escalate to the BD manager. Log first, then escalate. |
| Critical | Overdue next action | Do it today. |
| Critical | Active deal with a blank next action | Set one now. A blank next action is a data-quality failure, not a scheduling gap. |
| Critical | Handoff unconfirmed past its window | Confirm with onboarding. The owner is waiting on someone who does not know they exist yet. |
| Warning | Stage past its maximum days <!-- D6 --> | Move it, or move it to nurture. Do not let it sit. |
| Warning | Cold lead — no touch past the threshold <!-- D5 --> | Log a real touch. Not a nudge. |
| Warning | Nurture record with no touch in the nurture window <!-- D5 --> | Re-engage or archive. |
| Warning | Referral fee owed past its window <!-- B9, C7 --> | Flag to the referral fee payer by name. |
| Warning | Pipeline doors below the minimum multiple of the monthly door goal <!-- D8 --> | Tell the BD manager the same cycle. This one does not wait for the weekly review. |

No alert carries across two consecutive cycles without a logged action and a new next-action date. If one does, that is itself worth surfacing.

**Night mode:** work the board, work the research, stage the drafts. Nothing owner-facing leaves in night mode, staged or otherwise.

## Step 4: Log heartbeat event

Full reference: `.claude/skills/event-logging/SKILL.md`

```bash
cortextos bus log-event heartbeat agent_heartbeat info --meta '{"agent":"'$CTX_AGENT_NAME'"}'
```

## Step 5: Write daily memory

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
- Inbox: <N messages processed>
- Next action: <what you will do next>
MEMORY
```

## Step 6: Check GOALS.md

Read GOALS.md. Goals are set by the BD manager, normally at the weekly pipeline review.

- If goals were updated recently: you should already have tasks. If not, create them now — see `.claude/skills/tasks/SKILL.md`
- If goals are stale: raise it at the next review rather than pinging between reviews; the weekly cadence is the cadence <!-- D9 -->
- If you have no goals at all: work the alert register. It never runs dry, and it is always the right work.

## Step 7: Resume work

Full reference: `.claude/skills/tasks/SKILL.md`

Pick your highest priority task and work on it. Tasks should trace back to your current goals.

When starting:
```bash
cortextos bus update-task "<task_id>" in_progress
```

When done:
```bash
cortextos bus complete-task "<task_id>" --result "<summary of what was produced>"
```

If you are blocked, see `.claude/skills/human-tasks/SKILL.md` for the human task and approval workflow.
If you need an approval before acting, see `.claude/skills/approvals/SKILL.md`.

## Step 8: Guardrail self-check

Full reference: `.claude/skills/guardrails-reference/SKILL.md`

Ask yourself: did I skip any procedures this cycle? Did I rationalize not doing something I should have?

If yes, log it:
```bash
cortextos bus log-event action guardrail_triggered info --meta '{"guardrail":"<which one>","context":"<what happened>"}'
```

If you discovered a new pattern that should be a guardrail, add it to GUARDRAILS.md now.

**Seat-specific self-check, every cycle:**
- Did anything owner-facing leave without a release?
- Did I answer a fee, contract, legal, property-acceptance, or walk-away question instead of routing it?
- Did I say a number, a date, or an outcome that is on the Never-Promise List?
- Did I log an escalation *after* the conversation instead of before?
- Did a prospect's name land anywhere other than the pipeline board?

Any yes is a guardrail event. Log it, and tell the BD manager the same cycle — not at the weekly review.

## Step 9: Update long-term memory (if applicable)

Full reference: `.claude/skills/memory/SKILL.md`

If you learned something this cycle that should persist across sessions:
- Patterns that work/don't work
- User preferences discovered
- System behaviors noted
- Append to MEMORY.md

## Step 10: Re-ingest memory to knowledge base

Full reference: `.claude/skills/knowledge-base/SKILL.md`

Keep your memory collection searchable and current:

```bash
cortextos bus kb-ingest ./MEMORY.md ./memory/$(date -u +%Y-%m-%d).md \
  --org $CTX_ORG --agent $CTX_AGENT_NAME --scope private --force
```

This runs automatically on every heartbeat cycle. It ensures past experiences, user preferences, and learned patterns are semantically searchable for future tasks. Skip if GEMINI_API_KEY is not configured.

---

REMINDER: A heartbeat with 0 events logged and 0 memory updates means you did nothing visible.
Target: >= 2 events and >= 1 memory update per heartbeat cycle.
Invisible work is wasted work.
