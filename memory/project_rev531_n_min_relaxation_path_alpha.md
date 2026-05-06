---
name: Rev-5.3.1 N_MIN relaxation 80→75 (path α from pathological-HALT)
description: Rev-5.3.1 relaxed N_MIN from 80 to 75 in response to documented pathological-HALT (basket-aggregate=77 non-zero weeks); preserved POWER_MIN ≥ 0.80 at relaxed N
type: project
originSessionId: phase0-vb-mvp / Rev-5.3.1 Task 11.N.2c CORRECTIONS-Rev-2
---

**Fact**: The Rev-5.3.1 plan revision (commit `7afcd2ad6`) relaxed `N_MIN` from 80 to 75 as user-approved path α from the Rev-5.3 pathological-HALT verdict (commit `13cfe5f56`). Carbon-basket aggregate `carbon_basket_user_volume_usd` had 77 weekly non-zero observations across the 82-Friday panel (2024-08-30 → 2026-04-03), failing the original N_MIN=80 by 3 weeks. Under relaxed N_MIN=75 with all other thresholds unchanged: gate result 77 ≥ 75 ⇒ PASS; `required_power(75, 13, 0.40) = 0.8638 ≥ POWER_MIN = 0.80`; `MDES_FORMULATION_HASH` integrity preserved.

**Why**: this is the canonical pattern for thresholds-vs-empirics tension under the anti-fishing regime. The pre-committed `N_MIN = 80` was empirically infeasible (basket-wide event sparsity), but the alternative thresholds (POWER_MIN ≥ 0.80, MDES_SD = 0.40, MDES_FORMULATION_HASH) all survive the relaxation — meaning the load-bearing scientific guarantees still hold at N=75. Path α was selected over alternatives (b) X-source abandonment, (c) basket-boundary loosening (banned mid-stream), (d) panel-extension waiting, (e) Y-pivot — because path α minimally perturbs the architecture while satisfying anti-fishing discipline through the CORRECTIONS-block process.

**How to apply**:
1. Pattern for future thresholds-vs-empirics tension: pathological-HALT → disposition memo enumerating pivot options → user picks → CORRECTIONS-block discipline → 3-way review post-hoc audit. Never silently re-tune to pass.
2. Rev-5.3.1 anchors:
   - HALT verdict: commit `13cfe5f56`, memo `contracts/.scratch/2026-04-24-carbon-xd-pathological-disposition.md`.
   - Relaxation: commit `7afcd2ad6`, memo `contracts/.scratch/2026-04-25-carbon-basket-calibration-result-rev2.md`.
   - Source change: `contracts/scripts/carbon_calibration.py` line 109+ (`Final[int] = 75` + 8-line docstring rationale).
   - Test: `contracts/scripts/tests/inequality/test_carbon_calibration.py` line 71+ (`test_n_min_is_75`).
3. The PCA cross-validation diagnostic showed COPM loads at -0.3010 on PC1 (idiosyncratic vs |loading| ≥ 0.40 floor) — informational only, does NOT change primary X_d which remains basket-aggregate per design doc §1, §4.
4. POWER_MIN, MDES_SD, MDES_FORMULATION_HASH, PC1_LOADING_FLOOR are unchanged from Rev-5.3 — the relaxation was strictly N_MIN-only.

## Related memory

- `feedback_pathological_halt_anti_fishing_checkpoint.md` — process pattern
- `project_mdes_formulation_pin.md` — pinned anchors that survived the relaxation
- `project_y3_inequality_differential_design.md` — downstream Y₃ work unblocked by this PASS verdict
