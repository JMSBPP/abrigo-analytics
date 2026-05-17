"""utils-tier IO Boundary for dev_ai_cost_v2.

Reads ``~/.claude/projects/**/*.jsonl`` directly with a permissive Pydantic
schema mirroring Anthropic's documented Claude Code session-log fields
(``extra="allow"``; only ``timestamp + message.usage.{input_tokens,
output_tokens}`` required). Spec ref:
``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.3 §3.5
+ §0.3 CORRECTIONS-Y-1/-Y-5b/-Y-5e/-Y-5f.

Sibling spec ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md``
v0.1.3 CORRECTIONS-RR/-TT requires the per-JSONL-line ``uuid`` field for R6
pool canonicalization (tertiary sort key + same-path dedupe tiebreaker).
v0.2.3 (Y-5e) relaxes the uuid requirement at the wire: when absent, a
stable basename-derived synthesis fills in
``"synth-sha256:" + sha256(file.stem + ":" + line_no_zfill_8).hexdigest()[:16]``.
Rename-stable across paths; line-bound; basename-bound.

Tier rule: this is the ONLY module in the ``dev_ai_cost_v2`` sub-package
permitted to perform IO. Modules and types tiers must remain pure.

v0.2.3 closure (Y-5f, CR-Z-2):
  - ``JSONLReader.__call__`` returns ``JSONLReadResult`` (types tier),
    NOT a bare ``Sequence[MessageRecord]``. The result container carries
    ``dropped_non_assistant_count`` per Y-5a.
  - ``PricingTable`` injected via ``JSONLReader.__init__`` so cost is
    computed at parse time (was: cost read off ``costUSD`` field, which is
    now removed from the schema).
  - Type-discriminator filter (Y-1): rows with ``type != "assistant"`` are
    skipped BEFORE Pydantic validation; the skip count surfaces in the
    result container.
"""
from __future__ import annotations

import hashlib
import json
import warnings
from datetime import date, datetime, time, timezone
from pathlib import Path

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, ValidationError

from simulations.dev_ai_cost_v2._errors import JSONLSchemaError
from simulations.dev_ai_cost_v2.anthropic_pricing import PricingTable
from simulations.dev_ai_cost_v2.types import (
    JSONLReadResult,
    MessageRecord,
    TokensByCategory,
)


# ─── Pinned Pydantic schema (mirrors Anthropic Claude Code JSONL) ────────────
#
# v0.2.3 (Y-5f): ``extra="allow"`` — Anthropic frequently adds new fields and
# we do not want to fail-loud on benign drift. Required fields are narrowed
# to the minimum needed to construct a ``MessageRecord``: timestamp,
# message.model, message.usage.input_tokens, message.usage.output_tokens.
# Everything else is Optional with sensible defaults.


class _CacheCreation(BaseModel):
    """``message.usage.cache_creation`` sub-block (optional)."""

    model_config = ConfigDict(extra="allow")
    ephemeral_5m_input_tokens: int = 0
    ephemeral_1h_input_tokens: int = 0


class _Usage(BaseModel):
    """``message.usage`` block. Only token counts are required."""

    model_config = ConfigDict(extra="allow")
    input_tokens: int
    output_tokens: int
    cache_creation: _CacheCreation = Field(default_factory=_CacheCreation)
    cache_read_input_tokens: int = 0


class _Message(BaseModel):
    """``message`` block (model + usage)."""

    model_config = ConfigDict(extra="allow")
    model: str = "unknown"
    usage: _Usage


class _Row(BaseModel):
    """One JSONL line in an Anthropic Claude Code session log.

    v0.2.3 (Y-5f) — ``extra="allow"``; the only fields required are
    ``timestamp`` and ``message.usage.{input_tokens, output_tokens}``. All
    other fields Optional with documented defaults. ``costUSD`` removed
    entirely (cost is computed at parse time via the injected ``PricingTable``).
    """

    model_config = ConfigDict(extra="allow")
    timestamp: AwareDatetime  # tz-naive rejected per Task 5 fix 283673d
    sessionId: str = ""
    requestId: str | None = None
    isApiErrorMessage: bool | None = False  # Y-1: absent → False
    uuid: str | None = None  # Y-5e: absent → synthesized at construct time
    message: _Message
    type: str | None = None  # Y-1 type-discriminator (filtered pre-validation)


