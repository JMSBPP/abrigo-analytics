# STOCHASTIC-FX VARIANT — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Code-agnostic plan.** Per repo memory `memory/feedback_no_code_in_specs_or_plans.md` (NON-NEGOTIABLE), this plan does NOT contain Python code blocks. Each task dispatches a specialized agent who authors code per the functional-python skill + the Honnibal audit-pass chain.
>
> **Foreground orchestrates, never authors.** Per repo memory `memory/feedback_specialized_agents_per_task.md` (NON-NEGOTIABLE).

**Plan version:** v0.1 (initial draft — awaiting Wave-1 RC + MQ review per master-spec §6.1)
**Parent spec:** `docs/specs/2026-05-11-stochastic-fx-variant-design.md` v0.3 (Wave-1 ACCEPT_WITH_FLAGS-DISPOSED)
**Predecessor:** `simulations/saas_builder/cohort_5_strip/` (commit `3442852`, audit `94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329` — PRESERVED unchanged per Pin Z1.6)
**Status:** DRAFT — Wave-1 review dispatch pending
**Estimated wall-time:** 5–7 days of focused work

---

## §0 Goal

**One sentence.** Build the `simulations/stochastic_fx/` package per the spec v0.3 architecture: three SDE families (GBM, OU, Merton jump-diffusion) with the three-phase per-family verification pipeline (Phase A algebraic inversion / Phase B moment match against hand-derived analytic moments / Phase C KS goodness-of-fit against moment-matched parametric reference), preserving the cohort_5_strip strip-emit invariant.

## §1 Architecture

Three-tier discipline mirroring cohort_5_strip. Package is INDEPENDENT of all first-wave Stage-3 tracks; READ-ONLY consumer of `notes/PRIMITIVES.md` and reuse of `simulations.saas_builder.cohort_4.types::NUMERICAL_IDENTITY_TOL`. Strip preservation invariant (Pin Z1.6) means no cohort_5_strip file is touched.

Hand-derived analytic moments per family (Hull §15 for GBM; standard OU; Andersen-Piterbarg Vol I §2.7 for Merton) live as both Python expressions in `moments.py` AND `.tex` fragments rendered via `sympy.latex(...)` under `notes/stochastic_fx_tex/`. The `.tex` fragments are the integration hook for the future LaTeX-econ-paper consolidator (spec §7.2).

## §2 Tech stack

- Python 3.13, functional-python skill (frozen-dc / free fns / IO Boundary tier).
- NumPy for path generation (`numpy.random.default_rng` for deterministic RNG).
- SciPy for the KS test (`scipy.stats.ks_1samp`) and reference-distribution fits (`scipy.stats.lognorm.fit`, `scipy.stats.gamma.fit`).
- Sympy for algebraic simplification + LaTeX rendering (NOT Itô calculus).
- Hypothesis for property tests on path-distribution invariants and RNG determinism.
- Existing `simulations/utils/{parquet_io.py, json_io.py, audit_block.py}` patterns for emit.

---

## §3 Cross-spec references

| Spec section | This plan's coverage |
|---|---|
| §3 Components — `_errors.py` | Task 1.1 |
| §3 Components — `types.py` | Tasks 1.2 (Parameters frozen-dc per family), 1.3 (PathEnsemble + InversionVerdict) |
| §3 Components — `moments.py` | Task 2.1 (GBM + OU + Merton hand-derived moments + LaTeX rendering) |
| §3 Components — `generators.py` | Tasks 3.1 (GBM), 3.2 (OU), 3.3 (Merton) |
| §3 Components — `variance_proxy.py` | Task 4.1 |
| §3 Components — InversionVerifier (combines Phase A/B/C) | Task 4.2 |
| §3 Components — `emit.py` | Task 5 |
| §3 tests/ | Each task has its own test sub-step; Task 6 runs end-to-end gates |
| §4.1 Phase A (Pin Z1.3a algebraic) | Task 4.1 |
| §4.1 Phase B (Pin Z1.3b moment match) | Task 4.2 |
| §4.1 Phase C (Pin Z1.4 KS test) | Task 4.2 |
| §4.2 Per-family parameter pin table | Task 1.2 (constants); Task 6 (verification) |
| §5 Pin Z1.6 (strip preservation) | Task 7 |
| §11.2 outstanding repo work | Task 0 (gitignore line) |

---

## §4 File structure

