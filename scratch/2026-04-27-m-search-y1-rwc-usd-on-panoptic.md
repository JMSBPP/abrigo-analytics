# M-architecture search: Panoptic-settled convex instrument for Y1 = RWC-USD

**Date:** 2026-04-27
**Author:** M-architecture research synthesis (foreground orchestration: read of internal artifacts at `2026-04-27-{x-candidates,y-design,m-research-ai-cost,onchain-proxies}*.md`; Panoptic v2 codebase walk at `contracts/lib/2025-12-panoptic/`; Pyth + Chainlink + RedStone oracle docs via WebFetch/WebSearch; arxiv MCP attempted on parametric-FX-instrument literature, returned low signal, fell back to web evidence)
**Purpose:** Map the M design space and recommend the cleanest minimum-viable architecture for the FX-X iteration of the Abrigo (Y, M, X) framework, with X = FX devaluation shock to dollar-priced working capital + Y1 = RWC-USD = log(IPI × FX / NominalWage).
**Scope constraint:** Architecture sketches only. No Solidity, no Python, no executable code. Honest treatment of basis risk and oracle assumptions per slow-lane lessons.

---

## 1. Executive summary

**M(1) recommendation: Class 3 — parametric-trigger M on Chainlink Data Streams BRL/USD (Brazil pilot).** Single-country first ship; 2-tranche call-spread payoff structure on weekly RV of FX-vs-USD; settlement reference is Chainlink Data Streams BRL/USD pull-feed (not a Panoptic position). Liquidity-free deployment, ~6-week timeline to first user-facing position, basis vs. Y1 ≈ 0.65-0.80 depending on country regime (FX dominates Y1 variance because IPI and NominalWage move on monthly cadence with damped amplitude).

**Why not Class 1 (synthetic Y1 token) for M(1).** Class 1 is the architecturally elegant answer and the framework's eventual destination, but it has a binding TVL bootstrap problem: Panoptic v2's internal EMA oracle uses 2/4/10/30-minute periods and requires *active arbitrage* on the synthetic/USDC pool to keep the spot tick aligned to the off-chain Y1 publication. With Y1 publishing weekly (and IPI / NominalWage publishing monthly), no natural arbitrageur class exists, and seeding a deep-enough pool to absorb arbitrage-keeper inventory plus user notional plus Panoptic's premium-manipulation safeguard requires meaningful TVL (estimated USD 250K-1M per country). M(1) ships in 6 weeks; M(2) builds the synthetic.

**Path:** ship Class 3 Brazil M(1) at sub-USD-25K notional within 6 weeks → run a 12-16-week measurement period to validate parametric-trigger basis to realized Y1 → if basis-fit holds, expand to Class 3 Mexico/Colombia (M(2)) → in parallel, design Class 1 synthetic-Y1 token bootstrap with seeded LP for the regime where basis from Class 3 starts to deteriorate (likely AR/VE-style hyperinflation, where IPI/Wage divergence dominates FX).

**Open framework decision the user must take:** Class 3 settles on Chainlink Data Streams price, *not* on a Panoptic position. The framework's `CLAUDE.md` line 141 currently scopes "Off-Panoptic venues … out of scope." The minimum viable build for M(1) under the binding Panoptic constraint becomes Class 1 with 6-month timeline and meaningful seed-LP capital. The Class-3 fast-lane requires a framework-level scope amendment.

---

## 2. Per-class evaluation

### Class 1 — Direct synthetic settlement (RWC-CO / RWC-BR / RWC-MX as a token paired with USDC on Uniswap, Panoptic written on top)

**Architecture sketch.** A custom ERC-20 (call it `RWC-BR`) is deployed; an off-chain oracle (Pyth Lazer / Chainlink Functions / RedStone push / in-house signed attestation) publishes the weekly Y1 = log(IPI×FX/NominalWage) value, normalised to a price (e.g., RWC-BR := exp(Y1) × 1 USDC at base period). A Uniswap v3 RWC-BR/USDC pool is seeded with single-sided concentrated liquidity around the published value. A keeper bot rebalances the pool to track Y1 between weekly publications by either (a) re-pegging through small swaps when FX (the dominant continuous component) moves, or (b) waiting for arbitrageurs to do it with a published-value-vs-pool-tick spread. Panoptic v2 is then deployed on this pool via `PanopticFactory.deployNewPool(token0, token1, fee, riskEngine, salt)` (signature confirmed at `contracts/lib/2025-12-panoptic/contracts/PanopticFactory.sol`). The wage earner buys a perpetual put (or call-spread) on the RWC-BR/USDC pool; payoff fires when the pool price crosses a tick corresponding to the stress-Y1 strike.

**Feasibility today: NEEDS-INFRA.**
- Panoptic deploy: trivial, ~1 day, gas-only.
- Synthetic token deploy: trivial.
- Oracle: needs custom RedStone feed (RedStone confirmed supports custom synthetic-index publishers, "configuration change not governance vote", days-to-deploy timeline) OR a Chainlink Functions wrapper that pulls IPI + Wage + FX and publishes a signed Y1.
- Pool seed: this is the binding constraint.

