---
spec_id: saas-builder-stage-2-prereg-lock
spec_version: v1.0 (post-research; §5.2 brackets landed)
emit_timestamp_utc: 2026-05-07
parent_framework: notes/PRIMITIVES.md (a_s / a_l / CPO primitives)
cohort_note: notes/SaaS_Builders_AI_NativeBuilders.md (cohort instantiation of §4.2)
research_anchor: scratch/2026-05-07-claude-code-cost-research/RESEARCH.md (1500 words, 22 references)
authority: CLAUDE.md anti-fishing invariants (NON-NEGOTIABLE); brainstorming flow; CORRECTIONS-ι per-user a_s framing
status: LOCKED-PENDING-USER-REVIEW — sha-pinnable; sub-task plans dispatch on user approval
---

# Stage-2 pre-registration lock — SaaS-builder $a_s$ instantiation

This spec **locks the cross-cutting invariants** that all Stage-2 sub-tasks
(TODO-COHORT-1..4 + downstream) consume. Per CLAUDE.md anti-fishing
discipline, sub-tasks dispatch in parallel only against a sha-pinned
pre-registration. This is that document.

The sub-tasks themselves (cohort-specific calibration, sticky-form
verification, $\pi(t)$ derivation, $\Upsilon_t$-form selection) are
written as separate plans against this lock.

## §0 Scope statement

**In scope.** Stage-2 ideal-scenario M-sketch for the AI-native solo-builder
cohort. Specifies per-user $a_s$ functional form, $q_t$ workflow-derived
cost dynamics, $\Upsilon_t$ revenue process, and verification gates. The
CPO math (Carr-Madan replication, 12-leg IronCondor, $K_l = K_s$
equilibrium) is **inherited from PRIMITIVES.md and is not re-derived**.

**Out of scope.** Stage-1 empirical β work (handled by separate iteration);
Stage-3 deployment (LP capital sourcing, on-chain $a_s$ instantiation
plumbing); cross-LATAM aggregate welfare (CGE-class question); sustained
multi-vendor cost cross-validation beyond the canonical class.

## §1 Geographic and stage scope

- **Primary geography:** Colombia (CO).
- **Secondary geography:** LATAM (Mexico, Brazil, Argentina, Peru, Chile)
  flagged for Stage-3 cohort-survey expansion; not in primary calibration.
- **Stage filter:** post-revenue, pre-scale solo AI-native builder. Critical
  inclusion: per-user $a_s^{(T)} > 0$ today (solvent absent the hedge).
- **Cohort exclusions (out of primary):** cross-border-USD-revenue builders
  (Stripe USD MRR); B2B enterprise customers; teams >1 founder; pre-revenue
  experiments. These are separate cohorts with different $\Delta^{(a_s)}$
  signs / magnitudes.

## §2 Time grain

- **Cost cadence:** **monthly** — matches subscription billing (Anthropic
  Claude Pro/Max, AWS billing cycles) and MRR cadence.
- **FX cadence:** **monthly mean of daily TRM** for the primary
  specification; daily TRM available as sensitivity arm.
- **Sticky-cost ratchet (S3):** evaluated monthly.
- **Reporting horizon $T$:** rolling 12-month windows. Perpetual variant
  per PRIMITIVES.md §15 open item 4 is a sensitivity arm, not primary.

## §3 FX path class

- **Primary scenario:** deterministic perturbation generator from
  PRIMITIVES.md (6) — $(X/Y)_t = (1 + \varepsilon(\cos^2(\omega t) - 1/2))\,\overline{X/Y}$
  with $\varepsilon(\sigma_T)$ inversion (8) and $0 < \varepsilon < 1$.
- **Sensitivity arms:** Path A v3 stochastic SDEs — GBM, OU on $\log X$,
  jump-diffusion. Empirical-calibrated SDE (BanRep TRM 2010–2026 fit) is a
  Phase-2 hardening arm, not primary.
- **Mean $\overline{X/Y}$ pin:** 12-month trailing mean of monthly Banrep
  TRM as of audit_block timestamp. Recomputed and sha-pinned per
  audit_block.

## §4 Numeraire convention

