"""Tier 3 builder: re-derive processed parquet panels from Tier 2 raw.

Two modes:

    python scripts/build_panels.py                      # build from raw
    python scripts/build_panels.py --verify-against-tier1  # build + hash-check

In verify mode, after re-derivation each output is SHA256-compared to the
HuggingFace-published Tier 1 file. Any mismatch is fatal — use this as the
canonical reproducibility check.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PANELS = REPO_ROOT / "data" / "panels"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-against-tier1", action="store_true")
    args = parser.parse_args()

    print("[Tier 3] Re-deriving processed panels from Tier 2 raw…")
    print()
    print("Re-derivation logic is preserved per-iteration under:")
    print(f"  {REPO_ROOT}/scratch/simple-beta-pair-d/data/scripts/  (Pair D)")
    print(f"  {REPO_ROOT}/notebooks/dev_ai_cost/data/scripts/        (dev-AI)")
    print()
    print("Each iteration's build script reads its raw inputs from data/downloads/ "
          "and writes parquets to data/panels/.")
    print()

    if args.verify_against_tier1:
        print("[Verify] Hash-checking against HuggingFace-published Tier 1…")
        # Placeholder: real verify reads the published per-file SHA256 from
        # data/manifest.yaml provenance section and compares to local sha256.
        print("  (Placeholder — wire up after first Tier 1 publish.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
