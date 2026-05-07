"""IO-Boundary unit tests for ``simulations.utils``.

Covers parquet round-trip + dtype enforcement at the writer boundary,
JSON round-trip via Pydantic, the audit-block sha256 helper (path-order
invariance + str/Path acceptance), and the typed error surfaces
(``SchemaMismatchError`` on column drift; ``FileNotFoundError`` on
empty / missing dataset paths per the I4-fix).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from simulations.types.posterior import ZCapPinned
from simulations.utils.audit_block import AuditBlockHasher, compute_audit_block
from simulations.utils.errors import SchemaMismatchError
from simulations.utils.json_io import ZCapPinnedReader, ZCapPinnedWriter
from simulations.utils.parquet_io import (
    COHORT_PRIOR_COLUMNS,
    SYNTHETIC_TAU_COLUMNS,
    CohortPriorReader,
    CohortPriorRow,
    CohortPriorWriter,
    SyntheticTauReader,
    SyntheticTauWriter,
    cohort_prior_row,
    synthetic_tau_row,
)


# ─── Cohort prior parquet round-trip ──────────────────────────────────────────


class TestCohortPriorIO:
    def test_cohort_prior_round_trip(self, tmp_path: Path) -> None:
        """Write 3 rows of cohort_prior and read back with all columns intact."""
        rows: list[CohortPriorRow] = [
            cohort_prior_row(
                param=p,
                percentile=q,
                value=v,
                source="spec_5_2",
                fetched_at_utc="2026-05-07T00:00:00Z",
            )
            for p, q, v in [
                ("alpha", "p50", 2.0),
                ("alpha", "p90", 2.5),
                ("p_in_sonnet", "pin", 3.0),
            ]
        ]
        writer = CohortPriorWriter(base_dir=tmp_path)
        writer(rows)
        reader = CohortPriorReader(base_dir=tmp_path)
        recovered = reader()
        assert len(recovered) == 3
        recovered_sorted = sorted(recovered, key=lambda r: (r["param"], r["percentile"]))
        original_sorted = sorted(rows, key=lambda r: (r["param"], r["percentile"]))
        for got, want in zip(recovered_sorted, original_sorted):
            assert got == want

    def test_cohort_prior_writer_empty_raises(self, tmp_path: Path) -> None:
        """Empty rows list rejected."""
        with pytest.raises(ValueError, match="non-empty"):
            CohortPriorWriter(base_dir=tmp_path)([])

    def test_cohort_prior_reader_missing_file_raises(self, tmp_path: Path) -> None:
        """Reading from an empty directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="missing parquet"):
            CohortPriorReader(base_dir=tmp_path)()

    def test_cohort_prior_reader_schema_mismatch_extra_column(
        self, tmp_path: Path
    ) -> None:
        """Reader raises SchemaMismatchError when on-disk parquet has extra column."""
        # Hand-craft a parquet with an extra column.
        df = pd.DataFrame(
            {
                "param": ["alpha"],
                "percentile": ["p50"],
                "value": [2.0],
                "source": ["s"],
                "fetched_at_utc": ["t"],
                "schema_version": ["v1.0"],
                "rogue_extra": ["nope"],
            }
        )
        out = tmp_path / "cohort_prior.parquet"
        df.to_parquet(out, index=False)
        with pytest.raises(SchemaMismatchError, match="extra"):
            CohortPriorReader(base_dir=tmp_path)()

    def test_cohort_prior_reader_schema_mismatch_missing_column(
        self, tmp_path: Path
    ) -> None:
        """Reader raises SchemaMismatchError when on-disk parquet is missing a column."""
        df = pd.DataFrame(
            {
                "param": ["alpha"],
                "percentile": ["p50"],
                "value": [2.0],
                "source": ["s"],
                # Missing fetched_at_utc + schema_version.
            }
        )
        out = tmp_path / "cohort_prior.parquet"
        df.to_parquet(out, index=False)
        with pytest.raises(SchemaMismatchError, match="missing"):
            CohortPriorReader(base_dir=tmp_path)()


# ─── Synthetic-tau Hive-partitioned parquet round-trip ────────────────────────


def _make_tau_rows(n_per_combo: int = 1) -> list:
    """Build 12 SyntheticTauRows: 3 tiers × 4 months × n_per_combo."""
    rows = []
    sim_id = 0
    for tier in ("pro", "max_5x", "max_20x"):
        for month in (1, 2, 3, 4):
            for _ in range(n_per_combo):
                rows.append(
                    synthetic_tau_row(
                        month=month,
                        simulation_id=sim_id,
                        tier_id=tier,
                        r=4.0,
                        p=0.5,
                        alpha=2.0,
                        x_m=1.0,
                        tau_t=1234.0,
                        q_t_usd=20.0,
                        q_t_cop=80000.0,
                    )
                )
                sim_id += 1
    return rows


