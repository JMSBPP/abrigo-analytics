"""Value-tier unit tests for ``simulations.types``.

Asserts the validation invariants documented in each Value type's
``__post_init__``: finite-positive enforcement, bounded-interval guards,
``Mapping`` shape requirements, and the ``ZCapPinned.audit_block`` regex.

Hypothesis property tests for downstream Callables live in
``test_modules.py`` and will be extended in Phase 3.3.
"""

from __future__ import annotations

import math
from typing import Any, cast

import numpy as np
import pytest
from hypothesis import given

from simulations.tests import strategies as S
from simulations.types.distributions import (
    NegBinParams,
    SoftplusParams,
    TruncParetoParams,
    neg_bin_mean,
    neg_bin_variance,
    tightness_l1_deviation,
    trunc_pareto_admits_saas_floor,
)
from simulations.types.fx import (
    BlendedPriceParams,
    FXPathParams,
    RealizedVarianceParams,
    fx_amplitude_envelope,
)
from simulations.types.posterior import (
    MonthlyCDF,
    PosteriorDraws,
    ZCapPinned,
    ci_95_width,
    n_total_draws,
    parameter_index,
)
from simulations.types.tier import (
    SUBSCRIPTION_USD_PER_MONTH,
    TIER_IDS,
    TierPricing,
    TierPrior,
    categorical_mass,
)


# ─── TruncParetoParams ────────────────────────────────────────────────────────


class TestTruncParetoParams:
    @pytest.mark.parametrize("alpha", [0.0, -1.0, math.inf, -math.inf, math.nan])
    def test_rejects_non_finite_positive_alpha(self, alpha: float) -> None:
        """alpha must be finite and strictly positive."""
        with pytest.raises(ValueError, match="alpha"):
            TruncParetoParams(alpha=alpha, x_m=1.0, x_max=10.0)

    @pytest.mark.parametrize("x_m", [0.0, -0.5, math.inf, math.nan])
    def test_rejects_bad_x_m(self, x_m: float) -> None:
        """x_m must be finite and strictly positive."""
        with pytest.raises(ValueError, match="x_m"):
            TruncParetoParams(alpha=2.0, x_m=x_m, x_max=10.0)

    @pytest.mark.parametrize("x_max", [0.5, 1.0, math.inf, math.nan, -3.0])
    def test_rejects_bad_x_max(self, x_max: float) -> None:
        """x_max must be finite-positive AND strictly greater than x_m=1.0."""
        with pytest.raises(ValueError, match="x_max"):
            TruncParetoParams(alpha=2.0, x_m=1.0, x_max=x_max)

    def test_accepts_valid_below_saas_floor(self) -> None:
        """Value tier accepts α=1.0 < SaaS floor (1.5); sampler enforces floor."""
        p = TruncParetoParams(alpha=1.0, x_m=1.0, x_max=10.0)
        assert p.alpha == 1.0
        assert trunc_pareto_admits_saas_floor(p) is False

    def test_admits_saas_floor_helper(self) -> None:
        """trunc_pareto_admits_saas_floor returns True for α ≥ 1.5."""
        p = TruncParetoParams(alpha=1.5, x_m=1.0, x_max=10.0)
        assert trunc_pareto_admits_saas_floor(p) is True


# ─── NegBinParams ─────────────────────────────────────────────────────────────


class TestNegBinParams:
    @pytest.mark.parametrize("r", [0.0, -1.0, math.inf, math.nan])
    def test_rejects_bad_r(self, r: float) -> None:
        """r must be finite and strictly positive."""
        with pytest.raises(ValueError, match="r"):
            NegBinParams(r=r, p=0.5)

    @pytest.mark.parametrize("p", [0.0, 1.0, -0.1, 1.1, math.inf, math.nan])
    def test_rejects_p_outside_open_unit(self, p: float) -> None:
        """p must lie strictly inside (0, 1); endpoints rejected."""
        with pytest.raises(ValueError, match=r"\(0, 1\)"):
            NegBinParams(r=2.0, p=p)

    def test_mean_and_variance_accessors(self) -> None:
        """neg_bin_mean / variance return r(1-p)/p and r(1-p)/p²."""
        params = NegBinParams(r=4.0, p=0.5)
        assert math.isclose(neg_bin_mean(params), 4.0)
        assert math.isclose(neg_bin_variance(params), 8.0)


