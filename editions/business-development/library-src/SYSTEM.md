# System Context

**Organization:** {{org}}
**Timezone:** (set from context.json at agent creation)
**BD manager seat:** (set from the onboarding interview — see business-development-config.json `people.bd_manager`)
**Dashboard:** (set from context.json at agent creation)
**Framework:** cortextOS Node.js

---

This file contains static org context only. For the live agent roster, run:
```bash
cortextos bus list-agents
```

For agent health (last heartbeat per agent), run:
```bash
cortextos bus read-all-heartbeats
```
