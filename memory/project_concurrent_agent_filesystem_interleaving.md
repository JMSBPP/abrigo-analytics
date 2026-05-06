---
name: Concurrent-agent file-system interleaving
description: When two subagents touch overlapping files in parallel, one agent's commit may pick up the other's modifications; verify via git log -p per file
type: feedback
originSessionId: phase0-vb-mvp / Rev-5.3 Tasks 11.N.1b + 11.N.2b.2 parallel dispatch
---

**Fact**: When two specialized subagents (e.g., two Data Engineer agents) operate in parallel on the same worktree and touch overlapping files (e.g., both writing to `contracts/scripts/econ_pipeline.py` for different ingestion paths), the file-system state at commit time may interleave their edits. One agent's `git add + git commit` can sweep up changes the other agent made in the interim, producing a commit whose diff is broader than the dispatched agent's actual scope.

**Why**: the worktree's filesystem is a shared-state resource across concurrent agents. Each agent's session is logically isolated, but their writes land on the same disk. If Agent A finishes and commits `[file X, file Y]` while Agent B has been writing to `file X` on a different scope, Agent A's commit will include Agent B's partial work — silently. The Rev-5.3 chain saw this pattern when Task 11.N.1b (COPM raw-transfers backfill) and Task 11.N.2b.2 (Carbon ingestion) both touched `econ_pipeline.py`; the 11.N.1b commit picked up some Carbon-ingestion scaffold from 11.N.2b.2's earlier draft.

**How to apply**:
1. After concurrent-agent dispatches that touch overlapping files, the orchestrator MUST run `git log -p <file>` per overlapping file to verify each agent's commit contains only its scoped changes.
2. If interleaving is detected: inventory the rogue lines, decide which commit they belong in, and either (a) reset and re-commit cleanly, or (b) file a CORRECTIONS-block-style memo documenting the interleaving and the corrected attribution.
3. Prefer SEQUENTIAL dispatch over PARALLEL dispatch for tasks that touch overlapping files; only parallelize when file-scopes are demonstrably disjoint.
4. Add disjointness verification to the dispatch brief: each agent should declare its expected file-touch list up-front, and the orchestrator should validate disjointness before dispatch.
5. Pattern observed in: Rev-5.3 Tasks 11.N.1b (`9f0997ed5`) + 11.N.2b.2 (`2855240ae`); see git log -p for both commits to inspect actual interleaving.

## Related memory

- `feedback_no_parallel_agents_same_dir.md` — companion existing rule (broader scope)
- `feedback_specialized_agents_per_task.md` — companion: orchestrator verifies, never authors
- `feedback_background_agent_stream_watchdog_timeout.md` — companion operational caveat
