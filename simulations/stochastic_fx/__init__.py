"""Stochastic-FX variant — PRIMITIVES.md §15 open item 2 (Path A v3).

Parent spec: docs/specs/2026-05-11-stochastic-fx-variant-design.md v0.3.
Parent plan: docs/plans/2026-05-11-stochastic-fx-variant.md v0.2.

Three SDE families (GBM, OU, Merton jump-diffusion) with per-family
three-phase verification (Phase A algebraic / Phase B moment match /
Phase C KS goodness-of-fit). Strip preservation invariant
(Pin Z1.6 — cohort_5_strip's IronCondor_strip.json audit_block
unchanged before/after this package).
"""
from simulations.stochastic_fx._errors import (
    InversionTestFailedError,
    MCBudgetExceededError,
    MomentMatchFailedError,
    SDEParameterError,
    StochasticFXError,
)
from simulations.stochastic_fx.generators import (
    GBMPathGenerator,
    JumpDiffusionPathGenerator,
    OUPathGenerator,
)
from simulations.stochastic_fx.moments import (
    gbm_sigma_t_moments,
    merton_sigma_t_moments,
    ou_sigma_t_moments,
)
from simulations.stochastic_fx.types import (
    CANONICAL_GBM,
    CANONICAL_MERTON,
    CANONICAL_OU,
    GBMParameters,
    InversionVerdict,
    JumpDiffusionParameters,
    OUParameters,
    PathEnsemble,
)
from simulations.stochastic_fx.variance_proxy import (
    NUMERICAL_IDENTITY_TOL,
    eq_8_inversion,
    phase_a_algebraic_check,
    recompute_sigma_t,
)

__all__ = [
    "CANONICAL_GBM",
    "CANONICAL_MERTON",
    "CANONICAL_OU",
    "GBMParameters",
    "GBMPathGenerator",
    "InversionTestFailedError",
    "InversionVerdict",
    "JumpDiffusionParameters",
    "JumpDiffusionPathGenerator",
    "MCBudgetExceededError",
    "MomentMatchFailedError",
    "NUMERICAL_IDENTITY_TOL",
    "OUParameters",
    "OUPathGenerator",
    "PathEnsemble",
    "SDEParameterError",
    "StochasticFXError",
    "eq_8_inversion",
    "gbm_sigma_t_moments",
    "merton_sigma_t_moments",
    "ou_sigma_t_moments",
    "phase_a_algebraic_check",
    "recompute_sigma_t",
]
