"""Value-tier containers for stochastic-fx — per-family SDE Parameters + canonical pins.

Parent spec: ``docs/specs/2026-05-11-stochastic-fx-variant-design.md`` v0.3 §4.2
is the authority for the canonical numerical pins re-exported from this module.

This module declares one ``@dataclass(frozen=True)`` Parameters container per
SDE family covered by the stochastic-fx variant package:

- ``GBMParameters`` — geometric Brownian motion (drift ``mu``, volatility
  ``sigma``).
- ``OUParameters`` — mean-reverting Ornstein-Uhlenbeck (speed ``theta``,
  long-run level ``mu_bar``, volatility ``sigma``).
- ``JumpDiffusionParameters`` — Merton jump-diffusion (continuous drift
  ``mu``/``sigma`` plus compound-Poisson jump component
  ``lambda_jump``/``jump_mean``/``jump_std``).

Each frozen-dc validates invariants in ``__post_init__`` and raises
``SDEParameterError`` on violation. All numeric fields are checked for
finiteness; family-specific positivity / non-negativity constraints follow the
invariants table in the parent plan Task 1.2 brief.

The three module-level ``Final`` canonical pins (``CANONICAL_GBM``,
``CANONICAL_OU``, ``CANONICAL_MERTON``) reproduce spec v0.3 §4.2 verbatim and
function as the reference fixtures consumed downstream by the per-family
verifiers (Phase A algebraic / Phase B moment match / Phase C KS GoF).

NO IO at this tier. NO inheritance except Exception (via the raised
``SDEParameterError`` from ``simulations.stochastic_fx._errors``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

from simulations.stochastic_fx._errors import SDEParameterError


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _require_finite(name: str, value: float) -> None:
    """Raise ``SDEParameterError`` if ``value`` is NaN or +/- infinity."""
    if not math.isfinite(value):
        raise SDEParameterError(f"{name} must be finite; got {value!r}")


# ─── GBM ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GBMParameters:
    """Parameters for the geometric Brownian motion family.

    Invariants (raise ``SDEParameterError``):

    - ``sigma > 0``, ``x_0 > 0``, ``T > 0``, ``dt > 0``;
    - ``n_steps >= 2``;
    - ``abs(n_steps * dt - T) < 1e-9 * T`` (grid consistency);
    - all numeric fields finite.
    """

    mu: float
    sigma: float
    x_0: float
    T: float
    dt: float
    n_steps: int

    def __post_init__(self) -> None:
        _require_finite("mu", self.mu)
        _require_finite("sigma", self.sigma)
        _require_finite("x_0", self.x_0)
        _require_finite("T", self.T)
        _require_finite("dt", self.dt)
        if self.sigma <= 0.0:
            raise SDEParameterError(f"sigma must be > 0; got {self.sigma!r}")
        if self.x_0 <= 0.0:
            raise SDEParameterError(f"x_0 must be > 0; got {self.x_0!r}")
        if self.T <= 0.0:
            raise SDEParameterError(f"T must be > 0; got {self.T!r}")
        if self.dt <= 0.0:
            raise SDEParameterError(f"dt must be > 0; got {self.dt!r}")
        if self.n_steps < 2:
            raise SDEParameterError(f"n_steps must be >= 2; got {self.n_steps!r}")
        if abs(self.n_steps * self.dt - self.T) >= 1e-9 * self.T:
            raise SDEParameterError(
                "n_steps * dt must equal T within 1e-9 * T; "
                f"got n_steps={self.n_steps!r}, dt={self.dt!r}, T={self.T!r}, "
                f"residual={abs(self.n_steps * self.dt - self.T)!r}"
            )


# ─── OU ──────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class OUParameters:
    """Parameters for the Ornstein-Uhlenbeck (mean-reverting) family.

    Invariants (raise ``SDEParameterError``):

    - ``theta > 0``, ``sigma > 0``, ``mu_bar > 0``, ``x_0 > 0``;
    - ``T > 0``, ``dt > 0``;
    - ``n_steps >= 2``;
    - all numeric fields finite.
    """

    theta: float
    mu_bar: float
    sigma: float
    x_0: float
    T: float
    dt: float
    n_steps: int

    def __post_init__(self) -> None:
        _require_finite("theta", self.theta)
        _require_finite("mu_bar", self.mu_bar)
        _require_finite("sigma", self.sigma)
        _require_finite("x_0", self.x_0)
        _require_finite("T", self.T)
        _require_finite("dt", self.dt)
        if self.theta <= 0.0:
            raise SDEParameterError(f"theta must be > 0; got {self.theta!r}")
        if self.sigma <= 0.0:
            raise SDEParameterError(f"sigma must be > 0; got {self.sigma!r}")
        if self.mu_bar <= 0.0:
            raise SDEParameterError(f"mu_bar must be > 0; got {self.mu_bar!r}")
        if self.x_0 <= 0.0:
            raise SDEParameterError(f"x_0 must be > 0; got {self.x_0!r}")
        if self.T <= 0.0:
            raise SDEParameterError(f"T must be > 0; got {self.T!r}")
        if self.dt <= 0.0:
            raise SDEParameterError(f"dt must be > 0; got {self.dt!r}")
        if self.n_steps < 2:
            raise SDEParameterError(f"n_steps must be >= 2; got {self.n_steps!r}")


# ─── Merton jump-diffusion ───────────────────────────────────────────────────


@dataclass(frozen=True)
class JumpDiffusionParameters:
    """Parameters for the Merton jump-diffusion family.

    Invariants (raise ``SDEParameterError``):

    - ``sigma > 0``, ``lambda_jump >= 0``, ``jump_std > 0``;
    - ``x_0 > 0``, ``T > 0``, ``dt > 0``;
    - ``n_steps >= 2``;
    - all numeric fields finite.

    The continuous drift ``mu`` and the jump-size mean ``jump_mean`` are
    unrestricted (any finite real number is admitted).
    """

    mu: float
    sigma: float
    lambda_jump: float
    jump_mean: float
    jump_std: float
    x_0: float
    T: float
    dt: float
    n_steps: int

    def __post_init__(self) -> None:
        _require_finite("mu", self.mu)
        _require_finite("sigma", self.sigma)
        _require_finite("lambda_jump", self.lambda_jump)
        _require_finite("jump_mean", self.jump_mean)
        _require_finite("jump_std", self.jump_std)
        _require_finite("x_0", self.x_0)
        _require_finite("T", self.T)
        _require_finite("dt", self.dt)
        if self.sigma <= 0.0:
            raise SDEParameterError(f"sigma must be > 0; got {self.sigma!r}")
        if self.lambda_jump < 0.0:
            raise SDEParameterError(
                f"lambda_jump must be >= 0; got {self.lambda_jump!r}"
            )
        if self.jump_std <= 0.0:
            raise SDEParameterError(f"jump_std must be > 0; got {self.jump_std!r}")
        if self.x_0 <= 0.0:
            raise SDEParameterError(f"x_0 must be > 0; got {self.x_0!r}")
        if self.T <= 0.0:
            raise SDEParameterError(f"T must be > 0; got {self.T!r}")
        if self.dt <= 0.0:
            raise SDEParameterError(f"dt must be > 0; got {self.dt!r}")
        if self.n_steps < 2:
            raise SDEParameterError(f"n_steps must be >= 2; got {self.n_steps!r}")


# ─── Canonical pins (spec v0.3 §4.2) ─────────────────────────────────────────


#: Canonical GBM pin per spec v0.3 §4.2.
CANONICAL_GBM: Final[GBMParameters] = GBMParameters(
    mu=0.0,
    sigma=0.10 / math.sqrt(12.0),
    x_0=4000.0,
    T=12.0,
    dt=12.0 / 5000.0,
    n_steps=5000,
)

#: Canonical OU pin per spec v0.3 §4.2.
CANONICAL_OU: Final[OUParameters] = OUParameters(
    theta=1.0,
    mu_bar=4000.0,
    sigma=0.10 * 4000.0 / math.sqrt(2.0 * 1.0),
    x_0=4000.0,
    T=12.0,
    dt=12.0 / 5000.0,
    n_steps=5000,
)

#: Canonical Merton jump-diffusion pin per spec v0.3 §4.2.
CANONICAL_MERTON: Final[JumpDiffusionParameters] = JumpDiffusionParameters(
    mu=0.0,
    sigma=0.05 / math.sqrt(12.0),
    lambda_jump=1.0,
    jump_mean=0.0,
    jump_std=0.10,
    x_0=4000.0,
    T=12.0,
    dt=12.0 / 5000.0,
    n_steps=5000,
)


__all__ = [
    "CANONICAL_GBM",
    "CANONICAL_MERTON",
    "CANONICAL_OU",
    "GBMParameters",
    "JumpDiffusionParameters",
    "OUParameters",
]
