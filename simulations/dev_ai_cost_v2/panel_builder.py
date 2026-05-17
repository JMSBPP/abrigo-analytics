"""modules-tier pure function: per-message records → ``DailyNotionalPanel``.

Spec ref: ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1
§3.3 (daily aggregation), §3.5 (panel contract), §0.1 CORRECTIONS-V
(``is_error`` dropped, UTC half-open), CORRECTIONS-M (forward-fill forbidden).

Tier rule: ``modules/`` may import ``types/`` (and the sibling pure-callable
``anthropic_pricing``) but NOT ``utils/`` nor ``_errors``. This function is
pure: no IO, no mutation of inputs, no module-level state.

Weekday-filter semantics
------------------------
``polars`` 1.40 returns ``dt.weekday()`` as Mon=1..Sun=7 (ISO-8601 ordinal),
whereas the stdlib ``datetime.weekday()`` returns Mon=0..Sun=6. These two
conventions are NOT interchangeable; the filter constants below are different
on each side of the join on purpose:

    * python record side: ``< 5`` excludes Sat=5, Sun=6 (correct: keep Mon-Fri).
    * polars TRM side:    ``<= 5`` excludes Sat=6, Sun=7 (correct: keep Mon-Fri).

A unit test fixes both conventions against known calendar dates to prevent
silent regression on a polars version bump.

Decimal exactness
-----------------
Per spec §3.5, all monetary arithmetic is exact ``Decimal``. The per-message
``cost_usd`` column is constructed from ``Decimal`` values produced upstream
by ``PricingTable`` (cached on ``MessageRecord.cost_usd_notional``); polars
preserves ``Decimal`` dtype through ``group_by`` sums and ``with_columns``
multiplications. The reconciliation property test pins this exactness.
"""
from __future__ import annotations

from collections.abc import Sequence

import polars as pl

from simulations.dev_ai_cost_v2.anthropic_pricing import PricingTable
from simulations.dev_ai_cost_v2.types import (
    EXPECTED_PANEL_SCHEMA,
    DailyNotionalPanel,
    MessageRecord,
)


# ─── Per-message empty-frame schema ──────────────────────────────────────────
#
# Schema for the per-message DataFrame when ``records`` is empty (or after
# ``is_error`` filtering leaves no rows). Keeping this constant ensures the
# downstream ``group_by``/``join`` pipeline is dtype-stable regardless of
# input cardinality.

_MSG_FRAME_SCHEMA: dict[str, pl.DataType] = {
    "date_utc": pl.Date,
    "weekday": pl.Int8,
    "cost_usd": pl.Decimal,
    "input_tok": pl.Int64,
    "output_tok": pl.Int64,
    "cache_create_5m": pl.Int64,
    "cache_create_1h": pl.Int64,
    "cache_read": pl.Int64,
}


