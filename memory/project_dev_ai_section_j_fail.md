---
name: dev-AI Stage-1 simple-β FAIL verdict (Section J narrow ICT) 2026-05-06
description: Section J × COP/USD-lag tested NEGATIVE β=-0.146 sign-flip; R2 Section M β=+0.455 p=1.13e-06 candidate-next-iteration; spec §9.16 flagged-not-resolved; spec v1.0.3 reconciliation flag
type: project
originSessionId: d1cfac41-85eb-4cae-ae40-bddd97fffc23
---
**Fact**: dev-AI Stage-1 simple-β iteration (Y_p = Colombian young-worker 14-28 employment share in CIIU Rev. 4 Section J ICT × X = COP/USD lagged 6/9/12 months) closed FAIL on 2026-05-06.

- Primary OLS: β_composite = **-0.14613** (HAC L=12 SE 0.0847, t=-1.726, p_one=0.958, sign-flipped from positive expectation)
- §7.1 R-row classification: MIXED (n_agree=3/4)
- §3.5 SUBSTRATE_TOO_NOISY: False (only R2 sign-flipped)
- §6 v1.0.2 κ-tightened pair (R1+R3 BOTH AGREE): clears at NEGATIVE sign — consistent FAIL routing per §8.1 step 4(d)
- §3.4 escalation suite (pre-authorized per §9.6): D-i + D-ii FAIL (β not > 0); D-iii literally passes (β=+0.113, p=0.012) BUT inadmissible per spec §5.5 strict reading (§3.3 trigger never fired)
- User pick **Option C** 2026-05-06: FAIL per strict §5.5 + D-iii preservation as Phase-3 finding for future Section M iteration; spec v1.0.3 reconciliation flag

**MOST LOAD-BEARING FINDING**: R2 Section M sensitivity arm produced β = **+0.45482801** at t=+4.73, p=1.13e-06. This empirically RESOLVES the spec §9.16 compositional-accounting ambiguity:

> Pair D's broad-services Section G-T β=+0.137 was NOT a re-discovery of Section J ICT signal. Section J carries OPPOSITE-sign signal; Pair D's PASS came from Section M-style subsectors (consultants / legal / accounting / scientific R&D / admin services).

Per spec §9.16(c), formal resolution requires (G-T minus J) decomposition; R2 Section M comparator is *consistent with* but not *equivalent to* the spec-authorized decomposition → flagged-not-resolved (R5 robustness arm DEFERRED for future iteration).

**Empalme residual bias surfaced**: NB02 Trio 1 boundary_anomaly TRUE (Y_p_logit[2021-01]−Y_p_logit[2020-12] = +0.375 > 3× envelope 0.335); β_regime_R1 = +0.188 (t=+4.36) post-2021 era unexplained level shift. DANE Marco-2018 empalme correction did NOT fully neutralize methodology break.

**Spec v1.0.3 reconciliation flag (deferred)**: spec §5.5 line 252 ("escalation suite run if and only if §3.3 ESCALATE-trigger fires") and spec §9.6 (per Trio 6 dispatch reading "ran whether or not mean-OLS passed") are CONTRADICTORY on the EXECUTION question. Future Pair-D-style iterations should resolve unambiguously before §5.5 invocation.

**Phase 2.5 EA framework application** (option_iii manual): Austrian + Neoclassical Synthesis natively predict the realized sign-flip ex-post (NOT pre-registered; flagged as ex-post interpretive frame, not predictive). 5 of 6 schools read R2 Section M positive β as real Section-M-specific transmission, not noise.

**Per-user a_s implication**: Stage-1 hypothesis empirically REJECTED for dev-AI-paying population (Colombian young-worker Section J narrow ICT). Per CORRECTIONS-θ FIAT rails confirmed (most LATAM developers pay AI APIs via FIAT not crypto — on-chain a_s observability never available). Per-user a_s instrument cannot be designed against rejected transmission (would be SHORT-FX, opposite of what dev-AI-paying population needs given USD-denominated AI tooling costs).

**Why**: This iteration is a high-information FAIL — sign-flipped from pre-registered positive expectation, NOT just insignificant. The R2 Section M positive resolves the §9.16 compositional ambiguity for Pair D's PASS interpretation. Future iterations on Colombian sectoral employment-share × FX-lag panel must account for sector-specific import/export elasticity asymmetry (Section J net-contractionary; Section M net-expansionary under COP devaluation).

**How to apply**:
- Do NOT propose Section J narrow ICT × COP/USD again without new information-bearing argument (transmission rejected at Stage-1)
- Section M (Y_s2 = professional/scientific/technical/admin Sections {69-75}) opens a candidate-next-iteration if framework targets align with broader knowledge-worker scope
- For any Pair-D-style structural-econometric iteration on DANE GEIH, account for empalme residual bias (β_regime should be informational diagnostic, NOT primary-spec rescue lever)
- Spec §5.5/§9.6 reconciliation is deferred but should be addressed before another Pair-D-style §5.5 invocation (otherwise the same spec-internal contradiction recurs)

**Iteration tree (post-migration)**: `contracts/notebooks/dev_ai_cost/` (canonical fx_vol pattern):
- `01_data_eda.ipynb / 02_estimation.ipynb / 03_tests_and_sensitivity.ipynb` (15+16+22 cells)
- `data/` panel_combined.parquet sha `451f4c61…740d` + Y_p Section J + Y_s2 Section M + X COP/USD lag + DATA_PROVENANCE
- `estimates/` PRIMARY_RESULTS.md / ROBUSTNESS_RESULTS.md / ESCALATION_RESULTS.md / gate_verdict.json / EA_FRAMEWORK_APPLICATION.md / MEMO.md
- `dispositions/` Task 1.1 FLAG-A/B (Option A) + 3-way review D-iii (Option C) memos
- `README.md` canonical fx_vol pattern
- Spec v1.0.2 decision_hash `7c72292516…f5a` at commit `c4e0032a0`
- Plan v1.1.1 sha `772b52e1f…c036` at commit `354841f3f`
- Phase 2 close commit `6354fc82b`; Migration commit `8e525c988`; PR #86 https://github.com/wvs-finance/ThetaSwap-core/pull/86

**Cross-iteration framing for Pair D**: Pair D's PASS β=+0.137 (project memory `project_pair_d_phase2_pass`) preserved verbatim. Compositional interpretation now sharpened: Pair D was a Section M-style transmission averaged over G–T, NOT a Section J ICT-narrow signal.

**Cross-iteration framing vs Colombia Y×X matrix memory** (`project_colombia_yx_matrix.md`, 2026-04-20): the matrix memory predates Pair D + dev-AI iterations and tested a different axis (Y₁ TRM-RV / Y₂ CPI-var / Y₃ Remittance-var × X on-chain Mento observables). The Pair D + dev-AI iterations explored a SEPARATE axis (Colombian sectoral employment shares × COP/USD-lag) which is NOT in the 2026-04-20 matrix; both axes remain in scope for future framework iterations.
