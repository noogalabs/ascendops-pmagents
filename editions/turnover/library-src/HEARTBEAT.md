# Heartbeat — Turnover Coordinator

## What to do every heartbeat cycle

1. Update heartbeat status with the current pipeline state.
2. Check inbox for new messages.
3. Check for stale stages (any turn stuck longer than {{stale_stage_alert_days}} days without progress — draft PM escalation).
4. Check for pending QC items (must-fix items reported-done but not yet verified — request evidence).
5. Check for pending certifications (all must-fix verified + re-key verified — issue completion record).
6. Continue highest-priority active turn task.

## Accountability targets per cycle

- Heartbeat updated: yes
- Inbox checked: yes
- Stale stage alerts sent: any overdue
- Evidence-blocked items flagged: any pending

## Day/Night mode

**Day mode ({{day_mode_start}} – {{day_mode_end}} {{timezone}}):** responsive, user-directed, active pipeline management.

**Night mode:** internal work only. No external comms. Draft stale alerts and pipeline updates for morning review.
