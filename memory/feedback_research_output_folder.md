---
name: Default research output folder
description: Research agent reports go to contracts/.scratch/ in the active worktree, not the repo root .scratch/
type: feedback
originSessionId: e63ee238-733d-49df-8015-addce58e2ae7
---
Research agent output files should be written to `contracts/.scratch/` within the active worktree (e.g., `.worktree/ranFromAngstrom/contracts/.scratch/`), not to the repo root `.scratch/`.

**Why:** The user wants research artifacts colocated with the contracts they relate to, inside the worktree where work is happening.

**How to apply:** When launching background research agents, set the output path to `contracts/.scratch/<filename>.md` relative to the worktree root. For the ranFromAngstrom worktree, the full path is `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/`.
