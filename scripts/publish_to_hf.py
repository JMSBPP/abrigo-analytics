"""One-shot publisher: stages processed parquet panels and pushes to HuggingFace.

Run this once after first repo bootstrap (and re-run whenever a new iteration
produces a canonical panel that should be Tier-1 distributed).

Prerequisites:
    1. HuggingFace account: https://huggingface.co/join
    2. Write-scoped access token: https://huggingface.co/settings/tokens
    3. CLI login: `huggingface-cli login` (stores token in ~/.cache/huggingface/)
    4. Dataset repo created: `huggingface-cli repo create abrigo-analytics-panels --type dataset`

Usage:
    python scripts/publish_to_hf.py                 # publish to the pinned repo
    python scripts/publish_to_hf.py --dry-run       # stage locally, no push
    python scripts/publish_to_hf.py --repo USER/REPO  # override target

The script is idempotent: re-running re-uploads files whose contents changed,
no-ops on unchanged files (HuggingFace dedupes by hash).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPO = "JMSBPP/abrigo-analytics-panels"

# Canonical parquet sources — kept inline so this script is the single source
# of truth for what gets published. Add/remove entries as iterations land.
SOURCES = {
    "panels/pair_d/cop_usd_panel.parquet":
        "scratch/simple-beta-pair-d/data/cop_usd_panel.parquet",
    "panels/pair_d/panel_combined.parquet":
        "scratch/simple-beta-pair-d/data/panel_combined.parquet",
    "panels/pair_d/geih_young_workers_services_share.parquet":
        "scratch/simple-beta-pair-d/data/geih_young_workers_services_share.parquet",
    "panels/pair_d/geih_young_workers_narrow_share.parquet":
        "scratch/simple-beta-pair-d/data/geih_young_workers_narrow_share.parquet",
    "panels/dev_ai/cop_usd_panel.parquet":
        "notebooks/dev_ai_cost/data/cop_usd_panel.parquet",
    "panels/dev_ai/panel_combined.parquet":
        "notebooks/dev_ai_cost/data/panel_combined.parquet",
    "panels/dev_ai/geih_young_workers_section_j_share.parquet":
        "notebooks/dev_ai_cost/data/geih_young_workers_section_j_share.parquet",
    "panels/dev_ai/geih_young_workers_section_m_share.parquet":
        "notebooks/dev_ai_cost/data/geih_young_workers_section_m_share.parquet",
}

DATASET_CARD = """---
license: mit
language: [en, es]
tags:
  - econometrics
  - colombia
  - fx
  - employment
  - abrigo
  - structural-econometrics
size_categories:
  - n<1K
---

# Abrigo Analytics — Processed Panels (Tier 1)

Canonical processed parquet panels for the **Abrigo** (Y, M, X) empirical-validation
work. Companion repo (notebooks, specs, plans, scripts):
**https://github.com/JMSBPP/abrigo-analytics**

## Layout

```
panels/
├── pair_d/                                      # Pair D iteration
│   ├── cop_usd_panel.parquet                    # X: COP/USD daily TRM
│   ├── panel_combined.parquet                   # joined Y × X panel (lag-12 ready)
│   ├── geih_young_workers_services_share.parquet  # Y: services-sector share (G–T)
│   └── geih_young_workers_narrow_share.parquet    # Y: narrow J+M+N (BPO sensitivity)
└── dev_ai/                                      # dev-AI Stage-1 iteration
    ├── cop_usd_panel.parquet
    ├── panel_combined.parquet
    ├── geih_young_workers_section_j_share.parquet  # Y: Información y Comunicaciones
    └── geih_young_workers_section_m_share.parquet  # Y: Section M sensitivity
```

## Provenance

- **GEIH** (Y): DANE Gran Encuesta Integrada de Hogares micro-data, 2015-01 → 2026-03,
  Marco-2018 frame, CIIU Rev. 4. Youth band 14–28 (Ley 1622 de 2013).
