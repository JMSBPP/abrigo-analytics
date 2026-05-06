---
name: NO Mento↔Carbon protocol-level integration (Rev-5.3.7 finding)
description: Mento V3 deployment manifest contains zero references to Carbon DeFi or BancorArbitrage; Carbon hosts Mento basket tokens as standard ERC-20s; Carbon-Mento volume is third-party DEX activity (mostly Bancor's own arb routers), NOT Mento Reserve user demand. Pivots β-track Rev-3 X_d to Broker-native signal.
type: project
originSessionId: phase0-vb-mvp / Rev-5.3.7 strategic re-evaluation 2026-04-27
---

**Fact**: As of 2026-04-27, the Mento V3 deployment manifest at `https://docs.mento.org/mento-v3/build/deployments/addresses.md` contains **zero references to Carbon DeFi or BancorArbitrage**. The complete contract roster on Celo mainnet is:

**V2 (legacy, still active):**
- Broker `0x777A8255cA72412f0d706dc03C9D1987306B4CaD`
- BiPoolManager `0x22d9db95E6Ae61c104A7B6F6C78D7993B94ec901`
- Reserve `0x9380fA34Fd9e4Fd14c06305fd7B6199089eD4eb9`

**V3 (new architecture):**
- Router `0x4861840C2EfB2b98312B0aE34d86fD73E8f9B6f6`
- FPMMFactory `0xa849b475FE5a4B5C9C3280152c7a1945b907613b`
- ReserveV2 `0x4255Cf38e51516766180b33122029A88Cb853806`
- FPMM pools: USDT/USDm `0x0FEBa760d93423D127DE1B6ABECdB60E5253228D`; USDC/USDm `0x462fe04b4FD719Cbd04C0310365D421D02AaA19E`; axlUSDC/USDm `0xb285d4C7133d6f27BfB29224fb0D22E7EC3ddD2D`; GBPm/USDm `0x8C0014afe032E4574481D8934504100bF23fCB56`

**StableTokens (12 currencies):** USD, EUR, BRL, XOF, KES, PHP, **COP `0x8a567e2aE79CA692Bd748aB832081C45de4041eA`**, GHS, GBP, ZAR, CAD, AUD, CHF, JPY, NGN.

**Why this matters**: the Carbon-basket X_d thesis (originally authored under Phase-A.0 Task 11.N.2) was framed as "closed-loop two-sided market across Mento working-class-stablecoin basket ↔ global-asset basket" — implicitly assuming Carbon was a Mento-protocol-integrated exchange channel. Empirical Mento manifest fetch + Dune contract-decoder verification 2026-04-27 disconfirms this:

- Mento V3 manifest has zero Carbon/Bancor references.
- Mento is a closed Reserve+Broker+Pools system; Reserve never mints/burns in response to a Carbon trade.
- Carbon `tokenstraded` events on Celo are pure third-party-DEX activity. Anyone can pair Mento basket tokens with USDT/USDC/WETH on Carbon since Mento basket tokens are standard ERC-20s.
- The dominant traders on Carbon-Mento pairs are Bancor's own arbitrage routers (V1 `0x8c05ea30…` 2024-07-25 → 2025-07-01; V2 `0x20216f30…` 2025-07-02 → present), extracting value from price-misalignment between Mento Reserve pricing and secondary-market liquidity.

**Empirical comparison (Dune query 7382711, 0.124 credits)**:

| Signal | Lifetime events | Distinct traders | Events in Rev-2 panel window | Ratio (Broker/Carbon) |
|---|---|---|---|---|
| Mento Broker V2 Swap | 6,161,979 | **383,303** | 4,226,345 | — |
| Carbon `tokenstraded` (current X_d) | 2,231,212 | **147** | 1,785,588 | **2,604× more traders on Broker** |

**How to apply**:

1. **NEVER frame Carbon-Mento volume as Mento-native demand.** It is third-party DEX activity. The framing breaks the analytical interpretation of any X_d signal built from Carbon `tokenstraded` events.

2. **For β-track Rev-3 spec authoring (Task 11.P.spec-β; deferred)**: pivot X_d to Mento-Broker-native:
   - **Primary X_d**: `mento_celo.broker_evt_swap` events on Broker `0x777A8255…` aggregated weekly (Friday anchor); partitioned by direction (mint vs redeem) and basket currency.
   - **Secondary X_d**: V3 FPMM pool swap events (when Dune decodes Router V3 — currently 0 decoded tables for `0x4861840C2E…`; check `searchTablesByContractAddress` periodically).
   - **Diagnostic X_d**: StableToken `Transfer` events with `from = 0x0` (mint) / `to = 0x0` (burn) per currency.

3. **For any future research**: cross-check protocol-level integration claims by fetching the official deployment manifest BEFORE building analytical pipelines off third-party-DEX data. Mento V3 docs URL is the authoritative source for Mento contract identity.

4. **NB-α scope-mismatch close-out**: NB-α terminates at sub-task 12 (HEAD `2b46ef0f6`); sub-tasks 13-31 superseded. Closer cells in NB1 + NB2 document the compound 3-layer scope-mismatch.

5. **PR #74 disposition**: closed (NOT merged) at upstream `wvs-finance/ThetaSwap-core` to avoid propagating Rev-5.3.5/6/7 contamination.

**Three-layer compound scope-mismatch summary** (all 3 layers compound on the SAME X_d):
- Rev-5.3.5: per-currency proxy `carbon_per_currency_copm_volume_usd` filtered to `0xc92e8fc2…` Minteo (not Mento-native COPm `0x8A567e2a…`)
- Rev-5.3.6: basket-aggregate partition rule V1-only; broken post-2025-07-01 (V2 successor `0x20216f30…` not in whitelist; 78% post-July contamination)
- Rev-5.3.7: Carbon DeFi has no protocol-level Mento integration; entire X_d signal is third-party-DEX volume not Mento Reserve user demand

**Audit trail**:
- Rev-5.3.5 disposition: `scratch/2026-04-26-mr-beta-1-1-halt-resolution-beta.md`
- Rev-5.3.6 disposition: `scratch/2026-04-27-x-d-partition-rule-staleness-disposition-beta.md`
- Rev-5.3.7 disposition (Option A pivot): `scratch/2026-04-27-x-d-strategic-re-evaluation-disposition.md`
- Mento V3 deployment manifest: https://docs.mento.org/mento-v3/build/deployments/addresses.md
- Dune queries: 7382618, 7382632, 7382639, 7382645, 7382647, 7382711

## Related memory

- `project_carbon_defi_attribution_celo.md` — V1 + V2 + CarbonController address roster (β-corrigendum landed)
- `project_carbon_user_arb_partition_rule.md` — V1-only partition broken post-2025-07-01 (β-corrigendum landed)
- `project_mento_canonical_naming_2026.md` — Mento basket addresses (β-corrigendum on COPm landed)
- `project_abrigo_mento_native_only.md` — scope directive (β-corrigendum on COPm address landed)
- `project_abrigo_inequality_hedge_thesis.md` — product thesis (β-track Rev-3 spec needed to re-derive on Broker-native X_d)
- `feedback_pathological_halt_anti_fishing_checkpoint` — discipline applied to the 3-layer compound corrigendum
