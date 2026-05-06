---
name: Background-agent stream-watchdog timeout pattern
description: Single 400+ line edits stall the background-agent watchdog after ~600s; mitigation = ≤200-line edits OR bash heredoc + sed splice for large content moves
type: feedback
originSessionId: phase0-vb-mvp / Rev-5.3 fold recovery
---

**Fact**: Technical-Writer (and other) background subagents attempting a single large `Edit` tool call covering 400+ lines of replacement consistently hit the stream-watchdog timeout at approximately 600 seconds and stall mid-edit. The dispatched agent does not error cleanly — it appears unresponsive. Affected workflows include large plan-section folds, design-doc revisions, and CORRECTIONS-block insertions when authored as a single monolithic edit.

**Why**: the watchdog appears to monitor stream activity, not raw elapsed time, and large diff payloads can starve the heartbeat between tool-call segments. The Rev-5.3 plan-fold recovery (commit `17fa79d82`) hit this pattern when a TW agent tried to fold the entire Rev-5.3 brainstorm result into the plan in one Edit call; recovery required the orchestrator to splice the edits manually using `head + cat + tail` redirect against the raw plan file, then re-dispatch a follow-on TW agent for verification.

**How to apply**:
1. When dispatching a TW agent for a large section insertion (>200 lines), instruct the agent to split into multiple sequential `Edit` calls (≤200 lines each) anchored on stable surrounding context.
2. As a fallback for content moves where Edit splitting is impractical, use a bash heredoc + sed splice pattern (e.g., `head -n N file > tmp && cat new-section >> tmp && tail -n +N+1 file >> tmp && mv tmp file`) executed by the orchestrator directly, then re-dispatch TW for verification.
3. Watch for the "agent unresponsive after ~10 min" signature — that is almost always this pattern.
4. If the agent has stalled, do NOT kill-and-retry blindly; the partial edit may be on disk. Run `git diff` first; if dirty, salvage what's complete and resume from the last clean cut.
5. Pattern recovered in: Rev-5.3 plan-fold (`17fa79d82`); the same pattern was observed but unreported in earlier Rev-5.2 fold attempts.

## Related memory

- `feedback_specialized_agents_per_task.md` — companion: orchestrator verifies agent output, never authors
- `project_concurrent_agent_filesystem_interleaving.md` — sister operational caveat
- `feedback_implementation_review_agents.md` — TW is part of the spec-review trio (not implementation review)
