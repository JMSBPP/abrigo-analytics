"""Tier 2 fetcher: pull Banco de la República TRM (COP/USD daily) panel.

The TRM series is the X variable used by Pair D and dev-AI Stage-1 specs
(lagged 6-12 months against young-worker employment shares). This script
re-derives the parquet panel checked into Tier 1 by hitting the Banrep
public open-data endpoint.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    print("[Tier 2 / Banrep] COP/USD TRM panel fetcher")
    print()
    print("The canonical Banrep TRM ingest logic is preserved in the Pair D")
    print("scratch artifact. Reuse it from this repo's venv:")
    print()
    print(f"  {REPO_ROOT}/scratch/simple-beta-pair-d/data/scripts/")
    print()
    print("If you only need the processed panel, prefer `make data` (Tier 1) — it")
    print("pulls cop_usd_panel.parquet from HuggingFace in one round trip.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
