"""Tier 1 fetcher: pull processed parquet panels from the public HuggingFace dataset.

Usage:
    python scripts/fetch_data.py --tier 1

Tier 1 ships ~1 MB of analysis-ready panels. For Tier 2 (raw DANE / Banrep / on-chain)
or Tier 3 (re-derivation), see fetch_geih.py / fetch_banrep.py / fetch_onchain.py /
build_panels.py.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "data" / "manifest.yaml"
PANELS_DIR = REPO_ROOT / "data" / "panels"


def load_manifest() -> dict:
    with MANIFEST.open() as f:
        return yaml.safe_load(f)


def fetch_tier1() -> None:
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        sys.exit(
            "huggingface_hub not installed. Run `make install` "
            "or `uv pip install huggingface-hub`."
        )

    cfg = load_manifest()["huggingface"]
    dataset = cfg["dataset"]
    revision = cfg["revision"]
    files = cfg["files"]

    PANELS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Tier 1] Pulling {len(files)} panels from {dataset}@{revision}...")
    for fname in files:
        local = hf_hub_download(
            repo_id=dataset,
            filename=fname,
            revision=revision,
            repo_type="dataset",
            local_dir=REPO_ROOT / "data",
        )
        print(f"  ✓ {Path(local).relative_to(REPO_ROOT)}")
    print(f"[Tier 1] Done. Panels available under {PANELS_DIR.relative_to(REPO_ROOT)}/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", type=int, default=1, choices=[1])
    args = parser.parse_args()

    if args.tier == 1:
        fetch_tier1()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
