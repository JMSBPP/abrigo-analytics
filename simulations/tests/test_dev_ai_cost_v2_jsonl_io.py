"""Tests for ``simulations.dev_ai_cost_v2.jsonl_io.JSONLReader``.

Spec refs:
- ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.3 §3.5,
  §0.3 CORRECTIONS-Y-1 (type-discriminator), Y-5b (JSONLReadResult tier),
  Y-5e (uuid synthesis), Y-5f (permissive Pydantic + cost via injected
  PricingTable).
- ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md`` v0.1.3
  CORRECTIONS-RR/-TT (uuid required at MessageRecord level — synthesized
  here when absent at wire level).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from simulations.dev_ai_cost_v2._errors import JSONLSchemaError
from simulations.dev_ai_cost_v2.anthropic_pricing import (
    LITELLM_SHA_PINNED,
    PricingTable,
    _REQUIRED_KEYS,
)
from simulations.dev_ai_cost_v2.jsonl_io import JSONLReader, _synth_uuid
from simulations.dev_ai_cost_v2.types import JSONLReadResult, MessageRecord


# ─── Fixtures ────────────────────────────────────────────────────────────────


def _toy_pricing(tmp_path: Path) -> PricingTable:
    fake = {"claude-sonnet-4-5": {k: 1e-06 for k in _REQUIRED_KEYS}}
    p = tmp_path / "lite.json"
    p.write_text(json.dumps(fake))
    return PricingTable.from_litellm_sha(
        LITELLM_SHA_PINNED, p, skip_sha_check=True
    )


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def _valid_row(
    ts: str = "2026-05-01T12:00:00Z",
    uuid: str | None = "msg-uuid-001",
    type_: str = "assistant",
) -> dict:
    r = {
        "timestamp": ts,
        "sessionId": "s1",
        "requestId": "r1",
        "isApiErrorMessage": False,
        "type": type_,
        "message": {
            "model": "claude-sonnet-4-5",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 50,
                "cache_creation": {
                    "ephemeral_5m_input_tokens": 0,
                    "ephemeral_1h_input_tokens": 0,
                },
                "cache_read_input_tokens": 0,
            },
        },
    }
    if uuid is not None:
        r["uuid"] = uuid
    return r


# ─── Core: returns JSONLReadResult (Y-5b / CR-Z-2) ──────────────────────────


def test_jsonlreader_returns_jsonl_read_result(tmp_path: Path) -> None:
    """Y-5b: __call__ returns JSONLReadResult, not bare Sequence."""
    proj = tmp_path / "projects" / "p1"
    _write_jsonl(proj / "session.jsonl", [_valid_row()])
    reader = JSONLReader(pricing=_toy_pricing(tmp_path))
    out = reader(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert isinstance(out, JSONLReadResult)
    assert isinstance(out.records, tuple)
    assert len(out.records) == 1
    assert isinstance(out.records[0], MessageRecord)
    assert out.records[0].uuid == "msg-uuid-001"


def test_jsonlreader_utc_boundary_half_open(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    _write_jsonl(
        proj / "s.jsonl",
        [
            _valid_row("2026-05-01T00:00:00Z", uuid="u1"),  # included
            _valid_row("2026-05-01T23:59:59Z", uuid="u2"),  # included
            _valid_row("2026-05-02T00:00:00Z", uuid="u3"),  # EXCLUDED — half-open upper
        ],
    )
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 2
    uuids = {r.uuid for r in out.records}
    assert uuids == {"u1", "u2"}


# ─── Y-1: type-discriminator filter ──────────────────────────────────────────


def test_jsonlreader_skips_non_assistant_rows(tmp_path: Path) -> None:
    """Y-1: rows with type != 'assistant' are skipped before validation;
    skip count surfaces in JSONLReadResult.dropped_non_assistant_count.
    """
    proj = tmp_path / "projects" / "p1"
    rows = [
        _valid_row(uuid="u1", type_="assistant"),
        _valid_row(uuid="u2", type_="user"),
        _valid_row(uuid="u3", type_="system"),
        _valid_row(uuid="u4", type_="summary"),
        _valid_row(uuid="u5", type_="assistant"),
    ]
    _write_jsonl(proj / "s.jsonl", rows)
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 2
    assert {r.uuid for r in out.records} == {"u1", "u5"}
    assert out.dropped_non_assistant_count == 3


def test_jsonlreader_skips_rows_with_no_type_field(tmp_path: Path) -> None:
    """Y-1: absent ``type`` field is treated as non-assistant and skipped."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["type"]
    _write_jsonl(proj / "s.jsonl", [row])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 0
    assert out.dropped_non_assistant_count == 1


