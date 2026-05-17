"""utils-tier IO Boundary for dev_ai_cost_v2.

Reads ``~/.claude/projects/**/*.jsonl`` directly with a Pydantic schema that
mirrors Anthropic's documented Claude Code session-log fields
(``extra="forbid"``). Spec ref:
``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1 §3.1, §3.5.

Sibling spec ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md``
v0.1.3 CORRECTIONS-RR/-TT requires the per-JSONL-line top-level ``uuid`` field
(used by R6 pool canonicalization as the tertiary sort key + same-path dedupe
tiebreaker). The field is required on input rows and propagated to
``MessageRecord.uuid``.

Tier rule: this is the ONLY module in the ``dev_ai_cost_v2`` sub-package
permitted to perform IO. Modules and types tiers must remain pure.

CR FLAG A closure (CORRECTIONS-V): ``__call__`` returns a materialized
``Sequence[MessageRecord]`` (concretely a ``list``), not an ``Iterator``, so
downstream consumers (reconciliation cell + panel-builder aggregation) can
iterate multiple times without re-parsing JSONL.
"""
from __future__ import annotations

import json
import warnings
from collections.abc import Sequence
from datetime import date, datetime, time, timezone
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from simulations.dev_ai_cost_v2._errors import JSONLSchemaError
from simulations.dev_ai_cost_v2.types import MessageRecord


# ─── Pinned Pydantic schema (mirrors Anthropic Claude Code JSONL) ────────────


class _CacheCreation(BaseModel):
    """``message.usage.cache_creation`` sub-block."""

    model_config = ConfigDict(extra="forbid")
    ephemeral_5m_input_tokens: int = 0
    ephemeral_1h_input_tokens: int = 0


class _Usage(BaseModel):
    """``message.usage`` block."""

    model_config = ConfigDict(extra="forbid")
    input_tokens: int
    output_tokens: int
    cache_creation: _CacheCreation = Field(default_factory=_CacheCreation)
    cache_read_input_tokens: int = 0


class _Message(BaseModel):
    """``message`` block (model + usage)."""

    model_config = ConfigDict(extra="forbid")
    model: str
    usage: _Usage


class _Row(BaseModel):
    """One JSONL line in an Anthropic Claude Code session log.

    All fields are required except ``requestId`` (legacy pre-2.0 Claude Code
    rows may emit ``null``; ``JSONLReader`` warns but does not error).
    """

    model_config = ConfigDict(extra="forbid")
    timestamp: datetime
    sessionId: str
    requestId: str | None
    isApiErrorMessage: bool
    uuid: str  # R6 v0.1.3 CORRECTIONS-RR/-TT — required, no default
    message: _Message
    costUSD: Decimal


# ─── JSONLReader ─────────────────────────────────────────────────────────────