- **All cash-flow outputs reported in COP** (cohort's lived unit).
- **Internal computation may use USD** (per PRIMITIVES (5')); conversion
  via $(X/Y)_t$ at the audit_block-pinned spot.
- **Premium $\pi(t)$ reported in COP/month.**
- **$Z$ in the pitch ("bill in COP never exceeds $Z$") reported in COP.**

## §5 Empirical-anchor commitment (Option α + workflow-derived)

Stage-2 calibration uses **Option α — public-pricing bracket-bound** for
all cost parameters. **Cohort first-party survey (Option γ) is a Stage-3
prerequisite, not a Stage-2 input.** Public-figure P&L scraping (Option
β) is queued as a Phase-2 hardening track.

### §5.1 Workflow-derived cost specification

Replace flat $\bar C$ with the canonical-class workflow cost model from
the SaaS-builder note. Class scope per the cohort note: terminal-based
agentic AI coding services (Claude Code as canonical exemplar; Aider,
Cursor agent mode, Codex CLI, Gemini CLI, Cline, Continue, Open
Interpreter, Devin in class).

**Token-consumption process (T1) — primary form (post-research update):**

$$
\tau_t = \sum_{j=1}^{D_t}\sum_{i=1}^{N_j} \tau_{j,i}, \qquad
N_j \sim \text{LogNormal}(\nu_N, s_N^2), \qquad
\tau_{j,i} \overset{\text{w/in-session}}{\sim} \text{Pareto}(\alpha, x_m)
$$

with $D_t \approx 22$ active coding days/month, $N_j$ = turns within
session-day $j$ (LogNormal not Poisson — research finds 30× same-task
variance and heavy right tail incompatible with Poisson dispersion;
arxiv 2604.22750), $\tau_{j,i}$ Pareto-tailed reflecting agentic
turn-cost distribution (arxiv 2604.22750: 1000× agentic-vs-chat
ratio, p99 > 200k tokens). Within-session position-dependence
(*"40th message pays for everything before it"* — Ouyang) is captured
via $x_m$ scaling with turn index $i$ in the Markovian sensitivity arm
(arxiv 2603.24582).

**Sensitivity arms:** (a) iid LogNormal $\tau_{j,i}$ — under-prices
right tail; (b) Markovian session-state model per arxiv 2603.24582 with
transition kernel over tool-call types; (c) over-dispersed turn count
(NegBin instead of LogNormal $N_j$).

**Two-regime pricing (T2):**

$$
q_t^{\text{USD}} = \bar p_{\text{sub}} + p_t \cdot (\tau_t - \kappa)^+
$$

### §5.2 Parameter brackets — LOCKED (post-research)

Sources: Anthropic published per-developer distribution
[`code.claude.com/docs/en/costs`]; per-token pricing
[`platform.claude.com/docs/en/about-claude/pricing`]; arxiv 2604.22750
(token-consumption variance); arxiv 2603.24582 (Markovian framework);
arxiv 2601.14470 (input/output/reasoning split).

**Tier and pricing (firm, vendor-published May 2026):**

| Parameter | Value | Source |
|---|---|---|
| $\bar p_{\text{sub}}$ tiers | $\{$20$ Pro, $100$ Max-5x, $200$ Max-20x$\}$ | claude.com/pricing |
| **Primary tier** | $\bar p_{\text{sub}} = 200$ (Max-20x) | rationale: cap-kink / metered-overflow boundary; matches the operational regime where $(\tau_t - \kappa)^+ > 0$ has positive mass |
| $p_t$ Sonnet 4.6 | $3$ /MTok input, $15$/MTok output | platform.claude.com pricing |
| $p_t$ Opus 4.6 | $5$/MTok input, $25$/MTok output | platform.claude.com pricing |
| $p_t$ Haiku 4.5 | $1$/MTok input, $5$/MTok output | platform.claude.com pricing |
| $p_t$ Opus 4.7 (released 2026-04-16) | $5$/$25 nominal; effective +35% via new tokenizer | finout-opus47 |
| Prompt cache discount | input −90% on cache hit | finout-pricing |
| Batch discount | −50% all classes | finout-pricing |

**Cap structure (firm):**

- 5-hour rolling session window + weekly hard cap (introduced 2025-08-28).
- Pro / Max-5x: blocked when capped.
- Max-20x: opt-in metered API overflow at standard $p_t$ — this is the
  exit door from subscription mode into the $q_t = N \cdot \tau \cdot p$
  regime that the (T2) overage term models.
- 2026-05-06: 5-hour limits doubled, peak-hour reductions removed
  [9to5google, anthropic-spacex]; baseline numbers not officially
  published.
- $\kappa$ token-equivalent estimate (independent third-party, not
  Anthropic-confirmed): Pro ≈ 44k tok/5h; Max-5x ≈ 88k tok/5h; Max-20x
  ≈ 220k tok/5h [tokenmix, verdent]. Annualized at 22 active days/mo,
  three 5-hour windows/day: **Max-20x $\kappa \approx 14.5$ M
  tokens/month**. Treat as ±50% bracket given the third-party nature.

**Empirical $\$/$mo distribution (Anthropic first-party, enterprise):**

| Statistic | Value | Source |
|---|---|---|
| Mean | $13$/active-day | costs-doc |
| p90 | ≤ $30$/active-day | costs-doc |
| Monthly enterprise | $150$–$250$/dev/month | costs-doc |
| Implied p90/mo (22 active days × $30) | $660$/month | derived |

**Empirical token-consumption process (independent + arxiv):**

| Quantity | Bracket | Source |
|---|---|---|
| Light user $/day API | $2$–$5$/day | tokenmix |
| Active user (3–5 hr) $/day | $6$–$12$/day → ≈ $100$–$200$/mo Sonnet 4.6 | tokenmix, verdent |
| Heavy / multi-agent $/day | $30$–$50$/day | costs-doc, b2l-ouyang |
| **Same-task token-spread (run-to-run)** | **30×** | arxiv 2604.22750 |
| **Agentic-vs-chat token ratio** | **1000×** | arxiv 2604.22750 |
| Input / output / reasoning split | 53.9% / 24.4% / 21.6% | arxiv 2601.14470 |
| Code-review-style turn share of session tokens | ≈ 59% | arxiv 2601.14470 |
| Multi-agent vs single-agent token ratio | ≈ 7× | costs-doc |
| Self-prediction correlation (model predicts own cost) | ≤ 0.39 | arxiv 2604.22750 |

**Recommended priors for (T1) Bayesian fit (this is the primary spec):**

| Param | Median | p90 | Distribution |
|---|---|---|---|
| $N_j$ (turns/active-day) | ~80 | ~250 | LogNormal |
| $\tau_{j,i}$ (tokens/turn, weighted i+o) | 2–8k | 50–150k; p99 > 200k | Pareto |
| Effective input rate w/ 95% cache hit | ≈ $0.30$/MTok Sonnet | — | scalar |

**Plausible LATAM-builder $/mo (full-time agentic, no subsidy):**
**$150–$400 modal, $500–$1,500 p90, > $2,000 p99.** This is the
random variable the CPO sells — heavy-tailed with cap-induced kink,
exactly the regime where convex payoff has positive value.

### §5.3 Heavy-user regime — substantiation status

Per RESEARCH.md §4: substantiated *qualitatively* (Ouyang $1,600/mo
[b2l-ouyang]; alderson HN-cited 150–200M tok/day → $5k/mo retail
[alderson]; GitHub #9424 mass cap-breach reports [gh-9424]) but **not
substantiated with clean screenshotted distributions**. Anthropic's own
p90 × 22 days = $660/mo, so the > $1,000/mo regime is the empirical
right tail (5–15% of full-time agentic users) — consistent, not
contradicted, by first-party data.

Levelsio / Marc Lou / Tony Dinh public bills: **NOT FOUND**. Earlier
spec drafts that cited them as anchor sources are corrected here.

### §5.4 Realism overrides committed

Per the prior conversation:
- (a) Bracket subsumes mixed-tier usage including API-heavy builders to
  ~$2k/mo upper bound.
- (b) Cost-revenue endogeneity $\rho(q_t, \Upsilon_t) = 0$ in primary
  spec; sensitivity arm pins $\rho > 0$ for the production-agent
  cohort sub-population (deferred to a separate iteration).
- (c) Bank-spread overlay $s_t \in [1\%, 3\%]$ applied to $(X/Y)_t$ in
  primary spec; varied as sensitivity arm.
- (d) Cross-border-USD-revenue builders OUT of cohort scope per §1.

## §6 Primary functional-form pins

| Object | Primary form | Source | Sensitivity arms |
|---|---|---|---|
| $a_s^{(T)}$ | (S1): $\sum \Upsilon_t - \sum q_t/(X/Y)_t$ | PRIMITIVES (5'); SaaS note | n/a — universal |
| $\Upsilon_t$ | (S4): martingale $\mathbb{E}[\Upsilon_{t+1}\mid\mathcal F_t] = \Upsilon_t$ | SaaS note §"Revenue" | AR(1)-log-MRR; det+churn |
| $q_t^{\text{det}}$ | $\bar p_{\text{sub}}$ from (T2) primary tier | §5.1 | tier sensitivity $\{20, 100, 200\}$ |
| $q_t^{\text{sticky}}$ | (T2) overage $p_t (\tau_t - \kappa)^+$ as stochastic, NOT one-sided ratchet | §5.1 supersedes (S3) | ratchet (S3) for true commitments (annual plans, AWS reserved) |
| $\tau_t$ | (T1) LogNormal $N_j$ × Pareto $\tau_{j,i}$ | §5.1 (post-research update) | iid LogNormal $\tau_{j,i}$; Markovian session-state (arxiv 2603.24582); NegBin $N_j$ |
| $(X/Y)_t$ | (6) deterministic perturbation | §3 | GBM, OU, jump, empirical |
| FX vol $\sigma_T$ | (7) realized variance | PRIMITIVES.md | high-frequency RV; GARCH |
| Premium $\pi(t)$ | Streamed COP/month per §9; $T = $ rolling 12-mo | §2; PRIMITIVES §9, §15 op4 | discrete monthly $P_0^{\Pi}$ |

**Note on (T2) supersedes (S3).** The earlier SaaS-note draft picked S3
one-sided ratchet as primary for $q_t^{\text{sticky}}$. The
canonical-class workflow model (T1)+(T2) replaces that — the variable
component is *stochastic via token consumption*, not sticky in the
SaaS-commitment sense. The (S3) ratchet is preserved for *true*
multi-month commitments (annual plans, AWS reserved instances), now
treated as an additive $q_t^{\text{commit}}$ term flagged for Phase-2
hardening if cohort data shows non-trivial commitment density.

## §7 Tooling commitment (Option 1)

**Stack:** Python 3.13 + uv + sympy + numpy + scipy + pandas + PyMC for
all slices.

- **Symbolic derivation:** sympy notebooks per Path A v0 trio-checkpoint
  discipline (`feedback_notebook_trio_checkpoint`).
- **Sign / equilibrium claims:** numerically certified via Path A v0
  exit criteria (a)–(e); tolerance $\le 10^{-10} \cdot N_{\text{legs}}$
  for self-consistency, $\pm 5\%$ for sympy↔numeric reconciliation per
  Path A spec §10.4.
- **Stochastic FX paths (sensitivity arms):** numpy + scipy.stats SDE
  Euler-Maruyama; no Itô-formal proofs.
- **Cohort calibration:** PyMC for Bayesian posterior over
  $(\lambda, \mu, s, \bar p_{\text{sub}}, \kappa)$; Politis-Romano
  stationary bootstrap (per CORRECTIONS-η MQ-BLOCK-5 precedent) for any
  CI on time-series quantities.
- **Notebooks:** all Stage-2 work lands in `notebooks/saas_builder/` per
  the existing fx_vol pattern (`01_data_eda.ipynb`,
  `02_estimation.ipynb`, `03_tests_and_sensitivity.ipynb`).

**No Lean 4, no Aristotle, no Mathematica, no Julia migration.** Slice-B
load-bearing claims (sign of $\Delta^{(a_s)}$, $K_l = K_s$) accept
numerical certification as the verification standard for v0.1. Formal
proof is a flagged Phase-2 hardening track if a referee challenges; not a
v0.1 commitment.

## §8 Anti-fishing invariants

Carried verbatim from CLAUDE.md (NON-NEGOTIABLE):

- $N_{\text{MIN}} = 75$, $\text{POWER}_{\text{MIN}} = 0.80$,
  $\text{MDES}_{\text{SD}} = 0.40$ SD-units of any outcome variable.
- Pre-pin sign expectation, lag structure, primary specification
  BEFORE data is touched. **This spec IS that pin** for Stage-2 cohort
  calibration.
- HALT + disposition memo + user-enumerated pivot + CORRECTIONS block +
  post-hoc 3-way review whenever spec contradicts data.

Cohort-specific additions:

- **Sign expectation:** $\Delta^{(a_s)} < 0$ across the entire admissible
  parameter region $0 < \varepsilon < 1$ AND across all bracket points
  in §5.2. A computed sign reversal at any bracket point fires HALT.
- **Convexity expectation:** $\Pi^{(s)}$ convex in $\sigma_T$ (the
  $\sqrt{\cdot}$ shape, locally concave but globally non-decreasing in
  $\sigma_T$ — *check sign convention in implementation*). A linear or
  concave-in-$\sigma_T$ winning $\Pi$ form fires the thesis-fitness
  HALT per CORRECTIONS-η RC-BLOCK-2 precedent.
- **Bracket immutability:** §5.2 brackets, once landed, are sha-pinned
  and frozen. Tightening / widening post-hoc requires CORRECTIONS-block.
- **Tier-cap mechanics immutability:** $\kappa$ pinned per audit_block
  cannot be retuned to fit a desired result.

## §9 Verification gates per sub-task

| Sub-task | Done when | Tolerance |
|---|---|---|
| TODO-COHORT-1 ($\bar C$ distribution / monthly $/mo CDF) | Posterior over (T1) parameters $(\nu_N, s_N, \alpha, x_m)$ + tier mix $\bar p_{\text{sub}}$ emitted; resulting $\$/$mo CDF reported at p10/p50/p90/p99 | priors anchored to RESEARCH.md §3 (Anthropic first-party + arxiv 2604.22750 / 2603.24582 / 2601.14470). Indie-hacker public P&L sources are NOT required (none found in research per §5.3). |
| TODO-COHORT-2 (sticky form) | (T2) overage form fitted on synthetic $\tau_t$ from §5.1; $\Gamma^{(a_s)}$ sign + magnitude reported with 95% bootstrap CI | $\Gamma^{(a_s)}$ sign matches sign expectation per §8; bootstrap = stationary Politis-Romano, $n=10000$, BCa CI |
| TODO-COHORT-3 ($\Upsilon_t$ form) | Three forms (martingale, AR(1)-log, det+churn) fit on cohort prior; AICc winner declared with PASS / PASS-WEAK / MARGINAL / FAIL routing per CORRECTIONS-η MQ-BLOCK-2 precedent | AICc not AIC (n/k < 40 likely); INDISTINGUISHABLE verdict allowed |
| TODO-COHORT-4 ($\pi(t)$ derivation) | Closed-form or numerical $\pi(t) \cdot dt = d\Pi/dt$ identity certified at three pinned $(\overline{X/Y}, \sigma_T)$ test points | Per Path A v0 §10.4 reconciliation tolerance |

All sub-task gates also require: input-data sha pinned, output schema
matched per §10, decision-citation block (4-part: reference / why /
relevance / connection) per `feedback_notebook_citation_block`.

## §10 Output artifact contract

Each sub-task emits to `notebooks/saas_builder/`:

| Artifact | Format | Schema |
|---|---|---|
| `data/cohort_prior.parquet` | parquet | columns: `param`, `percentile`, `value`, `source`, `fetched_at_utc` |
| `data/synthetic_tau_t.parquet` | parquet | columns: `month`, `simulation_id`, `lambda`, `mu`, `s`, `tau_t`, `q_t_usd`, `q_t_cop` |
| `estimates/PRIMARY_RESULTS.md` | markdown | per-sub-task primary outcome + numerical evidence + decision-citation block |
| `estimates/ROBUSTNESS_RESULTS.md` | markdown | sensitivity arms results |
| `estimates/gate_verdict.json` | JSON | `{"sub_task": ..., "verdict": "PASS|MARGINAL|FAIL", "evidence": [...]}` |
| `dispositions/` | markdown | HALT memos if any |
| `MEMO.md` | markdown | overall Stage-2 verdict |

Reproducibility manifest: `notebooks/saas_builder/REPRODUCIBILITY.md`
records library version pins, RNG seeds, FX-mean audit_block pin, $p_t$
fetch timestamp.

## §11 Sub-task dependency graph

```
§5.2 brackets (LOCKED v1.0)
        │
        ├──► TODO-COHORT-1 ($\bar C$ distribution)
        │        │
        │        └──► TODO-COHORT-2 (sticky / (T2) fit)
        │                  │
        │                  └──► $\Delta^{(a_s)}$ closed form per cohort
        │                            │
        │                            └──► TODO-COHORT-4 ($\pi(t)$ derivation)
        │
        └──► TODO-COHORT-3 ($\Upsilon_t$ form)
                  │
                  └──► joins TODO-COHORT-4 input
```

Parallelism: TODO-COHORT-1 and TODO-COHORT-3 are independent and can
dispatch in parallel as soon as §5.2 brackets land. TODO-COHORT-2
depends on COHORT-1 output. TODO-COHORT-4 depends on both COHORT-2 and
COHORT-3.

## §12 What this spec does NOT lock (deferred)

| Item | Deferred to |
|---|---|
| Cross-LATAM cohort survey (Option γ; n=30–75; conditional $/mo CDF given Colombian solo builder ≥30h/wk Claude Code) | Stage-3 prerequisite — closes the only real public-data gap per RESEARCH.md §6 |
| Public-figure P&L scraping (Option β) | Phase-2 hardening track |
| Stochastic SDE Itô-formal proofs | Phase-2 hardening (Mathlib SDE coverage gap) |
| Cost-revenue endogeneity sub-population ($\rho > 0$) | Separate iteration |
| Cross-border-USD-revenue builders | Separate cohort iteration |
| Production-agent cost workflow (W_prod) | Separate workflow iteration |
| Cross-vendor (non-Anthropic) class-member cost dispersion | Phase-2 hardening; only required if Stage-2 results show vendor sensitivity |
| Formal $K_l = K_s$ proof in Lean | Phase-2 hardening if referee challenge |

## §13 Pre-condition for sub-task dispatch

The following must be true before TODO-COHORT-1..4 sub-task plans are
written:

1. ✅ PRIMITIVES.md sha-pinned at `notes/PRIMITIVES.md` (HEAD).
2. ✅ Cohort note sha-pinned at `notes/SaaS_Builders_AI_NativeBuilders.md`.
3. ✅ §5.2 empirical brackets landed (research complete; RESEARCH.md sha-pinnable at HEAD).
4. ✅ This spec is v1.0; sha-pinnable on commit.
5. ⏳ Self-review per `superpowers:brainstorming` flow (placeholder
   scan, internal consistency, scope check, ambiguity check).
6. ⏳ User review per the brainstorming skill's "User Review Gate".

Steps 5–6 unblock sub-task plan authoring via `superpowers:writing-plans`.

---

## Spec self-review (to be executed when v1.0 lands, post-§5.2 patch)

- [ ] Placeholder scan: §5.2 brackets all replaced with cited values.
- [ ] Internal consistency: (T2) supersedes (S3) flagged in §6 — no
      conflicting pins in TODO-COHORT-2 verification gate (§9).
- [ ] Scope check: single Stage-2 ideal-scenario M-sketch deliverable;
      no creep into Stage-1 or Stage-3.
- [ ] Ambiguity: $\bar p_{\text{sub}}$ tier — primary tier pinned, not
      "varies"?
- [ ] Cross-reference: every TODO-COHORT-N tag in §5.2 / §6 / §9 / §11
      consistent.

End of v0.1.
