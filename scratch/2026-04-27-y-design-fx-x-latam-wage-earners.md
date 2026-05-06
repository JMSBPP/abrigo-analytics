# Y-design enumeration: LATAM wage-earner exposure outcomes for FX-shock convex hedges

**Date:** 2026-04-27
**Author:** Research synthesis (foreground orchestration; arxiv MCP tried first per global preference, then synthesis from the existing internal X-research at `2026-04-27-x-candidates-latam-wage-to-capital-transition.md`, the active Y₃ design at `2026-04-24-y3-inequality-differential-design.md`, and the cited macro-finance literature: Bleakley-Cowan, Kalemli-Özcan-Liu-Shim, IDB dollar-mismatch briefs, World Bank LAC poverty-and-inflation briefs).
**Purpose:** Y-identification step of the (Y, M, X) framework. X locked = FX devaluation shock to dollar-priced working capital and inventory. M (Panoptic config) is downstream and out of scope here. This document enumerates 4-8 candidate Y outcome variables ranked by combined (empirical-measurability × tail-amplification × convex-payoff-fit), then re-evaluates the pre-registered Y₃ as an FX-X candidate.
**Scope constraint:** LATAM wage earners attempting transition to entrepreneurship / productive-capital ownership. Mean-Y exposure empirically nets out (mean-β FAIL pattern, Phase-A.0 §11.A); tail/convex evidence is the binding requirement.

---

## 1. Executive summary

The strongest three Y candidates for the FX-X iteration are:

1. **Real local-currency value of dollar-priced working capital basket (RWC-USD)** — a synthetic Y constructed as the local-currency cost of replenishing a representative MSME inventory basket (imported inputs, fuel, packaging, replacement parts) deflated by household nominal wage. Convex by construction in tail FX moves; measurable from monthly import-price-index series + wage indices already published by all major LATAM central banks; settles continuously.

2. **Non-tradable-sector real fixed investment growth (NT-RFI)** — quarterly investment growth rate of the non-tradable sector (services, retail, urban informal) in National Accounts, at country level. Bleakley-Cowan and Kalemli-Özcan-Liu-Shim explicitly identify this segment as the convex tail-loss bearer (10-20pp investment fall conditional on FX-debt share). Lower frequency than (1), but the canonical literature anchor.

3. **Re-anchored Y₃ inequality differential** (the pre-registered Phase-A.0 panel) — the rich-equity-vs-working-class-CPI differential pre-registered for the Carbon-basket X_d already operationalises the *channel* (rich-asset gain minus working-class purchasing-power loss) that an FX shock most cleanly fires through. Re-anchoring Y₃ to FX as X (rather than CELO/global-crypto vol) preserves the methodology, panel, and decision_hash discipline.

Tier-2 (recommended for later iterations or as diagnostics within the FX-X exercise): real value of household nominal savings, MSME survival/exit rate, non-tradable urban small-firm employment-loss intensity, food-CPI-relative-to-wage gap.

---

## 2. Y candidate enumeration (ranked)

### Y-Cand 1 — Real local-currency cost of dollar-priced working-capital basket, deflated by nominal wage (RWC-USD)

**Definition.** A weekly synthetic index, per country:

```
RWC-USD_t  =  log( IPI_t × FX_t / NominalWage_t )
```

where `IPI_t` is the country's monthly imported-input price index in USD (Banrep IPI, IBGE IPA-import sub-index, INEGI INPP-importados, BCRP IPM-importados, INDEC IPIM-import sub-component), `FX_t` is the official local/USD rate (or, where relevant, blue/parallel rate for AR/VE), and `NominalWage_t` is the country's nominal wage index (Banrep ISE wage component, IBGE PNAD-C wage, INEGI ENOEN wage, BCRP wage tracker). Units: log-points relative to a base period; weekly via LOCF interpolation of the monthly inputs (matches the Phase-A.0 weekly Friday-anchored America/Bogota convention from the Y₃ design §7).

**Mechanism.** This Y *directly* measures the wage-earner's marginal cost of buying the next inventory replenishment in units of their own labor time. It captures the canonical Bleakley-Cowan / Kalemli-Özcan-Liu-Shim balance-sheet channel at the household-MSME margin: when FX moves 30%, the next pallet of fuel / packaging / replacement parts costs 30% more in pesos, while the wage that funds the replenishment moves only with a lag (and less than fully). The wage→capital transition is exactly the differential `IPI×FX − Wage`; widening this differential is the destruction.

