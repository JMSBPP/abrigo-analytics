r"""Tests for SAAS-COHORT-5-STRIP / strategies sub-package (Task 2.1).

Coverage:

- NormalizedEnvelopeScore validation contract: rejects empty
  primitive_id, out-of-alphabet comparability_proof, negative or
  non-finite normalized_score.
- compute_normalized_score: returns the expected scalar on a
  hand-constructed strip whose payoff floor at spot is 0
  (tiled-body geometry -> penalty = 1.0 -> score == max_rel_error).
- Exception hierarchy: ComparabilityProof{Missing,Falsified}Error
  both subclass StrategyAdapterError, which subclasses Exception.

These are Value-tier sanity tests only; behaviour-level tests for
concrete StrategyAdapter implementations land in Task 2.2.
"""

from __future__ import annotations

import math

import pytest

from simulations.saas_builder.cohort_5_strip import (
    IronCondorStrip,
    ReplicationVerdict,
    build_strip,
    default_strip_geometry,
    verify_carr_madan_envelope,
)
from simulations.saas_builder.cohort_5_strip.strategies import (
    ComparabilityProofFalsifiedError,
    ComparabilityProofMissingError,
    NormalizedEnvelopeScore,
    StrategyAdapterError,
    compute_normalized_score,
)

# ─── Canonical strip fixture (mirrors test_saas_cohort5_strip.py) ────────────

S_0_CANONICAL = 4000.0
SIGMA_0_CANONICAL = 20_000.0
K_STAR_CANONICAL = 4_687.94


@pytest.fixture
def canonical_strip() -> IronCondorStrip:
    return build_strip(
        s_0=S_0_CANONICAL,
        sigma_0=SIGMA_0_CANONICAL,
        k_star=K_STAR_CANONICAL,
        geometry=default_strip_geometry(),
    )


@pytest.fixture
def canonical_verdict(canonical_strip: IronCondorStrip) -> ReplicationVerdict:
    return verify_carr_madan_envelope(canonical_strip)


# ─── NormalizedEnvelopeScore validation ──────────────────────────────────────


def test_normalized_envelope_score_rejects_empty_primitive_id(
    canonical_verdict: ReplicationVerdict,
) -> None:
    with pytest.raises(ValueError, match="primitive_id"):
        NormalizedEnvelopeScore(
            primitive_id="",
            comparability_proof="tiled_body",
            normalized_score=0.10,
            raw_verdict=canonical_verdict,
        )


def test_normalized_envelope_score_rejects_unknown_comparability_proof(
    canonical_verdict: ReplicationVerdict,
) -> None:
    with pytest.raises(ValueError, match="comparability_proof"):
        NormalizedEnvelopeScore(
            primitive_id="reverse_iron_condor",
            comparability_proof="ad_hoc_lane",  # type: ignore[arg-type]
            normalized_score=0.10,
            raw_verdict=canonical_verdict,
        )


def test_normalized_envelope_score_rejects_negative_score(
    canonical_verdict: ReplicationVerdict,
) -> None:
    with pytest.raises(ValueError, match="must be >= 0"):
        NormalizedEnvelopeScore(
            primitive_id="reverse_iron_condor",
            comparability_proof="tiled_body",
            normalized_score=-0.01,
            raw_verdict=canonical_verdict,
        )


def test_normalized_envelope_score_rejects_nonfinite_score(
    canonical_verdict: ReplicationVerdict,
) -> None:
    with pytest.raises(ValueError, match="must be finite"):
        NormalizedEnvelopeScore(
            primitive_id="reverse_iron_condor",
            comparability_proof="tiled_body",
            normalized_score=math.inf,
            raw_verdict=canonical_verdict,
        )


def test_normalized_envelope_score_accepts_valid_construction(
    canonical_verdict: ReplicationVerdict,
) -> None:
    score = NormalizedEnvelopeScore(
        primitive_id="reverse_iron_condor",
        comparability_proof="tiled_body",
        normalized_score=canonical_verdict.max_relative_error,
        raw_verdict=canonical_verdict,
    )
    assert score.primitive_id == "reverse_iron_condor"
    assert score.comparability_proof == "tiled_body"
    assert score.normalized_score == canonical_verdict.max_relative_error
    assert score.raw_verdict is canonical_verdict


# ─── compute_normalized_score formula ────────────────────────────────────────


def test_compute_normalized_score_tiled_body_gives_unit_penalty(
    canonical_strip: IronCondorStrip,
    canonical_verdict: ReplicationVerdict,
) -> None:
    """Pin S5 holds for the canonical strip -> Π(S_0) = 0 ->

    penalty factor = 1.0 -> score == max_relative_error exactly.
    """
    score = compute_normalized_score(canonical_verdict, canonical_strip)
    assert math.isclose(
        score, canonical_verdict.max_relative_error, rel_tol=1e-9, abs_tol=1e-12
    ), (
        f"Tiled-body strip should yield score == max_rel_error;"
        f" got score={score}, max_rel_error={canonical_verdict.max_relative_error}"
    )


# ─── Exception hierarchy ─────────────────────────────────────────────────────


def test_strategy_adapter_exception_hierarchy() -> None:
    assert issubclass(StrategyAdapterError, Exception)
    assert issubclass(ComparabilityProofMissingError, StrategyAdapterError)
    assert issubclass(ComparabilityProofFalsifiedError, StrategyAdapterError)
    # The two leaf exceptions are NOT siblings of each other -
    # both descend from StrategyAdapterError but are distinct.
    assert not issubclass(
        ComparabilityProofMissingError, ComparabilityProofFalsifiedError
    )
    assert not issubclass(
        ComparabilityProofFalsifiedError, ComparabilityProofMissingError
    )
