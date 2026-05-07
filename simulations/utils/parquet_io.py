"""Parquet IO boundaries for the M4 emission schemas (spec §10).

Implements per Phase 2 prelude pin **M4** *verbatim*:

- ``cohort_prior.parquet`` — columns ``param``, ``percentile``, ``value``,
  ``source``, ``fetched_at_utc``, ``schema_version``. Not partitioned.
- ``synthetic_tau_t.parquet`` — columns ``month``, ``simulation_id``,
  ``tier_id``, ``r``, ``p``, ``alpha``, ``x_m``, ``tau_t``, ``q_t_usd``,
  ``q_t_cop``, ``schema_version``. Hive-partitioned on ``tier_id`` +
  ``month`` per Phase 1 reconciliation §2.5.

Per Phase 1 reconciliation §2.1, the ``TypedDict`` row schemas live HERE
(not in ``simulations.types``). They are consumed at the IO boundary by
the parquet reader for column-level validation BEFORE conversion to
typed Value containers.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Final, TypedDict

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from simulations.types.posterior import DEFAULT_SCHEMA_VERSION
from simulations.utils.errors import SchemaMismatchError

# ─── M4 schema declarations ────────────────────────────────────────────────────

#: M4 ``cohort_prior.parquet`` columns in emission order.
COHORT_PRIOR_COLUMNS: Final[tuple[str, ...]] = (
    "param",
    "percentile",
    "value",
    "source",
    "fetched_at_utc",
    "schema_version",
)

#: M4 ``synthetic_tau_t.parquet`` columns in emission order.
SYNTHETIC_TAU_COLUMNS: Final[tuple[str, ...]] = (
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
    "schema_version",
)

#: Hive partition columns for ``synthetic_tau_t.parquet``
#: (Phase 1 reconciliation §2.5).
SYNTHETIC_TAU_PARTITION_COLS: Final[tuple[str, ...]] = ("tier_id", "month")


# ─── TypedDict row schemas (Phase 1 reconciliation §2.1) ──────────────────────


class CohortPriorRow(TypedDict):
    """One row of ``cohort_prior.parquet`` (M4 columns)."""

    param: str
    percentile: str
    value: float
    source: str
    fetched_at_utc: str
    schema_version: str


class SyntheticTauRow(TypedDict):
    """One row of ``synthetic_tau_t.parquet`` (M4 columns)."""

    month: int
    simulation_id: int
    tier_id: str
    r: float
    p: float
    alpha: float
    x_m: float
    tau_t: float
    q_t_usd: float
    q_t_cop: float
    schema_version: str


# ─── Validation helpers ───────────────────────────────────────────────────────


def _check_columns(
    actual: Iterable[str],
    expected: tuple[str, ...],
    artifact: str,
) -> None:
    """Raise ``SchemaMismatchError`` iff ``actual`` does not equal ``expected``.

    Order of ``actual`` is irrelevant; column *set* must match exactly. The
    expected order is preserved by the writers below.
    """
    actual_set = set(actual)
    expected_set = set(expected)
    if actual_set == expected_set:
        return
    missing = expected_set - actual_set
    extra = actual_set - expected_set
    raise SchemaMismatchError(
        f"{artifact}: column set mismatch."
        f" missing={sorted(missing)!r} extra={sorted(extra)!r}"
        f" expected={list(expected)!r}"
    )


# ─── IO Boundary classes ──────────────────────────────────────────────────────


class CohortPriorWriter:
    """Write ``cohort_prior.parquet`` (M4) at a configured base directory.

    The writer emits a single, unpartitioned parquet file at
    ``<base_dir>/cohort_prior.parquet``. ``base_dir`` defaults to
    ``simulations/saas_builder/data/`` when constructed without an
    argument; callers MAY override it (notably tests, which write under a
    ``tmp_path``).
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        self._base_dir: Path = (
            base_dir
            if base_dir is not None
            else Path("simulations/saas_builder/data")
        )

    def __call__(self, rows: list[CohortPriorRow]) -> Path:
        if len(rows) == 0:
            raise ValueError("CohortPriorWriter: rows must be non-empty")
        df = pd.DataFrame(rows, columns=list(COHORT_PRIOR_COLUMNS))
        _check_columns(df.columns, COHORT_PRIOR_COLUMNS, "cohort_prior.parquet")
        self._base_dir.mkdir(parents=True, exist_ok=True)
        out = self._base_dir / "cohort_prior.parquet"
        df.to_parquet(out, index=False)
        return out