```
docs/plans/2026-05-11-stochastic-fx-variant.md          ← THIS plan
scratch/2026-05-11-stochastic-fx-execution/
├── moment_verification_log.md         Task 6 record of per-family Phase B verdicts
├── ks_test_log.md                     Task 6 record of per-family Phase C verdicts
└── pin_z16_strip_preservation_log.md  Task 7 record of audit_block hex grep verdict

.gitignore                              MODIFY (Task 0)

simulations/stochastic_fx/              NEW package
├── __init__.py                         Public API re-exports (Task 1.1 final)
├── _errors.py                          Task 1.1
├── types.py                            Task 1.2 + 1.3
├── moments.py                          Task 2.1
├── generators.py                       Tasks 3.1 + 3.2 + 3.3
├── variance_proxy.py                   Task 4.1 + 4.2
└── emit.py                             Task 5

notes/stochastic_fx_tex/                NEW directory (Task 5)
├── eps_inversion.tex                   Single fragment — eq. (8) algebraic form (family-agnostic)
├── sigma_t_moments_gbm.tex             GBM moments (Hull §15 anchor)
├── sigma_t_moments_ou.tex              OU stationary moments
└── sigma_t_moments_merton.tex          Merton jump-diffusion moments (Andersen-Piterbarg Vol I §2.7)

notes/STOCHASTIC_FX_RESULTS.md          NEW (Task 6) — parallel to STAGE_2_RESULTS.md

simulations/stochastic_fx/data/         NEW gitignored directory (per Task 0)
├── path_ensemble_gbm.parquet           emitted; gitignored
├── path_ensemble_ou.parquet            emitted; gitignored
├── path_ensemble_merton.parquet        emitted; gitignored
├── inversion_verdict_gbm.json          emitted; gitignored
├── inversion_verdict_ou.json           emitted; gitignored
└── inversion_verdict_merton.json       emitted; gitignored

simulations/tests/test_saas_stochastic_fx.py   NEW (tests under each task; final integration in Task 6)
```

---

## §5 Phase 0 — Repo infrastructure

### Task 0 — Add gitignore line for new emit directory

**Files:**
- Modify: `.gitignore` (add `simulations/stochastic_fx/data/` per spec v0.3 §11.2 outstanding repo work)

**Agent dispatch:** N/A — orchestrator-only operation (single-line gitignore edit per `memory/feedback_specialized_agents_per_task.md` shell-ops exception).

**Acceptance:**
- `.gitignore` now contains a line `simulations/stochastic_fx/data/` (alphabetically near existing line 53's `simulations/saas_builder/data/`).
- `git check-ignore simulations/stochastic_fx/data/anything.parquet` returns the path (gitignored).

**Commit message:** `chore(gitignore): add simulations/stochastic_fx/data/ per stochastic-fx-variant spec v0.3 §11.2`

---

## §6 Phase 1 — Value tier (types + errors)

### Task 1.1 — Author `_errors.py` + initial `__init__.py`

**Files:**
- Create: `simulations/stochastic_fx/__init__.py`
- Create: `simulations/stochastic_fx/_errors.py`

**Agent dispatch:** `Senior Developer` (Value-tier exception authoring per `memory/feedback_specialized_agents_per_task.md`).

**Acceptance:**
- `_errors.py` exports `StochasticFXError(Exception)` base + `SDEParameterError(StochasticFXError)` + `InversionTestFailedError(StochasticFXError)` + `MomentMatchFailedError(StochasticFXError)` + `MCBudgetExceededError(StochasticFXError)`. Mirrors `simulations/saas_builder/cohort_4/_errors.py` style.
- `__init__.py` is a minimal stub re-exporting the four exceptions. Full public API re-exports get appended as tasks land.
- One unit test in `simulations/tests/test_saas_stochastic_fx.py` confirms exception inheritance chain via `issubclass`.

**Commit message:** `feat(stochastic_fx): _errors.py + __init__.py stub`

---

### Task 1.2 — Author per-family Parameters Value types

**Files:**
- Create: `simulations/stochastic_fx/types.py` (initial — Parameters types only; PathEnsemble + InversionVerdict added in Task 1.3)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export Parameters types)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add Parameters tests)

**Agent dispatch:** `Senior Developer`.

