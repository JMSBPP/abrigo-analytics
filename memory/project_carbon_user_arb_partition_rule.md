---
name: Carbon TokensTraded user-vs-arb partition rule — Rev-5.3.6 β-corrigendum (V1-only; broken post-2025-07-01)
description: Canonical V1 partition rule (trader = 0x8c05ea30) on Carbon TokensTraded events; **β-corrigendum 2026-04-27**: rule is V1-only and silently fails post-2025-07-01 when BancorArbitrageV2 successor 0x20216f30 took over. 78% post-July-2025 contamination of 'user' partition documented.
type: project
originSessionId: phase0-vb-mvp / Rev-5.3 Task 11.N.2b.2; β-corrigendum 2026-04-27 mid-NB-α sub-task 12
---

## β-CORRIGENDUM (2026-04-27, Rev-5.3.6 + Rev-5.3.7 X_d strategic re-evaluation)

The original memo's claim that "the `trader`-field rule survives the staleness of the `bancorarbitrage_evt_arbitrageexecuted` table (which stops at 2025-07-01)" is **technically true at the partition-rule-mechanics level** (no JOIN; rule remains computable) but **FALSE at the analytical-correctness level**: post-2025-07-01, BancorArbitrage V1 (`0x8c05ea30…`) is dead, but a SUCCESSOR contract took over.

**Empirical V1→V2 transition:**
- V1 last event: 2025-07-01 12:45:27 UTC.
- V2 first event: 2025-07-02 01:17:32 UTC. Gap: 12h31m.
- V2 address: `0x20216f3056bf98e245562940e6c9c65ad9b31271` (BancorArbitrageV2).
- V2 decoded on Dune as `carbon_defi_multichain.bancorarbitragev2_*` (38 decoded tables).

**Empirical contamination (Dune query 7382632, 0.026 credits):**
- Pre-2025-07-01 'arb' partition: 929,614 events from 1 trader (V1). ✅ correct.
- Pre-2025-07-01 'user' partition: 368,389 events from 68 traders. ✅ correct.
- **Post-2025-07-01 'user' partition: 669,872 events from 80 traders. 524,104 (78.2%) are V2 misclassified as user.**
- Post-2025-07-01 'arb' partition: 0 events (V1 dead).

**Authoritative going forward (under Rev-5.3.6):**
The single-address V1-only partition rule **MUST be replaced** by a multi-version rule covering V1 + V2 + future successor arb routers:
```
partition = CASE
    WHEN trader IN (
        0x8c05ea305235a67c7095a32ad4a2ee2688ade636,  -- BancorArbitrage V1 (dead 2025-07-01)
        0x20216f3056bf98e245562940e6c9c65ad9b31271   -- BancorArbitrageV2 (live 2025-07-02 → present)
    ) THEN 'arb'
    ELSE 'user'
END
```

**Future-research safeguard**: any contract decoded by Dune as `*ArbitrageExecuted` event-emitter MUST be added to the partition whitelist before X_d ingestion. Triangulation procedure: `searchTablesByContractAddress` → check `contract_name` for `*Arbitrage*` patterns; cross-check `bancorarbitrage*_evt_arbitrageexecuted` table-name proliferation under `carbon_defi_multichain`.

## Compound scope-mismatch under Rev-5.3.7 (no Mento-protocol-integration finding)

Even with the partition rule fixed, the Carbon `tokenstraded` signal is NOT Mento-native user demand — Mento V3 deployment manifest (https://docs.mento.org/mento-v3/build/deployments/addresses.md) confirms zero protocol-level integration with Carbon DeFi. Carbon hosts Mento basket tokens as standard ERC-20s; the volume signal is third-party DEX activity, mostly Bancor's own arb routers (V1+V2). The actual Mento user-demand signal lives at:
- Mento Broker V2 `0x777A8255cA72412f0d706dc03C9D1987306B4CaD` (Swap events; 6.16M lifetime, 383K distinct traders)
- Mento V3 Router `0x4861840C2EfB2b98312B0aE34d86fD73E8f9B6f6` + FPMM pools
- StableToken `Transfer` events filtered to mint (from=0x0) / burn (to=0x0)

NB-α terminates at sub-task 12 (HEAD `2b46ef0f6`); β-track Rev-3 spec (Task 11.P.spec-β) pivots X_d to Mento Broker.

**Audit trail:**
- Rev-5.3.6 disposition: `contracts/.scratch/2026-04-27-x-d-partition-rule-staleness-disposition-beta.md`
- Rev-5.3.7 disposition: `contracts/.scratch/2026-04-27-x-d-strategic-re-evaluation-disposition.md`
- Dune queries: 7382618, 7382632, 7382639, 7382645, 7382647, 7382711

---

## Original content (pre-β-corrigendum, preserved for audit trail)


**Fact**: For partitioning Carbon DeFi `carboncontroller_evt_tokenstraded` rows into user-initiated vs Arb-Fast-Lane-routed activity, the canonical rule is the `trader` field on the row itself: `trader = 0x8c05ea305235a67c7095a32ad4a2ee2688ade636` ⇒ arb-routed; `trader ≠ <arb>` ⇒ user-initiated. This is NOT `evt_tx_from` (the EOA relay; uniformly distinct from the BancorArbitrage contract address) and NOT a tx-hash JOIN against `bancorarbitrage_evt_arbitrageexecuted` (which is empirically equivalent on the overlap window but unnecessary).

**Why**: a Dune 2×2 contingency probe (query `7372247`, cost 0.094 credits) on all 175,005 boundary-crossing TokensTraded events (2024-09-01 → 2026-04-25) found the partition perfectly diagonal: 51,494 events have BOTH `trader = arb` AND `tx ∈ arb_events_table`; 123,511 events have NEITHER; both off-diagonal cells are exactly zero; `trader_null_count = 0`. The two partitions are mathematically equivalent on the population, but the `trader`-field rule is simpler, requires no JOIN, and survives the staleness of the `bancorarbitrage_evt_arbitrageexecuted` table (which stops at 2025-07-01 — 10 months stale relative to the TokensTraded table that runs through 2026-04-25). Naive use of `evt_tx_from ≠ arb` (the original Rev-5.3 plan §982 X_d formula) produced all-zero `carbon_basket_arb_volume_usd` rows because the EOA relay is universally distinct from the contract address.

**How to apply**:
1. Aggregate user volume per week as `Σ |source_amount_usd| WHERE trader != 0x8c05ea305235a67c7095a32ad4a2ee2688ade636` (basket-boundary filter applied separately).
2. Aggregate arb volume per week as `Σ |source_amount_usd| WHERE trader = 0x8c05ea305235a67c7095a32ad4a2ee2688ade636`.
3. Empirical 17%/83% split by USD volume (29%/71% by event count) on the 175,005-event basket-boundary panel — arb is a real but minority share.
4. Source corrigendum: `contracts/.scratch/2026-04-25-carbon-basket-gate-memo-corrigendum.md` (supersedes §3.3 of `2026-04-25-carbon-basket-gate-decision-memo.md`).
5. Plan task that fired this rule: 11.N.2b.2 Step 0 resume directive at `contracts/docs/superpowers/plans/2026-04-20-remittance-surprise-implementation.md`.

## Related memory

- `project_carbon_defi_attribution_celo.md` — protocol identity behind the arb address
- `project_concurrent_agent_filesystem_interleaving.md` — operational caveat from the parallel ingestion that exposed the original `evt_tx_from` bug