# ─── Y-5f: permissive Pydantic (extra='allow') ──────────────────────────────


def test_jsonlreader_allows_extra_fields(tmp_path: Path) -> None:
    """Y-5f: extra fields are silently accepted (no JSONLSchemaError)."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    row["unknown_extra_field"] = "drift"
    row["another_new_field"] = {"nested": [1, 2, 3]}
    _write_jsonl(proj / "s.jsonl", [row])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 1


def test_jsonlreader_costUSD_field_removed(tmp_path: Path) -> None:
    """Y-5f: costUSD is removed from _Row; cost computed at parse time
    via injected PricingTable. The presence/absence of costUSD on the wire
    is now ignored (extra=allow).
    """
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    row["costUSD"] = "0.99"  # legacy wire field — should be ignored
    _write_jsonl(proj / "s.jsonl", [row])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    # Pricing was 1e-06 across all rates; cost = 100*1e-06 + 50*1e-06 = 1.5e-4.
    assert out.records[0].cost_usd_notional == pytest.approx(1.5e-4)
    # NOT 0.99 (the wire costUSD is ignored).


# ─── Y-5e: uuid synthesis ────────────────────────────────────────────────────


def test_jsonlreader_synthesizes_uuid_when_absent(tmp_path: Path) -> None:
    """Y-5e: when row uuid is None/absent, synth uuid is filled in."""
    proj = tmp_path / "projects" / "p1"
    _write_jsonl(proj / "session.jsonl", [_valid_row(uuid=None)])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 1
    rec = out.records[0]
    assert rec.uuid.startswith("synth-sha256:")
    # The synth hash is bound to basename ("session") + line ("00000001").
    expected = _synth_uuid(proj / "session.jsonl", 1)
    assert rec.uuid == expected


def test_jsonlreader_preserves_real_uuid_when_present(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    _write_jsonl(proj / "session.jsonl", [_valid_row(uuid="real-uuid-xyz")])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert out.records[0].uuid == "real-uuid-xyz"


# ─── CR-Z-5: uuid synthesis stability under rename ──────────────────────────


def test_cr_z_5_synth_uuid_path_independent_basename_bound() -> None:
    """CR-Z-5: synth uuid is rename-stable across paths (basename-bound).

    Moving the JSONL file to a different directory must NOT change the
    synth uuid (basename and line stay the same). Changing line number
    MUST change the synth uuid. Changing basename MUST change the synth uuid.
    """
    # Path A (line 42).
    uuid_path_a = _synth_uuid(Path("/path/A/session.jsonl"), 42)
    # Path B with same basename, same line — must be identical.
    uuid_path_b = _synth_uuid(Path("/different/path/B/session.jsonl"), 42)
    assert uuid_path_a == uuid_path_b

    # Different line — must differ.
    uuid_diff_line = _synth_uuid(Path("/path/A/session.jsonl"), 43)
    assert uuid_diff_line != uuid_path_a

    # Different basename — must differ.
    uuid_diff_basename = _synth_uuid(Path("/path/A/other.jsonl"), 42)
    assert uuid_diff_basename != uuid_path_a

    # All synth uuids carry the prefix.
    assert uuid_path_a.startswith("synth-sha256:")
    assert uuid_diff_line.startswith("synth-sha256:")
    assert uuid_diff_basename.startswith("synth-sha256:")


# ─── Y-5f: required-field violations still raise ────────────────────────────


def test_jsonlreader_raises_on_missing_timestamp(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["timestamp"]
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_raises_on_missing_input_tokens(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["message"]["usage"]["input_tokens"]
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_raises_on_missing_output_tokens(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["message"]["usage"]["output_tokens"]
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_allows_missing_uuid_via_synthesis(tmp_path: Path) -> None:
    """Y-5e: uuid is no longer required at the wire level — synthesized."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["uuid"]
    _write_jsonl(proj / "s.jsonl", [row])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 1
    assert out.records[0].uuid.startswith("synth-sha256:")