**Acceptance:**
- Three frozen-dataclass Parameters types:
  - `GBMParameters(mu: float, sigma: float, x_0: float, T: float, dt: float, n_steps: int)` with `__post_init__` validating `sigma > 0; x_0 > 0; T > 0; dt > 0; n_steps >= 2; n_steps * dt == T` within float tolerance.
  - `OUParameters(theta: float, mu_bar: float, sigma: float, x_0: float, T: float, dt: float, n_steps: int)` validating `theta > 0; sigma > 0; mu_bar > 0; x_0 > 0; T > 0; dt > 0; n_steps >= 2`.
  - `JumpDiffusionParameters(mu: float, sigma: float, lambda_jump: float, jump_mean: float, jump_std: float, x_0: float, T: float, dt: float, n_steps: int)` validating `sigma > 0; lambda_jump >= 0; jump_std > 0; x_0 > 0; T > 0; dt > 0; n_steps >= 2`.
- Module-level canonical-pin constants per spec v0.3 §4.2 table:
  - `CANONICAL_GBM = GBMParameters(mu=0.0, sigma=0.10/sqrt(12), x_0=4000.0, T=12.0, dt=12.0/5000, n_steps=5000)`.
  - `CANONICAL_OU = OUParameters(theta=1.0, mu_bar=4000.0, sigma=0.10 * 4000.0 / sqrt(2.0 * 1.0), x_0=4000.0, T=12.0, dt=12.0/5000, n_steps=5000)`.
  - `CANONICAL_MERTON = JumpDiffusionParameters(mu=0.0, sigma=0.05/sqrt(12), lambda_jump=1.0, jump_mean=0.0, jump_std=0.10, x_0=4000.0, T=12.0, dt=12.0/5000, n_steps=5000)`.
- One Hypothesis property test per family checking `__post_init__` rejects invalid parameters (zero / negative volatility; n_steps < 2; etc.) AND accepts the canonical pins.
- ruff + ty clean on `simulations/stochastic_fx/`.

**Commit message:** `feat(stochastic_fx/types): per-family Parameters + canonical pins`

---

### Task 1.3 — Author `PathEnsemble` + `InversionVerdict` Value types

**Files:**
- Modify: `simulations/stochastic_fx/types.py` (append the two new Value types)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add validation tests)

**Agent dispatch:** `Senior Developer`.

**Acceptance:**
- `PathEnsemble` frozen-dc with fields: `family_id: Literal["gbm", "ou", "merton"]`, `paths: NDArray[(N, n_steps+1)]`, `sigma_t_per_path: NDArray[(N,)]`, `parameters_canonical_json: str`, `rng_seed: int`, `audit_block: str` (64-char hex). `__post_init__` validates: paths is 2D; sigma_t shape matches paths.shape[0]; audit_block is 64-char lowercase hex; family_id in the closed set.
- `InversionVerdict` frozen-dc with fields: `family_id`, `phase_a_passes: bool` (Z1.3a), `phase_a_max_residual: float`, `phase_b_passes: bool` (Z1.3b), `phase_b_mean_relative_error: float`, `phase_b_var_relative_error: float`, `phase_c_passes: bool` (Z1.4), `phase_c_ks_pvalue: float`, `phase_c_n_paths: int`, `passes: bool`, `tex_anchor: str`, `audit_block: str`. `__post_init__` validates: bool fields are bool; `passes == phase_a AND phase_b AND phase_c`; tolerances numerically reasonable.
- One Hypothesis property test per type confirming `__post_init__` rejects invalid combinations.
- ruff + ty clean.

**Commit message:** `feat(stochastic_fx/types): PathEnsemble + InversionVerdict`

---

## §7 Phase 2 — Hand-derived analytic moments + LaTeX fragments

### Task 2.1 — Author `moments.py` with per-family E[σ_T] and Var[σ_T]

**Files:**
- Create: `simulations/stochastic_fx/moments.py`
- Create: `notes/stochastic_fx_tex/sigma_t_moments_gbm.tex`
- Create: `notes/stochastic_fx_tex/sigma_t_moments_ou.tex`
- Create: `notes/stochastic_fx_tex/sigma_t_moments_merton.tex`
- Create: `notes/stochastic_fx_tex/eps_inversion.tex`
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add per-family moment tests)

**Agent dispatch:** `AI Engineer` (math-heavy; coordinates with sympy) + inline `Reality Checker` cross-check that the implemented Python expressions match the hand-derived formulas in spec v0.3 §4.2 verbatim.

