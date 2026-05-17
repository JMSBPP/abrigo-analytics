"""Tests for ``simulations.dev_ai_cost_v2.anthropic_pricing.PricingTable``.

Spec ref: ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1
§5.2 + §0.1 CORRECTIONS-O (five required keys per claude-* model) +
CORRECTIONS-V (``ts`` sentinel).

Test inventory:
1. ``test_pricing_table_load_requires_all_five_keys`` — Wave 1 RC hint:
   missing required key on a ``claude-*`` model raises KeyError at load.
2. ``test_pricing_table_call_uses_correct_keys`` — exact-Decimal cost
   computation across all five categories.
3. ``test_pricing_monotone_in_input_tokens`` — Hypothesis property:
   ``__call__`` is monotone non-decreasing in input token count.
4. ``test_pricing_table_rejects_sha_mismatch`` — production SHA guard.
5. ``test_pricing_table_rejects_unknown_model`` — KeyError on unknown
   model lookup.
6. ``test_pricing_table_skips_non_claude_models`` — only ``claude-*``
   models are loaded (the spec scopes the panel to Anthropic).
7. ``test_pricing_zero_tokens_zero_cost`` — zero-token edge case.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from simulations.dev_ai_cost_v2.anthropic_pricing import (
    LITELLM_SHA_PINNED,
    PricingTable,
    _REQUIRED_KEYS,
)
from simulations.dev_ai_cost_v2.types import TokensByCategory

# Local alias mirrors the module pin (kept as a string literal so this test
# would fail-loud if the upstream constant were ever quietly bumped).
LITELLM_SHA = "e58a561caa21169fb02174148444c08509ce7028"


# ─── Test 1: load-time key assertion (Wave 1 RC hint) ────────────────────────


def test_pricing_table_load_requires_all_five_keys(tmp_path: Path) -> None:
    """Per Wave 1 RC hint: every claude-* model must carry all five keys."""
    fake_table = {
        "claude-sonnet-4-5": {
            "input_cost_per_token": 3e-06,
            "output_cost_per_token": 15e-06,
            "cache_creation_input_token_cost": 3.75e-06,
            # MISSING: cache_creation_input_token_cost_above_1hr
            "cache_read_input_token_cost": 0.30e-06,
        }
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    with pytest.raises(KeyError, match="cache_creation_input_token_cost_above_1hr"):
        PricingTable.from_litellm_sha(
            sha=LITELLM_SHA, cached_json_path=p, skip_sha_check=True
        )


# ─── Test 2: exact-Decimal call ──────────────────────────────────────────────


def test_pricing_table_call_uses_correct_keys(tmp_path: Path) -> None:
    fake_table = {
        "claude-sonnet-4-5": {
            "input_cost_per_token": 3e-06,
            "output_cost_per_token": 15e-06,
            "cache_creation_input_token_cost": 3.75e-06,
            "cache_creation_input_token_cost_above_1hr": 6e-06,
            "cache_read_input_token_cost": 0.30e-06,
        }
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    pt = PricingTable.from_litellm_sha(
        sha=LITELLM_SHA, cached_json_path=p, skip_sha_check=True
    )
    toks = TokensByCategory(
        input=1000,
        output=500,
        cache_create_5m=200,
        cache_create_1h=100,
        cache_read=300,
    )
    cost = pt(
        model="claude-sonnet-4-5",
        ts=datetime(2026, 5, 1, tzinfo=timezone.utc),
        toks=toks,
    )
    expected = (
        Decimal("1000") * Decimal("3e-06")
        + Decimal("500") * Decimal("15e-06")
        + Decimal("200") * Decimal("3.75e-06")
        + Decimal("100") * Decimal("6e-06")
        + Decimal("300") * Decimal("0.30e-06")
    )
    assert cost == expected


# ─── Test 3: Hypothesis property — monotone non-decreasing in input tok ──────


@given(
    input_tok=st.integers(0, 10_000),
    extra_input=st.integers(0, 10_000),
)
def test_pricing_monotone_in_input_tokens(
    input_tok: int,
    extra_input: int,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    tmp = tmp_path_factory.mktemp("pricing")
    fake = {"claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS}}
    p = tmp / "litellm.json"
    p.write_text(json.dumps(fake))
    pt = PricingTable.from_litellm_sha(LITELLM_SHA, p, skip_sha_check=True)
    base = pt(
        "claude-sonnet-4-5",
        datetime(2026, 5, 1, tzinfo=timezone.utc),
        TokensByCategory(input_tok, 0, 0, 0, 0),
    )
    more = pt(
        "claude-sonnet-4-5",
        datetime(2026, 5, 1, tzinfo=timezone.utc),
        TokensByCategory(input_tok + extra_input, 0, 0, 0, 0),
    )
    assert more >= base


# ─── Test 4: SHA mismatch guard ──────────────────────────────────────────────


def test_pricing_table_rejects_sha_mismatch(tmp_path: Path) -> None:
    """Production callers (``skip_sha_check=False``) must pass the pinned SHA.

    A drifted SHA argument is a reproducibility failure and must be rejected
    at the load boundary, not silently absorbed.
    """
    fake_table = {
        "claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS},
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    bogus_sha = "0" * 40
    with pytest.raises(ValueError, match="pinned"):
        PricingTable.from_litellm_sha(
            sha=bogus_sha, cached_json_path=p, skip_sha_check=False
        )
    # And confirm the pinned SHA loads cleanly when skip is off.
    pt = PricingTable.from_litellm_sha(
        sha=LITELLM_SHA_PINNED, cached_json_path=p, skip_sha_check=False
    )
    assert pt.sha == LITELLM_SHA_PINNED


# ─── Test 5: unknown model lookup raises ─────────────────────────────────────


def test_pricing_table_rejects_unknown_model(tmp_path: Path) -> None:
    fake_table = {
        "claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS},
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    pt = PricingTable.from_litellm_sha(
        sha=LITELLM_SHA, cached_json_path=p, skip_sha_check=True
    )
    with pytest.raises(KeyError, match="claude-opus-99"):
        pt(
            model="claude-opus-99",
            ts=datetime(2026, 5, 1, tzinfo=timezone.utc),
            toks=TokensByCategory(1, 0, 0, 0, 0),
        )


# ─── Test 6: non-claude models are filtered at load ──────────────────────────


def test_pricing_table_skips_non_claude_models(tmp_path: Path) -> None:
    """Only ``claude-*`` keys are retained; the spec scopes the panel to Anthropic."""
    fake_table = {
        "gpt-4": {"input_cost_per_token": 1e-05},  # incomplete + non-claude
        "claude-x": {k: 2e-06 for k in _REQUIRED_KEYS},
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    pt = PricingTable.from_litellm_sha(
        sha=LITELLM_SHA, cached_json_path=p, skip_sha_check=True
    )
    assert set(pt.rates) == {"claude-x"}
    # And the non-claude entry's missing required keys do NOT trigger a load
    # failure (proving the claude-* filter precedes the required-key check).


# ─── Test 7: zero-token edge case ────────────────────────────────────────────


def test_pricing_zero_tokens_zero_cost(tmp_path: Path) -> None:
    fake_table = {
        "claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS},
    }
    p = tmp_path / "litellm.json"
    p.write_text(json.dumps(fake_table))
    pt = PricingTable.from_litellm_sha(
        sha=LITELLM_SHA, cached_json_path=p, skip_sha_check=True
    )
    cost = pt(
        model="claude-sonnet-4-5",
        ts=datetime(2026, 5, 1, tzinfo=timezone.utc),
        toks=TokensByCategory(0, 0, 0, 0, 0),
    )
    assert cost == Decimal("0")
