r"""Tests for SAAS-COHORT-5-STRIP / strategies sub-package (Task 2.1 + 2.2).

Coverage:

- NormalizedEnvelopeScore validation contract: rejects empty
  primitive_id, out-of-alphabet comparability_proof, negative or
  non-finite normalized_score.
- compute_normalized_score: returns the expected scalar on a
  hand-constructed strip whose payoff floor at spot is 0
  (tiled-body geometry -> penalty = 1.0 -> score == max_rel_error).
- Exception hierarchy: ComparabilityProof{Missing,Falsified}Error
  both subclass StrategyAdapterError, which subclasses Exception.
- Task 2.2 — per-adapter Hypothesis property tests for the four
  Phase-1 filtered StrategyAdapter implementations:
  ReverseIronCondorAdapter, LongStraddleAdapter, LongStrangleAdapter,
  ZeehbsAdapter. Each adapter's ``__call__`` must produce a fully-
  validated ``IronCondorStrip`` (all Pin S1-S4 invariants pass) over
  the admissible (s_0, sigma_0, k_star) region.
"""

from __future__ import annotations

import math

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from simulations.saas_builder.cohort_5_strip import (
    IronCondorStrip,
    ReplicationVerdict,
    assert_long_vol_signature,
    build_strip,
    default_strip_geometry,
    verify_carr_madan_envelope,
)
from simulations.saas_builder.cohort_5_strip.strategies import (
    STRATEGY_COMPARISON_ANCHOR,
    ComparabilityProofFalsifiedError,
    ComparabilityProofMissingError,
    LongStraddleAdapter,
    LongStrangleAdapter,
    NormalizedEnvelopeScore,
    ReverseIronCondorAdapter,
    StrategyAdapterError,
    ZeehbsAdapter,
    compute_normalized_score,
)
from simulations.saas_builder.cohort_5_strip.strategies.types import (
    StrategyAdapter,
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


# ─── Task 2.2 — per-adapter Hypothesis property tests ────────────────────────
#
# Each adapter is exercised over the admissible (s_0, sigma_0, k_star) region:
#
# - s_0, sigma_0, k_star: finite, > 0 (per IronCondorStrip.__post_init__).
# - Numerical caps below avoid float-overflow when exp(±2·epsilon)·s_0 is
#   evaluated inside StripBuilder (default epsilon = 0.1; widest geometry
#   is ZeehbsAdapter at log_offsets ±0.15 + delta_outer = 0.15, so
#   max exponent magnitude is 0.30 — exp(0.30) ≈ 1.35 — safe under 1e6).


@st.composite
def _adapter_inputs(draw: st.DrawFn) -> tuple[float, float, float]:
    """Draw a (s_0, sigma_0, k_star) triple over the admissible region.

    Ranges chosen to be well inside the cohort_5_strip API guards:

    - s_0 ∈ [1.0, 1e6]: spot price; canonical 4000.0 sits comfortably.
    - sigma_0 ∈ [1.0, 1e10]: linearization point; canonical 20_000 sits
      in this range. Bounded below 1.0 would risk K̂ blowing up.
    - k_star ∈ [1.0, 1e6]: equilibrium strike; canonical 4687.94 in range.
    """
    s_0 = draw(
        st.floats(min_value=1.0, max_value=1e6, allow_nan=False, allow_infinity=False)
    )
    sigma_0 = draw(
        st.floats(
            min_value=1.0, max_value=1e10, allow_nan=False, allow_infinity=False
        )
    )
    k_star = draw(
        st.floats(min_value=1.0, max_value=1e6, allow_nan=False, allow_infinity=False)
    )
    return s_0, sigma_0, k_star


def _assert_strip_invariants(strip: IronCondorStrip) -> None:
    """Re-assert the cohort_5_strip Pin S1-S4 invariants on a built strip.

    ``IronCondorStrip.__post_init__`` has already validated these at
    construction; this helper re-asserts at the test level so any
    silent regression surfaces in test output rather than as a raw
    ``ValueError`` from the dataclass.
    """
    # Pin S3 — exactly 3 condors, 12 legs.
    assert len(strip.condors) == 3
    total_legs = sum(len(c.legs) for c in strip.condors)
    assert total_legs == 12
    # Pin S2 — Carr-Madan weights sum to 1.
    weight_sum = sum(c.weight for c in strip.condors)
    assert math.isclose(weight_sum, 1.0, rel_tol=0.0, abs_tol=1e-12)
    # Pin S1 — strike ladder strictly ordered within each condor.
    for c in strip.condors:
        strikes = tuple(leg.strike for leg in c.legs)
        for i in range(3):
            assert strikes[i] < strikes[i + 1]
    # Pin S4 — anchor citations non-empty.
    assert strip.primitives_anchor
    assert strip.saas_note_anchor


@given(_adapter_inputs())
@settings(max_examples=40, deadline=None)
def test_reverse_iron_condor_adapter_produces_valid_strip(
    inputs: tuple[float, float, float],
) -> None:
    """ReverseIronCondorAdapter — strip invariants + tiled-body Pin S5."""
    s_0, sigma_0, k_star = inputs
    adapter = ReverseIronCondorAdapter()
    assert adapter.primitive_id == "reverse_iron_condor"
    assert adapter.comparability_proof == "tiled_body"
    strip = adapter(s_0=s_0, sigma_0=sigma_0, k_star=k_star)
    _assert_strip_invariants(strip)
    # Baseline lane = tiled_body — Pin S5 must hold by construction.
    assert_long_vol_signature(strip)


@given(_adapter_inputs())
@settings(max_examples=40, deadline=None)
def test_long_straddle_adapter_produces_valid_strip(
    inputs: tuple[float, float, float],
) -> None:
    """LongStraddleAdapter — narrow-clustered geometry, strip invariants pass."""
    s_0, sigma_0, k_star = inputs
    adapter = LongStraddleAdapter()
    assert adapter.primitive_id == "long_straddle"
    assert adapter.comparability_proof == "normalized_score"
    strip = adapter(s_0=s_0, sigma_0=sigma_0, k_star=k_star)
    _assert_strip_invariants(strip)
    # Geometry: log_offsets = (-eps/4, 0, +eps/4) with default eps = 0.1.
    assert strip.geometry.log_offsets[0] == pytest.approx(-0.025)
    assert strip.geometry.log_offsets[2] == pytest.approx(+0.025)
    assert strip.geometry.delta_inner == pytest.approx(0.0125)
    assert strip.geometry.delta_outer == pytest.approx(0.025)


@given(_adapter_inputs())
@settings(max_examples=40, deadline=None)
def test_long_strangle_adapter_produces_valid_strip(
    inputs: tuple[float, float, float],
) -> None:
    """LongStrangleAdapter — wider separated-body geometry, strip invariants pass."""
    s_0, sigma_0, k_star = inputs
    adapter = LongStrangleAdapter()
    assert adapter.primitive_id == "long_strangle"
    assert adapter.comparability_proof == "normalized_score"
    strip = adapter(s_0=s_0, sigma_0=sigma_0, k_star=k_star)
    _assert_strip_invariants(strip)
    # Geometry: log_offsets = (-eps, 0, +eps) with default eps = 0.1;
    # delta_inner = eps/2 (bodies separated, not tiled).
    assert strip.geometry.log_offsets[0] == pytest.approx(-0.1)
    assert strip.geometry.log_offsets[2] == pytest.approx(+0.1)
    assert strip.geometry.delta_inner == pytest.approx(0.05)
    assert strip.geometry.delta_outer == pytest.approx(0.1)


@given(_adapter_inputs())
@settings(max_examples=40, deadline=None)
def test_zeehbs_adapter_produces_valid_strip(
    inputs: tuple[float, float, float],
) -> None:
    """ZeehbsAdapter — asymmetric-wider geometry, strip invariants pass."""
    s_0, sigma_0, k_star = inputs
    adapter = ZeehbsAdapter()
    assert adapter.primitive_id == "zeehbs"
    assert adapter.comparability_proof == "normalized_score"
    strip = adapter(s_0=s_0, sigma_0=sigma_0, k_star=k_star)
    _assert_strip_invariants(strip)
    # Geometry: log_offsets = (-1.5·eps, 0, +1.5·eps) with default eps = 0.1.
    assert strip.geometry.log_offsets[0] == pytest.approx(-0.15)
    assert strip.geometry.log_offsets[2] == pytest.approx(+0.15)
    assert strip.geometry.delta_inner == pytest.approx(0.1)
    assert strip.geometry.delta_outer == pytest.approx(0.15)


def test_adapters_re_exported_from_package_root() -> None:
    """All four adapters + STRATEGY_COMPARISON_ANCHOR re-exported (acceptance §5)."""
    from simulations.saas_builder.cohort_5_strip import strategies

    assert hasattr(strategies, "ReverseIronCondorAdapter")
    assert hasattr(strategies, "LongStraddleAdapter")
    assert hasattr(strategies, "LongStrangleAdapter")
    assert hasattr(strategies, "ZeehbsAdapter")
    assert STRATEGY_COMPARISON_ANCHOR.startswith("scratch/2026-05-11")


def test_adapters_conform_to_strategy_adapter_protocol() -> None:
    """All four Task 2.2 adapters satisfy the StrategyAdapter Protocol.

    Verifies structural typing — adapters expose a ``__call__(s_0,
    sigma_0, k_star) -> IronCondorStrip`` surface matching the Protocol
    declared in ``strategies/types.py``. The Protocol is decorated with
    ``@runtime_checkable`` to enable ``isinstance`` validation.
    """
    for adapter in (
        ReverseIronCondorAdapter(),
        LongStraddleAdapter(),
        LongStrangleAdapter(),
        ZeehbsAdapter(),
    ):
        assert isinstance(adapter, StrategyAdapter)


def test_adapters_are_frozen_dataclasses() -> None:
    """Adapter attributes are read-only (frozen-dc invariant)."""
    for cls in (
        ReverseIronCondorAdapter,
        LongStraddleAdapter,
        LongStrangleAdapter,
        ZeehbsAdapter,
    ):
        a = cls()
        with pytest.raises((AttributeError, Exception)):
            a.primitive_id = "spoof"  # type: ignore[misc]