class TestSyntheticTauIO:
    def test_synthetic_tau_round_trip_via_hive_tree(self, tmp_path: Path) -> None:
        """Write 12 mixed-tier mixed-month rows; read back with partitions intact."""
        rows = _make_tau_rows()
        SyntheticTauWriter(base_dir=tmp_path)(rows)
        recovered = SyntheticTauReader(base_dir=tmp_path)()
        assert len(recovered) == 12
        # Confirm partition columns survived.
        tiers = {r["tier_id"] for r in recovered}
        months = {r["month"] for r in recovered}
        assert tiers == {"pro", "max_5x", "max_20x"}
        assert months == {1, 2, 3, 4}

    def test_synthetic_tau_dtype_enforcement(self, tmp_path: Path) -> None:
        """Float-typed `month=4.0` input lands on disk as int (Hive dir `month=4/`)."""
        # SyntheticTauRow is a TypedDict; runtime ignores the int annotation.
        # We construct via dict() to bypass the helper's keyword validation.
        rogue_row: dict[str, object] = {
            "month": 4.0,  # caller passed float
            "simulation_id": 0,
            "tier_id": "pro",
            "r": 4.0,
            "p": 0.5,
            "alpha": 2.0,
            "x_m": 1.0,
            "tau_t": 1234.0,
            "q_t_usd": 20.0,
            "q_t_cop": 80000.0,
            "schema_version": "v1.0",
        }
        SyntheticTauWriter(base_dir=tmp_path)(cast(Any, [rogue_row]))
        # The Hive partition directory must be `month=4/`, not `month=4.0/`.
        partition_dirs = list(
            (tmp_path / "synthetic_tau_t" / "tier_id=pro").glob("month=*")
        )
        assert len(partition_dirs) == 1
        assert partition_dirs[0].name == "month=4"
        # Reader-side: month is int.
        recovered = SyntheticTauReader(base_dir=tmp_path)()
        assert recovered[0]["month"] == 4
        assert isinstance(recovered[0]["month"], int)

    def test_synthetic_tau_reader_empty_dir_raises(self, tmp_path: Path) -> None:
        """Reading a missing dataset directory raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="missing dataset"):
            SyntheticTauReader(base_dir=tmp_path)()

    def test_synthetic_tau_reader_empty_existing_dir_raises(
        self, tmp_path: Path
    ) -> None:
        """An existing but empty dataset dir surfaces the I4 'no parquet files' guard."""
        empty_root = tmp_path / "synthetic_tau_t"
        empty_root.mkdir()
        with pytest.raises(FileNotFoundError, match="no parquet files"):
            SyntheticTauReader(base_dir=tmp_path)()

    def test_synthetic_tau_reader_schema_mismatch(self, tmp_path: Path) -> None:
        """A parquet emitted with the wrong column set raises SchemaMismatchError."""
        out_root = tmp_path / "synthetic_tau_t" / "tier_id=pro" / "month=1"
        out_root.mkdir(parents=True)
        # Drop the schema_version column on purpose.
        df = pd.DataFrame(
            {
                "simulation_id": [0],
                "r": [4.0],
                "p": [0.5],
                "alpha": [2.0],
                "x_m": [1.0],
                "tau_t": [1234.0],
                "q_t_usd": [20.0],
                "q_t_cop": [80000.0],
                # missing schema_version
            }
        )
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_table(table, out_root / "part-0.parquet")
        with pytest.raises(SchemaMismatchError):
            SyntheticTauReader(base_dir=tmp_path)()


# ─── ZCapPinned JSON round-trip ───────────────────────────────────────────────


def _zcap_sample() -> ZCapPinned:
    return ZCapPinned(
        Z_cop_per_month=120_000.0,
        ci_95_lo=110_000.0,
        ci_95_hi=130_000.0,
        audit_block="a" * 64,
        tier_mix={"pro": 0.20, "max_5x": 0.50, "max_20x": 0.30},
    )


class TestZCapPinnedJsonIO:
    def test_zcap_pinned_round_trip(self, tmp_path: Path) -> None:
        """Pydantic-validated round trip preserves every M4 field."""
        target = tmp_path / "Z_cap_pinned.json"
        z = _zcap_sample()
        ZCapPinnedWriter()(z, target)
        recovered = ZCapPinnedReader()(target)
        assert recovered == z

    def test_zcap_pinned_reader_missing_file(self, tmp_path: Path) -> None:
        """Reading a missing JSON raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="missing JSON"):
            ZCapPinnedReader()(tmp_path / "absent.json")

    def test_zcap_pinned_reader_schema_drift_extra_field(self, tmp_path: Path) -> None:
        """Extra top-level field surfaces as SchemaMismatchError."""
        target = tmp_path / "Z_cap_pinned.json"
        payload = {
            "Z_cop_per_month": 100.0,
            "ci_95_lo": 90.0,
            "ci_95_hi": 110.0,
            "audit_block": "0" * 64,
            "tier_mix": {"pro": 0.2, "max_5x": 0.5, "max_20x": 0.3},
            "schema_version": "v1.0",
            "rogue_extra": "nope",
        }
        target.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(SchemaMismatchError, match="extra"):
            ZCapPinnedReader()(target)

    def test_zcap_pinned_reader_top_level_must_be_object(self, tmp_path: Path) -> None:
        """A JSON list at top level is rejected with SchemaMismatchError."""
        target = tmp_path / "Z_cap_pinned.json"
        target.write_text(json.dumps(["nope"]), encoding="utf-8")
        with pytest.raises(SchemaMismatchError, match="object"):
            ZCapPinnedReader()(target)

    def test_zcap_pinned_reader_tier_mix_drift(self, tmp_path: Path) -> None:
        """tier_mix with wrong keys surfaces as SchemaMismatchError."""
        target = tmp_path / "Z_cap_pinned.json"
        payload = {
            "Z_cop_per_month": 100.0,
            "ci_95_lo": 90.0,
            "ci_95_hi": 110.0,
            "audit_block": "0" * 64,
            "tier_mix": {"a": 0.5, "b": 0.5},
            "schema_version": "v1.0",
        }
        target.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(SchemaMismatchError, match="tier_mix"):
            ZCapPinnedReader()(target)


