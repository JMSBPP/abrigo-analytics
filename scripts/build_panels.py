"""Tier 3 builder: re-derive processed parquet panels from Tier 2 raw.

Two modes:

    python scripts/build_panels.py                       # build from raw
    python scripts/build_panels.py --verify-against-tier1  # build + hash-check

In verify mode, after re-derivation each output is SHA256-compared to the
HuggingFace-published Tier 1 file (per data/manifest.yaml). Any mismatch is
fatal — use this as the canonical reproducibility check.

This script delegates to the canonical per-iteration ingest engines preserved
under scratch/ and notebooks/<iter>/data/scripts/. It centralizes the
orchestration so a cloner has one entry point.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PANELS = REPO_ROOT / "data" / "panels"
DOWNLOADS = REPO_ROOT / "data" / "downloads"

# Per-iteration canonical engines (path → engine label).
ENGINES = {
    "pair_d_geih":
        REPO_ROOT / "scratch" / "simple-beta-pair-d" / "data" / "scripts" / "ingest_geih.py",
    "dev_ai_geih_jm":
        REPO_ROOT / "notebooks" / "dev_ai_cost" / "data" / "scripts" / "ingest_geih_section_jm.py",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module: required so @dataclass(frozen=True) can
    # resolve cls.__module__ via sys.modules (Python 3.13 strictness).
    sys.modules[path.stem] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build_pair_d() -> list[Path]:
    engine_path = ENGINES["pair_d_geih"]
    if not engine_path.exists():
        print(f"  ✗ skip pair_d (engine missing: {engine_path})")
        return []

    print(f"[Tier 3 / pair_d] running {engine_path.name}")
    engine = _load(engine_path)
    # Redirect engine I/O to repo-root data/ paths.
    engine.DOWNLOADS = DOWNLOADS
    PANELS.mkdir(parents=True, exist_ok=True)
    engine.OUT_BROAD = PANELS / "pair_d" / "geih_young_workers_services_share.parquet"
    engine.OUT_NARROW = PANELS / "pair_d" / "geih_young_workers_narrow_share.parquet"
    engine.OUT_BROAD.parent.mkdir(parents=True, exist_ok=True)
    rc = engine.main()
    if rc != 0:
        sys.exit(f"  ✗ pair_d engine returned non-zero: {rc}")
    return [engine.OUT_BROAD, engine.OUT_NARROW]


def build_dev_ai() -> list[Path]:
    engine_path = ENGINES["dev_ai_geih_jm"]
    if not engine_path.exists():
        print(f"  ✗ skip dev_ai (engine missing: {engine_path})")
        return []

    print(f"[Tier 3 / dev_ai] running {engine_path.name}")
    engine = _load(engine_path)
    engine.DOWNLOADS = DOWNLOADS
    out_dir = PANELS / "dev_ai"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Wire output paths if engine exposes them; otherwise fall back to its defaults.
    for attr in ("OUT_J", "OUT_M", "OUT_PANEL"):
        if hasattr(engine, attr):
            old = getattr(engine, attr)
            setattr(engine, attr, out_dir / Path(old).name)
    rc = engine.main()
    if rc != 0:
        sys.exit(f"  ✗ dev_ai engine returned non-zero: {rc}")
    return [p for p in out_dir.glob("*.parquet")]


def verify(outputs: list[Path]) -> None:
    """Hash-check each rebuilt panel against the Tier 1 SHA256SUMS.json."""
    sums_path = PANELS / "SHA256SUMS.json"
    if not sums_path.exists():
        print(f"  ✗ Tier 1 SHA256SUMS.json missing — run `make data` first")
        sys.exit(1)
    expected = json.loads(sums_path.read_text())
    failed = 0
    for out in outputs:
        rel = out.relative_to(PANELS).as_posix()
        got = sha256(out)
        want = expected.get(rel)
        if want is None:
            print(f"  ?  {rel}  (no Tier 1 reference — new panel)")
            continue
        if got != want:
            print(f"  ✗  {rel}  expected {want[:12]}…, got {got[:12]}…")
            failed += 1
        else:
            print(f"  ✓  {rel}  {got[:12]}…")
    if failed:
        sys.exit(f"\n  {failed} panels did NOT match Tier 1 — investigate before trusting")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-against-tier1", action="store_true")
    parser.add_argument("--only", choices=["pair_d", "dev_ai"], default=None)
    args = parser.parse_args()

    outputs: list[Path] = []
    if args.only in (None, "pair_d"):
        outputs += build_pair_d()
    if args.only in (None, "dev_ai"):
        outputs += build_dev_ai()

    print()
    print(f"[Tier 3] re-derived {len(outputs)} panels")
    for o in outputs:
        if o.exists():
            print(f"  {o.relative_to(REPO_ROOT)}  ({o.stat().st_size:,} bytes)")

    if args.verify_against_tier1:
        print()
        print("[Verify] hash-checking against Tier 1 SHA256SUMS.json…")
        verify(outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
