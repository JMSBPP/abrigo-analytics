"""Tests for ``simulations.dev_ai_cost_v2.jsonl_io.JSONLReader``.

Spec refs:
- ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1 §3.1, §3.5,
  CORRECTIONS-N (extra="forbid" + missing-required schema gate),
  CORRECTIONS-V (UTC half-open + materialized Sequence not Iterator,
  CR FLAG A).
- ``docs/specs/2026-05-16-r6-continuous-stream-simulation-design.md`` v0.1.3
  CORRECTIONS-RR/-TT (uuid field required for R6 pool canonicalization).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from simulations.dev_ai_cost_v2._errors import JSONLSchemaError
from simulations.dev_ai_cost_v2.jsonl_io import JSONLReader
from simulations.dev_ai_cost_v2.types import MessageRecord


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def _valid_row(ts: str = "2026-05-01T12:00:00Z", uuid: str = "msg-uuid-001") -> dict:
    return {
        "timestamp": ts,
        "sessionId": "s1",
        "requestId": "r1",
        "isApiErrorMessage": False,
        "uuid": uuid,  # R6 v0.1.3 CORRECTIONS-RR/-TT
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
        "costUSD": "0.0015",
    }


def test_jsonlreader_emits_sequence_not_iterator(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    _write_jsonl(proj / "session.jsonl", [_valid_row()])
    reader = JSONLReader()
    out = reader(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    # Sequence, not Iterator (CR FLAG A / CORRECTIONS-V).
    assert isinstance(out, list)
    assert len(out) == 1
    assert isinstance(out[0], MessageRecord)
    assert out[0].uuid == "msg-uuid-001"  # R6 amendment
    # Double-iteration property: second pass must equal first.
    first = list(out)
    second = list(out)
    assert first == second


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
    out = JSONLReader()(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out) == 2
    uuids = {r.uuid for r in out}
    assert uuids == {"u1", "u2"}


def test_jsonlreader_raises_on_extra_field(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    bad = _valid_row()
    bad["unknown_extra_field"] = "drift"
    _write_jsonl(proj / "s.jsonl", [bad])
    with pytest.raises(JSONLSchemaError):
        JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_raises_on_missing_uuid(tmp_path: Path) -> None:
    """R6 v0.1.3 CORRECTIONS-RR/-TT — uuid is a required field."""
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    del row["uuid"]
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_warns_on_null_request_id(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    row["requestId"] = None
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.warns(UserWarning, match="request_id"):
        out = JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )
    assert len(out) == 1
    assert out[0].request_id is None


def test_jsonlreader_raises_on_naive_timestamp(tmp_path: Path) -> None:
    """Tz-naive timestamps must be rejected at parse time, not silently shifted.

    Defense in depth against future Anthropic schema drift (if `Z` suffix is
    ever dropped). Code-quality review I-1 (Task 5).
    """
    proj = tmp_path / "projects" / "p1"
    row = _valid_row()
    row["timestamp"] = "2026-05-01T12:00:00"  # tz-naive (no Z)
    _write_jsonl(proj / "s.jsonl", [row])
    with pytest.raises(JSONLSchemaError):
        JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_raises_on_invalid_json(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    (proj / "s.jsonl").write_text('{"not": "closed"\n')
    with pytest.raises(JSONLSchemaError):
        JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "projects",
        )


def test_jsonlreader_raises_on_missing_projects_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        JSONLReader()(
            since=date(2026, 5, 1),
            until=date(2026, 5, 2),
            projects_root=tmp_path / "does_not_exist",
        )


def test_jsonlreader_recurses_subprojects(tmp_path: Path) -> None:
    """rglob walks nested project directories — verifies multi-project case."""
    root = tmp_path / "projects"
    _write_jsonl(root / "p1" / "s1.jsonl", [_valid_row(uuid="a")])
    _write_jsonl(root / "p2" / "nested" / "s2.jsonl", [_valid_row(uuid="b")])
    out = JSONLReader()(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=root,
    )
    assert len(out) == 2
    assert {r.uuid for r in out} == {"a", "b"}


def test_jsonlreader_skips_blank_lines(tmp_path: Path) -> None:
    proj = tmp_path / "projects" / "p1"
    proj.mkdir(parents=True, exist_ok=True)
    with (proj / "s.jsonl").open("w") as f:
        f.write(json.dumps(_valid_row()) + "\n")
        f.write("\n")
        f.write("   \n")
        f.write(json.dumps(_valid_row(uuid="u2")) + "\n")
    out = JSONLReader()(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    assert len(out) == 2


# ─── Hypothesis property: double-iteration equality (CR FLAG A) ──────────────


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
    """Returned Sequence must yield identical contents on repeated iteration.

    Closes CORRECTIONS-V FLAG A: ``Sequence`` not ``Iterator``.
    """
    tmp_path = tmp_path_factory.mktemp("hyp")
    proj = tmp_path / "projects" / "p1"
    rows = [
        _valid_row(uuid=f"u-{uuid_seed}-{i}")
        for i in range(n_rows)
    ]
    if rows:
        _write_jsonl(proj / "s.jsonl", rows)
    else:
        proj.mkdir(parents=True, exist_ok=True)
        (proj / "empty.jsonl").write_text("")
    out = JSONLReader()(
        since=date(2026, 5, 1),
        until=date(2026, 5, 2),
        projects_root=tmp_path / "projects",
    )
    first = list(out)
    second = list(out)
    assert first == second
    assert len(first) == n_rows
