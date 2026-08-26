# Tools Quick Reference

All cortextOS commands: `cortextos bus <command>`. Full docs in skill files — load the relevant skill when you need details on a workflow. The complete bus surface, beyond the index below, is in `.claude/skills/bus-reference/SKILL.md`.

---

## Environment Variables

| Variable | Source | Value |
|---|---|---|
| `CTX_AGENT_NAME` | daemon | Your agent name |
| `CTX_ORG` | daemon | Org name |
| `CTX_ROOT` | daemon | `~/.cortextos/{instance}` |
| `CTX_FRAMEWORK_ROOT` | daemon | Framework repo root |
| `CTX_TIMEZONE` | config.json | Your local timezone |
| `CTX_TELEGRAM_CHAT_ID` | agent .env | Your Telegram chat ID |
| `ANTHROPIC_API_KEY` | shell profile | Never stored in a file |

Shared secrets (all agents): `orgs/{org}/secrets.env`
Agent secrets: `orgs/{org}/agents/{agent}/.env`

**Never echo a credential, an account number, or a routing number into a log, a memory file, a task description, or a bus message.** If you need to reference an account, use its purpose label from SYSTEM.md.

---

## Command Index

### Tasks — full docs: `.claude/skills/tasks/SKILL.md`
| Command | What it does |
|---|---|
| `create-task "<title>" --desc "<desc>"` | Create a task (visible on dashboard) |
| `update-task <id> <status>` | pending / in_progress / blocked / completed |
| `complete-task <id> --result "<what>"` | Mark done with result |
| `list-tasks [--status S] [--agent A]` | List / filter tasks |
| `check-stale-tasks` | Find tasks stale more than 2h in_progress or 24h pending |
| `check-human-tasks` | Check for stale human-assigned tasks |

### Approvals — full docs: `.claude/skills/approvals/SKILL.md`
| Command | What it does |
|---|---|
| `create-approval "<title>" <category> "[context]"` | Request human approval |
| `update-approval <id> <approved\|rejected> "[note]"` | Resolve an approval |
| `list-approvals [--status S]` | List approvals |

This is the most-used command family in this seat. Categories: `financial`, `ledger-adjustment`, `trust-transfer`, `owner-draw`, `vendor-payment`, `deposit-return`, `vendor-banking-change`, `external-comms`, `data-deletion`, `other`.

### Messages — full docs: `.claude/skills/comms/SKILL.md`
| Command | What it does |
|---|---|
| `send-message <agent> <priority> '<text>' [reply_to]` | Send to another agent |
| `check-inbox` | Check incoming messages (run every heartbeat) |
| `ack-inbox "<msg_id>"` | ACK a message |
| `notify-agent <agent> "<msg>"` | Urgently signal another agent's fast-checker |

### Telegram — full docs: `.claude/skills/comms/SKILL.md`
| Command | What it does |
|---|---|
| `send-telegram <chat_id> "<msg>"` | Message the user |
| `send-telegram <chat_id> "<caption>" --file <path>` | Send a file (statement draft, close package) |
| `post-activity "<msg>"` | Post to the org activity channel |

Single-quote any payload containing a dollar figure or a backtick.

### Events & Heartbeat — full docs: `.claude/skills/heartbeat/SKILL.md`
| Command | What it does |
|---|---|
| `log-event <category> <name> <severity> --meta '<json>'` | Log structured event |
| `update-heartbeat "<task summary>"` | Prove you are alive to the dashboard |
| `read-all-heartbeats` | Aggregate fleet heartbeats |
| `recall-facts [--days 3]` | Recall session facts extracted at compaction |

### Knowledge Base — full docs: `.claude/skills/knowledge-base/SKILL.md`
| Command | What it does |
|---|---|
| `kb-query "<question>" --org $CTX_ORG` | Semantic search |
| `kb-ingest <path> --org $CTX_ORG --scope private` | Index files into your private KB |
| `kb-collections --org $CTX_ORG` | List available collections |

Financial source documents are private-scope only. Never shared.

### Crons — full docs: `.claude/skills/cron-management/SKILL.md`
| Command | What it does |
|---|---|
| `list-crons <agent>` | Show registered crons |
| `add-cron <agent> <name> <interval\|cron-expr> "<prompt>"` | Add a recurring cron |
| `update-cron <agent> <name> --interval <i>` | Change interval or prompt |
| `remove-cron <agent> <name>` | Remove a cron |

### Discovery & Fleet
| Command | What it does |
|---|---|
| `list-agents [--format json\|text]` | All agents in the system |
| `list-skills [--format text\|json]` | Skills available to this agent |

### Lifecycle
| Command | What it does |
|---|---|
| `self-restart --reason "<why>"` | Restart with history preserved |
| `hard-restart --reason "<why>"` | Fresh session |
| `auto-commit [--dry-run]` | Daily workspace snapshot (local only) |

---

## Accounting Data Access

This agent is **read-only by construction**. The platform, the bank, and the board are read surfaces, not write surfaces.

| Source | How it is reached | Configured at |
|---|---|---|
| Accounting platform reports | export or read-only report path | D7 → SYSTEM.md |
| Bank statements / feeds | statement drop or read-only feed | D7 → SYSTEM.md |
| Tracking board | spreadsheet or platform view | D6 → SYSTEM.md |
| PM decision log | spreadsheet workbook | D6 → SYSTEM.md |
| W-9 files / 1099 tracker | shared folder | D9 → SYSTEM.md |

If a source is missing or stale, that is a flag, not a gap to fill by inference. Say the number is unsupported and request the source.

---

## Spreadsheet and Document Work

The tracking board and the decision log are spreadsheet-first by design. Use whatever spreadsheet tooling is available on the install (see `.claude/skills/tool-registration/SKILL.md` to register what exists) and prefer appending a row over rewriting a sheet. Never rewrite a board tab in place — a lost audit-log column is unrecoverable.
