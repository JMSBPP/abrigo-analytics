---
spec_id: stochastic-fx-variant-design
spec_version: v0.4 (v0.3 ACCEPT_WITH_FLAGS-DISPOSED at Wave-1; v0.4 amends Pin Z1.3b to mean-only Phase B per user disposition Option B 2026-05-13 — the variance-match-at-N=1000 gate was structurally unsatisfiable due to MC-noise floor 8-30% per family vs MOMENT_REL_TOL=0.05. Full-distribution match remains in Phase C KS test against moment-matched reference. See §11.6 CORRECTIONS-α.)
emit_timestamp_utc: 2026-05-11
parent_framework: notes/PRIMITIVES.md §15 open item — "Path A v3" stochastic-FX variant
stage_2_results_anchor: notes/STAGE_2_RESULTS.md (R1–R8 closed forms under deterministic eq. (6))
stage_3_first_wave_spec: docs/specs/2026-05-11-stage-3-first-wave-design.md v0.2 (the master Stage-3 spec; this spec is a parallel second-wave sub-project)
strip_anchor: simulations/saas_builder/cohort_5_strip/ (commit 3442852, audit_block 94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329)
authority: CLAUDE.md anti-fishing invariants (NON-NEGOTIABLE); brainstorming flow; memory/feedback_pathological_halt_anti_fishing_checkpoint.md
predecessor: none (first stochastic-FX spec)
status: v0.2 — awaiting BOTH-reviewers re-dispatch per master-spec §6.1 (BLOCK requires RC+MQ re-review on the revision)
---

# Stochastic-FX variant — design spec

This spec scopes the `simulations/stochastic_fx/` package, a NEW sibling
package to `simulations/saas_builder/cohort_5_strip/` that produces
stochastic FX-path ensembles under three SDE families (GBM, OU,
jump-diffusion) and verifies that PRIMITIVES.md §6 eq. (8) variance-proxy
inversion `ε(σ_T) = √(8·σ_T/(X̄/Ȳ)²)` holds DISTRIBUTIONALLY under each.

The spec closes PRIMITIVES.md §15 open item ("Path A v3" stochastic-FX
variant) at the math + simulation level. It is a Stage-3 second-wave
sub-project: independent from the first-wave A1 / A2 / B1 tracks, and
chosen as the first second-wave spec because it addresses a structural
concern the deterministic generator cannot — that equilibrium behavior
under the deterministic eq. (6) is artificial (periodicity → synchronized
paths → equilibrium becomes a fixed point of the periodic dynamics
rather than an emergent property).

## §0 Scope statement

**In scope.** A new sibling package `simulations/stochastic_fx/` that:

1. Specifies frozen-dataclass parameter containers for three SDE
   families: GBM (geometric Brownian motion), OU (Ornstein-Uhlenbeck
   mean-reverting), and Merton jump-diffusion (GBM + Poisson jumps).
2. Implements path-ensemble generators per family with deterministic
   `rng_seed → audit_block` pinning.
3. Implements distributional verification of PRIMITIVES.md §6 eq. (8)
   `ε ↔ σ_T` inversion per family: (a) symbolic via sympy, asserting
   reduction to the deterministic form under the σ → 0 limit; (b)
   Monte-Carlo KS-test of the empirical ε̂-distribution against the
   analytic ε distribution.
4. Emits artifacts: per-family parquet path ensemble + per-family JSON
   inversion verdict + a single `notes/STOCHASTIC_FX_RESULTS.md`
   markdown anchor mirroring `notes/STAGE_2_RESULTS.md`.

**Anti-fishing scope guard.** This spec does NOT pre-pin which families
will PASS or FAIL the inversion verifier. Pre-pinning outcome direction
would be the post-hoc-fishing pattern. The exit criterion is
deliverable-existence + review-PASS at well-defined gates, not
outcome-direction at the gate.

**Strip preservation invariant.** The cohort_5_strip emit
(`IronCondor_strip.json`, audit `94150326…`) is PRESERVED unmodified by
this spec. Stochastic-FX is an ADDITIVE verification layer; it does NOT
re-emit cohort_5_strip under stochastic-path expectations. Re-emitting
would be a strip retuning and is anti-fishing-banned at the master-spec
§6.4 level (would route through CORRECTIONS-α + Wave-1 re-review on
cohort_5_strip itself).

## §1 Cross-references

| Anchor | Section | What this spec inherits or extends |
|---|---|---|
| `notes/PRIMITIVES.md` | §5 eq. (6) | The deterministic FX generator this spec parallels-stochastically. |
| `notes/PRIMITIVES.md` | §6 eq. (7), eq. (8) | The variance proxy and inversion identity verified distributionally per SDE family. |
| `notes/PRIMITIVES.md` | §15 open item 2 | This spec is the canonical closure of "Path A v3 stochastic-FX variant" at the math + simulation level. |
| `notes/STAGE_2_RESULTS.md` | §2.1 (R1) | The σ_0 anchor reduces to eq. (8)'s deterministic case under σ → 0 — this spec verifies that limit symbolically per SDE family. |
| `docs/specs/2026-05-11-stage-3-first-wave-design.md` v0.2 | §3 cross-track dependency graph | This spec is NOT in the first-wave dependency graph; it stands independently. |
| `simulations/saas_builder/cohort_5_strip/` | commit `3442852`, audit `94150326…` | The strip artifact this spec verifies stochastic-stress-resilience for (PRESERVED unchanged). |
| `memory/feedback_pathological_halt_anti_fishing_checkpoint.md` | — | HALT routing protocol consumed by §5 Pin Z1.5. |
| `memory/feedback_no_code_in_specs_or_plans.md` | — | This spec contains no code; implementation lives in a separate plan. |

## §2 Architecture

`simulations/stochastic_fx/` is a NEW sibling package to
`simulations/saas_builder/cohort_5_strip/`. It does NOT modify
cohort_5_strip, does NOT consume cohort_5_strip artifacts, and does
NOT import from cohort_5_strip. The two packages are independently
testable. Coupling between them happens ONLY at the verification
layer (a future stochastic-strip-envelope verifier — out of scope for
this spec; see §7 hook points).

