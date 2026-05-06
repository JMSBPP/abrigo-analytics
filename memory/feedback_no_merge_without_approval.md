---
name: No code merged without explicit user approval
description: NON-NEGOTIABLE — competing agent implementations stay in worktrees until user reviews and approves the winner for merge
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**NON-NEGOTIABLE:** No code from any implementing agent is merged to the working branch until the user explicitly approves it.

**Flow:**
1. Agents implement in isolated git worktrees (their own branches)
2. Code Reviewer compares competing implementations
3. Results presented to user
4. User selects the winner
5. ONLY THEN is the winning branch merged

**Why:** User requires full control over what enters the codebase. Competing implementations mean multiple valid approaches exist — the user decides which ships.

**How to apply:** After agents complete their worktree work, NEVER auto-merge. Present the comparison, wait for explicit user approval ("merge A" / "go with B"), then merge.