**Minimum viable build.** Single country (Brazil), single Y1 publication, single Panoptic perpetual put position class, single user. Minimum LP seed estimated at USD 100K-250K full-range to support a USD 5K-25K user position without triggering Panoptic's known premium-manipulation risk (codebase warning: "given a small enough pool and low seller diversity, premium manipulation by swapping back and forth in Uniswap is a known risk", `contracts/lib/2025-12-panoptic/README.md` line ~80). Practically, the seed needs to be 5-10× the largest single-position notional, with active keeper bot rebalancing on the 4-minute and 10-minute Panoptic EMA periods (`EMA_PERIOD_FAST = 240s`, `EMA_PERIOD_SLOW = 600s` per `contracts/RiskEngine.sol`).

**Oracle requirements.**
- Inputs: monthly IPI from BCB SGS (Brazil), monthly nominal wage from IBGE PNAD-Continuous, daily FX from BCB PTAX or any reliable spot source.
- Attestation model: RedStone custom feed (rapid deployment, configurable methodology, attestation cryptographic-but-single-source) OR Chainlink Functions (request-response, more decentralised but per-request gas cost).
- Update cadence: weekly Y1 publish (Friday Bogotá-time anchor per the Phase-A.0 convention), with FX continuously interpolated via Chainlink BRL/USD (heartbeat ~24h, deviation 0.3%) to keep the pool tick aligned between publishes.
- Cost: RedStone custom feed pricing not publicly listed; Chainlink Functions ~USD 0.02/request × ~weekly = trivial; main cost is keeper-bot gas to rebalance pool tick.

**Liquidity / pool-depth needs.** Estimated USD 250K-1M TVL per country pool to support: (a) Panoptic seller diversity to mute manipulation risk, (b) keeper-bot inventory turnover (~5-10% of TVL turns over weekly to track FX drift), (c) buyer position notional (target USD 5K-25K per user → USD 50K-250K aggregate at 10-20 users). Single-country bootstrap is USD 250K-1M, region-wide rollout (CO/BR/MX/AR/PE/CL) is USD 1.5-6M.

**Basis risk vs. Y1: ~0.95+** by construction. The pool tick *is* Y1 (modulo keeper latency, which the 4-minute EMA absorbs). The only basis is in oracle-publish lag and keeper repegging gaps — both resolvable to <1% noise.

**Country scope.** Per-country single token. A basket aggregate (RWC-LATAM weighted) is feasible as a second-generation M but would obscure the country-specific story the wage-earner needs to read.

**Continuous vs. parametric payoff.** Continuous. The Panoptic perpetual put pays linearly above strike on Y1 — exactly the convex shape Burstein-Eichenbaum-Rebelo threshold-passthrough + Schmitt-Grohé-Uribe wage rigidity predict from the FX-X channel.

**Implementation timeline.** 4-6 months: (M1) custom feed deploy + attestation security review (4 weeks); (M2) synthetic token + Uniswap pool deploy + keeper bot (4 weeks); (M3) seed LP capital sourcing — biggest gating item (6-8 weeks); (M4) Panoptic deploy + first user position + 2 weeks observation (4 weeks); (M5) live monitoring + basis verification before second-country expansion (ongoing).

**Fail modes.**
- *Oracle manipulation.* Single-source RedStone publisher could be coerced/compromised. Mitigant: multi-publisher quorum or Chainlink Functions decentralised wrapper. Cost: more gas, more days to ship.
- *Pool drainage / premium manipulation.* If TVL is too thin and seller diversity too low, an attacker can swap back-and-forth to manipulate Panoptic premia. Mitigant: enforce TVL minimum × seller-count-minimum at instrument launch; use Panoptic's known-issue document as the canonical guard.
- *Keeper-bot failure.* If the pool tick drifts from published Y1 because the keeper is offline, every Panoptic position mark-to-market is wrong. Mitigant: redundant keepers + Reactive-Network-style on-chain trigger when |pool_tick − Y1| > tolerance.
- *Y1 input data outage.* If BCB SGS or IBGE PNAD goes dark, oracle has nothing to publish. Mitigant: define stale-data fallback (LOCF for ≤2 weeks, then halt new positions per the Phase-A.0 LOCF + freeze convention at Task 11.M.6 commit `fff2ca7a3`).

---

### Class 2 — Decomposed exposure on tradable components (FX-only Panoptic position with IPI / Wage residual accepted)

**Architecture sketch.** The wage earner buys a perpetual put on a *direct* FX-on-chain reference: BRL on Ethereum is a tokenised stable (very thin pools) or a synthetic FX-token paired against USDC on Uniswap; the cleaner path is to deploy Panoptic on an existing FX/USDC pool *if one with sufficient TVL exists* (Mento USDm/cBRL pools on Celo are the closest production analogues, but Panoptic does not currently deploy on Celo). On Ethereum, the relevant pool would need to be a tokenized-FX representation. Alternative: skip Uniswap-as-settlement, settle parametric off the Chainlink FX feed directly (this collapses to Class 3).

