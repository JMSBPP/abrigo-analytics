"""Tests for the stochastic-fx variant package.

Parent plan: docs/plans/2026-05-11-stochastic-fx-variant.md v0.2.
"""
import re

import numpy as np
import pytest
from hypothesis import given, strategies as st

from simulations.stochastic_fx import (
    CANONICAL_GBM,
    CANONICAL_MERTON,
    CANONICAL_OU,
    GBMParameters,
    InversionTestFailedError,
    InversionVerdict,
    JumpDiffusionParameters,
    MCBudgetExceededError,
    MomentMatchFailedError,
    OUParameters,
    PathEnsemble,
    SDEParameterError,
    StochasticFXError,
)

_AUDIT_BLOCK_REGEX_PY = re.compile(r"^[0-9a-f]{64}$")
_VALID_AUDIT_BLOCK = "0" * 64
_VALID_AUDIT_BLOCK_ALT = "a" * 64


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


# ─── PathEnsemble ────────────────────────────────────────────────────────────


def _valid_path_ensemble_kwargs(
    family_id: str = "gbm",
    n_paths: int = 3,
    n_steps_plus_1: int = 5,
) -> dict:
    """Construct a happy-path kwargs dict for PathEnsemble."""
    rng = np.random.default_rng(0)
    return {
        "family_id": family_id,
        "paths": rng.standard_normal((n_paths, n_steps_plus_1)),
        "sigma_t": rng.uniform(0.01, 1.0, size=n_paths),
        "canonical_params_json": '{"mu": 0.0}',
        "rng_seed": 42,
        "audit_block": _VALID_AUDIT_BLOCK,
    }


def test_path_ensemble_happy_path() -> None:
    """A well-formed PathEnsemble constructs without raising."""
    kwargs = _valid_path_ensemble_kwargs()
    ens = PathEnsemble(**kwargs)
    assert ens.family_id == "gbm"
    assert ens.paths.shape == (3, 5)
    assert ens.sigma_t.shape == (3,)
    assert ens.rng_seed == 42
    assert ens.audit_block == _VALID_AUDIT_BLOCK


@pytest.mark.parametrize("family_id", ["gbm", "ou", "merton"])
def test_path_ensemble_accepts_all_alphabet_families(family_id: str) -> None:
    """Each member of the closed alphabet {gbm, ou, merton} constructs cleanly."""
    PathEnsemble(**_valid_path_ensemble_kwargs(family_id=family_id))


@pytest.mark.parametrize("bad_id", ["GBM", "heston", "", "gbm "])
def test_path_ensemble_rejects_out_of_alphabet_family(bad_id: str) -> None:
    """family_id outside the closed alphabet is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["family_id"] = bad_id
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_1d_paths() -> None:
    """paths must be 2-D — a 1-D array is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["paths"] = np.zeros(10)
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_3d_paths() -> None:
    """paths must be 2-D — a 3-D array is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["paths"] = np.zeros((2, 3, 4))
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_2d_sigma_t() -> None:
    """sigma_t must be 1-D — a 2-D array is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["sigma_t"] = np.zeros((3, 2))
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_mismatched_sigma_t_length() -> None:
    """sigma_t length must equal paths.shape[0]."""
    kwargs = _valid_path_ensemble_kwargs(n_paths=3)
    kwargs["sigma_t"] = np.zeros(2)
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_non_finite_paths() -> None:
    """NaN inside the path matrix is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["paths"][0, 0] = np.nan
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_non_finite_sigma_t() -> None:
    """+infinity inside sigma_t is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["sigma_t"][0] = np.inf
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


@pytest.mark.parametrize("bad_block", [
    "",
    "ABCDEF" + "0" * 58,
    "0" * 63,
    "0" * 65,
    "z" * 64,
    "g" * 64,
    " " + "0" * 63,
])
def test_path_ensemble_rejects_bad_audit_block(bad_block: str) -> None:
    """audit_block must match ^[0-9a-f]{64}$."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["audit_block"] = bad_block
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_empty_canonical_params_json() -> None:
    """canonical_params_json must be non-empty."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["canonical_params_json"] = ""
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_negative_rng_seed() -> None:
    """rng_seed must be non-negative."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["rng_seed"] = -1
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_bool_rng_seed() -> None:
    """rng_seed must be a true int, not bool (bool is a subclass of int)."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["rng_seed"] = True
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


