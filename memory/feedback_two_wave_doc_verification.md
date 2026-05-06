---
name: Document-write verification = Reality Checker + purpose-matched specialist (2-wave)
description: NON-NEGOTIABLE — every write to CLAUDE.md, docs/plans/, docs/specs/, or any tracked contracts/docs/** artifact runs two-wave verification (Reality Checker mandatory + specialized agent matched to document purpose) BEFORE commit
type: feedback
originSessionId: d1cfac41-85eb-4cae-ae40-bddd97fffc23
---
NON-NEGOTIABLE: Every write to a project document — `.worktree/ranFromAngstrom/CLAUDE.md`, anything under `docs/plans/`, anything under `docs/specs/`, or any tracked `contracts/docs/**` artifact — runs a two-wave verification BEFORE the change is committed.

**Why:** User directive 2026-04-27. Framework-level governance writes (CLAUDE.md edits, plans, specs) are load-bearing for everything downstream — bad claims propagate fast and are expensive to roll back once committed. Reality Checker catches fantasy / unsupported assertions; the purpose-matched specialist catches domain-specific defects (econometric flaws in econ specs, security flaws in Solidity specs, workflow gaps in process policies, etc.). One-agent review is insufficient because no single agent covers both the evidence axis and the domain axis.

**How to apply:**
- Wave 1 (always): dispatch Reality Checker on the draft text.
- Wave 2 (purpose-matched): pick the specialist whose domain matches the document content. Defaults:
   - Econometric / structural-econ spec → Model QA Specialist
   - Solidity / EVM contract spec → Senior Developer or Code Reviewer
   - Research artifact → domain-appropriate research agent (Trend Researcher, Anthropologist, etc.)
   - Process / governance / workflow policy → Workflow Architect
   - Documentation prose / clarity → Technical Writer
   - Plan or roadmap → Senior Project Manager or domain specialist
   - When in doubt → Technical Writer + surface ambiguity to user
- Run both waves in parallel unless findings are mutually dependent (almost always independent).
- Integrate findings BEFORE commit. Revise + re-run on failure; never silent override.
- Out of scope for this rule: memory files (`~/.claude/.../memory/`), scratch artifacts (`scratch/`), runtime outputs (notebooks, pipeline data, parquets).
- Supersedes `feedback_three_way_review` (Code Reviewer + Reality Checker + Technical Writer) for *documents*; that 3-way pattern survives only for code-implementation reviews per `feedback_implementation_review_agents`.

**Recursion note:** This rule applies to writes to CLAUDE.md itself. The CLAUDE.md edit installing this rule was verified by Reality Checker + Workflow Architect in parallel (the canonical Wave-2 specialist for governance/process policies) before commit.
