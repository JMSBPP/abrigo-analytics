r"""SAAS-COHORT-5-STRIP / strategies — Stage-3 A1 alternative primitives.

Stage-3 Track A1 evaluates whether non-reverse-IC Panoptic primitives
(long strangle, butterfly, calendar spread, ...) can be compared on
equal footing against the canonical reverse-IC 12-leg strip emitted
by the parent ``cohort_5_strip`` package.

The Wave-1 pin commits each alternative primitive to one of three
comparability proofs (declared at adapter authorship time, NOT
post-hoc):

- ``tiled_body`` — adapter's built strip satisfies Pin S5
  ``Π_strip(S_0) = 0`` (canonical long-vol signature). Verified
  by the shipped ``assert_long_vol_signature``.
- ``primitive_variant`` — adapter supplies a primitive-specific
  envelope verifier (Task 2.3b authors concrete implementations).
- ``normalized_score`` — fallback scalar
  ``max_relative_error * (1 + |Π(S_0)| / max|Π|_grid)``, FROZEN at
  this commit per plan v0.3 §2.1.

Three-tier discipline (functional-python skill):

- ``types.py`` — Value tier (Protocols + frozen-dc + free function +
  module constants). NO inheritance except Protocol / Exception.
- ``_errors.py`` — typed sub-package exceptions (subclass Exception
  only).

Future tasks (out of scope for Task 2.1):

- Task 2.2 — concrete ``StrategyAdapter`` implementations per
  primitive (long_strangle, reverse_iron_condor, ...).
- Task 2.3a — pipeline glue that calls
  :func:`compute_normalized_score` with the canonical verifier.
- Task 2.3b — concrete ``PrimitiveVariantVerifier`` implementations
  for primitives that justify a non-log-contract proxy.
"""

from __future__ import annotations

from simulations.saas_builder.cohort_5_strip.strategies._errors import (
    ComparabilityProofFalsifiedError,
    ComparabilityProofMissingError,
    StrategyAdapterError,
)
from simulations.saas_builder.cohort_5_strip.strategies.adapters import (
    STRATEGY_COMPARISON_ANCHOR,
    LongStraddleAdapter,
    LongStrangleAdapter,
    ReverseIronCondorAdapter,
    ZeehbsAdapter,
)
from simulations.saas_builder.cohort_5_strip.strategies.types import (
    COMPARABILITY_PROOFS,
    NORMALIZED_SCORE_FORMULA_DOCSTRING,
    NORMALIZED_SCORE_GRID_POINTS,
    NORMALIZED_SCORE_GRID_SPAN,
    ComparabilityProof,
    NormalizedEnvelopeScore,
    PrimitiveVariantVerifier,
    StrategyAdapter,
    compute_normalized_score,
)

__all__ = [
    "COMPARABILITY_PROOFS",
    "ComparabilityProof",
    "ComparabilityProofFalsifiedError",
    "ComparabilityProofMissingError",
    "LongStraddleAdapter",
    "LongStrangleAdapter",
    "NORMALIZED_SCORE_FORMULA_DOCSTRING",
    "NORMALIZED_SCORE_GRID_POINTS",
    "NORMALIZED_SCORE_GRID_SPAN",
    "NormalizedEnvelopeScore",
    "PrimitiveVariantVerifier",
    "ReverseIronCondorAdapter",
    "STRATEGY_COMPARISON_ANCHOR",
    "StrategyAdapter",
    "StrategyAdapterError",
    "ZeehbsAdapter",
    "compute_normalized_score",
]
