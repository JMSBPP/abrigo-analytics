---
name: Y₃ inequality-differential structure (4-country, pre-registered weights)
description: Y₃_t = (1/4) × Σ Δ_country where Δ = R_equity + Δlog(WC_CPI); CO/BR/KE/EU; WC-CPI weights 60/25/15 (food/energy+housing-utilities/transport-fuel)
type: project
originSessionId: phase0-vb-mvp / Y₃ design doc 2026-04-24
---

**Fact**: The Y₃ inequality-differential target variable is constructed as `Y₃_t = (1/4) × (Δ_CO + Δ_BR + Δ_KE + Δ_EU)`, where each per-country differential is `Δ_country = R_equity + Δlog(WC_CPI)`. Country-aggregation is equal-weighted (1/4 each, pre-registered to avoid data-driven weight selection). The four countries map to four Mento working-class stablecoins: Colombia→COPM, Brazil→BRLm, Kenya→KESm, Eurozone→EURm. WC-CPI is computed per country with pre-registered budget-share weights: 60% food, 25% energy + housing utilities, 15% transport-fuel — derived from World Bank LAC bottom-quintile budget shares per `contracts/.scratch/2026-04-24-y3-consumption-proxy-research.md` §4.

**Why**: the inequality-hedge thesis (`project_abrigo_inequality_hedge_thesis.md`) requires measuring the DIFFERENTIAL between rich-asset returns (equity) and working-class consumption returns (CPI on WC basket). Equity per country: COLCAP (CO), BOVESPA (BR), Nairobi NSE-20 (KE), STOXX 600 (EU); 10Y bond as diagnostic Y. Equal-weight country aggregation is anti-fishing-clean per LAC-comparative-literature precedent (Banrep Borradores, IDB working papers). Pre-registered budget weights avoid the alternative of fitting weights to maximise Y₃ variance — a textbook fishing risk.

**How to apply**:
1. Design doc (immutable post-`23560d31b`): `contracts/docs/superpowers/specs/2026-04-24-y3-inequality-differential-design.md`.
2. Y₃ panel construction is Task 11.N.2d (in flight at session close); panel spans Sep-2024 → 2026-04-24 (~84 weeks); persisted to `onchain_y3_weekly` table.
3. Sensitivity panel (Task 11.N.2d.1, queued): Aug-2023 → 2026-04-24 under `source_methodology = 'y3_v1_sensitivity'`.
4. Eurozone HICP transport-fuel substitution: `(transport CPI − food/energy double-count adjustment)` per Eurostat HICP documentation; documented as a per-country exception in design doc §6.
5. Friday-anchored America/Bogotá weekly cadence, LOCF interpolation for monthly→weekly CPI.
6. Per-country WC-CPI source modules: Banrep open-data (CO), IBGE (BR), KNBS (KE), Eurostat (EU).

## Related memory

- `project_abrigo_inequality_hedge_thesis.md` — product thesis
- `project_carbon_defi_attribution_celo.md` — primary X_d that pairs with Y₃
- `project_duckdb_xd_weekly_state_post_rev531.md` — onchain_xd_weekly state for X-Y join
- `project_phase15_5_task_chain_post_rev531.md` — task chain that produces Y₃ panel
