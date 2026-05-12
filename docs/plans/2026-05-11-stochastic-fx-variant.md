# STOCHASTIC-FX VARIANT — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. **Tracking unit is the TASK (one task per commit), not per-step** — matches the repo's cohort-N convention (see `docs/plans/2026-05-08-saas-cohort-*` precedents). Per-step `- [ ]` checkboxes are intentionally NOT used; subagent-driven-development's TaskCreate/TaskUpdate is the tracking surface. (FLAG-RC-2 disposition; §16.1.)
>
> **Code-agnostic plan.** Per repo memory `memory/feedback_no_code_in_specs_or_plans.md` (NON-NEGOTIABLE), this plan does NOT contain Python code blocks. Each task dispatches a specialized agent who authors code per the functional-python skill + the Honnibal audit-pass chain.
>
> **Foreground orchestrates, never authors.** Per repo memory `memory/feedback_specialized_agents_per_task.md` (NON-NEGOTIABLE).

**Plan version:** v0.2 (Wave-1 RC ACCEPT_WITH_FLAGS + MQ ACCEPT_WITH_FLAGS — 8 flags + 4 NITs disposed inline per §16.1)
**Parent spec:** `docs/specs/2026-05-11-stochastic-fx-variant-design.md` v0.3 (Wave-1 ACCEPT_WITH_FLAGS-DISPOSED)
**Predecessor:** `simulations/saas_builder/cohort_5_strip/` (commit `3442852`, audit `94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329` — PRESERVED unchanged per Pin Z1.6)
**Status:** Wave-1 ACCEPT_WITH_FLAGS-DISPOSED — per-task execution authorized once §16.1 corrections land
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
- Three frozen-dataclass Parameters Value types, one per SDE family. Each has the fields and `__post_init__` invariants documented in the table below (FLAG-RC-1 disposition: function/class signatures replaced with prose tables).

  **Per-family Parameters fields + invariants:**

  | Family | Required fields | `__post_init__` invariants |
  |---|---|---|
  | GBM | drift, volatility, spot, horizon, step size, number of steps | volatility > 0; spot > 0; horizon > 0; step size > 0; number of steps ≥ 2; number of steps × step size equals horizon within float tolerance |
  | OU | mean-reversion rate, long-run mean, volatility, spot, horizon, step size, number of steps | mean-reversion rate > 0; volatility > 0; long-run mean > 0; spot > 0; horizon > 0; step size > 0; number of steps ≥ 2 |
  | Merton jump-diffusion | drift, diffusion volatility, jump intensity, jump-size mean, jump-size std, spot, horizon, step size, number of steps | diffusion volatility > 0; jump intensity ≥ 0; jump-size std > 0; spot > 0; horizon > 0; step size > 0; number of steps ≥ 2 |