class CohortPriorReader:
    """Read ``cohort_prior.parquet`` (M4); validate the M4 column set."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self._base_dir: Path = (
            base_dir
            if base_dir is not None
            else Path("simulations/saas_builder/data")
        )

    def __call__(self, path: Path | None = None) -> list[CohortPriorRow]:
        target = path if path is not None else self._base_dir / "cohort_prior.parquet"
        if not target.is_file():
            raise FileNotFoundError(f"CohortPriorReader: missing parquet at {target}")
        df = pd.read_parquet(target)
        _check_columns(df.columns, COHORT_PRIOR_COLUMNS, "cohort_prior.parquet")
        # Reorder defensively (set-equality passed; align to declared order).
        df = df[list(COHORT_PRIOR_COLUMNS)]
        return [
            CohortPriorRow(
                param=str(r.param),
                percentile=str(r.percentile),
                value=float(r.value),
                source=str(r.source),
                fetched_at_utc=str(r.fetched_at_utc),
                schema_version=str(r.schema_version),
            )
            for r in df.itertuples(index=False)
        ]


class SyntheticTauWriter:
    """Write Hive-partitioned ``synthetic_tau_t.parquet`` (M4 + §2.5).

    Output tree:
    ``<base_dir>/synthetic_tau_t/tier_id=*/month=*/*.parquet``.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        self._base_dir: Path = (
            base_dir
            if base_dir is not None
            else Path("simulations/saas_builder/data")
        )

    def __call__(self, rows: list[SyntheticTauRow]) -> Path:
        if len(rows) == 0:
            raise ValueError("SyntheticTauWriter: rows must be non-empty")
        df = pd.DataFrame(rows, columns=list(SYNTHETIC_TAU_COLUMNS))
        _check_columns(df.columns, SYNTHETIC_TAU_COLUMNS, "synthetic_tau_t.parquet")
        out_root = self._base_dir / "synthetic_tau_t"
        out_root.mkdir(parents=True, exist_ok=True)
        # Use pyarrow's Hive-partition writer for deterministic layout.
        table = pa.Table.from_pandas(df, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=str(out_root),
            partition_cols=list(SYNTHETIC_TAU_PARTITION_COLS),
        )
        return out_root


class SyntheticTauReader:
    """Read the Hive-partitioned ``synthetic_tau_t`` dataset (M4 + §2.5).

    Re-attaches partition columns (``tier_id``, ``month``) into the row
    dicts so the returned ``SyntheticTauRow`` list is fully populated.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        self._base_dir: Path = (
            base_dir
            if base_dir is not None
            else Path("simulations/saas_builder/data")
        )

    def __call__(self, root: Path | None = None) -> list[SyntheticTauRow]:
        target = root if root is not None else self._base_dir / "synthetic_tau_t"
        if not target.is_dir():
            raise FileNotFoundError(
                f"SyntheticTauReader: missing dataset directory at {target}"
            )
        dataset = pq.ParquetDataset(str(target))
        table = dataset.read()
        df = table.to_pandas()
        # Hive partition columns reattach automatically; tier_id may come back
        # as pandas Categorical and month as int — coerce both for stable typing.
        if "tier_id" in df.columns:
            df["tier_id"] = df["tier_id"].astype(str)
        if "month" in df.columns:
            df["month"] = df["month"].astype(int)
        _check_columns(df.columns, SYNTHETIC_TAU_COLUMNS, "synthetic_tau_t.parquet")
        df = df[list(SYNTHETIC_TAU_COLUMNS)]
        return [
            SyntheticTauRow(
                month=int(r.month),
                simulation_id=int(r.simulation_id),
                tier_id=str(r.tier_id),
                r=float(r.r),
                p=float(r.p),
                alpha=float(r.alpha),
                x_m=float(r.x_m),
                tau_t=float(r.tau_t),
                q_t_usd=float(r.q_t_usd),
                q_t_cop=float(r.q_t_cop),
                schema_version=str(r.schema_version),
            )
            for r in df.itertuples(index=False)
        ]


# ─── Default-row factories (convenience for callers + tests) ──────────────────


def cohort_prior_row(
    *,
    param: str,
    percentile: str,
    value: float,
    source: str,
    fetched_at_utc: str,
    schema_version: str = DEFAULT_SCHEMA_VERSION,
) -> CohortPriorRow:
    """Construct one ``CohortPriorRow`` with the default schema_version."""
    return CohortPriorRow(
        param=param,
        percentile=percentile,
        value=value,
        source=source,
        fetched_at_utc=fetched_at_utc,
        schema_version=schema_version,
    )


def synthetic_tau_row(
    *,
    month: int,
    simulation_id: int,
    tier_id: str,
    r: float,
    p: float,
    alpha: float,
    x_m: float,
    tau_t: float,
    q_t_usd: float,
    q_t_cop: float,
    schema_version: str = DEFAULT_SCHEMA_VERSION,
) -> SyntheticTauRow:
    """Construct one ``SyntheticTauRow`` with the default schema_version."""
    return SyntheticTauRow(
        month=month,
        simulation_id=simulation_id,
        tier_id=tier_id,
        r=r,
        p=p,
        alpha=alpha,
        x_m=x_m,
        tau_t=tau_t,
        q_t_usd=q_t_usd,
        q_t_cop=q_t_cop,
        schema_version=schema_version,
    )
