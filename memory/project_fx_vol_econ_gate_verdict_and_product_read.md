---
name: FX-vol-econ gate verdict FAIL + Abrigo strategic product read
description: Strategic memo for any agent picking up the Abrigo product thread after the 3-phase pipeline closed FAIL — covers scientific verdict, pivot paths (A1 monthly, A4 release-day-excluded, intraday future work), anti-fishing framing for external pitch, and honest commercial positioning guidance.
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---

# Abrigo strategic product memo — post gate_verdict=FAIL

For any agent picking up the Abrigo commercial thread after the econ-notebook pipeline closed. Co-read: `project_fx_vol_econ_complete_findings.md` (scientific detail), `project_ran_positioning_principles.md`, `project_ran_brand_name.md`, `project_abrigo_painkiller_evidence_base.md`.

## One-sentence verdict

**`gate_verdict.gate_verdict = "FAIL"`.** Under the pre-committed Rev 4 weekly OLS primary, Colombian CPI surprises do NOT cause statistically detectable COP/USD realized volatility. The "weekly CPI-surprise hedge" pitch line is NOT defensible against the audit trail.

## What this is NOT

- **Not a pipeline failure.** All 36 planned tasks delivered. 758+3 tests green. HEAD `479ebf609` pushed.
- **Not a product death sentence.** Two pre-registered sensitivities (A1 monthly cadence, A4 release-day-excluded) show CIs excluding zero at 90% in the POSITIVE direction.
- **Not methodologically contested.** HAC-bootstrap AGREEMENT rules out SE artifact; Colombian asymmetry (94% negative surprises) is regime-specific (hyperinflation anchor), confirmed not a bug.

## What it IS

- **A scientific-integrity success.** Pre-commitment held through 12 reviewer passes and 3 full phases. Post-hoc spec search to clear T3b was available at every step and was refused every time.
- **A pivot cue for commercial positioning.** The evidence directs the product from "weekly pre-event hedge" to "monthly CPI-cycle hedge" or "between-release vol dynamics hedge."

## The three live pivot paths

### Pivot 1: A1 monthly cadence (STRONGEST)

- β̂ = +0.0152, 90% CI [+0.0057, +0.0246]; n=220 after Decision #1 sample-window compliance (R1 fix in Task 31)
- CI excludes zero and is positive — consistent with commercial hypothesis
- Commercial framing: "Abrigo monthly CPI-cycle hedge" — LP provides FX vol cover across a 30-day CPI publication cycle; hedge buyer pays premium priced against the empirical monthly CPI → TRM-vol relationship
- Audit trail defense: A1 was pre-registered in `nb1_panel_fingerprint.json` sensitivity_preregistration_hash before any results were observed. It is NOT a post-hoc specification pick.

### Pivot 2: A4 release-day-excluded (SECONDARY SUPPORT)

- β̂ = +0.0033, 90% CI [+0.0005, +0.0062]; n=947
- CI excludes zero, positive, but effect magnitude small
- Commercial framing: "non-release-day FX-vol dynamics respond to realized-surprise shock" — supports a hedge that activates across the full week rather than clustering on release days
- Physical interpretation: anticipation effect (vol builds pre-release) or lagged-response effect (vol persists post-release into following days). Either reading is commercially actionable.

### Pivot 3: Intraday event-window analysis (FUTURE WORK)

- **OUTSIDE current spec.** Rev 4 pre-committed to weekly aggregation; intraday analysis would be a new spec with its own pre-registration.
- Weekly aggregation averages out classical ABDV 2003 AER intraday announcement effects. T2 Levene FAIL TO REJECT at weekly cadence (release-week var marginally LOWER) matches this — the effect classical finance expects is at intraday scale, not weekly.
- Commercial framing: if Abrigo MVP needs a weekly-cadence primary before intraday work is feasible, **Pivot 1 or 2 carry the MVP; Pivot 3 is a V2 research track.**

## Anti-fishing discipline for external pitch

When external stakeholders (Crecimiento operators, Mento integrators, investors) ask about the research:

