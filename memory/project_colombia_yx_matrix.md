---
name: Colombia Abrigo Y×X matrix — next-primary candidates post-CPI-FAIL
description: Complete Y×X matrix from 3 research agents ranking Colombia macro-risk (X, Y) cells for Phase-A engine candidates, post CPI-FAIL
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
**Fact**: On 2026-04-20, three research agents produced a complete Y×X landscape for Colombia-specific macro-risk identification candidates. The landscape supersedes any ad-hoc candidate picks from prior conversation; any new Phase-A engine candidate must be justified against this matrix.

**Why**: Post-CPI-T3b-FAIL (β̂_CPI=−0.000685, 2026-04-19), the user reframed the exercise as a matrix exploration rather than a single-candidate re-pick. Three agents (corpus + ≤8 external queries each) systematically ranked cells to avoid the error of naming controls (VIX, DXY, EMBI, Fed Funds, Oil, Banrep Repo) as candidates and to avoid the error of limiting Y to TRM-vol only. Re-deriving this matrix costs ~3 agent runs (~15 min + credits); recalling it costs nothing.

**How to apply**: Before proposing any new structural-econometric candidate for Colombia, check this matrix. Pick from the triangulated cells and the top-1 rows per agent. Do NOT propose cells the matrix already scored as low ship-value without a new information-bearing argument.

---

## Top cells per agent

### Fixed-Y (what X best predicts this Y?)

- **Y₁ TRM weekly RV** → **#1 Remittance-flow surprise** (BanRep monthly US-corridor AR(1) residual); #2 BanRep ITI-PPI ToT surprise; #3 TES 10Y-auction yield surprise; #4 Venezuelan-migration shock; #5 coffee-differential — *Agent 3*
- **Y₂ Colombian CPI monthly variability** → **#1 DANE IPP imported-goods residual** (dominates TRM because it pre-aggregates basket-weighting; Borrador 930 ERPT only 0.01-0.05 and declining); #2 TRM/ΔTRM pass-through; #3 Banrep policy-rate surprise (Kuttner-Svensson); #4 cCOP/USDT log-volume; #5 Venezuelan-migration — *Agent 4*
- **Y₃ Remittance-flow variance** → **#1 US Hispanic-employment surprise** (BLS CES; Dallas Fed 2023 + IDB TN-3243 2025; US corridor 53%); #2 US migration-policy event dummies (Trump-Petro Jan 2025); #3 World Bank RPW US-Colombia corridor cost; #4 COPM mint/burn net-flow; #5 Venezuelan-Colombian bidirectional migration — *Agent 4*

### Fixed-X (what Y does this on-chain observable predict?)

