"""Tests for ``simulations.dev_ai_cost_v2.panel_builder.build_daily_panel``.

Spec ref: ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1
§3.3 (daily aggregation), §3.5 (panel contract), §0.1 CORRECTIONS-V
(``is_error`` dropped, UTC half-open), CORRECTIONS-M (forward-fill forbidden).

Sibling spec ref: ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md``
v0.1.3 CORRECTIONS-RR/-TT — ``MessageRecord.uuid`` required. The ``_rec``
helper assigns a unique ``u-{day}-{hour}-{suffix}`` uuid per record so the
type-tier validator (``MessageRecord.__post_init__``) accepts every fixture.

Test inventory:
1. ``test_reconciliation_exact_decimal`` — sum of per-message
   ``cost_usd_notional`` over non-error rows equals panel
   ``notional_cost_usd`` EXACTLY under ``Decimal``.
2. ``test_is_error_rows_dropped_from_cost_counted_separately`` —
   ``is_error=True`` rows do not contribute to ``n_messages`` and are
   surfaced via ``dropped_error_count`` (CORRECTIONS-V).
3. ``test_forward_fill_forbidden_property`` — no output day lacks source
   rows on EITHER side (records OR TRM) (§6 / CORRECTIONS-M).
4. ``test_weekends_dropped`` — Sat/Sun records and TRM rows are dropped
   on both sides; weekend records contribute to ``dropped_rows_count``.
5. ``test_double_iteration_equivalence`` — re-iterating ``records``
   produces an identical panel (CR FLAG A closure).
6. ``test_polars_weekday_calendar_pin`` — pins the polars ``dt.weekday()``
   convention (Mon=1..Sun=7) against known calendar dates so a future
   polars-version bump that flipped the ordinal would fail loud.
7. ``test_python_weekday_calendar_pin`` — pins the python
   ``datetime.weekday()`` convention (Mon=0..Sun=6) symmetrically.
8. ``test_no_records_only_days_in_output`` — Hypothesis property: every
   output ``date_utc`` appears in BOTH the records side AND the TRM side
   (forward-fill forbidden, strengthened from Test 3).
9. ``test_empty_records_yields_empty_panel`` — edge case: no records →
   empty panel with valid schema (no KeyError, no schema drift).
10. ``test_trm_only_days_not_in_output`` — explicit cousin to Test 3:
    TRM-only days (no message records that day) must not appear.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import polars as pl
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from simulations.dev_ai_cost_v2.anthropic_pricing import (
    LITELLM_SHA_PINNED,
    PricingTable,
    _REQUIRED_KEYS,
)
from simulations.dev_ai_cost_v2.panel_builder import build_daily_panel
from simulations.dev_ai_cost_v2.types import MessageRecord


# ─── Fixtures ────────────────────────────────────────────────────────────────


def _toy_pricing(tmp_path: Path) -> PricingTable:
    fake = {"claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS}}
    p = tmp_path / "lite.json"
    p.write_text(json.dumps(fake))
    return PricingTable.from_litellm_sha(
        LITELLM_SHA_PINNED, p, skip_sha_check=True
    )


def _toy_trm() -> pl.DataFrame:
    """5 weekdays 2026-05-04..2026-05-08 (Mon-Fri)."""
    return pl.DataFrame(
        {
            "date": [date(2026, 5, d) for d in (4, 5, 6, 7, 8)],
            "trm_cop_per_usd": [
                Decimal("4100"),
                Decimal("4105"),
                Decimal("4090"),
                Decimal("4110"),
                Decimal("4120"),
            ],
        }
    )


def _rec(
    day: int,
    hour: int = 12,
    *,
    is_error: bool = False,
    uuid_suffix: str = "",
) -> MessageRecord:
    """Build a ``MessageRecord`` fixture with a unique non-empty uuid.

    The ``uuid_suffix`` parameter exists to disambiguate multiple records
    on the same (day, hour) in the same test — the upstream
    ``MessageRecord.__post_init__`` only requires non-empty uuids (R6
    v0.1.3 CORRECTIONS-RR/-TT), but distinct uuids per record keep the
    fixtures honest with respect to the R6 pool canonicalization invariant.
    """
    return MessageRecord(
        ts=datetime(2026, 5, day, hour, tzinfo=timezone.utc),
        model="claude-sonnet-4-5",
        input_tok=1000,
        output_tok=500,
        cache_create_5m=0,
        cache_create_1h=0,
        cache_read=0,
        cost_usd_notional=Decimal("0.0015"),
        session_id="s",
        request_id="r",
        is_error=is_error,
        uuid=f"u-{day}-{hour}-{uuid_suffix}",
    )


# ─── Test 1: reconciliation under exact Decimal ──────────────────────────────


def test_reconciliation_exact_decimal(tmp_path: Path) -> None:
    pricing = _toy_pricing(tmp_path)
    records = [
        _rec(4, uuid_suffix="a"),
        _rec(5, uuid_suffix="a"),
        _rec(5, uuid_suffix="b"),
    ]
    panel = build_daily_panel(records, pricing, _toy_trm())
    raw_total = sum(
        (r.cost_usd_notional for r in records if not r.is_error),
        Decimal("0"),
    )
    panel_total = panel.df["notional_cost_usd"].sum()
    # polars Decimal sum returns ``Decimal`` directly — equality is exact.
    assert panel_total == raw_total
    # Belt-and-suspenders: round-trip through str (preserves Decimal scale).
    assert Decimal(str(panel_total)) == raw_total


# ─── Test 2: is_error dropped from cost, counted separately ──────────────────


def test_is_error_rows_dropped_from_cost_counted_separately(
    tmp_path: Path,
) -> None:
    pricing = _toy_pricing(tmp_path)
    records = [
        _rec(4, uuid_suffix="ok"),
        _rec(4, is_error=True, uuid_suffix="err"),
        _rec(5, uuid_suffix="ok"),
    ]
    panel = build_daily_panel(records, pricing, _toy_trm())
    assert panel.dropped_error_count == 1
    # 2026-05-04 should reflect only 1 message (the error is excluded).
    may4 = panel.df.filter(pl.col("date_utc") == date(2026, 5, 4))
    assert may4["n_messages"].item() == 1
    # The error row's cost must NOT appear in the panel cost column.
    assert may4["notional_cost_usd"].item() == Decimal("0.0015")


# ─── Test 3: forward-fill forbidden (records side gaps) ──────────────────────


def test_forward_fill_forbidden_property(tmp_path: Path) -> None:
    """No output day should lack source rows on EITHER side (records OR TRM)."""
    pricing = _toy_pricing(tmp_path)
    # Records on May 5 only; TRM has May 4..8. May 4, 6, 7, 8 must NOT appear.
    records = [_rec(5, uuid_suffix="solo")]
    panel = build_daily_panel(records, pricing, _toy_trm())
    out_dates = set(panel.df["date_utc"].to_list())
    assert out_dates == {date(2026, 5, 5)}


# ─── Test 4: weekends dropped on both sides ──────────────────────────────────


def test_weekends_dropped(tmp_path: Path) -> None:
    pricing = _toy_pricing(tmp_path)
    # 2026-05-02 = Saturday, 2026-05-03 = Sunday, 2026-05-04 = Monday.
    records = [
        _rec(2, uuid_suffix="sat"),
        _rec(3, uuid_suffix="sun"),
        _rec(4, uuid_suffix="mon"),
    ]
    # Extend TRM to include weekends (will be filtered).
    trm = pl.DataFrame(
        {
            "date": [date(2026, 5, d) for d in (2, 3, 4)],
            "trm_cop_per_usd": [
                Decimal("4100"),
                Decimal("4100"),
                Decimal("4100"),
            ],
        }
    )
    panel = build_daily_panel(records, pricing, trm)
    assert set(panel.df["date_utc"].to_list()) == {date(2026, 5, 4)}
    # 2 weekend records (records side) + 2 weekend TRM rows = ≥ 4 dropped.
    assert panel.dropped_rows_count >= 2  # at minimum, the 2 weekend records.


# ─── Test 5: double iteration equivalence (Sequence contract) ────────────────


def test_double_iteration_equivalence(tmp_path: Path) -> None:
    """records is a Sequence — building twice must yield identical panels."""
    pricing = _toy_pricing(tmp_path)
    records: list[MessageRecord] = [
        _rec(4, uuid_suffix="a"),
        _rec(5, uuid_suffix="b"),
    ]
    p1 = build_daily_panel(records, pricing, _toy_trm())
    p2 = build_daily_panel(records, pricing, _toy_trm())
    assert p1.df.equals(p2.df)
    assert p1.dropped_rows_count == p2.dropped_rows_count
    assert p1.dropped_error_count == p2.dropped_error_count


# ─── Test 6: polars weekday calendar pin ─────────────────────────────────────


def test_polars_weekday_calendar_pin() -> None:
    """polars ``dt.weekday()`` is Mon=1..Sun=7 on the active polars pin.

    The panel_builder's TRM-side filter uses ``<= 5`` (keep Mon-Fri); if a
    polars version bump flipped the ordinal to Mon=0..Sun=6, this test
    would fail loud and the filter would need to be updated to ``< 5``
    (matching the python-side convention).
    """
    # 2026-05-04 = Monday, 2026-05-08 = Friday,
    # 2026-05-02 = Saturday, 2026-05-03 = Sunday.
    s = pl.Series([date(2026, 5, 4), date(2026, 5, 8), date(2026, 5, 2), date(2026, 5, 3)])
    assert s.dt.weekday().to_list() == [1, 5, 6, 7]


# ─── Test 7: python weekday calendar pin ─────────────────────────────────────


def test_python_weekday_calendar_pin() -> None:
    """python ``datetime.weekday()`` is Mon=0..Sun=6.

    The panel_builder's records-side filter uses ``< 5`` (keep Mon-Fri).
    Pinning this prevents accidentally treating polars and python ordinals
    as interchangeable.
    """
    assert datetime(2026, 5, 4).weekday() == 0  # Mon
    assert datetime(2026, 5, 8).weekday() == 4  # Fri
    assert datetime(2026, 5, 2).weekday() == 5  # Sat
    assert datetime(2026, 5, 3).weekday() == 6  # Sun


# ─── Test 8: Hypothesis property — no records-only days in output ────────────


@given(
    # Pick a non-empty subset of weekdays {Mon..Fri} = days {4,5,6,7,8} to
    # contain records.
    record_days=st.lists(
        st.sampled_from([4, 5, 6, 7, 8]),
        min_size=1,
        max_size=10,
    ),
    # Pick a non-empty subset of those same weekdays for the TRM panel.
    trm_days=st.lists(
        st.sampled_from([4, 5, 6, 7, 8]),
        min_size=1,
        max_size=5,
        unique=True,
    ),
)
@settings(max_examples=40, deadline=None)
def test_no_records_only_days_in_output(
    record_days: list[int],
    trm_days: list[int],
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    """Every output ``date_utc`` must appear on BOTH the records and TRM sides.

    Strengthens Test 3: across many random (records-days, trm-days) splits,
    no day appears in the output unless it has a source row on BOTH sides.
    This pins the forward-fill-forbidden contract symmetrically.
    """
    tmp_path = tmp_path_factory.mktemp("toy_pricing")
    pricing = _toy_pricing(tmp_path)

    records = [
        _rec(d, uuid_suffix=f"i{i}") for i, d in enumerate(record_days)
    ]
    trm = pl.DataFrame(
        {
            "date": [date(2026, 5, d) for d in sorted(set(trm_days))],
            "trm_cop_per_usd": [
                Decimal("4100") for _ in range(len(set(trm_days)))
            ],
        }
    )
    panel = build_daily_panel(records, pricing, trm)

    out_dates = set(panel.df["date_utc"].to_list())
    record_date_set = {date(2026, 5, d) for d in record_days}
    trm_date_set = {date(2026, 5, d) for d in trm_days}

    # Forward-fill-forbidden invariant: output ⊆ (records ∩ trm).
    assert out_dates <= (record_date_set & trm_date_set), (
        f"Forward-fill detected: out_dates={out_dates}, "
        f"records={record_date_set}, trm={trm_date_set}"
    )
    # And exactly equal to the intersection (no spurious drops on weekdays).
    assert out_dates == (record_date_set & trm_date_set)


# ─── Test 9: empty records edge case ─────────────────────────────────────────


def test_empty_records_yields_empty_panel(tmp_path: Path) -> None:
    """Zero records must not raise — empty panel with valid schema."""
    pricing = _toy_pricing(tmp_path)
    panel = build_daily_panel([], pricing, _toy_trm())
    assert panel.df.height == 0
    assert panel.dropped_error_count == 0
    # All TRM weekday rows go unjoined; weekend TRM rows = 0 (5 weekdays in fixture).
    # dropped_rows_count is the sum of: weekend records (0) + weekend trm (0) +
    # left-join misses (0 — daily is empty, so join loss is 0).
    assert panel.dropped_rows_count == 0
    # Schema validity is enforced by DailyNotionalPanel.__post_init__; reaching
    # this point at all means the schema matched EXPECTED_PANEL_SCHEMA.


# ─── Test 10: TRM-only days not in output ────────────────────────────────────


def test_trm_only_days_not_in_output(tmp_path: Path) -> None:
    """TRM has 5 weekdays; records only on May 4. Days 5..8 must not appear."""
    pricing = _toy_pricing(tmp_path)
    records = [_rec(4, uuid_suffix="only")]
    panel = build_daily_panel(records, pricing, _toy_trm())
    out_dates = set(panel.df["date_utc"].to_list())
    assert out_dates == {date(2026, 5, 4)}
    assert date(2026, 5, 5) not in out_dates
    assert date(2026, 5, 8) not in out_dates
