"""Types tier for dev_ai_cost_v2 — frozen-dataclass value containers.

Tier-import rule: ``types/`` imports neither ``modules/`` nor ``utils/`` from
the dev_ai_cost_v2 sub-package. Polars is a value-tier-admissible dependency
(it is a pure data-container library, not an IO boundary).

Spec ref: ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1 §3.5.

Sibling spec ref: ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md``
v0.1.3 CORRECTIONS-RR/-TT adds the ``uuid: str`` field on ``MessageRecord``
(per-JSONL-line uuid from the Anthropic Claude Code schema). The field is
required for R6 pool canonicalization (tertiary sort key + same-path
dedupe tiebreaker); an empty uuid would make the sort ambiguous and is
therefore rejected at construction.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

import polars as pl


# ─── EXPECTED_PANEL_SCHEMA ────────────────────────────────────────────────────
#
# Pinned schema for ``DailyNotionalPanel.df``. Validated in __post_init__.
# Decimal columns are validated by polars-DataTypeClass equality (which
# permits any precision/scale); the Pricing layer (Task 6) commits to a
# canonical precision/scale at panel construction.

EXPECTED_PANEL_SCHEMA: dict[str, pl.DataType] = {
    "date_utc": pl.Date,
    "notional_cost_usd": pl.Decimal,
    "notional_cost_cop": pl.Decimal,
    "trm_cop_per_usd": pl.Decimal,
    "input_tok": pl.Int64,
    "output_tok": pl.Int64,
    "cache_create_5m": pl.Int64,
    "cache_create_1h": pl.Int64,
    "cache_read": pl.Int64,
    "n_messages": pl.Int64,
}


# ─── MessageRecord ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class MessageRecord:
    """A single parsed assistant message from a Claude Code JSONL session log.

    Fields:
        ts: timezone-aware UTC datetime (ms-precision from Anthropic JSONL).
            ``tz-naive`` and non-UTC tz inputs are rejected.
        model: Anthropic model identifier (e.g., ``"claude-sonnet-4-5"``).
        input_tok: standard input token count (``≥ 0``).
        output_tok: standard output token count (``≥ 0``).
        cache_create_5m: ``cache_creation.ephemeral_5m_input_tokens`` from the
            Anthropic JSONL ``usage`` block (``≥ 0``).
        cache_create_1h: ``cache_creation.ephemeral_1h_input_tokens`` from the
            Anthropic JSONL ``usage`` block (``≥ 0``).
        cache_read: ``cache_read_input_tokens`` from the Anthropic JSONL
            ``usage`` block (``≥ 0``).
        cost_usd_notional: rate-card USD cost computed at parse time by
            ``PricingTable`` (``Decimal``, exact arithmetic; ``≥ 0``).
        session_id: Claude Code ``sessionId`` (groups messages within a
            session).
        request_id: Anthropic ``requestId``; ``None`` on legacy Claude Code
            (pre-2.0). ``JSONLReader`` emits a warning when ``None`` is
            observed but does not error.
        is_error: ``True`` if the assistant message was an error response.
        uuid: per-JSONL-line UUID from the Anthropic Claude Code schema.
            Required for R6 pool canonicalization (CORRECTIONS-RR/-TT) as
            the tertiary sort key + same-path dedupe tiebreaker. Must be
            non-empty.

    Raises:
        ValueError: if ``ts`` is tz-naive or non-UTC; if any token field is
            negative; if ``cost_usd_notional`` is negative; if ``uuid`` is
            empty.
    """

    ts: datetime
    model: str
    input_tok: int
    output_tok: int
    cache_create_5m: int
    cache_create_1h: int
    cache_read: int
    cost_usd_notional: Decimal
    session_id: str
    request_id: str | None
    is_error: bool
    uuid: str  # R6 v0.1.3 CORRECTIONS-RR/-TT

    def __post_init__(self) -> None:
        # tz-awareness + UTC-offset check. ``timezone.utc`` and any
        # ``timezone(timedelta(0))`` both pass (offset == zero).
        if self.ts.tzinfo is None or self.ts.utcoffset() != timezone.utc.utcoffset(self.ts):
            raise ValueError(
                f"MessageRecord.ts must be timezone-aware UTC; got {self.ts!r}"
            )
        for fname in (
            "input_tok",
            "output_tok",
            "cache_create_5m",
            "cache_create_1h",
            "cache_read",
        ):
            v: int = getattr(self, fname)
            if v < 0:
                raise ValueError(f"MessageRecord.{fname} must be >= 0; got {v}")
        if self.cost_usd_notional < 0:
            raise ValueError(
                f"MessageRecord.cost_usd_notional must be >= 0; got {self.cost_usd_notional}"
            )
        if not self.uuid:
            raise ValueError(
                "MessageRecord.uuid must be non-empty (required by R6 canonicalization)"
            )


# ─── TokensByCategory ─────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TokensByCategory:
    """Token counts per Anthropic billing category; consumed by
    ``PricingTable.__call__`` (Task 6).

    The five categories correspond to LiteLLM pricing keys at
    SHA ``e58a561c`` (the canonical pricing snapshot pinned by the
    dev_ai_cost_v2 sub-package):

    - ``input``           → ``input_cost_per_token``
    - ``output``          → ``output_cost_per_token``
    - ``cache_create_5m`` → ``cache_creation_input_token_cost`` (5m default)
    - ``cache_create_1h`` → ``cache_creation_input_token_cost_above_1hr``
    - ``cache_read``      → ``cache_read_input_token_cost``

    Raises:
        ValueError: if any field is negative.
    """

    input: int
    output: int
    cache_create_5m: int
    cache_create_1h: int
    cache_read: int

    def __post_init__(self) -> None:
        for fname in (
            "input",
            "output",
            "cache_create_5m",
            "cache_create_1h",
            "cache_read",
        ):
            v: int = getattr(self, fname)
            if v < 0:
                raise ValueError(f"TokensByCategory.{fname} must be >= 0; got {v}")


# ─── DailyNotionalPanel ───────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class DailyNotionalPanel:
    """Frozen-dc wrapper over a polars ``DataFrame`` holding the daily
    notional cost panel (one row per UTC date).

    The wrapper itself is frozen; the inner ``DataFrame`` is *not* (an
    acknowledged threat in spec v0.2.1 §6). Consumers should treat ``df``
    as read-only or call ``.clone()`` before mutation.

    Schema is validated in ``__post_init__`` against
    ``EXPECTED_PANEL_SCHEMA``: missing columns, extra columns, and wrong
    dtypes all raise ``ValueError`` with a descriptive message identifying
    the offending column(s).

    ``Decimal`` columns are validated by ``DataTypeClass``-equality, which
    matches any precision/scale; downstream consumers (the Pricing layer
    in Task 6) commit to a canonical (precision, scale) at construction.

    Fields:
        df: the underlying polars ``DataFrame``. Schema pinned by
            ``EXPECTED_PANEL_SCHEMA``.
        dropped_rows_count: count of JSONL rows dropped due to schema /
            parse errors during panel construction (``≥ 0``). Surfaced to
            the CLI for an operator-visible audit line.
        dropped_error_count: count of assistant-error messages dropped
            during panel construction (``≥ 0``). Operator visibility
            requirement per spec v0.2.1 §3.4.

    Raises:
        ValueError: if ``df.schema`` diverges from ``EXPECTED_PANEL_SCHEMA``
            (missing columns, extra columns, or wrong dtype); if either
            ``dropped_rows_count`` or ``dropped_error_count`` is negative.
    """

    df: pl.DataFrame
    dropped_rows_count: int
    dropped_error_count: int

    def __post_init__(self) -> None:
        actual: dict[str, pl.DataType] = dict(self.df.schema)
        missing = set(EXPECTED_PANEL_SCHEMA) - set(actual)
        extra = set(actual) - set(EXPECTED_PANEL_SCHEMA)
        if missing or extra:
            raise ValueError(
                f"DailyNotionalPanel schema drift: missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )
        for col, expected in EXPECTED_PANEL_SCHEMA.items():
            if actual[col] != expected:
                raise ValueError(
                    f"DailyNotionalPanel column {col!r}: expected dtype "
                    f"{expected}, got {actual[col]}"
                )
        if self.dropped_rows_count < 0:
            raise ValueError(
                f"DailyNotionalPanel.dropped_rows_count must be >= 0; "
                f"got {self.dropped_rows_count}"
            )
        if self.dropped_error_count < 0:
            raise ValueError(
                f"DailyNotionalPanel.dropped_error_count must be >= 0; "
                f"got {self.dropped_error_count}"
            )


__all__ = [
    "EXPECTED_PANEL_SCHEMA",
    "MessageRecord",
    "TokensByCategory",
    "DailyNotionalPanel",
]