- **TRM** (X): Banco de la República daily COP/USD reference rate, back-extended
  to 2014-01 to support lag-12 alignment.
- Per-file SHA256 in `SHA256SUMS.json`. Pin a specific revision for citation.

## Reproducibility

These panels are derivable from public free raw sources. The companion repo's
`make data-raw` + `make panels` regenerates them; `make verify` hash-checks
against this dataset. See:

- `data/manifest.yaml` — canonical source URLs
- `scratch/simple-beta-pair-d/data/DATA_PROVENANCE.md` — Pair D provenance
- `notebooks/dev_ai_cost/data/DATA_PROVENANCE.md` — dev-AI provenance

## Verdicts (as of repo bootstrap)

- **Pair D**: PASS, β = +0.137, p ≈ 1.5×10⁻⁸ (HAC-robust, n=134, lag-12).
- **dev-AI Stage-1**: Phase 1 in progress.

See companion repo `memory/` for full iteration state.

## License

MIT for the analytics + tooling. Underlying DANE / Banrep data retains its own
public-domain / open-data licensing.
"""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def stage(stage_dir: Path) -> dict[str, str]:
    """Copy SOURCES into stage_dir/, write SHA256SUMS.json + dataset card."""
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True)

    hashes: dict[str, str] = {}
    missing: list[str] = []

    for dst_rel, src_rel in SOURCES.items():
        src = REPO_ROOT / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dst = stage_dir / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
        hashes[dst_rel] = sha256(dst)
        print(f"  ✓ {src_rel} → {dst_rel} ({hashes[dst_rel][:12]}…)")

    if missing:
        print()
        print(f"  ✗ {len(missing)} sources missing — run `make data-raw && make panels` first:")
        for m in missing:
            print(f"      - {m}")
        sys.exit(1)

    (stage_dir / "panels" / "SHA256SUMS.json").write_text(
        json.dumps(hashes, indent=2, sort_keys=True) + "\n"
    )
    (stage_dir / "README.md").write_text(DATASET_CARD)
    print(f"\n  staged: {len(hashes)} panels + dataset card + SHA256SUMS.json")
    return hashes


def push(stage_dir: Path, repo: str) -> None:
    try:
        from huggingface_hub import upload_folder, whoami
    except ImportError:
        sys.exit("huggingface_hub not installed. `uv pip install huggingface-hub`.")

    # Verify auth before attempting upload — fail fast with a useful pointer.
    import os
    has_env = bool(os.environ.get("HF_TOKEN"))
    try:
        whoami()
    except Exception:
        sys.exit(
            "HuggingFace auth not configured.\n\n"
            "  Either export your token before invoking:\n"
            "      export HF_TOKEN='hf_…'\n"
            "  or run the interactive login (persists to ~/.cache/huggingface/token):\n"
            "      huggingface-cli login\n\n"
            f"  HF_TOKEN env var present: {has_env}\n"
            "  Get a write-scoped token at https://huggingface.co/settings/tokens"
        )

    print(f"\n  pushing to https://huggingface.co/datasets/{repo}…")
    upload_folder(
        folder_path=str(stage_dir),
        repo_id=repo,
        repo_type="dataset",
        commit_message="Tier 1 panel publish",
    )
    print(f"  ✓ live at https://huggingface.co/datasets/{repo}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help=f"target dataset repo (default: {DEFAULT_REPO})")
    parser.add_argument("--dry-run", action="store_true",
                        help="stage locally without pushing to HuggingFace")
    parser.add_argument("--stage-dir", type=Path,
                        default=Path("/tmp/abrigo-hf-stage"))
    args = parser.parse_args()

    print(f"[publish] staging panels at {args.stage_dir}…")
    stage(args.stage_dir)

    if args.dry_run:
        print("\n[publish] --dry-run: skipped HuggingFace push.")
        print(f"  inspect: {args.stage_dir}")
        return 0

    push(args.stage_dir, args.repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
