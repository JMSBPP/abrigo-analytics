---
name: MDES Cohen f² canonical formulation pin (sha256 anchor)
description: required_power(n,k,mdes_sd) source text is sha256-pinned; free-tuning MDES_SD upward to chase target power is anti-fishing-banned
type: project
originSessionId: phase0-vb-mvp / Rev-5.3 §0.3 + Rev-5.3.1 Task 11.N.2c
---

**Fact**: The pinned canonical formulation for `required_power(n_obs: int, k_regressors: int, mdes_sd: float, alpha: float = 0.10, df1: int = 6) -> float` (Cohen 1988 ch. 9, partial-F via `scipy.stats.ncf.ppf`) is sha256-pinned at `4940360dcd298738a1f7321c1573bc3aad01b8a4c5acbc546d0855276389cefa`. Pinned empirical values: `required_power(75, 13, 0.40) = 0.8638`; `required_power(77, 13, 0.40) = 0.8739`; `required_power(80, 13, 0.40) = 0.8877`. The `MDES_FORMULATION_HASH` constant in `contracts/scripts/carbon_calibration.py` is computed as `hashlib.sha256(inspect.getsource(required_power).encode("utf-8")).hexdigest()` at Step 0; modifying the function source (whitespace, docstring, df₁, α, body) invalidates the hash and HALTs the Step-0 test.

**Why**: during the Rev-5.3 final-fix-pass, RC's live-scipy reproduction across four standard formulations yielded {0.770, 0.989, 0.987, 0.888} — a 0.22 spread. Without a pinned formulation, the operative power figure could be free-tuned by selecting whichever formulation cleared `POWER_MIN ≥ 0.80` for whatever `MDES_SD` the analyst chose post-hoc. That is anti-fishing-banned per X_d design doc §1 ("Once primary X_d is chosen, downstream tasks consume it without re-selection; mid-stream re-tuning of the primary measure is banned"). The hash is the load-bearing tamper-evident anchor; the pinned formulation is the load-bearing scientific anchor.

**How to apply**:
1. Any change to `required_power()` in `contracts/scripts/carbon_calibration.py` requires (a) full design-doc revision; (b) CORRECTIONS block in next plan revision; (c) full 3-way review (CR + RC + Senior PM) before commit.
2. If `required_power(n, 13, 0.40)` drifts below `POWER_MIN = 0.80` due to data-driven `n` shrinkage, the correct response is HALT under `CalibrationStructurallyPathological`, NOT free-tuning `MDES_SD` upward to recover power.
3. The Rev-5.3.1 N_MIN relaxation 80 → 75 was permitted because the pinned `required_power(75, 13, 0.40) = 0.8638 ≥ 0.80` — power floor preserved, not power-target chased.
4. Source-text location: `contracts/scripts/carbon_calibration.py` (function + Final[str] hash constant); test file `contracts/scripts/tests/inequality/test_carbon_calibration.py` Step-0 block asserts hash byte-exact.
5. Plan reference: `docs/plans/2026-04-20-remittance-surprise-implementation.md` Task 11.N.2c CORRECTIONS block + §0.3 MDES formulation pin.

## Related memory

- `feedback_pathological_halt_anti_fishing_checkpoint.md` — companion process discipline
- `project_rev531_n_min_relaxation_path_alpha.md` — the post-HALT relaxation that exercised this anchor
- `feedback_no_code_in_specs_or_plans.md` — exception: tamper-evident hashes ARE pinned in source code, not specs