def test_path_ensemble_rejects_non_ndarray_paths() -> None:
    """paths must be a numpy.ndarray — a list is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["paths"] = [[0.0, 1.0], [2.0, 3.0]]
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


@given(
    family_id=st.sampled_from(["GBM", "Heston", "ou ", "", "Merton"]),
    n_paths=st.integers(min_value=1, max_value=5),
)
def test_path_ensemble_property_rejects_invalid_family(
    family_id: str, n_paths: int
) -> None:
    """Hypothesis: any out-of-alphabet family_id is rejected regardless of shape."""
    kwargs = _valid_path_ensemble_kwargs(n_paths=n_paths)
    kwargs["family_id"] = family_id
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


@given(
    audit_block=st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0,
        max_size=80,
    ).filter(lambda s: _AUDIT_BLOCK_REGEX_PY.fullmatch(s) is None),
)
def test_path_ensemble_property_rejects_invalid_audit_block(audit_block: str) -> None:
    """Hypothesis: any string that doesn't match the 64-char lowercase hex regex is rejected."""
    kwargs = _valid_path_ensemble_kwargs()
    kwargs["audit_block"] = audit_block
    with pytest.raises(SDEParameterError):
        PathEnsemble(**kwargs)


# ─── InversionVerdict ────────────────────────────────────────────────────────


def _valid_inversion_verdict_kwargs(
    family_id: str = "gbm",
    phase_a_pass: bool = True,
    phase_b_pass: bool = True,
    phase_c_pass: bool = True,
) -> dict:
    """Construct happy-path kwargs for InversionVerdict with consistent composite."""
    return {
        "family_id": family_id,
        "phase_a_pass": phase_a_pass,
        "phase_a_max_residual": 1e-9,
        "phase_b_pass": phase_b_pass,
        "phase_b_mean_rel_err": 0.01,
        "phase_b_var_rel_err": 0.02,
        "phase_c_pass": phase_c_pass,
        "phase_c_ks_pvalue": 0.5,
        "phase_c_n_paths": 1000,
        "composite_pass": phase_a_pass and phase_b_pass and phase_c_pass,
        "tex_anchor": "notes/stochastic_fx_tex/sigma_t_moments_gbm.tex",
        "audit_block": _VALID_AUDIT_BLOCK,
    }


def test_inversion_verdict_happy_path() -> None:
    """A well-formed all-pass InversionVerdict constructs cleanly."""
    v = InversionVerdict(**_valid_inversion_verdict_kwargs())
    assert v.composite_pass is True
    assert v.phase_c_n_paths == 1000


@pytest.mark.parametrize("family_id", ["gbm", "ou", "merton"])
def test_inversion_verdict_accepts_all_alphabet_families(family_id: str) -> None:
    """Each closed-alphabet family_id constructs cleanly."""
    InversionVerdict(**_valid_inversion_verdict_kwargs(family_id=family_id))


@pytest.mark.parametrize(
    "phase_a, phase_b, phase_c",
    [
        (True, True, True),
        (False, True, True),
        (True, False, True),
        (True, True, False),
        (False, False, False),
    ],
)
def test_inversion_verdict_composite_matches_and(
    phase_a: bool, phase_b: bool, phase_c: bool
) -> None:
    """composite_pass must equal the logical AND of the three phase flags."""
    kwargs = _valid_inversion_verdict_kwargs(
        phase_a_pass=phase_a, phase_b_pass=phase_b, phase_c_pass=phase_c
    )
    v = InversionVerdict(**kwargs)
    assert v.composite_pass == (phase_a and phase_b and phase_c)