**Acceptance:**
- Three free functions in `moments.py`, one per family, returning a `(e_sigma_t: float, var_sigma_t: float)` tuple given the Parameters frozen-dc:
  - `gbm_moments(params: GBMParameters) -> (float, float)` — exact form `E[σ_T] = params.x_0**2 * ((exp(params.sigma**2 * params.T) - 1) / (params.sigma**2 * params.T) - 1)`. Var[σ_T] form per Hull §15 (hand-derived leading order; rendered exactly in the `.tex` fragment).
  - `ou_moments(params: OUParameters) -> (float, float)` — exact `E[σ_T] = params.sigma**2 / (2 * params.theta)`. Var[σ_T] = `2 * params.sigma**4 / ((2 * params.theta)**2 * params.T)` (leading order under chi-squared approximation).
  - `merton_moments(params: JumpDiffusionParameters) -> (float, float)` — exact form per spec §4.2 Merton row.
- Numerical sanity test per family: at canonical pins (Task 1.2 CANONICAL_*), values match hand-computed analytic numbers within 1e-12.
- LaTeX-fragment emission via `sympy.latex(...)` for each family's moment expressions; saved to `notes/stochastic_fx_tex/sigma_t_moments_{family}.tex`. Each fragment contains:
  - The exact-form LaTeX (e.g., for GBM: `E[\sigma_T] = (\bar X/\bar Y)^2 \cdot \left[ \frac{e^{\sigma^2 T} - 1}{\sigma^2 T} - 1 \right]`).
  - Literature citation as a `\cite{}` or inline comment.
  - Numerical-pin example at the canonical fixture.
- Also write the family-agnostic eq. (8) algebraic inversion LaTeX to `notes/stochastic_fx_tex/eps_inversion.tex` (single one-line fragment).
- Hypothesis property tests: monotonicity of `E[σ_T]` in `params.sigma` per family; bounds checks (E ≥ 0, Var ≥ 0).
- ruff + ty clean.

**Commit message:** `feat(stochastic_fx/moments): per-family E[σ_T] + Var[σ_T] + LaTeX fragments`

---

## §8 Phase 3 — SDE path generators

### Task 3.1 — Author `GBMPathGenerator`

**Files:**
- Create: `simulations/stochastic_fx/generators.py` (initial — GBM only; OU + Merton added in 3.2 + 3.3)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add GBM generator tests)

**Agent dispatch:** `Senior Developer` + `AI Engineer` (paired — Senior Developer for the three-tier scaffolding; AI Engineer for the SDE discretization scheme).

**Acceptance:**
- `GBMPathGenerator(params: GBMParameters)` frozen-dc with `__call__(rng_seed: int, n_paths: int) -> PathEnsemble`. Uses `numpy.random.default_rng(rng_seed)` for reproducibility per Pin Z1.2.
- Discretization scheme: Euler-Maruyama on log-scale. For each path: `X_{t+dt} = X_t * exp((mu - sigma^2/2) * dt + sigma * sqrt(dt) * Z_t)` where `Z_t ~ N(0, 1)`.
- σ_T computed per path via PRIMITIVES.md §6 eq. (7) discretely: `sigma_t = (1/T) * sum_{i=0..n_steps} (path[i] - mean(path))**2`. Matches B1 plan's σ_T contract per MQ-FLAG-B1.1 disposition.
- audit_block deterministic from `(params canonical JSON, rng_seed, paths bytes)`.
- Hypothesis property tests:
  - Determinism (Pin Z1.2): same `(rng_seed, n_paths)` → bit-exact `audit_block`.
  - Lognormality: at large `n_steps` and `T=1`, `log(path[..., -1] / x_0)` is approximately normal with mean `(mu - sigma^2/2) * T` and variance `sigma^2 * T`. Use Hypothesis with a Normality goodness-of-fit check (Anderson-Darling) at N=1000.
  - Trivial-degenerate limit: at `params.sigma == 1e-8` (effectively 0), all paths collapse near `x_0` and `sigma_t_per_path` mean is `< 1e-6`.
- ruff + ty clean.

**Commit message:** `feat(stochastic_fx/generators): GBMPathGenerator`

---

### Task 3.2 — Author `OUPathGenerator`

**Files:**
- Modify: `simulations/stochastic_fx/generators.py` (append)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add OU tests)

**Agent dispatch:** `Senior Developer` + `AI Engineer`.

