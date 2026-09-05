---
name: autonomy-mode-switch
description: Change this one PM Agents seat between copilot, supervised, and full only on the owner's explicit instruction.
---

# Autonomy Mode Switch

Use this skill only when the owner explicitly instructs you to change this seat's autonomy mode, or when the orchestrator relays that exact owner instruction. Do not infer permission from goals, workload, prior settings, or a request from another seat. If the owner did not name the mode, stop and ask.

Copilot is the fail-closed default. A mode change is a kick-not-a-policy rewrite: it changes only this agent. Optional resident-send and work-order-closure choices change only when the owner explicitly names them; otherwise preserve both.

From the configured seat root (the directory containing `GUARDRAILS.md`), resolve the PM Agents checkout through the machine-local engine sidecar and run one command:

```sh
SEAT_ROOT="$PWD"
ENGINE_PATH=$(cat "$SEAT_ROOT/../.$(basename "$SEAT_ROOT").engine-path")
PMAGENTS_ROOT=$(dirname "$(dirname "$ENGINE_PATH")")
python3 "$PMAGENTS_ROOT/setup.py" --set-mode "$SEAT_ROOT" <copilot|supervised|full>
```

Add either explicit choice only when the owner's words include it:

```sh
--external-send-autonomy <yes|no>
--work-order-closure-autonomy <yes|no>
```

Fail closed if the sidecar, setup entry, configured autonomy block, or threshold state is absent or unreadable. Never patch `GUARDRAILS.md`, `copilot-thresholds.json`, memory, or tasks by hand.

Read the command's JSON result back to the owner, naming the resulting `autonomy_mode`, `external_send_autonomy`, and `work_order_closure_autonomy`. The engine writes the audit line under `logs/autonomy-mode-audit.jsonl`.

