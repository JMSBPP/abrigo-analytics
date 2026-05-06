---
name: Agent orchestration pattern for branched tasks
description: Branched/parallel tasks must use Agents Orchestrator dispatching to Data Engineer, Backend Architect, Analytics Reporter agents + functional-python skill
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
For tasks that branch into parallel or multi-concern work, follow this agency pattern:

**Agents Orchestrator** (top-level coordinator) dispatches to:
- **Data Engineer** — pipelines, storage schemas, ETL, data infrastructure
- **Senior Developer** (Backend) — API design, service logic, integration
- **Analytics Reporter** — data analysis, dashboards, metrics, reporting
- **functional-python skill** — enforced on all Python code output

These are **recommended, not restricted** — other agents can be added as needed.

**Why:** User wants structured orchestration for complex tasks rather than a single agent trying to do everything. Ensures each concern gets domain-expert treatment.

**How to apply:** When a brainstorm or plan reveals 2+ independent work streams, use the Agents Orchestrator subagent_type to coordinate, dispatching child agents with the appropriate subagent_type from the list above. Always invoke functional-python skill before any Python code is written by any agent.