**Acceptance:**
- `OUPathGenerator(params: OUParameters)` frozen-dc with `__call__(rng_seed, n_paths) -> PathEnsemble`.
- Discretization: exact transition `X_{t+dt} = mu_bar + (X_t - mu_bar) * exp(-theta * dt) + sigma * sqrt((1 - exp(-2*theta*dt))/(2*theta)) * Z_t`.
- Hypothesis property tests:
  - Mean reversion: at long T and large theta, `mean(path[..., -1])` is close to `mu_bar`.
  - Determinism (Pin Z1.2).
  - Trivial-degenerate limit at `params.theta = 1e8` (effectively instant mean reversion): paths collapse near `mu_bar` and `sigma_t_per_path` mean is `< 1e-3`.
  - Trivial-degenerate limit at `params.sigma = 1e-8`: `sigma_t_per_path` mean `< 1e-6`.

**Commit message:** `feat(stochastic_fx/generators): OUPathGenerator`

---

### Task 3.3 — Author `JumpDiffusionPathGenerator`

**Files:**
- Modify: `simulations/stochastic_fx/generators.py` (append)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add Merton tests)

**Agent dispatch:** `Senior Developer` + `AI Engineer`.

**Acceptance:**
- `JumpDiffusionPathGenerator(params: JumpDiffusionParameters)` frozen-dc with `__call__(rng_seed, n_paths) -> PathEnsemble`.
- Discretization: Euler-Maruyama (per Task 3.1) augmented by compound-Poisson jumps. For each path step: (i) sample number of jumps `N ~ Poisson(lambda_jump * dt)`; (ii) sample N jump sizes from `lognormal(jump_mean, jump_std)`; (iii) multiplicative jump aggregation `X_{t+dt} = X_{t+dt}^{diffusion} * prod(jump_sizes)`.
- Hypothesis property tests:
  - Determinism (Pin Z1.2).
  - Trivial-degenerate limit at `params.sigma = 1e-8 AND params.lambda_jump = 0`: paths collapse near `x_0`; `sigma_t_per_path` mean `< 1e-6`.
  - At `lambda_jump = 0`, JumpDiffusionPathGenerator output statistically matches GBMPathGenerator output (Kolmogorov-Smirnov agreement on terminal-spot distributions at the same N, same rng_seed).

**Commit message:** `feat(stochastic_fx/generators): JumpDiffusionPathGenerator`

---

## §9 Phase 4 — Variance proxy + Inversion verifier

### Task 4.1 — Author `variance_proxy.py` (Phase A algebraic inversion)

**Files:**
- Create: `simulations/stochastic_fx/variance_proxy.py`
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add variance-proxy tests)

**Agent dispatch:** `Senior Developer`.

**Acceptance:**
- Free function `compute_sigma_t_per_path(ensemble: PathEnsemble) -> NDArray` that re-applies PRIMITIVES.md §6 eq. (7) to the ensemble's paths and returns the per-path realised variance array. Verifies the σ_T values stored on the ensemble match the computation within `NUMERICAL_IDENTITY_TOL = 1e-6` (reused from `simulations.saas_builder.cohort_4.types::NUMERICAL_IDENTITY_TOL`).
- Free function `apply_inversion(sigma_t: float, x_bar: float) -> float` implementing PRIMITIVES.md §6 eq. (8) algebraically: `eps = sqrt(8 * sigma_t / x_bar**2)`.
- Free function `verify_phase_a(ensemble: PathEnsemble, x_bar: float) -> (passes: bool, max_residual: float)` implementing Pin Z1.3a: for each path's σ_T_n, verify `apply_inversion(sigma_t_n, x_bar)**2 == 8 * sigma_t_n / x_bar**2` to float64 precision. Compute the max absolute residual across the N paths. PASS iff max residual ≤ `NUMERICAL_IDENTITY_TOL`.
- Unit test: at canonical fixture (`x_bar = 4000`, sigma_t = 20000), `apply_inversion` returns exactly `0.1`.
- Property test (Hypothesis): for any valid `(sigma_t > 0, x_bar > 0)`, `apply_inversion(sigma_t, x_bar)` is finite, non-negative, and `apply_inversion(0, x_bar) == 0` (trivial-degenerate-limit Pin Z1.3a).
- ruff + ty clean.

**Commit message:** `feat(stochastic_fx/variance_proxy): σ_T computation + Phase-A algebraic inversion`

---

### Task 4.2 — Author `InversionVerifier` combining Phase A/B/C

**Files:**
- Modify: `simulations/stochastic_fx/variance_proxy.py` (append `InversionVerifier`)
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add verifier tests)

**Agent dispatch:** `Senior Developer` + `AI Engineer` (paired for the moment-match and KS-test math).