def build_daily_panel(
    records: Sequence[MessageRecord],
    pricing: PricingTable,
    trm_panel: pl.DataFrame,
) -> DailyNotionalPanel:
    """Aggregate per-message records to a daily UTC panel joined with TRM.

    Contract:
        * ``is_error=True`` rows are DROPPED from cost aggregation; their
          count is surfaced as ``DailyNotionalPanel.dropped_error_count``
          (spec CORRECTIONS-V).
        * Weekends (Sat/Sun) are dropped on BOTH sides before the inner
          join; their combined count is included in
          ``DailyNotionalPanel.dropped_rows_count`` (spec §3.5).
        * Forward-fill is FORBIDDEN: a UTC date that lacks a source row on
          EITHER side (no records that day OR no TRM observation that day)
          does NOT appear in the output (spec §6 threat / CORRECTIONS-M).
          A property test pins this contract.
        * Re-iterating ``records`` produces an identical panel (the
          ``Sequence`` type hint exists precisely to guarantee multi-pass
          iteration; ``Iterator`` would be exhausted after the first pass).
        * All arithmetic is exact ``Decimal`` — sums in ``group_by`` and
          the USD→COP multiplication in ``with_columns`` preserve dtype.

    Args:
        records: per-message records produced by ``JSONLReader``. MUST be
            a ``Sequence`` (re-iterable); ``Iterator`` is rejected by type
            system (CR FLAG A closure).
        pricing: ``PricingTable`` — accepted for signature parity with the
            downstream CLI orchestrator. Per spec §3.5, ``cost_usd_notional``
            is pre-computed by ``JSONLReader`` at parse time using this same
            table, so the cost column is already finalized on every
            ``MessageRecord``. The argument is retained so the CLI can pass
            a single ``PricingTable`` instance through both the reader and
            the aggregator (and so a future spec revision permitting late
            re-pricing has a hook).
        trm_panel: daily Banrep TRM panel with columns ``date`` (``pl.Date``)
            and ``trm_cop_per_usd`` (``pl.Decimal``). Both weekday and
            weekend rows are accepted; weekends are filtered internally.

    Returns:
        ``DailyNotionalPanel`` with ``df`` matching ``EXPECTED_PANEL_SCHEMA``
        column-for-column and dtype-for-dtype. ``dropped_rows_count`` counts
        weekend records dropped + weekend TRM rows dropped + weekday records
        whose date had no matching TRM observation (and vice versa) under
        the inner join. ``dropped_error_count`` counts ``is_error=True``
        rows dropped pre-aggregation.

    Raises:
        ValueError: propagated from ``DailyNotionalPanel.__post_init__`` if
            the final DataFrame schema diverges from ``EXPECTED_PANEL_SCHEMA``
            (a defensive guard against future polars dtype regressions; the
            implementation should make this unreachable on the supported
            polars pin).

    Errors from external state:
        None. This function is pure: no IO, no module-level mutation, no
        global clocks. ``trm_panel`` is a polars DataFrame whose schema is
        treated as input — schema errors on the TRM side surface as
        downstream ``DailyNotionalPanel`` schema-validation errors at the
        boundary, not as silent corruptions.

    Silenced errors:
        None. Dropped rows (weekends, ``is_error``, inner-join misses) are
        accounted for explicitly via ``dropped_rows_count`` and
        ``dropped_error_count``; they are not silent.
    """
    # ── Phase 1: split errors from kept rows ──────────────────────────────
    dropped_error: int = sum(1 for r in records if r.is_error)
    kept: list[MessageRecord] = [r for r in records if not r.is_error]

    # ── Phase 2: build per-message frame (dtype-stable on empty) ─────────
    # ``datetime.weekday()`` returns Mon=0..Sun=6 (Python stdlib semantics).
    # The `< 5` filter below excludes Sat=5 and Sun=6 — DIFFERENT from the
    # polars-side filter below (Mon=1..Sun=7), where Sat=6 and Sun=7 require
    # `<= 5`. See module docstring.
    if kept:
        rows = [
            {
                "date_utc": r.ts.date(),
                "weekday": r.ts.weekday(),
                "cost_usd": r.cost_usd_notional,
                "input_tok": r.input_tok,
                "output_tok": r.output_tok,
                "cache_create_5m": r.cache_create_5m,
                "cache_create_1h": r.cache_create_1h,
                "cache_read": r.cache_read,
            }
            for r in kept
        ]
        msg_df = pl.DataFrame(rows)
    else:
        msg_df = pl.DataFrame(schema=_MSG_FRAME_SCHEMA)

    # ── Phase 3: count and drop weekend records ───────────────────────────
    weekend_records: int = msg_df.filter(pl.col("weekday") >= 5).height
    weekday_msg = msg_df.filter(pl.col("weekday") < 5)

    # ── Phase 4: group-by-date aggregation (Decimal-preserving) ──────────
    daily = weekday_msg.group_by("date_utc").agg(
        [
            pl.col("cost_usd").sum().alias("notional_cost_usd"),
            pl.col("input_tok").sum(),
            pl.col("output_tok").sum(),
            pl.col("cache_create_5m").sum(),
            pl.col("cache_create_1h").sum(),
            pl.col("cache_read").sum(),
            # ``pl.len()`` returns ``UInt32``; cast to ``Int64`` to match
            # ``EXPECTED_PANEL_SCHEMA``.
            pl.len().cast(pl.Int64).alias("n_messages"),
        ]
    )

    # ── Phase 5: weekend filter on TRM side ──────────────────────────────
    # polars ``dt.weekday()`` is Mon=1..Sun=7 — `<= 5` keeps Mon-Fri.
    trm_weekday = trm_panel.filter(pl.col("date").dt.weekday() <= 5).rename(
        {"date": "date_utc"}
    )
    weekend_trm: int = trm_panel.height - trm_weekday.height

    # ── Phase 6: inner join (forward-fill forbidden) ─────────────────────
    pre_join_daily_height: int = daily.height
    joined = daily.join(trm_weekday, on="date_utc", how="inner")

    # USD → COP conversion under Decimal exactness.
    joined = joined.with_columns(
        (pl.col("notional_cost_usd") * pl.col("trm_cop_per_usd")).alias(
            "notional_cost_cop"
        )
    )
    # Final column ordering/selection to match ``EXPECTED_PANEL_SCHEMA`` exactly.
    joined = joined.select(list(EXPECTED_PANEL_SCHEMA.keys()))

    # ── Phase 7: dropped-rows accounting ─────────────────────────────────
    # Weekday-records-with-no-matching-TRM are inner-join losses on the
    # daily (left) side.
    join_loss_left: int = pre_join_daily_height - joined.height
    dropped_rows: int = weekend_records + weekend_trm + join_loss_left

    return DailyNotionalPanel(
        df=joined,
        dropped_rows_count=int(dropped_rows),
        dropped_error_count=int(dropped_error),
    )


__all__ = ["build_daily_panel"]