# ─── Audit-block sha256 helper ────────────────────────────────────────────────


class TestAuditBlock:
    def _make_files(self, tmp_path: Path) -> tuple[Path, Path, Path]:
        a = tmp_path / "a.txt"
        b = tmp_path / "b.txt"
        c = tmp_path / "c.txt"
        a.write_bytes(b"alpha")
        b.write_bytes(b"beta")
        c.write_bytes(b"gamma")
        return a, b, c

    def test_compute_audit_block_returns_64_lowercase_hex(self, tmp_path: Path) -> None:
        """Output is a 64-char lowercase hex string."""
        a, _, _ = self._make_files(tmp_path)
        h = compute_audit_block([a])
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_compute_audit_block_path_order_invariant(self, tmp_path: Path) -> None:
        """Reordering input paths does not change the digest."""
        a, b, c = self._make_files(tmp_path)
        h1 = compute_audit_block([a, b, c])
        h2 = compute_audit_block([c, a, b])
        h3 = compute_audit_block([b, c, a])
        assert h1 == h2 == h3

    def test_compute_audit_block_str_or_path_mixed(self, tmp_path: Path) -> None:
        """Accepts a mixed list of str and Path inputs."""
        a, b, _ = self._make_files(tmp_path)
        h_str = compute_audit_block([str(a), str(b)])
        h_mixed = compute_audit_block([str(a), b])
        h_path = compute_audit_block([a, b])
        assert h_str == h_mixed == h_path

    def test_compute_audit_block_empty_raises(self) -> None:
        """Empty path list rejected."""
        with pytest.raises(ValueError, match="non-empty"):
            compute_audit_block([])

    def test_compute_audit_block_missing_file_raises(self, tmp_path: Path) -> None:
        """A non-existent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="not a regular file"):
            compute_audit_block([tmp_path / "absent.txt"])

    def test_compute_audit_block_content_sensitive(self, tmp_path: Path) -> None:
        """Mutating one byte changes the digest."""
        a = tmp_path / "a.txt"
        a.write_bytes(b"alpha")
        h0 = compute_audit_block([a])
        a.write_bytes(b"alphb")
        h1 = compute_audit_block([a])
        assert h0 != h1

    def test_audit_block_hasher_class_matches_function(self, tmp_path: Path) -> None:
        """AuditBlockHasher class delegates to compute_audit_block."""
        a, b, _ = self._make_files(tmp_path)
        free_hash = compute_audit_block([a, b])
        cls_hash = AuditBlockHasher()((a, b))
        assert free_hash == cls_hash

    def test_compute_audit_block_known_value(self, tmp_path: Path) -> None:
        """Single-file digest matches the documented stream-format."""
        a = tmp_path / "x.txt"
        a.write_bytes(b"hello")
        expected = hashlib.sha256(f"--- {a}\n".encode("utf-8") + b"hello").hexdigest()
        assert compute_audit_block([a]) == expected


# ─── Schema-set sanity (M4 column tuples are immutable & complete) ────────────


class TestM4Schemas:
    def test_cohort_prior_columns_present(self) -> None:
        """COHORT_PRIOR_COLUMNS contains the M4 spec §10 columns."""
        assert "param" in COHORT_PRIOR_COLUMNS
        assert "percentile" in COHORT_PRIOR_COLUMNS
        assert "value" in COHORT_PRIOR_COLUMNS
        assert "source" in COHORT_PRIOR_COLUMNS
        assert "fetched_at_utc" in COHORT_PRIOR_COLUMNS

    def test_synthetic_tau_columns_present(self) -> None:
        """SYNTHETIC_TAU_COLUMNS contains the M4 spec §10 columns."""
        for c in (
            "month",
            "simulation_id",
            "tier_id",
            "r",
            "p",
            "alpha",
            "x_m",
            "tau_t",
            "q_t_usd",
            "q_t_cop",
        ):
            assert c in SYNTHETIC_TAU_COLUMNS, f"missing column {c!r}"