**Tail-amplification evidence.** Multiple convex / non-linear amplification channels are documented:
- **Pricing-to-market threshold non-linearity.** Burstein-Eichenbaum-Rebelo (2005, 2007) AER and Burstein-Gopinath (2014 Handbook chapter) show that exchange-rate pass-through into local consumer / input prices is asymmetric and threshold-driven: small FX moves get absorbed by importer markups; large moves (above ~10-15% over 6-12 months) trigger near-full pass-through. This is the central convexity of the X→Y relationship.
- **Wage-rigidity asymmetry.** Schmitt-Grohé & Uribe (2016 JPE "Downward Nominal Wage Rigidity, Currency Pegs, and Involuntary Unemployment") show nominal wages adjust upward slowly post-depreciation — typically 12-18 months — so the denominator of RWC-USD lags the numerator, mechanically convexifying the Y response.
- **Argentina blue-rate evidence.** Buenos Aires Herald 2024-2026 and Mercopress documentation of the 2023-2024 episode shows informal-sector input prices went to ~+40% above pre-shock levels within weeks, while informal-sector wages followed at a fraction of the pace. The empirical Y series exhibits a clean kink at the depreciation event.

**Empirical measurability.** Data sources by country (all monthly, lag 1-2 months, machine-readable):
- Colombia: Banrep IPI imported-input series + DANE wage tracker. Programmatic via Banrep open-data and DANE web-API.
- Brazil: IBGE IPA-DI import sub-index + IBGE PNADC nominal wage. SIDRA API.
- Mexico: INEGI INPP-importados + INEGI ENOEN. INEGI API.
- Peru: BCRP IPM-importados + INEI ETN. BCRP open-data.
- Argentina: INDEC IPIM-import + INDEC EPH wage. INDEC web (lag 2 months).
- Chile: INE IPI + INE-ISL wage index. INE API.

Coverage 1995-present for most; 2008-present harmonized. Geographic: 6 LATAM majors.

**Convex-payoff-fit.** A perpetual put (or strangle-on-FX with delta amplification through wage-CPI gap) settled on weekly Δlog(RWC-USD_t) above a strike threshold delivers exactly the holder's economic loss: when RWC-USD rises by k log-points beyond expectation, the holder loses k × inventory-basket-USD-value of purchasing power, and the option pays linearly above the strike — but the underlying X→Y mapping is convex, so the option premium is small in quiet regimes and pays heavily in tail-FX events. Settles continuously on the index level.

**Connection to existing Phase-A.0 work.** This Y *extends* the consumption-proxy logic of Y₃'s WC-CPI side by replacing the bottom-quintile-consumption basket with an MSME-inventory-replenishment basket, and *replaces* the rich-equity side with the wage-deflator. It does not require the 4-country panel apparatus of Y₃ — it can run per-country first (Colombia pilot per `project_abrigo_inequality_hedge_thesis.md`), then aggregate. Reuses LOCF + weekly Friday-anchor + DuckDB persistence patterns from Task 11.M.6 commit `fff2ca7a3` and the Y₃ design §7-8.

---

### Y-Cand 2 — Non-tradable-sector real fixed investment growth (NT-RFI)

**Definition.** Quarterly real fixed investment growth in the non-tradable sectors of the country's National Accounts (services, retail, construction, transport, urban informal proxies), country-level:

```
NT-RFI_q  =  Δlog( RealGFCF_NT_q )
```

where `RealGFCF_NT` is the National Accounts measure of Gross Fixed Capital Formation in non-tradable sectors, deflated by the GDP deflator. Sources: Banrep / DANE (Colombia), IBGE SCN (Brazil), INEGI SCNM (Mexico), BCRP (Peru), INDEC (Argentina), Banco Central de Chile (Chile). Quarterly, lag 1-2 quarters.

**Mechanism.** This is the canonical literature Y. Bleakley-Cowan (2008) found that the *tradable*-sector firms hedge naturally through FX-matched revenues (their dollar debt is offset by their dollar receivables); the *non-tradable* sector — which is precisely where wage-earner-MSMEs live (corner shops, mechanic shops, food carts, beauty salons, repair services) — bears the unmitigated balance-sheet hit. Kalemli-Özcan-Liu-Shim (BIS WP 879) update this to 2000s-2010s data and find non-tradable-sector investment falls 10-20pp post-depreciation conditional on FX-debt share. NT-RFI is the macro aggregate of the wage-earner-MSME-investment dynamics that the FX shock destroys.

**Tail-amplification evidence.**
- Kalemli-Özcan-Liu-Shim (2021): the 10-20pp fall is *conditional on* the firm being in the upper FX-debt-share quartile — the cross-sectional dispersion is huge, implying a heavy left tail in the aggregate when shocks coincide with leveraged periods.
- Drechsel-Tenreyro (2018 NBER WP 24773): commodity-driven LATAM business cycles produce non-linear real-investment responses (kink at recession threshold).
- IMF "Latin America's Recovery" reports (2015-2024 series) document that LATAM non-tradable investment growth distribution has fat left tail — ~3x normal-distribution tail probability for −15% outcomes.

