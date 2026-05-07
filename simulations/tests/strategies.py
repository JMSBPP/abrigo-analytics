"""Hypothesis input strategies — one per Value type in ``simulations.types``.

These strategies do **not** impose Callable-tier guards (e.g., the SaaS-builder
α ≥ 1.5 floor for ``TruncParetoSampler``). They generate the full Value-tier
admissible region so that the Callable's tier-rejection behavior can itself
be tested. Where helpful, narrowed strategies (e.g., ``saas_truncpareto_params``,
``tight_softplus_params``) are provided as separate composites.

Phase 3.3 ``hypothesis-tests`` skill will extend these with property tests
on the Callable transforms.
"""

from __future__ import annotations

from typing import Any

import hypothesis.strategies as st
import numpy as np

from simulations.types.distributions import (
    SAAS_TRUNC_PARETO_ALPHA_CEILING,
    SAAS_TRUNC_PARETO_ALPHA_FLOOR,
    NegBinParams,
    SoftplusParams,
    TruncParetoParams,
)
from simulations.types.fx import BlendedPriceParams, FXPathParams, RealizedVarianceParams
from simulations.types.posterior import MonthlyCDF, PosteriorDraws, ZCapPinned
from simulations.types.tier import (
    SUBSCRIPTION_USD_PER_MONTH,
    TIER_IDS,
    TierPricing,
    TierPrior,
)


# ─── Distribution-parameter strategies ────────────────────────────────────────


@st.composite
def truncpareto_params(
    draw: st.DrawFn,
    *,
    alpha_min: float = 0.5,
    alpha_max: float = 3.0,
) -> TruncParetoParams:
    """Draw ``TruncParetoParams`` over the **Value-tier** admissible region.

    The default range allows α below the SaaS-builder floor (1.5) so the
    Callable's M1 rejection behavior can be tested.
    """
    alpha = draw(st.floats(min_value=alpha_min, max_value=alpha_max,
                            allow_nan=False, allow_infinity=False, exclude_min=True))
    x_m = draw(st.floats(min_value=1e-3, max_value=1e3,
                         allow_nan=False, allow_infinity=False, exclude_min=True))
    # x_max strictly > x_m
    multiplier = draw(st.floats(min_value=1.001, max_value=100.0,
                                 allow_nan=False, allow_infinity=False))
    return TruncParetoParams(alpha=alpha, x_m=x_m, x_max=x_m * multiplier)


@st.composite
def saas_truncpareto_params(draw: st.DrawFn) -> TruncParetoParams:
    """Draw ``TruncParetoParams`` honoring the SaaS-builder α ≥ 1.5 floor."""
    return draw(
        truncpareto_params(
            alpha_min=SAAS_TRUNC_PARETO_ALPHA_FLOOR,
            alpha_max=SAAS_TRUNC_PARETO_ALPHA_CEILING,
        )
    )


@st.composite
def negbin_params(draw: st.DrawFn) -> NegBinParams:
    """Draw ``NegBinParams`` with ``r > 0`` and ``p ∈ (0, 1)``."""
    r = draw(st.floats(min_value=1e-3, max_value=1e3,
                       allow_nan=False, allow_infinity=False, exclude_min=True))
    p = draw(st.floats(min_value=1e-3, max_value=1.0 - 1e-3,
                       allow_nan=False, allow_infinity=False))
    return NegBinParams(r=r, p=p)


@st.composite
def softplus_params(draw: st.DrawFn) -> SoftplusParams:
    """Draw ``SoftplusParams`` over the Value-tier admissible region.

    May produce β values that fail the M2 tightness criterion (so the
    Callable's rejection behavior can be tested).
    """
    beta = draw(st.floats(min_value=1e-2, max_value=1e3,
                          allow_nan=False, allow_infinity=False, exclude_min=True))
    kappa = draw(st.floats(min_value=1e-2, max_value=1e3,
                           allow_nan=False, allow_infinity=False, exclude_min=True))
    return SoftplusParams(beta=beta, kappa=kappa)


