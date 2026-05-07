"""Callable-tier unit tests — math pins M1, M2, M3, M5.

- M1: ``TruncParetoSampler`` refuses ``alpha < 1.5`` at construction time.
- M2: ``SoftplusRegularizer`` refuses non-tight ``beta`` (deviation ≥ 1e-3·κ).
- M3: ``BlendedPriceFn(Sonnet defaults)`` returns ≈ 7.149 USD/MTok plus
       cache-corner closed-form expectations (h=0 → no cache, h=1 → full cache).
- M5: ``FXPathGen`` evaluated at ``t ∈ {0, π/2, π}`` matches the closed-form
       triple ``(4200, 3800, 4200)``; ``epsilon_from_sigma_T`` round-trips
       within a documented numerical tolerance.

Phase 3.3 ``hypothesis-tests`` will EXTEND this file with property tests over
the Callable transforms (joint identifiability per CORRECTIONS-α §15.3).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from simulations.modules.fx_path import (
    FXPathGen,
    RealizedVarianceCalc,
    epsilon_from_sigma_T,
)
from simulations.modules.pricing import BlendedPriceFn
from simulations.modules.regularizers import SoftplusRegularizer
from simulations.modules.samplers import (
    NegBinSampler,
    TierMixCategorical,
    TruncParetoSampler,
)
from simulations.types.distributions import (
    NegBinParams,
    SoftplusParams,
    TruncParetoParams,
)
from simulations.types.fx import (
    BlendedPriceParams,
    FXPathParams,
    RealizedVarianceParams,
)
from simulations.types.tier import TIER_IDS, TierPrior


# ─── Pin M1 — TruncPareto α-floor ─────────────────────────────────────────────


class TestM1TruncParetoAlphaFloor:
    """Math pin M1 (spec §8(6))."""

    @pytest.mark.parametrize("alpha", [1.0, 1.4999, 1.0001, 0.5])
    def test_truncpareto_sampler_refuses_alpha_below_floor(self, alpha: float) -> None:
        """Sampler refuses α < 1.5 with a typed ValueError citing the spec."""
        params = TruncParetoParams(alpha=alpha, x_m=1.0, x_max=100.0)
        with pytest.raises(ValueError, match=r"§8\(6\)|alpha"):
            TruncParetoSampler(params=params)

    @pytest.mark.parametrize("alpha", [1.5, 2.0, 2.5])
    def test_truncpareto_sampler_accepts_alpha_at_or_above_floor(
        self, alpha: float
    ) -> None:
        """Sampler accepts α ≥ 1.5 (the spec §8(6) floor)."""
        params = TruncParetoParams(alpha=alpha, x_m=1.0, x_max=100.0)
        sampler = TruncParetoSampler(params=params)
        rng = np.random.default_rng(seed=42)
        samples = sampler(size=128, rng=rng)
        assert samples.shape == (128,)
        assert np.all(samples >= 1.0) and np.all(samples <= 100.0)

    def test_truncpareto_sampler_size_zero(self) -> None:
        """size=0 yields an empty array."""
        sampler = TruncParetoSampler(
            params=TruncParetoParams(alpha=2.0, x_m=1.0, x_max=10.0)
        )
        out = sampler(size=0, rng=np.random.default_rng(0))
        assert out.shape == (0,)

    def test_truncpareto_sampler_negative_size_raises(self) -> None:
        """size < 0 is rejected."""
        sampler = TruncParetoSampler(
            params=TruncParetoParams(alpha=2.0, x_m=1.0, x_max=10.0)
        )
        with pytest.raises(ValueError, match="size"):
            sampler(size=-1, rng=np.random.default_rng(0))


# ─── Pin M2 — Softplus β-tightness ────────────────────────────────────────────


class TestM2SoftplusTightness:
    """Math pin M2 (spec §5.1 (T2))."""

    def test_softplus_regularizer_refuses_loose_beta(self) -> None:
        """β=0.1, κ=1.0 fails the tightness floor by orders of magnitude."""
        with pytest.raises(ValueError, match="L¹|deviation"):
            SoftplusRegularizer(params=SoftplusParams(beta=0.1, kappa=1.0))

    def test_softplus_regularizer_accepts_tight_beta(self) -> None:
        """β=200, κ=1.0 clears the tightness floor."""
        reg = SoftplusRegularizer(params=SoftplusParams(beta=200.0, kappa=1.0))
        x = np.linspace(-2.0, 2.0, 16, dtype=np.float64)
        y = reg(x)
        # Softplus must be ≥ ReLU pointwise.
        relu = np.maximum(x, 0.0)
        assert np.all(y + 1e-9 >= relu)

    def test_softplus_call_shape_preservation(self) -> None:
        """Output shape equals input shape."""
        reg = SoftplusRegularizer(params=SoftplusParams(beta=200.0, kappa=1.0))
        x = np.zeros((3, 4), dtype=np.float64)
        assert reg(x).shape == (3, 4)


# ─── Pin M3 — Blended per-token price ─────────────────────────────────────────


class TestM3BlendedPrice:
    """Math pin M3 (spec §5.1)."""

    def test_blended_price_sonnet_default(self) -> None:
        """Sonnet defaults yield ≈ 7.149 USD/MTok within 1e-3."""
        params = BlendedPriceParams(
            w_in=0.539, w_out=0.461, h_cache=0.95, p_in=3.0, p_out=15.0
        )
        result = BlendedPriceFn(params=params)()
        # 0.539·3·0.145 + 0.461·15 = 0.234465 + 6.915 = 7.149465
        assert math.isclose(result, 7.149465, abs_tol=1e-3)

    def test_blended_price_no_cache_corner(self) -> None:
        """h_cache=0 collapses cache_factor to 1: p_t = w_in·p_in + w_out·p_out."""
        params = BlendedPriceParams(
            w_in=0.539, w_out=0.461, h_cache=0.0, p_in=3.0, p_out=15.0
        )
        expected = 0.539 * 3.0 + 0.461 * 15.0
        result = BlendedPriceFn(params=params)()
        assert math.isclose(result, expected, abs_tol=1e-12)

    def test_blended_price_full_cache_corner(self) -> None:
        """h_cache=1 collapses cache_factor to 0.10 (cached_input_discount)."""
        params = BlendedPriceParams(
            w_in=0.539, w_out=0.461, h_cache=1.0, p_in=3.0, p_out=15.0
        )
        expected = 0.539 * 3.0 * 0.10 + 0.461 * 15.0
        result = BlendedPriceFn(params=params)()
        assert math.isclose(result, expected, abs_tol=1e-12)

    @pytest.mark.parametrize(
        ("p_in", "p_out", "label"),
        [(5.0, 25.0, "opus"), (1.0, 5.0, "haiku")],
    )
    def test_blended_price_other_tiers_positive(
        self, p_in: float, p_out: float, label: str
    ) -> None:
        """Opus and Haiku also evaluate to a positive blended price."""
        params = BlendedPriceParams(
            w_in=0.539, w_out=0.461, h_cache=0.95, p_in=p_in, p_out=p_out
        )
        result = BlendedPriceFn(params=params)()
        assert result > 0.0, f"tier={label} produced non-positive p_t"


# ─── Pin M5 — FX path closed form ─────────────────────────────────────────────


class TestM5FXPath:
    """Math pin M5 (PRIMITIVES.md (6) + (8))."""

    def test_fx_path_at_anchor_points(self) -> None:
        """t ∈ {0, π/2, π} yield (4200, 3800, 4200) within 1e-9.

        Closed form: cos²(0)=1 → 1.05·4000=4200; cos²(π/2)=0 → 0.95·4000=3800;
        cos²(π)=1 → 4200.
        """
        params = FXPathParams(mean_x_over_y=4000.0, epsilon=0.1, omega=1.0)
        gen = FXPathGen(params=params)
        ts = np.array([0.0, math.pi / 2.0, math.pi], dtype=np.float64)
        out = gen(ts)
        np.testing.assert_allclose(out, [4200.0, 3800.0, 4200.0], atol=1e-9)

    def test_fx_path_envelope_bounds(self) -> None:
        """Generated path stays inside mean·(1±ε/2)."""
        params = FXPathParams(mean_x_over_y=4000.0, epsilon=0.2, omega=2.5)
        gen = FXPathGen(params=params)
        ts = np.linspace(0.0, 10.0, 1024, dtype=np.float64)
        out = gen(ts)
        assert np.all(out >= 4000.0 * (1.0 - 0.1) - 1e-9)
        assert np.all(out <= 4000.0 * (1.0 + 0.1) + 1e-9)

    def test_realized_variance_proxy(self) -> None:
        """σ_T over a flat path equal to the mean is exactly zero."""
        rv = RealizedVarianceCalc(
            params=RealizedVarianceParams(horizon_T=100),
            mean_x_over_y=4000.0,
        )
        flat_path = np.full(100, 4000.0, dtype=np.float64)
        assert rv(flat_path) == 0.0

    def test_epsilon_from_sigma_T_inverts_within_tolerance(self) -> None:
        """Round-trip: given ε, compute σ_T over a long path, invert; recover ε.

        Note (per Task 2.4 brief): the round trip is approximate because σ_T
        from a finite path samples the cos² envelope rather than its true
        mean-square deviation. The closed form gives
        ``σ_T(true) = ε² · mean² / 8`` (cos² has variance 1/8 about its mean
        of 1/2). With a long t-grid spanning many periods the empirical σ_T
        converges to this. Tolerance 1e-3 (abs) holds for this regime.
        """
        mean = 4000.0
        true_eps = 0.1
        # Closed-form σ_T from PRIMITIVES (8) inverted: σ_T = ε² mean² / 8
        sigma_T_closed = (true_eps ** 2) * (mean ** 2) / 8.0
        recovered = epsilon_from_sigma_T(sigma_T_closed, mean)
        assert math.isclose(recovered, true_eps, abs_tol=1e-9)

    def test_epsilon_from_sigma_T_path_round_trip_loose(self) -> None:
        """Path-derived round trip clears 1e-2 tolerance over many cycles.

        Document why: σ_T is mean-of-squared-deviation over a discrete path
        of length T+1, so it carries grid-induced bias of order 1/T. We use
        ω=1, T=4096 spanning ~650 cycles to wash that out; tolerance 1e-2
        is generous and holds reliably.
        """
        mean = 4000.0
        true_eps = 0.1
        params = FXPathParams(mean_x_over_y=mean, epsilon=true_eps, omega=1.0)
        gen = FXPathGen(params=params)
        ts = np.linspace(0.0, 4096.0, 4096, dtype=np.float64)
        path = gen(ts)
        sigma_T = RealizedVarianceCalc(
            params=RealizedVarianceParams(horizon_T=ts.size),
            mean_x_over_y=mean,
        )(path)
        recovered = epsilon_from_sigma_T(sigma_T, mean)
        assert math.isclose(recovered, true_eps, abs_tol=1e-2)

    def test_epsilon_from_sigma_T_rejects_negative_sigma(self) -> None:
        """sigma_T must be ≥ 0."""
        with pytest.raises(ValueError, match="sigma_T"):
            epsilon_from_sigma_T(-1.0, 4000.0)

    def test_epsilon_from_sigma_T_rejects_bad_mean(self) -> None:
        """mean_x_over_y must be > 0."""
        with pytest.raises(ValueError, match="mean_x_over_y"):
            epsilon_from_sigma_T(1.0, 0.0)


# ─── Other Callable tier sanity ───────────────────────────────────────────────


class TestNegBinSampler:
    def test_negbin_sampler_returns_int64(self) -> None:
        """NegBinSampler returns int64 non-negative array."""
        sampler = NegBinSampler(params=NegBinParams(r=4.0, p=0.5))
        out = sampler(size=64, rng=np.random.default_rng(0))
        assert out.dtype == np.int64
        assert np.all(out >= 0)

    def test_negbin_sampler_negative_size_raises(self) -> None:
        """size < 0 rejected."""
        sampler = NegBinSampler(params=NegBinParams(r=4.0, p=0.5))
        with pytest.raises(ValueError, match="size"):
            sampler(size=-1, rng=np.random.default_rng(0))


class TestTierMixCategorical:
    def test_tier_mix_returns_admissible_ids(self) -> None:
        """TierMixCategorical returns only members of TIER_IDS."""
        sampler = TierMixCategorical(prior=TierPrior())
        out = sampler(size=128, rng=np.random.default_rng(0))
        assert set(out.tolist()).issubset(set(TIER_IDS))

    def test_tier_mix_negative_size_raises(self) -> None:
        """size < 0 rejected."""
        sampler = TierMixCategorical(prior=TierPrior())
        with pytest.raises(ValueError, match="size"):
            sampler(size=-1, rng=np.random.default_rng(0))
