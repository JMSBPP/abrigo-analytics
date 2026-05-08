"""Sign-certification gate Callable for SAAS-COHORT-2.

Implements:

- :class:`SignCertificationGate` — for each ``BracketPoint`` in a
  ``BracketGrid``, evaluates Δ^(a_s) over posterior τ_t draws,
  computes the posterior-predictive 95% credible interval (NOT
  bootstrap; spec §9 row TODO-COHORT-2), and certifies
  ``delta_upper_bound_95 < 0`` strictly per Pin BRACKET-M5.
- :class:`PPCQuantileCoverageCheck` — computes empirical coverage of
  the nominal 95% credible interval at τ_t quantiles ``{50, 90, 99}``-pct
  and raises :class:`PPCQuantileMiscoverageError` when any falls outside
  ``[0.93, 0.97]`` (MQ-FLAG-3 v0.2 fix).

Verdict alphabet per spec §10 line 520 (verbatim): ``PASS|WEAK|MARGINAL|
FAIL|INDISTINGUISHABLE``. HALT is a foreground action — not a verdict
value emitted to ``gate_verdict.json``.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final, Mapping

import numpy as np
from numpy.typing import NDArray

from simulations.saas_builder.cohort_2._errors import (
    PPCQuantileMiscoverageError,
)
from simulations.saas_builder.cohort_2.derivatives import (
    DeltaNumericalEvaluator,
)
from simulations.saas_builder.cohort_2.types import (
    BracketGrid,
    CohortGateVerdict,
    SignVerdict,
    VerdictLabel,
)

# ─── Module-level constants ───────────────────────────────────────────────────

#: Default credible-interval level (spec §9 TODO-COHORT-2).
DEFAULT_CI_LEVEL: Final[float] = 0.95

#: Pin (MQ-FLAG-3 v0.2 fix) — τ_t quantiles whose PPC coverage is checked.
PPC_QUANTILE_LEVELS: Final[tuple[float, float, float]] = (0.50, 0.90, 0.99)

#: PPC coverage tolerance band ±0.02 around the nominal 95% level
#: (MQ-FLAG-3 v0.2 fix; calibration ±0.02 implied: nominal 0.95).
PPC_COVERAGE_LOWER: Final[float] = 0.93
PPC_COVERAGE_UPPER: Final[float] = 0.97
PPC_NOMINAL_LEVEL: Final[float] = 0.95


# ─── Helpers ────────────────────────────────────────────────────────────────


def _credible_interval(
    delta_draws: NDArray[np.float64], ci_level: float
) -> tuple[float, float, float]:
    """Return ``(median, lower, upper)`` credible-interval bounds.

    Pure quantile-based (NOT bootstrap; spec §9 row TODO-COHORT-2
    explicitly forbids bootstrap).
    """
    if not (0.0 < ci_level < 1.0):
        raise ValueError(
            f"_credible_interval: ci_level = {ci_level} must lie in (0, 1)"
        )
    alpha = 1.0 - ci_level
    lower_q = alpha / 2.0
    upper_q = 1.0 - alpha / 2.0
    median = float(np.median(delta_draws))
    lower = float(np.quantile(delta_draws, lower_q))
    upper = float(np.quantile(delta_draws, upper_q))
    return (median, lower, upper)


def _audit_block_for(payload: bytes) -> str:
    """Compute sha256 of payload as 64-char lowercase hex."""
    return hashlib.sha256(payload).hexdigest()


def _now_utc_iso() -> str:
    """ISO-8601 UTC timestamp, second precision."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ─── Sign-certification gate ────────────────────────────────────────────────