# ─── JSONLReader ─────────────────────────────────────────────────────────────


def _synth_uuid(file_path: Path, line_no: int) -> str:
    """Y-5e: rename-stable basename-derived uuid synthesis.

    Per CR-Z-5: the synth uuid is bound to the JSONL file's BASENAME (via
    ``Path.stem``, which strips both directory AND extension) plus the line
    number (zero-padded to 8 digits). Moving the file to a different
    directory does NOT change the synth uuid; renaming the file does.

    Output format: ``"synth-sha256:" + first 16 hex chars of
    sha256(stem + ":" + line_no_zfill_8)``. R6 canonicalization gates on
    the ``synth-`` prefix and splits-or-warns to preserve hash stability.
    """
    basename: str = Path(file_path).stem
    digest_input: str = f"{basename}:{str(line_no).zfill(8)}"
    digest: str = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()[:16]
    return f"synth-sha256:{digest}"


def _construct_message_record(
    row: _Row,
    file_path: Path,
    line_no: int,
    pricing: PricingTable,
    ts: datetime,
) -> MessageRecord:
    """Y-5e: build a MessageRecord, synthesizing uuid if absent and
    computing cost from the injected pricing table.

    Args:
        row: validated ``_Row`` from Pydantic.
        file_path: path to the source JSONL file (used for uuid synthesis).
        line_no: 1-indexed line number within ``file_path``.
        pricing: ``PricingTable`` to compute ``cost_usd_notional``.
        ts: UTC-normalized timestamp.

    Returns:
        Fully-constructed ``MessageRecord`` with uuid, cost, and tokens.
    """
    if row.uuid is None or row.uuid == "":
        uuid: str = _synth_uuid(file_path, line_no)
    else:
        uuid = row.uuid

    toks = TokensByCategory(
        input=row.message.usage.input_tokens,
        output=row.message.usage.output_tokens,
        cache_create_5m=row.message.usage.cache_creation.ephemeral_5m_input_tokens,
        cache_create_1h=row.message.usage.cache_creation.ephemeral_1h_input_tokens,
        cache_read=row.message.usage.cache_read_input_tokens,
    )
    cost: float = pricing(row.message.model, ts, toks)

    return MessageRecord(
        ts=ts,
        model=row.message.model,
        input_tok=row.message.usage.input_tokens,
        output_tok=row.message.usage.output_tokens,
        cache_create_5m=row.message.usage.cache_creation.ephemeral_5m_input_tokens,
        cache_create_1h=row.message.usage.cache_creation.ephemeral_1h_input_tokens,
        cache_read=row.message.usage.cache_read_input_tokens,
        cost_usd_notional=cost,
        session_id=row.sessionId,
        request_id=row.requestId,
        is_error=bool(row.isApiErrorMessage),
        uuid=uuid,
    )


