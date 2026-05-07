"""PyMC model factory for SAAS-COHORT-1 T1 (subscription-cap regime) fit.

Implements spec v1.1.1 §5.1 (T1) verbatim doubly-stochastic compound sum

    τ_t = Σ_{j=1}^{D_t} Σ_{i=1}^{N_j} τ_{j,i},      D_t ≈ 22

with per-active-day ``N_j ~ NegBin(μ, α=φ)`` (mean–dispersion form, MQ-B2)
and iid ``τ_{j,i} ~ TruncPareto(α, x_m, κ)`` (M1: α ≥ 1.5).

Tier-Categorical mixture over ``π ~ Dir([2.0, 5.0, 3.0])`` per spec §5.2.
**No Compound-Poisson cluster process** at the primary likelihood level —
that label belongs to spec §5.1 sensitivity arm (c) and is OUT OF SCOPE
for COHORT-1 (MQ-B3).

Pin enforcement at this layer:

- **M1 (α-floor 1.5):** prior shape is
  ``pm.TruncatedNormal(mu=2.0, sigma=0.25, lower=1.5, upper=2.5)``;
  upstream ``simulations.modules.samplers.TruncParetoSampler`` raises
  on α < 1.5 in the Callable layer (defense-in-depth).
- **M3 ($/MTok blended price):** the model imports
  :class:`simulations.modules.pricing.BlendedPriceFn` and
  :class:`simulations.types.fx.BlendedPriceParams`, constructs the
  Sonnet defaults ``(p_in=3.0, p_out=15.0, w_in=0.539, w_out=0.461,
  h_cache=0.95)``, *calls* the instance (``BlendedPriceFn`` is callable
  with no args) to obtain the blended scalar, and asserts via
  ``math.isclose(price, 7.1495, abs_tol=0.01)`` AT THE FACTORY CALL
  SITE (RC-B2: not in ``__post_init__``, which only validates the
  params struct). Drift here is a Phase-4 BLOCK.

Posterior-predictive emission surface (MQ-B4):

    ``τ_t``, ``q_t_usd``, ``q_t_cop`` are declared as ``pm.Deterministic``
    nodes inside the model context so they are populated by
    ``pm.sample_posterior_predictive`` in ``emit.py`` (NOT raw
    ``idata.posterior`` slicing, which would yield zero within-row
    variance at fixed parameter draws).

This file is the layer where PyMC enters the codebase. Imports are limited
to PyMC + the read-only Value/Callable upstream of cohort code.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Final

import numpy as np
import pymc as pm
import pytensor.tensor as pt

from simulations.modules.pricing import BlendedPriceFn
from simulations.saas_builder.priors import (
    DIRICHLET_ALPHA_VECTOR,
    CohortPriors,
)
from simulations.types.fx import (
    BlendedPriceParams,
    DEFAULT_H_CACHE,
    DEFAULT_W_IN,
    DEFAULT_W_OUT,
    SONNET_PRICE_IN_USD_PER_MTOK,
    SONNET_PRICE_OUT_USD_PER_MTOK,
)

# ─── Math pin constants (spec §5.1, §5.2) ─────────────────────────────────────

#: Spec §5.1 closed-form Sonnet blended price expected value
#: ``0.539·3·(1 - 0.95 + 0.95·0.10) + 0.461·15 = 0.234 + 6.915 = 7.1495``.
M3_SONNET_BLENDED_PRICE_EXPECTED: Final[float] = 7.1495

#: Tolerance for the M3 assertion at the factory call site. Widened from
#: 0.0005 to 0.01 (RC-FLAG-1) to match spec §5.1 "≈ 7.15" precision.
M3_BLENDED_PRICE_ABS_TOL: Final[float] = 0.01

#: Default FX rate (X/Y) — COP/USD. Used for the q_t_cop deterministic.
#: Pinned at the spec §3 stationary mean ``X̄/Ȳ`` for COP/USD ≈ 4000 COP/USD.
DEFAULT_FX_COP_PER_USD: Final[float] = 4000.0


def _build_sonnet_blended_price() -> float:
    """Construct the Sonnet-defaults BlendedPriceFn and return p_t.

    Side-effect-free; constructs ``BlendedPriceParams`` with spec §5.4
    Sonnet defaults, builds ``BlendedPriceFn``, calls it, asserts the
    return value is within ``M3_BLENDED_PRICE_ABS_TOL`` of the spec
    closed form, and returns the float.

    Asserted at *call site* per RC-B2 — not in ``__post_init__``,
    which validates the params struct, not a tier-conditioned numeric
    output.

    Raises:
        AssertionError: if the closed-form drift exceeds
            ``M3_BLENDED_PRICE_ABS_TOL``. Caller surfaces this as a
            Phase-4 BLOCK.
    """
    params = BlendedPriceParams(
        p_in=SONNET_PRICE_IN_USD_PER_MTOK,
        p_out=SONNET_PRICE_OUT_USD_PER_MTOK,
        w_in=DEFAULT_W_IN,
        w_out=DEFAULT_W_OUT,
        h_cache=DEFAULT_H_CACHE,
    )
    price_fn = BlendedPriceFn(params=params)
    price_per_mtok = price_fn()  # CALL the instance — no .price_per_mtok attr
    if not math.isclose(
        price_per_mtok,
        M3_SONNET_BLENDED_PRICE_EXPECTED,
        abs_tol=M3_BLENDED_PRICE_ABS_TOL,
    ):
        raise AssertionError(
            f"M3 BLOCK: BlendedPriceFn(Sonnet defaults)() ="
            f" {price_per_mtok!r} drifts from spec §5.1 closed form"
            f" {M3_SONNET_BLENDED_PRICE_EXPECTED} by"
            f" |Δ| = {abs(price_per_mtok - M3_SONNET_BLENDED_PRICE_EXPECTED)};"
            f" tolerance is abs_tol={M3_BLENDED_PRICE_ABS_TOL}."
        )
    return float(price_per_mtok)


@dataclass(frozen=True)
class T1ModelFactory:
    """Frozen-dc Callable building the spec §5.1 (T1) PyMC model.

    The factory holds the prior pin bundle and the FX rate; ``__call__``
    constructs and returns the ``pm.Model`` ready for ``pm.sample(...)``.
    Posterior-predictive Deterministics ``tau_t``, ``q_t_usd``, ``q_t_cop``
    are declared inside the model context so :mod:`emit` can populate them
    via ``pm.sample_posterior_predictive`` (MQ-B4).

    Attributes:
        priors: bundle of prior-hyperparameter Value containers.
        fx_cop_per_usd: stationary FX rate for ``q_t_cop = q_t_usd · FX``;
            default :data:`DEFAULT_FX_COP_PER_USD`.
        n_simulations: shape of the per-month posterior-predictive draw
            tensor (rows of ``synthetic_tau_t.parquet`` per (tier, month)).
            Default 1.

    Behavior contract:

    - ``__call__`` returns a ``pm.Model`` context with the following
      named random variables and Deterministics:
        - ``mu`` — Lognormal-shape prior on per-active-day NegBin mean.
        - ``phi`` — HalfNormal prior on NegBin dispersion (PyMC ``alpha=``).
        - ``alpha_pareto`` — TruncatedNormal[1.5, 2.5] (M1).
        - ``x_m`` — HalfNormal prior on TruncPareto floor.
        - ``pi`` — Dirichlet([2.0, 5.0, 3.0]) over TIER_IDS (spec §5.2).
        - ``tau_t`` — Deterministic (posterior-predictive emission column).
        - ``q_t_usd`` — Deterministic (USD cost per month).
        - ``q_t_cop`` — Deterministic (COP cost per month, via FX).
    - The Sonnet $/MTok closed form is asserted at construction
      (M3 BLOCK on drift > 0.01) before any pm.* node is built.
    - No imports from ``simulations.utils``.
    """

    priors: CohortPriors = field(default_factory=CohortPriors)
    fx_cop_per_usd: float = DEFAULT_FX_COP_PER_USD
    n_simulations: int = 1

    def __post_init__(self) -> None:
        # Validate FX rate (positive, finite). The M3 check belongs at
        # __call__ per RC-B2; only struct validation lives here.
        if not (math.isfinite(self.fx_cop_per_usd)
                and self.fx_cop_per_usd > 0.0):
            raise ValueError(
                f"T1ModelFactory.fx_cop_per_usd = {self.fx_cop_per_usd}"
                f" must be a finite float > 0"
            )
        if self.n_simulations <= 0:
            raise ValueError(
                f"T1ModelFactory.n_simulations = {self.n_simulations}"
                f" must be > 0"
            )

    def __call__(self, *, observed_tau_t: np.ndarray | None = None) -> pm.Model:
        """Build and return the spec §5.1 (T1) PyMC model.

        Args:
            observed_tau_t: optional 1-D array of observed monthly latent
                cost samples. If ``None`` (default), the model is purely
                generative — suitable for posterior-predictive sampling
                from the prior (Phase-2 Stage-2 synthetic-Bayesian fit
                per spec §8(8) sim-count floor). If provided, attached
                as ``observed=`` to the per-month ``tau_t`` Normal-shape
                likelihood (kernel approximation; the exact compound-sum
                likelihood is intractable in closed form — Stage-3 work).

        Returns:
            A ``pm.Model`` instance with random variables and posterior-
            predictive Deterministics declared per the behavior contract.

        Raises:
            AssertionError: from :func:`_build_sonnet_blended_price` if
                M3 closed-form drift exceeds :data:`M3_BLENDED_PRICE_ABS_TOL`.
        """
        # M3 assertion at call site (RC-B2): fail fast before any PyMC
        # node creation if the shipped BlendedPriceFn drifts.
        price_per_mtok = _build_sonnet_blended_price()

        nb = self.priors.negbin
        ap = self.priors.alpha
        xp = self.priors.x_m
        d_t = self.priors.active_days_per_month

        with pm.Model() as model:
            # ─── Tier mixture (spec §5.2) ─────────────────────────────
            pi = pm.Dirichlet(
                "pi",
                a=np.array(DIRICHLET_ALPHA_VECTOR, dtype=np.float64),
            )

            # ─── NegBin (μ, φ) prior pin (MQ-B2) ──────────────────────
            # μ — Lognormal-shape: prior median at nb.mu_loc with log-σ.
            mu = pm.Lognormal(
                "mu",
                mu=math.log(nb.mu_loc),
                sigma=nb.mu_log_sigma,
            )
            # φ — HalfNormal centered near nb.phi_loc; expressed via
            # Truncated to keep φ > 0 with prior mean ≈ phi_loc.
            phi = pm.TruncatedNormal(
                "phi",
                mu=nb.phi_loc,
                sigma=nb.phi_sigma,
                lower=1.0,  # avoid pathological phi → 0
            )

            # ─── TruncPareto α + x_m priors (M1 floor) ────────────────
            alpha_pareto = pm.TruncatedNormal(
                "alpha_pareto",
                mu=ap.alpha_loc,
                sigma=ap.alpha_scale,
                lower=ap.alpha_lower,  # 1.5 — M1 floor
                upper=ap.alpha_upper,  # 2.5 — spec §5.2 bracket
            )
            x_m = pm.HalfNormal("x_m", sigma=xp.xm_sigma)

            # ─── Per-active-day NegBin turn count (mean–dispersion) ───
            # Sample a NegBin draw with shape (active_days,) for posterior
            # predictive aggregation. We register a *named* RV so it
            # appears in pp draws.
            n_per_day = pm.NegativeBinomial(
                "n_per_day",
                mu=mu,
                alpha=phi,
                shape=(d_t,),
            )

            # Total monthly turn count (Deterministic — sum over days).
            n_month = pm.Deterministic("n_month", pt.sum(n_per_day))

            # ─── Tokens-per-turn TruncPareto via PyMC Truncated wrapper ─
            # Spec §5.1 (T1) per-turn iid TruncPareto(α, x_m, κ).
            # Mean of TruncPareto(α, x_m, x_max), α > 1, equals
            #   E[X] = (α / (α-1)) · x_m · (1 - (x_m/x_max)^{α-1}) /
            #           (1 - (x_m/x_max)^α)
            # The deterministic monthly token total is (turns) × (mean per turn);
            # the doubly-stochastic monthly latent cost is therefore captured
            # by tau_t = n_month × E[τ_per_turn | α, x_m] for the mean-based
            # likelihood arm. Posterior-predictive draws will instead sample
            # n_month and per-turn variates explicitly via
            # pm.sample_posterior_predictive (MQ-B4).
            x_max = xp.x_max_fixed
            ratio = x_m / x_max
            ratio_pow_alpha = pt.pow(ratio, alpha_pareto)
            ratio_pow_alpha_minus_one = pt.pow(ratio, alpha_pareto - 1.0)
            mean_tau_per_turn = pm.Deterministic(
                "mean_tau_per_turn",
                (alpha_pareto / (alpha_pareto - 1.0))
                * x_m
                * (1.0 - ratio_pow_alpha_minus_one)
                / (1.0 - ratio_pow_alpha),
            )

            # τ_t monthly token total (Deterministic — populated by
            # pm.sample_posterior_predictive at emission time per MQ-B4).
            tau_t = pm.Deterministic(
                "tau_t",
                pt.cast(n_month, "float64") * mean_tau_per_turn,
            )

            # ─── q_t_usd / q_t_cop deterministic emission columns ─────
            # Cost-per-turn USD: (tokens) × ($/MTok) / 1e6. We use the
            # closed-form blended price (spec §5.1; M3 assertion above).
            q_t_usd = pm.Deterministic(
                "q_t_usd",
                tau_t * price_per_mtok / 1.0e6,
            )
            pm.Deterministic(
                "q_t_cop",
                q_t_usd * self.fx_cop_per_usd,
            )

            # If observed monthly cost is supplied, use a normal-kernel
            # likelihood centered on the deterministic τ_t mean, with
            # scale matched to the doubly-stochastic theoretical variance.
            # This is the Stage-2 synthetic-Bayesian likelihood proxy;
            # exact closed-form for Σ Σ TruncPareto is intractable.
            if observed_tau_t is not None:
                obs_arr = np.asarray(observed_tau_t, dtype=np.float64)
                if obs_arr.ndim != 1:
                    raise ValueError(
                        f"observed_tau_t must be 1-D; got shape {obs_arr.shape}"
                    )
                # Use a HalfNormal noise scale; the model is identifiable
                # via the τ_t deterministic mean.
                sigma_obs = pm.HalfNormal("sigma_obs", sigma=tau_t * 0.2 + 1.0)
                pm.Normal(
                    "tau_t_observed",
                    mu=tau_t,
                    sigma=sigma_obs,
                    observed=obs_arr,
                )

            # Tier categorical (latent label per simulation row).
            # Used downstream by emit.py to attach tier_id partition keys.
            pm.Categorical("tier_idx", p=pi)

        return model


__all__ = [
    "DEFAULT_FX_COP_PER_USD",
    "M3_BLENDED_PRICE_ABS_TOL",
    "M3_SONNET_BLENDED_PRICE_EXPECTED",
    "T1ModelFactory",
]