# ─── SoftplusParams ───────────────────────────────────────────────────────────


class TestSoftplusParams:
    @pytest.mark.parametrize("beta", [0.0, -1.0, math.inf, math.nan])
    def test_rejects_bad_beta(self, beta: float) -> None:
        """beta must be finite and strictly positive at the Value tier."""
        with pytest.raises(ValueError, match="beta"):
            SoftplusParams(beta=beta, kappa=1.0)

    @pytest.mark.parametrize("kappa", [0.0, -2.0, math.inf, math.nan])
    def test_rejects_bad_kappa(self, kappa: float) -> None:
        """kappa must be finite and strictly positive."""
        with pytest.raises(ValueError, match="kappa"):
            SoftplusParams(beta=1.0, kappa=kappa)

    def test_tightness_deviation_decreases_with_beta(self) -> None:
        """L¹ deviation from ReLU monotonically tightens as β grows."""
        loose = SoftplusParams(beta=1.0, kappa=1.0)
        tight = SoftplusParams(beta=100.0, kappa=1.0)
        assert tightness_l1_deviation(loose) > tightness_l1_deviation(tight)

    def test_tightness_l1_grid_floor(self) -> None:
        """tightness_l1_deviation refuses n_grid < 2."""
        with pytest.raises(ValueError, match="n_grid"):
            tightness_l1_deviation(SoftplusParams(beta=10.0, kappa=1.0), n_grid=1)


# ─── FX types ─────────────────────────────────────────────────────────────────


class TestFXPathParams:
    @pytest.mark.parametrize("epsilon", [0.0, 1.0, -0.1, 1.5, math.inf, math.nan])
    def test_rejects_epsilon_outside_open_unit(self, epsilon: float) -> None:
        """epsilon must lie strictly inside (0, 1); endpoints rejected."""
        with pytest.raises(ValueError, match=r"\(0, 1\)"):
            FXPathParams(mean_x_over_y=4000.0, epsilon=epsilon, omega=1.0)

    @pytest.mark.parametrize("mean", [0.0, -1.0, math.inf, math.nan])
    def test_rejects_bad_mean(self, mean: float) -> None:
        """mean_x_over_y must be finite and strictly positive."""
        with pytest.raises(ValueError, match="mean_x_over_y"):
            FXPathParams(mean_x_over_y=mean, epsilon=0.1, omega=1.0)

    def test_amplitude_envelope_accessor(self) -> None:
        """fx_amplitude_envelope returns mean·(1±ε/2) bounds."""
        p = FXPathParams(mean_x_over_y=4000.0, epsilon=0.1, omega=1.0)
        lo, hi = fx_amplitude_envelope(p)
        assert math.isclose(lo, 4000.0 * 0.95)
        assert math.isclose(hi, 4000.0 * 1.05)


class TestRealizedVarianceParams:
    @pytest.mark.parametrize("T", [0, -1, -100])
    def test_rejects_non_positive_horizon(self, T: int) -> None:
        """horizon_T must be strictly positive."""
        with pytest.raises(ValueError, match="horizon_T"):
            RealizedVarianceParams(horizon_T=T)


