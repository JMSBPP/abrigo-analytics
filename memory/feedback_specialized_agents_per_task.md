---
name: Specialized agents per task (execution rule)
description: Every Abrigo plan task must leverage the appropriate specialized subagent from the catalog, not hand-authoring by the foreground session
type: feedback
originSessionId: bc613a18-50d4-4456-83d1-ae746e1240e0
---
For every task executed from the Abrigo implementation plan (and by extension, any plan in this project), the foreground session MUST dispatch a specialized subagent appropriate to the task rather than authoring the output directly. The foreground session's role is orchestration + verification, not authorship.

**Task-to-agent mapping (Abrigo plan):**
- Authoring the brand-agent system prompt → `system-prompt-creator` (custom, guided by `~/.claude/system-prompt-generator.md`)
- Authoring reviewer invocation templates → `system-prompt-creator` per template
- Authoring orchestrator operating procedure → `Workflow Architect` or `Technical Writer`
- Authoring source-manifest format spec → `Software Architect` or `Technical Writer`
- Drafting copy artifacts (one-pager, pitches, application answers, taglines) → `abrigo-brand-agent` (once built)
- Reviewing artifacts → the triad defined in spec §7.1 (`Brand Guardian`, `Claim Auditor`/Reality Checker, plus the artifact-specific third seat)
- Verifying Crecimiento intake is open → can be foreground (single URL check)
- Founder-input tasks (facts.yml, form questions paste, final submission) → founder direct; no agent

**Why:** specialized agents bring domain posture, formatting discipline, and critical distance the foreground session cannot easily self-impose. Having Claude Code instead of the foreground session draft the brand-agent prompt also creates an audit trail per-artifact.

**How to apply:** before every plan task, identify the specialist. If none fits, flag to the founder. Never default to "I'll write it myself" for artifacts that have a specialist match.

**Exceptions:** shell-ops tasks (mkdir, mv, git commit, gitignore edits) run from the foreground session because they have no specialist. Smoke-test verification runs from the foreground because it must observe the specialist's output to test it.
