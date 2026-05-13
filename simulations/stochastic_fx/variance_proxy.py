"""Phase-A algebraic σ_T computation and ε-inversion for the stochastic-fx variant.

Parent spec: ``docs/specs/2026-05-11-stochastic-fx-variant-design.md`` v0.3 §6
defines the realised-variance proxy σ_T (eq. 7) and its algebraic inversion to
the IronCondor strike width ε (eq. 8). Parent plan
``docs/plans/2026-05-11-stochastic-fx-variant.md`` v0.4 §9 Task 4.1 scopes this
module to **Phase A only** — the algebraic-substitution identity check that is
family-agnostic and closed-form. Phase B (moment match) and Phase C (KS
goodness-of-fit) belong to Task 4.2's ``InversionVerifier`` and are
intentionally NOT defined here.

Module surface (Callable tier — three free functions, no class):

- :func:`recompute_sigma_t` — re-applies spec v0.3 §6 eq. (7) discretely to the
  ensemble's paths and returns the per-path realised-variance array. Used to
  cross-check the σ_T values stored on the PathEnsemble by Task 3.x's
  generators against an INDEPENDENTLY recomputed copy of the same formula.
  Round-trip discrepancy must lie within :data:`NUMERICAL_IDENTITY_TOL`.
- :func:`eq_8_inversion` — closed-form spec v0.3 §6 eq. (8):
  ``ε = sqrt(8·σ_T / x̄²)``. Trivial-degenerate limit at ``σ_T = 0`` returns
  ``0.0`` exactly (Pin Z1.3a corner case).
- :func:`phase_a_algebraic_check` — Pin Z1.3a algebraic substitution check.
  For each path's stored σ_T_n, verifies the closed-form identity
  ``ε_n² == 8·σ_T_n / x̄²`` to float64 precision. Family-agnostic — the
  algebra is identical for GBM, OU, and Merton.

Module-level constant:

- :data:`NUMERICAL_IDENTITY_TOL` — re-exported from
  ``simulations.saas_builder.cohort_4.types`` (FLAG-RC-3 single-source-of-truth
  disposition per plan v0.4 §9 Task 4.1 acceptance bullet 1). Downstream
  consumers (Task 4.2 ``InversionVerifier``; Task 5 emit) import this constant
  from ``variance_proxy`` so the stochastic_fx subtree exposes one canonical
  numerical-identity tolerance.

Tier purity (functional-python skill — Callable tier):

- Allowed imports: stdlib ``json`` / ``math``, ``numpy``,
  ``simulations.stochastic_fx.types`` (PathEnsemble),
  ``simulations.stochastic_fx._errors`` (SDEParameterError), and
  ``simulations.saas_builder.cohort_4.types`` (NUMERICAL_IDENTITY_TOL reuse).
- FORBIDDEN imports: sibling Callables ``moments`` and ``generators``
  (cross-Callable imports break tier purity); ``utils`` (Task 5 territory).
"""

from __future__ import annotations

import json
import math
from typing import Final

import numpy as np

from simulations.saas_builder.cohort_4.types import (
    NUMERICAL_IDENTITY_TOL as _COHORT_4_NUMERICAL_IDENTITY_TOL,
)
from simulations.stochastic_fx._errors import SDEParameterError
from simulations.stochastic_fx.types import PathEnsemble

#: Numerical-identity tolerance ceiling for Phase-A algebraic checks
#: (FLAG-RC-3 disposition per plan v0.4 §9 Task 4.1 acceptance bullet 1 —
#: reused verbatim from :data:`simulations.saas_builder.cohort_4.types.NUMERICAL_IDENTITY_TOL`).
NUMERICAL_IDENTITY_TOL: Final[float] = _COHORT_4_NUMERICAL_IDENTITY_TOL


# ─── Function 1: recompute σ_T from ensemble.paths ───────────────────────────


def recompute_sigma_t(ensemble: PathEnsemble) -> np.ndarray:
    """Re-apply spec v0.3 §6 eq. (7) to ``ensemble.paths`` and return per-path σ_T.

    The discrete realised-variance estimator is, for each path *i*:

    .. math::

        \\sigma_{T,i} = \\frac{1}{T} \\sum_{t=0}^{n_{\\text{steps}}}
                       \\bigl(x_{i,t} - \\bar{x}_i\\bigr)^2,

    where :math:`\\bar{x}_i` is the path-mean and *T* is read out of
    ``ensemble.canonical_params_json``. The formula mirrors the vectorised
    computation in ``simulations.stochastic_fx.generators`` (e.g. GBM line
    ~183), so a fresh re-application here is the natural Phase-A
    cross-check: any drift between the generator and this recomputation
    signals a formula transcription error.

    Parameters
    ----------
    ensemble:
        A validated :class:`PathEnsemble`. The function reads ``paths`` and
        the ``"T"`` key out of ``canonical_params_json``.

    Returns
    -------
    numpy.ndarray
        1-D float array of shape ``(N_paths,)``.

    Raises
    ------
    SDEParameterError
        If ``canonical_params_json`` cannot be parsed as JSON or lacks a
        positive-real ``"T"`` field.
    """
    try:
        params_dict = json.loads(ensemble.canonical_params_json)
    except json.JSONDecodeError as exc:
        raise SDEParameterError(
            "canonical_params_json must be parseable JSON; "
            f"got error: {exc!s}"
        ) from exc
    if "T" not in params_dict:
        raise SDEParameterError(
            "canonical_params_json must contain a 'T' key; "
            f"got keys: {sorted(params_dict.keys())!r}"
        )
    T_value = params_dict["T"]
    if not isinstance(T_value, (int, float)) or isinstance(T_value, bool):
        raise SDEParameterError(
            f"canonical_params_json['T'] must be a real number; got {T_value!r}"
        )
    if not math.isfinite(T_value) or T_value <= 0.0:
        raise SDEParameterError(
            f"canonical_params_json['T'] must be finite and > 0; got {T_value!r}"
        )

    paths = ensemble.paths
    path_means = np.mean(paths, axis=1, keepdims=True)
    sigma_t: np.ndarray = np.sum((paths - path_means) ** 2, axis=1) / float(T_value)
    return sigma_t