**Acceptance:**
- `InversionVerifier` frozen-dc with module-level constants `MOMENT_REL_TOL = 0.05` and `KS_PVALUE_FLOOR = 0.01` (Pin Z1.4 calibration per spec v0.3 §8). `__call__(parameters, ensemble, x_bar) -> InversionVerdict`.
- Per-family dispatch on `ensemble.family_id` to select the right moment function from `moments.py` and the right reference distribution shape per spec v0.3 §4.2 table (lognormal for GBM/Merton; gamma for OU).
- Phase A check: calls `verify_phase_a` from Task 4.1 to populate `phase_a_passes` and `phase_a_max_residual`.
- Phase B check (Pin Z1.3b): compute empirical `mean(ensemble.sigma_t_per_path)` and `var(ensemble.sigma_t_per_path)`; compute analytic via `{gbm,ou,merton}_moments(parameters)`; relative-error each moment; PASS iff both are ≤ `MOMENT_REL_TOL`. Raises `MomentMatchFailedError` if relative error > `MOMENT_REL_TOL` (HALT routing per Pin Z1.5).
- Phase C check (Pin Z1.4): fit the family's reference distribution to the analytic E[σ_T] and Var[σ_T] (scipy's `gamma.fit` with `floc=0, fscale=Var/E` for gamma; `lognorm.fit` with parameters derived from log-mean = log(E²/√(Var+E²)) and log-std = √(log(1 + Var/E²)) for lognormal). KS-test empirical `sigma_t_per_path` against this reference; populate `phase_c_ks_pvalue`. PASS iff p ≥ `KS_PVALUE_FLOOR`. Raises `InversionTestFailedError` if p < `KS_PVALUE_FLOOR`.
- Anti-fishing rule: the verifier rejects calls where `ensemble.paths.shape[0] != 1000` (the N=1000 floor per spec v0.3 §8). Does NOT accept "increased N" — explicit constant.
- `tex_anchor` populated with relative path `notes/stochastic_fx_tex/sigma_t_moments_{family}.tex`.
- `audit_block` is sha256 of `(ensemble.audit_block, parameters canonical JSON, x_bar, MOMENT_REL_TOL, KS_PVALUE_FLOOR)`.
- Round-trip read-back test: same inputs → same `InversionVerdict` audit_block.
- Per-family unit tests at canonical pins: verify all three Phases PASS for GBM, OU, Merton.

**Commit message:** `feat(stochastic_fx/variance_proxy): InversionVerifier — Phase A+B+C combiner`

---

## §10 Phase 5 — IO Boundary tier (emit)

### Task 5 — Author `emit.py` with parquet + JSON + LaTeX + MD emitters

**Files:**
- Create: `simulations/stochastic_fx/emit.py`
- Modify: `simulations/stochastic_fx/__init__.py` (re-export)
- Modify: `simulations/tests/test_saas_stochastic_fx.py` (add emit round-trip tests)

**Agent dispatch:** `Senior Developer`.

**Acceptance:**
- `PathEnsembleEmitter(emit_dir: Path)` class (IO Boundary tier — `__init__` allowed). `__call__(ensemble: PathEnsemble) -> Path` writes parquet at `simulations/stochastic_fx/data/path_ensemble_{family_id}.parquet`. Schema: one row per (path_index, step_index, x_t) triple; metadata holds the canonical parameters JSON + audit_block + rng_seed.
- `InversionVerdictEmitter(emit_dir: Path)` class. `__call__(verdict: InversionVerdict) -> Path` writes JSON v1.0 schema at `simulations/stochastic_fx/data/inversion_verdict_{family_id}.json`. Schema includes all `InversionVerdict` fields + `phase_a_tolerance = NUMERICAL_IDENTITY_TOL` + `phase_b_tolerance = MOMENT_REL_TOL` + `phase_c_tolerance = KS_PVALUE_FLOOR`. Round-trip read-back equality enforced.
- `TexFragmentEmitter(emit_dir: Path)` class. NOT writing to data/ (committed): writes under `notes/stochastic_fx_tex/`. No-op if the fragment already exists — these are Task 2.1 artifacts; this class is for re-emit only.
- `StochasticFxResultsEmitter(emit_dir: Path)` class. `__call__(verdicts: tuple[InversionVerdict, ...]) -> Path` writes `notes/STOCHASTIC_FX_RESULTS.md` parallel to STAGE_2_RESULTS.md, R-tagged sections per family. Format mirrors STAGE_2_RESULTS.md exactly.
- Unit tests:
  - Round-trip on each emitter (write + read + field-equality).
  - File-existence assertions per emit.
  - `simulations/stochastic_fx/data/` files are NOT git-tracked (Task 0 verification — `git check-ignore` returns the path).

