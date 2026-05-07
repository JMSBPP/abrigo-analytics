# CLAUDE.md — Abrigo Analytics

This file provides guidance to Claude Code when working in this repository.

## Repository scope

This repo is the **analytics half** of the Abrigo project. It contains:

- Empirical-validation work (does the underlying microeconomic risk admit a
  positive measurable beta?) for the (Y, M, X) instrument family.
- Notebooks, plans, specs, and research artifacts driving each (Y, X) iteration.
- Data fetchers and processed panels, distributed via three reproducibility tiers.

The **contract half** (Solidity, Foundry, Rust nodes) lives separately in the
`thetaSwap-core-dev` repo; pointers to it are preserved in `memory/` and the
specs that depend on Panoptic / Uniswap V4 settlement.

## Abrigo Operating Framework — (Y, M, X) Triples for Permissionless Convex Hedges

**Highest-level goal**: minimize income inequality, framed in post-Keynesian
terms — distribution is institutionally determined, not equilibrium-given. The
product family contributes to this goal by altering the institutional structure
that currently blocks wage earners from accumulating productive capital.

**Instrument family**: permissionless on-chain perpetual convex instruments,
settled on **Panoptic** (perpetual options written on Uniswap v3/v4 LP
positions). The denomination of any given hedge — Mento-native (COPm, BRLm,
KESm, EURm, USDm), USDC, ETH, sectoral basket tokens, or any Panoptic-eligible
pair — is a *parameter of each iteration*, selected to fit the target population.

**Ideal-scenario modeling permitted (Panoptic-liquidity caveat).** Panoptic
deployment liquidity is structurally thin today. The framework permits — and at
this stage *requires* — modeling the **ideal scenario** in which the proposed
instrument settles cleanly with adequate liquidity. The empirical β-estimate
work (does the underlying microeconomic risk admit a positive measurable beta?)
is independent of actual on-chain deployment; the M-design step proposes the
ideal settlement architecture; only the deployment step requires real LP
capital. **Stage-correctly with explicit exit criteria:**

1. Empirical risk validation FIRST (exit: positive-β confirmation on the chosen X
   at conventional significance).
2. Ideal-scenario M sketch SECOND (exit: a Panoptic-position construction that
   *would* settle the empirical β if deployed; no liquidity sourcing required).
3. Deployment LAST (exit: live LP capital + execution test).

Stage drift (M-design ballooning back into apparatus) is anti-fishing-banned.

**Transmission channel — wage → productive capital via premium-funded ratchet
(self-LBM)**: the perpetual hedge functions as a self liquidity-bootstrapping
mechanism for the *holder*. A wage earner pays a small recurring premium out of
wage income; the instrument's accumulated convex payoff and roll yield convert
over time into productive-capital exposure. The hedge's existence is what
*creates* the capital position — absent the instrument, the wage earner never
crosses the wage/capital boundary because the macro risks (X) along the path
are unbearable from a pure-savings start. This is the premium-funded ratchet
design, not up-front capital protection.

**Operating unit of work — (Y, M, X) triples**:

- **Y** = outcome variable on which a target population's exposure to the
  wage→capital transition is measured. Examples: realized volatility of a
  household consumption basket; cross-sectional differential between
  productive-capital returns and wage-indexed CPI; structural-transformation
  indicators (e.g., young-worker services-sector share).
- **M** = the Panoptic pool configuration that hosts the hedge — the underlying
  token pair, the strike/range geometry of the deployed position, and the payoff
  shape (long-gamma covered call, range LP, perpetual put, straddle, etc.). M
  choice is constrained by Panoptic's pool mechanics: the (Y, X) pair must
  admit a continuous on-chain reference price representable as a Panoptic
  position. Off-Panoptic venues are out of scope.
- **X** = the *major risk* that currently blocks the target population's
  wage→capital transition. First-cut iteration question is always: "what kills
  wage earners' attempts to enter productive-capital ownership for *this*
  population?" X identification is empirical and must precede M selection.

**Iteration order (default — target-population dominant)**: fix the population →
fix Y on a candidate inequality/transition-exposure measure → enumerate X
candidates from the empirical risk surface → for each surviving X, search
Panoptic-eligible M for tradability. The (Y, X) pair only graduates to
instrument design once a Panoptic position with viable convex pricing exists.
Closed iterations (gate verdict FAIL) inform the X-search prior for the next
population, not silent re-runs of the same (Y, X) at different thresholds —
anti-fishing invariants carry forward.

## Active iterations (snapshot)

State of each iteration is canonical in `memory/` (project memories). Quick
summary as of repo bootstrap:

- **Pair D** (BPO offshoring × COP/USD lag) — **PASS** verdict; β = +0.137,
  p ≈ 1.5e-08; Stage-2 M-sketch unblocked. See `memory/project_pair_d_phase2_pass.md`
  + notebooks/`bpo_offshoring_fx_lag/`, `pair_d_stage_2_path_a/`,
  `pair_d_stage_2_path_b/`.
