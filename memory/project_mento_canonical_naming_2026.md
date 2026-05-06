---
name: Mento 2026 canonical stablecoin naming (rebrand) — Rev-5.3.5 β-corrigendum on COPM address
description: cUSD/cEUR/cREAL/cKES → USDm/EURm/BRLm/KESm canonical 2026 names; XOFm unchanged; COPm canonical address corrected from 0xc92e8fc2 (Minteo, out of scope) to 0x8A567e2a (Mento V2 StableTokenCOP) per Rev-5.3.5 HALT-VERIFY β resolution
type: project
originSessionId: phase0-vb-mvp / Rev-5.3 Task 11.N.2b.1; β-corrigendum 2026-04-26
---

## β-CORRIGENDUM (2026-04-26, Rev-5.3.5 HALT-VERIFY resolution)

The original "COPM (Minteo, unchanged) — `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606`" line below is **WRONG on the Mento-native scope claim**. Empirical disambiguation (Dune `searchTablesByContractAddress` + activity probe + Mento V3 deployments docs + Celo Token List, all triangulated under MR-β.1 sub-task 1):

- `0x8A567e2aE79CA692Bd748aB832081C45de4041eA` — **canonical Mento V2 `StableTokenCOP`** ("celocolombianpeso" project on Dune; 285,390 transfers; 78 weeks of activity 2024-10-31 → 2026-04-26 live; Mento `evt_exchangeupdated` + `evt_validatorsupdated` events present, dispositive of Mento-protocol-native status). Ticker: **COPm** (lowercase-m, per Celo Token List entry "Mento Colombian Peso").
- `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606` — **Minteo-fintech token** ("COP Minteo" per Celo Token List). 110,253 transfers ingested in `onchain_copm_transfers` for Rev-2. **Out of Mento-native scope** per `project_abrigo_mento_native_only`. Ticker: **COPM-Minteo** (uppercase-M for disambiguation; cite as "COPM-Minteo" or "Minteo-COPM" wherever ambiguity could arise).

The address-level identity claim of the original memo ("address-level identity preserved") **fails for COP** — there are two distinct COP-named tokens on Celo, only one of which is Mento-protocol-native. The other five Mento-native tickers (USDm/EURm/BRLm/KESm + XOFm) are unaffected by this corrigendum; their addresses remain authoritative as listed below.

**Authoritative going forward:**
- COPm (lowercase) at `0x8A567e2aE79CA692Bd748aB832081C45de4041eA` is the in-scope Mento-native Colombian peso.
- COPM-Minteo at `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606` is out of Mento-native scope.

**Audit trail:**
- HALT-VERIFY disposition memo: `scratch/2026-04-26-mr-beta-1-1-halt-resolution-beta.md`
- DE inventory: `scratch/2026-04-25-mento-native-address-inventory.md`
- RC spot-check: `scratch/2026-04-25-subtask-mr-beta-1-1-rc-spot-check.md`
- Rev-5.3.5 CORRECTIONS block in major plan
- Dune project: `celocolombianpeso_celo.stabletokenv2_*` (24 decoded tables)

---

## Original content (pre-β-corrigendum, preserved for audit trail)

**Fact**: As of the 2026 Mento rebrand, the canonical stablecoin tickers are:
- USDm (was cUSD) — `0x765de816845861e75a25fca122bb6898b8b1282a`
- EURm (was cEUR) — `0xd8763cba276a3738e6de85b4b3bf5fded6d6ca73`
- BRLm (was cREAL) — `0xe8537a3d056da446677b9e9d6c5db704eaab4787`
- KESm (was cKES) — `0x456a3D042C0DbD3db53D5489e98dFb038553B0d0`
- COPM (Minteo, unchanged) — `0xc92e8fc2947e32f2b574cca9f2f12097a71d5606`  ⚠️ SUPERSEDED by β-corrigendum above; this address is Minteo-fintech, NOT Mento-native. The Mento-native COPm address is `0x8A567e2aE79CA692Bd748aB832081C45de4041eA`.
- XOFm (was eXOF, unchanged tail) — `0x73F93dcc49cB8A239e2032663e9475dd5ef29A08`

**Why**: legacy code, plans, and reports authored before 2026-04-24 (including the Phase-A.0 remittance plan and the COPM bot-attribution research §2.1 token table) use cUSD/cEUR/cREAL/cKES exclusively. New code, design docs (`2026-04-24-carbon-basket-xd-design.md`), and external-facing memos must use USDm/EURm/BRLm/KESm. Cross-references between old and new terminology are required when retiring legacy artefacts. Address-level identity is unchanged — only the human-readable ticker rebranded — so on-chain partition rules and Celoscan token lists key off the address.

**How to apply**:
1. When authoring new specs/plans/notebooks: USDm/EURm/BRLm/KESm.
2. When reading legacy 2026-04-23 and earlier artefacts: translate cUSD↔USDm, cEUR↔EURm, cREAL↔BRLm, cKES↔KESm; trust the address as the canonical identity.
3. The `proxy_kind` slug naming in `onchain_xd_weekly` table follows `carbon_per_currency_<LEGACY_TICKER>_volume_usd` (slugged off the design doc revision pre-rebrand-discovery) — do not mass-rename to avoid migration disruption; document the legacy slug in the loader docstring.
4. Address-verification provenance: `scratch/2026-04-25-carbon-basket-gate-decision-memo.md` §1.

## Related memory

- `project_carbon_defi_attribution_celo.md` — context where this rebrand surfaced
- `project_usdt_celo_canonical_address.md` — companion address-canonicality note for bridged USDT
