---
name: Phase 5 ready state
description: Structural-econ spec Rev 4 accepted; Phase 5 data pipeline ready to start; all data sources verified free-tier; 12 reviewer passes converged
type: project
originSessionId: e63ee238-733d-49df-8015-addce58e2ae7
---
Structural econometric spec at `contracts/notes/structural-econometrics/specs/2026-04-15-fx-vol-cpi-surprise.md` (Rev 4) accepted after 4 rounds × 3 reviewers (12 independent passes). MQA gave first clean pass (CONDITIONAL PASS, 0 BLOCKs).

**Pre-committed primary specification:**
```
RV_t^{1/3} = α + β·s_CPI + γ₁·s_US_CPI + γ₂·s_BanRep + γ₃·VIX + γ₄·I_intervention + γ₅·r_oil + ε
```
- LHS: cube-root of weekly realized vol (sum of 5 daily squared COP/USD log-returns)
- RHS: Colombian CPI surprise (DANE release − BanRep EME consensus) + 6 controls
- Estimation: OLS + Newey-West HAC (lag=4)
- Confirmatory: GARCH(1,1)-X with |s_CPI| in variance equation
- Gate: T3a (β≠0 two-sided) + T3b (β̂ − 1.28·SE > 0, product gate)

**Data sources (all free-tier, verified 2026-04-15):**
- FRED DEXCOUS: daily COP/USD (20+ years)
- BanRep EME: monthly CPI consensus (historical tables at banrep.gov.co)
- DANE IPC + IPP: monthly releases (dane.gov.co)
- IBR: overnight rate via SUAMECA + Datos Abiertos Colombia (datos.gov.co)
- SUAMECA: FX intervention (series ID to confirm in catalog)
- FRED VIXCLS: daily VIX
- FRED DCOILWTICO: daily WTI oil

**Phase 5 structure (per structural-econometrics skill):**
- Step A: Data Engineer agent builds dataset (MANDATORY: use free-tier sources, NOT Dune MCP — this is off-chain macro data)
- Step B: Analytics Reporter agent runs estimation per spec

**Key papers in refs/:**
1. be_1171.pdf — Rincón-Torres 2021, FX↔TES interdependence (transmission architecture)
2. rinconHortuaSilvaRoman.pdf — Rincón-Torres 2023, macro-news→TES (ABG 2017 filter methodology)
3. traspasoAinflacion.pdf — Rincón-Castro 2021, FX→π pass-through (0.01–0.05)
4. intradayToCIP.pdf — BIS WP 462 / Fuentes et al. 2014 (intraday event study, CPI in surprise basket)

**4 minor items deferred from Rev 4 (fix during Phase 5):**
1. Delete "exploratory" from cube-root label (contradicts "primary")
2. Add minimum sample rule (2008–2025; if EME < 2008, AR(1) becomes primary)
3. Define "disagree" in reconciliation: different sign OR one sig at 10% while other not
4. Justify 90% one-sided CI (CLM convention; report 95% as sensitivity)

**How to apply:** Start Phase 5 in a fresh session. Read this memory + the spec file. Data Engineer builds the dataset from the 7 free sources. Analytics Reporter estimates the primary + confirmatory + sensitivity battery.
