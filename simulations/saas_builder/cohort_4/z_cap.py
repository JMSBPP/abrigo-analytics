r"""Posterior-predictive Z-cap evaluator + 5-test-point sign certification.

Plan v0.2 §Phase-2 Task 2.2 / 2.4 / Pin M2 (5-TP sign cert) / Pin M2-fix
(MC error budget). NO IO at this tier — emission is delegated to
``cohort_4.io``.

Z definition (spec §4.1 cap operationalization):

    Z = E[q_t^USD / (X/Y)_t + π(t)]

with ``q_t^USD`` drawn from the C1 ``synthetic_tau_t`` panel and ``π(t)``
the closed-form streamed premium derived in ``pi_derivation.py``.

Per-test-point: each TP fixes ``(κ, X̄/Ȳ, σ₀)``; the per-draw posterior-
predictive realisation is::

    Z_d = (q_t_cop)_d / (X̄/Ȳ)_TP + π(t_anchor; K⋆_d, σ₀, ε, ω, t_anchor, κ_TP)

with ``K⋆_d = (q_t_cop)_d`` (per-draw equilibrium strike — units of
COP per month, the cohort's posterior-predictive overage realisation).
This identification ties the convex-hedge notional to the C1 posterior's
overage distribution, satisfying the saas-note §4.1 pitch identity.

The MC stderr/Ẑ ≤ 1e-3 budget is enforced at runtime; breaches raise
``MCErrorBudgetExceededError``. Sign violations (any per-TP ``ci_95_lo
≤ 0``) raise ``DiagnosticGateError`` per the HALT protocol.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from simulations.saas_builder.cohort_4._errors import (
    DiagnosticGateError,
    IdentityToleranceError,
    MCErrorBudgetExceededError,
)
from simulations.saas_builder.cohort_4.pi_derivation import (
    IdentityResidualEvaluator,
)
from simulations.saas_builder.cohort_4.types import (
    MCBudget,
    MC_DRAWS_FLOOR,
    NUMERICAL_IDENTITY_TOL,
    PiTSymbolic,
    SignVerdict,
    TestPoint,
    ZEvaluationResult,
    stderr_ratio,
)

# ─── Defaults (plan v0.2 §M2 + spec §6 functional-form pins) ─────────────────

#: Spec §6 / PRIMITIVES.md §6 — ε ∈ (0, 1) FX-path amplitude (default mid-bracket).
DEFAULT_FX_EPSILON: float = 0.1

#: Spec §6 — ω > 0 FX-path frequency (default; M5-anchor compatible).
DEFAULT_FX_OMEGA: float = 1.0

#: Spec §2 — monthly time grain; t_anchor = T/2 = 6.0 months for stable σ_T.
DEFAULT_T_ANCHOR: float = 6.0


# ─── Z evaluator (Callable tier) ─────────────────────────────────────────────


@dataclass(frozen=True)
class PerDrawZEvaluator:
    """Compute the per-draw Z realisation array for one TestPoint.

    Inputs at ``__call__``:

    - ``pi_t``: PiTSymbolic carrying the lambdified π(t).
    - ``test_point``: one TestPoint (κ, X̄/Ȳ, σ₀, label).
    - ``q_t_cop_draws``: 1-D float64 array of posterior-predictive
      ``q_t^cop`` realisations from the C1 synthetic_tau_t panel.

    Returns: ZEvaluationResult carrying the per-draw Z array + summary
    statistics + the identity residual at this test point.

    Pin M2-fix (MC error budget) is enforced upstream by ``ZCapRunner``;
    this Callable computes the budget metric but does not raise on breach.
    """

    fx_epsilon: float = DEFAULT_FX_EPSILON
    fx_omega: float = DEFAULT_FX_OMEGA
    t_anchor: float = DEFAULT_T_ANCHOR
    identity_evaluator: IdentityResidualEvaluator = IdentityResidualEvaluator()

    def __post_init__(self) -> None:
        if not (0.0 < self.fx_epsilon < 1.0):
            raise ValueError(
                f"PerDrawZEvaluator.fx_epsilon = {self.fx_epsilon}"
                " must lie in (0, 1) per spec §6"
            )
        if not (self.fx_omega > 0.0):
            raise ValueError(
                f"PerDrawZEvaluator.fx_omega = {self.fx_omega} must be > 0"
            )
        if not (self.t_anchor > 0.0):
            raise ValueError(
                f"PerDrawZEvaluator.t_anchor = {self.t_anchor}"
                " must be > 0 (σ_T(t) has 1/t factor)"
            )

    def __call__(
        self,
        pi_t: PiTSymbolic,
        test_point: TestPoint,
        q_t_cop_draws: NDArray[np.float64],
    ) -> ZEvaluationResult:
        """Return the per-draw posterior-predictive Z result."""
        if q_t_cop_draws.ndim != 1:
            raise ValueError(
                "PerDrawZEvaluator: q_t_cop_draws.ndim ="
                f" {q_t_cop_draws.ndim} must be 1"
            )
        if q_t_cop_draws.size < MC_DRAWS_FLOOR:
            raise ValueError(
                f"PerDrawZEvaluator: q_t_cop_draws.size = {q_t_cop_draws.size}"
                f" must be ≥ {MC_DRAWS_FLOOR} (Pin M2-fix)"
            )
        if not np.all(np.isfinite(q_t_cop_draws)):
            raise ValueError(
                "PerDrawZEvaluator: q_t_cop_draws contains non-finite values"
            )
        if not np.all(q_t_cop_draws >= 0.0):
            raise ValueError(
                "PerDrawZEvaluator: q_t_cop_draws contains negative values;"
                " q_t^cop is a cost (must be ≥ 0)"
            )

        # K⋆_d = (q_t_cop)_d (per-draw equilibrium strike — saas-note §4.1
        # pitch identity ties hedge notional to expected COP overage).
        # Add a small floor to keep K⋆ > 0 (PiTSymbolic positivity assumption).
        K_star_per_draw = np.maximum(q_t_cop_draws, 1e-12).astype(np.float64)

        # π(t_anchor; K⋆_d, σ₀, ε, ω, t_anchor, κ_TP) per draw.
        pi_per_draw = pi_t.lambdified(
            K_star_per_draw,
            test_point.sigma_0,
            self.fx_epsilon,
            self.fx_omega,
            self.t_anchor,
            test_point.kappa,
        )
        pi_per_draw = np.asarray(pi_per_draw, dtype=np.float64)

        # q_t_cop / (X̄/Ȳ) per draw.
        q_over_xy = q_t_cop_draws / test_point.x_over_y_bar

        # Z_d = q/(X/Y) + π(t).
        z_per_draw = (q_over_xy + pi_per_draw).astype(np.float64, copy=False)
        if not np.all(np.isfinite(z_per_draw)):
            raise ValueError(
                "PerDrawZEvaluator: per-draw Z contains non-finite values"
            )

        z_mean = float(np.mean(z_per_draw))
        z_var = float(np.var(z_per_draw, ddof=1))
        z_stderr = float(np.sqrt(z_var / z_per_draw.size))
        ci_95_lo = float(np.percentile(z_per_draw, 2.5))
        ci_95_hi = float(np.percentile(z_per_draw, 97.5))

        # Numerical identity residual at this TP (uses K⋆ = posterior-mean).
        K_star_mean = float(np.mean(K_star_per_draw))
        identity_residual = self.identity_evaluator(
            pi_t,
            K_star=K_star_mean,
            sigma_0=test_point.sigma_0,
            epsilon=self.fx_epsilon,
            omega=self.fx_omega,
            kappa=test_point.kappa,
        )

        return ZEvaluationResult(
            label=test_point.label,
            z_per_draw=z_per_draw,
            z_mean=z_mean,
            z_stderr=z_stderr,
            ci_95_lo=ci_95_lo,
            ci_95_hi=ci_95_hi,
            identity_residual=identity_residual,
        )


# ─── 5-test-point sign certification (Callable tier) ─────────────────────────


@dataclass(frozen=True)
class SignCertifier:
    """Convert a tuple of ``ZEvaluationResult`` into per-TP ``SignVerdict``.

    Plan v0.2 §M2 sign expectation (immutable per anti-fishing): every TP
    must have ``ci_95_lo > 0``. Identity residual must be ≤
    ``NUMERICAL_IDENTITY_TOL = 1e-6`` (Path A v0 §10.4 inheritance).

    Monotonicity check (called separately by the runner):
    ``|π|_TP2 > |π|_TP1 > |π|_TP3`` (∂|π|/∂κ < 0 strict, plan v0.2 M2-fix).
    """

    def __call__(
        self, results: Sequence[ZEvaluationResult]
    ) -> tuple[SignVerdict, ...]:
        """Return one SignVerdict per ZEvaluationResult."""
        return tuple(
            SignVerdict(
                label=r.label,
                z_value=r.z_mean,
                ci_95_lo=r.ci_95_lo,
                ci_95_hi=r.ci_95_hi,
                passes=r.ci_95_lo > 0.0,
                identity_residual=r.identity_residual,
                identity_passes=r.identity_residual <= NUMERICAL_IDENTITY_TOL,
            )
            for r in results
        )


def assert_pin_m2_monotonicity(
    pi_t: PiTSymbolic,
    test_points: Sequence[TestPoint],
    fx_epsilon: float = DEFAULT_FX_EPSILON,
    fx_omega: float = DEFAULT_FX_OMEGA,
    t_anchor: float = DEFAULT_T_ANCHOR,
    K_star_anchor: float = 1.0e6,
) -> tuple[float, float, float]:
    """Return ``(|π|_TP2, |π|_TP1, |π|_TP3)`` and assert strict monotonicity.

    Plan v0.2 §M2-fix: ``∂|π|/∂κ < 0`` strict. Equivalent strict chain
    ``|π|_TP2 > |π|_TP1 > |π|_TP3`` is asserted at fixed
    ``(X̄/Ȳ_0, σ_0, K⋆_anchor)``. Raises ``DiagnosticGateError`` on
    violation.

    Args:
        pi_t: symbolic π(t) anchor.
        test_points: must include TP1, TP2, TP3 in canonical positions
            (the default 5-tuple from ``make_default_test_point_grid``).
        fx_epsilon, fx_omega, t_anchor: shared FX path constants.
        K_star_anchor: shared K⋆ for the κ-direction property test.

    Returns:
        Tuple ``(|π|_TP2, |π|_TP1, |π|_TP3)`` for downstream sidecar
        emission.
    """
    by_label = {tp.label: tp for tp in test_points}
    missing = {"TP1", "TP2", "TP3"} - by_label.keys()
    if missing:
        raise DiagnosticGateError(
            f"assert_pin_m2_monotonicity: missing test-points {sorted(missing)};"
            " plan v0.2 §M2 grid requires TP1..TP3 (κ-monotonicity branch)"
        )
    pi_vals: dict[str, float] = {}
    for label in ("TP1", "TP2", "TP3"):
        tp = by_label[label]
        pi_v = pi_t.lambdified(
            K_star_anchor,
            tp.sigma_0,
            fx_epsilon,
            fx_omega,
            t_anchor,
            tp.kappa,
        )
        pi_vals[label] = float(np.abs(np.asarray(pi_v).item()))
    # Strict monotonicity: |π|_TP2 > |π|_TP1 > |π|_TP3.
    if not (pi_vals["TP2"] > pi_vals["TP1"] > pi_vals["TP3"]):
        raise DiagnosticGateError(
            "Pin M2 monotonicity violation:"
            f" |π|_TP2={pi_vals['TP2']:.6e},"
            f" |π|_TP1={pi_vals['TP1']:.6e},"
            f" |π|_TP3={pi_vals['TP3']:.6e};"
            " required strict chain |π|_TP2 > |π|_TP1 > |π|_TP3"
            " (plan v0.2 §M2-fix ∂|π|/∂κ < 0)"
        )
    return (pi_vals["TP2"], pi_vals["TP1"], pi_vals["TP3"])


# ─── Top-level cohort runner (Callable tier) ─────────────────────────────────


@dataclass(frozen=True)
class ZCapRunner:
    """Orchestrate the 5-test-point Z-cap evaluation + pin emission.

    Outputs a tuple ``(per_tp_results, sign_verdicts, monotonicity_triple)``
    consumed by ``cohort_4.io.pin_and_emit``. No IO at this tier.

    Pin M2-fix MC budget enforcement: every TP's ``ZEvaluationResult`` is
    checked against ``mc_budget.stderr_ratio_ceiling`` immediately after
    evaluation; on breach, ``MCErrorBudgetExceededError`` is raised
    (HALT routing per ``feedback_pathological_halt_anti_fishing_checkpoint``).

    Sign / identity gates: any TP failing ``passes`` or ``identity_passes``
    raises ``DiagnosticGateError`` / ``IdentityToleranceError`` respectively.
    """

    per_draw_evaluator: PerDrawZEvaluator = PerDrawZEvaluator()
    sign_certifier: SignCertifier = SignCertifier()
    mc_budget: MCBudget = MCBudget(n_draws=MC_DRAWS_FLOOR)

    def __call__(
        self,
        pi_t: PiTSymbolic,
        test_points: Sequence[TestPoint],
        q_t_cop_draws: NDArray[np.float64],
    ) -> tuple[
        tuple[ZEvaluationResult, ...],
        tuple[SignVerdict, ...],
        tuple[float, float, float],
    ]:
        """Evaluate all 5 test points + sign-certify + monotonicity-check."""
        if len(test_points) != 5:
            raise ValueError(
                f"ZCapRunner: test_points must have length 5;"
                f" got {len(test_points)}"
            )
        # Need ≥ mc_budget.n_draws posterior draws.
        if q_t_cop_draws.size < self.mc_budget.n_draws:
            raise ValueError(
                f"ZCapRunner: q_t_cop_draws.size = {q_t_cop_draws.size}"
                f" must be ≥ mc_budget.n_draws = {self.mc_budget.n_draws}"
            )
        # Truncate to exactly n_draws if the C1 panel is larger
        # (deterministic — first n rows; C1 emits a sorted panel).
        draws = q_t_cop_draws[: self.mc_budget.n_draws].astype(
            np.float64, copy=False
        )

        results = tuple(
            self.per_draw_evaluator(pi_t, tp, draws) for tp in test_points
        )

        # MC budget enforcement (Pin M2-fix).
        for r in results:
            ratio = stderr_ratio(r)
            if ratio > self.mc_budget.stderr_ratio_ceiling:
                raise MCErrorBudgetExceededError(
                    f"MC budget breach at {r.label}:"
                    f" stderr/Ẑ = {ratio:.6e} > "
                    f"ceiling {self.mc_budget.stderr_ratio_ceiling:.6e};"
                    f" N_draws = {draws.size};"
                    " HALT per feedback_pathological_halt_anti_fishing_checkpoint"
                )

        # Identity-tolerance gate (Pin M2 numerical inheritance).
        for r in results:
            if r.identity_residual > NUMERICAL_IDENTITY_TOL:
                raise IdentityToleranceError(
                    f"Identity residual breach at {r.label}:"
                    f" residual = {r.identity_residual:.6e}"
                    f" > tol {NUMERICAL_IDENTITY_TOL:.6e};"
                    " HALT per feedback_pathological_halt_anti_fishing_checkpoint"
                )

        sign_verdicts = self.sign_certifier(results)

        # Sign gate (Pin M2 — Z_cap > 0 ∀ TP).
        violations = [v for v in sign_verdicts if not v.passes]
        if violations:
            raise DiagnosticGateError(
                "Sign verdict failure at"
                f" {[v.label for v in violations]}:"
                " ci_95_lo ≤ 0 — HALT per spec §8(1) +"
                " feedback_pathological_halt_anti_fishing_checkpoint"
            )

        # Monotonicity assertion (uses K⋆ = posterior-mean for stability).
        K_star_mean = float(np.mean(np.maximum(draws, 1e-12)))
        monotonicity_triple = assert_pin_m2_monotonicity(
            pi_t,
            test_points,
            fx_epsilon=self.per_draw_evaluator.fx_epsilon,
            fx_omega=self.per_draw_evaluator.fx_omega,
            t_anchor=self.per_draw_evaluator.t_anchor,
            K_star_anchor=K_star_mean,
        )

        return results, sign_verdicts, monotonicity_triple


__all__ = [
    "DEFAULT_FX_EPSILON",
    "DEFAULT_FX_OMEGA",
    "DEFAULT_T_ANCHOR",
    "PerDrawZEvaluator",
    "SignCertifier",
    "ZCapRunner",
    "assert_pin_m2_monotonicity",
]
