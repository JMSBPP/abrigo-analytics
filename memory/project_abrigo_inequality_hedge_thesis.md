---
name: Abrigo inequality-differential hedge thesis
description: Abrigo product thesis refined 2026-04-24 — hedge an inequality DIFFERENTIAL (rich-household asset returns − working-class consumption returns), not a single macro aggregate; on-chain continuous-time instrument that appreciates as the differential widens, protecting working-class wealth from relative erosion
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
**Fact**: Abrigo's product is not a single-Y macro hedge. It is an instrument that settles on the **DIFFERENTIAL between (rich-household asset returns) and (working-class consumption-based returns)**. The instrument appreciates when the differential widens (inequality worsens), which is precisely when working-class purchasing power is eroded relative to capital-holding households. Working-class users BUY the instrument as a hedge against their own relative decline.

**REFRAMING (2026-04-24, Task 11.N.2 research at `scratch/2026-04-24-copm-bot-attribution-research.md`)**: the "two dominant bots" in the COPM dataset (`0x6619871…` and `0x8c05ea30…`) are not noise — they are **Bancor Carbon DeFi protocol contracts on Celo** (CarbonController + BancorArbitrage / Arb Fast Lane; HIGH-confidence attribution via Carbon DeFi docs + Dune decoded namespace). What they actually DO is **rebalance the Mento working-class-stablecoin basket {COPM, cUSD, cEUR, cREAL, cKES, XOFm} against the global-asset basket {CELO, USDT, USDC, WETH}** — almost exactly the two-leg structure of the inequality-differential hedge. Carbon basket-rebalancing volume becomes a DIRECT on-chain proxy for capital-flow-across-class-boundaries. The macro driver is CELO/global-crypto volatility + Mento-broker reset cadence (TRM Δ correlates only 11/30 peak-day events; Colombian quincena/prima/BanRep IBR show NO detectable footprint — further confirmation of the EXIT_NON_REMITTANCE verdict). This shifts the Y target from USD-COP carry to CELO/crypto-volatility + Mento-peg-stability spread; the original `(Banrep − Fed)/52 + ΔTRM/TRM` carry-return formula is no longer the right anchor for the Carbon-basket X_d. Data scope expands from COPM Transfer events to Carbon `TokensTraded` events across the full Mento basket.

**Why**: macro-income hedges that settle on a single aggregate (CPI, TRM, remittance) either (i) fail to capture the relative-income story that matters for welfare (CPI alone doesn't separate who's hurt — rich households often have CPI-indexed assets), or (ii) don't produce a naturally-investable instrument because there's no counter-party (who is LONG depreciation without this hedge?). The inequality differential solves both: it's a real economic variable with measurable wealth-redistribution consequences, AND it has a natural two-sided market (working-class LONG the hedge; capital-holders SHORT it as a carry-diversifier or they naturally capture the asset-return leg via their existing positions).

**The two legs (formal construction)**:

*Asset-return leg (rich-household proxy):*
- USD-COP interest-rate differential (carry-trade return) — observable OFF-chain (Banrep policy rate, Fed funds) AND ON-chain (cUSD yield on Celo DeFi − cCOP implied yield)
- TES 10Y yield (government-bond return — concentrated in institutional/wealthy portfolios)
- Colcap equity-index return (equity-concentrated wealth)
- Real-estate returns (if fetchable)
- **On-chain native candidate**: cUSD accumulation velocity by Colombian-overlap addresses (stablecoin dollarization — the digital analog of rich-household USD-refuge behavior)

*Consumption-return leg (working-class proxy):*
- DANE EMMV / EMCM retail-sales monthly index (consumption pattern of broad population)
- DANE ECV household-consumption survey
- BanRep household-debt-service-ratio (inverse: rising debt service = declining discretionary consumption)
- Wage-growth proxies (DANE formal-employment survey)
- **On-chain native candidate**: COPM B2B→B2C diffusion metric (commercial-trade-credit delivery to retail) + small-tx cCOP activity IF filterable from bot/arb contamination

