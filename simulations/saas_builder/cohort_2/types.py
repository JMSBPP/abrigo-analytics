r"""Value-tier containers for SAAS-COHORT-2 sign-certification gate.

All Value types are ``@dataclass(frozen=True)`` with ``__post_init__``
validation only. Free-function accessors live in this same module per the
functional-python skill (no methods on Value types).

Pin coverage:

- Pin M2 / M2-fit — ``T2CostParams`` carries (κ, β, p̄_sub, h_cache,
  w_in, w_out, p_in, p_out, tier-mix); β is the *fitted* value supplied
  by ``SoftplusBetaFitter`` and validated against Pin M2 by the shipped
  ``SoftplusRegularizer``. The tier-mix is a 3-key ``Mapping[TierID,
  float]`` summing to 1 within ``1e-9``.
- Pin Δ-cohort / Γ-cohort — ``BracketPoint`` packages one
  (T2CostParams, FXPathParams, σ_T, T) tuple consumed by the Δ / Γ
  evaluators. ``BracketPoint.__post_init__`` validates the M5
  path-reconstruction at ``t ∈ {0, π/2, π}``.
- Pin BRACKET-M5 — ``BracketGrid`` is an immutable tuple of
  ``BracketPoint`` whose construction passes through every member's
  M5 reconstruction check. Length ≥ 1.
- Pin spec §10 line 520 verdict alphabet — ``CohortGateVerdict.verdict``
  is ``Literal["PASS","WEAK","MARGINAL","FAIL","INDISTINGUISHABLE"]``
  (verbatim). HALT is a foreground/harness action and is NOT a
  verdict-enum value (RC-BLOCK-2 v0.2 fix).
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping as MappingABC
from dataclasses import dataclass, field
from typing import Final, Literal, Mapping, TypeAlias

import numpy as np
from numpy.typing import NDArray

from simulations.saas_builder.cohort_2._errors import FXPathReconstructionError
from simulations.types.fx import FXPathParams

# ─── Module-level constants ───────────────────────────────────────────────────

#: Pin BRACKET-M5 — anchor times for the M5 path reconstruction.
M5_ANCHOR_TIMES: Final[tuple[float, float, float]] = (
    0.0,
    math.pi / 2.0,
    math.pi,
)

#: Pin BRACKET-M5 — anchor values that the M5 path MUST recover at the
#: anchor times. Cross-reference shipped test
#: ``simulations/tests/test_modules.py:185,194``
#: (``test_fx_path_at_anchor_points``).
M5_ANCHOR_VALUES: Final[tuple[float, float, float]] = (4200.0, 3800.0, 4200.0)

#: Pin BRACKET-M5 — tolerance for the path-reconstruction check.
M5_RECONSTRUCTION_ATOL: Final[float] = 1e-9

#: Pin §5.2 — closed tier-mix keys for the saas-builder cohort.
SAAS_TIER_IDS: Final[tuple[str, str, str]] = ("pro", "max_5x", "max_20x")

#: Tier-mix sum tolerance.
TIER_MIX_SUM_ATOL: Final[float] = 1e-9

#: Audit-block sha256 hex regex.
_AUDIT_BLOCK_RE: Final[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}")


# ─── Type aliases ─────────────────────────────────────────────────────────────

#: Tier identifier; closed in `SAAS_TIER_IDS`.
TierID: TypeAlias = Literal["pro", "max_5x", "max_20x"]

#: Verdict alphabet — verbatim spec §10 line 520 (RC-BLOCK-2 v0.2 fix).
VerdictLabel: TypeAlias = Literal[
    "PASS", "WEAK", "MARGINAL", "FAIL", "INDISTINGUISHABLE"
]

#: 1-D float array.
FloatArray: TypeAlias = NDArray[np.float64]


# ─── Value types ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class T2CostParams:
    """T2 (metered-overage) cost-formula parameters (spec §5.1 (T2), §5.2).

    Symbol map (spec §5.1):

    - ``p_sub_bar`` ↔ $\\bar p_\\text{sub}$ subscription cost (USD/mo);
    - ``kappa`` ↔ subscription token cap κ (tokens/mo);
    - ``beta`` ↔ softplus β (1/tok), the *fitted* tightness from M2-fit;
    - ``p_t`` ↔ blended per-token price (USD/MTok) from
      ``simulations.modules.pricing.BlendedPriceFn`` — reduced to a
      scalar at gate time;
    - ``tier_mix`` ↔ Categorical weight per tier (sums to 1 within
      ``TIER_MIX_SUM_ATOL``).

    Validation contract:

    - ``p_sub_bar > 0``;
    - ``kappa > 0``;
    - ``beta > 0`` (tightness check is delegated to
      ``simulations.modules.regularizers.SoftplusRegularizer``;
      construction of this Value type does NOT re-run quad);
    - ``p_t > 0`` (USD/MTok);
    - ``tier_mix`` keys ⊆ ``SAAS_TIER_IDS``; values in ``[0, 1]``;
      sum ≈ 1 within ``TIER_MIX_SUM_ATOL``.
    """

    p_sub_bar: float
    kappa: float
    beta: float
    p_t: float
    tier_mix: Mapping[str, float]

    def __post_init__(self) -> None:
        for name, val in (
            ("p_sub_bar", self.p_sub_bar),
            ("kappa", self.kappa),
            ("beta", self.beta),
            ("p_t", self.p_t),
        ):
            if not math.isfinite(val):
                raise ValueError(f"T2CostParams.{name} = {val} must be finite")
            if val <= 0.0:
                raise ValueError(f"T2CostParams.{name} = {val} must be > 0")
        if not isinstance(self.tier_mix, MappingABC):
            raise TypeError("T2CostParams.tier_mix must be a Mapping")
        if not self.tier_mix:
            raise ValueError("T2CostParams.tier_mix must be non-empty")
        for k, v in self.tier_mix.items():
            if k not in SAAS_TIER_IDS:
                raise ValueError(
                    f"T2CostParams.tier_mix key {k!r} not in {SAAS_TIER_IDS}"
                )
            if not math.isfinite(v) or not (0.0 <= v <= 1.0):
                raise ValueError(
                    f"T2CostParams.tier_mix[{k!r}] = {v} must lie in [0, 1]"
                )
        weight_sum = sum(self.tier_mix.values())
        if not math.isclose(weight_sum, 1.0, abs_tol=TIER_MIX_SUM_ATOL):
            raise ValueError(
                f"T2CostParams.tier_mix sum = {weight_sum}"
                f" must equal 1 within {TIER_MIX_SUM_ATOL}"
            )


@dataclass(frozen=True)
class BracketPoint:
    """One spec §5.2 parameter bracket point on the M5 FX path.

    A BracketPoint pairs a ``T2CostParams`` (which fixes p̄_sub, κ, β, p_t,
    tier-mix) with the M5 ``FXPathParams`` (TRM-pinned ``X̄/Ȳ``,
    ``ε ∈ (0, 1)``, ``ω > 0``) and the realized-variance horizon ``T``.

    Pin BRACKET-M5 (RC-BLOCK-1 v0.2 semantics; cross-references shipped
    ``simulations/tests/test_modules.py:185,194``): construction
    re-evaluates the M5 path at ``t ∈ {0, π/2, π}``. With ``ε = 0.1`` and
    ``X̄/Ȳ = 4000`` the path is exactly ``(4200, 3800, 4200)``. For
    arbitrary ``(ε, X̄/Ȳ)`` the validity check is the closed-form
    pointwise reconstruction:

        (X/Y)_t = (1 + ε · (cos²(ω t) - ½)) · X̄/Ȳ

    which the BracketGrid optionally checks; this Value-type ONLY
    validates that the parameters are individually well-formed (delegating
    M5 reconstruction to ``BracketGrid.__post_init__`` per RC-BLOCK-1 v0.2
    fix to keep the path-reconstruction at *grid construction*, where the
    canonical anchor values ``(4200, 3800, 4200)`` are required to
    materialize at least once).

    Validation contract:

    - ``cost_params``: a ``T2CostParams`` (its own validation runs).
    - ``fx_params``: an ``FXPathParams`` (its own validation runs).
    - ``horizon_T``: int ≥ 1 (PRIMITIVES (7) divisor).
    """

    cost_params: T2CostParams
    fx_params: FXPathParams
    horizon_T: int

    def __post_init__(self) -> None:
        if self.horizon_T < 1:
            raise ValueError(
                f"BracketPoint.horizon_T = {self.horizon_T} must be ≥ 1"
            )


@dataclass(frozen=True)
class BracketGrid:
    """Immutable tuple of ``BracketPoint`` validated against Pin BRACKET-M5.

    Pin BRACKET-M5 (RC-BLOCK-1 v0.2 fix): construction asserts that
    *at least one* BracketPoint reconstructs the canonical anchor values
    ``(4200, 3800, 4200)`` at ``t ∈ {0, π/2, π}`` within
    ``M5_RECONSTRUCTION_ATOL``. This is the path-reconstruction check
    that pins the M5 single-mean / three-time-point semantics. Failure
    raises ``FXPathReconstructionError``.

    Rationale: the §5.2 parameter brackets sweep over (ε, ω, tier-mix
    realisations); they do NOT sweep over ``X̄/Ȳ`` (the TRM-pinned mean
    is a sha-pinned scalar per spec §3 lines 133–135). Requiring at
    least one canonical-anchor BracketPoint per grid is the value-type-
    level guard against silent drift away from the M5 anchor.
    """

    points: tuple[BracketPoint, ...]

    def __post_init__(self) -> None:
        if len(self.points) < 1:
            raise ValueError("BracketGrid.points must be non-empty")
        anchor_recovered = any(
            _reconstructs_m5_anchors(p.fx_params) for p in self.points
        )
        if not anchor_recovered:
            raise FXPathReconstructionError(
                "BracketGrid: no BracketPoint recovers the M5 anchor values"
                f" {M5_ANCHOR_VALUES} at t ∈ {M5_ANCHOR_TIMES}"
                f" within atol={M5_RECONSTRUCTION_ATOL}; cross-reference"
                " simulations/tests/test_modules.py:185,194"
            )


@dataclass(frozen=True)
class SignVerdict:
    """Per-bracket-point sign-certification record (Pin Δ-cohort).

    Records the posterior-predictive credible-interval bound used by the
    gate to certify ``Δ^(a_s) < 0``: when ``delta_upper_bound_95 < 0``
    strictly, the bracket point passes; otherwise ``sign_strictly_negative
    == False`` and the gate emits FAIL.

    Validation contract:

    - ``delta_median`` finite;
    - ``delta_lower_bound_95`` ≤ ``delta_median`` ≤ ``delta_upper_bound_95``;
    - ``sign_strictly_negative`` is True iff ``delta_upper_bound_95 < 0``;
    - ``audit_block`` is a 64-char lowercase sha256 hex string (or empty
      for in-memory test verdicts; the IO Boundary class fills it in
      before persistence).
    - ``bracket_index`` ≥ 0.
    """

    bracket_index: int
    delta_median: float
    delta_lower_bound_95: float
    delta_upper_bound_95: float
    sign_strictly_negative: bool
    audit_block: str = ""

    def __post_init__(self) -> None:
        if self.bracket_index < 0:
            raise ValueError(
                f"SignVerdict.bracket_index = {self.bracket_index} must be ≥ 0"
            )
        for name, val in (
            ("delta_median", self.delta_median),
            ("delta_lower_bound_95", self.delta_lower_bound_95),
            ("delta_upper_bound_95", self.delta_upper_bound_95),
        ):
            if not math.isfinite(val):
                raise ValueError(f"SignVerdict.{name} = {val} must be finite")
        if not (
            self.delta_lower_bound_95
            <= self.delta_median
            <= self.delta_upper_bound_95
        ):
            raise ValueError(
                "SignVerdict: must satisfy delta_lower_bound_95 ≤ delta_median"
                " ≤ delta_upper_bound_95;"
                f" got ({self.delta_lower_bound_95},"
                f" {self.delta_median}, {self.delta_upper_bound_95})"
            )
        # The boolean is a derived field; require consistency with the bound.
        derived = self.delta_upper_bound_95 < 0.0
        if derived != self.sign_strictly_negative:
            raise ValueError(
                "SignVerdict.sign_strictly_negative must equal"
                " (delta_upper_bound_95 < 0);"
                f" got flag={self.sign_strictly_negative},"
                f" upper_bound={self.delta_upper_bound_95}"
            )
        if self.audit_block != "" and not _AUDIT_BLOCK_RE.fullmatch(
            self.audit_block
        ):
            raise ValueError(
                "SignVerdict.audit_block must be empty or 64-char lowercase"
                f" sha256 hex; got {self.audit_block!r}"
            )


@dataclass(frozen=True)
class CohortGateVerdict:
    """COHORT-2 gate verdict — spec §10 artifact contract.

    Verdict alphabet (verbatim spec §10 line 520; RC-BLOCK-2 v0.2 fix):
    ``PASS|WEAK|MARGINAL|FAIL|INDISTINGUISHABLE``.

    HALT is a foreground/harness action — NOT a verdict value emitted to
    ``gate_verdict.json``. Whenever the gate would fire HALT, the
    foreground writes a disposition memo per
    ``feedback_pathological_halt_anti_fishing_checkpoint`` and the
    artifact records the most-informative non-HALT verdict (``FAIL``
    when any sign violation occurred).

    Validation contract:

    - ``sub_task == "COHORT-2"`` (Literal);
    - ``verdict`` ∈ closed alphabet;
    - ``n_bracket_points`` ≥ 1;
    - ``0 ≤ n_sign_violations ≤ n_bracket_points``;
    - ``len(evidence) == n_bracket_points`` and each
      ``SignVerdict.bracket_index`` is unique within ``[0, n_bracket_points)``;
    - ``audit_block`` is a 64-char lowercase sha256 hex string.
    - Logical: ``verdict == "PASS"`` iff ``n_sign_violations == 0`` AND
      every evidence row has ``sign_strictly_negative == True``.
    - Logical: ``verdict == "FAIL"`` iff ``n_sign_violations > 0``.
    """

    sub_task: Literal["COHORT-2"]
    verdict: VerdictLabel
    n_bracket_points: int
    n_sign_violations: int
    evidence: tuple[SignVerdict, ...]
    audit_block: str
    fetched_at_utc: str
    # PPC quantile-coverage diagnostics (MQ-FLAG-3 v0.2 fix). Empty mapping
    # means coverage was not computed (pre-gate path); a populated mapping
    # records empirical coverage at the {50, 90, 99}-pct τ_t quantiles.
    ppc_coverage: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.sub_task != "COHORT-2":
            raise ValueError(
                f"CohortGateVerdict.sub_task = {self.sub_task!r}"
                f" must equal 'COHORT-2'"
            )
        if self.verdict not in (
            "PASS", "WEAK", "MARGINAL", "FAIL", "INDISTINGUISHABLE",
        ):
            raise ValueError(
                f"CohortGateVerdict.verdict = {self.verdict!r}"
                " must be one of"
                " ('PASS','WEAK','MARGINAL','FAIL','INDISTINGUISHABLE')"
            )
        if self.n_bracket_points < 1:
            raise ValueError(
                f"CohortGateVerdict.n_bracket_points = {self.n_bracket_points}"
                f" must be ≥ 1"
            )
        if not (0 <= self.n_sign_violations <= self.n_bracket_points):
            raise ValueError(
                f"CohortGateVerdict.n_sign_violations = {self.n_sign_violations}"
                f" must lie in [0, {self.n_bracket_points}]"
            )
        if len(self.evidence) != self.n_bracket_points:
            raise ValueError(
                "CohortGateVerdict: len(evidence) ="
                f" {len(self.evidence)} must equal"
                f" n_bracket_points = {self.n_bracket_points}"
            )
        seen_indices: set[int] = set()
        violations_observed = 0
        all_strict = True
        for ev in self.evidence:
            if ev.bracket_index in seen_indices:
                raise ValueError(
                    f"CohortGateVerdict: duplicate bracket_index"
                    f" {ev.bracket_index} in evidence"
                )
            if not (0 <= ev.bracket_index < self.n_bracket_points):
                raise ValueError(
                    f"CohortGateVerdict: SignVerdict.bracket_index"
                    f" {ev.bracket_index} out of range"
                    f" [0, {self.n_bracket_points})"
                )
            seen_indices.add(ev.bracket_index)
            if not ev.sign_strictly_negative:
                violations_observed += 1
                all_strict = False
        if violations_observed != self.n_sign_violations:
            raise ValueError(
                "CohortGateVerdict: declared n_sign_violations"
                f" = {self.n_sign_violations}; counted from evidence"
                f" = {violations_observed}"
            )
        # Logical coupling: PASS ↔ no violations + all strictly negative.
        if self.verdict == "PASS" and not (
            self.n_sign_violations == 0 and all_strict
        ):
            raise ValueError(
                "CohortGateVerdict: verdict=PASS requires n_sign_violations=0"
                " and every evidence row sign_strictly_negative=True"
            )
        if self.verdict == "FAIL" and self.n_sign_violations == 0:
            raise ValueError(
                "CohortGateVerdict: verdict=FAIL requires n_sign_violations > 0"
            )
        if not _AUDIT_BLOCK_RE.fullmatch(self.audit_block):
            raise ValueError(
                "CohortGateVerdict.audit_block must be 64-char lowercase"
                f" sha256 hex; got {self.audit_block!r}"
            )
        if not self.fetched_at_utc:
            raise ValueError(
                "CohortGateVerdict.fetched_at_utc must be non-empty"
            )
        if not isinstance(self.ppc_coverage, MappingABC):
            raise TypeError(
                "CohortGateVerdict.ppc_coverage must be a Mapping"
            )
        for q, c in self.ppc_coverage.items():
            if q not in ("p50", "p90", "p99"):
                raise ValueError(
                    f"CohortGateVerdict.ppc_coverage key {q!r}"
                    " must be one of ('p50','p90','p99')"
                )
            if not math.isfinite(c) or not (0.0 <= c <= 1.0):
                raise ValueError(
                    f"CohortGateVerdict.ppc_coverage[{q!r}] = {c}"
                    " must lie in [0, 1]"
                )


# ─── Free-function accessors ──────────────────────────────────────────────────


def _reconstructs_m5_anchors(params: FXPathParams) -> bool:
    """Return True iff (X/Y)_t at ``M5_ANCHOR_TIMES`` equals ``M5_ANCHOR_VALUES``.

    Inlines PRIMITIVES.md (6) closed form:
        (X/Y)_t = (1 + ε · (cos²(ω t) - ½)) · X̄/Ȳ.

    Tolerance: ``M5_RECONSTRUCTION_ATOL = 1e-9`` (matches shipped
    ``simulations/tests/test_modules.py:194`` ``test_fx_path_at_anchor_points``).
    """
    eps = params.epsilon
    omega = params.omega
    mean = params.mean_x_over_y
    ts = np.array(M5_ANCHOR_TIMES, dtype=np.float64)
    cos_sq = np.cos(omega * ts) ** 2
    reconstructed = (1.0 + eps * (cos_sq - 0.5)) * mean
    expected = np.array(M5_ANCHOR_VALUES, dtype=np.float64)
    return bool(
        np.all(np.abs(reconstructed - expected) < M5_RECONSTRUCTION_ATOL)
    )


def n_evidence(verdict: CohortGateVerdict) -> int:
    """Return the number of SignVerdict rows in a CohortGateVerdict."""
    return len(verdict.evidence)


def all_signs_strict_negative(verdict: CohortGateVerdict) -> bool:
    """Return True iff every evidence row has sign_strictly_negative=True."""
    return all(ev.sign_strictly_negative for ev in verdict.evidence)


__all__ = [
    "M5_ANCHOR_TIMES",
    "M5_ANCHOR_VALUES",
    "M5_RECONSTRUCTION_ATOL",
    "SAAS_TIER_IDS",
    "TIER_MIX_SUM_ATOL",
    "BracketGrid",
    "BracketPoint",
    "CohortGateVerdict",
    "FloatArray",
    "SignVerdict",
    "T2CostParams",
    "TierID",
    "VerdictLabel",
    "all_signs_strict_negative",
    "n_evidence",
]