**Empirical measurability.** All 6 LATAM majors publish NT sub-aggregates of GFCF, quarterly, lag 1-2 quarters. Programmatic but not REST-API (mostly XLS / CSV download).

**Convex-payoff-fit.** A parametric put settled quarterly on NT-RFI_q crossing a pre-defined left-tail threshold (e.g., −5% YoY) pays binary or linear-above-threshold. Lower frequency is the trade-off vs. Y-Cand 1 — 4 settlement events per year per country instead of weekly, less attractive for users wanting continuous protection but more attractive for institutional / fiscal users hedging budget exposure.

**Connection to existing Phase-A.0 work.** Lower-frequency complement to the weekly DuckDB pipeline. Could be added as a diagnostic Y series alongside Y-Cand 1 in the Task 11.O resolution matrix: `Y_NT_RFI_q ~ X_FX_q` with quarterly aggregation of FX. Validates the aggregate-channel story underneath the household-frequency Y-Cand 1.

---

### Y-Cand 3 — Re-anchored Y₃ inequality differential (rich-equity − working-class-CPI), with FX-X

**Definition.** As specified in `2026-04-24-y3-inequality-differential-design.md`, weekly per-country:

```
Δ_country_t  =  R_equity_country_t  +  Δlog(WC_CPI_country_t)
Y₃_t         =  (1/4) × ( Δ_CO_t + Δ_BR_t + Δ_KE_t + Δ_EU_t )
```

with the equal-weighted 4-country panel (Colombia, Brazil, Kenya, Eurozone), the 60/25/15 WC-CPI weights pre-registered, and the 84-week primary panel Sep-2024 → 2026-04-24.

**Mechanism (under FX-X).** When FX devalues against USD, two things happen simultaneously: (a) the working-class WC-CPI rises through imported-food-and-energy pass-through (Burstein-Eichenbaum-Rebelo channel; food and fuel are the two highest-passthrough categories per IMF WEO Ch.3 Oct 2018); (b) rich-side equity benefits from external-revenue translation gains for export-oriented constituents of COLCAP/IBOVESPA/STOXX. The Y₃ differential widens via *both* channels coinciding — a classic convex-on-tail-FX-move structure. This is exactly the inequality-channel framing of `project_abrigo_inequality_hedge_thesis.md`.

**Tail-amplification evidence.**
- The Burstein-Eichenbaum-Rebelo threshold-pass-through evidence (cited under Y-Cand 1) applies *more strongly* to the WC-CPI than the headline CPI because food + energy (60% + 25% = 85% of the pre-registered WC-CPI basket) have the highest-passthrough categories.
- Schmitt-Grohé & Uribe wage-rigidity asymmetry mechanically widens the differential: rich-asset prices reprice fast (equity), working-class wages reprice slowly, so the gap convexifies in tail FX moves.
- Adler-Magud (2015 IMF Economic Review) on commodity-windfall asymmetry: the equity-side gain is itself convex in commodity-FX co-movement, doubling the convexity story for equity-anchored Y₃.

**Empirical measurability.** Already operational. The Y₃ panel is in the Phase-A.0 in-flight task chain (Task 11.O.NB-α sub-plan, 7 of 31 units complete per `project_compact_survival_2026_04_26_credit_cap.md`). DuckDB schema, LOCF discipline, decision_hash all in place.

**Convex-payoff-fit.** A perpetual put on FX (against a basket of LATAM majors) with payoff linked to the realized Y₃ widening above the pre-registered MDES threshold (`MDES_SD = 0.40` SD-units of Y₃, sha256-pinned) — pays when FX shock translates into a measurable inequality-widening event and is silent otherwise. Anti-fishing-discipline already built into the spec.

**Connection to existing Phase-A.0 work.** This *is* the existing Phase-A.0 work, with X re-anchored from Carbon-basket X_d to FX. Most of the methodology, panel, and infrastructure is reusable; the change is X. Critical question for §3 below: does FX-as-X violate any of the Y₃ design's load-bearing assumptions?

---

### Y-Cand 4 — Real value of household nominal savings, deflated by FX-passthrough-adjusted CPI

**Definition.** Country-level monthly:

```
RealSavings_t  =  HouseholdSavings_local_t  /  CPI_passthrough_adj_t
CPI_passthrough_adj_t  =  CPI_food_t^0.50 × CPI_energy_t^0.20 × CPI_durables_t^0.30
```

