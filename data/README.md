# `data/` — populated, not committed

This directory is gitignored except for `manifest.yaml` and this README.
Run one of the three Make targets to populate it:

| Target | Time | Bytes | Source |
|---|---|---|---|
| `make data` | ~30 sec | ~1 MB | HuggingFace dataset (Tier 1) |
| `make data-raw` | ~30 min | ~5.3 GB | DANE + Banrep (Tier 2) |
| `make data-onchain` | ~10 min | ~50 MB | Celo RPC (Tier 2) |
| `make panels` | ~1 hr | n/a | Local re-derivation (Tier 3) |

After `make data`, the layout is:

```
data/
├── manifest.yaml                                   # canonical sources (committed)
├── README.md                                       # this file (committed)
├── panels/                                         # processed (Tier 1, gitignored)
│   ├── cop_usd_panel.parquet
│   ├── geih_young_workers_section_j_share.parquet
│   ├── geih_young_workers_section_m_share.parquet
│   ├── geih_young_workers_services_share.parquet
│   ├── geih_young_workers_narrow_share.parquet
│   └── panel_combined.parquet
├── downloads/                                      # raw zips (Tier 2, gitignored)
└── onchain/                                        # raw block ranges (Tier 2, gitignored)
```

## Why three tiers?

- **Tier 1** lets a cloner reproduce notebook outputs in seconds without touching
  the issuer portals — useful for review, replication, citation.
- **Tier 2** lets a cloner re-derive everything from canonical free public data,
  guarding against silent rot of the published Tier 1 panels.
- **Tier 3** is the bridge: `make verify` re-derives Tier 1 from Tier 2 and
  hash-checks against the published bytes. A clean `verify` is the strongest
  reproducibility evidence the repo can produce.