# ─── Function 2: eq.(8) algebraic inversion σ_T → ε ──────────────────────────


def eq_8_inversion(sigma_t: float, x_bar: float) -> float:
    """Closed-form spec v0.3 §6 eq. (8): ``ε = sqrt(8·σ_T / x̄²)``.

    Returns the IronCondor strike width ε for a single realised-variance
    proxy value σ_T and FX mean x̄. The mapping is monotonic in σ_T and
    convex; closed-form so machine-epsilon-precise on float64.

    Trivial-degenerate limit (Pin Z1.3a): at ``sigma_t == 0.0`` the
    function returns exactly ``0.0``, since ``sqrt(0) == 0.0`` in IEEE 754.

    Parameters
    ----------
    sigma_t:
        Realised-variance proxy on the path, in the same units as ``x_bar**2``.
        Must be non-negative and finite.
    x_bar:
        Path-mean FX level (strictly positive, finite).

    Returns
    -------
    float
        The non-negative finite strike width ε.

    Raises
    ------
    SDEParameterError
        If ``sigma_t`` is negative or non-finite, or if ``x_bar`` is
        non-positive or non-finite.
    """
    if not math.isfinite(sigma_t):
        raise SDEParameterError(f"sigma_t must be finite; got {sigma_t!r}")
    if sigma_t < 0.0:
        raise SDEParameterError(f"sigma_t must be >= 0; got {sigma_t!r}")
    if not math.isfinite(x_bar):
        raise SDEParameterError(f"x_bar must be finite; got {x_bar!r}")
    if x_bar <= 0.0:
        raise SDEParameterError(f"x_bar must be > 0; got {x_bar!r}")
    return math.sqrt(8.0 * sigma_t / x_bar**2)


# ─── Function 3: Phase-A algebraic substitution check (Pin Z1.3a) ────────────


def phase_a_algebraic_check(
    ensemble: PathEnsemble, x_bar: float
) -> tuple[bool, float]:
    """Pin Z1.3a algebraic substitution check — closed-form identity round-trip.

    For each path's stored σ_T_n in ``ensemble.sigma_t``, compute
    ``ε_n = eq_8_inversion(σ_T_n, x̄)`` and verify the identity

    .. math::

        \\varepsilon_n^2 \\;=\\; \\frac{8 \\, \\sigma_{T,n}}{\\bar{x}^2}.

    Because eq. (8) is closed-form, the residual is essentially machine
    epsilon — this function tests the absence of a transcription bug, not
    the empirical viability of the mapping. PASS iff the maximum absolute
    residual across all N paths is ≤ :data:`NUMERICAL_IDENTITY_TOL`.

    Family-agnostic: the algebra is identical for GBM, OU, and Merton —
    the σ_T values on the ensemble already encode the family-specific
    information.

    Parameters
    ----------
    ensemble:
        A validated :class:`PathEnsemble`. Phase A consumes
        ``ensemble.sigma_t`` (N-vector of per-path realised-variance proxies).
    x_bar:
        Positive finite FX mean used in the closed-form inversion. Typically
        the canonical pin's ``x_0`` for trivial-degenerate testing; may also
        be a path-mean estimate from the ensemble in production use.

    Returns
    -------
    tuple[bool, float]
        ``(pass_flag, max_abs_residual)``. ``pass_flag`` is ``True`` iff
        ``max_abs_residual <= NUMERICAL_IDENTITY_TOL``.

    Raises
    ------
    SDEParameterError
        If ``x_bar`` is non-positive or non-finite.
    """
    if not math.isfinite(x_bar):
        raise SDEParameterError(f"x_bar must be finite; got {x_bar!r}")
    if x_bar <= 0.0:
        raise SDEParameterError(f"x_bar must be > 0; got {x_bar!r}")

    sigma_t_array = ensemble.sigma_t
    # Vectorised closed-form inversion: ε_n = sqrt(8·σ_T_n / x̄²).
    # numpy.sqrt is safe at σ_T_n == 0 (returns 0.0); the ensemble's
    # __post_init__ already guarantees finite sigma_t entries.
    eps_squared = 8.0 * sigma_t_array / (x_bar**2)
    eps_array = np.sqrt(eps_squared)
    # Round-trip identity: (ε_n)² − 8·σ_T_n / x̄² should be machine-epsilon.
    residuals = eps_array**2 - eps_squared
    max_abs_residual = float(np.max(np.abs(residuals)))
    pass_flag = bool(max_abs_residual <= NUMERICAL_IDENTITY_TOL)
    return pass_flag, max_abs_residual


__all__ = [
    "NUMERICAL_IDENTITY_TOL",
    "eq_8_inversion",
    "phase_a_algebraic_check",
    "recompute_sigma_t",
]
