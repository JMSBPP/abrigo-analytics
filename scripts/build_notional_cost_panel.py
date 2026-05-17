"""Tier-3 CLI: build data/panels/notional_cost_panel.parquet.

Single orchestration point that imports across utils + modules tiers
(spec v0.2.1 §3.3, §3.5). This is the only module in the dev_ai_cost_v2
pipeline permitted to wire IO Boundary (jsonl_io) together with Callable
tier (anthropic_pricing, panel_builder); per spec §3.3 the CLI is the
intentional cross-tier integration point and is NOT a tier-import-rule
violation.

Reads:
    --projects-root  Anthropic Claude Code JSONL transcript root.
    --litellm-cache  Pinned LiteLLM model_prices_and_context_window.json.
    --trm-path       Banrep daily TRM parquet (produced by fetch_banrep.py).

Writes:
    --out            Daily notional cost panel parquet (one row per UTC
                     date with cost in both USD and COP).

Exit codes:
    0  Panel written successfully.
    !0 Any reconciliation, schema-drift, SHA-mismatch, or IO failure
       propagates as a non-zero exit via uncaught exception (SystemExit
       wraps the traceback so the operator sees the root cause).
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import polars as pl

from simulations.dev_ai_cost_v2.anthropic_pricing import (
    LITELLM_SHA_PINNED,
    PricingTable,
)
from simulations.dev_ai_cost_v2.jsonl_io import JSONLReader
from simulations.dev_ai_cost_v2.panel_builder import build_daily_panel

REPO_ROOT = Path(__file__).resolve().parent.parent


def _parse_args() -> argparse.Namespace:
    """Parse and return CLI arguments.

    Contract:
        * ``--since`` and ``--until`` are required ISO-8601 dates
          (``date.fromisoformat`` raises ``ValueError`` on malformed input,
          which argparse converts to a non-zero exit).
        * All path arguments are typed as ``pathlib.Path``; defaults are
          resolved relative to ``REPO_ROOT``.
        * Missing ``--since`` or ``--until`` causes argparse to print
          usage and exit with code 2.
    """
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since", type=date.fromisoformat, required=True)
    p.add_argument("--until", type=date.fromisoformat, required=True)
    p.add_argument(
        "--projects-root",
        default=Path("~/.claude/projects").expanduser(),
        type=Path,
    )
    p.add_argument(
        "--litellm-cache",
        default=REPO_ROOT / "data" / "raw" / "litellm_model_prices.json",
        type=Path,
    )
    p.add_argument(
        "--trm-path",
        default=REPO_ROOT / "data" / "raw" / "banrep_trm_daily.parquet",
        type=Path,
    )
    p.add_argument(
        "--out",
        default=REPO_ROOT / "data" / "panels" / "notional_cost_panel.parquet",
        type=Path,
    )
    return p.parse_args()


def main() -> int:
    """Orchestrate the panel build end-to-end.

    Contract:
        * Creates ``args.out.parent`` if missing (CORRECTIONS-W: the
          ``data/panels/`` directory does not exist on a fresh clone).
        * Loads the LiteLLM pricing table at the spec-pinned SHA via
          ``PricingTable.from_litellm_sha(LITELLM_SHA_PINNED, ...)``.
          Passing the pinned SHA as the first positional argument (NOT
          ``skip_sha_check=True``) enforces reproducibility — any drift
          in the cached JSON raises ``PricingSchemaError`` and exits
          non-zero.
        * Reads the daily TRM parquet via ``pl.read_parquet``; a missing
          file raises ``FileNotFoundError``.
        * Materializes JSONL records via ``JSONLReader`` (the only IO
          Boundary call in this orchestration).
        * Joins records × pricing × TRM via ``build_daily_panel``;
          forward-fill is FORBIDDEN by the panel builder's contract.
        * Writes the resulting parquet and prints a one-line summary
          including ``dropped_rows_count`` and ``dropped_error_count``
          for operator reconciliation.

    Returns:
        ``0`` on success. Any exception (schema drift, SHA mismatch,
        missing file, reconciliation failure inside ``build_daily_panel``)
        propagates uncaught so the operator sees the full traceback and
        the process exits non-zero via the ``__main__`` ``SystemExit``.
    """
    args = _parse_args()

    # CORRECTIONS-W: data/panels/ may not exist on a fresh clone.
    args.out.parent.mkdir(parents=True, exist_ok=True)

    pricing = PricingTable.from_litellm_sha(
        LITELLM_SHA_PINNED, cached_json_path=args.litellm_cache
    )
    trm = pl.read_parquet(args.trm_path)
    reader = JSONLReader()
    records = reader(args.since, args.until, projects_root=args.projects_root)
    panel = build_daily_panel(records, pricing, trm)

    panel.df.write_parquet(args.out)
    print(
        f"[OK] wrote {args.out} ({panel.df.height} rows; "
        f"dropped_rows={panel.dropped_rows_count}, "
        f"dropped_error={panel.dropped_error_count})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