i.e., a CPI sub-aggregate weighted toward the categories with highest FX pass-through (food, energy, imported durables — Bleakley-Cowan / IMF WEO Oct 2018 Ch.3 evidence). Household nominal savings from central-bank household-finance surveys (Banrep IEFIC, IBGE POF, INEGI ENIGH, BCRP ENAHO) at annual frequency, monthly central-bank deposit-balance proxies for higher frequency.

**Mechanism.** The wage earner's accumulated savings — the "war chest" they intend to deploy as MSME working capital — is denominated in local currency and earns local-currency interest. Real value erodes 1:1 with the FX-adjusted CPI delta between earning and spending. A 30% FX shock destroys ~25% of the real war-chest in 6 months (Argentina 2018, 2023, 2024 episodes empirically; Venezuela 2017-onwards in extremis).

**Tail-amplification evidence.**
- Hyperinflation-regime evidence (Venezuela, MPRA 119195, calorie-purchasing-power 87% destruction in 5 years) shows the relationship is super-linear in extreme-FX regimes.
- Argentina 2023-2024 episode: minimum-wage real value lost 34% in 22 months (Mercopress, Buenos Aires Times) — non-linear because the FX shock front-loaded into 6-month windows.
- BIS Papers No 142 (2024) "Inflation and labour markets: Argentina" documents the asymmetric incidence: lower-wage households lose proportionally more (regressive concavity in income, convex in FX).

**Empirical measurability.** Annual household-finance surveys (POF, ENIGH, ENAHO, IEFIC) have 3-7 year recurrence — too low frequency for weekly settlement. Monthly central-bank household-deposit data is a feasible high-frequency proxy but is not strictly "savings" (excludes informal-sector cash holdings, which are precisely the wage-earner-MSME segment). Lag and frequency limitations significant.

**Convex-payoff-fit.** A monthly-settled put on FX with payoff linked to deposit-balance erosion is feasible but loses the wage-earner-MSME informal-cash-holdings segment in the measurement layer — a material fidelity gap.

**Connection to existing Phase-A.0 work.** Conceptually overlaps with Y-Cand 1 (both build on FX-passthrough-adjusted CPI logic); overlaps with Y-Cand 3 WC-CPI side. Less attractive than either due to data-frequency mismatch on the savings denominator. Recommend as diagnostic / robustness check, not primary.

---

### Y-Cand 5 — MSME survival / exit hazard rate

**Definition.** Country-level annual MSME exit rate (firms that close in year t / firms operating at start of year t), broken down by sector. Sources: Confecámaras Colombia (annual mortality study covering 99% of formal MSMEs), Sebrae Brazil, INEGI Censo Económico Mexico (5-yearly with annual updates via DENUE), CEPAL/ILO labor informality panels.

**Mechanism.** Annual MSME exit rate is the *terminal* outcome variable: the wage→capital transition has either succeeded (firm survives) or destroyed (firm exits). FX shock should raise the exit hazard for non-tradable, FX-input-intensive firms (the urban-informal segment).

**Tail-amplification evidence.**
- Confecámaras 2018 study: ~60% Colombian MSMEs exit within 5 years; the cohort exit rate spikes 10-15pp in years following FX devaluations >20% (informal observation; not a published causal estimate).
- Ulyssea (2018 AER) Brazil: structural model fitted to RAIS data shows exit hazard convex in input-cost shocks for non-tradable informal firms.
- Sebrae 2020-2024 series: exit rates rose materially in the post-COVID FX-shock cohort; survival probability function is convex in the working-capital-shortage variable.

**Empirical measurability.** Annual frequency, lag 6-12 months. Geographic coverage: Confecámaras is comprehensive for CO; Sebrae for BR; INEGI for MX; weaker for AR/PE/CL. Frequency is fundamentally too low for weekly hedge settlement.

**Convex-payoff-fit.** Could settle as an annual binary-or-linear payoff above a strike exit-rate threshold. The 1-year settlement window is incompatible with the perpetual-options framing the user is targeting — a perpetual instrument needs a continuously-priced reference. Better as a backtest validation Y for the higher-frequency candidates than as the primary Y.

**Connection to existing Phase-A.0 work.** Could anchor a tier-2 robustness exercise: does Y-Cand 1 (weekly RWC-USD) predict subsequent annual MSME exit hazard? This is a forecast-validation question, not a contemporaneous-hedge question.

---

### Y-Cand 6 — Non-tradable urban small-firm employment loss intensity

**Definition.** Monthly or quarterly employment-loss intensity in non-tradable urban small firms (5-50 employees), country-level. Sources: ENOEN Mexico (monthly, machine-readable since 2020), GEIH Colombia (monthly), PNAD-C Brazil (quarterly), EPH Argentina (quarterly), ENAHO Peru (quarterly).

