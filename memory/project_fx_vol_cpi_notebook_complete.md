---
name: FX vol on CPI surprise Colombia notebook pipeline COMPLETE
description: Scientific verdict FAIL (β̂_CPI = −0.000685 insignificant); 3 notebooks + 4 artifacts shipped; 33 tasks / 4 phases closed 2026-04-19; anti-fishing discipline held; A1 monthly + A4 release-excluded positive-significant preserved as pivot candidates, not rescue claims
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
# FX-vol-on-CPI-surprise — Colombia 2008-2026 — COMPLETE

**Closed:** 2026-04-19
**Branch:** `phase0-vb-mvp` on origin `dev` (JMSBPP)
**Total commits:** ~130 across 33 tasks / 4 phases
**Test baseline at close:** 768 passed + 7 skipped

## Scientific verdict

**`gate_verdict.json.gate_verdict = "FAIL"`**

```json
{
  "t1_verdict": "FAIL",
  "t2_verdict": "FAIL",
  "t3a_verdict": "FAIL TO REJECT",
  "t3b_verdict": "FAIL",
  "t4_verdict": "FAIL",
  "t5_verdict": "FAIL",
  "t6_verdict": "FAIL",
  "t7_verdict": "PASS",
  "material_movers_count": 0,
  "reconciliation": "AGREE",
  "bootstrap_hac_agreement": "AGREEMENT",
  "pkl_degraded": false,
  "gate_verdict": "FAIL"
}
```

**Primary OLS Column 6:**
- β̂_CPI = −0.000685 (HAC(4) Newey-West SE = 0.001794)
- 90% HAC CI [−0.003636, +0.002266] (contains zero)
- T3b stat = β̂ − 1.28·SE = −0.002981 < 0 → FAIL
- adj-R² = 0.193 (passes 0.15 floor; macro-surprise regressors alone ≈ 0)
- n = 947 weekly observations, 2008-01-02 to 2026-02-23

The research question under pre-committed Rev 4 weekly OLS specification is answered: **Colombian CPI AR(1) surprises do NOT cause a statistically detectable increase in COP/USD realized volatility, 2008-2026.**

## Four canonical artifacts

| path | purpose | size |
|---|---|---|
| `notebooks/fx_vol_cpi_surprise/Colombia/01_data_eda.ipynb` | NB1 data EDA + 12 locked Decisions + ledger emission | 118 cells, ~3 MB rendered |
| `notebooks/fx_vol_cpi_surprise/Colombia/02_estimation.ipynb` | NB2 OLS ladder + diagnostics + Student-t + GARCH-X + CPI/PPI + subsample + T3b + reconciliation + serialization | 45 cells |
| `notebooks/fx_vol_cpi_surprise/Colombia/03_tests_and_sensitivity.ipynb` | NB3 T1-T7 tests + 13-row forest plot (A1-A12 + S1-S7) + §9 anti-fishing halt + §10 gate aggregation + §11 README auto-render | 34 cells |
| `notebooks/fx_vol_cpi_surprise/Colombia/estimates/gate_verdict.json` | machine-readable final verdict, 358 B sorted-keys | 358 B |

Supporting artifacts:
- `estimates/nb1_panel_fingerprint.json` (6.7 KB) — 12 decision cards + weekly+daily panel sha256 + sensitivity_preregistration_hash
- `estimates/nb2_params_point.json` (247 KB) — all fitted params + covariances + subsamples
- `estimates/nb2_params_full.pkl` (1.5 MB) — full statsmodels fit objects
- `notebooks/fx_vol_cpi_surprise/Colombia/README.md` (3.5 KB) — Jinja2 auto-rendered, byte-identical-CI-checked
- `notebooks/fx_vol_cpi_surprise/Colombia/figures/forest_plot.png` (93 KB) — 14-row pre-registered sensitivity forest

## Phase summary (33 tasks / 4 phases)

| phase | tasks | completion commit |
|---|---|---|
| 0 Infrastructure | 1a-6 | `4d4818ea1` |
| 1 NB1 Data EDA + 12 Decisions + 3-way review | 7-15 | Task 15 remediation `1aff490f4` |
| 2 NB2 Estimation + T3b FAIL + 3-way review | 16-23 | Task 23 + hotfix `12170a803` |
| 3 NB3 Sensitivity + forest + gate_verdict.json + 3-way review | 24-31 | Task 31 remediation `479ebf609` |
| 4 Integration + documentation close | 32-33 | Task 32 `4391142ee` + Task 33 (this commit) |

## Three-way review gates — all PASSED

| gate | verdict | critical fixes landed |
|---|---|---|
| Task 15 NB1 review | PASS | S7 propagation, real commit SHAs in ledger, schema_version, sensitivity_preregistration_hash, verified Colombian citations (Anzoátegui 2019, Galvis 2017), cell 92 hardcoded-path fix |
| Task 23 NB2 review | PASS | E1 atomic-emit date coercion, E2 directional-concordance reconcile, E3 Andrews 1999 boundary CI caveat, E4 scipy version, E5-E8 PDF readability, E9-E10 LaTeX hat normalization |
| Task 31 NB3 review | PASS | R1 A1 Decision #1 window compliance, R2 §10 live-exec test, R3 prose/JSON schema sync, R4 forest-title single-source, C1 PDF pending markers, C2 anti-fishing visibility in README |

## What's live, what's dead, what's pivot

**Primary scientific story DEAD.**
- Weekly OLS on signed CPI surprise → FAIL
- Daily GARCH-X on |CPI surprise| → FAIL (δ̂ = 0 boundary)
- CPI/PPI decomposition → both null

**Anti-fishing discipline VINDICATED.**
- 3 co-primaries all null; no rescue permitted
- §9 halt on T3b FAIL; zero spotlight tables
- Pre-commitment binding held through 33 tasks

**Pivot candidates LIVE (pre-registered, not rescue):**
- **A1 monthly cadence** (n=220 after R1 fix): β̂ = +0.0152, 90% CI [+0.0057, +0.0246] — sign opposite to primary, positive-significant; weekly aggregation may drown the real signal
- **A4 release-day-excluded**: β̂ = +0.0033, 90% CI [+0.0005, +0.0062] — effect in non-release-day vol dynamics; suggests anticipation/lagged response
- **Intraday event-window** (outside current spec): weekly aggregation almost certainly averages out the classical ABDV 2003 AER intraday announcement effect. Future work.

## Peer memory files for a new agent

- `project_fx_vol_econ_complete_findings.md` — comprehensive 349-line findings digest
- `project_fx_vol_econ_gate_verdict_and_product_read.md` — Abrigo strategic memo
- `project_fx_vol_econ_reviewer_and_silent_test_pass_lessons.md` — agent-facing review discipline
- `project_fx_vol_econ_phase4_complete_task33_closing.md` — resume state
- `project_econ_notebook_handoff.md` — historical handoff note (pre-completion)
- `scratch/2026-04-19-fx-vol-econ-complete-findings-pre-task-33.md` — disk mirror

## Ceremonial close

**Task 33 complete. Project closed. Scientific pipeline delivered a disciplined FAIL under the pre-committed specification. The answer is empirically honest: on Colombian weekly data 2008-2026, pre-committed CPI-surprise specifications do not identify a detectable causal effect on COP/USD realized volatility. Pivot candidates (A1 monthly, A4 release-day-excluded) are pre-registered in the forest plot as empirical future-work hooks, not post-hoc rescues.**

For the Abrigo product: the primary-causal-story framing is no longer supportable. Honest positioning pivots to the conditional-event-day narrative and monthly-cycle hedge reframing per A1 — both grounded in pre-registered sensitivities.
