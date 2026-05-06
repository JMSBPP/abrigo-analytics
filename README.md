# Abrigo Analytics

Empirical-validation half of the **Abrigo** project: structural econometrics,
on-chain panels, and notebook trios driving each (Y, M, X) iteration of a
permissionless convex-hedge instrument family targeting wage-earner exposure
to macro risks that block the wage→capital transition.

The Solidity / settlement half lives separately. This repo is purely Python +
notebooks + research artifacts. **You do not need Foundry, Rust, or any
contract tooling to reproduce any analysis here.**

## Quickstart (3 minutes to first plot)

```bash
# 1. Clone
git clone https://github.com/JMSBPP/abrigo-analytics.git
cd abrigo-analytics

# 2. Create venv (Python 3.13)
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt

# 3. Pull Tier 1 panels from HuggingFace (~30 sec, ~1 MB)
make data

# 4. Open a notebook
jupyter lab notebooks/bpo_offshoring_fx_lag/Colombia/02_estimation.ipynb
```

That's it. Cell 1 of each estimation notebook reads from `data/panels/` and
the rest of the notebook runs end-to-end without internet.

## Reproducibility tiers

| Tier | Make target | Time | Bytes | What it gives you |
|---|---|---|---|---|
| 1 | `make data` | 30 sec | ~1 MB | Processed parquet panels (HuggingFace) |
| 2 | `make data-raw` | 30 min | 5.3 GB | DANE GEIH zips + Banrep TRM raw |
| 2 | `make data-onchain` | 10 min | ~50 MB | Celo on-chain panels (RPC) |
| 3 | `make panels` | ~1 hr | n/a | Re-derive Tier 1 locally from Tier 2 raw |
| 3 | `make verify` | n/a | n/a | Hash-check Tier 3 against published Tier 1 |

A clean `make verify` is the strongest reproducibility evidence the repo
produces. See `data/README.md` and `data/manifest.yaml` for canonical sources.

## What's inside

- **`notebooks/`** — 7 trio-structured analyses (Pair D, Pair D Stage-2 paths
  A & B, dev-AI cost, FX-vol-on-CPI-surprise, FX-vol-on-remittance-surprise,
  abrigo Y₃×X_d Carbon basket) + 2 standalone notebooks. Each trio: `01_data_eda`,
  `02_estimation`, `03_tests_and_sensitivity`.
- **`docs/specs/`** — Pre-committed pre-data specifications. 14 files. Anti-fishing
  invariants enforced.
- **`docs/plans/`** — Implementation plans matched to specs. 10 files.
- **`docs/sub-plans/`** — Two NB-α and ccop-provenance audit sub-plans.
- **`scratch/`** — Research outputs, reviewer dispositions, fix logs, M-search
  reports. ~245 markdown files. The narrative trail behind every gate verdict.
- **`memory/`** — 65 project / feedback memories. Read these before extending
  any iteration; they encode the anti-fishing rules and the verdict history.
- **`scripts/`** — Tier 1/2/3 data fetchers and the panel builder.

## Iteration headlines

- **Pair D** — Colombian young-worker services-sector share × COP/USD lagged
  6-12 mo. **PASS**: β = +0.137, p ≈ 1.5×10⁻⁸. Stage-2 M-sketch unblocked.
- **dev-AI Stage-1** — Colombian young-worker Section J (Información y
  Comunicaciones) share × COP/USD. Phase 1 in progress.
- **FX-vol-on-CPI-surprise** — **CLOSED FAIL** (β̂ = −0.000685, 90% CI ⊃ 0).
  Notebook trio retained as reference + as a worked example of disciplined
  pre-commitment under failure.
- **Phase-A.0 remittance** — **CLOSED EXIT_NON_REMITTANCE** (0/30 peak-day
  remittance fingerprints).
- **P1 Bittensor SN18** — **PARKED** for record.

Detailed state: `memory/MEMORY.md` indexes every iteration.

## Working with this repo as an agent

Read `CLAUDE.md` first. The Abrigo Operating Framework section is
load-bearing. Then read these memory files in order:

1. `memory/MEMORY.md` — index
2. `memory/project_*` — current iteration states
3. `memory/feedback_*` — non-negotiable rules (TDD, anti-fishing, trio
   checkpoints, decision-citation blocks)

Every notebook is governed by:

- Decision-citation block precedes every test / decision / spec choice
- Trio checkpoint after every (why-markdown → code-cell → interpretation) unit
- HALT + disposition memo whenever spec contradicts data — never silent
  threshold tuning

## License

MIT (analytics + tooling). Underlying public data — DANE, Banrep, Celo on-chain
events — retains its own licensing terms (see `data/manifest.yaml`).
