---
spec_id: stochastic-fx-variant-design
spec_version: v0.1 (initial draft — awaiting RC + MQ Wave-1 review)
emit_timestamp_utc: 2026-05-11
parent_framework: notes/PRIMITIVES.md §15 open item — "Path A v3" stochastic-FX variant
stage_2_results_anchor: notes/STAGE_2_RESULTS.md (R1–R8 closed forms under deterministic eq. (6))
stage_3_first_wave_spec: docs/specs/2026-05-11-stage-3-first-wave-design.md v0.2 (the master Stage-3 spec; this spec is a parallel second-wave sub-project)
strip_anchor: simulations/saas_builder/cohort_5_strip/ (commit 3442852, audit_block 94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329)
authority: CLAUDE.md anti-fishing invariants (NON-NEGOTIABLE); brainstorming flow; memory/feedback_pathological_halt_anti_fishing_checkpoint.md
predecessor: none (first stochastic-FX spec)
status: DRAFT — awaiting §10 Wave-1 RC+MQ 2-way review (both reviewers per wave)
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

```
simulations/stochastic_fx/
├── __init__.py                       Public API re-exports
├── _errors.py                        StochasticFXError (base) +
│                                     SDEParameterError +
│                                     InversionTestFailedError +
│                                     MCBudgetExceededError (reuse cohort_4 convention)
├── types.py                          Value tier
│   - GBMParameters (mu, sigma, x_0, T, dt, n_steps)
│   - OUParameters (theta, mu_bar, sigma, x_0, T, dt, n_steps)
│   - JumpDiffusionParameters (mu, sigma, lambda_jump, jump_mean,
│                              jump_std, x_0, T, dt, n_steps)
│   - PathEnsemble (family_id, paths: NDArray[(N, n_steps+1)],
│                   sigma_T_per_path: NDArray[(N,)], audit_block,
│                   parameters_canonical_json)
│   - InversionVerdict (family_id, sympy_form_passes: bool,
│                       sympy_residual: float, mc_ks_pvalue: float,
│                       mc_n_paths: int, deterministic_limit_passes: bool,
│                       passes: bool, tex_anchor: str, audit_block)
├── generators.py                     Callable tier
│   - GBMPathGenerator (frozen-dc, __call__(rng_seed: int, n_paths: int)
│                       → PathEnsemble)
│   - OUPathGenerator (similar)
│   - JumpDiffusionPathGenerator (similar)
├── variance_proxy.py                 Callable tier
│   - sympy_inversion_check_gbm(parameters) → (analytic_eps_expr,
│     deterministic_limit_residual)
│   - sympy_inversion_check_ou(parameters) → (analytic_eps_expr,
│     deterministic_limit_residual)
│   - sympy_inversion_check_jump(parameters) → (analytic_eps_expr,
│     deterministic_limit_residual)
│   - mc_inversion_check(ensemble: PathEnsemble, x_bar: float)
│     → (ks_pvalue, empirical_eps_array)
│   - InversionVerifier (frozen-dc, __call__(parameters, ensemble, x_bar)
│                        → InversionVerdict, combining symbolic + MC)
├── emit.py                           IO Boundary tier
│   - PathEnsembleEmitter (writes parquet under
│                          simulations/stochastic_fx/data/, gitignored)
│   - InversionVerdictEmitter (writes JSON v1.0 schema, gitignored)
│   - TexFragmentEmitter (writes .tex fragments under
│                         notes/stochastic_fx_tex/, NOT gitignored)
│   - StochasticFXResultsEmitter (writes
│                                 notes/STOCHASTIC_FX_RESULTS.md,
│                                 committed)
└── tests/                            (under simulations/tests/)
    - test_saas_stochastic_fx.py       Hypothesis property tests +
                                       regression-vs-deterministic +
                                       inversion-verifier tests per family
```

## §4 Data flow

For each SDE family the pipeline is:

1. **Parameter container construction** — `GBMParameters(...)` (or OU /
   jump-diffusion variant). Frozen-dc `__post_init__` validates: all
   numeric fields finite; `sigma > 0`; `x_0 > 0`; `dt > 0`;
   `n_steps >= 2`; family-specific constraints (OU: `theta > 0`;
   jump-diffusion: `lambda_jump >= 0`).