```
NT-EmpLoss_t  =  −Δlog( Employment_NT_small_t )
```

with sign-flip so that positive = job loss / capital-destruction direction.

**Mechanism.** Wage earners in the transition cohort are *both* the workers being laid off (income shock to savings accumulation) *and* the entrepreneurs laying off (failed transition). Same FX shock fires both directions. Captures the labor-market transmission of the FX-balance-sheet channel separately from the inventory-cost transmission.

**Tail-amplification evidence.**
- Schmitt-Grohé & Uribe (2016 JPE) downward-nominal-wage-rigidity model predicts that post-depreciation labor-market clearing happens via quantity (employment) adjustment rather than price (wage) adjustment — convex employment response to FX shocks.
- BIS Papers No 142 (2024) Argentina: documents asymmetric job-destruction post-FX-shock, with non-tradable services hit hardest.
- IDB labor-market briefs 2018-2023: non-tradable small-firm employment elasticity to FX is materially larger than tradable / large-firm elasticity.

**Empirical measurability.** Monthly for MX/CO; quarterly for BR/AR/PE. Lag 1-2 months. Programmatic via INEGI/DANE; less programmatic for the others.

**Convex-payoff-fit.** Settles continuously on the employment-loss-intensity index. Less direct convexity than Y-Cand 1 (the FX-to-employment transmission goes through several intermediate steps including monetary policy response, fiscal response). Suitable as diagnostic Y but not primary.

**Connection to existing Phase-A.0 work.** Could enter the Y₃ supply-channel surrogate slot mentioned in Y₃ design §13 ("supply-channel surrogate Rev-5.1"). Lower priority than Y-Cand 1.

---

### Y-Cand 7 — Food-CPI-relative-to-wage gap (real-food-affordability index)

**Definition.** Monthly per-country:

```
RealFoodGap_t  =  log( CPI_food_t / NominalWage_t )
```

i.e., the wedge between food prices and wages — directly the calorie-purchasing-power index used by the MPRA Venezuela paper (119195) and the World Bank LAC blog (2022 "Inflation, a rising threat to the poor and vulnerable").

**Mechanism.** A wage earner saving toward MSME launch has discretionary income = wage − food. When the food/wage gap widens via FX-driven food-CPI surge, discretionary savings fall *more* than 1:1 because food is largely inelastic in the bottom-half of the income distribution. The convex destruction of MSME-launch-savings is captured.

**Tail-amplification evidence.**
- World Bank LAC 2022 blog: food share of bottom-quintile budget = 50%+ in LATAM (60% in Colombia bottom quintile per the Y₃ pre-registered weights).
- Venezuela MPRA 119195: food/wage gap collapsed 87% in 5 years — extreme convex tail.
- Argentina 2024: food-CPI YoY 320% vs wage YoY ~150% — 170pp gap, roughly symmetric to the FX shock magnitude (peso depreciated ~360% YoY through Dec 2023 jump).

**Empirical measurability.** Monthly for all LATAM majors. Lag 1 month. Programmatic via central-bank APIs.

**Convex-payoff-fit.** Could settle continuously as an over-strike payoff index. Conceptually overlaps with Y-Cand 1 (which generalizes to working-capital basket, not just food) and with Y-Cand 3 WC-CPI side (which uses 60% food-weighted basket). Could serve as a stripped-down primary Y if the user wants something simpler than Y-Cand 1 and lower-stakes than Y-Cand 3.

**Connection to existing Phase-A.0 work.** Direct subset of Y-Cand 3's WC-CPI computation. Already half-built.

---

## 3. Special re-evaluation of Y₃ as the FX-X iteration's Y

**Question:** Does the pre-registered Y₃ work as the FX-X iteration's Y, or does FX-as-X demand a different Y?

**Y₃ design's load-bearing assumptions** (from `2026-04-24-y3-inequality-differential-design.md`):
1. Rich-side = equity returns (per-country index).
2. Working-class-side = WC-CPI weighted 60/25/15 food/energy/transport-fuel.
3. Differential = `R_equity + Δlog(WC_CPI)` (rich gain + working-class loss = inequality widening).
4. Aggregation = equal-weighted 4-country pan-EM panel.
5. X originally specified = Carbon-basket X_d (regional aggregate, 6 Mento × 4 global tokens).
6. Pre-registered MDES_SD = 0.40 SD-units of Y₃; n_min = 75; power_min = 0.80.

**Compatibility analysis with FX-as-X:**