def test_inversion_verdict_rejects_inconsistent_composite() -> None:
    """composite_pass=True with a failing phase is rejected."""
    kwargs = _valid_inversion_verdict_kwargs(phase_a_pass=False)
    kwargs["composite_pass"] = True
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_inconsistent_composite_false() -> None:
    """composite_pass=False with all phases passing is rejected."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["composite_pass"] = False
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


@pytest.mark.parametrize("bad_id", ["GBM", "heston", "", "merton "])
def test_inversion_verdict_rejects_out_of_alphabet_family(bad_id: str) -> None:
    """family_id outside the closed alphabet is rejected."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["family_id"] = bad_id
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_int_for_bool_phase_a() -> None:
    """phase_a_pass must be bool, not int."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_a_pass"] = 1
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_negative_max_residual() -> None:
    """phase_a_max_residual must be >= 0."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_a_max_residual"] = -1e-12
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_negative_mean_rel_err() -> None:
    """phase_b_mean_rel_err must be >= 0."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_b_mean_rel_err"] = -0.01
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_negative_var_rel_err() -> None:
    """phase_b_var_rel_err must be >= 0."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_b_var_rel_err"] = -0.01
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


@pytest.mark.parametrize("bad_p", [-0.1, 1.1, 2.0])
def test_inversion_verdict_rejects_out_of_unit_interval_ks_pvalue(bad_p: float) -> None:
    """phase_c_ks_pvalue must lie in [0.0, 1.0]."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_c_ks_pvalue"] = bad_p
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_negative_n_paths() -> None:
    """phase_c_n_paths must be >= 0."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_c_n_paths"] = -1
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_nan_residual() -> None:
    """phase_a_max_residual must be finite."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_a_max_residual"] = float("nan")
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_rejects_empty_tex_anchor() -> None:
    """tex_anchor must be non-empty."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["tex_anchor"] = ""
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


@pytest.mark.parametrize("bad_block", [
    "",
    "A" * 64,
    "0" * 63,
    "0" * 65,
    "z" * 64,
])
def test_inversion_verdict_rejects_bad_audit_block(bad_block: str) -> None:
    """audit_block must match ^[0-9a-f]{64}$."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["audit_block"] = bad_block
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


def test_inversion_verdict_accepts_valid_alt_audit_block() -> None:
    """A different valid 64-char lowercase hex audit_block also constructs cleanly."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["audit_block"] = _VALID_AUDIT_BLOCK_ALT
    v = InversionVerdict(**kwargs)
    assert v.audit_block == _VALID_AUDIT_BLOCK_ALT


@given(
    family_id=st.text(min_size=0, max_size=10).filter(
        lambda s: s not in {"gbm", "ou", "merton"}
    ),
)
def test_inversion_verdict_property_rejects_invalid_family(family_id: str) -> None:
    """Hypothesis: any out-of-alphabet family_id is rejected."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["family_id"] = family_id
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)


@given(
    phase_a=st.booleans(),
    phase_b=st.booleans(),
    phase_c=st.booleans(),
    declared_composite=st.booleans(),
)
def test_inversion_verdict_property_composite_consistency(
    phase_a: bool, phase_b: bool, phase_c: bool, declared_composite: bool
) -> None:
    """Hypothesis: composite_pass must equal AND of the three phase flags or construction fails."""
    kwargs = _valid_inversion_verdict_kwargs(
        phase_a_pass=phase_a, phase_b_pass=phase_b, phase_c_pass=phase_c
    )
    kwargs["composite_pass"] = declared_composite
    expected = phase_a and phase_b and phase_c
    if declared_composite == expected:
        v = InversionVerdict(**kwargs)
        assert v.composite_pass == expected
    else:
        with pytest.raises(SDEParameterError):
            InversionVerdict(**kwargs)


@given(
    p=st.floats(allow_nan=False, allow_infinity=False).filter(
        lambda x: not (0.0 <= x <= 1.0)
    ),
)
def test_inversion_verdict_property_rejects_invalid_ks_pvalue(p: float) -> None:
    """Hypothesis: any finite p outside [0, 1] is rejected."""
    kwargs = _valid_inversion_verdict_kwargs()
    kwargs["phase_c_ks_pvalue"] = p
    with pytest.raises(SDEParameterError):
        InversionVerdict(**kwargs)