Three-tier discipline per the functional-python skill, mirroring the
cohort_5_strip layout exactly:

- **Value tier** (`types.py` + `_errors.py`) — frozen-dataclass
  parameter containers + typed exceptions.
- **Callable tier** (`generators.py`, `variance_proxy.py`) — frozen-dc
  with `__call__` for path samplers and inversion verifiers; pure
  with respect to inputs except for the rng_seed.
- **IO Boundary tier** (`emit.py`) — class with `__init__` for parquet
  and JSON emit.

The package's RNG handling pins determinism: every path-generator
`__call__` accepts an `rng_seed: int` and produces a bit-exact ensemble.
The ensemble's `audit_block` is `sha256(parameters_canonical_json +
rng_seed + path_matrix_bytes)`. Same inputs → same audit_block → same
artifact. Pin Z1.2 enforces this.

## §3 Components

**File-tree layout** (RC-FLAG-1 disposition: function signatures
removed; per-file responsibility described in prose below per
`memory/feedback_no_code_in_specs_or_plans.md`):

```
simulations/stochastic_fx/
├── __init__.py
├── _errors.py
├── types.py
├── generators.py
├── variance_proxy.py
├── moments.py
└── emit.py

simulations/tests/test_saas_stochastic_fx.py
```

**Per-file responsibility:**

- `_errors.py` — Value tier. Typed exceptions: `StochasticFXError` (base);
  `SDEParameterError` (invalid SDE parameter at `__post_init__`);
  `InversionTestFailedError` (Z1.4 KS gate failure);
  `MomentMatchFailedError` (Z1.3b moment-equality gate failure);
  `MCBudgetExceededError` (reuse cohort_4 convention).

- `types.py` — Value tier. One frozen-dataclass per SDE family for
  parameters (GBMParameters / OUParameters / JumpDiffusionParameters),
  plus `PathEnsemble` (carries paths, per-path σ_T, audit_block,
  canonical parameters JSON) and `InversionVerdict` (carries the Z1.3a
  algebraic-pass, Z1.3b moment-match-pass, Z1.4 KS-pass, audit_block,
  tex_anchor). Constants for canonical parameter pins are defined here
  (see §4.1 Per-family parameter pin table).

- `generators.py` — Callable tier. One frozen-dataclass with `__call__`
  per SDE family that samples a `PathEnsemble` given a pre-pinned
  RNG seed and ensemble size. RNG handling per `numpy.random.default_rng`;
  determinism per Pin Z1.2.

- `variance_proxy.py` — Callable tier. Implements PRIMITIVES.md §6 eq.
  (7) discretely on the sampled paths (matches B1 plan's σ_T contract).
  Two free functions: one computes the per-path realised variance
  array from an ensemble's path matrix, the other applies the
  algebraic inversion of eq. (8) pointwise per Pin Z1.3a. NO Itô
  calculus (sympy cannot perform stochastic calculus; per BLOCK-MQ-3
  disposition the symbolic phase is strictly algebraic). RC-FLAG-1-v2
  disposition: function signatures previously embedded here are now
  described in prose; full implementation signatures live in the
  implementation plan, not this spec.

- `moments.py` — Callable tier (NEW in v0.2 per BLOCK-MQ-2/3). One
  function per SDE family returning the analytic `E[σ_T]` and
  `Var[σ_T]` expressions HAND-DERIVED from literature (Hull,
  Andersen-Piterbarg) and rendered via `sympy.latex(...)` into
  `.tex` fragments. These are the non-trivial mathematical content
  per BLOCK-MQ-3.

- `emit.py` — IO Boundary tier. Classes for parquet ensemble emit,
  JSON inversion-verdict emit (both gitignored under a new
  `simulations/stochastic_fx/data/` directory, per RC-FLAG-4
  disposition added explicitly to `.gitignore`), `.tex` fragment
  emit (NOT gitignored — under `notes/stochastic_fx_tex/`), and the
  consolidated `notes/STOCHASTIC_FX_RESULTS.md` emit (committed).

- `test_saas_stochastic_fx.py` — Hypothesis property tests per
  generator (statistical-property invariants of the path
  distribution), regression-vs-zero-volatility-degenerate-limit
  per Pin Z1.3a, moment-match tests per Pin Z1.3b, KS-test
  reproducibility tests per Pin Z1.4, audit_block-determinism tests
  per Pin Z1.2.

## §4 Data flow + per-family math content

### §4.1 Data flow (per SDE family)

(Reframed in v0.2 per MQ-BLOCK-1/2/3 disposition. The previous
"symbolic phase derives σ_T distribution" was infeasible — sympy
cannot perform Itô calculus. The current framing splits the symbolic
work into a trivial algebraic substitution (Z1.3a) and a hand-derived
moment match (Z1.3b), and replaces the under-specified KS test with
a moment-matched parametric reference (Z1.4).)

1. **Parameter container construction** — `GBMParameters(...)` (or OU /
   jump-diffusion variant). Frozen-dc `__post_init__` validates: all
   numeric fields finite; volatility parameters > 0; spot > 0;
   step size > 0; number of steps ≥ 2; family-specific constraints
   (OU mean-reversion rate > 0; jump-diffusion jump intensity ≥ 0).
   Canonical numerical pins per §4.2 table.

2. **Path generation** — generator's `__call__(rng_seed, n_paths)`
   returns a `PathEnsemble`. Uses `numpy.random.default_rng(rng_seed)`
   for reproducibility per Pin Z1.2. The (N × T+1) path matrix is
   produced by the family-specific SDE discretization (GBM:
   Euler-Maruyama on log-scale; OU: exact transition; jump-diffusion:
   Euler + compound-Poisson augmentation).

3. **σ_T computation** — `compute_sigma_t_per_path(ensemble)` applies
   PRIMITIVES.md §6 eq. (7) DISCRETELY to each sampled path
   (matches the B1 plan's σ_T contract per MQ-FLAG-B1.1
   disposition).

4. **Three-tier verification per family** (replaces v0.1's symbolic +
   KS pipeline; addresses BLOCK-MQ-1/2/3):
   - **Phase A — Algebraic inversion (Pin Z1.3a, family-agnostic, trivial).**
     For each path, verify pointwise that
     `apply_inversion(σ_T_n, x_bar) == sqrt(8·σ_T_n / x_bar²)` to
     float64 precision. This is an algebraic substitution that sympy
     handles in O(1ms). PASS iff residual ≤ `NUMERICAL_IDENTITY_TOL`
     (1e-6, reuses cohort_4 convention). Family-agnostic; passes
     trivially under all three families.
   - **Phase B — Mean match against hand-derived analytic (Pin Z1.3b, v0.4).**
     Per family, compute empirical `mean(σ_T_n)` across the N-path
     ensemble. Compare against hand-derived analytic `E[σ_T]` for the
     DISCRETE eq. (7) statistic at the canonical grid (Hull,
     Karatzas-Shreve, Andersen-Piterbarg literature; per
     `simulations/stochastic_fx/variance_proxy.py` discrete-moment
     functions added in Task 4.2 per plan §16.4 disposition b1).
     PASS iff relative error on the MEAN ≤ `MOMENT_REL_TOL` (default
     0.05). v0.4 amendment: variance was REMOVED from the Phase B gate
     because at the Pin Z1.5 anti-fishing floor `N=1000`, the
     sample-variance estimator's intrinsic standard error is 8-30% per
     family (MC-noise budget probe: GBM 11%/22%/51% median/p90/max,
     OU 5%/11%/18%, Merton 18%/54%/96%), structurally unsatisfiable
     against `MOMENT_REL_TOL=0.05` regardless of analytic-Var
     correctness. Full-distribution match (which constrains variance,
     skew, kurtosis jointly via the empirical CDF) is preserved at
     Phase C. The verdict's `phase_b_var_rel_err` field is still
     computed and reported as an audit-trail observation but does NOT
     gate composite_pass. See §11.6 CORRECTIONS-α for the disposition
     record + the implementer's BLOCK probe at
     `scratch/2026-05-13-task-4.2-discrete-moments/derivation.py`.
   - **Phase C — KS goodness-of-fit against moment-matched reference (Pin Z1.4).**
     Fit a parametric reference distribution (gamma OR lognormal,
     selected per family in §4.2) to the analytic `E[σ_T]` and
     `Var[σ_T]`. KS-test empirical `σ_T_n` samples against this
     reference distribution. PASS iff `ks_pvalue ≥ 0.01` (calibrated
     to a MC-noise-matched reference — see §8 anti-fishing posture
     for the rationale).

5. **Emit** — five artifacts per family:
   - Parquet: `simulations/stochastic_fx/data/path_ensemble_{family}.parquet`
     (NEW gitignore line `simulations/stochastic_fx/data/`; RC-FLAG-4
     disposition).
   - JSON: `simulations/stochastic_fx/data/inversion_verdict_{family}.json`
     (same gitignore).
   - LaTeX fragment for the algebraic inversion:
     `notes/stochastic_fx_tex/eps_inversion_{family}.tex` (committed).
   - LaTeX fragment for the variance dynamics:
     `notes/stochastic_fx_tex/sigma_t_moments_{family}.tex` (committed
     — the genuinely non-trivial mathematical content per BLOCK-MQ-3).
   - Consolidated summary `notes/STOCHASTIC_FX_RESULTS.md` once all
     three families have verdicts; R-tagged sections per family.

### §4.2 Variance dynamics per family (new in v0.2 per BLOCK-MQ-3)

The non-trivial mathematical content per family is the hand-derived
analytic `E[σ_T]` and `Var[σ_T]`. These are HAND-DERIVED (from
literature), not sympy-derived (sympy cannot perform Itô calculus).
Sympy is used only to (a) algebraically simplify the final closed
forms and (b) render LaTeX fragments via `sympy.latex(...)`.

**Per-family parameter pin table (Pin Z1.1 + Pin Z1.3b anchor).**
These values are FROZEN at this commit; ex-post adjustment requires
CORRECTIONS-α + scoped Wave-1 re-review per Pin Z1.5. Canonical
values consistent with the cohort_5_strip canonical fixture
(`x_bar = X̄/Ȳ = 4000`, ε = 0.1, T = 12 months):

| Family | Pinned parameters | Reference distribution for Phase C |
|---|---|---|
| **GBM** | drift μ = 0; volatility σ = 0.10/√12; spot x_0 = 4000; horizon T = 12; n_steps = 5000 (matches cohort_4 Nyquist convention) | Lognormal (σ_T is positive, right-skewed under GBM) |
| **OU** | mean-reversion θ = 1.0; long-run mean μ̄ = 4000; volatility σ = 0.10·4000/√(2·1.0); spot x_0 = 4000; T = 12; n_steps = 5000 | Gamma (chi-squared-like stationary distribution) |
| **Merton jump-diffusion** | drift μ = 0; diffusion σ = 0.05/√12 (half-attribution to diffusion); jump intensity λ = 1/year; jump-size mean μ_J = 0; jump-size std σ_J = 0.10; spot x_0 = 4000; T = 12; n_steps = 5000 | Lognormal (compound-Poisson + lognormal-diffusion is approximately lognormal at moderate λ) |

**Hand-derived analytic moments** (rendered as `.tex` fragments per
family in `notes/stochastic_fx_tex/sigma_t_moments_{family}.tex`):

| Family | E[σ_T] (analytic, hand-derived) | Reference for derivation |
|---|---|---|
| GBM (mean-zero drift) | E[σ_T] = (X̄/Ȳ)² · [(e^{σ²T} − 1)/(σ²T) − 1] (exact under lognormal-centered estimator); leading-order ≈ (X̄/Ȳ)² · σ²T/2 (NEW-BLOCK-MQ-4 disposition: previous v0.2 form omitted the `− 1` correction inside the brackets, producing a residual constant of `(X̄/Ȳ)²` at σ→0 that contradicted the trivial-degenerate-limit claim. Corrected form vanishes at σ→0 as required.) | Hull §15 Itô variance estimator |
| OU (stationary) | E[σ_T] = σ²/(2θ) exactly | Standard OU stationary variance |
| Merton jump-diffusion (mean-zero drift) | E[σ_T] = (X̄/Ȳ)²·σ²·T + λ·(X̄/Ȳ)²·(e^{2(μ_J+σ_J²)} − 2e^{μ_J+σ_J²/2} + 1)·T (leading order) | Andersen-Piterbarg Vol I §2.7 |

`Var[σ_T]` analytic forms are similarly hand-derived per family (see
the corresponding `.tex` fragments). These tables are the canonical
authority for Pin Z1.3b moment-match gate.

**Trivial-degenerate limit** (replaces v0.1's "reduces to eq. (6)" claim
per BLOCK-MQ-1). For each family, the zero-volatility-and-zero-jump
limit collapses to a point mass at x_0:

- GBM: σ → 0 ⟹ X_t ≡ x_0 ⟹ σ_T ≡ 0 ⟹ ε ≡ 0 (point mass).
- OU: σ → 0 (or θ → ∞) ⟹ X_t ≡ μ̄ ⟹ σ_T ≡ 0 ⟹ ε ≡ 0 (point mass).
- Merton: σ → 0 AND λ → 0 ⟹ X_t ≡ x_0 ⟹ σ_T ≡ 0 ⟹ ε ≡ 0 (point mass).

This is a trivial degeneracy, not a reduction to eq. (6) (which is
not the limit of any of these families along their parameter axes —
eq. (6) requires a periodic drift kernel none of these families has).
This is documented honestly as Pin Z1.3a's family-agnostic baseline,
not as a non-trivial verification. The genuine verification content
lives in Phase B (moment match per Pin Z1.3b) and Phase C (KS
goodness-of-fit per Pin Z1.4).

## §5 Pin coverage

| Pin | Description | Verifiable as |
|---|---|---|
| **Z1.1** | SDE parameters pre-pinned at spec authorship time (this v0.2 §4.2 per-family table) BEFORE running any verification phase. Post-hoc adjustment requires CORRECTIONS-α + scoped Wave-1 re-review per Pin Z1.5 / master-spec §6.4. | Spec text + commit anchor + diff visibility. |
| **Z1.2** | Path-ensemble determinism: same `rng_seed` → bit-exact ensemble AND bit-exact `audit_block`. | Hypothesis property test on (rng_seed, n_paths) → (ensemble, audit_block). |
| **Z1.3a** | Algebraic inversion (family-agnostic): for each path, the pointwise identity `apply_inversion(σ_T_n, x_bar) == √(8·σ_T_n/x_bar²)` holds to float64 precision. (Replaces v0.1's ill-posed "reduces to eq. (6)" claim per BLOCK-MQ-1.) Per family, the trivial-degenerate limit (σ → 0, θ → ∞, λ → 0) yields the trivial point mass ε ≡ 0; this is documented honestly as the family-agnostic baseline, not as a non-trivial test. | Pointwise residual ≤ NUMERICAL_IDENTITY_TOL (1e-6). |
| **Z1.3b** (v0.4) | Mean match against hand-derived analytic (per family): empirical `mean(σ_T_n)` across the N-path ensemble matches the hand-derived analytic `E[σ_T]` of the DISCRETE eq. (7) statistic at the canonical grid (Hull / Karatzas-Shreve / Andersen-Piterbarg; per `variance_proxy.py` discrete-moment functions added in Task 4.2 per plan §16.4 disposition b1). v0.4 dropped variance from this gate (was structurally unsatisfiable at N=1000 due to intrinsic 8-30% MC-noise floor on Var estimator — see §11.6). Variance rel-err is still computed and emitted to `InversionVerdict.phase_b_var_rel_err` as audit-trail observation but does not gate composite_pass. Full-distribution match (which jointly constrains all moments via empirical CDF) is preserved at Z1.4 KS test. | Relative error on the MEAN ≤ MOMENT_REL_TOL (default 0.05). |
| **Z1.4** | KS goodness-of-fit against moment-matched parametric reference (per family): fit a parametric reference distribution (lognormal for GBM/Merton, gamma for OU per §4.2 table) to the analytic `E[σ_T]` and `Var[σ_T]`; KS-test empirical `σ_T_n` samples against this reference. (BLOCK-MQ-2 disposition: replaces v0.1's tautological-or-infeasible KS framing with moment-matched parametric reference per MQ recommendation reading (c).) PASS iff `ks_pvalue ≥ 0.01` (calibration documented in §8). | `scipy.stats.ks_1samp` against the family's fitted reference; N ≥ 1000 paths. |
| **Z1.5** | Anti-fishing routing: observed family-level test FAILURES at Z1.3a / Z1.3b / Z1.4 route to CORRECTIONS-α + scoped Wave-1 re-review per master-spec §6.4. NEVER silent parameter re-tuning. NEVER "increase N until passing" — the N=1000 floor is a Z1.5 invariant, not a parameter to grow. | HALT-routing table in §6 of this spec; verification at Wave-2 review. |
| **Z1.6** | Strip preservation: cohort_5_strip's `IronCondor_strip.json` audit_block (`94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329`) is UNCHANGED before and after this spec's implementation. (RC-FLAG-3 disposition: verification by direct hex grep on the JSON file, not just `git log -p`.) | Bash: `grep -F '94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329' simulations/saas_builder/data/IronCondor_strip.json` returns the audit_block line before AND after the stochastic-fx package merge. |

## §6 Exit criteria and HALT routing

**Exit (track closure):**

- Package `simulations/stochastic_fx/` ships with three-tier discipline
  intact (ruff + ty clean).
- All three SDE families produce InversionVerdict with `passes = True`
  at the pre-pinned (Z1.1) canonical parameters.
- `notes/STOCHASTIC_FX_RESULTS.md` lands with R-tagged sections per
  family.
- Wave-1 RC+MQ ACCEPT on this spec; Wave-2 RC+MQ ACCEPT on the
  implementation's exit deliverables.
- `simulations/saas_builder/data/IronCondor_strip.json` audit_block
  unchanged (Pin Z1.6).

**HALT routing:**

| Trigger | Route |
|---|---|
| Pin Z1.3a algebraic inversion residual > 1e-6 | HALT — float64 numerical defect; investigate `apply_inversion` implementation. This is family-agnostic, so failure indicates a bug, not a family-level scientific result. |
| Pin Z1.3b MEAN match relative error > MOMENT_REL_TOL per family (v0.4 mean-only gate) | HALT — CORRECTIONS-α; either (a) hand-derived analytic `E[σ_T]` of the DISCRETE statistic is wrong (re-derive against literature; expansion uses centering projection `M = I − (1/N)·1·1^T` against the SDE family's auto-covariance kernel; see §4.2), OR (b) the SDE discretization in `generators.py` doesn't faithfully sample the SDE's stationary measure (refine the discretization — e.g., switch from Euler-Maruyama to a higher-order scheme). NEVER adjust SDE parameters to pass. Variance is no longer in this gate (v0.4 §11.6 disposition) — full-shape match constraint lives at Pin Z1.4. |
| Pin Z1.4 KS p-value < 0.01 per family | HALT — CORRECTIONS-α + scoped Wave-1 re-review per master-spec §6.4. The KS failure is a structural rejection of the family's distributional fit to the moment-matched reference; honest dispositions are (a) drop the family from the spec, (b) substitute a different reference distribution shape (e.g., gamma for a previously-lognormal family), (c) refine the discretization. NEVER "increase N until passing" — that's the §8 anti-fishing posture violation. |
| Pin Z1.6 audit_block hex grep fails (strip mutated) | HALT — implementation is anti-fishing-coupled to cohort_5_strip; route to cohort_5_strip review. |
| Wave-1 or Wave-2 RC+MQ on this spec returns BLOCK | HALT per master-spec §6.1; CORRECTIONS-α in §11. |

## §7 Out of scope of this spec (deferred)

Two sub-projects are explicitly DEFERRED to their own brainstorm
cycles. This spec provides integration HOOKS for both but does NOT
implement them.

### §7.1 cadCAD integration (deferred)

cadCAD is a system-dynamics simulation framework usable across ALL
cohorts and on-chain market dynamics. It is NOT stochastic-FX-specific
and warrants its own brainstorm cycle. This spec's PathEnsemble Value
type is a frozen-dc with `paths: NDArray[(N, n_steps+1)]` that cadCAD's
State-Update-Block (SUB) interface can consume directly without
translation. The Callable-tier `GBMPathGenerator(rng_seed=k, n_paths=1)`
can be invoked per-cadCAD-timestep for the streaming pattern, OR called
once with N=ensemble_size for the batch pattern. The variance-proxy
verifier is a frozen-dc Callable that cadCAD's Policy block can call
to compute σ_T as a state variable. No further work needed in this
spec to enable that future integration.

### §7.2 LaTeX-econ-paper consolidator (deferred)

A consolidated LaTeX writeup pulling together PRIMITIVES.md, Stage-2
R1–R8, cohort_5_strip Carr-Madan replication, Stage-3 first-wave
verdicts (A1 KEEP + A2 K⋆ + B1 forge), and stochastic-FX results is
a separate brainstorm cycle. This spec emits two integration artifacts
for that future paper:

- `notes/stochastic_fx_tex/eps_inversion_{family}.tex` — per-family
  LaTeX fragments emitted via `sympy.latex()` containing the analytic
  ε(σ_T) form. Future paper uses `\input{}` directly; no copy-paste,
  no derivation re-render.
- `notes/STOCHASTIC_FX_RESULTS.md` — parallel to STAGE_2_RESULTS.md;
  consumed by the future paper as a markdown source for narrative.
- `InversionVerdict.tex_anchor: str` field points to the fragment file
  per family, enabling deterministic cross-reference.

### §7.3 Equilibrium distributional test (K_l = K_s)

The PRIMITIVES.md (14) equilibrium identity `K_l = K_s` was Stage-2-
verified for the deterministic path. Verifying it holds IN EXPECTATION
under stochastic FX is a stronger claim and a substantial math task.
Deferred to a THIRD-wave spec ("stochastic-equilibrium-test-design").

### §7.4 Empirical-calibrated bootstrap

Drops PRIMITIVES eq. (8) inversion; out of scope per the brainstorm
choice to retain the closed-form inversion identity.

### §7.5 Re-emission of cohort_5_strip under stochastic expectations

Anti-fishing-banned (would be a strip retuning). Pin Z1.6 enforces.

## §8 Anti-fishing posture

- SDE parameter values for each family are PRE-PINNED in §4.2's
  per-family parameter table BEFORE any verification phase runs.
  Canonical values are diff-visible at the v0.2 commit; ex-post
  tuning requires CORRECTIONS-α + fresh Wave-1 review.
- Family-level test FAILURES at Z1.3a / Z1.3b / Z1.4 are SCIENTIFIC
  RESULTS, not tuning triggers (Pin Z1.5). A failed family is
  documented honestly, not silently dropped or retuned to PASS.
- The hand-derived analytic moments in §4.2 are taken from literature
  (Hull, Andersen-Piterbarg) — NOT chosen to match an observed Monte-
  Carlo distribution. Literature anchor for each formula is cited
  per family in the corresponding `.tex` fragment.
- **KS-gate calibration (Pin Z1.4 threshold = 0.01 vs the conventional
  0.05).** Per FLAG-MQ-1 in the v0.1 review: the 0.01 threshold is
  permissive (vs the conventional 0.05) but is chosen here because the
  test compares two MC-noise-bearing estimates of the same population
  quantity — empirical σ_T_n from the family's discretized paths vs
  a parametric reference fit to the family's hand-derived analytic
  moments. The reference itself carries finite-sample uncertainty
  (the discretization-implied moments converge to the analytic
  moments only in the dt → 0 limit). A 0.01 threshold tolerates that
  shared MC-noise floor while still rejecting genuine distributional
  mismatches. **This calibration is FROZEN at v0.2 §8; ex-post
  tightening (e.g., to 0.05) is admissible ONLY as a CORRECTIONS-α
  v0.x → v0.(x+1) with documented rationale.**
- **N-floor anti-fishing rule (Pin Z1.4 + Pin Z1.5).** Pin Z1.4
  specifies `N ≥ 1000` as the MC-budget floor. This is a FLOOR, not a
  parameter to grow. "Increasing N until the KS test passes" is an
  anti-fishing pattern (peeking under the budget knob until the gate
  trips green). If the family's KS test fails at N=1000, the family's
  test FAILS — not "needs more paths". Honest dispositions per Pin
  Z1.5 routing: drop the family, substitute the reference distribution
  shape, OR refine the discretization. NEVER increase N silently.
- Strip preservation (Pin Z1.6) prevents the most subtle anti-fishing
  pattern: re-emitting cohort_5_strip under stochastic-path expectations
  would let stochastic-FX results retroactively justify the existing
  strip. Pin Z1.6 keeps the strip-emit pinned at its deterministic-
  fixture commit (`3442852`); verification by direct hex grep on the
  audit_block per RC-FLAG-3 disposition.
- **No "deterministic limit reduces to eq. (6)" claim** (BLOCK-MQ-1
  disposition). v0.1 made this claim and it was mathematically
  ill-posed (none of GBM/OU/Merton has a periodic drift kernel
  matching eq. (6)). v0.2 documents the trivial-degenerate limit
  honestly as "all three families reduce to a point mass at x_0 under
  zero-volatility-and-zero-jump; this is a trivial degeneracy, not a
  reduction to eq. (6)." See §4.2.

## §9 Anti-coupling guard

This spec is INDEPENDENT of the first-wave Stage-3 tracks (A1 / A2 /
B1). The first-wave master spec's §3 cross-track dependency graph is
NOT extended to include stochastic-FX. Reasons:

1. No first-wave artifact is consumed by this spec.
2. No first-wave artifact is mutated by this spec.
3. The deferred integration hooks (§7.1 cadCAD, §7.2 LaTeX) are
   STRUCTURAL ONLY — passive interfaces, not active dependencies.

If stochastic-FX implementation is paused, abandoned, or fails, the
first-wave tracks are unaffected. Conversely, if a first-wave track
hits a BLOCK, stochastic-FX continues unimpeded.

## §10 Wave-1 RC+MQ review protocol

Per master-spec §6.1, both RC and MQ reviewers dispatch in parallel
on this spec v0.1 BEFORE any implementation begins. Verdict files:

- `scratch/2026-05-11-stochastic-fx-spec-review/rc-verdict.md`
- `scratch/2026-05-11-stochastic-fx-spec-review/mq-verdict.md`

Same Delphi-independence safeguards as the master spec's Wave-1
(identical context to both reviewers; orchestrator does NOT preview
either verdict before both land).

Wave-1 ACCEPT or ACCEPT_WITH_FLAGS-disposed → writing-plans skill
authoring of `docs/plans/2026-05-NN-stochastic-fx-variant.md` follows
in a subsequent brainstorm cycle.

## §11 CORRECTIONS-α (patch log)

### §11.1 v0.1 → v0.2 (Wave-1 RC ACCEPT_WITH_FLAGS + MQ BLOCK disposition)

**Wave-1 v0.1 review verdict:**
- RC: ACCEPT_WITH_FLAGS (1 material FLAG-RC-1 on §3 code-like signatures; 3 NITs).
- MQ: **BLOCK** (3 high-severity findings BLOCK-MQ-1/2/3 on math framing).

Verdict files:
- `scratch/2026-05-11-stochastic-fx-spec-review/rc-verdict.md`
- `scratch/2026-05-11-stochastic-fx-spec-review/mq-verdict.md`

Per master-spec §6.1 protocol, MQ BLOCK requires HALT + revise +
re-dispatch BOTH reviewers. v0.2 lands the revisions below; v0.2
Wave-1 re-review follows.

| Finding | Severity | Disposition | Location |
|---|---|---|---|
| **BLOCK-MQ-1** | High | Pin Z1.3 split into Z1.3a (algebraic inversion, family-agnostic, trivial substitution) and Z1.3b (per-family moment match against hand-derived analytic moments). The v0.1 "reduces to eq. (6)" claim was mathematically ill-posed (none of GBM/OU/Merton has periodic drift kernel); replaced with honest "trivial degenerate limit yields point mass at x_0" in §4.2. | §4.2 trivial-degenerate-limit note + §5 Pin Z1.3a / Z1.3b split |
| **BLOCK-MQ-2** | High | Pin Z1.4 reframed to MQ's recommended reading (c): moment-matched parametric reference. Empirical σ_T_n is KS-tested against a gamma OR lognormal reference fit to the family's hand-derived analytic E[σ_T] and Var[σ_T]. v0.1's "pushforward via same σ_T samples" tautology removed. | §4.1 Phase C + §5 Pin Z1.4 |
| **BLOCK-MQ-3** | High | New `moments.py` Callable-tier module added in v0.2. Hand-derived analytic moments per family (Hull / Andersen-Piterbarg) replace the v0.1 sympy-derives-σ_T-distribution claim (which was infeasible — sympy cannot perform Itô calculus). Sympy is now scoped to (a) the trivial algebraic inversion in `variance_proxy.py` and (b) `sympy.latex()` rendering of the hand-derived moment expressions into `.tex` fragments. | §3 moments.py file added + §4.2 hand-derived moment tables + §5 Pin Z1.3b |
| **FLAG-MQ-1** | Medium | KS-gate calibration rationale documented in §8: 0.01 vs 0.05 chosen because the test compares two MC-noise-bearing estimates of the same population quantity. Explicit "never increase N until passing" rule added. | §8 |
| **FLAG-MQ-2** | Medium | §4.2 per-family table makes the family-parameter dependence of E[ε(σ_T)] explicit. The mapping `ε ↔ σ_T` is now framed honestly as a pointwise algebraic identity (Z1.3a) plus a distributional moment match (Z1.3b), not as a family-independent inversion. | §4.2 |
| **NIT-MQ-1** | Low | §4.1 step 3 explicitly cites the B1 plan's σ_T discrete contract (MQ-FLAG-B1.1 disposition) to keep the discretization convention consistent across specs. | §4.1 |
| **FLAG-RC-1** | Material | §3 ASCII tree's typed function signatures removed; per-file responsibilities described in prose per `memory/feedback_no_code_in_specs_or_plans.md`. | §3 |
| **NIT-RC-2** | Low | §1 cross-references table now phrases PRIMITIVES.md §15 as "open item 2 (by bullet count)" with the caveat that §15 uses unnumbered bullets — no source numbering to anchor against; bullet count is the unambiguous reference. | §1 |
| **NIT-RC-3** | Low | Pin Z1.6 verification switched from `git log -p` (proves file unchanged but not audit_block unchanged) to direct hex grep on the audit_block in the JSON file (proves both). | §5 Pin Z1.6 |
| **NIT-RC-4** | Low | §4.1 step 5 ("Emit" section) clarifies that the new `simulations/stochastic_fx/data/` directory will require a NEW gitignore line (existing line 53 covers `simulations/saas_builder/data/` only). | §4.1 step 5 |

### §11.2 Outstanding repo work (NOT this spec)

The following are NOT spec changes but repo work that must land before
implementation begins (RC-FLAG-4 disposition):

1. **New `.gitignore` line.** Add `simulations/stochastic_fx/data/` to
   `.gitignore` per RC-FLAG-4. Single-line addition; lands in the
   stochastic-fx-package implementation plan's first task, NOT in this
   spec.

### §11.3 v0.2 Wave-1 re-review (landed)

- RC v0.2 verdict: ACCEPT_WITH_FLAGS — 2/4 prior FLAGs closed; 2 residual
  (FLAG-RC-1-v2 material on §3 function signatures still in inline
  backticks; FLAG-RC-2-v2 NIT on §1 §15 bullet-count caveat).
- MQ v0.2 verdict: BLOCK — three prior BLOCKs DISPOSED satisfactorily;
  one NEW high-severity finding NEW-BLOCK-MQ-4 on §4.2 GBM E[σ_T]
  formula (missing `− 1` correction inside brackets; spec form fails
  the trivial-degenerate-limit at σ→0).

Verdict files:
- `scratch/2026-05-11-stochastic-fx-spec-review/wave-1-v0.2/rc-verdict.md`
- `scratch/2026-05-11-stochastic-fx-spec-review/wave-1-v0.2/mq-verdict.md`

### §11.4 v0.2 → v0.3 (NEW-BLOCK-MQ-4 disposition + FLAG-RC-1-v2 closure)

| Finding | Severity | Disposition | Location |
|---|---|---|---|
| **NEW-BLOCK-MQ-4** | High | §4.2 GBM `E[σ_T]` row corrected from `(X̄/Ȳ)²·(e^{σ²T}−1)/(σ²T)` to `(X̄/Ȳ)² · [(e^{σ²T}−1)/(σ²T) − 1]` (exact); leading-order `≈ (X̄/Ȳ)² · σ²T/2`. Restores the σ→0 vanishing limit required by §4.2's trivial-degenerate-limit framing. | §4.2 GBM row |
| **FLAG-RC-1-v2** | Material | §3 variance_proxy.py prose-ified: function signatures with `(...) → return-type` syntax removed; per-file responsibility described in prose only; implementation signatures deferred to plan. | §3 variance_proxy.py bullet |
| **FLAG-RC-2-v2** | NIT | Deferred to a v0.3.1 cosmetic patch if required by Wave-1 re-review. §1 §15 reference uses "open item 2 (by bullet count)" framing in §11.1 disposition; explicit inline caveat at §1 not added in v0.3 to keep the patch narrow. | (deferred) |

### §11.5 v0.3 Wave-1 re-review reserve

Per master-spec §6.1, BOTH RC and MQ re-dispatch on v0.3. Narrow-scope
per MQ's own note ("Re-review will be narrow-scope"); verdicts land
in `scratch/2026-05-11-stochastic-fx-spec-review/wave-1-v0.3/`.

### §11.6 v0.3 → v0.4 (Pin Z1.3b mean-only gate; user disposition Option B, 2026-05-13)

**Trigger.** During Task 4.2 (`InversionVerifier` Phase A+B+C combiner)
implementation, the dispatched implementer (AI Engineer) hand-derived
the discrete eq. (7) statistic's analytic moments per family
(disposition b1 per plan §16.4) and ran a Monte-Carlo-noise budget
probe at the Pin Z1.5 anti-fishing floor `N=1000`. The probe
characterized the intrinsic standard error of the SAMPLE variance
estimator across 100 independent seeds per family:

| Family | median rel-err on Var | p90 | max | fraction within ±5% |
|---|---|---|---|---|
| GBM | 11.0% | 22.1% | 51.3% | 28% |
| OU | 5.2% | 11.2% | 18.3% | 46% |
| Merton | 18.4% | 53.5% | 95.5% | 12% |

The MC standard error on the sample variance at N is `SE_Var ≈
sqrt((κ_eff − 1) / (N − 1)) · Var`, where `κ_eff` is the kurtosis-like
4th-cumulant factor of the σ_T statistic. For canonical-pin families,
`κ_eff` is in the range 4-35 (MQ-V0.4-3 disposition: empirical Merton
κ_eff at canonical pin lands at 33-35 because of jump heavy tails;
the GBM/OU pair sits in 4-12). At N=1000, `SE_Var/Var` is intrinsically
8-30% regardless of analytic-Var correctness — the MC-noise budget
incompatibility with `MOMENT_REL_TOL=0.05` holds a fortiori at the
revised upper κ_eff range.

**Pins Z1.3b and Z1.5 were mathematically incompatible at v0.3.** Pin
Z1.5 fixed N=1000 as anti-fishing (NEVER raise to pass); Pin Z1.3b
required rel-err ≤ 5% on Variance. These two cannot both hold for
canonical-pin parameters. The implementer correctly halted before
committing any code — exactly the §16-anticipated BLOCK scenario.

**User disposition (Option B, 2026-05-13):** drop variance from the
Pin Z1.3b gate. Phase B becomes mean-only. Phase C's KS test against
the moment-matched reference distribution (constructed from analytic
E AND analytic Var per the NIT-MQ-1 method-of-moments construction)
preserves the full-distribution constraint that variance-match would
have separately provided.

**Why Option B over Option A (per-family variance tolerance
calibrated to MC budget):**

1. KS at Phase C jointly constrains mean + var + skew + kurtosis via
   the empirical CDF. A separate variance gate is redundant.
2. Single tolerance `MOMENT_REL_TOL = 0.05` preserved across families —
   no per-family tuning surface (which would look like fishing even
   when calibrated).
3. Smaller spec diff than Option A.

**Why NOT Option D (fall back to b3 — replace Phase B with KS):** the
b1 disposition's hand-derived analytic E[σ_T] is mathematically
nontrivial (especially Merton with `μ_j = x_0 · φ₁^j` jump-induced
drift) and provides a genuinely independent check on the SDE
discretization. Retaining mean-match anchors phase B to literature
(Hull, Karatzas-Shreve, Andersen-Piterbarg) rather than dissolving
it into a second KS test.

**Implementer's b1 analytic E[σ_T] formulas (load-bearing for the
amended Pin Z1.3b)** — verified empirically at canonical pins with
N=1000 producing 0.17% (OU), 0.70% (Merton), 1.12% (GBM) rel-err on
the mean. All three families HAND-DERIVED, transcribed to Python in
`simulations/stochastic_fx/variance_proxy.py` (forthcoming commit;
scratch derivation at `scratch/2026-05-13-task-4.2-discrete-moments/derivation.py`):

- **GBM** (Hull §15 / log-multiplicative martingale at μ=0):
  `Cov(X_j, X_k) = x_0² · (exp(σ² · min(t_j, t_k)) − 1)` where
  `t_j = j · dt`. Mean of σ_T uses centering projection
  `M = I − (1/N)·1·1ᵀ`, yielding `E[σ_T·T] = tr(M Σ_GBM) +
  μᵀ M μ` with `μ_j ≡ x_0` (constant) so `μᵀ M μ = 0`.

- **OU stationary** (Karatzas-Shreve §5.6 / Glasserman §3.3 exact
  transition; canonical `x_0 = μ_bar` so `μ_j ≡ μ_bar` and
  `μᵀ M μ = 0`): `Cov(X_j, X_k) = (σ² / (2θ)) · exp(−θ · |t_k −
  t_j|) · (1 − exp(−2θ · min(t_j, t_k)))`.

- **Merton** (Andersen-Piterbarg §2.7 jump-MGF + log-multiplicative):
  `log φ₁ = λ · dt · (exp(jump_mean²/2 + jump_std²/2) − 1)` and
  `log φ₂ = σ² · dt + λ · dt · (exp(2·jump_mean² + 2·jump_std²) − 1)`
  (canonical `jump_mean = 0` simplifies the first term to
  `log φ₁ = λ · dt · (exp(jump_std²/2) − 1)`). Drift
  `μ_j = x_0 · φ₁^j` (NOT constant — drifts ~6% over T at canonical
  λ), so `μᵀ M μ ≠ 0`; full expansion required.
  `Cov(X_j, X_k) = x_0² · φ₁^{|k−j|} · (φ₂^{min(j,k)} −
  φ₁^{2·min(j,k)})`.

The variance derivations under the Isserlis Gaussian-quadratic-form
approximation are EXACT for OU (Gaussian process), 8% under-estimating
for GBM (lognormal — missing 4th-cumulant terms), and 71%
under-estimating for Merton (jump heavy kurtosis). Even with PERFECT
analytic Var these would still face the intrinsic MC-noise budget
above. The variance formulas are NOT shipped in v0.4 — they would
have been the Phase B Var comparator under the old gate; under the
v0.4 mean-only gate they are superseded by Phase C's full-shape KS.

**Wave-1 re-review:** by master-spec §6.4 BLOCK protocol, BOTH RC
and MQ re-dispatch on this amendment. NARROW scope per the change
surface — Pin Z1.3b row + §4.1 Phase B bullet + §11.6 (this section).
Re-review verdicts land at
`scratch/2026-05-11-stochastic-fx-spec-review/wave-1-v0.4/`.

## §12 References

- `notes/PRIMITIVES.md` — §5 eq. (6) (deterministic generator); §6 eq.
  (7), (8) (variance proxy + inversion); §15 open item 2 (stochastic-FX
  variant — Path A v3); §13 variable map.
- `notes/STAGE_2_RESULTS.md` — R1 σ_0 anchor (this spec verifies its
  deterministic-limit reduction per SDE family).
- `docs/specs/2026-05-11-stage-3-first-wave-design.md` v0.2 — the
  Stage-3 master spec; this spec is independent of it.
- `simulations/saas_builder/cohort_5_strip/` — commit `3442852`,
  audit `94150326…` — the strip artifact this spec preserves under
  Pin Z1.6.
- `memory/feedback_pathological_halt_anti_fishing_checkpoint.md` —
  HALT protocol.
- `memory/feedback_post_hoc_fit_anti_fishing_pattern.md` — anti-
  fishing pattern catalogue (consumed by §8 posture).
- `memory/feedback_no_code_in_specs_or_plans.md` — this spec contains
  no code; implementation lives in a separate plan.
- `superpowers:brainstorming` — flow that produced this spec.
- `superpowers:writing-plans` — flow for the implementation plan to
  follow.

---

*End of stochastic-FX variant design spec v0.1. Independent RC + MQ
Wave-1 review dispatch by the orchestrator before any implementation
begins.*