2. **Path generation** —
   `generator(rng_seed: int, n_paths: int) → PathEnsemble`. Uses
   `numpy.random.default_rng(rng_seed)` for reproducibility. Returns a
   PathEnsemble with the (N, n_steps+1) path matrix and per-path σ_T
   computed via PRIMITIVES eq. (7) DISCRETELY on the sampled path
   (matches the B1 plan's σ_T contract — MQ-FLAG-B1.1 disposition).

3. **Inversion verification** —
   `InversionVerifier()(parameters, ensemble, x_bar) → InversionVerdict`:
   - **Symbolic phase**: derive analytic `ε(σ_T)` for the family by
     simplifying the SDE's stationary or quasi-stationary variance
     formula. Compute `deterministic_limit_residual = |analytic_eps_expr
     evaluated at sigma→0 − √(8·σ_T_det/(X̄/Ȳ)²)|`. PASS iff
     `≤ NUMERICAL_IDENTITY_TOL = 1e-6`.
   - **MC phase**: compute empirical `ε̂_n = √(8·σ_T_n / x_bar²)` for
     each of the N paths. KS-test the empirical distribution against
     the analytic ε distribution sampled at the same N. PASS iff
     `ks_pvalue >= 0.01`.
   - Combine: `verdict.passes = sympy_form_passes AND
     deterministic_limit_passes AND (ks_pvalue >= 0.01)`.

4. **Emit** — three artifacts per family:
   - Parquet: `simulations/stochastic_fx/data/path_ensemble_{family}.parquet`
     (gitignored at `.gitignore:53` — under `simulations/saas_builder/data/`
     is gitignored; we'll add `simulations/stochastic_fx/data/` to the
     gitignore as a single-line addition).
   - JSON: `simulations/stochastic_fx/data/inversion_verdict_{family}.json`
     (gitignored).
   - LaTeX fragment: `notes/stochastic_fx_tex/eps_inversion_{family}.tex`
     (committed — used by future LaTeX-econ-paper consolidator).

5. **Summary emit** — once all 3 families have verdicts, one consolidated
   markdown emits to `notes/STOCHASTIC_FX_RESULTS.md` (parallel to
   `notes/STAGE_2_RESULTS.md`), containing R-tagged sections per family
   plus cross-family comparison plot fixtures (see §7 hook).

## §5 Pin coverage

| Pin | Description | Verifiable as |
|---|---|---|
| **Z1.1** | SDE parameters pre-pinned at spec authorship time (this v0.1 §4) BEFORE running the inversion verifier. Post-hoc adjustment requires CORRECTIONS-α and a fresh Wave-1 review. | Spec text + commit anchor. |
| **Z1.2** | Path-ensemble determinism: same `rng_seed` → bit-exact ensemble AND bit-exact `audit_block`. | Hypothesis property test on `(rng_seed, n_paths) → (ensemble, audit_block)`. |
| **Z1.3** | Variance-proxy sympy analytic form per family reduces to PRIMITIVES eq. (8) under the deterministic limit (σ → 0 for GBM; θ → ∞ for OU; λ_jump → 0 for jump-diffusion). | sympy.simplify residual ≤ 1e-6. |
| **Z1.4** | MC KS p-value ≥ 0.01 for empirical ε̂-distribution vs analytic ε-distribution per family. | `scipy.stats.ks_2samp` test on N ≥ 1000 paths. |
| **Z1.5** | Anti-fishing routing: observed family-level inversion-test FAILURES route to CORRECTIONS-α + scoped Wave-1 re-review per master-spec §6.4. NEVER silent parameter re-tuning. | HALT-routing table in §6 of this spec; verification at Wave-2 review. |
| **Z1.6** | Strip preservation: cohort_5_strip's `IronCondor_strip.json` audit_block (`94150326…`) is UNCHANGED before and after this spec's implementation. | `git log -p simulations/saas_builder/data/IronCondor_strip.json` shows no commits between the strip's pin commit and the stochastic-fx package merge. |

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
| Family-level symbolic deterministic-limit residual > 1e-6 | HALT — disposition memo; CORRECTIONS-α v0.x → v0.(x+1) on this spec; scoped Wave-1 re-review per master-spec §6.4 semantic. NEVER silent re-tuning of SDE parameters. |
| Family-level MC KS p-value < 0.01 | HALT — same routing as above. The KS gate failure is a structural rejection of the family's distributional inversion; document the failure and route to user-enumerated pivot (drop the family from the spec OR refine the parameters with explicit anti-fishing justification). |
| Implementation breaks any cohort_5_strip test (Pin Z1.6) | HALT — implementation is anti-fishing-coupled to cohort_5_strip; route to cohort_5_strip review. |
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

- SDE parameter values for each family are PRE-PINNED in this spec
  v0.1 §4 BEFORE the inversion verifier runs. Canonical values
  documented in the per-family parameter docstrings; ex-post tuning
  requires CORRECTIONS-α + fresh Wave-1 review.
- Family-level inversion-test FAILURES are SCIENTIFIC RESULTS, not
  tuning triggers (Pin Z1.5). A failed family is documented honestly,
  not silently dropped or retuned to PASS.
- The "expected" sympy form per family is derived from the SDE's
  stationary or quasi-stationary variance closed form — NOT chosen to
  match an observed Monte-Carlo distribution.
- This spec does NOT pre-pin a target value for the KS p-value beyond
  the conventional `≥ 0.01` threshold. Sub-conventional p-values are
  honest rejections, not opportunities to re-run with more paths until
  passing.
- Strip preservation (Pin Z1.6) prevents the most subtle anti-fishing
  pattern: re-emitting cohort_5_strip under stochastic-path expectations
  would let stochastic-FX results retroactively justify the existing
  strip. Pin Z1.6 keeps the strip-emit pinned at its deterministic-
  fixture commit (`3442852`).

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

## §11 CORRECTIONS-α (reserved patch log)

v0.1 has no corrections. Wave-1 RC+MQ may land v0.2 here.

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
