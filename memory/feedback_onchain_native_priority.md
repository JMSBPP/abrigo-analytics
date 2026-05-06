---
name: On-chain-native priority for Abrigo exercises
description: NON-NEGOTIABLE priority — structural-econometric exercises must leverage already-existing on-chain behavior (cCOP, COPM, Celo flows) as X before off-chain-dependent Y×X cells; tier-2 cells preserved as reserve, not abandoned
type: feedback
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
**Rule**: Every Abrigo structural-econometric exercise prioritizes **already-existing on-chain behavior** as the X data source. Off-chain-data-dependent Y×X cells (DANE surveys, CeFi exchange APIs, Bancolombia reports, non-tokenized series) remain valid future exercises but are LOWER priority than on-chain-native cells.

**Why**: (a) If an exercise using off-chain X proves an interesting relationship, the downstream product still requires INDUCING new on-chain behavior that mirrors the paper — a separate, heavier lift (behavior-design work). Starting with existing on-chain behavior means the product path is "measure what's already there, then hedge it." Starting with off-chain requires "prove the relationship, THEN induce behavior to make it investable." (b) Anti-fishing: forcing off-chain signals onto on-chain rails (as Phase-A.0 attempted with remittance) risks mis-representing what the data actually is. Honest on-chain exercises don't need a mirroring step.

**How to apply**:
1. **First-pass screening of any Y×X candidate**: is X directly observable on-chain from *existing user activity* (not new behavior we'd have to induce)? If yes → tier-1 priority. If no → tier-2 reserve.
2. **Existing on-chain behavior categories empirically established in Phase-A.0**:
   - TRM-arbitrage activity (on-chain↔off-chain FX convergence) — ~37% of peak-day cCOP flow
   - DeFi roundtripping / market-making — ~50%
   - Campaign/event spikes (airdrops, summits, UBI) — ~6%
   - Small retail tail — ≤7%
   - COPM mint/burn (Minteo commercial/treasury) — ~$1.2M/$1M over 585 days
3. **Macro-risk mapping**: for any on-chain behavior category, ask what macroeconomic phenomenon it LEGITIMATELY proxies — not what we wish it proxied.
4. **Retired approach**: do NOT attempt to reconstruct a macro aggregate by filtering out power-users and hoping the residual maps to a household observable (the Phase-A.0 remittance failure mode).
5. **Tier-2 reserve**: off-chain-data cells can be revisited AFTER a tier-1 on-chain-native exercise produces an honest verdict. At that point, the product-induce-behavior question becomes the scope of the tier-2 work (implementation proposal: "drive the behavior of people based on that paper" per user 2026-04-24).

**Anti-fishing corollary**: on-chain-native priority does NOT mean "force any on-chain signal into a macro story." It means: honestly characterize what on-chain behavior IS, then ask what macro risk that behavior legitimately represents. If the answer is "no macro — this is DeFi liquidity microstructure," the exercise is a microstructure exercise (not macro), and product framing must match.

## Related memory

- `project_phase_a0_exit_verdict.md` — Phase-A.0 remittance EXIT established this priority empirically
- `project_colombia_yx_matrix.md` — Y×X matrix; tier-1 vs tier-2 annotation to be added at next memory-update pass
- `project_ran_product_framing.md` — Abrigo permissionless-mainstream-user thesis aligns with on-chain-native mandate
