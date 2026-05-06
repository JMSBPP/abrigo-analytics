---
name: Abrigo painkiller evidence base = MACRO_RISKS folder
description: Reality Checker grounds every painkiller claim in the liq-soldk-dev MACRO_RISKS research folder
type: project
originSessionId: bc613a18-50d4-4456-83d1-ae746e1240e0
---
Every painkiller / "10x better" / "real pain" claim the brand agent writes must be grounded in source evidence. The primary evidence base is:

**Path:** `/home/jmsbpp/apps/liq-soldk-dev/notes/MACRO_RISKS/`

**Contents (as of 2026-04-15):**
- `MACRO_RISKS.md` (~415 lines) \u2014 main reality-check framework; proxy taxonomy for LocalInflation, InterestRateShock, TermsOfTrade, CapitalFlight, RemittanceCorridorRisk; historical precedents (USA 1985 and Brazil 1987 CPI futures); macro financial-contract settlement design.
- `INCOME_SETTLEMENT.md` (~213 lines) \u2014 income-settled derivative theory.
- `MACRO_DERIVATIVES.md` (~88 lines) \u2014 macro-derivative design patterns.
- `SIGNAL_TO_INDEX.md` (~58 lines) \u2014 signal-to-index construction for macro observables.
- `PRICE_SETTLEMENT.md`, `ECONOMETRICS_NOTES.md`, `MACRO_RISKS_CHECKPOINT.md` \u2014 supporting notes.

**Secondary evidence:**
- `/home/jmsbpp/apps/liq-soldk-dev/refs/macro-risk/` \u2014 primary-source papers and data.
- The Tier 1 feasibility spec at `contracts/docs/superpowers/specs/2026-04-14-inflation-mirror-tier1-feasibility-design.md` \u2014 per-channel literature verdicts for \u03c0 and C_remittance.
- `contracts/notebooks/ranPricing.ipynb` \u2014 instrument definition and CES basket application.

**How the Reality Checker uses it:**
- For every copy claim ("X loses Y% to inflation," "remittance corridors bleed Z% in value," "existing hedges fail because W"), cite a specific file and line range in the MACRO_RISKS folder.
- If no citation exists, the claim is either dropped or explicitly labeled as "directional, evidence pending" in the artifact.
- Claims that cite the MACRO_RISKS folder are marked PASS; uncited claims are BLOCK until grounded or softened.

**Why:** the positioning principle says painkiller not vitamin; painkiller is a claim about a real, verifiable pain. Marketing puff about pain the founder assumes but can't cite will fail under founder scrutiny, judge scrutiny, or first-user scrutiny. Grounding the copy in the existing research folder turns the pitch into evidence-backed narrative.

**How to apply:** the Reality Checker's prompt template lists this folder as required reading before any painkiller-adjacent claim is verified. If the folder moves or is extended, update this memory.