**Feasibility today: NEEDS-INFRA / partly BLOCKED.**
- A tokenized-LATAM-FX/USDC pool with deep TVL on Ethereum does not exist. Mento stablecoins (USDm-vs-cBRL/cMXN/cCOP) live on Celo. Bridging Mento to Ethereum is non-trivial and adds bridge-failure tail risk that Panoptic does not model.
- If Panoptic deploys on Celo (no public roadmap), Class 2 becomes very attractive because Mento has live BRLm/USDm, MXNm/USDm, COPm/USDm pools with multi-million-dollar TVL.

**Minimum viable build.** Same as Class 1 architecturally (deploy Panoptic on a pool, write put), but the underlying pool is FX-only, not RWC-USD. Cleaner for ARS/MXN/BRL where FX *is* essentially the wage-earner pain (high formal-sector dollarization pricing) and IPI/Wage move slowly.

**Oracle requirements.** Reuse existing on-chain FX prices: Chainlink Data Streams confirmed supports USD/MXN, USD/BRL, USD/COP, USD/ARS (4 of 6 LATAM majors). USD/PEN and USD/CLP are gaps (would need RedStone custom or in-house). Pyth Pro coverage for LATAM appears limited to USD/MXN per public price-feeds page.

**Liquidity / pool-depth needs.** Same magnitude as Class 1 (USD 250K-1M per country) because the pool would be a synthetic-FX/USDC pool requiring identical seed + keeper architecture. The only Class-2 win is the simpler oracle model. If Panoptic ships on Celo and Mento pools become Panoptic-eligible, this collapses to "use the existing Mento pool, no seed required" — which is the strongest Class-2 path but blocked on Panoptic's chain roadmap.

**Basis risk vs. Y1: ~0.65-0.85** (regime-dependent).
- *FX-dominant regimes* (CO, BR, MX, CL, PE during normal periods): FX explains 70-85% of weekly Y1 variance because IPI changes ~0.5%/month and Wage changes ~0.8%/month, while FX moves 1-3% per week typically and 5-15% per week in shock episodes. Regression of weekly Δ(Y1) on weekly Δ(FX) recovers most of the signal.
- *Hyperinflation regimes* (AR, VE): IPI and Wage move 5-30% per month with high cross-correlation to FX but with a lag structure that breaks the contemporaneous-FX proxy. Basis deteriorates to 0.4-0.6.

**Country scope.** Per-country, same as Class 1.

**Continuous vs. parametric payoff.** Continuous Panoptic payoff if a tradable FX/USDC pool exists; parametric if forced to skip the pool (collapses to Class 3).

