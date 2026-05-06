---
name: Compact-survival snapshot 2026-04-28 (Pair D Phase 1 in flight)
description: SUPERSEDED 2026-04-28 PM late evening by project_pair_d_phase2_pass — Pair D verdict closed PASS; this snapshot retained as historical Phase-1-in-flight record. Branch HEAD `f4a6761db` is PRE-Phase-1-results; current HEAD past Phase 3 closure.
type: project
originSessionId: d1cfac41-85eb-4cae-ae40-bddd97fffc23
---

**SUPERSEDED-BY:** `project_pair_d_phase2_pass.md` — Pair D simple-β empirical validation closed 2026-04-28 PM late evening with verdict **PASS**. This snapshot preserved for historical Phase-1-in-flight context. The HEAD reference below (`f4a6761db`) reflects the spec v1.1 pin commit BEFORE Phase 1 panel commit, BEFORE Phase 2 script execution, BEFORE Phase 3 3-way review, and BEFORE Option-β notebook re-execution. For current branch state, see `project_pair_d_phase2_pass`.

---

**[ORIGINAL CONTENT BELOW — DO NOT TREAT AS CURRENT TRUTH]**

**Branch state:** `phase0-vb-mvp`, HEAD `f4a6761db` (spec v1.1 pin commit). Recent commit chain:
- `f4a6761db` spec(abrigo): pin simple-β Pair D spec v1.1 sha256, integrate v1 verifier findings
- `10464763b` plan(abrigo): simple-β Pair D — empirical validation of Colombian BPO trap
- `33727eaa7` docs(abrigo): commit Pair D + GEIH feasibility result + escalation pre-pin
- `3c110e513` docs(abrigo): narrow target to Colombian BPO workers + ideal-scenario clause
- `34e500eb7` docs(abrigo): pin P1 spec sha256, park slow-lane, refocus to fast-lane simple-β
- `e4f09622f` docs(abrigo): add P1 plan — SN18 Cortex.t alpha event study
- `70606f4c9` docs(abrigo): add (Y, M, X) operating framework + retire Mento-only constraint

**Active iteration — Pair D (committed):**
- Y = Colombian young-worker (14-28, Ley 1622/2013) services-sector employment share (DANE GEIH monthly, CIIU Rev.4 A.C. G-T broad services primary + J+M+N narrow sensitivity, logit-transformed for bounded [0.55, 0.75])
- X = COP/USD lagged 6-12 months (closed FX-vol-CPI Phase-A.0 pipeline)
- Sign expectation pre-pinned positive (Baumol → US-Colombia wage arbitrage → offshoring transmission, lit-grounded via Mendieta-Muñoz 2017 + Beerepoot-Hendriks 2013)
- Test: one-sided H₁ (composite β > 0), α=0.05; methodology-break empalme primary + 2021-dummy R1; restrict-≥2022 BANNED
- ESCALATE numerics pre-pinned: Clause B `|β̂|/SE < 0.5` AND (`|skew| > 1.0` OR `excess kurtosis > 3.0`); ESCALATE-PASS disjunction `quantile β̂(0.90) > 0 OR GARCH-X mean-β > 0 OR EVT extreme-quantile β̂ > 0` at p ≤ 0.10 one-sided

**Spec sha256 (Pair D simple-β):** `f74b2ac577d5182842116a8798f307a610c185f1e6e259b8530e2ec266141728`
- File: `docs/specs/2026-04-27-simple-beta-pair-d-design.md`
- Computed against file with `decision_hash` = sentinel `<to-be-pinned-after-Task-0.3>`; re-verify by replacing pinned hash with sentinel + recomputing
- Spec v1 → v1.1 (RC + MQS-fresh both PASS-WITH-REV; ZERO BLOCKERs at any wave; MQS noted spec author "NOT sloppy")

**Plan (Pair D simple-β):** `docs/plans/2026-04-27-simple-beta-pair-d-implementation.md` — 407 lines, 4 phases / 9 tasks. v1 → v2 → v2.1 with 3 verifier waves (RC + SPM both PASS-WITH-REV); ZERO BLOCKERs at v2/v2.1.

**Phase 0 status:** COMPLETE. Spec sha256-pinned + committed.

**Phase 1 status:** IN FLIGHT (parallel DE dispatches, background):
- Task 1.1 GEIH Y construction: agent `a24ac0381c46fae4f` (Step 0 schema-stability pre-flight — handles CIIU Rev.3.1→Rev.4 boundary at 2012-01 + Marco-2005→Marco-2018 boundary at 2021; then ~218 monthly GEIH micro-data pulls + Y_broad + Y_narrow construction with empalme + RC self-verify spot-check)
- Task 1.2 COP/USD panel: agent `a1b25a866f3f5026d` (reuses closed FX-vol-CPI pipeline; daily→monthly aggregation; lag panel k ∈ {6, 9, 12})

**Phase 1 next action (after both DEs DONE):** Task 1.3 sequential alignment + N verification (HALT-disposition with typed exception `PairDSampleStructurallyPathological` if N < 75 per spec §3.6) + RC QC + commit data directory.

**Slow lane:** SN18 P1 PARKED at spec sha256 `f855e036d3c7807e2bef414a91a806caec1279a9d83575020bc2b3e82b47aeab` (committed at `34e500eb7`). May reactivate as second instrument family if Pair D track succeeds.

**Pending decisions:** (1) v2 doc-verification policy still paused (Task #12); (2) M framework-scope A/B/C — MOOT under ideal-scenario clause until M-sketch graduates to deployment.

**Anti-fishing invariants carried forward:** N_MIN=75; α=0.05 one-sided; methodology-break empalme primary; restrict-≥2022 BANNED; ESCALATE numerics pre-pinned at spec authoring time; HALT protocol per `feedback_pathological_halt_anti_fishing_checkpoint` (typed exception → disposition memo with ≥3 pivot options → user surface → CORRECTIONS block → 3-way review).

**Key file paths for resume:**
- Spec: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/docs/specs/2026-04-27-simple-beta-pair-d-design.md`
- Plan: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/docs/plans/2026-04-27-simple-beta-pair-d-implementation.md`
- BPO research: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-27-colombian-bpo-non-industrialization-hedge-research.md` (committed in worktree per RC O1 closure)
- GEIH feasibility: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-27-dane-geih-y-feasibility.md`
- Output dir (Phase 1 DEs writing here): `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/simple-beta-pair-d/`
- Worktree CLAUDE.md: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/CLAUDE.md` (Active iteration block lines ~148-172)

**Auto-mode active.** User confirmed Phase 1 dispatch with "yes do on auto mode"; agents running unattended.
