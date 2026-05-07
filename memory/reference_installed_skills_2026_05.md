---
name: Installed skills inventory 2026-05-07
description: Locations and grouping of 24 newly-installed Claude skills (FP/types, sim, econ, audit) — for invocation routing and gap-skill authoring
type: reference
---

24 skills installed 2026-05-07 to `~/.claude/skills/`. Use these triggers to route work:

**FP / Type-driven (Honnibal + TOB)**
- `tighten-types`, `contract-docstrings`, `hypothesis-tests`, `mutation-testing`, `pre-mortem`, `try-except`, `stub-package` — Python type strictness, property-based tests, mutation tests
- `fp-check`, `modern-python` (Trail of Bits) — false-positive verification; uv/ruff/ty toolchain
- `property-based-testing` (TOB, multi-language; complements honnibal's Python-only `hypothesis-tests`)

**Spec / Audit (Trail of Bits)**
- `spec-to-code-compliance` — verify implementation matches spec (formalizes anti-fishing pre-pin doctrine)
- `dimensional-analysis` — unit/scale annotation; useful for econ pipelines and CFMM math

**Numerical / Bayesian / Sim (K-Dense)**
- `pymc` — Bayesian, MCMC NUTS, hierarchical models, LOO/WAIC (fills GMM/MLE-adjacent gap)
- `statsmodels` — classical inference (OLS/GLM/ARIMA) with diagnostics
- `polars` — in-RAM 1–100 GB DataFrames; `dask` — larger-than-RAM/parallel
- `sympy` — symbolic math, calculus, matrix algebra; useful with `cfmm-from-payoff` and `latex-econ-model`

**Econometrics (Melea)**
- `python-panel-data` (linearmodels), `r-econometrics` (fixest IV/DiD/RDD), `stata-regression`
- `api-data-fetcher` — FRED, World Bank (NOT for DANE/Banrep/Celo-RPC)
- `latex-econ-model`, `general-equilibrium-model-builder`, `econ-visualization`

**Collisions to know**
- `mutation-testing`: Honnibal version installed; TOB version (Solidity-flavored) skipped — swap if needed for contract work.
- `econ-visualization` overlaps `graph` (existing); both kept — econ-viz is paper-specific.
- `latex-econ-model` complements (does NOT replace) `latex-doc` and `notation-clean`.
- `property-based-testing` (multi-lang) + `hypothesis-tests` (Python-specific) — use both as appropriate.

**Why:** External research 2026-05-07 confirmed these were the strongest open-source matches to the Abrigo paradigm (functional Python + type-driven + econometrics + numerical sim). Dead-end gaps still unfilled: Lean/Coq/F\*, dedicated GMM/MLE structural estimation, Nix/DVC/Snakemake reproducibility, and **anti-fishing replication-package discipline** (where Abrigo's existing memory rules already exceed any public skill — strongest candidate for self-authoring via `superpowers:writing-skills`).

**How to apply:** When starting econ analysis on an iteration, prefer `python-panel-data` for linearmodels code, `pymc` for Bayesian/structural, `statsmodels` for classical inference, `sympy` for theoretical derivation. When writing Python implementation, chain `functional-python` → `tighten-types` → `hypothesis-tests` → `mutation-testing`. For audit / spec-compliance work, dispatch `spec-to-code-compliance` alongside `audit-econ`.