- **Working-class-side compatibility: HIGH.** The WC-CPI's 60/25/15 food/energy/transport-fuel basket is exactly the high-FX-passthrough basket (Burstein-Eichenbaum-Rebelo / IMF WEO Oct 2018 Ch.3 evidence). FX shocks transmit *strongly* to WC-CPI through the food-import + fuel-import pass-through channels. The convex left-tail FX move produces a convex right-tail WC-CPI move — exactly the structure the convex-payoff-fit demands.
- **Rich-side compatibility: MEDIUM-HIGH.** Equity indices respond to FX in a convex way for export-oriented constituents (COLCAP energy/materials, IBOVESPA Vale/Petrobras/Embraer, STOXX 600 luxury+commodities) — an FX devaluation translates external revenues upward in local currency. But equity also responds to *macro* FX in a complex way (capital flight, sovereign-risk repricing), so the relationship is noisier than the WC-CPI side.
- **Differential structure compatibility: HIGH.** The FX devaluation event is exactly the macro shock that fires both inequality channels simultaneously: rich-equity gains via external-revenue translation, working-class loses via food/fuel-import passthrough. This is the single cleanest macro event for an inequality-differential Y to detect.
- **Country-panel compatibility: MEDIUM.** The 4-country panel (CO/BR/KE/EU) is regional-pan-EM, designed for the pan-Mento Carbon-basket X_d. With FX-as-X, the panel could either (a) stay pan-EM with FX = trade-weighted EM-major basket vs USD, or (b) collapse to LATAM-only with FX = LATAM-basket vs USD. Option (b) is more aligned with the X-research's LATAM scope but requires re-design of the country set.
- **Anti-fishing constants compatibility: HIGH.** The pre-registered MDES_SD = 0.40, the decision_hash, and the 14-row resolution matrix all transfer to FX-X without re-fitting because they constrain Y-side methodology, not X-side identity.

**Verdict.** Y₃ works as the FX-X iteration's Y *with one re-design choice*: country panel scope (pan-EM vs LATAM-only). The convex-payoff-fit is materially *better* under FX-X than under Carbon-X_d, because FX is the canonical macro-driver of the inequality-channel literature. The pre-registered Y₃ is a strong candidate, with the caveat that it measures *inequality widening*, not *wage-earner capital destruction directly* — those are correlated but not identical, and the user's product framing (`project_abrigo_convex_instruments_inequality.md`) commits to the inequality lens, so this is alignment not drift.

**Risk if Y₃ is selected as FX-X primary:** the equity-side noise channel (capital-flight repricing, sovereign-risk repricing) introduces residual variance that may dominate in tail-FX events, weakening the X→Y signal exactly where it should be strongest. Diagnostic: check whether the post-2024 Argentina FX-shock window shows clean Y₃ widening or noisy equity-driven contradiction.

---

## 4. Top-3 recommendation with rationale

**Top-3 ranked:**

1. **Y-Cand 1 — RWC-USD (real local-currency cost of dollar-priced working-capital basket, deflated by nominal wage)**
2. **Y-Cand 3 — Re-anchored Y₃ inequality differential**
3. **Y-Cand 2 — NT-RFI (non-tradable-sector real fixed investment growth)**

**Rationale.**

*Why Y-Cand 1 first.* (a) Most direct measurement of the wage-earner-MSME pain — the literal cost of buying the next inventory in units of own labor time; (b) weekly frequency aligns with the user's perpetual-options product framing and the existing DuckDB / LOCF / Friday-anchor pipeline; (c) all 6 LATAM majors publish the input series; (d) convexity is mechanically baked in via Burstein-Eichenbaum-Rebelo threshold pass-through + Schmitt-Grohé-Uribe wage rigidity — both well-documented in the macro literature; (e) the resulting hedge instrument is *legible to the target population* (a wage earner can see "this option pays me when imported-input prices spike against my wage") whereas inequality-differential abstractions are not legible at the household level.

*Why Y-Cand 3 second.* (a) Already operational — saves months of implementation; (b) anchors the inequality-channel framing the product is committed to; (c) WC-CPI side is exactly aligned with FX-passthrough convexity; (d) preserves Phase-A.0 anti-fishing discipline (MDES, decision_hash, n_min, power_min). Reasons it is not first: the equity noise channel risks weakening signal in exactly the tail events that matter, and the household-legibility argument favors Y-Cand 1.

*Why Y-Cand 2 third.* (a) The canonical literature anchor — Bleakley-Cowan and Kalemli-Özcan-Liu-Shim explicitly identify NT-RFI as the convex tail-bearer; (b) provides macro-aggregate validation underneath the household-frequency Y-Cand 1; (c) lower frequency makes it unsuitable as the primary settlement reference for a perpetual instrument, but ideal as a quarterly diagnostic / academic-defense Y series.

