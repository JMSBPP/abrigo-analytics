---
name: DuckDB onchain_xd_weekly state post-Rev-5.3.1
description: onchain_xd_weekly has 10 proxy_kind values × ~80 weeks = 819 rows; primary X_d = carbon_basket_user_volume_usd (82 weeks, 77 non-zero) plus 9 diagnostics
type: project
originSessionId: phase0-vb-mvp / Rev-5.3.1 post-Task 11.N.2c
---

**Fact**: As of commit `7afcd2ad6` (Rev-5.3.1, 2026-04-25), the DuckDB table `onchain_xd_weekly` at `contracts/data/structural_econ.duckdb` (~42MB) contains 10 distinct `proxy_kind` values across ~80 Friday-anchored weeks = ~819 rows total. Three are primary X_d candidates and seven are diagnostics:

| proxy_kind | weeks | role |
|---|---:|---|
| `net_primary_issuance_usd` | 84 | supply-channel primary candidate |
| `b2b_to_b2c_net_flow_usd` | 79 | distribution-channel primary candidate |
| `carbon_basket_user_volume_usd` | 82 (77 non-zero) | post-Rev-5.3.1 committed primary |
| `carbon_basket_arb_volume_usd` | 82 | Arb-Fast-Lane diagnostic |
| 6 × `carbon_per_currency_<TICKER>_volume_usd` | 82 each | per-currency diagnostics (legacy slugs cUSD/cEUR/cREAL/cKES/COPM/XOFm preserved) |

**Why**: the table accumulated incrementally across Rev-5.1 (supply-channel + distribution-channel for inequality-differential pivot), Rev-5.2.1 (COPM raw-transfers backfill), and Rev-5.3 (Carbon basket-rebalancing ingestion for X_d). Each `proxy_kind` is additive — none invalidates another — and downstream Task 11.O resolution-matrix authoring will select primary X_d from the three candidates with the diagnostic seven available for cross-validation. The 77/82 non-zero ratio for the committed primary is what triggered the Rev-5.3.1 N_MIN relaxation.

**How to apply**:
1. Reload via `econ_query_api.load_onchain_xd_weekly(proxy_kind="<key>")`; pass `proxy_kind=None` to get all channels in one DataFrame.
2. Schema: composite primary key `(week_start, proxy_kind)`; columns `week_start, value_usd, is_partial_week, proxy_kind`. Schema migration commit `a724252c6` (Rev-5.2.1 Step 0); CHECK constraint enumerates all 10 valid `proxy_kind` strings (see `econ_schema.py` line 503+).
3. The 6 per-currency diagnostic slugs use legacy pre-rebrand names (cUSD/cEUR/cREAL/cKES) — see `project_mento_canonical_naming_2026.md` for the new-name mapping. Do NOT mass-rename the slugs; document in loader docstring.
4. Provenance: Carbon ingestion is byte-exact against Dune query `7372282` execution `01KQ1ZZGYYMFKADNZDB8Z4ECDY` (`contracts/data/carbon_celo/README.md`).
5. Friday-anchored America/Bogotá weekly cadence; `is_partial_week` flag true for any week where the underlying ingestion source was incomplete at extraction time.

## Related memory

- `project_carbon_defi_attribution_celo.md` — protocol identity behind the Carbon X_d
- `project_carbon_user_arb_partition_rule.md` — partition rule between user and arb proxy_kinds
- `project_y3_inequality_differential_design.md` — Y₃ panel that joins to this X_d
- `project_phase15_5_task_chain_post_rev531.md` — task chain that produced this state
- `project_rev51_resume_state.md` — historical predecessor state (Rev-5.1, 11.M.5 cut-off)
