---
name: Phase-A.0 EXIT verdict — remittance exercise closed 2026-04-24
description: Phase-A.0 cCOP/COPM-on-chain-remittance-proxy → TRM-RV exercise CLOSED with EXIT_NON_REMITTANCE verdict; k1 intent + partial k2 data-source fired; Pivot-α (payment/consumption) in brainstorm
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
**Fact**: Phase-A.0 remittance-surprise exercise closed 2026-04-24 with verdict `EXIT_NON_REMITTANCE`. Task 11.F Axis-1 research found 0/30 peak-day remittance fingerprints (87%+ non-remittance: 37% TRM-arbitrage + 50% treasury/bot roundtripping + campaigns + events). Task 11.K kill criterion k1 (intent non-remittance dominant) fired; k2 (data-source) partial-fire from uncorroborated migration-date constant.

**Why**: the unfiltered cCOP/COPM aggregate from Dune #7366593 does not measure Colombian household remittance — it measures a mixture of TRM-arbitrage, treasury ops, bot roundtripping, campaigns, and a thin retail tail. No post-hoc filter can reconstruct what was never captured upstream. Prior research (`CELO_ECOSYSTEM_USERS.md:157`, `2026-04-02-ccop-qa-audit.md:73`, `2026-04-02-ccop-cop-usd-flow-response.md:74`) had documented this failure mode; the Rev-4 plan's "non-stop filter iteration" risked forcing a spurious relationship. The EXIT criterion was added in Rev-4.1 specifically to preempt that.

**How to apply**:
1. For anyone resuming this thread: read `contracts/.scratch/2026-04-24-phase-a0-exit-disposition.md` first. It enumerates kill-criteria evaluations, preserved artifacts, retired artifacts, and pivot candidates.
2. Rev-1, Rev-1.1, Rev-1.1.1 specs are all SUPERSEDED + RETIRED. Do not reference for methodology guidance.
3. Task 11.G/H/I/J as written in Rev-4.1 are retired under this EXIT.
4. Preserved infrastructure (reusable under any X-construction pivot that uses daily on-chain flow): `dune_onchain_flow_fetcher.py`, `weekly_onchain_flow_vector.py`, `cleaning.py` extensions, `surprise_constructor.py`, Phase-1.5.5 plan template.
5. Known data-provenance issue to fix before any reuse: `CCOP_COPM_MIGRATION_DATE = 2026-01-25` in the loader is uncorroborated (MGP-12 vote 2025-12-05; MGP-16 posted 2026-02-13); verify before pivot spec authoring.
6. Pivot direction approved by user 2026-04-24: brainstorm "payments mirroring consumption" niche. Leading candidate = Pivot-α (retail-payment surprise → TRM-RV with DANE EMCM retail-sales or ICCE as validation anchor). Alternatives documented in exit memo Section "Pivot direction".

**Anti-fishing lesson (carry to pivot)**: the EXIT criterion was NOT optional ceremony — it was load-bearing. Without Task 11.K, Rev-4's "non-stop filter iteration" policy would have run to argmax and produced a filter that appeared to "rescue" a remittance signal that never existed. Any pivot plan MUST inherit the kill-criterion pattern: define k1/k2/k3/k4-analogs BEFORE iterating, with git-hash-pinned pre-commitment.

## Related memory

- `project_phase_a0_remittance_execution_state.md` — historical execution state; to be marked CLOSED
- `project_colombia_yx_matrix.md` — remittance cell to be annotated CLOSED_NON_REPRESENTATIVE
- `project_fx_vol_cpi_notebook_complete.md` — precedent for honest-FAIL closure discipline (2026-04-19 CPI exercise)
- `project_fx_vol_econ_gate_verdict_and_product_read.md` — Abrigo product-read post-CPI-FAIL; same discipline applies under Phase-A.0 EXIT

## Reviewer artifacts consulted

- `contracts/.scratch/2026-04-24-ccop-peak-day-event-research.md` — Task 11.F Axis-1 findings (0/30 remittance fingerprints)
- `contracts/.scratch/2026-04-24-tier1e-rev111-review-code-reviewer.md` — CR REJECT on Rev-1.1.1 spec
- `contracts/.scratch/2026-04-24-tier1e-rev111-review-reality-checker.md` — RC NEEDS WORK (MDES arithmetic error)
- `contracts/.scratch/2026-04-24-tier1e-rev111-review-technical-writer.md` — TW NEEDS FIXES
- `contracts/.scratch/2026-04-24-plan-rev4-review-code-reviewer.md` — plan CR ACCEPT-WITH-FIXES
- `contracts/.scratch/2026-04-24-plan-rev4-review-reality-checker.md` — plan RC NEEDS WORK (M mis-bounded, N-overstated, FWER unaddressed)
- `contracts/.scratch/2026-04-24-plan-rev4-review-senior-pm.md` — plan PM ACCEPT-WITH-FIXES
