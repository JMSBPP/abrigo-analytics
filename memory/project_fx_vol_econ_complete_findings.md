---
name: FX-vol-on-CPI-surprise complete findings digest (Phases 1+2+3)
description: Comprehensive scientific + methodological + strategic findings from the full 3-phase structural-econometrics pipeline; gate_verdict=FAIL; A1/A4 positive-significant sensitivities; Colombian asymmetry regime-specific; intervention data-freshness gap; HAC-bootstrap AGREEMENT; five silent-test-pass patterns caught; three integration-test guard installed; strategic product read for Abrigo pivot to monthly-cycle hedge.
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---

# Complete findings digest (as of 2026-04-19, post Task 31 / pre Task 33)

This file consolidates all substantive empirical + methodological + strategic findings from Phases 1+2+3 of the FX-vol-on-CPI-surprise econ-notebook pipeline. Peer memory files:
- `project_fx_vol_econ_phase4_task32_in_flight.md` — logistical resume state (task status, dispatch patterns, baseline)
- `project_fx_vol_econ_gate_verdict_and_product_read.md` — Abrigo strategic memo
- `project_fx_vol_econ_reviewer_and_silent_test_pass_lessons.md` — agent-facing review lessons

## Context (one paragraph)

Structural econometrics pipeline testing whether Colombian CPI surprises cause COP/USD (TRM) realized volatility. Product goal: ground Abrigo (permissionless FX vol insurance via Mento stablecoins) in empirical causal identification. The scientific gate is **T3b: β̂_CPI − 1.28·SE > 0** on the primary weekly OLS. Passing = clean empirical support. Spec Rev 4 pre-committed primary: OLS on RV^{1/3}, weekly, 6 controls, HAC(4) SEs. Sample: 2008-01-02 → 2026-03-01, n_weeks=947.

# Section I: Scientific verdict

## THE HEADLINE

**`gate_verdict.gate_verdict = "FAIL"`** driven by T3b one-sided β̂_CPI − 1.28·SE > 0 failing (value = −0.002981). Under the pre-committed weekly OLS specification, **Colombian CPI surprises do NOT cause a statistically detectable increase in COP/USD realized volatility, 2008-2026.**

## Primary (weekly OLS Column 6)

| statistic | value |
|---|---|
| β̂_CPI | −0.000685 |
| HAC(4) Newey-West SE | 0.001794 |
| T3b statistic (β̂ − 1.28·SE) | −0.002981 |
| T3b verdict | FAIL |
| 90% HAC CI | [−0.003636, +0.002266] (contains zero) |
| T3a two-sided | FAIL TO REJECT (t=−0.38, p=0.70) |
| adj-R² Column 6 | 0.193 |
| n | 947 |

**Block-bootstrap HAC comparison (§3.5):** Politis-Romano stationary block bootstrap vs HAC(4). Overlap ratio = 1.0 (full containment each way); bootstrap CI [−0.003604, +0.002351]. Verdict: **AGREEMENT**. SEs trustworthy; no kernel misspecification; failure is a real scientific finding, not inference artifact.

## Co-primary 1 (daily GARCH-X, Task 19)

- δ̂ = 0 (pinned at Han-Kristensen positivity boundary)
- Self 1987 boundary-corrected LR p = 0.50
- **VARIANCE channel is also null.**

## Co-primary 2 (CPI/PPI decomposition, Task 20)

- β̂_CPI = −0.000605 (with IPP standardized)
- β̂_PPI = +0.000245
- Neither significant; inflation-channel "dominates" but both null.

## Auxiliary gates (NB3 Tasks 24-26)

| gate | result | note |
|---|---|---|
| T1 exogeneity | REJECT (F=15.12, p=1.3e-9) | surprises PREDICTABLE from lagged info → β̂ is predictive-regression coefficient, not strict impulse-response |
| T2 Levene announcement channel | FAIL TO REJECT (W=0.099, p=0.75) | NO weekly variance premium on release weeks; release-week var 0.000490 vs 0.000533 non-release |
| T4 Ljung-Box Q(1..8) | REJECT at every lag | diagnostic; HAC(4) handles |
| T5 Jarque-Bera | REJECT (JB=541, p<1e-118; skew=0.96, kurt=6.2) | diagnostic; Student-t refit absorbs |
| T6 Bai-Perron | UNALIGNED | data-driven breaks at 2009-10, 2014-08, 2016-09; analyst subsample boundaries 2015-01 + 2021-01 → closest break 21 weeks off; diagnostic |
| T7 intervention adequacy | TIGHT PASS | 91% of 1·SE threshold; sign FLIPS negative→positive when intervention dropped |

