---
name: USDT bridged Celo canonical address (vs scam impersonator)
description: Canonical USDT on Celo is `0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e` (Tether-deployed); `0x88eEC4…` previously cited is a Celoscan-flagged scam impersonator
type: project
originSessionId: phase0-vb-mvp / Rev-5.3 Task 11.N.2b.1
---

**Fact**: The legitimate bridged-USDT contract on Celo is `0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e` (Celoscan label "Tether: Gate on Celo", deployed by Tether: Deployer `0x1f9b97ecac47c16b14d4551c92572a3ee4e9380c` two years ago, transparent proxy → impl `0xBF83F843…8aEe07B98`, 467M+ transactions). The address `0x88eEC49252c8cbc039DCdB394c0c2BA2f1637EA0` that propagated through earlier Reality-Checker empirical lookups and into the Rev-5.3 plan as a flagged "RC empirical canonical" is a scam impersonator — Celoscan labels it `Suspicious_Token243` with "This token has been reported for impersonating well-known cryptocurrencies", deployed by Optics: Deployer 4+ years ago, holding only $46.65.

**Why**: the Rev-5.3 plan §1 had a HALT-VERIFY-MANDATORY 5-minute gate on USDT and WETH discrepancies precisely because two address candidates were in conflict. The Task 11.N.2b.1 gate memo resolved the discrepancy by Celoscan token-page inspection — the `0x48065fbb…83d5e` prefix in the COPM bot-attribution research §2.1 matches the legitimate Tether contract; the `0x88eEC4…` value carried by the plan's RC-empirical lookup was the impersonator. Without the HALT-VERIFY gate, the basket boundary would have been defined against a scam token and the X_d series would have been silently meaningless.

**How to apply**:
1. For any Celo basket-membership work: hard-code USDT = `0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e`.
2. Treat any `0x88eEC4…` USDT-named contract as scam; do not include in baskets, do not query.
3. Pattern: when an address discrepancy survives review, do Celoscan deployer-trace + impersonation-flag check before accepting either side. The plan's HALT-VERIFY-MANDATORY gate (5-min timeboxed) is the canonical containment.
4. Source: `contracts/.scratch/2026-04-25-carbon-basket-gate-decision-memo.md` §1 + §1.1.

## Related memory

- `project_mento_canonical_naming_2026.md` — companion address canonicality
- `project_carbon_defi_attribution_celo.md` — basket context
- `feedback_real_data_over_mocks.md` — the "verify real-world identity not assumption" discipline that fired here
