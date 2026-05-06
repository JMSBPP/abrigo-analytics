---
name: Econometric notebook handoff (historical — SUPERSEDED by project_fx_vol_cpi_notebook_complete)
description: Historical pre-Phase-1 handoff note. Superseded 2026-04-19 by project_fx_vol_cpi_notebook_complete.md — all 33 tasks closed, gate_verdict = FAIL. This file preserved as historical record only.
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
# PROJECT CLOSED 2026-04-19 — see project_fx_vol_cpi_notebook_complete.md

This file is the pre-Phase-1 handoff note from 2026-04-16. The pipeline has since shipped:
- All 33 tasks completed across 4 phases
- 3 notebooks (NB1 118 cells, NB2 45 cells, NB3 34 cells)
- 5 artifacts emitted (nb1_panel_fingerprint.json + nb2_params_point.json + nb2_params_full.pkl + gate_verdict.json + README.md)
- gate_verdict = "FAIL" (β̂_CPI = −0.000685, 90% CI [-0.0036, +0.0023])
- Anti-fishing discipline held; A1 monthly + A4 release-excluded pivot candidates pre-registered
- Test baseline at close: 768 passed + 7 skipped

See `project_fx_vol_cpi_notebook_complete.md` for the completion record.
See `project_fx_vol_econ_complete_findings.md` for the 349-line comprehensive findings digest.

# Historical resume state as of 2026-04-16 end of session

## What's COMPLETE (do not redo)

### Data pipeline (8 tasks, 47 tests)
- `contracts/scripts/econ_schema.py` — 10 CREATE TABLE DDL + `init_db()`
- `contracts/scripts/econ_banrep.py` — TRM (Socrata), IBR (SDMX XML), intervention (cached JSON)
- `contracts/scripts/econ_fred.py` — FRED daily/monthly + BLS release dates
- `contracts/scripts/econ_dane.py` — IPC/IPP/release calendar CSV parsers
- `contracts/scripts/econ_panels.py` — `build_weekly_panel()`, `build_daily_panel()`, `compute_ar1_surprises()`
- `contracts/scripts/econ_pipeline.py` — `log_manifest()`, `validate_weekly_panel()`, `validate_daily_panel()`, `ValidationError`

### Query API (4 tasks, 27 tests, 17 endpoints)
- `contracts/scripts/econ_query_api.py` — the ONLY thing the notebook imports
- `contracts/scripts/tests/test_econ_query_api.py` — 27 tests against real DB

**Complete endpoint list:**
1. `get_weekly_panel(conn, start, end)` → DataFrame — primary OLS dataset
2. `get_daily_panel(conn, start, end)` → DataFrame — GARCH-X dataset
3. `get_weekly_panel_release_only(conn, start, end)` → DataFrame
4. `get_weekly_panel_subsample(conn, split_date, start, end)` → (pre, post) tuple
5. `get_manifest(conn)` → list[ManifestRow]
6. `get_table_summary(conn)` → dict[str, int]
7. `get_rv_excluding_release_day(conn, start, end)` → DataFrame (A4 sensitivity)
8. `get_weekly_panel_by_release_type(conn, start, end)` → (cpi_only, ppi_only, both)
9. `get_daily_panel_release_days(conn, start, end)` → DataFrame
10. `get_weekly_panel_release_split(conn, start, end)` → (release, non_release) for T2 Levene
11. `get_date_coverage(conn)` → dict[str, DateCoverage]
12. `get_surprise_series(conn, series="cpi"|"us_cpi"|"ppi", start, end)` → DataFrame (T1)
13. `get_release_calendar_aligned(conn, series="ipc"|"ipp"|"bls", start, end)` → DataFrame
14. `get_monthly_panel(conn, start, end)` → DataFrame (A1 monthly horizon)
15. `get_standardized_ppi_change(conn, start, end)` → DataFrame (expanding-window)
16. `get_panel_completeness(conn)` → DataFrame (quality gate)
17. `get_intervention_details(conn, start, end)` → DataFrame (T7 deep-dive)

**Exported constants:** `PRIMARY_LHS = "rv_cuberoot"`, `PRIMARY_RHS = ("cpi_surprise_ar1", "us_cpi_surprise", "banrep_rate_surprise", "vix_avg", "intervention_dummy", "oil_return")`, `SUBSAMPLE_SPLITS = (date(2015,1,5), date(2021,1,4))`