def test_jsonlreader_allows_missing_requestId_via_default(tmp_path: Path) -> None:
    """Y-5f: requestId is Optional with default=None."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["requestId"]
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.warns(UserWarning, match="request_id"):
        out = JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )
    assert out.records[0].request_id is None


def test_jsonlreader_allows_missing_isApiErrorMessage_via_default(
    tmp_path: Path,
) -> None:
    """Y-1: absent isApiErrorMessage treated as False."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["isApiErrorMessage"]
    _write_jsonl(proj / "s.jsonl", [row])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert out.records[0].is_error is False


# ─── Tz-naive timestamp rejection (defense in depth) ────────────────────────


def test_jsonlreader_raises_on_naive_timestamp(tmp_path: Path) -> None:
    """Tz-naive timestamps must be rejected at parse time. DO NOT regress
    on Task 5 fix 283673d (AwareDatetime).
    """
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    row["timestamp"] = "2026-05-01T12:00:00"  # tz-naive (no Z)
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_skips_invalid_json_does_not_raise(tmp_path: Path) -> None:
    """v0.2.4 Y-7: malformed JSON (JSONDecodeError) is silently skipped
    and counted in ``dropped_malformed_line_count``. Supersedes the v0.2.3
    behavior which raised ``JSONLSchemaError`` on any decode failure.
    """
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    (proj / "s.jsonl").write_text('{"not": "closed"\n')
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 0
    assert out.dropped_malformed_line_count == 1


def test_jsonlreader_raises_on_missing_projects_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "does_not_exist",
        )


def test_jsonlreader_recurses_subprojects(tmp_path: Path) -> None:
    root = tmp_path / "projects"
    _write_jsonl(root / "p1" / "s1.jsonl", [_valid_row(uuid="a")])
    _write_jsonl(root / "p2" / "nested" / "s2.jsonl", [_valid_row(uuid="b")])
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=root,
    )
    assert len(out.records) == 2
    assert {r.uuid for r in out.records} == {"a", "b"}


