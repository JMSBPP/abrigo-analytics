---
name: SaaS-builder Stage-2 — ACTIVE iteration
description: Parallel (Y, M, X) iteration registered 2026-05-07 — solo AI-native SaaS builders × COP/USD vol; Stage-2 idealized welfare model with Stage-1 empirical β deferred until professor data arrives
type: project
---

**Iteration ID.** `saas_builder_stage_2`
**Status.** ACTIVE — Stage-2 idealized welfare model in progress; Stage-1 DEFERRED.
**Kickoff.** 2026-05-07.

**(Y, M, X).**
- Population: Colombian solo AI-native SaaS builders (post-revenue, pre-scale; COP MRR + USD tooling cost).
- Y: per-builder profit/survival under FX shocks ($\Pi_t = \Upsilon_t - C_t$, perpetual rolling horizon).
- X: COP/USD spot, realized variance $\sigma_T$ over monthly rolling window.
- M: Panoptic CPO with $\sqrt{\sigma_T}$ payoff (PRIMITIVES.md §8.1), 12-leg IronCondor strip, streamed premium $\pi(t)$.

**Why:** Parallel alternative to Pair D Stage-2 (PASS, β=+0.137) and to the just-closed dev-AI Stage-1 (FAIL 2026-05-06, Section J β=-0.146 sign-flip). Different population, different Y; independent iteration in the framework. dev-AI failure raises required Stage-1 sign-prior strength but does not invalidate this iteration's hypothesis.

**How to apply:**
- Planning lives in `.planning/` (bespoke filenames, NOT GSD/superpowers conventions — see `feedback_planning_dir_bespoke_naming.md`).
- Source documents: `notes/SaaS_Builders_AI_NativeBuilders.md` + `notes/PRIMITIVES.md` (esp. §4.2, §8, §15).
- Methodology: A (CRRA welfare heatmap) + B (utility-indifference $\pi(t)$ + ratchet hitting time), additive on PRIMITIVES.md.
- Stage-1 is deferred; Stage-2 deliverables are PROVISIONAL until empirical β returns PASS.
- Anti-fishing pre-pins locked at kickoff in `.planning/04-anti-fishing-prepins.md`.

**Open threads** (see `.planning/02-open-threads.md`):
1. Basis risk source — proposed: joint of (per-user $\bar C$ deviation, stickiness mismatch, dollarization $\lambda$).
2. Sticky-cost form — proposed: run regimes (i) ratchet and (ii) linear pass-through separately.
3. Coping-benchmark structure — proposed: composite optimal-coping rep-agent (not three separate suboptimal benchmarks).
4. Horizon — proposed: monthly rolling $\sigma_T$, welfare at 12/36/60-mo.
5. Stage-1 deferral artifact — proposed: pre-pinned placeholder spec at `docs/specs/`.
6. Deliverable shape — proposed: Stage-2 spec + notebook trio.

**Cross-iteration relationships:**
- Independent of Pair D Stage-2 (different population/Y).
- Independent of dev-AI Stage-1 (different population/Y).
- Inherits PRIMITIVES.md scaffolding wholesale.
