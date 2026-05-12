"""Tests for the stochastic-fx variant package.

Parent plan: docs/plans/2026-05-11-stochastic-fx-variant.md v0.2.
"""
from simulations.stochastic_fx import (
    InversionTestFailedError,
    MCBudgetExceededError,
    MomentMatchFailedError,
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