def test_jsonlreader_skips_blank_lines(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    with (proj / "s.jsonl").open("w") as f:
        f.write(json.dumps(_valid_row()) + "\n")
        f.write("\n")
        f.write("   \n")
        f.write(json.dumps(_valid_row(uuid="u2")) + "\n")
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 2


# ─── Hypothesis property: re-iteration via tuple-records ────────────────────


@settings(max_examples=25, deadline=None)
@given(
    n_rows=st.integers(min_value=0, max_value=20),
    uuid_seed=st.integers(min_value=0, max_value=10_000),
)
def test_jsonlreader_double_iteration_property(
    tmp_path_factory: pytest.TempPathFactory,
    n_rows: int,
    uuid_seed: int,
) -> None:
    """Returned JSONLReadResult.records is a tuple — multi-iteration yields
    identical sequences. Replaces the v0.2.1 Sequence-flag-A test.
    """
    tmp_path = tmp_path_factory.mktemp("hyp")
    proj = tmp_path / "projects" / "p1"
    rows = [_valid_row(uuid=f"u-{uuid_seed}-{i}") for i in range(n_rows)]
    if rows:
        _write_jsonl(proj / "s.jsonl", rows)
    else:
        proj.mkdir(parents=True, exist_ok=True)
        (proj / "empty.jsonl").write_text("")
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    first = list(out.records)
    second = list(out.records)
    assert first == second
    assert len(first) == n_rows


# ─── v0.2.4 §0.4 CORRECTIONS-Y-7: line-level malformed-skip ─────────────────


def test_jsonlreader_skips_trailing_null_bytes(tmp_path: Path) -> None:
    """v0.2.4 Y-7: filesystem partial-write corruption (trailing null-byte
    block) is silently skipped; valid records before the corruption parse
    cleanly.

    Mirrors the production failure: agent-af5e1160f7be358ba.jsonl:586 had
    a trailing block of ``b"\\x00" * N`` after the last newline, which the
    pre-v0.2.4 reader treated as a JSONLSchemaError. v0.2.4 Y-7 contract:
    silently skip + increment ``dropped_malformed_line_count``.
    """
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    valid_rows = [
        _valid_row(ts="2026-05-01T10:00:00Z", uuid="u1"),
        _valid_row(ts="2026-05-01T11:00:00Z", uuid="u2"),
        _valid_row(ts="2026-05-01T12:00:00Z", uuid="u3"),
    ]
    body = b"".join(
        (json.dumps(r) + "\n").encode("utf-8") for r in valid_rows
    )
    # 3000 null bytes after the last valid line — same as a partial-write
    # corruption block. ``str.strip()`` does not strip null bytes, so the
    # null-byte block reaches the json.loads attempt and JSONDecodeError-s.
    body += b"\x00" * 3000
    (proj / "session.jsonl").write_bytes(body)

    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 3
    assert {r.uuid for r in out.records} == {"u1", "u2", "u3"}
    assert out.dropped_malformed_line_count == 1


def test_jsonlreader_skips_truncated_json(tmp_path: Path) -> None:
    """v0.2.4 Y-7: a truncated (mid-line) partial-write is silently skipped;
    the valid prefix records parse cleanly.
    """
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    valid_row = _valid_row(ts="2026-05-01T10:00:00Z", uuid="u1")
    truncated_line = (
        '{"type":"assistant","timestamp":"2026-05-01T11:00:00Z",'
        '"message":{"model":"claude-sonnet-4-5","usage":{"input_tokens'
    )
    (proj / "session.jsonl").write_text(
        json.dumps(valid_row) + "\n" + truncated_line + "\n"
    )

    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 1
    assert out.records[0].uuid == "u1"
    assert out.dropped_malformed_line_count == 1


def test_dropped_malformed_line_count_threaded_through_panel(
    tmp_path: Path,
) -> None:
    """v0.2.4 Y-7: ``JSONLReadResult.dropped_malformed_line_count`` is
    surfaced on ``DailyNotionalPanel.dropped_malformed_line_count`` by
    ``build_daily_panel``. Panel-builder is the JSONLReader→Panel counter
    threading point per Y-5a/Y-7.
    """
    import polars as pl
    from datetime import datetime, timezone, date as _date
    from simulations.dev_ai_cost_v2.panel_builder import build_daily_panel
    from simulations.dev_ai_cost_v2.types import MessageRecord

    # 2026-05-04 is a Monday (weekday=0) so it survives the weekend filter.
    rec = MessageRecord(
        ts=datetime(2026, 5, 4, 12, 0, 0, tzinfo=timezone.utc),
        model="claude-sonnet-4-5",
        input_tok=100,
        output_tok=50,
        cache_create_5m=0,
        cache_create_1h=0,
        cache_read=0,
        cost_usd_notional=1.5e-4,
        session_id="s",
        request_id="r",
        is_error=False,
        uuid="u-1",
    )
    rr = JSONLReadResult(
        records=(rec,),
        dropped_non_assistant_count=0,
        dropped_malformed_line_count=7,
    )
    pricing = _toy_pricing(tmp_path)
    trm = pl.DataFrame(
        {"date": [_date(2026, 5, 4)], "trm_cop_per_usd": [4000.0]},
        schema={"date": pl.Date, "trm_cop_per_usd": pl.Float64},
    )
    panel = build_daily_panel(rr, pricing, trm)
    assert panel.dropped_malformed_line_count == 7


def test_jsonlreader_blank_lines_do_not_increment_malformed_counter(
    tmp_path: Path,
) -> None:
    """v0.2.4 Y-7 RC FLAG-4a non-over-correction commitment: blank and
    whitespace-only lines are absorbed by the pre-existing
    ``if not stripped: continue`` guard BEFORE the JSON-decode attempt, so
    they leave ``dropped_malformed_line_count == 0``.
    """
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    row = _valid_row(ts="2026-05-01T10:00:00Z", uuid="u1")
    (proj / "session.jsonl").write_text(
        json.dumps(row) + "\n"
        "\n"            # blank
        "   \n"         # whitespace-only
        "\t\n"          # tab-only
        + json.dumps(_valid_row(ts="2026-05-01T11:00:00Z", uuid="u2")) + "\n"
    )
    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out.records) == 2
    assert out.dropped_malformed_line_count == 0