**Commit message:** `feat(stochastic_fx/emit): IO Boundary tier — parquet + JSON + tex + MD emitters`

---

## §11 Phase 6 — End-to-end verification

### Task 6 — Run end-to-end per family + emit `STOCHASTIC_FX_RESULTS.md`

**Files:**
- Create: `scratch/2026-05-11-stochastic-fx-execution/moment_verification_log.md`
- Create: `scratch/2026-05-11-stochastic-fx-execution/ks_test_log.md`
- Create: `notes/STOCHASTIC_FX_RESULTS.md` (via Task 5's emitter)

**Agent dispatch:** `Senior Developer` + `Reality Checker` (inline numerical cross-check per cohort_4 pattern).

**Acceptance:**
- A small ad-hoc driver script (NOT committed; run via `.venv/bin/python -c "..."` or a tempfile) for each family:
  1. Construct the canonical Parameters frozen-dc (Task 1.2 CANONICAL_*).
  2. Instantiate the family's PathGenerator (Task 3.x).
  3. Sample `n_paths = 1000` with a fixed `rng_seed = 42`.
  4. Run the `InversionVerifier` against the ensemble at `x_bar = parameters.x_0` (= 4000).
  5. Emit parquet, JSON, MD via the Phase-5 emitters.
- Per family the `InversionVerdict.passes == True`:
  - Phase A residual ≤ NUMERICAL_IDENTITY_TOL (1e-6).
  - Phase B mean and var relative errors ≤ MOMENT_REL_TOL (0.05).
  - Phase C KS p-value ≥ KS_PVALUE_FLOOR (0.01).
- `notes/STOCHASTIC_FX_RESULTS.md` emitted with R-tagged sections per family + cross-family summary table.
- `moment_verification_log.md` records each family's analytic-vs-empirical moments + relative errors.
- `ks_test_log.md` records each family's reference-fit parameters + KS p-value.
- HALT routing: if any Phase fails for any family, do NOT silent-retune. Report the failure, route per Pin Z1.5 (CORRECTIONS-α + scoped Wave-1 re-review on the plan, NOT silent fix).
- Reality-Checker cross-check: re-run the same driver from scratch with `rng_seed = 42`; confirm bit-exact identical `InversionVerdict.audit_block` per family (Pin Z1.2 determinism).

**Commit message:** `eval(stochastic_fx): end-to-end run at canonical pins — all 3 families PASS`

---

## §12 Phase 7 — Pin Z1.6 strip preservation verification

### Task 7 — Verify cohort_5_strip audit_block unchanged

**Files:**
- Create: `scratch/2026-05-11-stochastic-fx-execution/pin_z16_strip_preservation_log.md`

**Agent dispatch:** N/A — orchestrator-only operation (single hex-grep shell command + log entry per `memory/feedback_specialized_agents_per_task.md` shell-ops exception).

**Acceptance:**
- Bash command: `grep -F '94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329' simulations/saas_builder/data/IronCondor_strip.json` returns the audit_block line. Same command run before Task 1.1 (at the plan's start commit) AND after Task 6 (at the plan's last commit). Both runs MUST return the same line.
- `pin_z16_strip_preservation_log.md` records both grep results + the two commit shas.
- HALT routing: if the audit_block has changed during plan execution, HALT and route to cohort_5_strip review (the strip emit is anti-fishing-coupled to this plan's correctness; any drift is a master-spec-level concern).

**Commit message:** `verify(stochastic_fx): Pin Z1.6 cohort_5_strip audit_block preservation`

---

## §13 Pin coverage (per spec v0.3 §5)

| Pin | This plan's coverage |
|---|---|
| Z1.1 — SDE parameters pre-pinned ex-ante | Task 1.2 canonical pins frozen at this commit; Pin enforced by anti-fishing routing in Task 6. |
| Z1.2 — Path-ensemble determinism | Tasks 3.1 / 3.2 / 3.3 each have a Hypothesis test pinning bit-exact audit_block for the same `(rng_seed, n_paths)`. |
| Z1.3a — Algebraic inversion (family-agnostic) | Task 4.1 free function + property test. |
| Z1.3b — Moment match per family | Task 4.2 InversionVerifier Phase B + Task 6 end-to-end. |
| Z1.4 — KS goodness-of-fit per family | Task 4.2 InversionVerifier Phase C + Task 6 end-to-end. |
| Z1.5 — Anti-fishing routing | HALT triggers per task; explicit "N=1000 floor, not parameter to grow" enforcement in Task 4.2 InversionVerifier. |
| Z1.6 — Strip preservation | Task 7. |

## §14 HALT routing

| Trigger | Route |
|---|---|
| Task 1.x ruff / ty / Hypothesis-test fail | HALT — Senior Developer iterates; no relaxation of property tests. |
| Task 2.1 hand-derived moment numerical sanity fails | HALT — re-verify the spec v0.3 §4.2 formulas against literature; CORRECTIONS-α to the spec if the formula was wrong. |
| Task 3.x SDE generator's trivial-degenerate-limit test fails | HALT — discretization defect; investigate (e.g., dt too coarse). NEVER raise sigma to pass. |
| Task 4.1 algebraic-inversion property test fails | HALT — float64 numerical defect; investigate `apply_inversion`. |
| Task 4.2 InversionVerifier raises for canonical fixture | HALT — CORRECTIONS-α + scoped Wave-1 re-review per spec v0.3 Pin Z1.5. |
| Task 6 any family's Phase B / Phase C fails | HALT per Pin Z1.5. NEVER increase N. NEVER retune SDE parameters silently. |
| Task 7 strip audit_block changed | HALT — route to cohort_5_strip review (master-spec-level coupling concern). |
| Wave-1 or Wave-2 RC+MQ on this plan returns BLOCK | HALT per master-spec §6.1; CORRECTIONS-α in §16. |

## §15 Artifacts emitted

| Artifact | Phase | Schema | Lineage parent |
|---|---|---|---|
| `simulations/stochastic_fx/{__init__,_errors,types,moments,generators,variance_proxy,emit}.py` | 1–5 | code | (new package) |
| `notes/stochastic_fx_tex/{eps_inversion,sigma_t_moments_{family}}.tex` | 2 | LaTeX fragments | sympy.latex() rendering of hand-derived moments |
| `simulations/stochastic_fx/data/path_ensemble_{family}.parquet` | 6 | new v1.0 | sha over (params, rng_seed, paths bytes); gitignored |
| `simulations/stochastic_fx/data/inversion_verdict_{family}.json` | 6 | new v1.0 | sha over (ensemble audit, params, tolerances); gitignored |
| `notes/STOCHASTIC_FX_RESULTS.md` | 6 | parallel to STAGE_2_RESULTS.md | composed of per-family verdicts |
| `scratch/2026-05-11-stochastic-fx-execution/{moment_verification,ks_test,pin_z16_strip_preservation}_log.md` | 6–7 | markdown | run logs |

## §16 CORRECTIONS-α (reserved)

v0.1 has no corrections. Wave-1 RC+MQ on this plan may land v0.2 → §16.1.

## §17 References

- `docs/specs/2026-05-11-stochastic-fx-variant-design.md` v0.3 — parent spec (the §10 protocol for this plan's Wave-1 review).
- `notes/PRIMITIVES.md` §5 eq. (6), §6 eq. (7), (8), §15 open item 2.
- `notes/STAGE_2_RESULTS.md` — parallel structure for `notes/STOCHASTIC_FX_RESULTS.md`.
- `simulations/saas_builder/cohort_5_strip/` — strip artifact preserved per Pin Z1.6.
- `simulations/saas_builder/cohort_4/types.py::NUMERICAL_IDENTITY_TOL` — reused as the float64 floor for Pin Z1.3a.
- `simulations/saas_builder/cohort_4/io.py` — pattern for `pin_and_emit` + round-trip read-back equality, reused for InversionVerdictEmitter.
- `simulations/utils/{parquet_io, json_io, audit_block}.py` — IO Boundary tier patterns.
- `memory/feedback_no_code_in_specs_or_plans.md` — plan-as-orchestration convention.
- `memory/feedback_specialized_agents_per_task.md` — foreground-orchestrates-never-authors.
- `superpowers:writing-plans` — flow that produced this plan.
- `superpowers:subagent-driven-development` — recommended execution flow.

---

*End of stochastic-FX variant plan v0.1. Independent RC + MQ Wave-1 review dispatch by the orchestrator before any task execution.*