class JSONLReader:
    """IO Boundary: reads Anthropic Claude Code JSONL transcripts.

    Returns a ``JSONLReadResult`` (types tier; see Y-5b/CR-Z-2) carrying
    a materialized ``tuple[MessageRecord, ...]`` + the
    ``dropped_non_assistant_count`` counter per Y-5a.

    This is the ONLY module in the ``dev_ai_cost_v2`` sub-package permitted
    to perform filesystem IO; types and modules tiers must remain pure.

    The ``PricingTable`` is injected at construction time so cost is
    computed at parse time using the spec-pinned LiteLLM SHA rate table.
    """

    def __init__(self, pricing: PricingTable) -> None:
        """Inject the pricing table used to compute per-message cost.

        Args:
            pricing: ``PricingTable`` instance. Stored on the reader so
                each ``__call__`` invocation uses the same rate snapshot.
        """
        self._pricing = pricing

    def __call__(
        self,
        since: date,
        until: date,
        projects_root: Path = Path("~/.claude/projects").expanduser(),
    ) -> JSONLReadResult:
        """Parse all JSONL files under ``projects_root`` within ``[since, until)``.

        Walks ``projects_root`` recursively via ``rglob("*.jsonl")``, filters
        rows by the Y-1 type-discriminator (``type == "assistant"`` only),
        parses each surviving line with the pinned permissive Pydantic
        ``_Row`` schema, filters by UTC half-open window, computes cost via
        the injected ``PricingTable``, and returns a ``JSONLReadResult``.

        Invariants enforced:
            - Type-discriminator filter (Y-1): rows where ``type !=
              "assistant"`` are skipped BEFORE Pydantic validation. The
              skip count surfaces in
              ``JSONLReadResult.dropped_non_assistant_count``. Absent
              ``type`` field is treated as non-assistant and skipped.
            - ``extra="allow"`` on every nested Pydantic model — unknown
              fields are silently accepted (Y-5f permissive schema).
            - Required fields (``timestamp``, ``message.usage.input_tokens``,
              ``message.usage.output_tokens``) raise ``JSONLSchemaError``
              when absent.
            - ``timestamp`` must be tz-aware. Tz-naive timestamps are
              rejected at Pydantic validation time via ``AwareDatetime``
              (raises ``JSONLSchemaError``).
            - Window boundary is UTC half-open: rows at
              ``until 00:00:00Z`` are EXCLUDED.
            - Blank lines (empty or whitespace-only) are skipped silently.
            - uuid synthesis per Y-5e: when ``row.uuid`` is None, the
              synthesized uuid is bound to the file basename + line number;
              rename-stable across paths; basename-bound.

        Args:
            since: inclusive lower bound (UTC date).
            until: exclusive upper bound (UTC date).
            projects_root: root directory containing per-project JSONL
                session logs. Defaults to ``~/.claude/projects`` expanded.

        Returns:
            ``JSONLReadResult`` with materialized ``records: tuple[...]``
            and ``dropped_non_assistant_count``.

        Raises:
            JSONLSchemaError: on Pydantic validation failure (missing
                required field, wrong dtype) OR on malformed JSON
                (``json.JSONDecodeError`` wrapped). The error message
                includes the offending ``{path}:{line_no}``.
            FileNotFoundError: if ``projects_root`` does not exist.
            ValueError: propagated from ``MessageRecord.__post_init__`` if
                a schema-valid row violates a downstream invariant.

        Errors silenced:
            None at the JSONL layer. Pydantic surfaces every schema
            mismatch; ``json.JSONDecodeError`` is wrapped in
            ``JSONLSchemaError``. Blank-line skipping is the documented
            JSONL convention. Non-assistant rows are explicitly counted,
            not silenced.

        Warnings emitted:
            ``UserWarning`` (``stacklevel=2``) when ``requestId is None``
            (legacy pre-2.0 Claude Code rows).
        """
        if not projects_root.exists():
            raise FileNotFoundError(projects_root)

        lo = datetime.combine(since, time.min, tzinfo=timezone.utc)
        hi = datetime.combine(until, time.min, tzinfo=timezone.utc)

        records: list[MessageRecord] = []
        dropped_non_assistant: int = 0
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

                    # Y-1 type-discriminator: skip non-assistant rows BEFORE
                    # Pydantic validation. Absent ``type`` → treat as
                    # non-assistant (covers user, system, summary, and any
                    # future row types not yet enumerated).
                    if not isinstance(raw, dict) or raw.get("type") != "assistant":
                        dropped_non_assistant += 1
                        continue

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
                    records.append(
                        _construct_message_record(
                            row=row,
                            file_path=jsonl_path,
                            line_no=line_no,
                            pricing=self._pricing,
                            ts=ts,
                        )
                    )
        return JSONLReadResult(
            records=tuple(records),
            dropped_non_assistant_count=dropped_non_assistant,
        )


__all__ = ["JSONLReader"]
