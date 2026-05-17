"""Tests for ``simulations.dev_ai_cost_v2.types`` — frozen-dc value containers.

Spec ref: docs/specs/2026-05-16-ai-cost-factor-model-design.md v0.2.1 §3.5.
Sibling spec: docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md
v0.1.3 CORRECTIONS-RR/-TT — adds ``uuid: str`` field on ``MessageRecord`` for
R6 pool canonicalization (tertiary sort key + dedupe disambiguation).
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import polars as pl
import pytest
from hypothesis import given

from simulations.dev_ai_cost_v2.types import (
    EXPECTED_PANEL_SCHEMA,
    DailyNotionalPanel,
    MessageRecord,
    TokensByCategory,
)


# ─── MessageRecord ────────────────────────────────────────────────────────────


def _valid_message_kwargs() -> dict:
    return dict(
        ts=datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc),
        model="claude-sonnet-4-5",
        input_tok=100,
        output_tok=50,
        cache_create_5m=0,
        cache_create_1h=0,
        cache_read=0,
        cost_usd_notional=Decimal("0.0015"),
        session_id="sess-1",
        request_id=None,
        is_error=False,
        uuid="msg-uuid-abc-123",  # R6 v0.1.3 CORRECTIONS-RR/-TT
    )


def test_message_record_constructs_with_valid_fields() -> None:
    rec = MessageRecord(**_valid_message_kwargs())
    assert rec.model == "claude-sonnet-4-5"
    assert rec.uuid == "msg-uuid-abc-123"
    assert rec.input_tok == 100
    assert rec.cost_usd_notional == Decimal("0.0015")


def test_message_record_rejects_negative_tokens() -> None:
    kwargs = _valid_message_kwargs() | {"input_tok": -1}
    with pytest.raises(ValueError, match="input_tok"):
        MessageRecord(**kwargs)


def test_message_record_rejects_negative_output_tok() -> None:
    kwargs = _valid_message_kwargs() | {"output_tok": -5}
    with pytest.raises(ValueError, match="output_tok"):
        MessageRecord(**kwargs)


def test_message_record_rejects_negative_cache_create_5m() -> None:
    kwargs = _valid_message_kwargs() | {"cache_create_5m": -1}
    with pytest.raises(ValueError, match="cache_create_5m"):
        MessageRecord(**kwargs)


def test_message_record_rejects_negative_cache_create_1h() -> None:
    kwargs = _valid_message_kwargs() | {"cache_create_1h": -1}
    with pytest.raises(ValueError, match="cache_create_1h"):
        MessageRecord(**kwargs)


def test_message_record_rejects_negative_cache_read() -> None:
    kwargs = _valid_message_kwargs() | {"cache_read": -1}
    with pytest.raises(ValueError, match="cache_read"):
        MessageRecord(**kwargs)


def test_message_record_rejects_negative_cost() -> None:
    kwargs = _valid_message_kwargs() | {"cost_usd_notional": Decimal("-0.01")}
    with pytest.raises(ValueError, match="cost_usd_notional"):
        MessageRecord(**kwargs)


def test_message_record_rejects_naive_datetime() -> None:
    kwargs = _valid_message_kwargs() | {"ts": datetime(2026, 5, 1, 12, 0)}  # tz-naive
    with pytest.raises(ValueError, match="timezone-aware UTC"):
        MessageRecord(**kwargs)


def test_message_record_rejects_non_utc_timezone() -> None:
    from datetime import timedelta
    kwargs = _valid_message_kwargs() | {
        "ts": datetime(2026, 5, 1, 12, 0, tzinfo=timezone(timedelta(hours=-5)))
    }
    with pytest.raises(ValueError, match="UTC"):
        MessageRecord(**kwargs)


def test_message_record_rejects_empty_uuid() -> None:
    """R6 canonicalization sorts by uuid; empty string is ambiguous."""
    kwargs = _valid_message_kwargs() | {"uuid": ""}
    with pytest.raises(ValueError, match="uuid"):
        MessageRecord(**kwargs)


def test_message_record_is_frozen() -> None:
    rec = MessageRecord(**_valid_message_kwargs())
    with pytest.raises((AttributeError, Exception)):
        rec.model = "other"  # type: ignore[misc]


def test_message_record_request_id_can_be_none() -> None:
    """Legacy Claude Code pre-2.0 emits request_id=None; JSONLReader warns
    but does not error. Type contract permits None."""
    rec = MessageRecord(**(_valid_message_kwargs() | {"request_id": None}))
    assert rec.request_id is None


# ─── TokensByCategory ─────────────────────────────────────────────────────────


def test_tokens_by_category_constructs() -> None:
    t = TokensByCategory(
        input=100, output=50, cache_create_5m=10, cache_create_1h=5, cache_read=200
    )
    assert t.input == 100
    assert t.cache_read == 200


def test_tokens_by_category_zero_is_valid() -> None:
    t = TokensByCategory(input=0, output=0, cache_create_5m=0, cache_create_1h=0, cache_read=0)
    assert t.input == 0


def test_tokens_by_category_rejects_negative_input() -> None:
    with pytest.raises(ValueError, match="input"):
        TokensByCategory(input=-1, output=0, cache_create_5m=0, cache_create_1h=0, cache_read=0)


def test_tokens_by_category_rejects_negative_cache_read() -> None:
    with pytest.raises(ValueError, match="cache_read"):
        TokensByCategory(input=0, output=0, cache_create_5m=0, cache_create_1h=0, cache_read=-1)


# ─── DailyNotionalPanel ───────────────────────────────────────────────────────


def _valid_panel_df() -> pl.DataFrame:
    """Build a minimal one-row DataFrame matching EXPECTED_PANEL_SCHEMA."""
    return pl.DataFrame(
        {
            "date_utc": [datetime(2026, 5, 1).date()],
            "notional_cost_usd": [Decimal("1.50")],
            "notional_cost_cop": [Decimal("6300.00")],
            "trm_cop_per_usd": [Decimal("4200.00")],
            "input_tok": [1000],
            "output_tok": [500],
            "cache_create_5m": [0],
            "cache_create_1h": [0],
            "cache_read": [0],
            "n_messages": [5],
        },
        schema={
            "date_utc": pl.Date,
            "notional_cost_usd": pl.Decimal(precision=18, scale=8),
            "notional_cost_cop": pl.Decimal(precision=18, scale=8),
            "trm_cop_per_usd": pl.Decimal(precision=18, scale=8),
            "input_tok": pl.Int64,
            "output_tok": pl.Int64,
            "cache_create_5m": pl.Int64,
            "cache_create_1h": pl.Int64,
            "cache_read": pl.Int64,
            "n_messages": pl.Int64,
        },
    )


def test_daily_notional_panel_constructs() -> None:
    p = DailyNotionalPanel(
        df=_valid_panel_df(), dropped_rows_count=0, dropped_error_count=0
    )
    assert p.df.height == 1
    assert p.dropped_rows_count == 0


def test_daily_notional_panel_rejects_missing_column() -> None:
    df = _valid_panel_df().drop("trm_cop_per_usd")
    with pytest.raises(ValueError, match="missing"):
        DailyNotionalPanel(df=df, dropped_rows_count=0, dropped_error_count=0)


def test_daily_notional_panel_rejects_extra_column() -> None:
    df = _valid_panel_df().with_columns(pl.lit(1).alias("rogue_col"))
    with pytest.raises(ValueError, match="extra"):
        DailyNotionalPanel(df=df, dropped_rows_count=0, dropped_error_count=0)


def test_daily_notional_panel_rejects_wrong_dtype() -> None:
    df = _valid_panel_df().with_columns(pl.col("input_tok").cast(pl.Float64))
    with pytest.raises(ValueError, match="input_tok"):
        DailyNotionalPanel(df=df, dropped_rows_count=0, dropped_error_count=0)


def test_daily_notional_panel_rejects_negative_dropped_counts() -> None:
    with pytest.raises(ValueError, match="dropped"):
        DailyNotionalPanel(df=_valid_panel_df(), dropped_rows_count=-1, dropped_error_count=0)


def test_daily_notional_panel_rejects_negative_error_counts() -> None:
    with pytest.raises(ValueError, match="dropped"):
        DailyNotionalPanel(df=_valid_panel_df(), dropped_rows_count=0, dropped_error_count=-1)


def test_expected_panel_schema_has_ten_columns() -> None:
    """Pin schema width — additions require explicit spec change."""
    assert len(EXPECTED_PANEL_SCHEMA) == 10


# ─── Hypothesis property test ─────────────────────────────────────────────────


from simulations.tests.strategies import message_records  # noqa: E402


@given(rec=message_records())
def test_message_record_post_init_invariants(rec: MessageRecord) -> None:
    """Every successfully-constructed MessageRecord must satisfy __post_init__ invariants."""
    assert rec.input_tok >= 0
    assert rec.output_tok >= 0
    assert rec.cache_create_5m >= 0
    assert rec.cache_create_1h >= 0
    assert rec.cache_read >= 0
    assert rec.cost_usd_notional >= 0
    assert rec.uuid != ""
    assert rec.ts.tzinfo is not None
    assert rec.ts.utcoffset() == timezone.utc.utcoffset(rec.ts)
