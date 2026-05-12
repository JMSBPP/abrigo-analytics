"""Callable-tier SDE path generators for the stochastic-fx variant.

Parent spec: ``docs/specs/2026-05-11-stochastic-fx-variant-design.md`` v0.3
§5 eq. (6) (Itô log-update) and §6 eq. (7) (discrete σ_T proxy).
Parent plan: ``docs/plans/2026-05-11-stochastic-fx-variant.md`` §8 Task 3.1
pins the Euler-Maruyama-on-log-scale discretization plus the deterministic
``audit_block`` recipe transcribed here.

This module hosts one frozen-dataclass per SDE family whose ``__call__``
surface accepts a deterministic RNG seed and an ensemble size and returns
the family's :class:`~simulations.stochastic_fx.types.PathEnsemble`. RNG
handling pins determinism (Pin Z1.2): identical
``(params, rng_seed, n_paths)`` triples yield bit-exact ensembles AND
bit-exact ``audit_block``\\ s.

Task 3.1 ships ``GBMPathGenerator`` only; ``OUPathGenerator`` (Task 3.2)
and ``JumpDiffusionPathGenerator`` (Task 3.3) append to this module in
subsequent commits.

Discretization scheme (Plan §8.3.1, GBM family)
------------------------------------------------
Euler-Maruyama on the log-scale, exact for GBM modulo float arithmetic:

    log_step = (mu - sigma**2 / 2) * dt + sigma * sqrt(dt) * Z

where ``Z ~ N(0, 1)`` and the trailing ``- sigma**2 / 2`` is the Itô
correction. Omitting it produces a biased mean of the terminal log-price
of magnitude ``sigma**2 / 2 * T``; the math-anchor test in
``simulations/tests/test_saas_stochastic_fx.py`` catches this directly.

σ_T per path (Plan §8.3.1 step 3 / Spec v0.3 §6 eq. 7)
-------------------------------------------------------
Discrete realised-variance proxy, normalised by ``T`` (NOT by ``n+1``):

    sigma_t[i] = (1 / T) * sum_{j=0..n_steps} (paths[i, j] - mean(paths[i, :]))**2

Matches the B1 plan's σ_T contract per MQ-FLAG-B1.1 disposition.

Audit-block recipe (Pin Z1.2)
-----------------------------
SHA-256 over three inputs in fixed order:

1. ``canonical_params_json`` bytes (``json.dumps(asdict(params),
   sort_keys=True)`` — stable byte serialization);
2. ``rng_seed`` packed as 8 little-endian bytes;
3. ``paths.tobytes()`` — the C-contiguous float64 path matrix bytes.

Result is a 64-char lowercase hex string consumed by
``PathEnsemble.__post_init__`` audit-block regex validation.

Tier discipline
---------------
Callable tier under the ``functional-python`` regime. Imports limited to
``dataclasses``, ``hashlib``, ``json``, ``math``, ``numpy``,
``simulations.stochastic_fx.types``, and
``simulations.stochastic_fx._errors``. MUST NOT import
``simulations.stochastic_fx.moments`` (sibling Callable — cross-Callable
imports break tier purity) or ``simulations.stochastic_fx.utils`` (does
not yet exist; Task 5 territory).
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from dataclasses import dataclass

import numpy as np

from simulations.stochastic_fx.types import GBMParameters, PathEnsemble


def _canonical_params_json(params: GBMParameters) -> str:
    """Serialize a Parameters frozen-dc to a stable canonical JSON string.

    ``dataclasses.asdict`` flattens the frozen-dc to a plain ``dict`` of
    plain Python scalars; ``json.dumps(..., sort_keys=True)`` enforces a
    stable byte ordering so the resulting string is reproducible across
    Python sessions. This canonical form is hashed into ``audit_block``
    AND stored on the returned ``PathEnsemble``.
    """
    return json.dumps(dataclasses.asdict(params), sort_keys=True)


def _compute_audit_block(
    canonical_params_json: str, rng_seed: int, paths: np.ndarray
) -> str:
    """Compute the deterministic SHA-256 audit_block for a path ensemble (Pin Z1.2).

    Inputs are hashed in fixed order: params JSON bytes, then ``rng_seed``
    packed as 8 little-endian bytes, then ``paths.tobytes()`` (the
    C-contiguous float64 path-matrix bytes). Returns a 64-char lowercase
    hex digest matching the ``PathEnsemble.audit_block`` regex.
    """
    hasher = hashlib.sha256()
    hasher.update(canonical_params_json.encode("utf-8"))
    hasher.update(rng_seed.to_bytes(8, "little"))
    hasher.update(paths.tobytes())
    return hasher.hexdigest()


@dataclass(frozen=True)
class GBMPathGenerator:
    """Deterministic GBM path-ensemble generator (Callable tier, Pin Z1.2).

    Holds a :class:`~simulations.stochastic_fx.types.GBMParameters` frozen-dc
    and exposes a ``__call__(rng_seed, n_paths)`` surface that returns a
    :class:`~simulations.stochastic_fx.types.PathEnsemble`. The discretization
    is Euler-Maruyama on the log-scale (exact for GBM modulo float
    arithmetic); the multiplicative log-step embeds the Itô correction
    ``-sigma**2 / 2``. σ_T per path follows spec v0.3 §6 eq. (7) discretely.

    Pin Z1.2 reproducibility: identical ``(params, rng_seed, n_paths)``
    triples yield bit-exact ``paths``, ``sigma_t``, and ``audit_block``.
    """

    params: GBMParameters

    def __call__(self, rng_seed: int, n_paths: int) -> PathEnsemble:
        """Sample ``n_paths`` GBM trajectories under the held parameters.

        Inputs (callee-validated; ``__post_init__`` on the returned
        ``PathEnsemble`` cross-validates the output invariants):

        - ``rng_seed`` — non-negative ``int`` seed for
          ``numpy.random.default_rng``; Pin Z1.2 reproducibility surface.
        - ``n_paths`` — positive ``int`` ensemble size; ``paths`` will have
          shape ``(n_paths, n_steps + 1)``.

        Returns
        -------
        PathEnsemble
            Family ``"gbm"``, validated by
            :meth:`PathEnsemble.__post_init__`.
        """
        params = self.params
        n_steps = params.n_steps
        dt = params.T / n_steps

        rng = np.random.default_rng(rng_seed)
        # Standard-normal Brownian increments; shape (n_paths, n_steps).
        z = rng.standard_normal((n_paths, n_steps))

        # Log-step per Euler-Maruyama on log-scale (Plan §8.3.1 step 2):
        # the trailing -sigma**2/2 is the Itô correction (MQ check anchor).
        log_step = (params.mu - params.sigma**2 / 2.0) * dt + params.sigma * math.sqrt(dt) * z

        # Cumulative log path with a leading zero column so column 0 maps to
        # log(x_0) after exponentiation; resulting shape (n_paths, n_steps+1).
        log_paths = np.concatenate(
            [np.zeros((n_paths, 1), dtype=log_step.dtype), np.cumsum(log_step, axis=1)],
            axis=1,
        )
        paths = params.x_0 * np.exp(log_paths)
        # Column 0 must equal x_0 EXACTLY (bit-exact); enforce via direct
        # assignment to avoid 1 * x_0 * exp(0) float-roundoff drift.
        paths[:, 0] = params.x_0

        # σ_T per path — spec v0.3 §6 eq. (7) DISCRETELY: sum of squared
        # deviations from the path mean, normalised by T (NOT by n+1).
        # Plan §8.3.1 step 3 pins this convention against B1 plan
        # MQ-FLAG-B1.1 disposition.
        path_means = np.mean(paths, axis=1, keepdims=True)
        sigma_t = np.sum((paths - path_means) ** 2, axis=1) / params.T

        canonical_params_json = _canonical_params_json(params)
        audit_block = _compute_audit_block(canonical_params_json, rng_seed, paths)

        return PathEnsemble(
            family_id="gbm",
            paths=paths,
            sigma_t=sigma_t,
            canonical_params_json=canonical_params_json,
            rng_seed=rng_seed,
            audit_block=audit_block,
        )


__all__ = [
    "GBMPathGenerator",
]