@dataclass(frozen=True)
class SignCertificationGate:
    """Pin BRACKET-M5 sign-certification gate.

    For each ``BracketPoint`` in ``grid``, computes Δ^(a_s) over the
    posterior τ_t draws (shape ``(n_draws, T)``), then certifies via
    posterior-predictive 95% credible interval that
    ``delta_upper_bound_95 < 0`` strictly. A single failure flips the
    verdict to ``FAIL`` and records ``n_sign_violations``.

    Verdict alphabet (spec §10 line 520): ``PASS|WEAK|MARGINAL|FAIL|
    INDISTINGUISHABLE``. The gate emits ``PASS`` if all bracket points
    strictly negative; ``FAIL`` otherwise. ``WEAK`` / ``MARGINAL`` /
    ``INDISTINGUISHABLE`` are reserved for future cohort-2 sub-verdicts
    (e.g. CI straddling zero with a robust median negative); the present
    implementation routes every non-PASS outcome to ``FAIL`` until those
    sub-verdicts are pinned by spec.
    """

    grid: BracketGrid
    sigma_T: float
    ci_level: float = DEFAULT_CI_LEVEL

    def __post_init__(self) -> None:
        if not (math.isfinite(self.sigma_T) and self.sigma_T > 0.0):
            raise ValueError(
                f"SignCertificationGate.sigma_T = {self.sigma_T}"
                " must be a finite float > 0"
            )
        if not (0.0 < self.ci_level < 1.0):
            raise ValueError(
                f"SignCertificationGate.ci_level = {self.ci_level}"
                " must lie in (0, 1)"
            )

    def __call__(
        self,
        tau_t_draws_per_bracket: tuple[NDArray[np.float64], ...],
        ppc_coverage: Mapping[str, float] | None = None,
    ) -> CohortGateVerdict:
        """Run the sign-certification gate over the bracket grid.

        Args:
            tau_t_draws_per_bracket: tuple of length ``len(grid.points)``;
                each entry is a 2-D float64 array of shape ``(n_draws, T_i)``
                aligned with ``grid.points[i].horizon_T``.
            ppc_coverage: optional pre-computed PPC coverage mapping for
                the {p50, p90, p99} τ_t quantiles. The gate does NOT
                re-compute coverage internally; it records what is
                provided. When ``None``, an empty mapping is recorded.

        Returns:
            ``CohortGateVerdict``.

        Raises:
            ValueError: shape mismatch between draws and grid.
        """
        n = len(self.grid.points)
        if len(tau_t_draws_per_bracket) != n:
            raise ValueError(
                "SignCertificationGate: tau_t_draws_per_bracket length"
                f" {len(tau_t_draws_per_bracket)} must equal grid size {n}"
            )

        evidence: list[SignVerdict] = []
        n_violations = 0
        for idx, (point, draws) in enumerate(
            zip(self.grid.points, tau_t_draws_per_bracket, strict=True)
        ):
            evaluator = DeltaNumericalEvaluator(
                bracket=point, sigma_T=self.sigma_T
            )
            delta_draws = evaluator(draws)
            median, lower, upper = _credible_interval(
                delta_draws, self.ci_level
            )
            strict = upper < 0.0
            if not strict:
                n_violations += 1
            verdict_evidence = SignVerdict(
                bracket_index=idx,
                delta_median=median,
                delta_lower_bound_95=lower,
                delta_upper_bound_95=upper,
                sign_strictly_negative=strict,
            )
            evidence.append(verdict_evidence)

        verdict_label: VerdictLabel = "PASS" if n_violations == 0 else "FAIL"
        # Audit block — sha256 of the (verdict-label, evidence-tuple repr).
        payload = repr(
            (
                verdict_label,
                tuple(
                    (
                        ev.bracket_index,
                        ev.delta_median,
                        ev.delta_lower_bound_95,
                        ev.delta_upper_bound_95,
                        ev.sign_strictly_negative,
                    )
                    for ev in evidence
                ),
            )
        ).encode("utf-8")
        return CohortGateVerdict(
            sub_task="COHORT-2",
            verdict=verdict_label,
            n_bracket_points=n,
            n_sign_violations=n_violations,
            evidence=tuple(evidence),
            audit_block=_audit_block_for(payload),
            fetched_at_utc=_now_utc_iso(),
            ppc_coverage=dict(ppc_coverage) if ppc_coverage else {},
        )


# ─── PPC quantile coverage check (MQ-FLAG-3 v0.2 fix) ────────────────────────