- **X_a cCOP/USDT log-volume** (540d, Dune #6941901, 4,913 real senders) → **top-Y = Y₃ Remittance variance (SHIP)**; 2nd Y₁ TRM RV (test); 3rd Y₈ FX-spread var (test); 4th Y₂ CPI var (test); 5th Y₇ TES var (skip) — *Agent 5*
- **X_b cCOP/USDT net directional flow** (USDT→cCOP minus reverse) → **top-Y = Y₈ FX P2P-spread / flight-to-USD variance (SHIP)**; 2nd Y₁ TRM RV (test); 3rd Y₃ Rem var (test); 4th Y₂ CPI var (skip); 5th Y₄ consumption (skip) — *Agent 5*
- **X_c COPM mint/burn net-flow** (720d, $200M/mo, 100K Littio users) → **top-Y = Y₃ Remittance variance (SHIP — FLAGSHIP)**; 2nd Y₅ household income var (test); 3rd Y₁ TRM RV (test); 4th Y₄ consumption var (test); 5th Y₂ CPI var (skip) — *Agent 5*

## Triangulated cells (cross-agent agreement)

- **(X_c COPM mint/burn, Y₃)** — Agent 4 rank 4 + Agent 5 rank 1 = strongest cross-agent on-chain cell. Phase-A flagship.
- **(X_a cCOP volume, Y₂)** — both agents rank 4 = "test, not ship" agreement.

## Universal observables (cross-Y coverage)

- **Venezuelan-migration shock** — ranks in all three Y shortlists; regime-specific caveat (2015-2022 peak; fading post-2024).
- **Trump-Petro Jan 2025 event** — cross-cuts all three Y's on event-study axis; documented +100% Littio USDC growth in 48h. Argues for shared event-dummy column in multi-Y engine.
- **US Hispanic-employment surprise** — top-1 for Y₃; defensible but untested for Y₁ via remittance→FX-inflow chain. Candidate universal-observable.

## Novelty claim (external search, Agent 5)

No existing DeFi variance swap prices variance of on-chain stablecoin flow volume — only price variance (Chainlink / Feldmex pattern surveys). All three shipping candidates (B1/B2/B3 below) are genuinely novel. Confirms `LITERATURE_PRECEDENTS.md` §9.

## Master matrix (X rows × Y columns; cells = rank 1-5 + ship-flag S/T/K)

| X \ Y | Y₁ TRM RV | Y₂ CPI var | Y₃ Rem var | Y₄ HH cons | Y₅ HH inc | Y₆ ToT var | Y₇ TES var | Y₈ FX-spread |
|---|---|---|---|---|---|---|---|---|
| X_a cCOP vol | 2 T | 4 T | **1 S** | — K | — K | — K | 5 K | 3 T |
| X_b net direction | 2 T | 4 K | 3 T | 5 K | — K | — K | — K | **1 S** |
| X_c COPM mint/burn | 3 T | 5 K | **1 S** | 4 T | 2 T | — K | — K | — K |

## Phase-A first-batch options (as of 2026-04-20)

| Row | Cell | Substrate | History | Role |
|---|---|---|---|---|
| A1 | Remittance-flow surprise → Y₁ TRM RV | off-chain weekly 2008-2026 | 18 yr | off-chain calibration |
| A2 | DANE IPP imported → Y₂ CPI var | off-chain monthly 2000-2026 | 26 yr | off-chain calibration (multicollinearity-flagged) |
| A3 | US Hispanic-emp surprise → Y₃ Rem var | off-chain monthly 2000-2026 | 26 yr | off-chain companion to B1 (cross-substrate check) |
| B1 | COPM mint/burn → Y₃ Rem var | on-chain weekly 2024-2026 | 24 mo | **triangulated flagship** |
| B2 | cCOP volume → Y₃ Rem var | on-chain weekly 2024-2026 | 18 mo | decentralized companion to B1 |
| B3 | cCOP net direction → Y₈ FX-spread var | on-chain weekly 2024-2026 | 18 mo | novel capital-flight cap |

**Option sets presented to user** (awaiting selection as of this memory write):
- **α**: Full 6-row batch (A1+A2+A3+B1+B2+B3)
- **β**: Lean 4-row batch (A1+A3+B1+B3) — recommended by foreground; drops IPP multicollinearity + B2 Y₃-overlap
- **γ**: Flagship-only (B1) — minimum scope

## Key open risks (from all agents)

1. **Overlap horizon** 18-24 months caps on-chain products to monthly tenor; quarterly tenor defers to 2027+.
2. **Regime breaks**: Isthmus hardfork (2025-07-09), Mento migration (2026-01-25 cCOP→COPm), Jan 2025 Trump-Petro — Quandt-Andrews + dummy columns mandatory.
3. **Revision vintages**: BanRep remittance data revised up to 3mo post-initial; real-time vintages required.
4. **Multicollinearity**: X_a and X_c co-move in Jan-2025 stress (VIF >10 expected); ridge / orthogonalized residuals if co-registered.
5. **Single-channel Littio risk** on X_c; X_a is the decentralized hedge.
6. **CPI-FAIL discipline**: every new row requires pre-registered gate, α, controls, SE method, reconciliation rule BEFORE estimation. No post-hoc "rescue" framing.

## Source reports (persisted 2026-04-20)

- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-20-ccop-mcop-observables-search.md` — Agent 1: on-chain observables inventory
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-20-remittance-volatility-swap-deep-read.md` — Agent 2: REMITTANCE_VOLATILITY_SWAP corpus deep-read
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-20-colombia-next-primary-candidate-ranked.md` — Agent 3: Y₁-fixed (TRM RV) X-ranking
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-20-colombia-Y2-CPI-Y3-remittance-X-ranking.md` — Agent 4: Y₂/Y₃-fixed X-ranking
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/scratch/2026-04-20-colombia-fixed-X-vary-Y-ranking.md` — Agent 5: fixed-X product-first Y-ranking

## Engine design implications (not yet selected)

- User picked **Approach C** (typed Python `@dataclass(frozen=True)` candidate registry, functional-python compliant) as engine architecture for Phase A.
- Engine must branch pipeline on a `DataSubstrate` enum (`OFF_CHAIN_WEEKLY` vs `ON_CHAIN_DAILY_AGG_WEEKLY`) to handle A-rows vs B-rows.
- Phase B = pool-design-space simulator; scope: *outlined* in this spec, detailed design in future spec.
- Phase C = actual pool construction, out of scope.