## §8 forest plot — 14 rows (1 anchor + 13 sensitivities)

Two sensitivity rows exclude zero at 90%, both POSITIVE (opposite primary sign):

- **A1 monthly cadence** (n=220 after R1 fix, Decision #1 compliant): β̂ = +0.0152, CI [+0.0057, +0.0246]
- **A4 release-day-excluded** (n=947): β̂ = +0.0033, CI [+0.0005, +0.0062]
- **A9⁺** (positive-surprise subset, n=13): severely underpowered
- **A9⁻** (negative-surprise subset, n=205): β̂ = +0.0068, CI contains zero

## §9 material-mover spotlight: HALTED

Per anti-fishing protocol (T3b FAIL binds); zero spotlight tables produced. A1/A4 significant rows remain visible in §8 forest plot appendix as pre-registered record only.

## Reconciliation (NB2 §10)

AGREE — directional concordance via joint null (both β̂_CPI 90% HAC CI and δ̂ 90% QMLE CI contain zero).

# Section II: Twelve Decisions locked (Phase 1)

| # | scope | primary | sensitivity alt |
|---|---|---|---|
| 1 | sample window | 2008-01-02 → 2026-03-01, n_weeks=947 | n/a |
| 2 | LHS transform | RV^(1/3) | log(RV) |
| 3 | frequency | weekly | daily |
| 4 | Colombian CPI surprise | `cpi_surprise_ar1` (ABDV 2003 AR(1) expanding, DANE IPC 1954-present) | A9 asymmetric + 60-month rolling AR(1) |
| 5 | US CPI surprise | `us_cpi_surprise_ar1` (AR(1) expanding, FRED CPIAUCSL, 12-mo warmup, BLS cal) | n/a |
| 6 | BanRep rate surprise | event-study daily ΔIBR at Junta dates, weekly sign-preserving sum | n/a |
| 7 | VIX aggregation | `vix_avg` (weekly arithmetic mean of daily FRED VIXCLS) | `vix_friday_close` rejected |
| 8 | oil_return | log-return of weekly-last positive WTI close (ARG_MAX, value>0) | n/a |
| 9 | intervention regressor | `intervention_dummy` (binary any-activity) | `intervention_amount`; S7 drops 2024-10+ |
| 10 | collinearity adjustment | none (max VIF well below 10, max \|corr\| = 0.142) | n/a |
| 11 | stationarity treatment | levels-primary (ADF rejects; KPSS flagged with Cavaliere-Taylor 2005 caveat) | first-differenced alt documented |
| 12 | merge policy | listwise complete-case (n=947) | ffill/MICE rejected |

All twelve respect spec Rev 4 pre-commitments with `anti_fishing_binding = True`.

# Section III: Phase 1 substantive findings

## Finding 1: Colombian CPI surprise asymmetry (§4a)

- Event density 23.0% (218/947 weeks)
- Sign balance: 205 negative / 13 positive — **~94% negative**
- Nonzero mean: −0.69 (strongly biased, NOT centered on zero)
- Nonzero |skew|: 0.90, kurt_exc: +1.11

### Root cause (Trio 2 audit, `6d3a130b4`)

Three candidate bugs ruled out: alignment rate=1.000; no imputation contamination; warm-up (643 months pre-sample vs 12-month threshold) far beyond adequate.

**Accepted root cause — regime mismatch.** AR(1) expanding-window anchors intercept to 1954-present history.
- Pre-sample mean MoM (1954-2007, incl. hyperinflation): +1.23%
- In-sample mean MoM (2008-2026, modern BanRep): +0.40%
- Ratio ~3× → forecast systematically pulled above modern reality → systematic negative surprises
- Correlation(surprise, CPI level) = +0.37

## Finding 2: US CPI symmetric + fat-tailed (§4b)

- Event density 22.9% (monthly cadence, ≈ Colombian)
- Sign balance: 110 pos / 107 neg — symmetric
- Nonzero mean: +0.0025 (centered)
- Nonzero |skew|: 1.31
- Nonzero kurt_exc: **+8.51**
- Top-5 outliers map to real macro events (Lehman, 2008 oil spike, COVID, 2022 deceleration)

**Interpretation:** same operator on US data is unbiased → confirms Colombian asymmetry is **regime-specific (hyperinflation anchoring), NOT a methodological bug.** Fat tails motivate A12 HAC(12) sensitivity.

## Finding 3: BanRep rate surprise (§4c)

Decision #6: event-study daily ΔIBR at Junta dates, weekly sign-preserving sum (policy rate is step function; AR(1) would be misspecified). Grounding: Anzoátegui-Zapata & Galvis 2019; Uribe-Gil & Galvis-Ciro 2022 BIS WP 1022. New table `banrep_meeting_calendar` (234 rows), scraper `contracts/scripts/build_banrep_meeting_calendar.py`. 88 non-zero weeks; sign balance 42/46 — symmetric; corr with `cpi_surprise_ar1` = +0.074 (NO collinearity).

## Finding 4: VIX admissibility (§4d)

Decision #7 `vix_avg` (weekly mean of daily VIXCLS). mean=19.90, std=8.75, max=74.62 (2020-03-16). kurt_exc=+8.51, lag-1 ACF=0.9435 (justifies HAC(4)). Univariate corr with rv_cuberoot=+0.355.

## Finding 5: Oil return construction (§4e)

Decision #8: log-return of weekly-LAST POSITIVE WTI close. Handles 2020-04-20 negative WTI. kurt_exc=+17.79 (**fattest-tailed regressor**). lag-1 ACF=−0.0004 (near-martingale). Top-5 outliers: 3× COVID 2020, 2× GFC 2008.

## Finding 6: Intervention regime heterogeneity + DATA-FRESHNESS GAP (§4f)

Decision #9: `intervention_dummy` primary; `intervention_amount` sensitivity; **S7 drops 2024-10+** for freshness.

- Active fraction 33% (316/947)
- **Data-freshness gap:** source `banrep_intervention_daily` ends 2024-10-04 → **73 weeks carry dummy=0 by absence-of-data, not confirmed absence** (8% of sample). Mitigated by pre-registered S7 sensitivity (n_effective=874 after drop).
- Regime heterogeneity:
  - 2008-2014: active 71%
  - 2015-2019: dormant 3.8% (post-free-float)
  - 2020 COVID: active 63.5% (only regime with negative mean signed amount)
  - 2024 partial: 22.6%

## Finding 7: Joint regressor behavior (§5)

- Max |corr| across 6 RHS regressors: **0.142** (vix × oil) — well below BKW 0.7 threshold
- VIF max well below 10 → Decision #10 no-collinearity-adjustment
- Non-linearity signal: oil ↔ rv Pearson −0.114 vs Spearman −0.046 — a handful of extreme weeks drive Pearson; §5 Trio 3 scatter confirms local, not systemic
- **Verdict:** regressor matrix clean; OLS inference stable at n=947

## Finding 8: Stationarity (§6)

ADF rejects unit root on RV + all surprises. KPSS flags residual structure on VIX and oil (Cavaliere-Taylor 2005 volatility-noise). **Decision #11: levels-primary.** First-differenced documented, not adopted.

## Finding 9: Merge policy (§7)

n=947 complete case. Listwise vs ffill vs MICE compared; ffill contaminates low-cadence macro; MICE overhead marginal at n=947. **Decision #12: listwise complete-case.**

# Section IV: Phase 2 + Phase 3 findings

## Finding 10: First β̂_CPI estimate — T3b primary FAIL (Task 17, NB2 §3+§3.5)

See Section I headline. Attenuation + asymmetry + measurement-error predictions all held. HAC-bootstrap AGREEMENT rules out SE artifact.

## Finding 11: Coefficient ladder isolates where explanatory power lives (NB2 §3)

| col | regressors | adj-R² | interpretation |
|---|---|---|---|
| 1 | cpi only | ≈ 0 | macro-surprise alone explains nothing |
| 2 | + us_cpi | ≈ 0 | still nothing |
| 3 | + banrep | ≈ 0 | still nothing |
| 4 | + vix_avg | 0.125 | **VIX does the work** |
| 5 | + intervention | 0.190 | FX-policy adds marginal power |
| 6 | + oil_return | **0.193** | commodity closes the set; primary gate column |

**Load-bearing qualitative result:** macro-surprises carry ≈0 conditional variance. VIX + intervention + oil carry the explanatory power. Critical for product framing.

## Finding 12: GARCH-X VARIANCE channel is null (Task 19, NB2 §4)

δ̂ = 0 pinned at Han-Kristensen positivity boundary; Self 1987 LR p = 0.50. No variance-channel transmission either.

## Finding 13: CPI/PPI decomposition — neither significant (Task 20, NB2 §5)

β̂_CPI = −0.000605, β̂_PPI = +0.000245 (with IPP standardized). Inflation-channel "dominates" but both null.

## Finding 14: T1 exogeneity REJECTS (NB3 §1)

F=15.12, p=1.3e-9. Lagged surprise + lagged RV + lagged controls predict current surprise (t_lag = −6.56 on lagged surprise). Primary β̂ is **predictive-regression coefficient**, NOT strict impulse-response. AR(1) expanding-window operator fit ONCE on full history, not rolling-refit → residual serial correlation → this is a specification finding, not an implementation bug.

## Finding 15: T2 Levene announcement channel FAIL TO REJECT (NB3 §2)

W=0.099, p=0.75. **No weekly variance premium on release weeks.** Mechanically, release-week variance is marginally LOWER (0.000490 vs 0.000533). This is the cleanest null in the pipeline — matches classical ABDV 2003 intraday announcement effects being absorbed by weekly aggregation.

## Finding 16: T6 Bai-Perron UNALIGNED (NB3 §6)

3 data-driven breaks at 2009-10, 2014-08, 2016-09 via ruptures.Binseg+RBF. NB2 analyst subsample boundaries at 2015-01 + 2021-01. Closest detected break is 21 weeks off from analyst choice → diagnostic only.

## Finding 17: T7 intervention adequacy TIGHT PASS (NB3 §7)

91% of 1·SE threshold. Sign FLIPS negative→positive when intervention dropped. Tight margin.

## Finding 18: A1 monthly + A4 release-day-excluded positive-significant (NB3 §8)

See Section I forest plot. Both CIs exclude zero at 90%, both POSITIVE (opposite primary sign):
- A1 monthly cadence (n=220, Decision #1 compliant after R1 fix): β̂=+0.0152, CI [+0.0057, +0.0246]
- A4 release-day-excluded (n=947): β̂=+0.0033, CI [+0.0005, +0.0062]

Under anti-fishing protocol these cannot be promoted to primary; they remain pre-registered robustness record.

# Section V: Strategic product read (for Abrigo)

## Clean-primary story DIED

"CPI surprise linearly moves weekly TRM vol by β" is NOT empirically supported on Colombian weekly data under Rev 4 spec.

## Anti-fishing discipline VINDICATED

Pre-committed primary failed cleanly; no post-hoc pivot to significant sensitivities permitted. **SUCCESS of scientific integrity, not a pipeline failure.** Reviewers asking "did you p-hack?" get shown pre-reg hash + 4 reviewer cycles passed in Task 15 + 3-phase audit trail.

## Conditional pivot paths remain live

1. **A1 monthly cadence** (pre-registered, CI excludes zero): reframes product as "monthly CPI-cycle hedge" rather than "weekly pre-event hedge"
2. **A4 release-day-excluded** (pre-registered, CI excludes zero): effect in non-release-day dynamics — possibly anticipation / lagged-response
3. **Intraday event-window analysis** (OUTSIDE current spec): weekly aggregation may average out classical ABDV 2003 AER intraday announcement effect. Future work.

## Honest commercial positioning

"At pre-registered primary specification, no effect detected; at monthly cadence with pre-commitment-compliant window, a positive effect is detectable at 90%. Commercial positioning pivots from weekly-CPI-hedge to monthly-cycle-hedge, grounded on A1 + A4 as pre-registered robustness."

**Do NOT:** pitch weekly CPI-surprise hedge against the pre-committed primary audit trail. That would be dishonest and contradict `anti_fishing_binding`.

See peer memory `project_fx_vol_econ_gate_verdict_and_product_read.md` for full Abrigo strategic memo.

# Section VI: Methodological findings (why primary failed)

1. **AR(1) expanding-window anchors to 1954-2007 hyperinflation.** Pre-sample mean IPC MoM (1954-2007) = +1.23% vs in-sample (2008-2026) = +0.40%. AR(1) forecasts pulled ~3× above modern reality → 94% of surprises NEGATIVE → classical attenuation bias on β̂_CPI.
2. **IBR structural absence pre-2008.** Forced sample start at 2008-01-02 → n=947 instead of n>1200 that 2003-2026 would have given.
3. **T1 rejection confirms AR(1) mis-specification.** Lagged CPI surprise predicts current surprise (t=−6.56) → operator fit once on full history, not rolling-refit → residual serial correlation → β̂_CPI is predictive-regression coefficient, not impulse-response.
4. **Intervention data-freshness gap.** `banrep_intervention_daily` ends 2024-10-04 → 73 weeks (8%) carry `intervention_dummy=0` by absence-of-data → mitigated by pre-registered S7 sensitivity (n_effective=874 after drop), not tested as primary.

# Section VII: Review process findings (lessons for future agents)

**Silent-test-pass pattern hit 5 times:**
1. Task 22 E1: `nb2_serialize.py` date coercion — tests used synthetic inputs
2. Task 25 cell 10: NB3 `panel` variable undefined — tests parsed source, never ran cell chain
3. Task 27 follow-up: NB3 §1 never unpacked PKL into bare-name variables
4. Task 24 `from scripts import cleaning` at NB1 cell 116 — bootstrap didn't add `contracts/` to sys.path
5. Task 31 R2: `test_nb3_section10_gate.py` tested synthetic only, didn't exec live cell 31

**Remediation: 3 integration tests** (`test_nb[123]_end_to_end_execution.py`) run `jupyter nbconvert --execute` on each notebook; fail on any runtime error. **New pattern:** always include at least one end-to-end execution test, not just source parsers.

**Three-way review value demonstrated:**
- **Model QA** catches: econometric label-vs-implementation drift (T1 Mincer-Zarnowitz vs BEG; "Bai-Perron" vs ruptures.Binseg), regressor spec changes not disclosed in row labels, boundary-case inference validity
- **Reality Checker** catches: spec-commitment violations (A1 window), silent-test-pass patterns, prose-vs-code schema drift, citation integrity, test architecture asymmetry
- **Technical Writer** catches: reader-journey information propagation (README-vs-notebook gap on anti-fishing), PDF export readiness, documentation honest-caveat visibility

Each reviewer finds things the others can't. The three-way pattern is load-bearing for scientific artifact quality.

# Section VIII: Motivated sensitivities (frozen pre-registration)

Frozen in Task 13, hashed into `nb1_panel_fingerprint.json` as `sensitivity_preregistration_hash` (commit `3fbc1409e`). Task 17 onwards does not modify this list.

| ID | sensitivity | motivating finding | Phase-3 result |
|---|---|---|---|
| A1 | monthly cadence | Decision #1 alt | **β̂=+0.0152, CI excludes zero POSITIVE** |
| A4 | release-day-excluded | diagnostic | **β̂=+0.0033, CI excludes zero POSITIVE** |
| A9 | asymmetric response | 94% negative asymmetry | A9⁺ n=13 underpowered; A9⁻ CI contains zero |
| A12 | HAC(12) bandwidth | fat tails | consistent with A9/HAC(4) |
| S1 | 60-month rolling AR(1) | attenuation-reduction hypothesis | consistent with primary |
| S2 | 2015-2017 COP-crisis drop | regime shock | consistent |
| S3 | 2020-2021 COVID drop | fat-tail outliers | consistent |
| S4 | CPI × intervention interaction | exploratory | consistent |
| S5 | event-day vol ratio | product-facing | see T2 null (release-week var marginally LOWER) |
| S6 | `intervention_amount` signed | Decision #9 alt | consistent |
| S7 | drop 2024-10+ | data-freshness | consistent |

**Note:** early digests treated S5 as "THE product-viability test"; NB3 T2 Levene's FAIL TO REJECT (W=0.099, p=0.75) with release-week variance marginally LOWER supplies the equivalent evidence at weekly cadence. The product pivot therefore routes through A1 monthly + A4 release-excluded rather than S5.

# Section IX: Deferred issues for Task 33 final cleanup

- R5 venv-misactivation silent-pass (handoff-metadata can't distinguish bare-python vs venv)
- UQ1 T1 Mincer-Zarnowitz vs BEG label
- UQ2 "Bai-Perron" vs ruptures.Binseg+RBF label
- UQ3 A1/A5 disclosure in forest row labels
- UQ4 GARCH-X 6dp zero display formatting
- UQ5 T7 heuristic formalization
- UQ6 bootstrap-HAC 50% lenient overlap tolerance
- UQ7 (see Task 31 Reality Checker report)
- Forest plot secondary rendering: cell 33 PNG emission independent from cell 25 in-notebook figure; full refactor to shared `_draw_forest_plot(ax, table)` helper deferred
- `gate_verdict.json` schema additions: `t1_pvalue`, `t1_source`, Abrigo-simulator predictive-regression-interpretation flag (prose stripped in Task 31 R3; schema expansion optional)
- Forest plot PDF-native rendering for three PDF exports (currently links PNG)

# Section X: Commit archaeology

## Phase 1 Decision locks

- §4a Trio 1 (Colombian CPI inspection): `0f9751bc6`
- §4a Trio 2 (alignment + imputation audit): `6d3a130b4`
- §4a Trio 3 (Decision #4 lock): `bfb52e8d0`
- §4b Trio 1 (US CPI inspection): `50da209f6`
- §4b Decision #5 lock: `53d0b4895`
- §4c Decision #6 lock (BanRep rate surprise): `11389a7b1`
- §4d Decision #7 lock (VIX aggregation): `d55eda6a9`
- §4e Decision #8 lock (oil_return): `c0c9d7eaf`
- §4f Decision #9 lock (intervention + S7): `050484524`
- §5 Trio 1 (correlation matrix): `2a47157e8`
- §5 Trio 2 (VIF + Decision #10): `f87bd4075`
- §5 Trio 3 (scatter matrix): `a224b80a1`
- §6 Trio 1 (ADF + KPSS): `540091eea`
- §6 Trio 2 (Decision #11 levels-primary): `460b08cd4`
- §7 Trio 1 (missingness audit): `d3f936cce`
- §7 Trio 2 (merge-policy comparison): `3e1e25ed7`
- §7 Trio 3 (Decision #12 listwise): `b3e034141`
- cleaning.py green: `55b512c02`
- §8b ledger + fingerprint emission: `abdf349c8`
- fingerprint drift refresh: `473d4ddda`

## Phase 2 canonical

- Task 16 green: `ffad2b739` — NB2 §1-2 setup
- Task 17 green: `ebe9bc681` — FIRST β̂_CPI
- Task 18 green: `3100f2ad7` — diagnostics + Student-t
- Task 19 green: `33238ddf5` — GARCH-X δ̂=0 boundary
- Task 20 green: `e68ac27c0` — CPI/PPI decomposition
- Task 21 green: `7fd8b1059` — T3B_GATE_VERDICT=FAIL
- Task 22 green: `250f9e713` — reconciliation AGREE + atomic serialization
- Task 22 hotfix: `12170a803` — E1+E2
- Task 23 green: `def90c540` — §12 economic magnitude + 3-way remediation
- E3-E10 batch: `c84dbaa02` — Andrews 1999 citation + PDF readability

## Phase 3 canonical

- Task 24 green: `a9e58be34` — NB3 §1-2 T1 rejected + pre-flight clean
- Task 25 green: `e77e81dc1` — T2 Levene FAIL TO REJECT
- Task 26 green: `a8d6a4bf3` — Bai-Perron UNALIGNED + T7 TIGHT PASS
- Task 27 green: `29b209dd8` — forest plot 14 rows + A1/A4 positive-significant
- Task 28 green: `a44c4e3c2` — §9 anti-fishing HALT
- Task 29 green: `1139f5717` — `gate_verdict.json` emitted
- Task 30 green: `5235a90cb` — README auto-render + CI diff check
- Task 31 remediation final: `479ebf609` — A1 window fix + C2 anti-fishing paragraph + R2 live-exec ← HEAD
