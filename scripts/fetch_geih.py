"""Tier 2 fetcher: download all DANE GEIH ZIPs pinned in the manifest.

Reads scratch/simple-beta-pair-d/data/dane_geih_manifest.json (the Pair D
Option-α' canonical 2015-01 → 2026-03 window pin) via the canonical
ingest engine, and pulls each ZIP into data/downloads/. Re-running is
idempotent — already-downloaded files of the expected size are skipped by
the engine's _http_get.

This wrapper imports the canonical engine living under scratch/ (the
historical record of where the script was authored) and only runs its
download phase, leaving extraction + parquet-build to scripts/build_panels.py.

Total time: ~30 min on a residential connection.
Total bytes: ~5.3 GB across ~270 ZIPs in the active window.
"""
from __future__ import annotations

import dataclasses
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = REPO_ROOT / "scratch" / "simple-beta-pair-d" / "data" / "scripts" / "ingest_geih.py"
DOWNLOADS = REPO_ROOT / "data" / "downloads"


def _load_canonical():
    """Import the canonical ingest engine from scratch/ as a module."""
    if not CANONICAL.exists():
        sys.exit(f"Canonical ingest script missing: {CANONICAL}")
    spec = importlib.util.spec_from_file_location("ingest_geih", CANONICAL)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module: required so @dataclass(frozen=True) can
    # resolve cls.__module__ via sys.modules (Python 3.13 strictness).
    sys.modules["ingest_geih"] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    engine = _load_canonical()

    # Re-route the engine's hardcoded scratch/ download path to data/downloads/.
    # The engine's _ingest_month() will use this when caching each ZIP.
    engine.DOWNLOADS = DOWNLOADS
    # The engine resolves cache paths in _build_plans relative to its own
    # DOWNLOADS at build time; rebuild plans, then re-target each FilePlan
    # to data/downloads/ via dataclasses.replace (FilePlan is frozen).
    manifest = engine._load_manifest()
    plans = [
        dataclasses.replace(p, cache_path=DOWNLOADS / p.cache_path.name)
        for p in engine._build_plans(manifest)
    ]

    print(f"[Tier 2 / GEIH] {len(plans)} ZIPs to fetch from DANE")
    print(f"  → {DOWNLOADS}")
    print()

    n_skip = 0
    n_get = 0
    for i, plan in enumerate(plans, 1):
        if plan.cache_path.exists() and plan.cache_path.stat().st_size > 0:
            n_skip += 1
            continue
        print(f"  [{i}/{len(plans)}] {plan.cache_path.name}")
        engine._http_get(plan.download_url, plan.cache_path)
        n_get += 1

    print()
    print(f"  ✓ done: fetched {n_get}, skipped {n_skip} already-cached")
    print(f"  next: `make panels` to extract + build parquet panels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