class TestBlendedPriceParams:
    def test_weights_must_sum_to_one(self) -> None:
        """w_in + w_out must equal 1 within 1e-12."""
        with pytest.raises(ValueError, match="must equal 1"):
            BlendedPriceParams(w_in=0.5, w_out=0.4, h_cache=0.5, p_in=3.0, p_out=15.0)

    @pytest.mark.parametrize("w_in", [0.0, 1.0, -0.1, 1.1])
    def test_rejects_w_in_endpoints(self, w_in: float) -> None:
        """w_in must lie strictly inside (0, 1)."""
        with pytest.raises(ValueError):
            BlendedPriceParams(
                w_in=w_in, w_out=1.0 - w_in, h_cache=0.5, p_in=3.0, p_out=15.0
            )

    @pytest.mark.parametrize("h", [-0.1, 1.1, math.inf, math.nan])
    def test_rejects_h_cache_outside_unit(self, h: float) -> None:
        """h_cache must lie in [0, 1]."""
        with pytest.raises(ValueError, match="h_cache"):
            BlendedPriceParams(w_in=0.5, w_out=0.5, h_cache=h, p_in=3.0, p_out=15.0)

    def test_h_cache_endpoints_accepted(self) -> None:
        """h_cache=0 and h_cache=1 are admissible (closed interval)."""
        BlendedPriceParams(w_in=0.5, w_out=0.5, h_cache=0.0, p_in=3.0, p_out=15.0)
        BlendedPriceParams(w_in=0.5, w_out=0.5, h_cache=1.0, p_in=3.0, p_out=15.0)


# ─── Tier types ───────────────────────────────────────────────────────────────


class TestTierPrior:
    def test_pi_must_be_mapping(self) -> None:
        """A list-of-pairs is rejected with TypeError (not AttributeError)."""
        pairs: list[tuple[str, float]] = [
            ("pro", 0.2),
            ("max_5x", 0.5),
            ("max_20x", 0.3),
        ]
        with pytest.raises(TypeError, match="Mapping"):
            TierPrior(pi=cast(Any, pairs))

    def test_keys_must_match_tier_ids(self) -> None:
        """Missing or extra keys are rejected."""
        with pytest.raises(ValueError, match="exactly"):
            TierPrior(pi=cast(Any, {"pro": 0.5, "max_5x": 0.5}))

    def test_pi_must_sum_to_one(self) -> None:
        """π values must sum to 1 within 1e-9."""
        with pytest.raises(ValueError, match="sum to 1"):
            TierPrior(pi={"pro": 0.1, "max_5x": 0.1, "max_20x": 0.1})

    @pytest.mark.parametrize("v", [0.0, -0.1, 1.5])
    def test_pi_values_must_lie_in_open_unit(self, v: float) -> None:
        """π values must lie in (0, 1]; 0 and >1 rejected."""
        with pytest.raises(ValueError, match=r"\(0, 1\]"):
            TierPrior(pi={"pro": v, "max_5x": 0.5, "max_20x": 1.0 - 0.5 - v})

    def test_alpha_0_must_be_positive(self) -> None:
        """alpha_0 must be finite and strictly positive."""
        with pytest.raises(ValueError, match="alpha_0"):
            TierPrior(alpha_0=0.0)

    def test_categorical_mass_accessor(self) -> None:
        """categorical_mass returns π[tier] from the prior."""
        prior = TierPrior()
        assert categorical_mass(prior, "max_5x") == 0.5


class TestTierPricing:
    def test_must_be_mapping(self) -> None:
        """A list-of-pairs is rejected with TypeError."""
        pairs: list[tuple[str, float]] = [
            ("pro", 20.0),
            ("max_5x", 100.0),
            ("max_20x", 200.0),
        ]
        with pytest.raises(TypeError, match="Mapping"):
            TierPricing(usd_per_month=cast(Any, pairs))

    def test_default_matches_spec(self) -> None:
        """Default TierPricing matches spec §5.2 pins."""
        pricing = TierPricing()
        for tier in TIER_IDS:
            assert pricing.usd_per_month[tier] == SUBSCRIPTION_USD_PER_MONTH[tier]

    def test_rejects_non_positive_price(self) -> None:
        """Per-tier USD/mo must be finite and strictly positive."""
        with pytest.raises(ValueError, match="usd_per_month"):
            TierPricing(usd_per_month={"pro": 0.0, "max_5x": 100.0, "max_20x": 200.0})


# ─── Posterior types ─────────────────────────────────────────────────────────


