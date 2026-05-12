"""Stochastic-FX typed errors.

Per functional-python skill: only Exception subclassing is admitted as
class-inheritance outside of Protocols. Parent spec
``docs/specs/2026-05-11-stochastic-fx-variant-design.md`` v0.3 defines
Pin Z1.3b (moment match), Pin Z1.4 (KS inversion), and the N=1000 MC
floor (§8 anti-fishing) gated by these error classes.
"""

from __future__ import annotations


class StochasticFXError(Exception):
    """Base class for the stochastic-fx package (gates Pin Z1 family)."""


class SDEParameterError(StochasticFXError):
    """Raised when an SDE Parameters frozen-dc ``__post_init__`` rejects invalid inputs."""


class InversionTestFailedError(StochasticFXError):
    """Raised by Pin Z1.4 KS goodness-of-fit gate failures."""


class MomentMatchFailedError(StochasticFXError):
    """Raised by Pin Z1.3b moment-match gate failures."""


class MCBudgetExceededError(StochasticFXError):
    """Raised when ``ensemble.paths.shape[0] != 1000`` at InversionVerifier construction (Pin Z1 N=1000 floor)."""


__all__ = [
    "InversionTestFailedError",
    "MCBudgetExceededError",
    "MomentMatchFailedError",
    "SDEParameterError",
    "StochasticFXError",
]
