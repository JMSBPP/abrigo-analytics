# STAGE_2_RESULTS — SaaS-Builder Stage-2 math anchor

> Math-results-and-verification anchor for the SaaS-Builder (Y, M, X) iteration.
> Frozen at HEAD `9fd92e5` ("deliverable(saas-cohort): Stage-2 modeling memo +
> Phase-4 schema-bump audit"). This document is the single import point for
> Stage-3 work and does NOT auto-update.

**Version:** v1.1 (post-RC+MQ FLAG fold; nomenclature/clarity tightenings only,
no substantive math or claim changes — see §"v1.0 → v1.1 patch notes" at end).

---

## §0 Preface

This file is a math-claim-indexed anchor, not a narrative. The narrative is in
`docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md`; the spec lock is
in `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` v1.2.1; the
abstract math primitives that Stage-2 specialized are in `notes/PRIMITIVES.md`;
the cohort-population instantiation is in `notes/SaaS_Builders_AI_NativeBuilders.md`.

**Predecessor chain.** `notes/PRIMITIVES.md` → `notes/SaaS_Builders_AI_NativeBuilders.md`
→ **STAGE_2_RESULTS.md** (this file). Stage-3 will produce
`notes/STAGE_3_RESULTS.md` following the same pattern.

**Status — Stage-2 frozen anchor.** Substantive Stage-2 codepaths
(`simulations/saas_builder/`, `simulations/modules/`, `simulations/types/`,
`simulations/utils/`, `simulations/tests/`,
`docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md`) have not changed
since `9fd92e5`. Cosmetic post-freeze diffs (memory hygiene, `simulations/README.md`
documentation updates) are permitted per §5 verification protocol; substantive
Stage-2 codepaths are unchanged at `9fd92e5`. The ancestor `80f4ed4` is the
CORRECTIONS-α v0.4 marginalization-closure commit. All file:line and pytest-name citations resolve
against `9fd92e5`. The two `audit_block` sha256 anchors cited verbatim in §5
were re-hashed live: `Z_cap_pinned.json::audit_block` =
`1fb1f7a42131268f3448da8d61b685ce27fe1facf356122e557ac10d329b5d31`;
`gate_verdict.json::audit_block` =
`4da660b55e7ad33071711dc313f12a4d06283717e7a332a7f7ddcd8a19672173`.

This doc captures Stage-2 frozen state. It is read-only with respect to upstream
specs, plans, code, and audits. Future commits beyond `9fd92e5` are out of scope
for this file; they belong in `STAGE_3_RESULTS.md`.

---

## §1 Empirical verdict

The SaaS-Builder Stage-2 instantiation **PASSES** its pre-registered sign
certification gate under both the primary regime and the bank-spread robustness
overlay (verdict memo §1, §4.2): Δ^(a_s) is strictly negative across all 24
brackets of spec §5.2 (3 cohort tiers × 2 churn-mix arms α × 2 cache regimes ×
2 softplus-tightness arms κ); 24/24 PASS primary; 24/24 PASS bank-spread; 0
sign violations. The cohort monthly cap statistic is pinned at
Z_cap = 4{,}687.94 COP/month with primary 95% CI [168.17, 14{,}606.14] COP
(strictly positive lower bound), and 5/5 sign-cert test points PASS with the
perpetual-identity residual at 6.31×10⁻⁹ (sympy-exact zero). The verdict is
synthetic-Bayesian only (ideal-scenario clause invoked per `CLAUDE.md` ll. 31–46);
magnitudes certify sign, not commercial scale.

---

## §2 Math claims index

Each entry below cites (a) **claim verbatim**, (b) **post-cycle form** (what the
Stage-2 forward-fix cycle did to the claim), (c) **code pointer** (file:line +
pytest test name), (d) **artifact pointer** (sha256 prefix … 4-char tail).
Anchor tails are pinned: `…5d31` for `Z_cap_pinned.json::audit_block`; `…2173`
for `gate_verdict.json::audit_block`.

### §2.A Math primitives extended/specialized in Stage-2

#### §2.A.1 — Eq. (6) FX path closed form

- **Claim verbatim.** `(X/Y)_t(ε, ω) = (1 + ε·(cos²(ω t) − 1/2))·(X̄/Ȳ)`,
  with `0 < ε < 1` (`notes/PRIMITIVES.md:186-191`, eq. (6)).
- **Post-cycle form.** Specialized to the cohort's M5 single-mean / three-time
  bracket; instantiated as the FXPath Callable used by C2/C4 evaluators.
  Unchanged math.
- **Code.** `simulations/modules/fx_path.py:66-72` (FXPath.__call__);
  test: `simulations/tests/test_modules.py` covers FXPath path-reconstruction
  semantics (185, 194 referenced in cohort-2 plan); `simulations/tests/test_saas_cohort4.py`
  `TestM2Monotonicity::test_pi_strict_increasing_in_xy_bar`.
- **Artifact.** Path values consumed by `gate_verdict.json::audit_block`
  (`4da660b5…2173`).

#### §2.A.2 — Eq. (7) Realized variance

- **Claim verbatim.** `σ_T ≡ (1/T)·Σ_{t=0}^{T} ((X/Y)_t − (X̄/Ȳ))²`
  (`notes/PRIMITIVES.md:204-208`, eq. (7)).
- **Post-cycle form.** Encoded verbatim with the (T+1)/T arithmetic discipline
  pinned (sum over T+1 points, divisor T); CR I-1 cross-check enforced.
- **Code.** `simulations/modules/fx_path.py:85-91` (`RealizedVarianceCalc`
  class docstring + body); test: `simulations/tests/test_modules.py` (module
  fixtures).
- **Artifact.** Used by C2 sign-cert pipeline emitting `gate_verdict.json`
  (`4da660b5…2173`).

#### §2.A.3 — Eq. (8) Variance-proxy ε ↔ σ_T inversion

- **Claim verbatim.** `ε(σ_T) = sqrt(8·σ_T / (X̄/Ȳ)²)` (`notes/PRIMITIVES.md:212-215`,
  eq. (8)).
- **Post-cycle form.** Re-derived in C4 v0.3 as the σ₀-anchor:
  `σ₀ = (X̄/Ȳ)²·ε²/8` (FLAG-4 fix, plan v0.3 §5; replaces the v0.2 unanchored
  default 1e4). With X̄/Ȳ=4000, ε=0.1 ⇒ σ₀ = 20{,}000.
- **Code.** `simulations/saas_builder/cohort_4/pi_derivation.py:70-100`
  (`_step_5a_variance_proxy_symbolic`); test:
  `simulations/tests/test_saas_cohort4.py` `TestM1SymbolicPiT::test_anchors_present`.
- **Artifact.** σ₀ propagated through `Z_cap_pinned.json` per-TP fields
  (`1fb1f7a4…5d31`).

#### §2.A.4 — Eq. (10) Δ^(a_s) closed form

- **Claim verbatim.** PRIMITIVES.md eq. (10) verbatim — the boxed primitive
  asserts: `Δ^(a_s) = (4 / ((X̄/Ȳ)·ε(σ_T))) · Σ_{t=1}^{T} q_t · f_t /
  (X/Y)_t² < 0` (`notes/PRIMITIVES.md:228-233`, eq. (10)). The strict-negativity
  inequality `< 0` is reproduced from the upstream source, not asserted by this
  document.
- **Post-cycle form.** Specialized to the saas cohort with
  `q_t = p̄_sub + p_t · softplus_β(τ_t − κ)` and consumed by the C2 24-cell
  bracket sign-certification gate (spec §5.2 parameter family); strict-negative
  verified across all 24 cells (primary) and all 24 cells under bank-spread
  overlay.
- **Code.** Symbolic deriver:
  `simulations/saas_builder/cohort_2/derivatives.py:118-129`; numerical evaluator
  at the gate level: `simulations/saas_builder/cohort_2/sign_cert.py:240-298`.
  Tests: `test_saas_cohort2.py::TestDeltaClosedForm::test_delta_symbolic_lambdify_matches_numerical`,
  `::test_delta_constant_q_positive_f_positive_phase_negative`,
  `TestSignCertificationGate::test_gate_pass_when_all_brackets_strictly_negative`.
- **Artifact.** `gate_verdict.json::audit_block` = `4da660b5…2173`
  (24/24 PASS; n_sign_violations = 0).

#### §2.A.5 — Eq. (11) Γ closed form

- **Claim verbatim.** `Δ^{a_l + Π} = Δ^(a_l) + ∂Π/∂σ_T = 0; Δ^{a_s − Π} =
  Δ^(a_s) − ∂Π/∂σ_T = 0` (`notes/PRIMITIVES.md:243-247`, eq. (11)).
- **Post-cycle form.** Used as the sign-neutralization anchor for the CPO
  payoff in C2's Γ finite-difference reporting; not directly emitted but
  exercised symbolically for self-consistency.
- **Code.** `simulations/saas_builder/cohort_2/derivatives.py` (Γ block within
  the symbolic deriver module); test:
  `test_saas_cohort2.py::TestGammaFiniteDifference::test_gamma_finite_and_reported`.
- **Artifact.** Reported as evidence in `gate_verdict.json` (`4da660b5…2173`).

#### §2.A.6 — §6 variance-proxy section

- **Claim verbatim.** §6 of `notes/PRIMITIVES.md:201-217` (the
  `ε ↔ σ_T` inversion + `σ_T = (X̄/Ȳ)²·ε²/8` as the algebraic inversion of
  PRIMITIVES.md eq. (8)).
- **Post-cycle form.** Anchor invoked by C4 v0.3 σ₀ derivation; replaces the
  v0.2 unanchored default `1.0e4` (BLOCK-4 fix).
- **Code.** `simulations/saas_builder/cohort_4/pi_derivation.py:294-302`
  (numerical σ_T grid via the §6 form). Test:
  `test_saas_cohort4.py::TestM2IdentityTolerance::test_residual_under_numerical_tolerance`.
- **Artifact.** Propagated through `Z_cap_pinned.json` per-TP `sigma_0` fields
  (`1fb1f7a4…5d31`).

#### §2.A.7 — §10 Carr-Madan replication anchor

- **Claim verbatim.** Π(σ_T) ≈ K̂·σ_T with K̂ = K⋆/(2√σ₀); strip identity
  σ_T ~ ∫P/K² + ∫C/K² (`notes/PRIMITIVES.md:295-341`, eqs. (16)–(19)).
- **Post-cycle form.** Used as the linearization step in the C4 π(t)
  derivation; the K̂ constant is built symbolically and feeds the perpetual
  identity π·dt ↔ dΠ/dt.
- **Code.** `simulations/saas_builder/cohort_4/pi_derivation.py:113-122`
  (`_step_4_carr_madan_K_hat`). Test:
  `test_saas_cohort4.py::TestM1SymbolicPiT::test_anchors_present`.
- **Artifact.** Symbolic only; no direct sha — exercised in the perpetual
  identity sympy-exact zero (see §2.C.7).

#### §2.A.8 — §11 discrete strip / Carr-Madan reference

- **Claim verbatim.** `Π_T ≈ Σ_j w_j · Condor_j(S_T)`, w_j ∝ 1/K_j², N=3
  condors / 12 legs (`notes/PRIMITIVES.md:343-361`, eq. (20)).
- **Post-cycle form.** Referenced as the Stage-3 deployment-side M-design;
  Stage-2 invokes §11 only as the natural discrete-strip endpoint of the §10
  linearization. Not implemented in code at Stage-2.
- **Code.** No Stage-2 codepath; documented in
  `simulations/saas_builder/cohort_4/pi_derivation.py:125-141` docstring as the
  source-chain reference. Test: N/A (Stage-3 deferred).
- **Artifact.** N/A.

### §2.B Math pins M1–M5

#### §2.B.1 — M1: TruncPareto α-floor (≥1.5)

- **Claim verbatim.** Per spec §8(6), the TruncPareto α prior is bounded
  below at 1.5 (sampler-Callable enforcement); Truncated-Normal centered with
  μ=2.0, σ=0.25.
- **Post-cycle form.** Floor enforced at the Value-tier `__post_init__` of
  `TruncParetoAlphaPrior` and at the sampler-Callable
  `TruncParetoSampler` (raises on draws < 1.5).
- **Code.** `simulations/saas_builder/priors.py:163-227` (`TruncParetoAlphaPrior`
  class + validation); `simulations/types/distributions.py:66-100`
  (`TruncParetoParams`). Tests:
  `test_saas_builder.py::TestPriorsM1Floor::test_default_alpha_lower_is_1_5`,
  `::test_alpha_lower_below_1_5_raises`,
  `TestAlphaPriorBracketInvariance::test_alpha_lower_above_floor`.
- **Artifact.** Enforced upstream of all C1/C2/C4 emitted artifacts (no
  dedicated sha); cohort prior column captured in `cohort_prior.parquet`.

#### §2.B.2 — M2: Softplus β-tightness (L¹ < 10⁻³·κ)

- **Claim verbatim.** Per spec §5.1 (T2) M2: `softplus_β(x) = β⁻¹ log(1 +
  exp(β x))` deviates from ReLU on `[0, 2κ]` by L¹ < 10⁻³·κ.
- **Post-cycle form.** Encoded as `tightness_l1_deviation` invariant in
  `SoftplusRegularizer.__post_init__`; the C2 `SoftplusBetaFitter` searches
  ascending β until the bound is satisfied.
- **Code.** `simulations/saas_builder/cohort_2/pricing.py:114-145`
  (fitter); `pricing.py:158-209` (composer + `__post_init__` re-run of M2).
  Tests: `test_saas_cohort2.py::TestM2SoftplusFit::test_fitter_returns_smallest_beta_satisfying_pin_m2`,
  `::test_fitter_raises_when_grid_too_loose`,
  `TestHypothesisProperties::test_softplus_fit_monotone_convergence`.
- **Artifact.** β fit consumed by all 24 brackets; verdict captured in
  `gate_verdict.json::audit_block` = `4da660b5…2173`.

#### §2.B.3 — M3: Blended p_t formula (Sonnet $7.1495 / MTok)

- **Claim verbatim.** `p_t = w_in·p_in·(1 − h_cache + h_cache·0.10) + w_out·p_out
  = 0.539·3·0.145 + 0.461·15 = 0.234 + 6.915 = 7.1495` (spec §5.1; default
  Sonnet weights).
- **Post-cycle form.** Asserted at factory call time via
  `math.isclose(price, 7.1495, abs_tol=0.01)`; price is recomputed from the
  shipped `BlendedPriceFn` rather than hard-coded.
- **Code.** `simulations/saas_builder/model.py:91-93` (constant);
  `model.py:116-144` (`_build_sonnet_blended_price`); `model.py:281-299`
  (T1ModelFactory call site). Tests:
  `test_saas_builder.py::TestM3SonnetClosedForm::test_closed_form_evaluates_within_tolerance`,
  `::test_assertion_fires_on_drift`,
  `::test_blended_price_call_is_deterministic`.
- **Artifact.** Locked at the inference graph; consumed by all C1
  posteriors emitted to `cohort_prior.parquet` and `synthetic_tau_t/`.

#### §2.B.4 — M4: Parquet schemas per spec §10

- **Claim verbatim.** Per spec §10 output-artifact contract: `cohort_prior.parquet`
  carries (`param`, `percentile`, `value`, `source`, `fetched_at_utc`);
  `synthetic_tau_t/` is partitioned by `tier_id` and carries (`month`,
  `simulation_id`, `tau_t`, `tier_id`, `chain`, `draw`, `schema_version`).
- **Post-cycle form.** Schema v1.0 → v1.1 schema-bump audited under CLOSE
  Phase-4 (BLOCK-3 fix: a breaking-change semver bump; previously mislabeled
  "additive"). **Scope of the v1.1 bump:** applies only to `Z_cap_pinned.json`
  (Phase-4 additive `sign_verdicts` field per CLOSE plan); `synthetic_tau_t/`
  and `cohort_prior.parquet` legitimately remain at schema v1.0.
- **Code.** Round-trip enforcement in `simulations/saas_builder/emit.py`
  (write path) and `simulations/utils/parquet_io.py` (read path). Tests:
  `test_saas_builder.py::TestEmitSchemaRoundTrip::test_synthetic_tau_round_trip`,
  `::test_cohort_prior_round_trip`,
  `TestHypothesisProperties::test_property_4_synthetic_tau_round_trip_includes_schema_version`.
- **Artifact.** `synthetic_tau_t/` (3 tier partitions, 712k draws);
  `cohort_prior.parquet`. Stage-2 audit block over the synthetic_tau payload
  ends in `…162a` (`_AUDIT.json::audit_block`); Z_cap pin block `1fb1f7a4…5d31`
  carries `schema_version: "v1.1"` field.

#### §2.B.5 — M5: FX path `[4200, 3800, 4200]` at t ∈ {0, π/2, π}

- **Claim verbatim.** Per spec §3 + §5.2 + §8(1): the FX path is parameterized
  by ONE TRM-pinned `(X̄/Ȳ)` (sha-pinned per spec §3 audit_block); the values
  `(4200, 3800, 4200)` are path values produced by the M5 sinusoidal kernel
  around the single mean.
- **Post-cycle form.** Encoded as constants `FX_HIGH_BRACKET = 4200.0`,
  `FX_LOW_BRACKET = 3800.0`; validated as path-reconstruction targets in
  C2 BracketGrid construction.
- **Code.** `simulations/saas_builder/cohort_4/types.py:72-73` (constants);
  `cohort_4/types.py:457-515` (TP4/TP5 documentation); `simulations/modules/fx_path.py:66-72`
  (path generator). Tests:
  `test_saas_cohort2.py::TestBracketM5::test_canonical_anchor_recovery_passes_grid`,
  `::test_grid_rejects_path_with_anchor_mismatch`,
  `test_saas_cohort4.py::TestM2Monotonicity::test_pi_strict_increasing_in_xy_bar`.
- **Artifact.** Path values stamped into `Z_cap_pinned.json::audit_block`
  (`1fb1f7a4…5d31`) per-TP rows TP4/TP5.

### §2.C Forward-fix claims

#### §2.C.1 — C1 marginalization: `tier_idx + n_per_day + n_month` sum-out

- **Claim verbatim.** Plan v0.4 §"CORRECTIONS-α v0.3 → v0.4": the per-builder
  `tier_idx` (1000-dim Categorical), per-active-day `n_per_day` (22-dim
  integer NegBin vector), and per-month `n_month` discrete latents are
  ANALYTICALLY MARGINALIZED out of the inference graph; the marginalized
  log-likelihood at fixed `(π, μ, φ, α, x_m)` equals the explicit-Categorical
  log-likelihood (LSE over tiers) within tolerance — an identity, not an
  approximation.
- **Post-cycle form.** Pure-NUTS chain. ESS rose from 38 (v0.3 CompoundStep
  Gibbs) → 7{,}537 (v0.4 prototype) → **338{,}540 bulk / 213{,}752 tail**
  (Phase-2 N_draws bump to 4 chains × 178k = 712k); r̂_max = 1.0000265;
  divergences = 0.0; ci_width_ratio_max = 1.0039.
- **Code.** `simulations/saas_builder/model.py:32-56` (model-surface
  marginalization narrative); `model.py:191-203` (PP-time sampling of
  `tier_idx ~ Categorical(π)` numpy-side); `simulations/saas_builder/diagnostics.py`
  (gate constants). Tests:
  `test_saas_builder.py::TestHypothesisProperties::test_property_7_marginalization_numerical_equivalence`,
  `::test_property_8_emit_pp_draws_tier_idx_from_posterior_pi`,
  `TestDiagnosticGate::test_clean_idata_passes`.
- **Artifact.** `_AUDIT.json::audit_block` =
  `ded06012ea8e01bea660e4ae6bdc2be1470b6de84c647735cb8161927b06162a`
  (full sha; `…162a` tail).

#### §2.C.2 — C2 bracket re-orientation: 24-cell parameter family per spec §5.2

- **Claim verbatim.** Plan v0.3 §"CORRECTIONS-α": the v0.2 5-cell `(ε, ω)`
  bracket grid was anti-fishing-banned for misalignment with spec §5.2; v0.3
  re-orients to the 24-cell parameter family (3 cohort tiers × 2 churn-mix α
  × 2 cache regimes × 2 softplus-tightness arms κ).
- **Post-cycle form.** 24/24 PASS primary; 24/24 PASS bank-spread overlay;
  `Δ_med ∈ [−2.28×10⁻⁸, −2.28×10⁻⁹]`; 0 sign violations.
- **Code.** `simulations/saas_builder/cohort_2/sign_cert.py:199-298`
  (SignCertificationGate over BracketGrid). Tests:
  `test_saas_cohort2.py::TestSpec5_2BracketGrid::test_grid_has_24_brackets`,
  `::test_grid_enumerates_all_three_tiers`,
  `::test_grid_enumerates_two_p_t_cache_values`,
  `::test_grid_runs_through_gate`.
- **Artifact.** `gate_verdict.json::audit_block` =
  `4da660b55e7ad33071711dc313f12a4d06283717e7a332a7f7ddcd8a19672173`
  (`4da660b5…2173`).

#### §2.C.3 — C2 Δ_analytic = −1.02×10⁻⁸ reconciliation

- **Claim verbatim.** Verdict memo §4.2: with `β·κ ≈ 2.33×10⁴`, the softplus
  argument saturates and `q_t` collapses to floor `q_0 = $20`; combined with
  cos²-near-cancellation at the calibrated θ, the predicted `|Δ|` sits
  ~13 decades above the float64 noise floor.
- **Post-cycle form.** Sign verdict robust; magnitude is the analytic
  prediction, not numerical underflow; documented in `PRIMARY_RESULTS.md`.
- **Code.** `simulations/saas_builder/cohort_2/derivatives.py:158-178`
  (composed T2 cost); `cohort_2/derivatives.py:373-376` (per-bracket
  `softplus_k`). Tests:
  `test_saas_cohort2.py::TestDeltaClosedForm::test_delta_numerical_finite_on_canonical_inputs`,
  `::test_delta_symbolic_lambdify_matches_numerical`.
- **Artifact.** `gate_verdict.json::audit_block` = `4da660b5…2173` carries
  the per-bracket `delta_value` evidence.

#### §2.C.4 — C3 Det+churn S_t with λ ∼ Beta(4.5, 95.5)

- **Claim verbatim.** Spec v1.2.1 §6.1: the Det+churn sensitivity arm pins
  `S_t = (1 − λ)^t` with `λ ∼ Beta(4.5, 95.5)` (concentration K=100,
  prior-mean 4.5%); this is the CLOSED candidate set (anti-fishing per
  spec §8(5)).
- **Post-cycle form.** v1.1.1 → v1.2.1 prior re-pin from Beta(2.0, 38.0) →
  Beta(4.5, 95.5) routed under NON-NO-OP regime; CLOSE Phase-0 Task 0.2b
  re-fit verified `rank_flip_detected: false`.
- **Code.** `simulations/saas_builder/cohort_3/priors.py` (Beta hyperparameters);
  `cohort_3/models.py` (det_churn PyMC builder). Tests:
  `test_saas_cohort3.py::test_r1_det_churn_params_validation`,
  `::test_r1_priors_validation`,
  `::test_det_churn_builder_returns_pymc_model`,
  `::test_det_churn_builder_validates_sigma_obs_scale`.
- **Artifact.** `revenue_form_verdict.json::audit_block` =
  `588a491b647c5817b42ce49efdd914b2729e21f3e95ab749efec064e36b68adb`
  (`588a491b…8adb`).

#### §2.C.5 — C3 ELPD ranking + INDISTINGUISHABLE verdict + HALT-on-flip

- **Claim verbatim.** Per spec §9 / Pin R3: PASS at `Δelpd > 4·SE`,
  INDISTINGUISHABLE at `< 2·SE`. Observed Δelpd/SE = 1.67 < 2.0 ⇒ verdict
  INDISTINGUISHABLE; ar1_log numerically best (ELPD 28.481, weight 0.974)
  but spec v1.2.1 §6.1 pins det_churn as canonical Υ_t for tractability.
  HALT-on-flip preserved.
- **Post-cycle form.** Verdict-router emits INDISTINGUISHABLE explicitly;
  no silent winner pick; `_first_trajectory` discards multi-sim panels (KNOWN
  LIMITATION documented for Stage-3 hierarchical re-implementation).
- **Code.** `simulations/saas_builder/cohort_3/loo.py` (VerdictRouter); tests:
  `test_saas_cohort3.py::test_r3_classify_indistinguishable_band`,
  `::test_r3_verdict_marginal_at_2se_boundary`,
  `::test_r3_verdict_marginal_at_4se_boundary`,
  `::test_r3_verdict_indistinguishable_no_winning_form_marginal_has_one`,
  `::test_first_trajectory_warns_on_multi_sim_panel`.
- **Artifact.** `revenue_form_verdict.json::audit_block` = `588a491b…8adb`
  (`verdict: INDISTINGUISHABLE`; weights {ar1_log: 0.974, det_churn: 0.026,
  martingale: 0.000}).

#### §2.C.6 — C4 π(t) post-fix closed form

- **Claim verbatim.** Plan v0.3 honest derivation:
  `π(t) = K⋆·ε²·(X̄/Ȳ)²·(4ωt·cos(4ωt) − sin(4ωt)) / (64·ω·√σ₀·t²)`
  with free symbols `{K_star, sigma_0, epsilon, omega, t, xy_bar}`;
  `κ ∉ free_symbols(π)`.
- **Post-cycle form.** Built solely from PRIMITIVES.md §6 (FX path) → §8.1
  (Π = K⋆√σ_T) → §10 (Carr-Madan linearization) → §15 (perpetual identity
  π·dt ↔ dΠ/dt). The v0.2 spurious `1/κ` factor is REMOVED; `(X̄/Ȳ)²`
  prefactor RESTORED (FLAG-1 fix). σ₀ anchored to (X̄/Ȳ)²·ε²/8 (BLOCK-4 fix).
- **Code.** `simulations/saas_builder/cohort_4/pi_derivation.py:124-201`
  (`derive_pi_t_symbolic`); `pi_derivation.py:43-58` (closed-form docstring).
  Tests:
  `test_saas_cohort4.py::TestM1SymbolicPiT::test_kappa_not_in_free_symbols`,
  `::test_free_symbols_are_canonical_subset`,
  `::test_lambdified_callable`,
  `::test_lambdified_broadcasts_K_star`.
- **Artifact.** π(t) evaluated per-TP into `Z_cap_pinned.json::audit_block` =
  `1fb1f7a42131268f3448da8d61b685ce27fe1facf356122e557ac10d329b5d31`
  (`1fb1f7a4…5d31`).

#### §2.C.7 — C4 perpetual identity sympy-exact zero + numerical residual 6.31×10⁻⁹

- **Claim verbatim.** `simplify(π − dΠ_lin/dt) ≡ 0` (sympy.S.Zero); numerical
  residual 6.31×10⁻⁹ on a 5000-point grid `t ∈ [0.5, 12]` (Δt ≈ 2.3×10⁻³).
- **Post-cycle form.** v0.2 BLOCK-2 (circular identity / `Pi_grid /= κ`
  rescaling tautology) REMOVED. Identity test is two-tier:
  symbolic (exact zero) + numerical (max relative residual ≤ tolerance).
- **Code.** `simulations/saas_builder/cohort_4/pi_derivation.py:324-356`
  (`assert_perpetual_identity_symbolic`); `pi_derivation.py:209-321`
  (`PerpetualIdentityResidual` numerical evaluator). Tests:
  `test_saas_cohort4.py::TestM1SymbolicPiT::test_perpetual_identity_symbolic`,
  `TestM2IdentityTolerance::test_residual_under_numerical_tolerance`,
  `::test_violation_raises_DiagnosticGateError`.
- **Artifact.** Residual stamped into `Z_cap_pinned.json` per-TP (6.31×10⁻⁹
  for all 5 TPs); `audit_block` = `1fb1f7a4…5d31`.

#### §2.C.8 — C4 5-test-point sign cert PASS magnitudes

- **Claim verbatim.** Plan v0.3 + verdict memo §4.4: TP1 z = 4{,}687.94 COP/mo,
  CI [168.17, 14{,}606.14]; TP2/TP3 share TP1 CI (κ ∉ free_symbols(π) under
  the honest derivation); TP4 (FX=4200) z = 4{,}922.32; TP5 (FX=3800)
  z = 4{,}453.57; identity passes for all 5; identity residual 6.31×10⁻⁹
  uniform; sign PASS for all 5.
- **Post-cycle form.** v0.2 κ-monotonicity expectation `∂|π|/∂κ < 0` is
  STRUCTURALLY UNSATISFIABLE under the honest π (κ ∉ free_symbols);
  re-pinned to (X̄/Ȳ)-monotonicity per PRIMITIVES.md §6:
  `|π|_TP4 > |π|_TP1 > |π|_TP5`. TP2/TP3 retained in the 5-tuple
  (anti-fishing immutability) but κ-chain deprecated.
- **Code.** `simulations/saas_builder/cohort_4/sign_cert.py:99` (monotonicity
  docstring); `cohort_4/z_cap.py:138-220` (`PerDrawZEvaluator`); 5-test-point
  grid: `cohort_4/types.py:457-515`. Tests:
  `test_saas_cohort4.py::TestM2FiveTestPointSignCert::test_grid_is_5_tuple`,
  `::test_sign_expectation_is_immutable_positive`,
  `::test_per_draw_evaluator_produces_z_gt_0`,
  `::test_runner_pass_path`,
  `TestM2Monotonicity::test_strict_chain_holds`.
- **Artifact.** `Z_cap_pinned.json::audit_block` = `1fb1f7a4…5d31`
  (5/5 sign verdicts, schema v1.1).

### §2.D Empirical artifacts

| # | Artifact | Path | sha256 (tail) | Schema |
|---|---|---|---|---|
| §2.D.1 | `synthetic_tau_t/` (3 months × 712k draws × 3 tiers) | `simulations/saas_builder/data/synthetic_tau_t/{tier_id=pro,max_5x,max_20x}/` | covered by `_AUDIT.json::audit_block` `…162a` | v1.0 partitioned by `tier_id` |
| §2.D.2 | `cohort_prior.parquet` | `simulations/saas_builder/data/cohort_prior.parquet` | row-schema validated by `simulations/utils/parquet_io.py` | M4: (`param`, `percentile`, `value`, `source`, `fetched_at_utc`) |
| §2.D.3 | `gate_verdict.json` (24/24 PASS primary) | `simulations/saas_builder/data/gate_verdict.json` | `4da660b55e7ad33071711dc313f12a4d06283717e7a332a7f7ddcd8a19672173` (`…2173`) | spec §10 verdict alphabet |
| §2.D.4 | `PRIMARY_RESULTS.md` | `simulations/saas_builder/data/PRIMARY_RESULTS.md` | (md narrative; sha via tree) | n/a |
| §2.D.5 | `ROBUSTNESS_RESULTS.md` (bank-spread overlay) | `simulations/saas_builder/data/ROBUSTNESS_RESULTS.md` | (md narrative; sha via tree) | n/a |
| §2.D.6 | `revenue_form_verdict.json` (INDISTINGUISHABLE) | `simulations/saas_builder/data/revenue_form_verdict.json` | `588a491b647c5817b42ce49efdd914b2729e21f3e95ab749efec064e36b68adb` (`…8adb`) | router `VerdictRouting` |
| §2.D.7 | `Z_cap_pinned.json` (5/5 sign-cert PASS, schema v1.1) | `simulations/saas_builder/data/Z_cap_pinned.json` | `1fb1f7a42131268f3448da8d61b685ce27fe1facf356122e557ac10d329b5d31` (`…5d31`) | v1.1 (Phase-4 schema bump) |
| §2.D.8 | `Z_cap_pinned.SIGN_VERDICTS.md` (sidecar) | `simulations/saas_builder/data/Z_cap_pinned.SIGN_VERDICTS.md` | (md narrative; deprecation pending — Stage-3 collapses sidecar into JSON) | n/a |

---

## §3 Cohort cross-cut

Pure cross-reference; no new claims.

### §3.1 C1 — T1 cost posterior (NegBin × TruncPareto)

Consumed/verified §2 entries: §2.A.1 (FX path — used at PP time),
§2.B.1 (M1 α-floor), §2.B.3 (M3 blended price), §2.B.4 (M4 schemas),
§2.C.1 (marginalization sum-out). Emits §2.D.1 (`synthetic_tau_t/`),
§2.D.2 (`cohort_prior.parquet`).

### §3.2 C2 — T2 pricing fit and Δ-sign certification

Consumed: §2.A.1, §2.A.2, §2.A.4 (Δ closed form), §2.A.5 (Γ),
§2.B.2 (M2 softplus tightness), §2.B.5 (M5 FX path).
Forward-fix verifications: §2.C.2 (24-cell), §2.C.3 (Δ_analytic
reconciliation). Emits §2.D.3 (`gate_verdict.json`), §2.D.4
(`PRIMARY_RESULTS.md`), §2.D.5 (`ROBUSTNESS_RESULTS.md`).

### §3.3 C3 — Υ_t functional-form selection (PSIS-LOO-CV)

Consumed: §2.B.4 (M4 schemas). Forward-fix verifications: §2.C.4
(Beta(4.5, 95.5) Det+churn), §2.C.5 (INDISTINGUISHABLE + HALT-on-flip).
Emits §2.D.6 (`revenue_form_verdict.json`).

### §3.4 C4 — Z_cap pin and perpetual-identity sign cert

Consumed: §2.A.3 (ε ↔ σ_T), §2.A.6 (§6 variance proxy), §2.A.7 (§10
Carr-Madan), §2.B.5 (M5 FX path), §2.D.1 (`synthetic_tau_t/` for
`q_t_cop_draws`). Forward-fix verifications: §2.C.6 (π(t) post-fix),
§2.C.7 (perpetual identity), §2.C.8 (5-TP sign cert magnitudes). Emits
§2.D.7 (`Z_cap_pinned.json`), §2.D.8 (`Z_cap_pinned.SIGN_VERDICTS.md`).

---

## §4 Anti-fishing case studies

Each case study below mirrors `feedback_post_hoc_fit_anti_fishing_pattern.md`.

### §4.1 C1 marginalization fix (sum-out of `tier_idx + n_per_day + n_month`)

- **(a) Pathology.** v0.3 implementation used PyMC's default `CompoundStep`,
  which selected `CategoricalGibbsMetropolis` on the 1000-dim `tier_idx`
  latent and `Metropolis` on the 22-dim integer `n_per_day` vector. r̂_max
  ≈ 1.115; ESS_bulk = 38, ESS_tail = 58 (26× shortfall vs gate floor 1{,}000).
  Each NUTS step required a Gibbs sweep over all 1000 latents; chains failed
  to mix in `π` and consequently in `(μ, φ, α, x_m)`.
- **(b) Pre-fix claim.** Plan v0.3 §"BLOCK-1 (compound-sum likelihood)"
  asserted hybrid PyMC + post-hoc numpy reduction was sufficient.
- **(c) Detection heuristic.** **Tautological-identity audit** (formal) +
  **ESS-floor sampler diagnostic** (operational first-catch: ESS=38 vs gate
  floor 1{,}000 was the proximate trigger that surfaced the pathology) +
  **derivation-anchor citation check.** Independent RC + MQ + CR audit at commit `ec26317`
  inspected the compound-step graph against the spec §5.1 / §5.2 likelihood
  text and found the discrete latents do NOT enter the `tau_t` likelihood
  (the per-turn TruncPareto and per-day NegBin parameters are tier-independent;
  tier-conditional `(α_k, x_m,k, μ_k, φ_k)` is a future C2/C3 enhancement
  per spec §5.4). The `tier_idx` per-builder mixture marginalization is
  therefore exactly degenerate — an identity, not an approximation.
  Citations: `scratch/2026-05-08-saas-cohort-1-independent-audit/rc-verdict.md`,
  `mq-verdict.md`, `cr-verdict.md`.
- **(d) Fix.** CORRECTIONS-α v0.3 → v0.4 (plan
  `docs/plans/2026-05-08-saas-cohort-1-t1-cost-posterior.md` §"CORRECTIONS-α
  v0.3 → v0.4"). Removed `tier_idx`, `n_per_day`, `n_month` from the
  inference graph; recovered them numpy-side at PP time from the posterior π.
- **(e) Evidence.** ESS rose 38 → 7{,}537 (v0.4 prototype) → 338{,}540
  bulk / 213{,}752 tail (Phase-2 N_draws = 712k); r̂_max = 1.0000265;
  divergences = 0.0. Pytest:
  `test_saas_builder.py::TestHypothesisProperties::test_property_7_marginalization_numerical_equivalence`
  (LSE-over-tiers ≡ marginalized log-likelihood, on synthetic τ_t grid).
  `_AUDIT.json::audit_block` = `…162a`.
- **(f) Lesson for Stage-3.** When discrete latents do not enter the
  likelihood at the resolution of the current model surface, prefer
  analytic marginalization to compound-step sampling; the per-builder draws
  can be recovered at PP time without loss.

### §4.2 C2 bracket re-orientation (24-cell parameter family per spec §5.2)

- **(a) Pathology.** v0.2 sign-certification gate evaluated Δ^(a_s) on a
  5-cell `(ε, ω)` sweep mistaken for the spec §5.2 24-cell parameter family.
  This conflated the M5 FX-path sweep (the (ε, ω) grid the path generator
  internally consumes) with the spec §5.2 cohort-parameter brackets
  (3 tiers × 2 churn-mix α × 2 cache regimes × 2 κ-arms = 24).
- **(b) Pre-fix claim.** v0.2 reported sign cert PASS on 5 cells, claimed
  spec §5.2 coverage.
- **(c) Detection heuristic.** **Free-symbol audit.** Independent CR + RC
  audit cross-walked the spec §5.2 parameter table against the `BracketGrid`
  construction; the (`tier`, `α`, `cache_regime`, `κ_arm`) tuple was absent
  in v0.2. The (ε, ω) sweep is over the FX-path-internal symbols; spec §5.2
  brackets are over cohort symbols. Citations:
  `scratch/2026-05-08-saas-cohort-2-independent-audit/rc-verdict.md`,
  `mq-verdict.md`, `cr-verdict.md`.
- **(d) Fix.** CORRECTIONS-α v0.2 → v0.3 (plan
  `docs/plans/2026-05-08-saas-cohort-2-t2-pricing-sign.md` §M2 bracket pin).
  Re-derive `BracketGrid` against the full 24-cell parameter family;
  sign-certification gate runs over the 24-cell × (ε, ω) inner sweep.
- **(e) Evidence.** 24/24 PASS primary; 24/24 PASS bank-spread overlay;
  0 sign violations. Pytest:
  `test_saas_cohort2.py::TestSpec5_2BracketGrid::test_grid_has_24_brackets`,
  `::test_grid_enumerates_all_three_tiers`,
  `::test_grid_enumerates_two_p_t_cache_values`,
  `::test_grid_runs_through_gate`. `gate_verdict.json::audit_block` =
  `4da660b5…2173`.
- **(f) Lesson for Stage-3.** Distinguish between cohort-parameter brackets
  (the spec lock) and FX-path-internal sweeps (the path generator's domain);
  do not let the latter masquerade as the former in a sign-cert gate.

### §4.3 C4 1/κ correction in π(t) closed form

- **(a) Pathology.** v0.2 `pi_derivation.py:106-123, 165-170` injected a
  `1/κ` factor into π(t) for the express purpose of satisfying plan v0.2 §M2's
  expectation `∂|π|/∂κ < 0`. The factor has NO anchor in PRIMITIVES.md §6 / §8 / §10
  nor in saas-note §4.1. The hand-wave docstring justification ("softplus →
  linear overage → premium scales linearly with overage which decreases with
  κ") (i) conflated the cap on `q^USD` with the strike on Π, (ii)
  double-counted κ (already in `q_t^USD`), and (iii) gave a proportionality,
  not a 1/κ functional form.
- **(b) Pre-fix claim.** v0.2 plan asserted `∂|π|/∂κ < 0` as a structural
  monotonicity pin.
- **(c) Detection heuristic.** **Sign-target retro-fit audit** +
  **derivation-anchor citation check.** Independent MQ audit at commit
  `c1aa6a2` (`scratch/2026-05-08-saas-cohort-4-independent-audit/mq-verdict.md`)
  cross-walked every multiplicative factor in v0.2's π(t) against PRIMITIVES.md
  §6 / §8.1 / §10 / §15 anchors and the saas-note §4.1 pitch identity;
  the `1/κ` factor had no anchor. Verdict: REJECT, BLOCK-1 anti-fishing
  violation per `feedback_pathological_halt_anti_fishing_checkpoint`.
- **(d) Fix.** CORRECTIONS-α v0.2 → v0.3 (plan
  `docs/plans/2026-05-08-saas-cohort-4-z-cap-derivation.md` §"CORRECTIONS-α
  v0.2 → v0.3"). Remove `_step_1_pitch_kappa_coupling` and the
  `kappa_coupling` factor; rebuild π(t) solely from PRIMITIVES.md §6 (FX
  path) → §8.1 (Π = K⋆√σ_T) → §10 (Carr-Madan linearization) → §15
  (perpetual identity π·dt ↔ dΠ/dt). Restore the `(X̄/Ȳ)²` prefactor
  (FLAG-1) and anchor σ₀ via §6 (BLOCK-4). Re-pin monotonicity to
  `|π|_TP4 > |π|_TP1 > |π|_TP5` per (X̄/Ȳ).
- **(e) Evidence.** Honest closed form
  `π = K⋆·ε²·(X̄/Ȳ)²·(4ωt·cos(4ωt) − sin(4ωt)) / (64·ω·√σ₀·t²)` with
  `κ ∉ free_symbols(π)`. Symbolic identity sympy.S.Zero; numerical residual
  6.31×10⁻⁹ on 5/5 TPs. Pytest:
  `test_saas_cohort4.py::TestM1SymbolicPiT::test_kappa_not_in_free_symbols`,
  `::test_perpetual_identity_symbolic`,
  `TestM2Monotonicity::test_pi_strict_increasing_in_xy_bar`,
  `::test_strict_chain_holds`. `Z_cap_pinned.json::audit_block` = `1fb1f7a4…5d31`.
- **(f) Lesson for Stage-3.** Every multiplicative factor in a closed-form
  derivation must trace to a labeled anchor in the source-of-truth chain;
  injecting a free factor to satisfy a sign-target expectation is the
  canonical anti-fishing failure mode and must be detected at the audit
  step before merge.

---

## §5 Reproducibility certificate

Stage-2 is frozen at HEAD `9fd92e5`. The two `audit_block` sha256 anchors that
gate Stage-3 hand-off are cited verbatim (full sha; no truncation):

- **`Z_cap_pinned.json::audit_block`** =
  `1fb1f7a42131268f3448da8d61b685ce27fe1facf356122e557ac10d329b5d31`
- **`gate_verdict.json::audit_block`** =
  `4da660b55e7ad33071711dc313f12a4d06283717e7a332a7f7ddcd8a19672173`

Supplementary anchors (full sha):

- **`revenue_form_verdict.json::audit_block`** =
  `588a491b647c5817b42ce49efdd914b2729e21f3e95ab749efec064e36b68adb`
- **`_AUDIT.json::audit_block`** (cohort_prior + synthetic_tau_t) =
  `ded06012ea8e01bea660e4ae6bdc2be1470b6de84c647735cb8161927b06162a`

**Verification protocol.** At HEAD `9fd92e5`, from the repo root:

```
python3 -c "import json,sys; \
  print(json.load(open('simulations/saas_builder/data/Z_cap_pinned.json'))['audit_block'])"
python3 -c "import json,sys; \
  print(json.load(open('simulations/saas_builder/data/gate_verdict.json'))['audit_block'])"
```

Both commands MUST return the values cited above byte-for-byte. Any divergence
indicates either (i) a Stage-2 substantive code change (HALT — Stage-2 is
frozen) or (ii) a corrupted artifact (HALT and re-emit per the cohort plan
phase that produces it).

The freeze pin is `git merge-base --is-ancestor 9fd92e5 HEAD` AND
`git diff 9fd92e5 HEAD -- simulations/ docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md`
empty. Cosmetic post-freeze commits outside those paths (memory hygiene,
README updates) are permitted; substantive changes are not.

---

## §6 Stage-3 hand-off

Stage-3 (`STAGE_3_RESULTS.md`) inherits the §2 claims as Stage-2-frozen
preconditions. Stage-2 made the following assumptions; Stage-3 must test each.
**No magnitude promises.**

1. **Synthetic-Bayesian only.** Stage-2 conditions on a generative model
   without real-data conditioning of cohort costs, churn, or revenue
   trajectory. The posterior is fully prior-driven. Stage-3 MUST condition
   the C1 cost posterior (and downstream pipelines) on real data.
2. **Single FX trajectory (M5 pin).** Stage-2 emits a single sinusoidal
   trajectory parameterized by one TRM-pinned `(X̄/Ȳ)`, ε, ω. Stage-3 MUST
   extend to a trajectory family (stochastic-FX variant per PRIMITIVES.md
   §15: GBM, OU, jump-diffusion, or empirical-calibrated).
3. **Sonnet $7.1495 / MTok blended price (M3).** Stage-2 froze p_t at the
   spec §5.1 closed form with default Sonnet weights. Stage-3 MUST re-pin
   with current pricing (vendor pricing pages, default model mix,
   `h_cache` sensitivity bracket).
4. **24-cell sign cert is over a parameter family.** Stage-2's 24/24 PASS
   (primary + bank-spread) certifies sign over the spec §5.2 cohort-parameter
   bracket. Stage-3 MUST verify whether real-data parameters fall INSIDE the
   certified bracket; out-of-bracket parameters require a new sign-cert run,
   not extrapolation.
5. **Magnitudes are synthetic and certify only sign.** Z_cap = 4{,}453–4{,}922
   COP/mo across TP1–TP5 reflects the (X̄/Ȳ)² coupling at canonical fixtures.
   Stage-3 MUST NOT inherit these as magnitude predictions; commercial-scale
   magnitudes are an open question for real-data conditioning.
6. **C3 INDISTINGUISHABLE is a HALT-on-flip preservation.** Δelpd/SE = 1.67
   on a single 36-month synthetic trajectory triggers INDISTINGUISHABLE per
   spec §9 / Pin R3. Stage-3 MUST re-run the form selection on real data
   AND respect the HALT semantic if the routing flips; threshold tuning
   post-hoc is anti-fishing-banned.
7. **`_first_trajectory` discards multi-sim panels.** The C3 implementation
   selects the first synthetic trajectory; multi-cohort hierarchical pooling
   is deferred. Stage-3 MUST reimplement C3 hierarchically across multiple
   trajectories.
8. **Per-tier θ_k differentiation deferred.** The Stage-2 cohort-level π
   posterior collapses near the prior at per-tier resolution; Stage-3 scope
   per spec §5.4 must re-fit with per-tier anchoring (resolves C1 MQ-FLAG-1).
9. **K⋆ identification is a Stage-2 M-design parameter.** Setting `K⋆_d =
   (q_t_cop)_d` is admissible under the ideal-scenario clause; alternative
   identifications (K⋆ = κ converted via FX, K⋆ = constant per-tier
   notional) are admissible Stage-2 M-design variants. Stage-3 deployment
   must pin a single identification with explicit rationale.
10. **No on-chain test.** Stage-2 does not deploy live Panoptic LP capital;
    the §11 IronCondor 12-leg strip is a deferred deployment-stage M-design.
    Stage-3 deployment exit is the genuine market test.

---

## §7 References

**Primitives (math) and population**
- `notes/PRIMITIVES.md` — abstract math primitives. Anchors used: §4.2
  (cohort instantiation, ll. 127–179), §5 (FX path generator, eq. (6),
  ll. 181–199), §6 (variance proxy, eq. (7)–(8), ll. 201–217), §7 (Δ
  closed forms, eq. (9)–(10), ll. 219–236), §8 (CPO neutralizing payoff,
  eq. (11)–(13), ll. 238–278), §10 (Carr-Madan replication, eq. (16)–(19),
  ll. 295–341), §11 (discrete strip, eq. (20), ll. 343–361), §15 (open
  items / perpetual identity, ll. 406–428).
- `notes/SaaS_Builders_AI_NativeBuilders.md` — cohort-population SaaS
  instantiation; Υ_t and q_t semantic table; pitch identity ("your Claude
  Code bill in COP never exceeds Z COP/month").

**Spec and verdict memo**
- `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` v1.2.1 — spec
  lock. Sections used: §3 (FX path class), §4.1 (Z definition), §5.1
  (workflow-derived cost), §5.2 (24-cell parameter brackets), §5.4
  (sensitivity arms), §6 (functional-form pins), §6.1 (Det+churn S_t lock),
  §8 (anti-fishing invariants), §9 (verification gates), §10 (output
  artifact contract), §15 (CORRECTIONS-α v1.1.1 → v1.2 / v1.2.1 delta record).
- `docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md` — narrative
  Stage-2 verdict memo (synthetic-Bayesian PASS).

**Cohort plans**
- `docs/plans/2026-05-08-saas-cohort-1-t1-cost-posterior.md` v0.4 (C1).
- `docs/plans/2026-05-08-saas-cohort-2-t2-pricing-sign.md` v0.3 (C2).
- `docs/plans/2026-05-08-saas-cohort-3-revenue-form-loo.md` v0.3 (C3).
- `docs/plans/2026-05-08-saas-cohort-4-z-cap-derivation.md` v0.3 (C4).
- `docs/plans/2026-05-09-saas-cohort-close.md` (CLOSE plan; Phase-4 schema
  bump).
- `docs/plans/2026-05-09-stage-2-results-anchor.md` v0.2 (this anchor's
  authoring plan).

**Independent audit verdicts (31 files across 7 audit cycles)**
- `scratch/2026-05-08-saas-cohort-1-independent-audit/` (rc + mq + cr,
  v0.3 + v0.4).
- `scratch/2026-05-08-saas-cohort-2-independent-audit/` (rc + mq + cr,
  v0.2 + v0.3).
- `scratch/2026-05-08-saas-cohort-3-independent-audit/` (rc + mq + combined,
  v0.3).
- `scratch/2026-05-08-saas-cohort-4-independent-audit/` (rc + mq + cr,
  v0.2 + v0.3).
- `scratch/2026-05-09-spec-v1.2-review/`.
- `scratch/2026-05-09-phase-4-schema-bump-review/`.
- `scratch/2026-05-09-cohort-close-plan-review/`.
- (Plus `scratch/2026-05-09-stage-2-memo-review/` and the plan-review
  directories at `scratch/2026-05-09-stage-2-results-anchor-plan-review/`,
  `scratch/2026-05-09-phase-2-path-alpha/`.)

**Codepaths**
- `simulations/types/distributions.py` (`TruncParetoParams`,
  `NegBinParams`).
- `simulations/types/__init__.py` (Value-tier exports).
- `simulations/modules/fx_path.py` (FXPath + `RealizedVarianceCalc`).
- `simulations/saas_builder/priors.py` (M1 α-floor; NegBin reparameterization
  μ,φ → r,p).
- `simulations/saas_builder/model.py` (T1ModelFactory; M3 closed form;
  marginalization narrative).
- `simulations/saas_builder/diagnostics.py` (gate floors).
- `simulations/saas_builder/emit.py` (PP draws + parquet round-trip).
- `simulations/saas_builder/cohort_2/{pricing,derivatives,sign_cert,robustness,io,types}.py`.
- `simulations/saas_builder/cohort_3/{models,priors,loo,io,types}.py`.
- `simulations/saas_builder/cohort_4/{pi_derivation,z_cap,sign_cert,io,types}.py`.
- `simulations/tests/test_saas_builder.py`,
  `test_saas_cohort2.py`,
  `test_saas_cohort3.py`,
  `test_saas_cohort4.py`,
  `test_modules.py`,
  `test_types.py`,
  `test_utils.py`.

**Emitted artifacts**
- `simulations/saas_builder/data/Z_cap_pinned.json` (sha `1fb1f7a4…5d31`).
- `simulations/saas_builder/data/gate_verdict.json` (sha `4da660b5…2173`).
- `simulations/saas_builder/data/revenue_form_verdict.json`
  (sha `588a491b…8adb`).
- `simulations/saas_builder/data/_AUDIT.json` (sha `ded06012…162a`).
- `simulations/saas_builder/data/synthetic_tau_t/` (3 partitions; 712k
  draws).
- `simulations/saas_builder/data/cohort_prior.parquet`.
- `simulations/saas_builder/data/PRIMARY_RESULTS.md`,
  `ROBUSTNESS_RESULTS.md`,
  `Z_cap_pinned.SIGN_VERDICTS.md`.

**Framework anchors**
- `CLAUDE.md` — Abrigo Operating Framework, ideal-scenario clause
  (ll. 31–46); anti-fishing invariants (`N_MIN = 75`, `POWER_MIN = 0.80`,
  `MDES_SD = 0.40`); feedback memories `feedback_pathological_halt_anti_fishing_checkpoint`,
  `feedback_post_hoc_fit_anti_fishing_pattern`,
  `feedback_no_code_in_specs_or_plans`,
  `feedback_specialized_agents_per_task`.

---

## §v1.0 → v1.1 patch notes

Folds 5 non-blocking FLAGs from the 2-wave RC + MQ verify of the Stage-2 results
anchor (`scratch/2026-05-09-stage-2-results-anchor-doc-review/`). All FLAGs are
nomenclature/clarity tightenings; no substantive math, no upstream-claim
relaxation, no new claims introduced. Frozen HEAD `9fd92e5` unchanged.

1. **RC-FLAG-1 — §0 README.md carve-out** (rc-verdict.md ll. 99–112).
   §0 wording extended to enumerate the in-scope `simulations/` subdirectories
   (`saas_builder/`, `modules/`, `types/`, `utils/`, `tests/`) and explicitly
   carve out the `simulations/README.md` doc-only diff already permitted by
   §5 ll. 612–614. Resolution: §0 "Status — Stage-2 frozen anchor" paragraph
   updated.

2. **RC-FLAG-2 — §2.A.4 verbatim labeling** (rc-verdict.md ll. 114–120).
   §2.A.4 now opens "PRIMITIVES.md eq. (10) verbatim — the boxed primitive
   asserts:" and adds a trailing clarifier that the strict-negativity inequality
   `< 0` is reproduced from upstream, not asserted by this document. Disambiguates
   doc-author claim from upstream claim.

3. **MQ-FLAG-1 — §2.A.6 σ_T label** (mq-verdict.md l. 73).
   "large-t asymptotic" replaced with "algebraic inversion of PRIMITIVES.md
   eq. (8)" to match PRIMITIVES.md §6 nomenclature. Math identical.

4. **MQ-FLAG-2 — §2.B.4 schema-bump scope** (mq-verdict.md l. 75).
   §2.B.4 post-cycle paragraph extended with explicit scope: v1.1 bump applies
   only to `Z_cap_pinned.json` (Phase-4 additive `sign_verdicts` field);
   `synthetic_tau_t/` and `cohort_prior.parquet` remain at v1.0. Reconciles
   §2.D.1 row label with §2.B.4 / §2.D.7.

5. **MQ-FLAG-3 — §4.1 detection-heuristic co-naming** (mq-verdict.md l. 77).
   §4.1 (c) co-names the formal "tautological-identity audit" with the
   operational first-catch "ESS-floor sampler diagnostic" (ESS=38 vs gate floor
   1{,}000). Both are retained; the derivation-anchor citation check remains.

*End of STAGE_2_RESULTS — Stage-2 anchor frozen at HEAD `9fd92e5`; doc v1.1.*
