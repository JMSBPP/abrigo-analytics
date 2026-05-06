---
name: Phase-A.0 remittance execution state — CLOSED 2026-04-24 EXIT_NON_REMITTANCE
description: CLOSED 2026-04-24 with EXIT_NON_REMITTANCE verdict after Task 11.F Axis-1 found 0/30 peak-day remittance fingerprints. See project_phase_a0_exit_verdict.md for authoritative close-out. This file preserves pre-exit resume state for audit.
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---

**STATUS (2026-04-24): CLOSED — EXIT_NON_REMITTANCE.** See `project_phase_a0_exit_verdict.md` (authoritative close-out) and `scratch/2026-04-24-phase-a0-exit-disposition.md` (full disposition memo). The content below is preserved as historical execution state for audit trail only.

---

**Fact**: Phase-A.0 execution reached 13/46 tasks before EXIT (Task 11.F Axis-1 completed but 11.F Axes 2-5 were not needed — Axis-1 alone established k1). Branch `phase0-vb-mvp`, worktree `ranFromAngstrom`.

**Why**: Task 11.E dispatched 3 parallel spec reviewers (CR+RC+TW) against Rev-1.1.1 spec patch @ `ac5189363`; all 3 bailed immediately with "out of extra usage" error. Blocker is external (credit ceiling), not design or plan.

**How to apply (resume protocol)**: when a future agent picks up this thread (either post-compaction or post-credit-reset), re-dispatch the 3 Task 11.E reviewers with these exact parameters:

1. **Code Reviewer** against `docs/specs/2026-04-20-remittance-surprise-trm-rv-spec-rev1.md` with fix-log at `scratch/2026-04-20-remittance-spec-rev1.1.1-fix-log.md` as first-class input. CRITICAL audit: did Task 11.D correctly classify all 10 patches as wording-only? Scrutinize patches 4 (§4.1 scalar→6-channel), 5 (§4.4 t-test→joint-F-test), 6 (§4.5 MDES recomputation), 8 (§12 rows 5/6/7/8 supersedes). Plan line 368 says methodology-mechanism mis-classification triggers structural-econometrics skill re-invocation.

2. **Reality Checker** against same spec+fix-log. Audit: Task 11.C verdict citation (ρ=+0.7554, 2/5 sign, N=6, FAIL-BRIDGE); commit hashes `bc12e3c30`, `2bff6d79f`, `91e5d2664`; Dune `#7366593`; channel names match Task 11.B module; N_eff=78 vs smoke-test 84 reconciliation; MDES arithmetic; NBER w26323 + IMF OP 259 citations; anti-fishing claims.

3. **Technical Writer** against same spec+fix-log. Audit: §0 supersedes-banner clarity; §4.1 6-channel vector pedagogical introduction; §4.4 joint-F-test explanation in plain English; §12 row-status typography; narrative coherence; softening-modal-verb drift.

After all 3 land, TW consolidation. Rule 13 cycle-cap: 3 cycles max, 3 per-reviewer re-dispatches max, then escalate to user.

## Task-completion audit trail (committed on branch `phase0-vb-mvp`)

| Phase | Tasks | Commits |
|---|---|---|
| Phase 0 | T1-T5 | `e71044ce0` → `9a5432d3a` |
| Phase 1 | T6-T10 | `666ba7da3` · `70ceeb8b2`+`a1cffcea0`+`50052af80` · `b23908067`+`63de65863` · `28d76cbb0` · `93b8529bd` |
| Phase 2a | T11 | `939df12e1` (DONE_WITH_CONCERNS — BanRep quarterly-only finding) |
| Phase 1.5 | T11.A-D | `bc12e3c30` · `2bff6d79f` · `91e5d2664` · `ac5189363` |
| Plan revs | Rev-2 → Rev-3.4 | `a87d096d8` → `6034b360f` → `d7dfc4390` → `a8085d2b5` → `fef5c821c` → `4a70bb726` → `726ce8f74` |

## Critical empirical findings landed

1. **Task 11 BanRep-only finding**: BanRep publishes remittance at QUARTERLY cadence only (grounded on suameca series 4150; 104 real quarterly rows 2000-Q1 → 2025-Q4; no monthly public feed). Invalidated Rev-1 §§4.6/4.7/4.8 monthly-cadence primary.

2. **Task 11.C FAIL-BRIDGE verdict (FIRST empirical signal, anti-fishing-verified)**:
   - ρ = +0.7554 (N=6; robustness N=5 excluding 2024-Q3 partial = +0.7069)
   - Sign-concordance = 2/5 quarter-over-quarter transitions (below majority threshold 3/5)
   - Gate verdict: FAIL-BRIDGE via OR-clause second disjunct (ρ PASSes left conjunct but 2/5 sign fails the AND)
   - Interpretation: on-chain COPM+cCOP rail tracks BanRep SECULAR TREND at quarterly LEVELS (ρ=0.76) but quarterly DELTAS don't co-move. On-chain rail is ~0.86% of BanRep aggregate.
   - Narrative shift: primary X reinterpreted from "remittance surprise" to "crypto-rail income-conversion surprise" per Rev-3.1 recovery protocol.

3. **Rev-1.1.1 primary redefinition (Task 11.D, wording-only per decision gate)**:
   - Primary X: 6-channel weekly rich-aggregation vector (Task 11.B output — flow_sum, flow_var, flow_concentration, flow_directional_asymmetry, unique_daily_active_senders, flow_max_single_day).
   - Primary gate: joint F-test at df₁=6, df₂=N_eff-13, α=0.10 (was scalar t-test).
   - N_eff conservative floor: 78 weekly obs (was 200 in Rev-1).
   - MDES_R² ≈ 0.143 / MDES ≈ 0.41 SD joint (was 0.20 SD scalar).
   - BanRep quarterly demoted to S14 sensitivity/validation row (N=6-7, not gate-relevant).

## Paper deep-reads (already on disk)

- `scratch/2026-04-20-nber-w26323-deep-read.md` — DGK 2019 fn 23 defends AR(1) surprise on admin aggregates
- `scratch/2026-04-20-imf-op259-deep-read.md` — Chami et al. 2008; reverse-causation motivates "predictive, not causal" caveat; REER vs TRM sign footnote

## Open gaps (pre-reset)

- Basco-Ojeda-Joya BdE 1273 citation still a placeholder; neither paper closed it
- N_eff=78 is a CONSERVATIVE FLOOR; actual Task-11.B smoke-test produced 84; spec-patch Rev-1.1.1 uses 78 for pre-commitment honesty
- 2/9 Task 9 deferred-stub tests (NotImplementedError) intentionally fail pending Task 12

## Plan location

`docs/plans/2026-04-20-remittance-surprise-implementation.md` @ `726ce8f74` (Rev-3.4). 46 tasks across 6 phase-labels (0, 1, 2a, 1.5, 2b, 3, 4).

## Memory cross-refs

- `project_colombia_yx_matrix.md` — Y×X matrix exploration that selected A1 remittance-surprise as primary
- `project_fx_vol_cpi_notebook_complete.md` — Rev-4 CPI exercise (FAIL verdict, shipped 2026-04-19)
- `feedback_three_way_review.md`, `feedback_no_code_in_specs_or_plans.md`, `feedback_specialized_agents_per_task.md` — core process rules

## Resume command for future agent

Read this file first. Then read MEMORY.md for active rules. Then `git log --oneline -25` on `phase0-vb-mvp` to confirm commit trail. Then re-dispatch the 3 Task 11.E reviewers (details above).