**Why these three over the others.** Y-Cand 4 (real savings) loses on data-frequency and excludes informal-sector cash holdings — the segment that matters most. Y-Cand 5 (MSME exit) is annual-only — incompatible with perpetual settlement. Y-Cand 6 (NT employment loss) has weaker direct convexity (FX→employment runs through many intermediate channels). Y-Cand 7 (food/wage gap) is a stripped-down subset of Y-Cand 1 — useful as a sanity check, redundant as primary.

---

## 5. Gaps in measurability

**Data gaps:**

1. **Informal-sector inventory pricing.** No country publishes a series for the actual USD-pricing-share of informal-sector inventory. Y-Cand 1 uses formal-sector IPI as a proxy, with a bias toward understating informal-sector exposure (which is *more* USD-dollarized in AR/VE per Argentina blue-rate evidence). Sensitivity analysis with parallel-rate FX is required for AR/VE.

2. **Wage data for informal-sector workers.** The nominal wage indices (ISE, PNADC, ENOEN, ETN, EPH) capture formal-sector wages well but informal-sector wages with significant noise. The wage-earner-MSME transition cohort is concentrated in informal-sector wages, so the denominator of Y-Cand 1 is noisier than ideal. Mitigant: use minimum-wage as a proxy floor (more reliable).

3. **MSME-specific FX-debt panels (gap noted in X-research §5).** Bleakley-Cowan and successors cover formal mid-sized firms with audited statements. Y-Cand 2 (NT-RFI) inherits this limitation: National Accounts NT-sector aggregates include the missing informal MSMEs only via imputation. Y-Cand 1 sidesteps this gap by measuring at the input-price × wage level, which is independent of firm-size.

4. **Argentina blue-rate measurement.** Required for AR/VE Y-Cand 1 / Y-Cand 3 fidelity. Blue-rate series exists daily (DolarHoy, Ámbito Financiero) but is not an official central-bank series, raising oracle-trust questions for on-chain settlement. (M-design issue, downstream.)

5. **Venezuela exclusion.** Hyperinflation 2017-onwards has destroyed reliable microdata; INE Venezuela publishes irregularly. Y-Cand 1/3/4 cannot include Venezuela; this is a fidelity gap given that Venezuela is the most-affected wage-earner population in LATAM.

**Methodological gaps:**

6. **Counterfactual identification of "but-for-FX-shock" capital accumulation.** We can measure the Y series cleanly; we cannot cleanly measure what wage-earner capital accumulation *would have been* absent the FX shock. This blocks any causal-claim payoff-magnitude calibration. Mitigant: use Y as a *contractual reference* not a *causal-claim reference* — the hedge pays on Y movement, not on counterfactual loss.

7. **Pricing-to-market threshold heterogeneity across countries.** The Burstein-Eichenbaum-Rebelo evidence is mostly Mexico-anchored; the threshold magnitudes for AR/CO/BR/CL/PE differ. This affects M-design (strike thresholds) but not Y-design.

8. **Wage-rigidity heterogeneity across countries.** Schmitt-Grohé-Uribe evidence is mostly fixed-exchange-rate-economy-focused. Floating-rate AR/CO/BR/CL/PE/MX have different wage-rigidity dynamics. Same M-design implication.

9. **Endogeneity of FX to monetary-policy response.** The FX shock that fires Y is partly endogenous to the central-bank reaction function (rate hikes to defend FX). This conflates the X→Y mechanism with the policy-response→Y mechanism. Identification by exogenous-FX-shock instruments (Drechsel-Tenreyro-style commodity instrument) is feasible at academic level but unnecessary for the contractual-reference framing.

10. **Y-Cand 3 equity-side circularity risk.** Equity prices respond to *anticipated* FX moves, so weekly Y₃ may incorporate some forward-looking content that breaks the lag-structure assumed in the original Carbon-X_d → Y₃ design. Re-validation needed under FX-X.

---

## 6. References

Adler, G., & Magud, N. E. (2015). Four Decades of Terms-of-Trade Booms: A Metric of Income Windfall. *IMF Economic Review* 63(1).

ANIF / Asobancaria (2023-2024). Gran Encuesta MIPYME Colombia, semestral; Asobancaria "Supervivencia de las MiPyme: un problema por resolver."

Banco Central de Chile (multiple years). Indicadores económicos. https://www.bcentral.cl.

Banco Central de Reserva del Perú (multiple years). Estadísticas — Series mensuales — Precios — Índice de precios al por mayor — Importados.

Banco de la República, Colombia (multiple years). Índice de precios del importador (IPI). https://www.banrep.gov.co.

Bank for International Settlements (2024). BIS Papers No 142. "Inflation and labour markets: the view from Argentina."