*The differential*: `Y_inequality(t) = Asset_return_leg(t) − Consumption_return_leg(t)` — constructed as a continuous-time stochastic process; the instrument's payoff scales with the realized path of this differential over a tenor (monthly / quarterly settlement windows).

**How to apply**:

1. **Structural-econometric exercises serve the differential**: any candidate X (including X_d COPM B2B→B2C filtered signal) should be mapped against BOTH legs separately, then against the differential itself. The gate test is whether the X predicts the DIFFERENTIAL — not a single Y.

2. **Multi-Y panel is the default**: one X → {Y₁ TRM, Y₂ CPI, Y_asset_onchain, Y_consumption, Y_inequality_spread}. Gate separately on each, then aggregate in a single reconciliation table. CPI and TRM data already exist (from CPI-FAIL panel); consumption data acquisition is a separate track.

3. **Data acquisition priorities**:
   - *Tier 1 (execute immediately — data on hand)*: Y₁ TRM weekly RV, Y₂ CPI weekly surprise — both in the Rev-4 947-obs panel.
   - *Tier 2 (fetch in parallel)*: DANE EMMV retail-sales monthly + ECV household-consumption; BanRep TES yield curve; BanRep household-debt-service-ratio. All off-chain but publicly published APIs or CSV-downloadable.
   - *Tier 3 (compute from existing + new on-chain)*: on-chain USD-COP carry (cUSD-Celo-yield − cCOP-yield) via Celo RPC / Dune spells; Colombian-overlap cUSD holdings via address-heuristics.

4. **Product instrument (future — NOT current exercise scope)**: continuous-time swap / ERC-4626-like vault that settles PnL on the realized differential; pricing primitive needs the structural-econometric foundation first. The exercise is to CALIBRATE the differential's dynamics, not to build the instrument yet.

5. **Anti-fishing corollary**: the multi-Y mapping INCREASES multiple-testing exposure. Pre-commit which Y is the gate target (the differential itself), which are auxiliary diagnostics (single-leg Y's), and apply FWER-aware aggregation rules (RC's plan-review finding on Rev-4: unadjusted-FWER ≈ 99.98% over 171-filter F was a genuine concern — same discipline applies here across Y's, not just filters).

**Progressive design principle**: the instrument is CONSTRUCTED to compensate working-class relative decline. This is not a neutral derivative — it has an explicit welfare-redistribution purpose. Marketing / product framing must honor this (not positioned as a speculative trade; positioned as a structural hedge for labor-income holders).

## Related memory

- `project_ran_product_framing.md` — Abrigo permissionless-mainstream-user thesis; inequality-hedge refines the positioning
- `project_ran_positioning_principles.md` — painkiller-not-vitamin; inequality-widening pain is real and underaddressed
- `project_abrigo_painkiller_evidence_base.md` — evidence base for painkiller claims; inequality evidence is already in MACRO_RISKS corpus
- `feedback_onchain_native_priority.md` — tier-1 on-chain X mandatory; applies to both legs where possible
- `project_phase_a0_exit_verdict.md` — Phase-A.0 remittance EXIT; enables this pivot
- `project_colombia_yx_matrix.md` — Y₄ HH consumption + Y₅ HH income variance are the tier-2 data-acquisition targets per this thesis

## Execution-priority sequencing (user directive 2026-04-24)

1. **Immediate execution** (CPI + TRM already on hand): once X_d is built from COPM per-tx data, run the multi-Y panel against Y₁ TRM RV and Y₂ CPI with same Rev-4 infrastructure.
2. **Parallel data acquisition track**: DANE EMMV / ECV / BanRep TES + household-debt-service — fetch, clean, align to weekly panel. This is a separate work-stream that can run alongside (1).
3. **Differential calibration**: once all Y's are in the panel, compute `Y_inequality = Y_asset_leg − Y_consumption_leg` at weekly frequency. This is the GATE target.
4. **Instrument design**: out of scope for current exercise; follow-on work.
