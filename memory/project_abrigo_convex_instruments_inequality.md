---
name: Abrigo product = convex instruments for macro shocks viewed through inequality
description: Abrigo sells option-like CONVEX instruments hedging MACROECONOMIC shocks viewed through the INEQUALITY lens (rich-asset returns vs. working-class consumption); mean-β regression alone insufficient — tail-risk evidence required
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---

Abrigo's product is **convex (option-like) financial instruments** hedging **MACROECONOMIC shocks viewed through the INEQUALITY lens**. Specifically:

- **Shocks are MACRO**: CPI release surprises, FOMC decisions, oil-price moves, FX shocks, growth-news, intervention-day interventions — country-level / aggregate disturbances.
- **The hedged outcome is INEQUALITY-FOCUSED**: Y₃ measures *how* macro shocks differentially impact rich-asset returns (R_equity_c) vs. working-class consumption-bundle returns (Δlog(WC_CPI_c) weighted 60/25/15 food/energy-housing/transport-fuel). The 60/25/15 weights are the inequality-focus marker — they're working-class-bundle weights, not aggregate-CPI weights, which makes Y₃ an inequality-differential outcome variable.
- **Convex payoffs**: laborers buy options (capped-loss, levered-upside) on Y₃ to hedge their disproportionate exposure to inflation-vs-asset-return divergence during macro shocks.
- **On-chain capture**: X_d (Mento basket user volume on Celo) is hypothesized to reflect retail demand for these convex instruments.

**Why:** User clarified during Task 11.O Rev-2 spec review (2026-04-25): originally said "microeconomic shocks" — corrected to "MACROECONOMIC SHOCKS more focused on inequality." The shocks themselves are macro; the inequality lens is in the WC-CPI weighting on Y₃.

**How to apply:**
- ALL econometric model reviews must evaluate validity against this purpose, not just statistical correctness.
- Mean-effect identification (e.g., β > 0 in OLS+HAC) is INSUFFICIENT for convex-payoff pricing. Convex instruments require tail-risk / asymmetric-response / variance-amplification evidence. Mean-shift on Y₃ is necessary but not sufficient.
- The Y₃ design (4-country inequality differential, WC-CPI weighted 60/25/15) is the inequality-focus marker — verify specs preserve this weighting structure rather than absorbing it into aggregate-CPI controls.
- Reviewers must surface any disconnect between mean-β framing in the spec and convex-payoff requirement of the product.
- Distributional welfare evidence (quantile shifts, variance amplification, lower-tail stabilization) — which the user earlier rejected at Q-1b — IS analytically required for the convex-instrument purpose. Future spec revisions may need to revisit this.
- Track A spec (`contracts/.scratch/2026-04-25-task110-rev2-spec-A-autonomous.md`, commit-pending) uses mean-β identification with HAC(4); reviewers must validate whether this is sufficient OR whether tail-risk extensions are required for product-validity.
- Macro shocks are exogenous instrumenting candidates: CPI/FOMC release calendars (already pre-committed in 11.O Step 2b as β-strategy event windows), FX-intervention dates, oil price shocks. The shocks themselves do NOT need to be "microeconomic" to be useful identification variation.
