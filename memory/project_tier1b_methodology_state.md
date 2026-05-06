---
name: Tier 1b methodology state
description: Current state of the FX-vol-on-CPI-surprise econometric exercise — papers read, transmission chain corrected, ready for structural-econometrics identification
type: project
originSessionId: e63ee238-733d-49df-8015-addce58e2ae7
---
Tier 1 literature feasibility completed with verdict PIVOT_TO_TIER_1B on channel π. be_1171 (Rincón-Torres, Rojas-Silva, Julio-Román 2021) discovered post-search and added — proves FX is the efficient Colombian macro aggregator (a₂₁=-0.067 FX→TES, a₁₂=-0.001 TES→FX), collapsing the transmission chain from 4 steps to 1: macro shock → FX directly.

**Why:** Not pass-through. The relevant coefficient is CPI-surprise → FX realized vol, NOT FX→π pass-through (which is 0.01–0.05 per Rincón-Castro 2021 Traspaso). The RAN observes FX vol directly via g^pool ≈ φ²V(P)/(8L).

**How to apply:** Next step is /structural-econometrics Phase -1 Identification using 4 key papers in refs/:
1. be_1171.pdf (FX↔TES interdependence, transmission architecture)
2. rinconHortuaSilvaRoman.pdf (Rincón-Torres 2023 macro-news-on-TES, ABG 2017 two-step surprise filter — methodology to replicate)
3. traspasoAinflacion.pdf (Rincón-Castro 2021 Traspaso, symmetry prior on magnitude)
4. intradayToCIP.pdf = BIS WP 462 (Fuentes et al. 2014, intraday event study with CPI in surprise basket)

Human-review file at: contracts/notes/structural-econometrics/identification/2026-04-14-inflation-mirror-two-channel-literature-human-review.md

Regression target: RV_t (weekly realized vol COP/USD) = α + β·s_CPI + γ₁·s_US_CPI + γ₂·s_BanRep_rate + γ₃·VIX + ε. Gate: adj-R² ≥ 0.15.

Deliverable at: contracts/notes/structural-econometrics/identification/2026-04-14-inflation-mirror-two-channel-literature.md (committed, T20 pending human sign-off)