@dataclass(frozen=True)
class PPCQuantileCoverageCheck:
    """Posterior-predictive coverage diagnostic at pinned τ_t quantiles.

    Pin (MQ-FLAG-3 v0.2 fix; plan Task 2.5): at each of the user-relevant
    τ_t quantiles ``{50, 90, 99}``-pct, empirical coverage of the nominal
    95% credible interval must fall within ``[0.93, 0.97]`` (calibration
    tolerance ±0.02). Failure indicates the posterior CI is mis-calibrated
    and could absorb a near-zero Δ sign violation; the check raises
    :class:`PPCQuantileMiscoverageError` (HALT trigger).

    Computation: given ``(n_draws, T)`` posterior τ_t draws and a
    ``(n_obs, T)`` array of held-out τ_t observations (one held-out
    sample per posterior draw, paired by index), compute the empirical
    quantile τ_q across each draw / observation pair and verify that the
    fraction of observations falling within the per-draw 95% credible
    interval is within ``[0.93, 0.97]``.
    """

    nominal_level: float = PPC_NOMINAL_LEVEL
    coverage_lower: float = PPC_COVERAGE_LOWER
    coverage_upper: float = PPC_COVERAGE_UPPER

    def __post_init__(self) -> None:
        if not (0.0 < self.nominal_level < 1.0):
            raise ValueError(
                f"PPCQuantileCoverageCheck.nominal_level = {self.nominal_level}"
                " must lie in (0, 1)"
            )
        if not (
            0.0 < self.coverage_lower
            < self.nominal_level
            < self.coverage_upper
            < 1.0
        ):
            raise ValueError(
                "PPCQuantileCoverageCheck: must satisfy 0 < coverage_lower"
                " < nominal_level < coverage_upper < 1;"
                f" got ({self.coverage_lower}, {self.nominal_level},"
                f" {self.coverage_upper})"
            )

    def __call__(
        self,
        ppc_draws: NDArray[np.float64],
        observed_quantiles: Mapping[str, NDArray[np.float64]],
    ) -> dict[str, float]:
        """Return empirical coverage per quantile; raise on miscoverage.

        Args:
            ppc_draws: 2-D float64 array of shape ``(n_ppc, n_obs)`` —
                posterior-predictive τ_t draws across observation
                replicates.
            observed_quantiles: mapping from ``"p50"|"p90"|"p99"`` to a
                1-D float64 array of length ``n_obs`` holding the
                observed τ_t quantile per replicate.

        Returns:
            Mapping ``{"p50": coverage, "p90": coverage, "p99": coverage}``
            of empirical coverage values in ``[0, 1]``.

        Raises:
            ValueError: input-shape mismatch.
            PPCQuantileMiscoverageError: any quantile's coverage outside
                ``[coverage_lower, coverage_upper]``.
        """
        if ppc_draws.ndim != 2:
            raise ValueError(
                f"PPCQuantileCoverageCheck: ppc_draws.ndim = {ppc_draws.ndim}"
                " must be 2"
            )
        n_ppc, n_obs = ppc_draws.shape
        if n_ppc < 1 or n_obs < 1:
            raise ValueError(
                f"PPCQuantileCoverageCheck: ppc_draws.shape = {ppc_draws.shape}"
                " must have positive size on both axes"
            )

        alpha = 1.0 - self.nominal_level
        lower_q = alpha / 2.0
        upper_q = 1.0 - alpha / 2.0
        # Per-replicate (column) credible interval across the ppc axis.
        col_lower = np.quantile(ppc_draws, lower_q, axis=0)
        col_upper = np.quantile(ppc_draws, upper_q, axis=0)

        coverage: dict[str, float] = {}
        for key, level in zip(("p50", "p90", "p99"), PPC_QUANTILE_LEVELS):
            if key not in observed_quantiles:
                raise ValueError(
                    f"PPCQuantileCoverageCheck: observed_quantiles missing"
                    f" key {key!r}"
                )
            obs = observed_quantiles[key]
            if obs.ndim != 1 or obs.shape[0] != n_obs:
                raise ValueError(
                    "PPCQuantileCoverageCheck: observed_quantiles"
                    f" [{key!r}] shape = {obs.shape} must be 1-D"
                    f" with length {n_obs}"
                )
            in_band = (obs >= col_lower) & (obs <= col_upper)
            cov = float(np.mean(in_band))
            coverage[key] = cov
            del level  # exposed via PPC_QUANTILE_LEVELS for traceability

        # Threshold check.
        for key, cov in coverage.items():
            if not (self.coverage_lower <= cov <= self.coverage_upper):
                raise PPCQuantileMiscoverageError(
                    "PPCQuantileCoverageCheck: empirical coverage at"
                    f" quantile {key} = {cov:.4f} outside band"
                    f" [{self.coverage_lower}, {self.coverage_upper}];"
                    " HALT per anti-fishing"
                    " (feedback_pathological_halt_anti_fishing_checkpoint)"
                )
        return coverage


__all__ = [
    "DEFAULT_CI_LEVEL",
    "PPCQuantileCoverageCheck",
    "PPC_COVERAGE_LOWER",
    "PPC_COVERAGE_UPPER",
    "PPC_NOMINAL_LEVEL",
    "PPC_QUANTILE_LEVELS",
    "SignCertificationGate",
]