def test_jsonlreader_valid_json_invalid_schema_still_raises(
    tmp_path: Path,
) -> None:
    """v0.2.4 Y-7 RC FLAG-4b non-over-correction commitment: the
    JSONDecodeError catch did NOT widen to swallow Pydantic schema errors.
    A line that decodes to valid JSON but is missing a required field
    still raises JSONLSchemaError.
    """
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    # Valid JSON, valid type discriminator, but ``message.usage`` is missing
    # the required ``input_tokens``/``output_tokens`` keys.
    bad_row = {
        "type": "assistant",
        "timestamp": "2026-05-01T10:00:00Z",
        "message": {},
    }
    (proj / "session.jsonl").write_text(json.dumps(bad_row) + "\n")
    with pytest.raises(JSONLSchemaError):
        JSONLReader(pricing=_toy_pricing(tmp_path))(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


@settings(max_examples=40, deadline=None)
@given(
    line_blobs=st.lists(
        st.binary(min_size=0, max_size=200),
        min_size=0,
        max_size=20,
    ),
)
def test_jsonlreader_line_conservation_property(
    tmp_path_factory: pytest.TempPathFactory,
    line_blobs: list[bytes],
) -> None:
    """v0.2.4 Y-7 / CR-7-N2 Hypothesis: line-accounting invariant.

    For any random byte-string input split into newline-separated lines
    the reader's output satisfies::

        dropped_malformed_line_count + len(records) + dropped_non_assistant_count
            + dropped_blank_inferred == total_input_lines

    where ``dropped_blank_inferred`` is computed from the fixture
    (lines whose ``.strip()`` is empty after utf-8 decode, or that cannot
    be decoded as utf-8). The reader never loses or double-counts a line.

    Per spec §0.4: ``dropped_blank`` is not exposed on JSONLReadResult in
    v0.2.4 (scope-minimal); the conservation test uses a fixture-derived
    blank count rather than adding a new field.
    """
    tmp_path = tmp_path_factory.mktemp("y7_inv")
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    # Construct one .jsonl file from the random blobs (one blob per line).
    # We strip embedded newlines from each blob so that ``len(line_blobs)``
    # equals the file's line count.
    sanitized: list[bytes] = [blob.replace(b"\n", b"") for blob in line_blobs]
    body: bytes = b"\n".join(sanitized)
    if line_blobs:
        body += b"\n"  # trailing newline to keep line-count == len(line_blobs)
    (proj / "session.jsonl").write_bytes(body)

    # Compute the fixture-derived blank count: a line is "blank" if its
    # utf-8 decode + str.strip() is empty. If the blob is not utf-8 we
    # treat it as non-blank (the reader's open(...,"r") with default
    # encoding will raise UnicodeDecodeError; this fixture confines blobs
    # to be safe by virtue of utf-8-clean strip-empty checks below).
    dropped_blank_inferred: int = 0
    for blob in sanitized:
        try:
            decoded = blob.decode("utf-8")
        except UnicodeDecodeError:
            # The reader will raise on the file open / iteration. Skip
            # the invariant check for this fixture by short-circuiting.
            return
        if decoded.strip() == "":
            dropped_blank_inferred += 1

    out = JSONLReader(pricing=_toy_pricing(tmp_path))(
        since=date(1970, 1, 1),
        until=date(9999, 12, 31),
        projects_root=tmp_path / "projects",
    )

    total_lines: int = len(line_blobs)
    accounted: int = (
        out.dropped_malformed_line_count
        + len(out.records)
        + out.dropped_non_assistant_count
        + dropped_blank_inferred
    )
    assert accounted == total_lines, (
        f"line-conservation invariant violated: "
        f"malformed={out.dropped_malformed_line_count}, "
        f"records={len(out.records)}, "
        f"non_assistant={out.dropped_non_assistant_count}, "
        f"blank_inferred={dropped_blank_inferred}, "
        f"total={total_lines}"
    )