class JSONLReader:
    """IO Boundary: reads Anthropic Claude Code JSONL transcripts.

    Returns a materialized ``Sequence[MessageRecord]`` (concretely a ``list``)
    so downstream consumers may iterate multiple times (reconciliation cell +
    panel-builder aggregation). See spec §3.5 / CORRECTIONS-V FLAG A.

    This is the ONLY module in the ``dev_ai_cost_v2`` sub-package permitted
    to perform filesystem IO; types and modules tiers must remain pure.
    """

    def __call__(
        self,
        since: date,
        until: date,
        projects_root: Path = Path("~/.claude/projects").expanduser(),
    ) -> Sequence[MessageRecord]:
        """Parse all JSONL files under ``projects_root`` within ``[since, until)``.

        Walks ``projects_root`` recursively via ``rglob("*.jsonl")``, parses
        each non-blank line with the pinned Pydantic ``_Row`` schema, filters
        by UTC half-open window, and returns the materialized list of
        ``MessageRecord``.

        Invariants enforced:
            - ``extra="forbid"`` on every nested Pydantic model — any unknown
              field in the JSONL raises ``JSONLSchemaError``.
            - Required fields (including ``uuid`` per R6 v0.1.3
              CORRECTIONS-RR/-TT) raise ``JSONLSchemaError`` when absent.
            - ``timestamp`` is interpreted as UTC; both naive (treated as UTC
              by Pydantic + ``astimezone``) and offset-aware inputs collapse
              to UTC before window comparison.
            - Window boundary is UTC half-open: rows at
              ``until 00:00:00Z`` are EXCLUDED (CORRECTIONS-V NIT).
            - Blank lines (empty or whitespace-only) are skipped silently.

        Args:
            since: inclusive lower bound (UTC date). Rows with
                ``ts >= since 00:00:00Z`` are included.
            until: exclusive upper bound (UTC date). Rows with
                ``ts < until 00:00:00Z`` are included; rows at exactly
                ``until 00:00:00Z`` are EXCLUDED.
            projects_root: root directory containing per-project JSONL
                session logs. Defaults to ``~/.claude/projects`` expanded.

        Returns:
            Materialized ``list[MessageRecord]`` (not Iterator) — supports
            multi-pass iteration per CR FLAG A.

        Raises:
            JSONLSchemaError: on Pydantic validation failure
                (``extra="forbid"`` violation, missing required field
                including ``uuid``, or wrong dtype) OR on malformed JSON
                (``json.JSONDecodeError`` wrapped). The error message
                includes the offending ``{path}:{line_no}``.
            FileNotFoundError: if ``projects_root`` does not exist.
            ValueError: propagated from ``MessageRecord.__post_init__`` if a
                schema-valid row violates a downstream invariant
                (e.g., empty ``uuid`` string — should be unreachable given
                Pydantic enforces non-empty via the parent ``str`` parse,
                but defense-in-depth from the types tier still applies).

        Errors silenced:
            None at the JSONL layer. Pydantic surfaces every schema
            mismatch; ``json.JSONDecodeError`` is wrapped in
            ``JSONLSchemaError`` (preserving ``__cause__``). The only
            non-error suppression is blank-line skipping, which is the
            documented JSONL convention.

        Errors from external state:
            - Filesystem: ``FileNotFoundError`` if ``projects_root`` is
              missing; ``PermissionError`` may propagate from
              ``Path.open()`` if the operator lacks read access.
            - JSONL file mutation mid-read: any data race is not detected;
              callers should ensure the projects_root tree is quiescent.

        Warnings emitted:
            ``UserWarning`` (``stacklevel=2``) when ``requestId is None``
            (legacy pre-2.0 Claude Code rows). Does not block ingest.
        """
        if not projects_root.exists():
            raise FileNotFoundError(projects_root)

        lo = datetime.combine(since, time.min, tzinfo=timezone.utc)
        hi = datetime.combine(until, time.min, tzinfo=timezone.utc)

        out: list[MessageRecord] = []
        for jsonl_path in projects_root.rglob("*.jsonl"):
            with jsonl_path.open("r") as f:
                for line_no, line in enumerate(f, start=1):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        raw = json.loads(stripped)
                    except json.JSONDecodeError as e:
                        raise JSONLSchemaError(
                            f"{jsonl_path}:{line_no} invalid JSON: {e}"
                        ) from e
                    try:
                        row = _Row.model_validate(raw)
                    except ValidationError as e:
                        raise JSONLSchemaError(
                            f"{jsonl_path}:{line_no} schema drift: {e}"
                        ) from e
                    ts = row.timestamp.astimezone(timezone.utc)
                    if not (lo <= ts < hi):
                        continue
                    if row.requestId is None:
                        warnings.warn(
                            f"{jsonl_path}:{line_no} legacy row: request_id is None",
                            UserWarning,
                            stacklevel=2,
                        )
                    out.append(
                        MessageRecord(
                            ts=ts,
                            model=row.message.model,
                            input_tok=row.message.usage.input_tokens,
                            output_tok=row.message.usage.output_tokens,
                            cache_create_5m=row.message.usage.cache_creation.ephemeral_5m_input_tokens,
                            cache_create_1h=row.message.usage.cache_creation.ephemeral_1h_input_tokens,
                            cache_read=row.message.usage.cache_read_input_tokens,
                            cost_usd_notional=row.costUSD,
                            session_id=row.sessionId,
                            request_id=row.requestId,
                            is_error=row.isApiErrorMessage,
                            uuid=row.uuid,  # R6 v0.1.3 CORRECTIONS-RR/-TT
                        )
                    )
        return out


__all__ = ["JSONLReader"]
