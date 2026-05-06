---
name: Angstrom code is READ-ONLY -- we cannot modify it
description: The ranFromAngstrom worktree forks Angstrom for integration but we CANNOT modify Angstrom's core contracts. We can only read from them (extsload) and build on top.
type: project
originSessionId: e63ee238-733d-49df-8015-addce58e2ae7
---
The ranFromAngstrom worktree is a fork of Angstrom for integration purposes. We CANNOT modify Angstrom's core contracts (GrowthOutsideUpdater, PoolUpdates, TopLevelAuth, etc.). We can only READ from Angstrom's storage via extsload and build our own contracts on top.

**Why:** The goal is to integrate with Angstrom, not fork and diverge. Angstrom's code stays upstream-compatible.

**How to apply:** When designing features that need data from Angstrom's reward distribution, ALWAYS use external reader patterns (extsload via the adapter). Never propose modifying GrowthOutsideUpdater, PoolUpdates, or any Angstrom contract. Option A (active observer) or Option B (lazy observer) patterns, never Option C (hook-based modification).