- **dev-AI Stage-1** (Colombian young-worker Section J × COP/USD lag) — Phase
  1 dispatched 2026-05-05; data ingest in progress. See specs
  `2026-05-04-dev-ai-stage-1-simple-beta-design.md` + notebooks/`dev_ai_cost/`.
- **FX-vol-on-CPI-surprise** — **CLOSED FAIL** 2026-04-19 (β̂ = −0.000685, 90%
  CI contains 0). Notebooks remain as reference. See
  `memory/project_fx_vol_cpi_notebook_complete.md`.
- **Phase-A.0 remittance** — **CLOSED EXIT_NON_REMITTANCE** 2026-04-24. See
  `memory/project_phase_a0_exit_verdict.md`.
- **P1 Bittensor SN18** — **PARKED** for record. See
  `memory/project_p1_sn18_spec_parked_for_record.md`.

## Repo structure

```
abrigo-analytics/
├── README.md              # Public-facing quickstart for cloners
├── CLAUDE.md              # This file
├── pyproject.toml         # uv-managed; mirrors requirements.txt; declares simulations/ package
├── requirements.txt       # exact pin from source repo's venv
├── Makefile               # data tiers + notebook execution + lint/test
├── notebooks/             # 7 notebook trios + 2 standalone analyses
├── simulations/           # functional-python three-tier package (added by SIM-INFRA-0)
│   ├── types/             # Value tier — frozen-dataclass parameter containers + Protocols
│   ├── modules/           # Callable tier — frozen-dc + __call__ stateless transforms
│   ├── utils/             # IO Boundary tier — class-with-__init__; mutable state lives ONLY here
│   ├── saas_builder/      # COHORT-1: T1 PyMC posterior + emission (priors/model/diagnostics/emit)
│   └── tests/             # pytest + Hypothesis strategies + math-pin verification
├── docs/specs/            # 14 specs (econ/analytics relevant)
├── docs/plans/            # 11 implementation plans (SIM-INFRA-0 added)
├── docs/sub-plans/        # 2 sub-plans (NB-α, ccop-provenance-audit)
├── scratch/               # ~245 research outputs (dispositions, reviews, designs)
├── memory/                # 65+ memory files — project state + feedback rules
├── data/                  # gitignored; populated via three Make targets
└── scripts/               # data fetchers (Tier 1/2) + panel builder (Tier 3)
```

**`simulations/` discipline.** Three-tier (Value / Callable / IO Boundary) per
`functional-python` skill: no inheritance except `Protocol` + `Exception` +
private Pydantic `BaseModel` (utils/json_io transient validators) + TypedDict
(utils/parquet_io row schemas). Tier-import discipline: types/ ↛ modules/utils;
modules/ ↛ utils. Code-touching work follows the Honnibal audit-pass chain
(tighten-types → contract-docstrings → hypothesis-tests → try-except →
pre-mortem → mutation-testing) as established by SIM-INFRA-0 Phase 3.

## Key commands

```bash
# First-time setup
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt

# Three data tiers (pick one — see data/README.md)
make data         # Tier 1: HuggingFace processed panels (~30 sec)
make data-raw     # Tier 2: DANE + Banrep raw (~30 min, ~5.3 GB)
make data-onchain # Tier 2: Celo RPC on-chain panels (~10 min)
make panels       # Tier 3: re-derive Tier 1 from Tier 2 raw

# Run all notebooks headless
make notebooks

# Verify reproducibility (Tier 3 vs published Tier 1)
make verify
```

## Code style

- **Python**: frozen dataclasses, free pure functions, full typing (per the
  `functional-python` skill). Composition over inheritance.
- **Notebooks**: trio discipline — every (why-markdown, code-cell,
  interpretation-markdown) trio is a HALT-checkpoint for human review per
  `feedback_notebook_trio_checkpoint.md`. Decision-citation block (4-part:
  reference / why / relevance / connection) precedes every test or spec choice
  per `feedback_notebook_citation_block.md`.

## Anti-fishing invariants (carried forward from contracts/ source)

These are NON-NEGOTIABLE across iterations:

- `N_MIN = 75`, `POWER_MIN = 0.80`, `MDES_SD = 0.40` SD-units of Y.
- Pre-pin sign expectation, lag structure, and primary specification BEFORE
  data is touched. Threshold tuning post-hoc is silent-fishing.
- HALT + disposition memo + user-enumerated pivot + CORRECTIONS block + post-hoc
  3-way review whenever spec contradicts data. See
  `feedback_pathological_halt_anti_fishing_checkpoint.md`.

## Cross-repo dependencies

This repo intentionally has **no Solidity / Foundry / Rust** code. Specs and
plans that reference Panoptic / Uniswap V4 / Mento contracts treat those as
external givens. The contract half remains in `thetaSwap-core-dev`; cloners do
not need it for analytics work.