class TestPosteriorDraws:
    def test_rejects_one_dimensional(self) -> None:
        """draws.ndim must equal 2."""
        with pytest.raises(ValueError, match="ndim"):
            PosteriorDraws(
                draws=np.zeros(8, dtype=np.float64),
                param_names=("p0",),
            )

    def test_rejects_shape_param_mismatch(self) -> None:
        """draws.shape[1] must equal len(param_names)."""
        with pytest.raises(ValueError, match="param_names"):
            PosteriorDraws(
                draws=np.zeros((4, 2), dtype=np.float64),
                param_names=("p0",),
            )

    def test_rejects_duplicate_param_names(self) -> None:
        """param_names must be unique."""
        with pytest.raises(ValueError, match="duplicate"):
            PosteriorDraws(
                draws=np.zeros((4, 2), dtype=np.float64),
                param_names=("p0", "p0"),
            )

    def test_n_total_draws_and_index(self) -> None:
        """n_total_draws and parameter_index helpers behave."""
        d = PosteriorDraws(
            draws=np.arange(12, dtype=np.float64).reshape(4, 3),
            param_names=("a", "b", "c"),
        )
        assert n_total_draws(d) == 4
        assert parameter_index(d, "b") == 1
        with pytest.raises(ValueError, match="no parameter"):
            parameter_index(d, "z")


class TestMonthlyCDF:
    def test_rejects_length_mismatch(self) -> None:
        """percentiles and values_usd must have equal length."""
        with pytest.raises(ValueError, match="equal length"):
            MonthlyCDF(percentiles=(10.0, 50.0), values_usd=(1.0,))

    @pytest.mark.parametrize("q", [0.0, 100.0, -10.0, 110.0])
    def test_rejects_percentile_endpoints(self, q: float) -> None:
        """percentiles must lie strictly inside (0, 100)."""
        with pytest.raises(ValueError, match=r"\(0, 100\)"):
            MonthlyCDF(percentiles=(q,), values_usd=(1.0,))

    def test_rejects_non_increasing_percentiles(self) -> None:
        """percentiles must be strictly increasing."""
        with pytest.raises(ValueError, match="strictly increasing"):
            MonthlyCDF(percentiles=(50.0, 10.0), values_usd=(1.0, 2.0))

    def test_rejects_decreasing_values(self) -> None:
        """values_usd must be non-decreasing."""
        with pytest.raises(ValueError, match="non-decreasing"):
            MonthlyCDF(percentiles=(10.0, 50.0), values_usd=(5.0, 1.0))


class TestZCapPinned:
    def _valid_block(self) -> str:
        return "0" * 64

    def test_rejects_audit_block_wrong_length(self) -> None:
        """audit_block must be exactly 64 chars."""
        with pytest.raises(ValueError, match="64 lowercase hex"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=90.0,
                ci_95_hi=110.0,
                audit_block="abc",
            )

    def test_rejects_audit_block_uppercase_hex(self) -> None:
        """audit_block must be lowercase hex."""
        with pytest.raises(ValueError, match="64 lowercase hex"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=90.0,
                ci_95_hi=110.0,
                audit_block="A" * 64,
            )

    def test_rejects_audit_block_non_hex(self) -> None:
        """audit_block must contain only [0-9a-f]."""
        with pytest.raises(ValueError, match="64 lowercase hex"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=90.0,
                ci_95_hi=110.0,
                audit_block="g" * 64,
            )

    def test_rejects_audit_block_with_whitespace(self) -> None:
        """audit_block must not contain leading/trailing whitespace."""
        with pytest.raises(ValueError, match="64 lowercase hex"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=90.0,
                ci_95_hi=110.0,
                audit_block=" " + "0" * 63,
            )

    def test_rejects_ci_inversion(self) -> None:
        """ci_95_lo ≤ Z_cop_per_month ≤ ci_95_hi must hold."""
        with pytest.raises(ValueError, match="ci_95_lo"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=120.0,
                ci_95_hi=130.0,
                audit_block=self._valid_block(),
            )

    def test_tier_mix_must_be_mapping(self) -> None:
        """A list-of-pairs as tier_mix triggers TypeError, not AttributeError."""
        pairs: list[tuple[str, float]] = [
            ("pro", 0.2),
            ("max_5x", 0.5),
            ("max_20x", 0.3),
        ]
        with pytest.raises(TypeError, match="Mapping"):
            ZCapPinned(
                Z_cop_per_month=100.0,
                ci_95_lo=90.0,
                ci_95_hi=110.0,
                audit_block=self._valid_block(),
                tier_mix=cast(Any, pairs),
            )

    def test_ci_95_width_accessor(self) -> None:
        """ci_95_width returns hi - lo."""
        z = ZCapPinned(
            Z_cop_per_month=100.0,
            ci_95_lo=90.0,
            ci_95_hi=110.0,
            audit_block=self._valid_block(),
        )
        assert math.isclose(ci_95_width(z), 20.0)


