"""Tests for the stochastic-fx variant package.

Parent plan: docs/plans/2026-05-11-stochastic-fx-variant.md v0.2.
"""
import pytest

from simulations.stochastic_fx import (
    CANONICAL_GBM,
    CANONICAL_MERTON,
    CANONICAL_OU,
    GBMParameters,
    InversionTestFailedError,
    JumpDiffusionParameters,
    MCBudgetExceededError,
    MomentMatchFailedError,
    OUParameters,
    SDEParameterError,
    StochasticFXError,
)


def test_exception_hierarchy() -> None:
    """All stochastic-fx errors derive from StochasticFXError, which derives from Exception."""
    assert issubclass(StochasticFXError, Exception)
    for child in (
        SDEParameterError,
        InversionTestFailedError,
        MomentMatchFailedError,
        MCBudgetExceededError,
    ):
        assert issubclass(child, StochasticFXError)
        assert issubclass(child, Exception)


def test_canonical_gbm_passes_post_init() -> None:
    """The spec v0.3 §4.2 GBM pin constructs successfully."""
    assert isinstance(CANONICAL_GBM, GBMParameters)
    assert CANONICAL_GBM.n_steps == 5000


def test_canonical_ou_passes_post_init() -> None:
    """The spec v0.3 §4.2 OU pin constructs successfully."""
    assert isinstance(CANONICAL_OU, OUParameters)
    assert CANONICAL_OU.theta == 1.0


def test_canonical_merton_passes_post_init() -> None:
    """The spec v0.3 §4.2 Merton jump-diffusion pin constructs successfully."""
    assert isinstance(CANONICAL_MERTON, JumpDiffusionParameters)
    assert CANONICAL_MERTON.lambda_jump == 1.0


def test_gbm_rejects_zero_sigma() -> None:
    """``sigma > 0`` invariant — zero sigma is rejected."""
    with pytest.raises(SDEParameterError):
        GBMParameters(
            mu=0.0,
            sigma=0.0,
            x_0=4000.0,
            T=12.0,
            dt=12.0 / 5000.0,
            n_steps=5000,
        )


def test_ou_rejects_zero_theta() -> None:
    """``theta > 0`` invariant — zero mean-reversion speed is rejected."""
    with pytest.raises(SDEParameterError):
        OUParameters(
            theta=0.0,
            mu_bar=4000.0,
            sigma=0.10 * 4000.0,
            x_0=4000.0,
            T=12.0,
            dt=12.0 / 5000.0,
            n_steps=5000,
        )


def test_merton_rejects_negative_lambda() -> None:
    """``lambda_jump >= 0`` invariant — negative jump intensity is rejected."""
    with pytest.raises(SDEParameterError):
        JumpDiffusionParameters(
            mu=0.0,
            sigma=0.05,
            lambda_jump=-0.1,
            jump_mean=0.0,
            jump_std=0.10,
            x_0=4000.0,
            T=12.0,
            dt=12.0 / 5000.0,
            n_steps=5000,
        )


def test_gbm_rejects_n_steps_dt_mismatch() -> None:
    """Grid-consistency invariant — n_steps * dt must equal T within tolerance."""
    with pytest.raises(SDEParameterError):
        GBMParameters(
            mu=0.0,
            sigma=0.10,
            x_0=4000.0,
            T=12.0,
            dt=1.0,
            n_steps=11,
        )


def test_gbm_rejects_n_steps_under_2() -> None:
    """``n_steps >= 2`` invariant — single-step grids are rejected."""
    with pytest.raises(SDEParameterError):
        GBMParameters(
            mu=0.0,
            sigma=0.10,
            x_0=4000.0,
            T=12.0,
            dt=12.0,
            n_steps=1,
        )


def test_merton_accepts_negative_mu_and_jump_mean() -> None:
    """``mu`` and ``jump_mean`` are unconstrained — negatives must construct cleanly."""
    params = JumpDiffusionParameters(
        mu=-0.5,
        sigma=0.05,
        lambda_jump=1.0,
        jump_mean=-0.2,
        jump_std=0.10,
        x_0=4000.0,
        T=12.0,
        dt=12.0 / 5000.0,
        n_steps=5000,
    )
    assert params.mu == -0.5
    assert params.jump_mean == -0.2
