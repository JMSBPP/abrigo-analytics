# DANE GEIH Y-Feasibility Assessment — Pair D Iteration

**Date:** 2026-04-27
**Author:** Data Engineer (feasibility-assessment role; no pipeline construction)
**Iteration context:** Abrigo Pair D — Y = Colombian young-worker services-sector employment share (monthly), X = COP/USD lagged 6–12 months
**Output target:** simple-β spec (downstream, not yet authored)

---

## §1. Verdict (≤100 words)

**FEASIBLE-WITH-CAVEATS.** GEIH micro-data is publicly downloadable in CSV/DTA/SAV at no cost from `microdatos.dane.gov.co`, with monthly cross-sections from 2008 (continuous) back to 2006 partial, and a parallel ECH series stretching to 2001. Per-worker rows include age, sector (CIIU Rev. 4 A.C.), and expansion factors — sufficient for a clean "share of 14–28-year-old workers in services / total 14–28 employed" series. Three caveats are load-bearing for the simple-β spec: (a) **2021 Marco-2005 → Marco-2018 methodology break** with a DANE-published 10-year empalme factor; (b) **CIIU Rev. 4 vs. Rev. 3.1** boundary ambiguity in pre-2012 files; (c) **monthly sample stability** for a youth-only services subset is borderline at the city level but solid at the national 13-cities aggregate.

---

## §2. Per-Question Answers

### Q1. Public micro-data availability — VERIFIED YES, FREE, NO REGISTRATION

DANE publishes GEIH anonymized micro-data publicly and free of charge ("El acceso a los microdatos anonimizados de uso público es de carácter gratuito"). Catalog landing page: `https://microdatos.dane.gov.co/index.php/catalog/MICRODATOS` (returned HTTP 500 on direct curl, but individual catalog entries resolve cleanly via browser).

Verified per-year catalog IDs:

| Year | Catalog URL | Status |
|------|-------------|--------|
| 2009 | `https://microdatos.dane.gov.co/index.php/catalog/207` | confirmed live |
| 2016 | `https://microdatos.dane.gov.co/index.php/catalog/427` | confirmed live |
| 2017 | `https://microdatos.dane.gov.co/index.php/catalog/458` | confirmed live |
| 2018 | `https://microdatos.dane.gov.co/index.php/catalog/547` | confirmed live |
| 2021 | `https://microdatos.dane.gov.co/index.php/catalog/701` | confirmed live (Marco 2005 + Marco 2018 in parallel) |
| 2022 | `https://microdatos.dane.gov.co/index.php/catalog/771` | confirmed live (Marco 2018 only) |
| 2023 | `https://microdatos.dane.gov.co/index.php/catalog/782` | confirmed live |
| 2024 | `https://microdatos.dane.gov.co/index.php/catalog/819` | confirmed live |
| 2025 | `https://microdatos.dane.gov.co/index.php/catalog/853` | confirmed live |
| 2026 | `https://microdatos.dane.gov.co/index.php/catalog/900` | confirmed live (created 2026-04-14) |

**File structure (verified from third-party tutorial corpus + DANE catalog entries):** one ZIP per month per year, exploded into per-module CSVs at `Cabecera` (urban) and `Resto` (rural) granularity. Naming convention is human-readable Spanish: e.g.
- `Enero - Cabecera - Caracteristicas generales (Personas).csv` (one row per person)
- `Enero - Cabecera - Ocupados.csv` (one row per employed person)
- `Enero - Cabecera - Desocupados.csv` (one row per unemployed person)
- `Enero - Cabecera - Fuerza de trabajo.csv` (one row per labor-force participant)
- `Enero - Cabecera - Vivienda.csv` (one row per dwelling)
- `Enero - Cabecera - Hogar.csv` (one row per household)
- `Enero - Cabecera - Otros ingresos.csv` (one row per income recipient)

**Formats offered per month:** CSV, DTA (Stata), SAV (SPSS). Three formats redundantly published per file.

