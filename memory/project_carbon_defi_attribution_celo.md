---
name: Carbon DeFi protocol attribution on Celo — Rev-5.3.6/5.3.7 β-corrigendum (V2 successor + no Mento-protocol-integration)
description: CarbonController + BancorArbitrage V1 + **BancorArbitrageV2** addresses on Celo; **β-corrigendum 2026-04-27**: V1 dead 2025-07-01; V2 successor at 0x20216f30...; Mento V3 manifest confirms NO protocol-level Carbon-Mento integration; Carbon-basket X_d thesis fundamentally re-interpreted as third-party-DEX activity not Mento-native demand
type: project
originSessionId: phase0-vb-mvp / Rev-5.3 Task 11.N.2; β-corrigendum 2026-04-27
---

## β-CORRIGENDUM (2026-04-27, Rev-5.3.6 + Rev-5.3.7)

The original memo's claim that the Carbon-basket flows "feed the Carbon-basket X_d thesis" as a Mento-basket two-sided market is **fundamentally re-interpreted** under empirical evidence collected 2026-04-27:

**Layer 1 (Rev-5.3.6) — V2 successor not in attribution roster.**
- BancorArbitrage V1 `0x8c05ea30…` died 2025-07-01 12:45:27 UTC (last event).
- **BancorArbitrageV2 `0x20216f3056bf98e245562940e6c9c65ad9b31271`** took over 2025-07-02 01:17:32 UTC. Decoded as `carbon_defi_multichain.bancorarbitragev2_*` (38 decoded tables).
- V2 alone accounts for 524,104 events post-2025-07-01 (78% of post-July 'user'-partition events under the V1-only partition rule).
- Add V2 to the attribution roster as Bancor's V1-successor arb router.

**Layer 2 (Rev-5.3.7) — No Mento-protocol-level integration.**
- Mento V3 deployment manifest at `https://docs.mento.org/mento-v3/build/deployments/addresses.md` (independently fetched 2026-04-27) lists the complete Celo mainnet contract set: Reserve, Broker (V2), BiPoolManager (V2), Router (V3), FPMMFactory (V3), ReserveV2 (V3), 12 StableTokens, breakers, oracles, governance, MENTO/veMENTO. **ZERO references to Carbon DeFi or BancorArbitrage anywhere.**
- Mento is a closed Reserve+Broker+Pools system. Carbon DeFi can host Mento basket tokens as standard ERC-20s (no permission required), but Mento Reserve never mints/burns in response to a Carbon trade.
- The "Carbon-basket two-sided MM" framing is **wrong-signal**: Carbon-Mento volume is third-party-DEX arbitrage activity (mostly Bancor's own V1+V2 routers), NOT Mento Reserve user demand.
- The actual Mento user-demand signal lives at:
  - Broker V2 `0x777A8255cA72412f0d706dc03C9D1987306B4CaD` (`mento_celo.broker_evt_swap`; 6.16M lifetime events; **383,303 distinct traders** — 2,604× Carbon's 147)
  - Router V3 `0x4861840C2EfB2b98312B0aE34d86fD73E8f9B6f6` + FPMM pools
  - StableToken `Transfer` events filtered to mint/burn (from=0x0 / to=0x0)

**Authoritative going forward (post-β-corrigendum):**
- Carbon-basket X_d thesis is CLOSED OUT as scope-mismatched. NB-α terminates at sub-task 12 (HEAD `2b46ef0f6`); sub-tasks 13-31 NOT authored.
- β-track Rev-3 spec (Task 11.P.spec-β; deferred) pivots X_d to Mento-Broker-native.
- This memory's "Why" + "How to apply" sections referencing Carbon-basket X_d as a Mento-native demand signal are SUPERSEDED.

**Updated address roster:**
- `0x6619871118D144c1c28eC3b23036FC1f0829ed3a` = **CarbonController** (third-party DEX; not Mento-integrated; emits `tokenstraded`)
- `0x8c05ea305235a67c7095a32ad4a2ee2688ade636` = **BancorArbitrage V1** (DEAD since 2025-07-01)
- `0x20216f3056bf98e245562940e6c9c65ad9b31271` = **BancorArbitrageV2** (V1 successor, live since 2025-07-02; not in original memo)

**Audit trail:**
- Rev-5.3.6 disposition: `scratch/2026-04-27-x-d-partition-rule-staleness-disposition-beta.md`
- Rev-5.3.7 disposition (Option A pivot): `scratch/2026-04-27-x-d-strategic-re-evaluation-disposition.md`
- Dune queries: 7382618, 7382632, 7382639, 7382645, 7382647, 7382711
- Mento V3 deployment manifest: https://docs.mento.org/mento-v3/build/deployments/addresses.md

---

## Original content (pre-β-corrigendum, preserved for audit trail)


**Fact**: The two addresses dominating the COPM Transfer log on Celo are official Bancor Carbon DeFi protocol contracts, not opportunistic bots:
- `0x6619871118D144c1c28eC3b23036FC1f0829ed3a` = CarbonController (Carbon DeFi DEX strategy registry; verified on Carbon DeFi mainnet-contracts docs page; Dune decodes 52 tables under `carbon_defi_celo.carboncontroller_*`).
- `0x8c05ea305235a67c7095a32ad4a2ee2688ade636` = BancorArbitrage / Arb Fast Lane (the on-chain arbitrage executor; verified by Dune namespace `carbon_defi_celo.bancorarbitrage_evt_arbitrageexecuted`).

**Why**: prior to Task 11.N.2 (2026-04-24), these addresses had been classified as "bots/MEV" and were proposed as filter-out targets in Phase-A.0 remittance work. The attribution research reframed them as the official Bancor Carbon DeFi protocol's MM contracts, making their flows interpretable as a closed-loop two-sided market across the Mento working-class-stablecoin basket {COPM, USDm, EURm, BRLm, KESm, XOFm} ↔ global-asset basket {CELO, USDT, USDC, WETH}. This reframing unlocked the Carbon-basket X_d thesis (Rev-5.3 plan section). BancorArbitrage was `trader` on 57,382 COPM trades (~52% of all COPM Transfer events). Funding source includes Credit Collective's $1M USDC/COPM allocation per the March 2025 Celo forum governance update.

**How to apply**: When constructing on-chain X for any Mento-basket exercise, treat these two addresses as PROTOCOL contracts (not random bots). Specifically:
1. The "user-vs-arb" partition for Carbon flows must use the `trader` field on `carboncontroller_evt_tokenstraded` rows (see corrigendum memo for canonical partition rule).
2. The protocol's hour-of-day signature (UTC 13–17 peak, ~1.9× peak/trough ratio, continuous diurnal) is consistent with North-American working-hours automation, not Colombian retail.
3. Dune query IDs for reproducing attribution: `7371006`, `7371007`, `7371008`, `7371009`, `7371019`, `7371020`, `7371021`.
4. Full attribution research: `scratch/2026-04-24-copm-bot-attribution-research.md` (Task 11.N.2).

## Related memory

- `project_carbon_user_arb_partition_rule.md` — canonical partition rule via `trader` field
- `project_mento_canonical_naming_2026.md` — cUSD/cEUR/cREAL/cKES → USDm/EURm/BRLm/KESm rebrand
- `project_phase_a0_exit_verdict.md` — predecessor Phase-A.0 EXIT that motivated the Carbon-basket pivot
- `project_abrigo_inequality_hedge_thesis.md` — product thesis the Carbon-basket X_d feeds