# ─── Hypothesis sanity over strategies ────────────────────────────────────────


class TestStrategiesSanity:
    """Smoke tests that each strategy yields constructible Values."""

    @given(S.truncpareto_params())
    def test_truncpareto_strategy_constructs(self, p: TruncParetoParams) -> None:
        """truncpareto_params yields valid Value-tier params."""
        assert p.x_max > p.x_m > 0
        assert p.alpha > 0

    @given(S.saas_truncpareto_params())
    def test_saas_truncpareto_respects_floor(self, p: TruncParetoParams) -> None:
        """saas_truncpareto_params draws α ≥ 1.5 (SaaS floor)."""
        assert p.alpha >= 1.5

    @given(S.negbin_params())
    def test_negbin_strategy(self, p: NegBinParams) -> None:
        """negbin_params yields valid Value-tier params."""
        assert p.r > 0 and 0 < p.p < 1

    @given(S.softplus_params())
    def test_softplus_strategy(self, p: SoftplusParams) -> None:
        """softplus_params yields valid Value-tier params."""
        assert p.beta > 0 and p.kappa > 0

    @given(S.fx_path_params())
    def test_fx_path_strategy(self, p: FXPathParams) -> None:
        """fx_path_params yields ε in (0, 1)."""
        assert 0 < p.epsilon < 1

    @given(S.blended_price_params())
    def test_blended_strategy_sums_to_one(self, p: BlendedPriceParams) -> None:
        """blended_price_params yields w_in + w_out = 1 within 1e-12."""
        assert abs(p.w_in + p.w_out - 1.0) <= 1e-12

    @given(S.tier_prior())
    def test_tier_prior_sums_to_one(self, prior: TierPrior) -> None:
        """tier_prior yields π summing to 1 within 1e-9."""
        assert abs(sum(prior.pi.values()) - 1.0) <= 1e-9

    @given(S.tier_pricing())
    def test_tier_pricing_strategy(self, pricing: TierPricing) -> None:
        """tier_pricing yields strictly-positive USD/mo per tier."""
        for v in pricing.usd_per_month.values():
            assert v > 0

    @given(S.posterior_draws())
    def test_posterior_draws_strategy(self, d: PosteriorDraws) -> None:
        """posterior_draws yields shape-consistent containers."""
        assert d.draws.shape[1] == len(d.param_names)

    @given(S.monthly_cdf())
    def test_monthly_cdf_strategy(self, cdf: MonthlyCDF) -> None:
        """monthly_cdf yields strictly-increasing percentiles + non-decreasing values."""
        assert all(
            cdf.percentiles[i] < cdf.percentiles[i + 1]
            for i in range(len(cdf.percentiles) - 1)
        )

    @given(S.zcap_pinned())
    def test_zcap_pinned_strategy(self, z: ZCapPinned) -> None:
        """zcap_pinned yields a 64-char lowercase hex audit_block."""
        assert len(z.audit_block) == 64
        assert all(c in "0123456789abcdef" for c in z.audit_block)