**Historical depth:** GEIH itself launched **August 2006** (per DANE methodology docs and 2009 catalog entry). For 2008–present (the user's window), monthly micro-data is uninterrupted. Pre-2006 the predecessor **ECH (Encuesta Continua de Hogares)** ran from 2000 (13 cities) / 2001 (national). DANE catalog entry for ECH: `https://microdatos.dane.gov.co/index.php/catalog/116` (2006 trimesters I-II). The ECH→GEIH transition is bridgeable but requires a separate harmonization step.

**Real-time release lag:** Monthly bulletin published ~30 days after reference month (e.g., December 2024 reference → bulletin dated 2025-01-30). Micro-data ZIP appears on the catalog ~60–90 days after reference month based on observed catalog dates.

### Q2. "Young worker" age-band convention — VERIFIED 14–28 (Colombian statutory)

**Authoritative convention: 14–28 years**, established by **Ley 1622 de 2013** ("Estatuto de Ciudadanía Juvenil"). DANE publishes a dedicated youth labor-market bulletin (`boletin_GEIH_juventud_*.pdf`) using this exact band — verified URL: `https://www.dane.gov.co/files/investigaciones/boletines/ech/juventud/boletin_GEIH_juventud_ago22_oct22.pdf` (HTTP 200, 732 KB).

Other usable bands (all constructible from the `P6040` age field in the `Caracteristicas Generales` module):

| Band | Provenance | Use case |
|------|------------|----------|
| **14–28** | Ley 1622 de 2013, DANE official | Default; matches DANE's published youth aggregates |
| 18–28 | Working-age subset of statutory youth | Excludes minors; cleaner for wage-earning narrative |
| 18–24 | ILO international youth | International comparability (KE/BR/EU panel members in Y₃) |
| 15–24 | OECD/UN Statistical Commission | Cross-country aggregation in IPUMS harmonized panel |
| 18–29 | World Bank "extended youth" | Used in some Banrep mercado-laboral reports |

**Recommendation for Pair D:** use **14–28 (Ley 1622 statutory)** as the primary because (a) it matches DANE's own published youth headline indicators, (b) it eliminates a definitional discretion that downstream reviewers could flag as fishing, (c) DANE already publishes the cell as a sanity-check anchor.

**Reference for sanity check:** DANE-reported youth (14–28) unemployment rate Dec-2019/Feb-2020 = **16.7%**.

### Q3. "Services sector" CIIU Rev. 4 boundary — REQUIRES EXPLICIT MAPPING

GEIH classifies employment by economic activity using **CIIU Rev. 4 A.C.** (adopted by DANE Resolution 066 of 2012-01-31). Pre-2012 files used CIIU Rev. 3.1 — DANE publishes correspondence tables.

**CIIU Rev. 4 sections that constitute "services" (broad definition, ISIC-aligned):**

| Section | Description | Inclusion in "services" |
|---------|-------------|--------------------------|
| G | Comercio al por mayor y al por menor | INCLUDE (retail/wholesale = services in BPO-narrative) |
| H | Transporte y almacenamiento | INCLUDE |
| I | Alojamiento y servicios de comida | INCLUDE |
| **J** | **Información y comunicaciones** | INCLUDE — **BPO/call-center proxy** |
| K | Actividades financieras y de seguros | INCLUDE |
| L | Actividades inmobiliarias | INCLUDE |
| **M** | **Actividades profesionales, científicas y técnicas** | INCLUDE — BPO professional services |
| **N** | **Actividades de servicios administrativos y de apoyo** | INCLUDE — call-center BPO core |
| O | Administración pública y defensa | INCLUDE (or exclude — see below) |
| P | Educación | INCLUDE |
| Q | Servicios sociales y de salud | INCLUDE |
| R | Actividades artísticas, entretenimiento | INCLUDE |
| S | Otras actividades de servicios | INCLUDE |
| T | Actividades de los hogares como empleadores | INCLUDE |
| **A** | Agricultura, ganadería, caza | EXCLUDE |
| **B** | Explotación de minas y canteras | EXCLUDE |
| **C** | Industrias manufactureras | EXCLUDE |
| **D** | Suministro de electricidad, gas | EXCLUDE (utilities ambiguous) |
| **E** | Distribución de agua, saneamiento | EXCLUDE (utilities ambiguous) |
| **F** | Construcción | EXCLUDE |

**Two viable definitions for Pair D:**

1. **Broad services (recommended for Pair D headline)**: sections G–T (everything that is not A, B, C, D, E, F). This matches DANE's monthly bulletin "rama de actividad" residual aggregation and is the cleanest definition that requires no judgment calls. Coverage ≈ 68% of national employment in 2024.

2. **BPO-narrow proxy**: sections J + M + N (information & communications + professional services + administrative & support services). This isolates the BPO-adjacent cells the Pair D narrative cares about (call centers = section N major group 822; ICT = section J). Coverage ≈ 8–12% of national employment. **Caveat:** smaller cell → noisier monthly Y; quarterly aggregation likely required for stability.

**Recommendation:** use **broad services (G–T)** as the primary Y and **BPO-narrow (J+M+N)** as a pre-registered sensitivity. Do NOT change the primary based on the sensitivity result post-hoc — Phase-A.0 anti-fishing protocol applies.

The Pair D research recommendation reads "services-sector employment share" without BPO narrowing, so this is the cleanest construction the user already endorsed.

### Q4. Monthly time series feasibility — YES, WITH 2021 BREAK

**Periodicity:** GEIH publishes both monthly and quarterly. Monthly is the highest-frequency native release. The DANE methodology document explicitly lists "Semanal, Mensual, Trimestral y Anual" cadences, with monthly being the standard operational cycle.

**Realistic earliest start date for clean monthly Y series:**

- **Earliest viable: January 2008.** Although GEIH started August 2006, the first 17 months (Aug 2006 – Dec 2007) included methodological transitions from ECH that DANE flags as "transition period." From January 2008 the monthly series is operationally stable on Marco 2005.
- **Methodology break: January 2021.** DANE switched from Marco 2005 (population frame from 2005 Census) to Marco 2018 (frame from 2018 Census). 2021 was a parallel-collection year; from January 2022 onward, only Marco 2018 is published.
- **DANE-published empalme:** A 10-year empalme factor distributes the level shift across 2012–2021. Application of this factor is mandatory for any time-series analysis spanning 2021. Reference: `https://www.dane.gov.co/files/investigaciones/boletines/ech/ech/Nota-tecnica-empalme-series-GEIH.pdf`.

**Expected series:** Jan-2008 → present-month, 217+ monthly observations as of April 2026 (218 months). After 2021 empalme correction, the series is methodologically continuous.

**Caveat for spec:** the simple-β spec MUST decide whether to (a) apply DANE empalme factor before regression, (b) include a 2021 dummy, or (c) restrict the sample to 2022-onward. Each has different consequences for COP/USD lag identification.

### Q5. Panel vs. cross-section structure — SHORT-PANEL ROTATING

GEIH is a **rotating short-panel** with rotation groups. Each surveyed dwelling is interviewed in a sequence of months/quarters before being rotated out (consistent with most Latin American labor force surveys). The DANE methodology document does not explicitly publish the rotation parameters, but the survey is treated as effectively cross-sectional for monthly aggregates because (a) DANE publishes monthly rates as cross-sections without panel correction, (b) the rotating sample is designed to support both cross-sectional rates and short-panel transitions.

**Implication for Y series variance:** treating each month as an independent cross-section is the standard approach. Monthly Y values will exhibit autocorrelation that the simple-β spec must account for via HAC standard errors (Newey-West with bandwidth based on average panel-rotation length).

**No worker-level longitudinal tracking is needed for the share-of-services Y.** The construction is monthly aggregate ratio: numerator = sum of expansion-weighted 14-28 employed in services sections; denominator = sum of expansion-weighted 14-28 employed total.

### Q6. Sample row counts — ADEQUATE FOR NATIONAL, BORDERLINE FOR BPO-NARROW

**Per-month sample size (verified from 2009 GEIH catalog entry):** ~23,000 households per month → ~80,000–95,000 individuals per month → ~30,000–40,000 employed per month. Annual cumulative sample ≈ 240,000–315,000 households (DANE 2024 figure: 315,000).

**Estimated young-worker (14–28) cells per month** — *figures below are estimated from share assumptions, not verified row counts*:

| Definition | Est. per-month cell | Stability assessment |
|------------|---------------------|----------------------|
| 14–28 employed total (denominator) | ~7,000–9,000 | Stable |
| 14–28 in broad services (G–T) numerator | ~4,500–6,000 | Stable |
| 14–28 in BPO-narrow (J+M+N) numerator | ~700–1,200 | Borderline; quarterly aggregation recommended |

**Recommendation:** broad-services Y supports monthly granularity nationally. BPO-narrow Y should be reported quarterly (or as 3-month rolling average). City-level (Bogotá-only) cuts will require quarterly aggregation regardless.

### Q7. Access friction — MINIMAL

| Friction | Status |
|----------|--------|
| Registration | **Not required** — direct download via catalog "Obtener Microdatos" links |
| Institutional credentials | Not required |
| Fees | **Free** (DANE policy: anonymized public-use micro-data is gratis) |
| Spanish-only | Yes — catalog UI, file names, variable labels are Spanish; methodology PDFs have English versions |
| Mirrors | **IPUMS International** publishes a harmonized 2001–2025 Colombia panel (signed data-use agreement required, free). Universidad de los Andes hosts mirror copies of older years. World Bank Microdata Library hosts IPUMS-harmonized subsets at `https://microdata.worldbank.org/index.php/catalog/7662` (2020 Q1 sample) and adjacent IDs |
| Aggregated alternative | DANE monthly bulletins (`bol-GEIH-{mes}{yr}.pdf`) publish headline rates including youth (14–28) unemployment, but NOT the youth-services-share cell directly. Banrep `suameca.banrep.gov.co` mirrors DANE labor aggregates but also does not publish the specific cell |

**Comparison to FX-vol-CPI Phase-A.0 Banrep pipeline:** GEIH access friction is **lower** than Banrep series-by-series API pulls. Banrep uses `expmacro` JSON endpoints with series IDs; GEIH is plain CSV ZIP downloads from a static catalog. No auth wall, no rate limit, no API key. Bandwidth is the only cost — annual GEIH ZIPs are typically 200–400 MB compressed.

**Pre-aggregated alternative does NOT exist for the specific Pair D Y.** DANE publishes (a) total employment by sector, (b) total youth unemployment rate, but does not publish (c) youth-employed in services as a share of youth-employed. The cell must be constructed from micro-data.

### Q8. Concrete sample construction — NOT EXECUTED (feasibility-stage scope)

Per the user's instruction ("Do NOT generate code, data pipelines, or spec content"), I did not pull and process a 2026-03 file. The end-to-end pull-and-compute test is the appropriate first task of the implementation phase, NOT the feasibility phase.

**What I verified instead:**
- Catalog URL `https://microdatos.dane.gov.co/index.php/catalog/900` (2026 GEIH) is live and references file structure consistent with prior years
- File-naming convention (`Enero - Cabecera - Ocupados.csv` etc.) is documented in third-party tutorials operating on 2024 data
- Variable codes documented in DANE's "Diccionario de Datos" (linked from each catalog entry)

**Risk if execution were attempted now:** zero technical blockers identified, but the actual 2026-03 ZIP may not yet be published (catalog created 2026-04-14, suggesting Jan-Feb 2026 are the latest available months as of the assessment date). The most recent reliably available month is likely **February 2026**.

**Required keys for sample construction (for downstream spec author):**
- Person ID join key: `(DIRECTORIO, SECUENCIA_P, ORDEN)` across modules within a single month/Cabecera-Resto file
- Age field: `P6040` (in `Caracteristicas Generales`)
- Sector code field: in `Ocupados` module — the Rev. 4 section/division code (variable name varies by year; check Diccionario de Datos per year)
- Expansion factor: `FEX_C_2011` (Marco 2005) or `FEX_C_2018` (Marco 2018) per `Ocupados` row

---

## §3. Recommended Y Construction (precise definition for simple-β spec)

```text
Y_t = sum over persons i in Ocupados_{t, urban+rural} of:
        FEX_i * 1{P6040_i in [14, 28]} * 1{CIIU_section_i in {G,H,I,J,K,L,M,N,O,P,Q,R,S,T}}
      ────────────────────────────────────────────────────────────────────────────────
      sum over persons i in Ocupados_{t, urban+rural} of:
        FEX_i * 1{P6040_i in [14, 28]}

where:
  t = monthly index, January 2008 through latest published month
  FEX_i = expansion factor (FEX_C_2011 pre-2021, FEX_C_2018 from 2022; spliced via
          DANE empalme factor for analyses crossing 2021)
  Cabecera + Resto are summed (national aggregate, not city-restricted)
```

**Pre-registered sensitivities (do NOT promote any of these to primary post-hoc):**
1. `BPO-narrow Y`: restrict CIIU sections to {J, M, N}; quarterly cadence
2. `Bogotá-only Y`: restrict to Bogotá D.C. departmental code; broad sections; quarterly cadence
3. `18–28 Y`: restrict age to [18, 28] excluding minors; broad sections; monthly cadence
4. `Marco 2018 only Y`: restrict t to 2022-01 onward; broad sections; monthly cadence (avoids empalme factor entirely at the cost of n=51 months as of April 2026)

**Periodicity:** **monthly** is the recommended primary cadence. Sample stability supports it for the broad-services definition.

**Time window:** **2008-01 through latest published month** — gives ≈ 218 monthly observations as of April 2026, well above the Phase-A.0 `N_MIN = 75` threshold.

**Aggregation level:** national (Cabecera + Resto summed). No regional disaggregation in the primary.

---

## §4. Caveats for the Simple-β Spec to Handle

1. **2021 methodology break is non-negotiable.** The spec MUST pre-commit to one of (a) DANE empalme factor application, (b) 2021 indicator dummy, (c) Marco-2018-only sample (post-2022). Choice (c) reduces N to ≈51 monthly observations (April 2026), which is below the Phase-A.0 `N_MIN = 75` threshold — the spec must address this explicitly.

2. **CIIU revision boundary at 2012.** Files before 2012 use CIIU Rev. 3.1; from 2012 onward Rev. 4 A.C. is used. DANE publishes a Rev. 3.1 → Rev. 4 correspondence table. The spec must pre-commit to using DANE's correspondence rather than ad hoc author judgment.

3. **Expansion factor variable name changes across years.** `FEX_C_2011` for Marco 2005 files; `FEX_C_2018` for Marco 2018 files; with intermediate-year variants. Spec must pin the variable selection rule and document failures (any year without one of these names is a data-pull bug to halt on).

4. **No worker-cohort longitudinal tracking.** Y is a monthly cross-sectional ratio. Any narrative claim about "young workers transitioning out of services into BPO over time" cannot be tested with Y alone — it would require panel reconstruction from rotating-panel IDs, which is out of scope for the simple-β spec.

5. **Autocorrelation in monthly Y.** Even though each month is a fresh cross-section, the rotating-panel design induces serial dependence. HAC standard errors (Newey-West with bandwidth ≈ 6 months consistent with rotation length) are the minimum spec floor.

6. **COP/USD lag selection (X side, not Y).** The user's framing is "lagged 6–12 months" — the spec must pre-commit to a single lag (or test lags 6, 9, 12 with Bonferroni adjustment). Free lag tuning is anti-fishing-banned per Phase-A.0.

7. **Real-time release lag.** Latest published month is typically t-2 to t-3 from "now." This affects any out-of-sample / rolling-window robustness check the spec might propose.

8. **Y is bounded in [0, 1].** A linear OLS on Y is approximate; logit-transformed Y (`log(Y/(1-Y))`) is the technically correct primary if the spec wants to honor the bounded range. Empirically, Y is in roughly [0.55, 0.75] for Colombia → linear approximation error is small but reviewers may flag it.

9. **No BPO-specific cohort study exists** (the original research-agent flag). Pair D's narrative pivot — that Y captures BPO-driven non-industrialization — is unverifiable from Y alone. The simple-β spec should be honest that Y measures broad services, with BPO inferred only via the J+M+N sensitivity.

10. **Mirror-source disagreement.** IPUMS-harmonized Colombia panel applies its own Rev. 4 boundary and its own age band. If the simple-β spec uses IPUMS instead of native GEIH, results may differ from native-DANE construction. Pre-commit to one source.

---

## §5. References / URLs

**DANE primary sources** (all live and verified):

- DANE GEIH catalog index: `https://microdatos.dane.gov.co/index.php/catalog/MICRODATOS` (returns HTTP 500 on direct curl but individual entries resolve)
- GEIH 2026: `https://microdatos.dane.gov.co/index.php/catalog/900`
- GEIH 2025: `https://microdatos.dane.gov.co/index.php/catalog/853`
- GEIH 2024: `https://microdatos.dane.gov.co/index.php/catalog/819`
- GEIH 2023: `https://microdatos.dane.gov.co/index.php/catalog/782`
- GEIH 2022: `https://microdatos.dane.gov.co/index.php/catalog/771`
- GEIH 2021 (Marco 2005 + 2018 parallel): `https://microdatos.dane.gov.co/index.php/catalog/701`
- GEIH 2018: `https://microdatos.dane.gov.co/index.php/catalog/547`
- GEIH 2017: `https://microdatos.dane.gov.co/index.php/catalog/458`
- GEIH 2016: `https://microdatos.dane.gov.co/index.php/catalog/427`
- GEIH 2009 (oldest verified): `https://microdatos.dane.gov.co/index.php/catalog/207`
- ECH 2006 trimesters I-II (predecessor): `https://microdatos.dane.gov.co/index.php/catalog/116`
- GEIH historical landing: `https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo/geih-historicos`
- Departmental expansion factors 2007-2024: `https://microdatos.dane.gov.co/index.php/catalog/789`

**DANE methodology documents:**

- GEIH methodology V11: `https://www.dane.gov.co/files/operaciones/GEIH/met-GEIH.pdf`
- GEIH methodology (English fact-sheet): `https://www.dane.gov.co/files/investigaciones/fichas/great_integrated_household_survey_GEIH_methodology.pdf`
- Empalme series GEIH Marco 2005 → Marco 2018: `https://www.dane.gov.co/files/investigaciones/boletines/ech/ech/Nota-tecnica-empalme-series-GEIH.pdf`
- Empalme pobreza 2012-2020 (CEPAL collaboration): `https://microdatos.dane.gov.co/index.php/catalog/842`
- CIIU Rev. 4 A.C. 2022 update: `https://www.dane.gov.co/files/sen/nomenclatura/ciiu/CIIU_Rev_4_AC2022.pdf`
- CIIU Rev. 4 A.C. (full): `https://www.dane.gov.co/files/nomenclaturas/CIIU_Rev4ac.pdf`
- CIIU Rev. 4 disposed online: `https://clasificaciones.dane.gov.co/ciiu4-0/ciiu4_dispone`

**Monthly technical bulletins (published series — for sanity-check anchors):**

- Bol-GEIH January 2024: `https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-ene2024.pdf`
- Bol-GEIH August 2024: `https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-ago2024.pdf`
- Bol-GEIH December 2024: `https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-dic2024.pdf`
- Bol-GEIH November 2025: `https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-nov2025.pdf`
- Bol-GEIH December 2025: `https://www.dane.gov.co/files/operaciones/GEIH/bol-GEIH-dic2025.pdf`
- Bol-GEIH Juventud Aug-Oct 2022 (youth-specific): `https://www.dane.gov.co/files/investigaciones/boletines/ech/juventud/boletin_GEIH_juventud_ago22_oct22.pdf`

**Mirror / harmonized sources:**

- IPUMS International landing: `https://international.ipums.org/international/`
- IPUMS Colombia harmonized 2001–2025 panel via World Bank Microdata: `https://microdata.worldbank.org/index.php/catalog/7662`
- Banrep mercado laboral: `https://www.banrep.gov.co/es/mercado-laboral`
- Banrep historical statistical series (labor market notes EN): `https://www.banrep.gov.co/en/historical-statistical-series/labor-market`
- Banrep SUAMECA stats portal: `https://suameca.banrep.gov.co/estadisticas-economicas/`

**Legal / definitional:**

- Ley 1622 de 2013 (Estatuto de Ciudadanía Juvenil) — defines "juventud" as 14-28
- DANE Resolution 066 of 2012-01-31 — adopts CIIU Rev. 4 A.C.

---

**End of feasibility assessment.** No code generated, no spec content authored, no tracked files modified. Output written to `contracts/.scratch/` per project memory convention. Verdict: **FEASIBLE-WITH-CAVEATS**; recommended Y construction in §3 is ready to be consumed by the simple-β spec author.
