---
name: Pathological-HALT as anti-fishing checkpoint
description: When a pre-committed threshold fails empirically, HALT + disposition memo + user-enumerated pivot + CORRECTIONS block + post-hoc 3-way review — never silent threshold tuning
type: feedback
originSessionId: phase0-vb-mvp / Rev-5.3 → Rev-5.3.1 transition
---

**Fact**: When a pre-committed scientific threshold fails the empirical evidence, the disciplined path is:
1. HALT the calibration with a typed exception (e.g., `CalibrationStructurallyPathological`).
2. File a disposition memo (`contracts/.scratch/...-pathological-disposition.md`) enumerating the threshold value, the empirical value, and ≥3 pivot options (abandon X-source / pivot to different X / loosen scope / panel-extend / pivot Y).
3. Surface the memo to the user and do NOT auto-select a pivot.
4. After user picks a path, file a CORRECTIONS block in the next plan revision documenting (a) the original threshold, (b) the empirical value, (c) the user-chosen relaxation, (d) the load-bearing-guarantees-preserved argument.
5. Run a 3-way review (CR + RC + Senior PM) of the CORRECTIONS revision before commit.

**Why**: the alternative — silently re-tuning thresholds to pass — is the textbook fishing pattern. The Rev-5.3 → Rev-5.3.1 transition (commits `13cfe5f56` HALT → `7afcd2ad6` relaxation) is the canonical example: N_MIN failed at 80 because basket-aggregate had 77 non-zero weeks; the HALT memo enumerated 5 pivot options; user selected path α (relax to 75 with `required_power(75, 13, 0.40) = 0.8638 ≥ POWER_MIN`); the CORRECTIONS block documented the load-bearing-guarantees argument; 3-way review audited the change post-hoc. Without the HALT discipline, an agent could have silently relaxed N_MIN inside the calibration code and produced a "PASS" verdict that nobody could reconstruct.

**How to apply**:
1. Pre-commit thresholds in source-code `Final` constants AND in design doc; modification requires design-doc revision + CORRECTIONS block + 3-way review.
2. Calibration code raises a TYPED exception on threshold failure; do not log-and-return-zero.
3. Disposition memo MUST enumerate ≥3 pivot options before user-input; option (c) "loosen scope mid-stream" is anti-fishing-banned and must be flagged as such in the memo.
4. CORRECTIONS-block content must cite (a) old value, (b) new value, (c) preserved-guarantees argument, (d) commit anchors for old + new state.
5. Pattern fired in: Rev-5.3.1 N_MIN relaxation; FX-vol-CPI Rev-3.1 nbconvert-guarded notebook patch; Phase-A.0 Rev-4.1 EXIT criterion insertion.

## Related memory

- `project_rev531_n_min_relaxation_path_alpha.md` — the canonical example
- `feedback_three_way_review.md` — the review pattern that audits CORRECTIONS blocks
- `feedback_no_code_in_specs_or_plans.md` — exception: pinned thresholds + tamper-evident hashes ARE in source
- `project_fx_vol_cpi_notebook_complete.md` — sister anti-fishing precedent (gate_verdict=FAIL, no rescue)
- `project_phase_a0_exit_verdict.md` — sister anti-fishing precedent (k1 EXIT criterion fired)
