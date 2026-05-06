---
name: RAN branch Python-only session
description: ran-v1a sessions are Python backend dev only — use Backend Architect, Data Engineer agents and functional-python skill; venv must be active for all agents
type: project
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
The ran-v1a branch sessions are **Python backend development only**. No Solidity work.

**Required agents for sub-agent dispatch:**
- Backend Architect (backend system design, API, data pipelines)
- Data Engineer (data pipelines, ETL, data infrastructure)

**Required skills:**
- `functional-python` — frozen dataclasses, free pure functions, full typing, no inheritance, composition-first
- `superpowers:test-driven-development` — TDD approach for all implementation

**Development approach:** Test-Driven Development (TDD) — tests first, then implementation.

**Agent orchestration:** Agents Orchestrator dispatching to Data Engineer, Senior Developer (Backend), Analytics Reporter + functional-python skill.

**Why:** User explicitly scoped this session to Python backend work building on the existing Angstrom Python infrastructure (eth-account venv, EIP-712 FFI, snapshot scripts). TDD enforced for all code.

**How to apply:**
- Always activate venv before running Python: `source contracts/.venv/bin/activate`
- When dispatching sub-agents, use `Backend Architect` or `Data Engineer` subagent_type
- Invoke `functional-python` skill before writing any Python code
- Invoke `superpowers:test-driven-development` before any implementation task
- All sub-agents in this session hierarchy inherit these constraints
