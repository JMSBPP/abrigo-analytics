---
name: Competing agents cannot share a working directory
description: Parallel agents writing to same files in same dir will collide — use sequential execution or separate clones, not branch-based parallelism
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**Competing parallel agents DO NOT WORK in this project** due to:

1. `isolation: "worktree"` creates worktrees of the **Angstrom submodule**, not the parent project. The submodule doesn't have `contracts/scripts/`.
2. Branch-based parallelism (checkout different branches) fails because both agents share the **same working directory** — `git checkout` only changes the branch pointer, untracked files are shared.
3. Both agents write to the same `contracts/scripts/ran_utils.py` → last writer wins.

**What works instead:**
- **Sequential execution with stash/branch:** Agent A implements on branch-a, commits. Reset to base. Agent B implements on branch-b, commits. Compare branches.
- **Single agent per task** with 3-way review for quality assurance. This is the recommended approach given the submodule constraints.
- **Separate directory clones** would work but are heavy and impractical for this repo size.

**Why:** The thetaSwap-core-dev repo has Angstrom as a git submodule. The `.git` structure routes worktree creation to the submodule, not the parent project.

**How to apply:** Drop the competitive worktree strategy for this project. Use single-agent execution with the established 3-way review process.