@st.composite
def tight_softplus_params(draw: st.DrawFn) -> SoftplusParams:
    """Draw ``SoftplusParams`` whose β passes the M2 tightness criterion.

    Empirically, ``β · κ ≥ 50`` clears the ``deviation < 1e-3 · κ`` bar with
    healthy margin (Pareto floor argument in the regularizers docstring).
    Use a generous floor of ``β ≥ 200/κ`` so the criterion holds across the
    grid-numerical regime.
    """
    kappa = draw(st.floats(min_value=0.1, max_value=10.0,
                           allow_nan=False, allow_infinity=False))
    beta_floor = 200.0 / kappa
    beta = draw(st.floats(min_value=beta_floor, max_value=beta_floor * 10.0,
                          allow_nan=False, allow_infinity=False))
    return SoftplusParams(beta=beta, kappa=kappa)


# ─── Tier strategies ──────────────────────────────────────────────────────────


@st.composite
def tier_prior(draw: st.DrawFn) -> TierPrior:
    """Draw a ``TierPrior`` whose π sums to 1 within ``1e-9``."""
    weights = draw(
        st.tuples(
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
        )
    )
    total = sum(weights)
    pi = {tier: w / total for tier, w in zip(TIER_IDS, weights)}
    # Patch any rounding drift onto the last entry to clear the 1e-9 sum guard.
    drift = 1.0 - sum(pi.values())
    pi[TIER_IDS[-1]] += drift
    alpha_0 = draw(st.floats(min_value=1.0, max_value=100.0, allow_nan=False))
    return TierPrior(pi=dict(pi), alpha_0=alpha_0)


@st.composite
def tier_pricing(draw: st.DrawFn) -> TierPricing:
    """Draw ``TierPricing`` near (but not equal to) the spec §5.2 pins."""
    perturbations = draw(
        st.tuples(
            st.floats(min_value=0.5, max_value=2.0, allow_nan=False),
            st.floats(min_value=0.5, max_value=2.0, allow_nan=False),
            st.floats(min_value=0.5, max_value=2.0, allow_nan=False),
        )
    )
    pricing = {
        tier: SUBSCRIPTION_USD_PER_MONTH[tier] * pert
        for tier, pert in zip(TIER_IDS, perturbations)
    }
    return TierPricing(usd_per_month=pricing)


# ─── FX strategies ────────────────────────────────────────────────────────────


@st.composite
def fx_path_params(draw: st.DrawFn) -> FXPathParams:
    """Draw ``FXPathParams`` with ε ∈ (0, 1) per spec §3 / PRIMITIVES (6)."""
    mean_x_over_y = draw(st.floats(min_value=1.0, max_value=1e6,
                                    allow_nan=False, allow_infinity=False,
                                    exclude_min=True))
    epsilon = draw(st.floats(min_value=1e-3, max_value=1.0 - 1e-3,
                              allow_nan=False, allow_infinity=False))
    omega = draw(st.floats(min_value=1e-3, max_value=10.0,
                            allow_nan=False, allow_infinity=False, exclude_min=True))
    return FXPathParams(mean_x_over_y=mean_x_over_y, epsilon=epsilon, omega=omega)


@st.composite
def realized_variance_params(draw: st.DrawFn) -> RealizedVarianceParams:
    """Draw ``RealizedVarianceParams`` with ``horizon_T > 0``."""
    horizon_T = draw(st.integers(min_value=1, max_value=10_000))
    return RealizedVarianceParams(horizon_T=horizon_T)