### Database populated
- `contracts/data/structural_econ.duckdb` (4.3 MB) — all 10 raw tables + 2 derived panels
- Key row counts: weekly_panel=1,215; daily_panel=5,527; TRM=8,251; IBR=4,461; intervention=1,674; IPC=861; IPP=322
- 280 Colombian CPI AR(1) surprises, 279 US CPI AR(1) surprises, 221 daily surprise placements

### Test suite
- 74 tests across 8 test files, all passing (`.venv/bin/python -m pytest scripts/tests/ -v`)

### Key commits (phase0-vb-mvp branch, origin=dev=JMSBPP)
- `133d1db50` — query API Task 4 (final)
- `3dbaf922a` — impl plan for query API
- `e4e66a1fe` — AR(1) surprises + CAST fix
- `cdf7cb488` — panel builders
- `e038db981` — data schema spec Rev 3
- `9948d37ec` — Priority 1b resolved (IBR + intervention verified)

---

## WHAT'S NEXT: Estimation Notebook

### The ONLY two context files needed to start

1. **Upstream econometric spec (DEFINES the model):**
   `contracts/notes/structural-econometrics/specs/2026-04-15-fx-vol-cpi-surprise.md` (Rev 4)
   - Primary OLS: RV^(1/3) on CPI surprise + 5 controls
   - Co-primary: GARCH(1,1)-X with |s_CPI| in variance equation
   - Sensitivities A1-A9, spec tests T1-T7
   - Pre-committed primary for gate decision (T3b)

2. **Query API (the notebook's ONLY interface to data):**
   `contracts/scripts/econ_query_api.py`
   - Import and call these functions — do NOT write SQL
   - Do NOT touch raw tables directly
   - Do NOT import `econ_panels.py` or `econ_pipeline.py`

### Workflow for the notebook

1. **Brainstorm the notebook narrative** (use `superpowers:brainstorming` skill)
   - What's the arc? Data overview → RV construction → Primary OLS → GARCH-X → T1-T7 → A1-A9 → Gate decision
   - What plots accompany each section?
   - Output format: `.ipynb` only, or also LaTeX PDF via nbconvert?
   - Location: propose `notebooks/structural_econ_analysis.ipynb`

2. **Write notebook spec** (narrative outline, not code plan)
   - Section headings + cell descriptions
   - Which API function each cell calls
   - Expected plot per section
   - Interpretation template for result text

3. **Dispatch Analytics Reporter agent** to author the notebook
   - Give it: notebook spec + API module path + database path
   - It writes cells, runs them, validates outputs, commits executed `.ipynb`

4. **3-way review** of the executed notebook:
   - Reality Checker (numbers match expected ranges)
   - Model QA (econometric correctness)
   - Technical Writer (narrative clarity)

### Non-negotiable rules for the notebook

- Use ONLY `econ_query_api.py` — never raw SQL, never direct table access
- Connection: `duckdb.connect("contracts/data/structural_econ.duckdb", read_only=True)`
- Pre-committed primary decision: use `PRIMARY_LHS` and `PRIMARY_RHS` constants from the API
- T3b gate: one-sided 90% CI on β̂ for cpi_surprise_ar1 in the pre-committed primary spec ONLY
- NEVER claim gate passed if GARCH-X disagrees with OLS on sign/significance of β (reconciliation protocol)
- Report primary FIRST, sensitivities AFTER with explicit multiple-testing caveat
- AR(1) CPI surprise (cpi_surprise_ar1) is the CONFIRMED PRIMARY (not fallback) — EME survey data is unavailable

### Working directory and commands

```bash
cd /home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts
.venv/bin/python -m pytest scripts/tests/ -v  # verify 74 tests pass
.venv/bin/jupyter notebook  # to run the notebook
```

### Critical files to read at session start

Just these two (do not read anything else — the API abstracts everything):
1. `contracts/scripts/econ_query_api.py` (the interface)
2. `contracts/notes/structural-econometrics/specs/2026-04-15-fx-vol-cpi-surprise.md` (the model spec)

Optional third for decomposition logic only:
3. `contracts/notes/structural-econometrics/specs/2026-04-16-data-schema-acquisition.md` (explains the panels)

**Do NOT read** `econ_panels.py`, `econ_pipeline.py`, `econ_banrep.py`, etc. — the API hides those details.
