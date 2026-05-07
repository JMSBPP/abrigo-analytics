"""Posterior-draw and emission Value containers.

Covers spec §10 emission schemas at the **Value-tier** layer (the *row*
TypedDict shapes used by the parquet/JSON readers live in
``simulations.utils`` per Phase 1 reconciliation §2.1):

- ``PosteriorDraws`` — frozen-dc holding numpy posterior arrays plus the
  parameter-metadata that disambiguates them. Consumed by sticky-cost /
  Z-pin downstream Callables.
- ``MonthlyCDF`` — pinned-percentile CDF (p10 / p50 / p90 / p99 per spec
  §9 TODO-COHORT-1 verdict gate).
- ``ZCapPinned`` — emission Value for ``estimates/Z_cap_pinned.json`` per
  spec §10. Includes ``schema_version`` per Phase 1 reconciliation §2.4.

Math pin involvement: M4 schema columns are validated at the IO boundary
in ``simulations.utils``. This file only carries the typed in-memory Values
that the IO boundary returns to consumers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Mapping

import numpy as np
from numpy.typing import NDArray

from simulations.types.tier import TIER_IDS, TierID

# ─── Module-level constants ───────────────────────────────────────────────────

#: Default schema version for emission artifacts (Phase 1 reconciliation §2.4).
DEFAULT_SCHEMA_VERSION: Final[str] = "v1.0"

#: Spec §9 pinned percentile grid for monthly $/mo CDF.
DEFAULT_CDF_PERCENTILES: Final[tuple[float, float, float, float]] = (
    10.0,
    50.0,
    90.0,
    99.0,
)


# ─── Value types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class PosteriorDraws:
    """Posterior-draws container for Stage-2 cohort calibration.

    Holds a 2-D numpy array of shape ``(n_chains * n_draws, n_params)`` plus
    the ordered parameter-name metadata that disambiguates columns. Per spec
    §8(8) the Stage-2 PyMC fits use ≥ 4000 draws across ≥ 4 chains; this Value
    container is the canonical hand-off shape from the sampler Callable
    (``simulations.modules``) to the analysis Callables.

    Validation contract:

    - ``draws.ndim == 2``;
    - ``draws.shape[1] == len(param_names)``;
    - ``len(param_names)`` ≥ 1;
    - ``param_names`` has no duplicates;
    - ``draws.shape[0]`` ≥ 1.

    Note:
        The numpy array is held by reference. Frozen-dc immutability does
        not prevent in-place mutation of array contents — callers MUST treat
        the array as read-only. Future hardening could ``draws.flags.writeable
        = False`` at construction time, but doing so cross-tier-couples to
        numpy semantics; the contract is documentary for now.
    """

    draws: NDArray[np.float64]
    param_names: tuple[str, ...]
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.draws.ndim != 2:
            raise ValueError(
                f"PosteriorDraws.draws.ndim = {self.draws.ndim} must be 2"
            )
        n_rows, n_cols = self.draws.shape
        if n_rows < 1:
            raise ValueError(
                f"PosteriorDraws.draws must have ≥ 1 row (got {n_rows})"
            )
        if len(self.param_names) < 1:
            raise ValueError("PosteriorDraws.param_names must be non-empty")
        if n_cols != len(self.param_names):
            raise ValueError(
                f"PosteriorDraws.draws.shape[1] = {n_cols} must equal"
                f" len(param_names) = {len(self.param_names)}"
            )
        if len(set(self.param_names)) != len(self.param_names):
            raise ValueError(
                f"PosteriorDraws.param_names contains duplicates: {self.param_names}"
            )


@dataclass(frozen=True)
class MonthlyCDF:
    """Pinned-percentile monthly $/mo CDF (spec §9 TODO-COHORT-1).

    Stores the posterior-predictive monthly cost CDF at the spec-pinned
    percentile grid (default p10 / p50 / p90 / p99). Per spec §9 the
    cohort-1 verdict gate compares these percentiles to the §5.2 brackets.

    Symbol map:

    - ``percentiles`` ↔ percentile grid (e.g. (10, 50, 90, 99));
    - ``values_usd`` ↔ posterior-predictive monthly cost in USD at each
      percentile (parallel to ``percentiles``);
    - ``currency`` ↔ ISO-4217 code; ``"USD"`` or ``"COP"``.

    Validation contract:

    - ``len(percentiles) == len(values_usd)`` and both ≥ 1;
    - ``percentiles`` strictly increasing in ``(0, 100)``;
    - ``values_usd`` non-decreasing and non-negative;
    - ``currency`` is one of ``("USD", "COP")``.
    """

    percentiles: tuple[float, ...]
    values_usd: tuple[float, ...]
    currency: str = "USD"

    def __post_init__(self) -> None:
        if len(self.percentiles) != len(self.values_usd):
            raise ValueError(
                f"MonthlyCDF: percentiles ({len(self.percentiles)}) and"
                f" values_usd ({len(self.values_usd)}) must have equal length"
            )
        if len(self.percentiles) < 1:
            raise ValueError("MonthlyCDF.percentiles must be non-empty")
        for i, q in enumerate(self.percentiles):
            if not (0.0 < q < 100.0):
                raise ValueError(
                    f"MonthlyCDF.percentiles[{i}] = {q} must lie in (0, 100)"
                )
            if i > 0 and not (q > self.percentiles[i - 1]):
                raise ValueError(
                    "MonthlyCDF.percentiles must be strictly increasing"
                    f" (got {self.percentiles!r})"
                )
        for i, v in enumerate(self.values_usd):
            if v < 0.0:
                raise ValueError(
                    f"MonthlyCDF.values_usd[{i}] = {v} must be ≥ 0"
                )
            if i > 0 and v < self.values_usd[i - 1]:
                raise ValueError(
                    "MonthlyCDF.values_usd must be non-decreasing"
                    f" (got {self.values_usd!r})"
                )
        if self.currency not in ("USD", "COP"):
            raise ValueError(
                f"MonthlyCDF.currency = {self.currency!r} must be 'USD' or 'COP'"
            )


@dataclass(frozen=True)
class ZCapPinned:
    """Pinned Z-cap emission Value for ``estimates/Z_cap_pinned.json`` (spec §10).

    Math pin M4 column-set (spec §10 + Phase 2 prelude):

    - ``Z_cop_per_month`` — posterior-predictive mean of monthly cap (COP);
    - ``ci_95_lo`` / ``ci_95_hi`` — 95% credible interval bounds;
    - ``audit_block`` — sha256 audit-block string (input-data lineage pin);
    - ``tier_mix`` — Mapping[TierID, float] of posterior tier mass;
    - ``schema_version`` — additive-only schema evolution tag (Phase 1
      reconciliation §2.4); default ``"v1.0"``.

    Validation contract:

    - ``Z_cop_per_month > 0``;
    - ``ci_95_lo ≤ Z_cop_per_month ≤ ci_95_hi`` and ``ci_95_lo > 0``;
    - ``audit_block`` is a 64-character lowercase hex string (sha256);
    - ``tier_mix`` keys are exactly ``TIER_IDS``; values in ``(0, 1]``
      summing to 1 within ``1e-9``;
    - ``schema_version`` is non-empty.
    """

    Z_cop_per_month: float
    ci_95_lo: float
    ci_95_hi: float
    audit_block: str
    tier_mix: Mapping[TierID, float] = field(
        default_factory=lambda: {"pro": 0.20, "max_5x": 0.50, "max_20x": 0.30}
    )
    schema_version: str = DEFAULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not (self.Z_cop_per_month > 0.0):
            raise ValueError(
                f"ZCapPinned.Z_cop_per_month = {self.Z_cop_per_month} must be > 0"
            )
        if not (self.ci_95_lo > 0.0):
            raise ValueError(
                f"ZCapPinned.ci_95_lo = {self.ci_95_lo} must be > 0"
            )
        if not (self.ci_95_lo <= self.Z_cop_per_month <= self.ci_95_hi):
            raise ValueError(
                f"ZCapPinned: must have ci_95_lo ({self.ci_95_lo})"
                f" ≤ Z_cop_per_month ({self.Z_cop_per_month})"
                f" ≤ ci_95_hi ({self.ci_95_hi})"
            )
        if len(self.audit_block) != 64 or not all(
            c in "0123456789abcdef" for c in self.audit_block
        ):
            raise ValueError(
                f"ZCapPinned.audit_block must be a 64-char lowercase hex sha256"
                f" (got len={len(self.audit_block)!r})"
            )
        if set(self.tier_mix.keys()) != set(TIER_IDS):
            raise ValueError(
                f"ZCapPinned.tier_mix keys must be exactly {set(TIER_IDS)};"
                f" got {set(self.tier_mix.keys())}"
            )
        for k, v in self.tier_mix.items():
            if not (0.0 < v <= 1.0):
                raise ValueError(
                    f"ZCapPinned.tier_mix[{k!r}] = {v} must lie in (0, 1]"
                )
        total = sum(self.tier_mix.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                f"ZCapPinned.tier_mix must sum to 1 (got {total!r})"
            )
        if not self.schema_version:
            raise ValueError("ZCapPinned.schema_version must be non-empty")


# ─── Free-function accessors ──────────────────────────────────────────────────


def n_total_draws(draws: PosteriorDraws) -> int:
    """Return the total number of posterior draws (rows)."""
    return int(draws.draws.shape[0])


def parameter_index(draws: PosteriorDraws, name: str) -> int:
    """Return the column index of a named parameter in ``draws.draws``."""
    try:
        return draws.param_names.index(name)
    except ValueError as exc:
        raise ValueError(
            f"PosteriorDraws has no parameter named {name!r};"
            f" available: {draws.param_names}"
        ) from exc


def cdf_percentile_value(cdf: MonthlyCDF, percentile: float) -> float:
    """Return the value at a pinned percentile, or raise if not pinned."""
    try:
        idx = cdf.percentiles.index(percentile)
    except ValueError as exc:
        raise ValueError(
            f"MonthlyCDF has no pinned percentile {percentile!r};"
            f" available: {cdf.percentiles}"
        ) from exc
    return cdf.values_usd[idx]


def ci_95_width(z: ZCapPinned) -> float:
    """Return the 95% CI width ``ci_95_hi - ci_95_lo``."""
    return z.ci_95_hi - z.ci_95_lo