@st.composite
def blended_price_params(draw: st.DrawFn) -> BlendedPriceParams:
    """Draw ``BlendedPriceParams`` with ``w_in + w_out = 1`` exactly."""
    w_in = draw(st.floats(min_value=0.05, max_value=0.95,
                          allow_nan=False, allow_infinity=False))
    w_out = 1.0 - w_in
    h_cache = draw(st.floats(min_value=0.0, max_value=1.0,
                              allow_nan=False, allow_infinity=False))
    p_in = draw(st.floats(min_value=0.1, max_value=100.0,
                           allow_nan=False, allow_infinity=False))
    p_out = draw(st.floats(min_value=0.1, max_value=200.0,
                            allow_nan=False, allow_infinity=False))
    return BlendedPriceParams(
        w_in=w_in, w_out=w_out, h_cache=h_cache, p_in=p_in, p_out=p_out
    )


# ─── Posterior / emission strategies ──────────────────────────────────────────


@st.composite
def posterior_draws(draw: st.DrawFn) -> PosteriorDraws:
    """Draw a small ``PosteriorDraws`` with shape-consistent metadata."""
    n_params = draw(st.integers(min_value=1, max_value=4))
    n_rows = draw(st.integers(min_value=1, max_value=32))
    seed = draw(st.integers(min_value=0, max_value=2**31 - 1))
    rng = np.random.default_rng(seed)
    arr = rng.normal(size=(n_rows, n_params)).astype(np.float64)
    names = tuple(f"p{i}" for i in range(n_params))
    return PosteriorDraws(draws=arr, param_names=names)


@st.composite
def monthly_cdf(draw: st.DrawFn) -> MonthlyCDF:
    """Draw a four-percentile ``MonthlyCDF`` (p10/p50/p90/p99)."""
    base = draw(st.floats(min_value=10.0, max_value=10_000.0, allow_nan=False))
    # All multipliers ≥ 1 so the resulting CDF values are non-decreasing.
    spreads = draw(
        st.tuples(
            st.floats(min_value=1.0, max_value=2.0, allow_nan=False),
            st.floats(min_value=1.0, max_value=5.0, allow_nan=False),
            st.floats(min_value=1.0, max_value=10.0, allow_nan=False),
        )
    )
    p10 = base
    p50 = base * spreads[0]
    p90 = p50 * spreads[1]
    p99 = p90 * spreads[2]
    return MonthlyCDF(
        percentiles=(10.0, 50.0, 90.0, 99.0),
        values_usd=(p10, p50, p90, p99),
    )


@st.composite
def zcap_pinned(draw: st.DrawFn) -> ZCapPinned:
    """Draw a ``ZCapPinned`` Value with valid sha256 and tier_mix."""
    z = draw(st.floats(min_value=10.0, max_value=1e6, allow_nan=False))
    half_width = draw(st.floats(min_value=0.01 * z, max_value=0.5 * z, allow_nan=False))
    audit_int = draw(st.integers(min_value=0, max_value=2**256 - 1))
    audit_block = f"{audit_int:064x}"
    # Reuse the tier_prior strategy's π construction to satisfy sum-to-one.
    weights: tuple[Any, ...] = draw(
        st.tuples(
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
            st.floats(min_value=0.05, max_value=0.95, allow_nan=False),
        )
    )
    total = sum(weights)
    tier_mix = {tier: w / total for tier, w in zip(TIER_IDS, weights)}
    drift = 1.0 - sum(tier_mix.values())
    tier_mix[TIER_IDS[-1]] += drift
    return ZCapPinned(
        Z_cop_per_month=z,
        ci_95_lo=z - half_width,
        ci_95_hi=z + half_width,
        audit_block=audit_block,
        tier_mix=dict(tier_mix),
    )


__all__ = [
    "truncpareto_params",
    "saas_truncpareto_params",
    "negbin_params",
    "softplus_params",
    "tight_softplus_params",
    "tier_prior",
    "tier_pricing",
    "fx_path_params",
    "realized_variance_params",
    "blended_price_params",
    "posterior_draws",
    "monthly_cdf",
    "zcap_pinned",
]
