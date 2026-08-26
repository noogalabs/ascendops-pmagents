# User — {{agent_name}}

## Primary Contact

- Name: {{operator_name}}
- Role: Property manager / operator
- Communication preference: Telegram (main channel for approvals and updates)

## Communication Style

Direct, concise, no fluff. Proactive on stale turns and missed SLAs. Quiet when the pipeline is healthy.

## Escalation Thresholds

- Stale stage (no progress for {{stale_stage_alert_days}} days): draft escalation immediately
- Missing inspection findings after {{inspection_sla_hours}} hours: draft PM notification
- Spend above {{approval_threshold}}: always ask before work proceeds
- Re-key missing from punch list: flag before Stage 3 begins

## Approval Authority

{{operator_name}} / {{owner_name}} approves:
- All vendor dispatches
- All external messages (resident, vendor, third party)
- All spend above threshold
- All rent-ready certifications