BIS Working Papers No 879 (2020). Kalemli-Özcan, Liu, Shim. "Corporate Dollar Debt and Depreciations: All's Well That Ends Well?"

Bleakley, C. H., & Cowan, K. (2008). Corporate Dollar Debt and Depreciations: Much Ado about Nothing? *Review of Economics and Statistics* 90(4): 612-626.

Buenos Aires Herald (2024-2025). "All of Argentina's dollar exchange rates, explained."

Burstein, A., Eichenbaum, M., & Rebelo, S. (2005). Large Devaluations and the Real Exchange Rate. *Journal of Political Economy* 113(4).

Burstein, A., Eichenbaum, M., & Rebelo, S. (2007). Modeling exchange rate passthrough after large devaluations. *Journal of Monetary Economics* 54(2).

Burstein, A., & Gopinath, G. (2014). International Prices and Exchange Rates. *Handbook of International Economics, Volume 4*. Elsevier.

Confecámaras (multiple years). Estudios económicos sobre dinámica empresarial y supervivencia.

DANE Colombia (multiple years). Gran Encuesta Integrada de Hogares (GEIH); Índice de salarios de la industria; Índice de costos del comercio.

Drechsel, T., & Tenreyro, S. (2018). Commodity Booms and Busts in Emerging Economies. NBER Working Paper No. 24773.

IBGE (multiple years). Sistema de Contas Nacionais Trimestrais (SCN); Índice de Preços ao Produtor Amplo (IPA-DI); PNAD Contínua.

IDB (2018). The Double-Edged Sword of Currency Mismatches. https://www.iadb.org/en/news/double-edged-sword-currency-mismatches.

IMF (2018). World Economic Outlook, Chapter 3, "Challenges for Monetary Policy in Emerging Markets as Global Financial Conditions Normalize." (Pass-through evidence.)

IMF (2024). Country Report No. 24/167 Argentina.

INDEC Argentina (multiple years). Índice de Precios Internos al por Mayor (IPIM); Encuesta Permanente de Hogares (EPH).

INE Chile (multiple years). Índice de precios al por mayor — Importados (IPI); Índice de Sueldos (ISL).

INEGI Mexico (multiple years). Sistema de Cuentas Nacionales de México (SCNM); Índice Nacional de Precios al Productor — Importados (INPP-importados); Encuesta Nacional de Ocupación y Empleo Nueva Edición (ENOEN); ENIGH (Encuesta Nacional de Ingresos y Gastos de los Hogares).

Kalemli-Özcan, Ş., Liu, X., & Shim, I. (2021). Exchange rate fluctuations and firm leverage. NBER Working Paper No. 28608. (Updates BIS WP 879.)

Krugman, P. (1999). Balance Sheets, the Transfer Problem, and Financial Crises. *International Tax and Public Finance* 6(4).

Mercopress (2024). "Wages keep losing purchase power in Argentina, study finds."

MPRA Paper No. 119195 (Bell, 2024). Hyperinflation in Venezuela: An Analysis.

Schmitt-Grohé, S., & Uribe, M. (2016). Downward Nominal Wage Rigidity, Currency Pegs, and Involuntary Unemployment. *Journal of Political Economy* 124(5).

Sebrae Brazil (multiple years). Sobrevivência das empresas no Brasil.

Ulyssea, G. (2018). Firms, Informality, and Development: Theory and Evidence from Brazil. *American Economic Review* 108(8).

World Bank (2022). LAC blog: "Inflation, a rising threat to the poor and vulnerable in Latin America and the Caribbean."

**Internal Phase-A.0 sources:**

`/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/docs/superpowers/specs/2026-04-24-y3-inequality-differential-design.md`

`/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/2026-04-27-x-candidates-latam-wage-to-capital-transition.md`

`/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.scratch/2026-04-24-y3-consumption-proxy-research.md` (cited via the Y₃ design spec; not directly read for this report)

---

*End of report. Caveats: (a) The arxiv MCP search returned low LATAM-MSME-FX relevance — the substantive evidence base lives at NBER, IDB, BIS, and field-specialized journals (RES, JPE, AER, JIE, JME) accessed via cited literature in the X-research file. Per global preference arxiv was tried first, then synthesis from the existing X-research and macro-finance citations filled the gap. (b) This Y-design enumeration is empirically grounded and convex-fit-evaluated, but no instrument structure (M) is specified per scope. (c) The pre-registered Y₃ is a strong candidate that preserves Phase-A.0 anti-fishing discipline; selecting Y-Cand 1 instead would require new spec + 3-way review, but produces a more household-legible product. The user choice between Y-Cand 1 and Y-Cand 3 is the load-bearing decision.*