- Module-level canonical-pin constants per spec v0.3 §4.2 table, one per family. Numerical values per spec v0.3 §4.2 row entries verbatim. Pin values frozen at this commit; ex-post tuning requires CORRECTIONS-α + scoped Wave-1 re-review per Pin Z1.5.
- One Hypothesis property test per family checking `__post_init__` rejects invalid parameter combinations (zero or negative volatility; number of steps < 2; etc.) AND accepts the canonical pins from spec v0.3 §4.2.
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
- `PathEnsemble` frozen-dataclass holding: a family identifier from the closed alphabet `{gbm, ou, merton}`; a 2-D path matrix (N paths × n_steps+1 timesteps); a 1-D realised-variance array of length N (one σ_T value per path); the canonical parameters JSON-serialized as a string; the deterministic RNG seed used to sample the ensemble; and a 64-char lowercase hex audit_block. `__post_init__` validates: path matrix is 2-D; σ_T array shape matches path-count; audit_block matches the 64-char lowercase hex regex; family identifier is in the closed alphabet.
- `InversionVerdict` frozen-dataclass holding: family identifier; Phase-A pass flag + max algebraic-inversion residual (Pin Z1.3a); Phase-B pass flag + mean and var relative errors (Pin Z1.3b); Phase-C pass flag + KS p-value + path-count used (Pin Z1.4); composite pass flag (logical AND of the three phase flags); a tex_anchor string pointing to the family's LaTeX fragment file; and a 64-char audit_block. `__post_init__` validates: bool fields are bool; composite pass equals the AND of the three phase flags; tolerances numerically reasonable; audit_block matches hex regex; family identifier in closed alphabet.
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
- Three free functions in `moments.py`, one per family. Each takes the family's Parameters frozen-dataclass and returns a tuple of two floats: the analytic E[σ_T] and the analytic Var[σ_T]. Per-family math content pinned in the table below (FLAG-MQ-1 + FLAG-MQ-3 disposition: Merton and Var forms now literalised; FLAG-RC-1 disposition: function signatures replaced with prose table).

  **Per-family hand-derived analytic moments** (substitution `(X̄/Ȳ)² → params.x_0**2` at the canonical pin per FLAG-MQ-2; symbolic form retained in `.tex`):

  | Family | Analytic E[σ_T] (Python form) | Analytic Var[σ_T] (Python form) |
  |---|---|---|
  | GBM | `params.x_0**2 * ((exp(params.sigma**2 * params.T) - 1) / (params.sigma**2 * params.T) - 1)` (exact; vanishes at σ→0 per NEW-BLOCK-MQ-4 fix) | `2 * (params.x_0**4) * (exp(params.sigma**2 * params.T) - 1)**2 / (params.sigma**4 * params.T**2)` (Hull §15 leading order; assumes mean-zero log-drift) |
  | OU (stationary) | `params.sigma**2 / (2 * params.theta)` (exact) | `2 * params.sigma**4 / ((2 * params.theta)**2 * params.T)` (leading order under chi-squared approximation; standard OU stationary moment) |
  | Merton jump-diffusion | `params.x_0**2 * params.sigma**2 * params.T + params.lambda_jump * params.x_0**2 * (exp(2*(params.jump_mean + params.jump_std**2)) - 2*exp(params.jump_mean + params.jump_std**2/2) + 1) * params.T` (Andersen-Piterbarg Vol I §2.7; leading order; mean-zero log-drift) | `2 * params.sigma**4 * params.x_0**4 * params.T + params.lambda_jump * params.x_0**4 * (variance contribution from compound-Poisson moment-of-moment; Andersen-Piterbarg §2.7.3 formula expanded literally — implementer transcribes the textbook expression into Python at authoring time, NOT spec-time) |

- **`moments.py` module docstring** (FLAG-MQ-2 disposition) MUST explicitly document the `(X̄/Ȳ)² → params.x_0**2` substitution: the canonical-pin convention pins `x_0 = X̄/Ȳ = 4000.0` so the two are interchangeable at evaluation time, but the SYMBOLIC form `(X̄/Ȳ)²` is the conceptually-correct one and is what the `.tex` fragments retain.

- Numerical sanity test per family: at canonical pins (Task 1.2 spec v0.3 §4.2 table values), the Python-form expressions evaluate to numbers within `1e-12` of hand-computed analytic numbers logged in the test.

- LaTeX-fragment emission via `sympy.latex(...)` for each family's moment expressions; saved to `notes/stochastic_fx_tex/sigma_t_moments_{family_id}.tex` where `{family_id}` ∈ `{gbm, ou, merton}` (NIT family naming drift disposition: use `{family_id}` consistently with the PathEnsemble closed alphabet). Each fragment contains:
  - The exact-form LaTeX retaining symbolic `(X̄/Ȳ)²` notation per FLAG-MQ-2 (NOT the Python substituted form).
  - Literature citation as a LaTeX `\cite{}` (or inline `% ref: ...` comment if a bib file is not present).
  - A numerical-pin example at the canonical fixture, computed via the Python form.

- Also write the family-agnostic eq. (8) algebraic inversion LaTeX to `notes/stochastic_fx_tex/eps_inversion.tex` (single one-line fragment).
- Hypothesis property tests: monotonicity of E[σ_T] in volatility per family; bounds checks (E ≥ 0, Var ≥ 0).
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
- `GBMPathGenerator` frozen-dataclass holding the family's Parameters. Its callable surface accepts a deterministic RNG seed and the number of paths, and returns a PathEnsemble. Uses `numpy.random.default_rng(seed)` for reproducibility per Pin Z1.2. (FLAG-RC-1 disposition: signature prose-ified.)
- Discretization scheme: Euler-Maruyama on log-scale. Per step, the path multiplicatively updates by `exp((drift − volatility²/2)·dt + volatility·√dt · Z)` where `Z ~ N(0, 1)`. The `−volatility²/2` term is the Itô correction (MQ check).
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
- `OUPathGenerator` frozen-dataclass holding the family's Parameters; callable surface mirrors `GBMPathGenerator` (deterministic RNG seed + n_paths in, PathEnsemble out).
- Discretization: EXACT transition (not Euler — OU admits a closed-form Gaussian transition). Per step, the new value equals `long-run-mean + (X_t − long-run-mean)·exp(−rate·dt) + volatility·√((1 − exp(−2·rate·dt))/(2·rate)) · Z`. This is the standard OU exact-conditional-Gaussian update.
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
- `JumpDiffusionPathGenerator` frozen-dataclass holding the family's Parameters; callable surface mirrors the other generators.
- Discretization: Euler-Maruyama on log-scale (per Task 3.1) augmented by compound-Poisson jumps. Per step: (i) sample the number of jumps from a Poisson distribution with mean `jump_intensity·dt`; (ii) sample that many jump sizes from a lognormal distribution with parameters `(jump_mean, jump_std)`; (iii) aggregate jumps multiplicatively into the diffusion step, so the new value equals the GBM diffusion update times the product of jump multipliers.
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
- A free function that re-applies PRIMITIVES.md §6 eq. (7) to the ensemble's paths and returns the per-path realised variance array. Verifies the σ_T values stored on the ensemble match the freshly-computed values within `NUMERICAL_IDENTITY_TOL = 1e-6` (reused from `simulations.saas_builder.cohort_4.types::NUMERICAL_IDENTITY_TOL`).
- A free function that implements PRIMITIVES.md §6 eq. (8) algebraically: given a realised variance σ_T and the FX mean x_bar, returns `sqrt(8 * σ_T / x_bar**2)`.
- A free function implementing Pin Z1.3a: for each path's σ_T_n, verifies `(eps_n)² == 8·σ_T_n / x_bar²` to float64 precision (algebraic substitution, family-agnostic). Returns the composite pass flag plus the maximum absolute residual across the N paths. PASS iff max residual ≤ `NUMERICAL_IDENTITY_TOL`.
- Unit test: at the canonical fixture (x_bar = 4000.0, σ_T = 20000.0), the inversion function returns exactly 0.1.
- Property test (Hypothesis): for any valid (σ_T > 0, x_bar > 0), the inversion result is finite and non-negative; at σ_T = 0, the result is exactly 0 (trivial-degenerate-limit per Pin Z1.3a).
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
- `InversionVerifier` frozen-dataclass with two module-level `Final` constants pinned in `simulations/stochastic_fx/variance_proxy.py`: `MOMENT_REL_TOL = 0.05` (Pin Z1.3b tolerance) and `KS_PVALUE_FLOOR = 0.01` (Pin Z1.4 calibration per spec v0.3 §8). Downstream consumers (Tasks 5, 6) import via `from simulations.stochastic_fx.variance_proxy import MOMENT_REL_TOL, KS_PVALUE_FLOOR` — single source of truth (FLAG-RC-3 disposition). The callable surface accepts the Parameters, a PathEnsemble, and the FX mean x_bar; returns an InversionVerdict.
- Per-family dispatch on the ensemble's family identifier to select the right moment function from `moments.py` and the right reference distribution shape per spec v0.3 §4.2 (lognormal for GBM/Merton; gamma for OU).
- Phase A check: calls the Task 4.1 Phase-A free function to populate `phase_a_passes` and `phase_a_max_residual`.
- Phase B check (Pin Z1.3b): compute empirical mean and variance from `ensemble.sigma_t_per_path`; compute analytic from `moments.py` (per family); compute the relative error on each moment separately; PASS iff both relative errors are ≤ `MOMENT_REL_TOL`. Raises `MomentMatchFailedError` if either relative error exceeds the tolerance (HALT routing per Pin Z1.5).
- Phase C check (Pin Z1.4): construct the family's reference distribution DIRECTLY from the analytic moments (NIT-MQ-1 disposition — do NOT call `.fit()` against empirical data, which would re-introduce a tautology surface). Construction formulas per family:
  - **Lognormal (GBM, Merton):** given analytic E and Var, compute the lognormal shape parameter `s = sqrt(log(1 + Var/E**2))` and scale `scale = E / sqrt(1 + Var/E**2)`; construct the SciPy distribution as `scipy.stats.lognorm(s=s, scale=scale)`. This is the standard method-of-moments lognormal construction from positive-mean, positive-variance.
  - **Gamma (OU):** given analytic E and Var, compute gamma shape `a = E**2 / Var` and scale `scale = Var / E`; construct as `scipy.stats.gamma(a=a, scale=scale)`. Standard MoM gamma construction.
  
  KS-test the empirical `ensemble.sigma_t_per_path` against this reference using `scipy.stats.ks_1samp(samples, reference.cdf)`; populate `phase_c_ks_pvalue`. PASS iff p ≥ `KS_PVALUE_FLOOR`. Raises `InversionTestFailedError` if p < `KS_PVALUE_FLOOR`.
- **Anti-fishing rule (Pin Z1.5 enforcement at construction time):** the InversionVerifier rejects calls where `ensemble.paths.shape[0] != 1000` (the N=1000 floor per spec v0.3 §8). The check happens INSIDE `__call__` BEFORE any phase runs; raises `MCBudgetExceededError` if violated. N=1000 is a frozen module-level constant, NOT a parameter to grow.
- `tex_anchor` populated with the relative path `notes/stochastic_fx_tex/sigma_t_moments_{family_id}.tex`.
- `audit_block` is sha256 of (ensemble.audit_block + canonical-parameters JSON + x_bar + MOMENT_REL_TOL + KS_PVALUE_FLOOR), deterministic across re-runs.
- Round-trip read-back test: same inputs → same InversionVerdict audit_block.
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
- Four IO-Boundary-tier classes, each with an `__init__(emit_dir)` and a callable surface (FLAG-RC-1 disposition: class signatures replaced with prose):
  - **PathEnsembleEmitter**: writes a parquet file at `simulations/stochastic_fx/data/path_ensemble_{family_id}.parquet` where `{family_id}` ∈ `{gbm, ou, merton}` (NIT family naming drift disposition: use `{family_id}` consistently, NOT `{family}`). Schema: one row per (path_index, step_index, x_t) triple; metadata holds the canonical parameters JSON + audit_block + rng_seed.
  - **InversionVerdictEmitter**: writes a JSON v1.0 schema file at `simulations/stochastic_fx/data/inversion_verdict_{family_id}.json`. Schema includes all InversionVerdict fields plus three tolerance constants imported from `simulations/stochastic_fx/variance_proxy.py` per FLAG-RC-3: `phase_a_tolerance = NUMERICAL_IDENTITY_TOL`, `phase_b_tolerance = MOMENT_REL_TOL`, `phase_c_tolerance = KS_PVALUE_FLOOR`. Round-trip read-back equality enforced (write → read → in-memory equality).
  - **TexFragmentEmitter**: writes under `notes/stochastic_fx_tex/` (NOT under data/; .tex fragments are committed). No-op if the fragment already exists — these are Task 2.1 artifacts; this class is for re-emit only.
  - **StochasticFxResultsEmitter**: writes `notes/STOCHASTIC_FX_RESULTS.md` (parallel to STAGE_2_RESULTS.md) given a tuple of InversionVerdicts. R-tagged sections per family + cross-family summary table. Format mirrors STAGE_2_RESULTS.md exactly.
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

**Commit message:** outcome-neutral, decided at run-time per FLAG-RC-4 disposition. If all three families PASS: `eval(stochastic_fx): end-to-end run at canonical pins — emit verdicts (3 families)`. If any family FAILS: `eval(stochastic_fx): end-to-end run at canonical pins — HALT per Pin Z1.5 (family X failed phase Y)`. NEVER pre-pin "all PASS" in the commit message — that would be the anti-fishing pattern of asserting the outcome before the run.

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
| Task 5 emit round-trip read-back equality fails on ANY emitter | HALT — IO Boundary tier defect; investigate parquet/JSON schema or LaTeX-fragment encoding. NIT-RC-Task5 disposition. |
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

## §16 CORRECTIONS-α (patch log)

### §16.1 v0.1 → v0.2 (Wave-1 RC+MQ disposition)

**Wave-1 review verdicts:**
- RC: ACCEPT_WITH_FLAGS (4 material flags + 1 NIT + minor naming consistency drift).
- MQ: ACCEPT_WITH_FLAGS (4 flags — math content faithful to spec v0.3; flags are surface-level surface-area improvements).

Verdict files:
- `scratch/2026-05-11-stochastic-fx-plan-review/rc-verdict.md`
- `scratch/2026-05-11-stochastic-fx-plan-review/mq-verdict.md`

Both reviewers explicitly stated no full Wave-1 re-dispatch required; orchestrator-side v0.2 patch suffices.

| Finding | Severity | Disposition | Location |
|---|---|---|---|
| **FLAG-RC-1** | Material | Inline-backtick code signatures pervaded acceptance bullets (`__call__(...) -> ...`, `Name(field: type, ...)`, etc.) — violated `memory/feedback_no_code_in_specs_or_plans.md` per the parent spec's RC-FLAG-1-v2 disposition. v0.2 prose-ifies signatures and replaces constant-construction lines with per-family Parameters tables (Tasks 1.2, 1.3, 2.1, 3.1, 3.2, 3.3, 4.1, 4.2, 5). Math notation and JSON-schema illustrations remain admissible. | Tasks 1.2 / 1.3 / 2.1 / 3.1 / 3.2 / 3.3 / 4.1 / 4.2 / 5 |
| **FLAG-RC-3** | Material | `MOMENT_REL_TOL` and `KS_PVALUE_FLOOR` import path pinned: defined as module-level `Final` in `simulations/stochastic_fx/variance_proxy.py`; downstream consumers import via `from simulations.stochastic_fx.variance_proxy import ...` (single source of truth). | Task 4.2 acceptance + Task 5 emit |
| **FLAG-RC-4** | Material (anti-fishing) | Task 6 commit message reframed as outcome-neutral. Two run-time-decided variants: (i) PASS case emits `eval(stochastic_fx): emit verdicts (3 families)`; (ii) FAIL case emits `eval(stochastic_fx): HALT per Pin Z1.5 (family X failed phase Y)`. Pre-pinning "all PASS" in the commit message was the anti-fishing pattern. | Task 6 |
| **FLAG-RC-2** | NIT | Header text clarifies that the cohort-N convention tracks the TASK (one task per commit), NOT per-step `- [ ]` checkboxes. Subagent-driven-development's TaskCreate/TaskUpdate is the canonical tracking surface. Matches A1/A2/B1 plan precedents. | Header |
| **NIT — `{family_id}` vs `{family}` drift** | Cosmetic | All filename templates and dispatch references now use `{family_id}` consistently with the PathEnsemble Value type's closed alphabet `{gbm, ou, merton}`. | Tasks 2.1 / 5 |
| **NIT — Task 5 missing HALT row** | Cosmetic | §14 HALT routing now has a Task 5 row: "Task 5 emit round-trip read-back equality fails → HALT IO Boundary tier defect". | §14 |
| **FLAG-MQ-1** | Medium | Merton `E[σ_T]` Python form now literalised in Task 2.1 acceptance table — full expression with all terms, mirroring GBM/OU rows (prevents the most-error-prone family from being implementer-discretion). | Task 2.1 per-family moment table |
| **FLAG-MQ-2** | Medium | `moments.py` module docstring requirement explicit: documents the `(X̄/Ȳ)² → params.x_0**2` substitution at canonical pin (x_0 = X̄/Ȳ = 4000); `.tex` fragments retain symbolic `(X̄/Ȳ)²` form. Task 2.1 acceptance now states this requirement separately. | Task 2.1 acceptance |
| **FLAG-MQ-3** | Low | `Var[σ_T]` Python forms for GBM and Merton added to Task 2.1 per-family moment table (alongside the previously-present OU form). Removes the silent-fishing surface. | Task 2.1 per-family moment table |
| **NIT-MQ-1** | Low | Task 4.2 Phase C construction changed from `scipy.stats.lognorm.fit(...)` / `gamma.fit(...)` (which would re-introduce the empirical-fit tautology MQ caught at spec v0.1) to DIRECT method-of-moments construction: `lognorm(s=…, scale=…)` from analytic E and Var; `gamma(a=…, scale=…)` similarly. Construction formulas spelled out in Task 4.2 acceptance. | Task 4.2 Phase C |

### §16.2 Wave-2 (post-execution) review reserve

Wave-2 RC+MQ on this plan's exit deliverables (each family's parquet + JSON + STOCHASTIC_FX_RESULTS.md emit) lands at §16.3 once execution completes.

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