**DO SAY:**
- "We pre-registered a weekly primary specification and it came back null — zero detected weekly effect from CPI surprises on TRM vol. Two of our pre-registered robustness checks (monthly cadence, release-day-excluded) show positive significant effects at 90%. We're pivoting the product from weekly pre-event to monthly cycle hedging, grounded on those pre-registered robustness results."
- "Our research discipline held through three phases of independent review. You can see the pre-registration hash, the 12 reviewer passes, the anti-fishing audit trail. The evidence base for the pivoted product is what the pre-registration said would be acceptable evidence ahead of time."

**DO NOT SAY:**
- "We found that CPI surprises drive weekly TRM vol." (FALSE — primary failed)
- "The monthly effect is our main finding." (VIOLATES anti-fishing; A1 was a robustness check, not a pre-committed primary — saying "main finding" would suggest post-hoc specification search.)
- "With some adjustments to the regression we got significance." (P-hack-sounding. The truthful frame: the pre-registered monthly sensitivity showed positive significance; no post-hoc adjustment was made.)

## Honest commercial positioning — painkiller framing

Per `project_abrigo_painkiller_evidence_base.md`, every pain claim must be grounded in Tier-1 feasibility documentation. Post-FAIL, the painkiller claim updates:

- **Pre-research claim:** "Hedge pre-CPI-release volatility spikes on COP/USD."
- **Post-research claim:** "Hedge the month-over-month FX-vol cycle around Colombian CPI publication timing, empirically validated on pre-registered monthly sensitivity A1."

The core painkiller economics (Colombian corporates + remittance receivers face FX vol they cannot currently hedge cost-effectively) are unchanged by the primary failure. What changed is the **rhythm** of the hedge: not a sharp pre-event payoff but a smoothed monthly cycle exposure.

## Abrigo simulator calibration — predictive-regression flag

T1 exogeneity REJECTS (F=15.12, p=1.3e-9). This means β̂_CPI (and by extension β̂_A1, β̂_A4) are **predictive-regression coefficients** — they describe how past information predicts current RV, not how exogenous surprises cause future RV. For simulator calibration:

- Use the coefficients as **conditional predictive input**, not as impulse-response generators
- Do NOT simulate "CPI surprise → TRM vol" as a causal chain; simulate "observed state including current-CPI-surprise predictor → next-period RV distribution"
- This is a modeling discipline note, not a product-pitch barrier. LP hedge premium pricing uses conditional distribution; the predictive-vs-causal distinction is technical, not commercial.

## What Task 33 still owes the product thread

- Forest plot: A1 + A4 rows must be visible, clearly labeled "pre-registered robustness, positive-significant at 90%"
- README: anti-fishing paragraph (C2, committed `c01ef24c6`) must remain; do NOT delete or soften
- `gate_verdict.json`: primary gate_verdict stays FAIL; do NOT edit to introduce a "conditional pass" field that would reopen anti-fishing risk
- Deferred schema additions (`t1_pvalue`, predictive-regression flag) ONLY expand schema, never change the top-line verdict field

## Pointer to peer material

- `project_fx_vol_econ_complete_findings.md` — full scientific detail (point estimates, CIs, all 18 findings)
- `project_fx_vol_econ_phase4_task32_in_flight.md` — logistics + next steps
- `project_fx_vol_econ_reviewer_and_silent_test_pass_lessons.md` — agent process lessons
- `project_ran_positioning_principles.md` — non-crypto mainstream framing, painkiller-not-vitamin, no-decentralization-sell
- `project_ran_brand_name.md` — Abrigo (Spanish: shelter/coat); trademark + domain clearance pending
- `project_abrigo_painkiller_evidence_base.md` — Tier-1 evidence grounding for all pain claims
- `project_ran_product_framing.md` — never name Angstrom/Panoptic in pitch; Colombia = pilot only
- `project_abrigo_two_tier_field_rule.md` — story fields hide crypto, tech-disclosure fields factually disclose