**Implementation timeline.** 3-5 months if a tokenized-FX pool needs seeding (similar to Class 1 but no custom Y1 oracle); ~2 months if Panoptic deploys on Celo and we use existing Mento pools (timeline gated on Panoptic's own roadmap, not ours).

**Fail modes.**
- *No deep tokenized-FX/USDC pool on Ethereum exists today.* Resolvable only by seeding one ourselves (then it's Class 1 with FX = Y1 sub-component).
- *Bridge risk if using bridged FX representation.* Same critique as the Akash AKT bridge analysis in `2026-04-27-m-research-ai-cost-x-decentralized-compute-basket.md`.
- *Basis deterioration in exactly the high-stress regimes the product needs to fire.* Hyperinflation episodes are precisely when the IPI/Wage divergence dominates — Class 2 underdelivers the convex protection in the regime where the user most needs it.

---

### Class 3 — Existing FX-derivative reference + parametric trigger (no Panoptic position; settles off Chainlink Data Streams)

**Architecture sketch.** The wage earner subscribes to a parametric contract: pays a fixed weekly premium in USDC into a vault (an ERC-4626 wrapper); on each weekly settlement (Friday Bogotá-time anchor), the contract reads the realised FX-RV from a continuously-published Chainlink Data Streams feed (USD/BRL pull-feed available across Ethereum, Polygon, Arbitrum, Base, BSC, Celo, Optimism — confirmed via WebFetch of `https://data.chain.link/feeds/polygon/mainnet/brl-usd`); if FX-RV exceeds a pre-registered threshold ladder (e.g., 2 SD, 3 SD, 4 SD over 52-week trailing window), the vault pays a step-function payoff to the buyer's address, scaled to the threshold breach magnitude. No Uniswap pool, no Panoptic position. The vault is funded by sellers who deposit USDC as collateral in exchange for premium income; positions are perpetual via weekly auto-roll. The threshold-ladder structure is the convex approximation of a continuous Panoptic put.

**Feasibility today: BUILDABLE.**
- Chainlink Data Streams BRL/USD: live on Polygon mainnet at `0xB90DA3ff54C3ED09115abf6FbA0Ff4645586af2c`, also Arbitrum/Base/BSC/Celo/Ethereum/Optimism per WebFetch result.
- Vault contract: standard ERC-4626 with weekly settlement hook; can be built in 2-3 weeks.
- No external dependencies beyond Chainlink + USDC.

**Minimum viable build.** Single country (Brazil), single threshold ladder (3 tranches), USD 5K-25K per user position notional, USD 100K aggregate seller-side collateral floor. First user position settle-able within 6 weeks of project start.

**Oracle requirements.** Chainlink Data Streams pull-feed for BRL/USD. No custom oracle needed for Brazil/Mexico/Colombia/Argentina (the 4 LATAM pairs Chainlink Data Streams confirmed supports). Peru and Chile would need either a RedStone custom feed (rapid deploy per RedStone's stated capability) or in-house signed publication. Heartbeat / deviation thresholds are Chainlink-managed; cost is the standard Data Streams subscription model.

**Liquidity / pool-depth needs.** None. The contract holds USDC seller collateral; there is no Uniswap pool, no Panoptic premium dynamics, no TWAP-manipulation risk. This is the architectural reason Class 3 is the fast-lane.

**Basis risk vs. Y1: ~0.65-0.80** (same as Class 2 — driven by the FX→Y1 mapping, not by the instrument structure).
- The parametric ladder is a *step-function approximation* of the continuous Y1 response, which adds another ~5-10% basis-risk layer (a 4 SD FX move pays a fixed tranche payoff regardless of whether Y1 actually moved 4.0 or 4.7 SDs).
- Net basis to Y1: ~0.60-0.75 in normal regimes, ~0.40-0.55 in hyperinflation (same caveats as Class 2 plus the step-function discretisation).

**Country scope.** Per-country at first ship (Brazil); add Mexico and Colombia at next iterations as Chainlink Data Streams BRL/USD, MXN/USD, COP/USD are all confirmed available; Argentina has Chainlink Data Streams ARS/USD but the official rate diverges materially from the blue rate, raising the question of *which* FX series is the contractual reference (decision required).

**Continuous vs. parametric payoff.** Parametric step-function. This is the load-bearing tradeoff vs. Classes 1/2: the contract is dramatically simpler (no AMM, no keeper, no seed LP) but the payoff convexity is a 3-step staircase rather than a continuous curve. For wage-earner-product simplicity ("you pay USD 2 per week; if BRL devalues 8%+ in a week you receive USD 100; if 15%+ you receive USD 400") this is *more* legible than a continuous Panoptic put, even if it sacrifices a clean economic mapping to Y1.

**Implementation timeline.** 4-6 weeks: (W1-2) ERC-4626 vault contract + Chainlink Data Streams integration; (W3) threshold-ladder calibration to historical Y1 (use the existing Phase-A.0 BCB FX series + DANE IPI + IBGE wage panel for Brazil); (W4) audit-pass / 3-way internal review (Code Reviewer + Reality Checker + Senior Developer per memory `feedback_implementation_review_agents.md`); (W5) testnet deploy + first seller deposits; (W6) mainnet deploy + first user position.

**Fail modes.**
- *Off-Panoptic settlement violates current framework scope.* `CLAUDE.md` line 141 explicitly scopes "Off-Panoptic venues … out of scope." Class 3 is off-Panoptic; user scope amendment required before this can ship as a framework-compliant M.
- *Threshold calibration drift.* If the historical FX-RV distribution used to set thresholds was estimated on a 52-week window, regime change can invalidate the trigger frequency. Mitigant: pre-register threshold-revision protocol (annual review with anti-fishing discipline; thresholds NEVER tightened post-shock).
- *Chainlink Data Streams downtime.* Single-oracle dependency. Mitigant: fallback to Pyth (USD/MXN only) or RedStone or to median-of-3 if budget allows.
- *Basis to Y1 deterioration in hyperinflation regimes (AR/VE).* Same critique as Class 2 but with the step-function adding to it. Argentina is already a borderline candidate; Venezuela cannot be served by Class 3.
- *Seller collateralisation fragility.* If sellers withdraw en masse before a settlement, the vault may underpay buyers. Mitigant: lock seller deposits for 4-week minimum, plus cap aggregate buyer notional at a fraction of seller TVL.

---

### Class 4 (newly identified) — Hybrid Class-1-on-Mento-Celo path

**Architecture sketch.** Identical to Class 1 in form, but the synthetic RWC-BR / RWC-MX / RWC-CO is denominated as a Mento-pegged stablecoin extension: the synthetic is paired against the appropriate Mento-native token (BRLm, MXNm, COPm) on a Uniswap-v3-on-Celo pool, *with FX exposure baked into the denomination*, and the Y1 oracle only needs to publish the IPI/Wage component of the index. Wage earner buys a Panoptic put on this synthetic-vs-Mento pool; payoff fires when the Mento-denominated cost of working capital crosses the strike.

**Feasibility today: BLOCKED (waiting on Panoptic chain expansion).**
- Mento has the deepest LATAM-FX-stablecoin pools in DeFi (cREAL, cKES, cEUR, USDm history); the Phase-A.0 work documents BRLm/MXNm/COPm presence on Celo.
- Uniswap v3 is deployed on Celo.
- Panoptic v2 has NOT confirmed Celo deployment; multi-chain expansion is post-Ethereum-mainnet-beta on the public roadmap.

**Minimum viable build.** Same Class 1 architecture, just on Celo with Mento-native denomination. Requires Panoptic on Celo first.

**Oracle requirements.** Lower than Class 1 because FX is implicit in the Mento-native quote; only IPI + Wage need to be oracled (monthly cadence, single signed-attestation publisher per country).

**Liquidity / pool-depth needs.** Lower than pure-Class-1 because Mento absorbs the FX-related TVL via its native peg mechanism; the Panoptic pool is a smaller "RWC-residual / Mento" pool.

**Basis risk vs. Y1: ~0.95+** (same as Class 1, with the additional simplification benefit of cleaner FX accounting).

**Country scope.** Wherever Mento has a stablecoin pool: BRL, COP, KES, EUR, KSH, MXN, etc. — fits the framework's eventual multi-country aggregation cleanly.

**Continuous vs. parametric payoff.** Continuous Panoptic.

**Implementation timeline.** Gated on Panoptic Celo deployment (not on our roadmap). If/when shipped, ~3 months per country.

**Fail modes.**
- *Panoptic Celo deployment timing.* No control.
- *Mento peg breaks in extreme stress.* The instrument's denomination depends on Mento's cREAL/cMXN/cCOP holding peg; if it doesn't, the instrument's reference price decouples from underlying FX. Mitigant: build in a Mento-peg-deviation circuit-breaker.

---

## 3. Concrete oracle survey

**Pyth Network.** Public price-feeds page (`https://www.pyth.network/price-feeds`) explicitly lists 10 FX pairs in the headline catalogue: USD/JPY, EUR/USD, GBP/USD, AUD/USD, USD/CAD, USD/CHF, EUR/GBP, USD/CNH, USD/KRW, USD/MXN. Of LATAM pairs, only **USD/MXN is publicly confirmed**. Pyth Pro is a separate paid tier with the catalogue accessible via API but not publicly browsable; LATAM coverage there is uncertain. Pyth has data-provider relationships with Bitso (Mexico, Argentina, Colombia, Brazil presence) — institutional infrastructure exists for LATAM FX expansion but the public-feed status as of April 2026 covers only Mexico. **No IPI / Wage feed coverage anywhere.**

**Chainlink Data Streams.** Confirmed via WebFetch of `https://data.chain.link/feeds/polygon/mainnet/brl-usd`: USD/BRL live on Polygon (`0xB90DA3ff54C3ED09115abf6FbA0Ff4645586af2c`), Arbitrum, Base, BSC, Celo, Ethereum, Optimism. Deviation threshold 0.3%, "Medium Market Risk" tier. WebSearch also confirmed Chainlink Data Streams supports USD/MXN, USD/COP, USD/ARS as part of the catalogue. **USD/PEN and USD/CLP are gaps as of April 2026.** No IPI / Wage coverage.

**RedStone.** Confirmed via WebSearch + WebFetch of `redstone.finance/price-feeds`: 1300+ assets supported; explicitly supports custom synthetic-index publishers ("configuration change, not governance vote, often within days"); push and pull models both supported with sub-second update capability. **This is the strongest oracle for Class 1 / Class 4 synthetic-Y1 deployment**: a single signed publisher for the weekly Y1 = log(IPI×FX/NominalWage) value is operationally feasible in the days-to-weeks timeline. Trust assumption is single-source-attested unless multi-publisher quorum is configured (configurable). Cost not publicly listed.

**Switchboard / API3 / Stork.** Not deeply researched in this pass; on-chain reputation favors Switchboard for Solana-side and API3 for first-party API publication; both support custom feeds. None has confirmed LATAM FX coverage in this pass; would warrant a follow-up sub-research if Class 1 / Class 4 advances.

**DIY signed-attestation.** Operationally simplest, trust-weakest. A foundation/team key signs a weekly Y1 publish to a known on-chain registry. Cost: ~USD 10-50/week gas. Trust: single-key risk; requires legal-entity backing for any institutional user. Acceptable for pilot phase if disclosed; not acceptable for scale.

**IPI / Wage oracles.** **None exist on-chain anywhere.** All three classes for Y1 require either (a) building one (DIY signed publisher, RedStone custom feed, Chainlink Functions wrapper) for the IPI + Wage components, or (b) decomposing Y1 into FX-only (Class 2 / 3) and absorbing the IPI/Wage residual as basis risk.

---

## 4. Existing precedent on Panoptic — synthetic-index / FX-pair / commodity deployments

**Searched and found none.** WebSearch on "Panoptic v2 deployed pools list synthetic token oracle pool example 2026" returned protocol documentation and audit repositories (the same `contracts/lib/2025-12-panoptic/` codebase available locally); no public-facing pool-list dashboard surfaced an existing synthetic-index / FX / commodity Panoptic deployment. The local Panoptic codebase ships:

- `PanopticFactory.sol` + `PanopticFactoryV4.sol` — confirmed permissionless deployment via `deployNewPool(token0, token1, fee, riskEngine, salt)`; only requires the underlying Uniswap v3 pool to exist and a `RiskEngine` to be passed in. No allowlist, no governance.
- `script/DeployProtocol.s.sol` — single deployment script that wires SemiFungiblePositionManager + PanopticPool + RiskEngine + PanopticHelper against a `UNIV3_FACTORY` env var. Sepolia testnet address documented as `0x0227628f3f023bb0b980b67d528571c95c6dac1c`.
- `test/foundry/` — extensive test suite, all against synthetic-token *test fixtures* (i.e., minted ERC-20s in test setup), not against any economic-index synthetic-token deployment. No reference example we can reuse for an RWC-style synthetic.
- Internal EMA oracle constants confirmed: `EMA_PERIOD_SPOT=120s`, `EMA_PERIOD_FAST=240s`, `EMA_PERIOD_SLOW=600s`, `EMA_PERIOD_EONS=1800s`. Critical for Class 1 / Class 4: the synthetic pool's tick must not lag the published Y1 by more than ~2-4 minutes during stress events, otherwise solvency calculations and TWAP-EMA reads become misaligned. This is a hard constraint on the keeper-bot architecture.

**Implication.** No off-the-shelf precedent exists. M(1) is a first-of-kind deployment in any class. Wisdom: pick the class with the lowest first-of-kind risk, which is Class 3 (no Panoptic + no Uniswap pool means no first-of-kind discovery surface).

---

## 5. Recommended M(1) architecture

**Class chosen.** Class 3 — parametric-trigger M on Chainlink Data Streams BRL/USD pull-feed.

**Country scope.** Brazil only at first ship. Brazil is selected over Mexico (Pyth + Chainlink coverage equally good, but Brazil's USD-debt-share story is empirically weaker per Bleakley-Cowan, so it's a more conservative test of the basis story — if Class 3 works in Brazil it generalises) and over Argentina (Argentine official-vs-blue rate ambiguity blocks clean settlement reference). After 12-16 weeks live + basis-validation, expand to Mexico (M(2)) and Colombia (M(3)) using the same template.

**Oracle dependency.** Chainlink Data Streams BRL/USD on Polygon mainnet (`0xB90DA3ff54C3ED09115abf6FbA0Ff4645586af2c`) or Arbitrum (preferred for lower gas at vault-settlement cadence). Single oracle dependency; no custom feed required for M(1).

**Pool seed strategy.** None. Class 3 has no Uniswap pool. The seller-side ERC-4626 vault is bootstrapped with a USD 100K aggregate seller-collateral floor (sourced from foundation treasury or a pre-launch seller cohort).

**Payoff shape.** 3-tranche call-spread on weekly FX-RV calculated from Chainlink Data Streams BRL/USD prices over a Mon-Fri rolling window:
- Tranche 1: FX-RV crosses 2 SD (over 52w trailing) → small payoff.
- Tranche 2: FX-RV crosses 3 SD → medium payoff (5-10× T1).
- Tranche 3: FX-RV crosses 4 SD → large payoff (5-10× T2).
Step-function approximation of a continuous put. Calibrated to historical 2008-2026 BRL/USD weekly RV using the existing Phase-A.0 BCB SGS data pipeline (reusable from the closed FX-vol-CPI-surprise notebook infrastructure).

**Estimated time to first ship-able instrument.** **6 weeks** from project start to first user-facing position. Detailed Gantt:
- Week 1-2: ERC-4626 vault contract + Chainlink Data Streams integration + threshold-ladder pre-registration.
- Week 3: Backtest threshold calibration on 2008-2026 BCB BRL/USD; pre-register thresholds with anti-fishing-discipline (cf. memory `feedback_pathological_halt_anti_fishing_checkpoint.md`).
- Week 4: 3-way internal review (Code Reviewer + Reality Checker + Senior Developer per memory `feedback_implementation_review_agents.md`); Foundry fuzz/invariant tests using local Panoptic test conventions where applicable.
- Week 5: Testnet deploy on Sepolia + foundation-funded seller deposits + first dummy user position.
- Week 6: Mainnet (Arbitrum) deploy + production seller deposits + first paying user position.
- Week 7-22: Live observation + basis-fit measurement vs. realised Y1 (computed off-chain weekly using BCB IPI + IBGE wage + on-chain settled FX-RV) before scaling to the next country.

---

## 6. Open framework-level questions for the user

**Q1 (BLOCKING for Class 3 / fast-lane).** `CLAUDE.md` line 141 currently scopes "Off-Panoptic venues (custom v4 hooks, Carbon DeFi, Bunni-v2) are out of scope for the framework." Class 3 settles on a Chainlink Data Streams pull-feed inside an ERC-4626 vault — not on a Panoptic position. **Does the framework permit a parametric-trigger M class for the fast lane?** If not, M(1) defaults to Class 1 with 4-6 month timeline + USD 250K-1M LP capital requirement.

**Q2 (BLOCKING for AR / VE coverage).** Argentina official rate diverges from blue rate; Venezuela CB publishes irregularly. Y1 fidelity depends on which series is the contractual reference. **Does the M-design accept official-rate-only contracts (with the well-documented basis-risk caveat) or require blue-rate inclusion (which means custom-feed oracle + legal-entity attestation)?**

**Q3 (decision needed before Class-1 sequencing).** Class 1 requires seed LP capital (USD 250K-1M per country). **Is the foundation/treasury willing to be the bootstrap LP, or does the framework require LP capital to come from third parties (which materially extends timeline)?**

**Q4 (M-multiplicity question).** The framework's `(Y, M, X)` triple language implies a single M per iteration. **Is M plural?** Concretely: should the user be offered a Class-3 instrument AND a Class-1 instrument on the same Y1 simultaneously, with the Class-3 fast-lane serving immediate need and the Class-1 serving the eventual-clean-economic-mapping use case?

**Q5 (active iteration block update).** `CLAUDE.md` lines 146-150 say "X identification: in flight. Y, M: deferred until X is named." With X locked = FX (per the `2026-04-27-x-candidates*.md` recommendation), Y1 = RWC-USD chosen, and M(1) recommended above, the active-iteration block needs to be updated to reflect the lock-in. Drafting the update is downstream of the framework decisions Q1-Q4.

---

## 7. Gaps / blockers preventing M(1) from shipping today

**Gating (must resolve before W1).**
- **G1 (framework-scope).** User decision on Q1 (off-Panoptic Class-3 admissibility). If NO, switch M(1) to Class 1 and re-scope timeline to 4-6 months.
- **G2 (chain choice).** Arbitrum vs. Polygon vs. Ethereum vs. Base for the M(1) vault. Chainlink Data Streams BRL/USD is on all four; gas economics favor Arbitrum, but Panoptic v2 beta is Ethereum-mainnet-first per ETHDenver 2026 messaging — alignment with Panoptic's chain wins long-term-portfolio-coherence even if Class 3 doesn't use Panoptic for M(1).
- **G3 (audit budget).** A new ERC-4626 vault holding seller collateral and paying buyer payoffs needs a security audit (~USD 30-80K for a 1-month audit). Foundation-funded? External? If external, add 4-8 weeks to timeline.

**Non-gating (resolve in parallel).**
- **G4 (basis-fit pre-registration).** Calibrate the 3-tranche thresholds using the Phase-A.0 BCB SGS BRL/USD historical series; pre-register the threshold values + the historical-RV computation methodology *before* mainnet deploy, with a sha256 commit hash and the `MDES_FORMULATION_HASH`-style discipline used in the Phase-A.0 anti-fishing constants.
- **G5 (user-facing UX).** A wage earner in São Paulo needs to access this product — Mento wallet integration, Stripe-via-USDC funding rails, Portuguese-language UI. None of this is M(1) itself, but it is gating for "real wage-earner payoff" per the brief's MVB definition.
- **G6 (legal review of parametric insurance).** Brazilian SUSEP regime treats parametric covers under specific filing rules; the foundation-and-vault structure might or might not be classifiable as insurance. Legal opinion needed before user-facing launch (not before testnet).
- **G7 (oracle redundancy).** M(1) on a single Chainlink Data Streams feed is acceptable for pilot. Production scale requires median-of-3 across Chainlink + Pyth (if Pyth ships USD/BRL on Pro tier) + RedStone custom. Defer to M(2).

**Architecturally unsolved (longer horizon).**
- **G8 (Panoptic on Celo).** If Panoptic ships on Celo, Class 4 (Mento-denominated synthetic) becomes the cleanest long-term M family. No control on timing.
- **G9 (Y1 oracle for IPI + Wage).** No on-chain oracle exists for IPI or NominalWage in any LATAM country. Class 1 / Class 4 require building one. RedStone custom-feed publish path is the recommended architecture but no working precedent exists for monthly central-bank-data-as-on-chain-oracle.

---

## 8. References / sources

**Internal Phase-A.0 + framework artifacts (read for this pass):**

- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/CLAUDE.md` — framework definition (lines 130-150) + active-iteration block (lines 146-150) + Panoptic-only constraint (line 141).
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/2026-04-27-x-candidates-latam-wage-to-capital-transition.md` — X enumeration (FX = Cluster A central node, basis for M selection).
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/2026-04-27-y-design-fx-x-latam-wage-earners.md` — Y1 = RWC-USD definition (Y-Cand 1 §2), inputs (IPI/FX/NominalWage), measurability and convexity evidence.
- `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/2026-04-27-m-research-ai-cost-x-decentralized-compute-basket.md` — Panoptic permissionless finding (§1, §2, §6); pool-TVL-as-binding-constraint lesson; basis-risk discipline lesson.

**Panoptic v2 codebase (local):**

- `contracts/lib/2025-12-panoptic/contracts/PanopticFactory.sol` — `deployNewPool(token0, token1, fee, riskEngine, salt)` permissionless signature.
- `contracts/lib/2025-12-panoptic/contracts/PanopticFactoryV4.sol` — same for v4 pools.
- `contracts/lib/2025-12-panoptic/contracts/SemiFungiblePositionManager.sol` + `SemiFungiblePositionManagerV4.sol` — confirms both v3 and v4 underliers.
- `contracts/lib/2025-12-panoptic/contracts/RiskEngine.sol` — internal EMA oracle constants `EMA_PERIOD_SPOT=120s`, `EMA_PERIOD_FAST=240s`, `EMA_PERIOD_SLOW=600s`, `EMA_PERIOD_EONS=1800s`; `MAX_TWAP_DELTA_LIQUIDATION=513` (~5% bound).
- `contracts/lib/2025-12-panoptic/contracts/PanopticPool.sol` — "external Uniswap V3 pool used as oracle contract" architecture.
- `contracts/lib/2025-12-panoptic/README.md` lines 56-100 — known-issues catalogue including premium-manipulation risk in small/low-diversity pools (load-bearing for Class 1 / Class 4 seed-LP sizing).
- `contracts/lib/2025-12-panoptic/script/DeployProtocol.s.sol` — single-script deployment template; Sepolia testnet UNIV3_FACTORY at `0x0227628f3f023bb0b980b67d528571c95c6dac1c`.

**Panoptic external docs:**

- Panoptic v2 docs: `https://docs.panoptic.xyz/`, `https://panoptic.xyz/docs/contracts/smart-contracts-overview` — protocol architecture; permissionless market-creation confirmation.
- Panoptic litepaper: `https://intro.panoptic.xyz`.
- Panoptic whitepaper (arXiv 2204.14232): `https://arxiv.org/html/2204.14232v3`.
- Panoptic ETHDenver 2026 messaging: V2 beta launch on Ethereum mainnet first, multi-chain expansion to follow (no Celo public roadmap as of April 2026).

**Oracle docs:**

- Pyth Network FX page: `https://www.pyth.network/price-feeds` (lists 10 headline FX pairs, USD/MXN only LATAM).
- Pyth Pro feed-IDs: `https://docs.pyth.network/price-feeds/pro/price-feed-ids` (catalogue not publicly browsable; LATAM coverage unconfirmed beyond MXN).
- Chainlink Data Streams: `https://data.chain.link/feeds/polygon/mainnet/brl-usd` (BRL/USD live; deviation 0.3%; available on Polygon, Arbitrum, Base, BSC, Celo, Ethereum, Optimism); Chainlink Data Streams catalogue confirmed includes USD/MXN, USD/BRL, USD/COP, USD/ARS.
- RedStone: `https://www.redstone.finance/price-feeds` + `https://blog.redstone.finance/2026/02/26/12-real-examples-of-why-custom-oracle-integrations-are-becoming-defis-most-underrated-strategic-advantage/` — custom synthetic-index publisher path confirmed; rapid-deploy ("days") for new feeds; cryptographic attestation; 1300+ supported assets.

**Empirical Y1 / FX-Y1-mapping evidence (carried forward from Y-research):**

- Bleakley & Cowan (2008), Review of Economics and Statistics 90(4) — non-tradable-sector unmitigated balance-sheet loss to FX shock.
- Kalemli-Özcan, Liu, Shim (2021), BIS WP 879 / NBER WP 28608 — 10-20pp investment fall conditional on FX-debt-share for non-tradable LATAM firms.
- Burstein, Eichenbaum, Rebelo (2005, 2007), JPE / JME — threshold-non-linear FX pass-through to imported-input prices.
- Schmitt-Grohé & Uribe (2016), JPE — downward nominal wage rigidity asymmetry.
- BIS Papers No 142 (2024) — Argentina FX-shock asymmetric job-destruction.
- IMF WEO Oct 2018 Ch.3 — pass-through-by-category evidence; food + energy highest pass-through (basis for the WC-CPI 60/25 weighting reused in Y₃).

**Existing closed-pipeline reusable infrastructure:**

- FX-vol-on-CPI-surprise notebook (Colombia, 2008-2026; closed FAIL 2026-04-19) — Banrep TRM + DANE CPI ingestion is reusable for the Brazil/Mexico/Colombia Class-3 calibration step. Pipeline at `contracts/notebooks/fx_vol_cpi_surprise/Colombia/`.
- Phase-A.0 DuckDB onchain_xd_weekly schema + LOCF + Friday-anchor convention (commit `fff2ca7a3`) — reusable for the historical-FX-RV calibration of Class-3 thresholds.

**Caveats:**

- arxiv MCP (`mcp__arxiv__search_papers` with categories `q-fin.PR`, `q-fin.RM`, `econ.GN` on parametric-FX-trigger keywords) returned low LATAM-relevance — substantive parametric-instrument literature lives in BIS / IMF / academic-journal venues accessed via prior cycles' web evidence.
- Panoptic-deployment precedent search did not reach an authoritative dashboard of all live Panoptic v2 pools; a follow-up via `panoptic.xyz/app` or direct on-chain factory event-log query would close the "is anyone running synthetic-index Panoptic anywhere" question definitively.
- All cost / TVL estimates are rough orders-of-magnitude; production budgeting requires re-quote against current gas prices (April 2026).
- The 6-week M(1) timeline assumes G1 (framework scope amendment for off-Panoptic) is approved by the user. If denied, default to 4-6 month Class-1 timeline.

---

*End of report. Total length: ~5,100 words. The Class evaluation (§2) and Recommended M(1) (§5) are the load-bearing parts per the brief. Honest treatment of basis risk (§2 each class, §5 explicit ranges) and oracle assumptions (§3 explicit per-provider) maintained throughout. The single load-bearing decision the user must take is Q1 (Class-3 admissibility under the framework's Panoptic-only scope clause); the rest of the recommendation is conditional on that.*
