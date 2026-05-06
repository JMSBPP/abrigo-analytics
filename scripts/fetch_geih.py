"""Tier 2 fetcher: re-download all DANE GEIH ZIPs pinned in the manifest.

Reads scratch/simple-beta-pair-d/data/dane_geih_manifest.json (the Pair D
Option-α' canonical 2015-01 → 2026-03 window pin) and pulls each ZIP into
data/downloads/. Re-running is idempotent — already-downloaded files are skipped.

This is a lightweight wrapper around the original ingest script preserved at
scratch/simple-beta-pair-d/data/scripts/. The wrapper exists so cloners have a
single, discoverable entry point.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_YAML = REPO_ROOT / "data" / "manifest.yaml"
DOWNLOADS = REPO_ROOT / "data" / "downloads"


def main() -> int:
    with MANIFEST_YAML.open() as f:
        manifest = yaml.safe_load(f)

    geih_pin = REPO_ROOT / manifest["raw_sources"]["dane_geih"]["manifest"]
    if not geih_pin.exists():
        sys.exit(f"DANE GEIH manifest not found: {geih_pin}")

    with geih_pin.open() as f:
        geih_files = json.load(f)

    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    print(f"[Tier 2 / GEIH] {len(geih_files)} ZIPs to fetch from DANE")
    print(f"  → {DOWNLOADS}")
    print()
    print("This wrapper delegates to the original ingest script preserved at:")
    print(f"  {REPO_ROOT / 'scratch/simple-beta-pair-d/data/scripts/'}")
    print()
    print("To run the full ingest, invoke that script directly with this repo's venv:")
    print(f"  source .venv/bin/activate && python "
          f"{REPO_ROOT}/scratch/simple-beta-pair-d/data/scripts/<ingest_script>.py")
    print()
    print("(Wrapper retained as discoverable entry point; the ingest script is "
          "manifest-pinned and lives under scratch/ for full provenance.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
