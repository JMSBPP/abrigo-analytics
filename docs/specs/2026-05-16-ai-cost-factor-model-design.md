---
spec_id: ai-cost-factor-model
spec_version: 0.2.5
created: 2026-05-16
status: DRAFT — v0.2.5 reliability-convergence patch (§0.5 CORRECTIONS-Y-8) closing the ~2.1× ccusage cost overcount via OSS-mirror uniqueHash dedup. Empirical validation in `scratch/2026-05-17-v0_2_5-dedup-discovery/findings.md` shows cost converges from 2.11× to 0.977× of ccusage post-dedup. Awaiting two-wave review.
v0_1_0_status: REJECTED 2026-05-16 by all three reviewers — see §12 revision history
v0_2_0_status: NEEDS_WORK (Wave 1 RC) + NEEDS_WORK (Wave 2 Model QA) + ACCEPT_WITH_FLAGS (Wave 2 Code Reviewer) — all prior BLOCKs closed; 5 new BLOCKs surfaced from deferred evidence + methodology pins
parent_iteration_pin: dev-AI-cost iteration (parent CLAUDE.md "Abrigo Operating Framework"; prior FAIL pinned)
prior_iteration_fail: project_dev_ai_section_j_fail.md (2026-05-06; Section J narrow ICT β=-0.146 sign-flipped)
iteration_directory: notebooks/dev_ai_cost_v2/
review_protocol: feedback_two_wave_doc_verification (Wave 1 = Reality Checker; Wave 2 = Model QA Specialist + Code Reviewer in parallel)
verifier_v0_1_0_wave1: REJECT (5 BLOCKs — scratch/2026-05-16-ai-cost-spec-review/wave1_reality_checker.md)
verifier_v0_1_0_wave2_model_qa: REJECT (5 BLOCKs — scratch/2026-05-16-ai-cost-spec-review/wave2_model_qa.md)
verifier_v0_1_0_wave2_code_reviewer: NEEDS_WORK (6 BLOCKs — scratch/2026-05-16-ai-cost-spec-review/wave2_code_reviewer.md)
verifier_v0_2_0_wave1: NEEDS_WORK — all 5 prior BLOCKs CLOSED; new BLOCKs 6 (claude-parser unfit) + 7 (LiteLLM keys); scratch/2026-05-16-ai-cost-spec-review/wave1_reality_checker_v0_2_0.md
verifier_v0_2_0_wave2_model_qa: NEEDS_WORK — all 5 prior BLOCKs CLOSED; new BLOCKs 8 (bootstrap) + 9 (covariance) + 12 (R5 role); scratch/2026-05-16-ai-cost-spec-review/wave2_model_qa_v0_2_0.md
verifier_v0_2_0_wave2_code_reviewer: ACCEPT_WITH_FLAGS — all 6 prior BLOCKs CLOSED; 2 new FLAGs (Iterator, ts param); scratch/2026-05-16-ai-cost-spec-review/wave2_code_reviewer_v0_2_0.md
verifier_v0_2_1_wave1: CLOSE_ALL — all 4 v0.2.0 RC findings closed; SHA pin verified at e58a561c...; plan-emission APPROVED (scratch/2026-05-16-ai-cost-spec-review/wave1_reality_checker_v0_2_1.md)
verifier_v0_2_1_wave2_model_qa: CLOSE_ALL — all 7 v0.2.0 Model QA findings closed; CORRECTIONS-P/Q/R/S/T/U compose without contradiction; plan-emission APPROVED (scratch/2026-05-16-ai-cost-spec-review/wave2_model_qa_v0_2_1.md)
verifier_v0_2_1_wave2_code_reviewer: CLOSE_ALL — both v0.2.0 FLAGs + partial-CLOSE + NITs closed; substrate swap clean; plan-emission APPROVED (scratch/2026-05-16-ai-cost-spec-review/wave2_code_reviewer_v0_2_1.md)
plan_emission_blocked_until: user decision on R6 (continuous-stream simulation for dual hedge-value framing) — options A/B/C pending in conversation 2026-05-16
impl_review_checkpoint_v0_2_1_code_reviewer: NEEDS_FIXES (2 Important + 5 Minor; scratch/2026-05-16-ai-cost-impl-review/code_reviewer.md)
impl_review_checkpoint_v0_2_1_reality_checker: REJECTED — 2 production BLOCKs spec-rooted (scratch/2026-05-16-ai-cost-impl-review/reality_checker.md). BLOCK A: JSONLReader cannot parse any real ~/.claude/projects/*.jsonl (no type-discriminator; extra='forbid' rejects 9 type values + 6 message.usage extra fields; required costUSD field absent from 0/355 real assistant rows). BLOCK B: LiteLLM SHA pin incomplete — 6/21 claude-* models lack cache_creation_input_token_cost_above_1hr including claude-sonnet-4-5 and claude-sonnet-4-6.
impl_review_checkpoint_v0_2_1_backend_architect: APPROVED with 2 Important fixes for Task 10 sub-task (scratch/2026-05-16-ai-cost-impl-review/backend_architect.md).
oss_algorithm_study: scratch/2026-05-16-ai-cost-impl-review/oss_algorithm_study.md — empirical study of ccusage / cc-lens / agentsview / claude-parser source code finds our schema policy is the outlier; all OSS tools type-discriminate first, use extra='allow', compute cost from Σ_cat tokens_cat × rate_cat with Optional rate fields, ignore ephemeral_5m/1h split. Recommendation: amend v0.2.1 via four CORRECTIONS-Y blocks (Y-1 parsing, Y-2 cost formula, Y-3 LiteLLM strategy, Y-4 integration test floor) + ccusage-parity oracle test.
verifier_v0_2_2_wave1: PARTIAL_CLOSE — BLOCK A + B both closed; 2 housekeeping fixes (stale Decimal language in §4 + §6 row 5) LANDED in v0.2.2 (no v0.2.3 work). scratch/2026-05-16-ai-cost-spec-review/wave1_reality_checker_v0_2_2.md
verifier_v0_2_2_wave2_model_qa: CLOSE_ALL — float precision sound; bootstrap precision sound; HAC precision sound; reconciliation tightening 1%→0.1% sound; cross-coherence with CORRECTIONS-P/Q/R/S/T/U preserved. 1 non-blocking FLAG: ephemeral 5m/1h aggregation introduces multiplicative scale bias on cost LEVELS but NOT on variance — recommend disclosing π̂=Σcache_create_1h/Σcache_create_total as DATA_PROVENANCE diagnostic. scratch/2026-05-16-ai-cost-spec-review/wave2_model_qa_v0_2_2.md
verifier_v0_2_2_wave2_code_reviewer: PARTIAL_CLOSE — WITHHELD plan-amendment approval; 6 architectural BLOCKs (CR-Z-1 counter ownership; CR-Z-2 JSONLReadResult tier-orphan; CR-Z-3 cache aggregation locus; CR-Z-4 longest-substring tiebreaker non-determinism; CR-Z-5 uuid synthesis breaks under rename → R6 false drift; CR-Z-6 missing CORRECTIONS-Y-5 + Task 9.5 migration). Driving v0.2.3 contract-only patch. scratch/2026-05-16-ai-cost-spec-review/wave2_code_reviewer_v0_2_2.md
verifier_v0_2_3_wave1: CLOSE_ALL after 2 inline doc fixes landed (§2.1 stale-Decimal + Y-5f missing scripts/build_notional_cost_panel.py row). scratch/2026-05-16-ai-cost-spec-review/wave1_reality_checker_v0_2_3.md
verifier_v0_2_3_wave2_model_qa: CLOSE_ALL — π̂ folded properly. scratch/2026-05-16-ai-cost-spec-review/wave2_model_qa_v0_2_3.md
verifier_v0_2_3_wave2_code_reviewer: CLOSE_ALL — all 6 CR-Z BLOCKs closed. **Plan-amendment-cycle APPROVED.** scratch/2026-05-16-ai-cost-spec-review/wave2_code_reviewer_v0_2_3.md
plan_amendment_status: APPROVED — proceed to v0.2.3 implementation patch (plan Task 9.5 migration covering 8 files per §0.3 Y-5f) then impl-review re-checkpoint then Task 10
related_skills:
  - structural-econometrics
  - python-panel-data
  - statsmodels
  - hypothesis-tests
  - functional-python
  - latex-econ-model
  - audit-econ
---

# AI-Cost Factor Model — Counterfactual Risk Quantification (Subscription-Aware Pilot)

## 0. CORRECTIONS block (v0.1.0 → v0.2.0)

The v0.1.0 spec was rejected by all three reviewers. The corrections that
produced v0.2.0 are itemized here because the framework rejection was
load-bearing and the user's pivot decisions are part of the audit trail.

**CORRECTIONS-A (Identification — Model QA BLOCK 1; Reality Checker BLOCK 5).**
v0.1.0 claimed COP re-denomination broke the accounting identity
$\text{Cost}^{USD} \equiv \text{priceAPI} \cdot \text{tokens}$. Reviewers
proved algebraically and empirically that this is false: re-denominating LHS
into COP merely lengthens the identity to three terms
($\ln \text{Cost}^{COP} \equiv \ln \text{priceAPI} + \ln \text{tokens} +
\ln \text{USDCOP}$). β₁ has zero residual variance to load on; the model is
mechanically unidentified.

**Fix**: pivot to **R5 — descriptive counterfactual risk quantification**
plus **R4-Stage-3 — vol-clustering regression on notional COP cost** as the
auxiliary inferential arm. LHS in R4-S3 is an absolute log-return, not an
identity-determined level — this is identified by construction.

**CORRECTIONS-B (Cost regime — user input 2026-05-16).** v0.1.0 implicitly
assumed pay-per-API regime. The pilot subject (repo maintainer) uses
**Claude Code on subscription only**. Therefore: (i) actual USD cost is flat
within a billing month; (ii) the `costUSD` field in JSONL is **notional** (rate
card × tokens) not actual billing; (iii) the framework-relevant question is
re-framed as "what COP cost-burden risk would a non-subscribed LATAM
developer face for equivalent usage" — the subscribed user's logs serve as a
proxy.

**CORRECTIONS-C (Data feeder — Reality Checker BLOCK 1; deeper OSS scan).**
v0.1.0 specified ccusage as parsing substrate. RC verified ccusage `session
--json` emits session aggregates only (no per-message rows, no `requestId`,
no `isApiErrorMessage`, model-mix collapsed to `modelsUsed[]`). Deeper OSS
scan found ccusage's library mode is not publicly exported and its schema
drops the ephemeral_5m/1h split. All AI-observability platforms (Helicone,
LangSmith, Langfuse, Phoenix, LiteLLM proxy, etc.) are live-proxy
architectures that cannot ingest existing JSONL. **Substrate switched to
`claude-parser` (PyPI, Pydantic + DuckDB)** with a 30-minute
ephemeral-split-preservation verification gate; fallback = ~150 LoC own
Python parser if the gate fails.

**CORRECTIONS-D (Ephemeral split — Reality Checker BLOCK 2a).** v0.1.0 §3.2
asserted Claude Code aggregates `ephemeral_5m_input_tokens` and
`ephemeral_1h_input_tokens` into `cache_creation_input_tokens` before
persisting. RC grepped the maintainer's own JSONL (version 2.1.143) and
confirmed the nested `cache_creation: {ephemeral_1h_input_tokens,
ephemeral_5m_input_tokens}` is preserved per assistant row. **The
granularity IS in source data.** v0.2.0 §3 preserves it.

**CORRECTIONS-E (Banrep panel — Reality Checker BLOCK 4).** v0.1.0 §2.1
claimed `notebooks/dev_ai_cost/data/cop_usd_panel.parquet` already contains
the daily TRM. RC verified: 135 rows indexed by `year_month` — **monthly**,
not daily. Daily TRM must be fetched. **Prerequisite work item**: extend
`scripts/fetch_banrep.py` for daily TRM (consistent with prior dev-AI
iteration source).

**CORRECTIONS-F (Anthropic Admin API — user input 2026-05-16).** v0.1.0
implicitly considered Anthropic Admin API as a canonical source. User
clarified: they use Claude Code on **consumer subscription**, not on a
workspace API plan. The Admin API + `usage_report/messages` endpoint is part
of the API Platform billing rail, separate from consumer Pro/Max
subscription billing. Admin API path is **out of scope for the pilot**;
documented as cohort-scaling work item.

**CORRECTIONS-G (Sample floor — Reality Checker BLOCK 6).** v0.1.0
required $N \geq 75$ developer-days. RC counted the maintainer's
`~/.claude/projects/` activity: 52 distinct dates, 38 weekdays. **N-floor
lowered to $N = \max(\text{weekday days observed})$** (≈38 at spec write
time, growing with usage). The pilot is now explicitly demonstration-grade
at n=1; the lowered floor is permissible because R5's primary outputs are
descriptive (bootstrap CIs handle uncertainty), and R4-S3 is auxiliary with
a one-sided pre-pinned hypothesis. CORRECTIONS-block deviation from project
default per anti-fishing protocol.

**CORRECTIONS-H (Implementation contracts — Code Reviewer BLOCKs 1–6).**
v0.1.0 §3.4 left interface signatures partially untyped, reproducibility
pins deferred, error-class definition site undeclared, 0.5% reconciliation
tolerance unjustified. v0.2.0 §4.4 pins concrete signatures; pins are
committed in this spec, not deferred; reconciliation tolerance is tightened
to exact-Decimal with a documented bound on representable rounding.

## 0.1 v0.2.0 → v0.2.1 CORRECTIONS (review-integration patch)

v0.2.0 review surfaced 5 new BLOCKs across Wave 1 RC + Wave 2 Model QA, plus
non-blocking FLAGs from Wave 2 Code Reviewer. All v0.1.0 BLOCKs were
confirmed CLOSED by reviewers. v0.2.1 integrates every new finding.

**CORRECTIONS-N (Parser substrate — RC BLOCK 6).** The 30-min
`claude-parser==2.0.0` ephemeral-split verification gate FAILED. RC
inspected the wheel: `NormalizedMessage` Pydantic schema contains only
`{uuid, timestamp, type, tool_result}` — no `usage`, no `cache_creation`,
no ephemeral fields. `count_tokens` sums only input+output. Billing uses a
hardcoded Jan-2025 price dict with a 125%-of-input cache heuristic.
**Fix**: per v0.2.0 §3.1 fallback clause, the own-parser is promoted to
**primary substrate** (Python, ~150 LoC). `claude-parser` is removed from
the spec entirely. The JSONL schema is documented and stable; Anthropic's
own field names (`message.usage.input_tokens`, `message.usage.output_tokens`,
`message.usage.cache_creation.ephemeral_5m_input_tokens`,
`message.usage.cache_creation.ephemeral_1h_input_tokens`,
`message.usage.cache_read_input_tokens`) are the parsing targets.

**CORRECTIONS-O (LiteLLM key names — RC BLOCK 7).** RC's verification of
the LiteLLM file at SHA `e58a561caa21169fb02174148444c08509ce7028`
(BerriAI/litellm main, 2026-05-14) found that the actual JSON keys are:

- `cache_creation_input_token_cost` (the **5m** default rate)
- `cache_creation_input_token_cost_above_1hr` (the **1h** rate)

NOT the `ephemeral_5m_input_token_cost` / `ephemeral_1h_input_token_cost`
names v0.2.0 §3.2 / §5.2 asserted. 45 Anthropic models in the LiteLLM table
carry the split. **Fix**: spec wording corrected throughout; SHA pin
committed to §5.2.

**CORRECTIONS-P (Bootstrap scheme — Model QA BLOCK 8).** v0.2.0 §2.1
specified $B = 10{,}000$ bootstrap without pinning the resampling scheme.
IID bootstrap is incorrect for serially-correlated daily absolute-return
data (vol clustering / ARCH effects), and would falsely tighten R5's CI
half-width gate. **Fix**: pin **stationary bootstrap (Politis & Romano
1994)** with expected block length $\lceil T^{1/3} \rceil$. At $T = 38$,
expected block length = 4; at $T = 75$, expected block length = 5.

**CORRECTIONS-Q (Covariance allocation — Model QA BLOCK 9).** v0.2.0 §2.1
output 3 specified the variance decomposition
$\text{Var}(\Delta\ln\text{NotionalCost}^{COP}) = \text{Var}(\Delta\ln
\text{NotionalCost}^{USD}) + \text{Var}(\Delta\ln \text{USDCOP}) +
2\,\text{Cov}(\cdot,\cdot)$ without pinning how the cross-covariance is
attributed to "FX share." Three standard practices diverge when
$\text{Cov} \neq 0$ (which it will be at cohort scale even if approximately
zero in the n=1 subscription regime). **Fix**: pin the **conservative
attribution rule** — covariance term is reported **separately**, not
attributed to either share. Headline "FX share" =
$\text{Var}(\Delta\ln \text{USDCOP}) / \text{Var}(\Delta\ln
\text{NotionalCost}^{COP})$ excluding covariance. The covariance is
reported as a separate diagnostic. This is conservative for the M-design
gate (a positive Cov would inflate the apparent FX share under alternative
attributions; dropping it understates and avoids overclaiming).

**CORRECTIONS-R (R5 Role disambiguation — Model QA BLOCK 12 / §10 Q5).**
v0.2.0 §2.1 left R5's M-design role ambiguous between (A) individual-
sizing — "how big should the wage-earner's hedge position be in COP terms
for $X notional usage" — and (B) channel-existence — "is FX the dominant
risk factor at all." Model QA noted that the "tokens-constant"
counterfactual reduces to a publicly known USDCOP-vol series scaled by a
constant, which is informationally redundant against Banrep's TRM panel
itself for purpose (B). **Fix**: pin R5's role as **(A) individual-
sizing**. The headline output is interpreted as "for this usage pattern at
this notional dollar volume, the M-design hedge must absorb $Y$ COP of
cost-burden variance per month" — a quantity the M-design step consumes
directly. Channel-existence (purpose B) is not claimed by R5; it follows
from R4-S3 if α₁ > 0.

**CORRECTIONS-S (R4-S3 reframing — Model QA FLAG 7).** Model QA noted
that R4-S3 with COP LHS partially recovers a well-established USDCOP
vol-clustering stylized fact, independent of any AI-cost transmission
channel. **Fix**: R4-S3-COP is reclassified as a **consistency check**
(not a novel finding); a new auxiliary arm **R4-S3-USD** is added as the
behavioral test:
$$|\Delta\ln\text{NotionalCost}^{USD}_t| = \alpha_0 + \alpha_1
|\Delta\ln\text{USDCOP}_{t-k}| + \alpha_2 |\Delta\ln\text{Tokens}_{t-k}| +
u_t$$
For a subscribed user with zero marginal token cost, the **null
hypothesis** on R4-S3-USD is $\alpha_1 \approx 0$ (two-sided test):
behavior should NOT respond to FX vol because there is no marginal-cost
incentive. **Test inversion**: if $\alpha_1 \neq 0$ at significance, a
behavioral channel exists despite zero marginal cost (interesting
finding); if $\alpha_1 \approx 0$, subscription-regime token inelasticity
is empirically confirmed (the framework prior).

**CORRECTIONS-T (Quality-threshold tightening — Model QA FLAG 10).** v0.2.0
§2.1 set the R5 CI half-width threshold at $\leq 0.20$ (i.e., $\pm$20 pp).
Model QA correctly observed that a CI of $[0.30, 0.70]$ around a point
estimate of 0.50 fails to distinguish FX-vol-share from a coin flip.
**Fix**: threshold tightened to $\leq 0.15$ ($\pm$15 pp). At $T = 38$ this
is achievable for the FX-share output by bootstrap construction provided
serial correlation is not pathological.

**CORRECTIONS-U (Power-HALT anticipation — Model QA FLAG 11).** Model QA's
independent power calc at $T = 38$, HAC $L = 3$, MDES = 0.40 residual-SD
gives ~0.54–0.66 with realistic HAC small-sample inflation. The power-HALT
checkpoint is therefore a high-probability operational event, not a tail
case. **Fix**: §8 explicitly anticipates the power-HALT path; a
disposition memo template lives at `notebooks/dev_ai_cost_v2/dispositions/
power_halt_template.md` and pre-enumerates the user pivots (expand $T$ by
waiting; lower MDES to 0.30 with documented downgrade; accept lower-power
result with explicit caveat in headline).

**CORRECTIONS-V (CR FLAGs A, B, partial-`is_error`, NITs).** Five
mechanical pins:

- **Iterator → Iterable + cache** (CR FLAG A): `JSONLReader.__call__`
  return type changed from `Iterator[MessageRecord]` to
  `Sequence[MessageRecord]` (materialized list); rationale = downstream
  panel builder may iterate twice for cross-validation between aggregation
  paths; silent-empty-second-pass is a Hypothesis-property-test target.
- **`PricingTable.__call__(model, ts, toks)` ts policy** (CR FLAG B): `ts`
  IS used for time-varying price-step lookups (Anthropic price changes
  appear as effective-from dates in the LiteLLM table over time; the
  pinned SHA captures the historical step structure at the lookup
  timestamp).
- **`is_error` aggregation policy** (CR partial-CLOSE): rows with
  `is_error=True` are **dropped from cost aggregation** but retained for
  diagnostic counting (`dropped_error_count` emitted alongside
  `dropped_rows_count` on the panel). Rationale: error responses still
  consume tokens billed at the rate card, but they are not productive
  developer usage and would inflate cost-burden estimates for the cohort
  population that is the inferential target.
- **UTC boundary half-open** (CR NIT): UTC-day boundaries are half-open
  `[00:00:00, 24:00:00)` to avoid double-counting; pinned in `JSONLReader`
  contract.
- **`request_id: str | None` nullable rationale**: older Claude Code
  versions (pre-2.0.x) omitted the field; the spec accepts None for
  legacy compatibility but `JSONLReader` emits a warning when None is
  encountered.

**CORRECTIONS-W (File-existence list — RC FLAG 8 / NIT 12).** v0.2.0 §11
listed `simulations/_errors.py` as existing — confirmed to NOT exist at
the top level (only sub-package `_errors.py` files exist, following the
repo's per-sub-package error-class convention). v0.2.0 §11 also listed
`data/panels/` as existing — confirmed missing. **Fix**: §11 updated to
the actual repo state; `simulations/dev_ai_cost_v2/_errors.py` is
introduced as a new sub-package errors file per repo convention; `data/
panels/` is created by the build pipeline at first run. Also the "ccusage
/ parser" string at the §6 threat row 5 is corrected to "own-parser /
panel-builder reconciliation".

## 0.2 v0.2.1 → v0.2.2 CORRECTIONS (implementation-review patch)

v0.2.1 was approved on all three closure-only review channels and an
implementation plan (17 tasks) was emitted and partially executed (Tasks
1–8 committed at `iter/ai-cost-2026-05` HEAD `010df55`, 796/796 unit tests
passing). The Task 9 implementation-review checkpoint (Code Reviewer +
Reality Checker + Backend Architect in parallel per
`feedback_implementation_review_agents`) **REJECTED** v0.2.1 on two
production BLOCKs that per-task reviews could not have caught because they
exercised only synthetic fixtures. An empirical study of the OSS landscape
(ccusage, cc-lens, agentsview, claude-parser source code at
`scratch/2026-05-16-ai-cost-impl-review/oss_algorithm_study.md`) found
that **our v0.2.1 JSONL schema policy is the outlier** — every OSS tool
that successfully ingests Claude Code session logs uses a different
algorithm. v0.2.2 amends the spec to align with empirically-validated OSS
algorithms while preserving the rest of v0.2.1's R5/R4-S3 framework
intact.

The four CORRECTIONS-Y blocks are itemized below.

**CORRECTIONS-Y-1 (JSONL parsing — Reality Checker BLOCK A; OSS algorithm
study finding 1, 2).**

v0.2.1's `_Row` Pydantic schema demanded `costUSD` at the top level and
applied `extra="forbid"` indiscriminately to all JSONL line types.
Empirical verification on the maintainer's `~/.claude/projects/**/*.jsonl`
found:

- Real Claude Code v2.1.x JSONL has **9 distinct `type` values**
  (`assistant`, `user`, `system`, `summary`, etc.); only `assistant` rows
  carry token-usage data
- The top-level `costUSD` field is **absent in 0/355 `assistant` rows
  across 5 sampled real sessions**
- `message.usage` has six fields beyond what v0.2.1's `_Usage` declared
  (`cache_creation_input_tokens` flat field, `inference_geo`,
  `iterations`, `server_tool_use`, `service_tier`, `speed`)

Every OSS tool (ccusage, cc-lens, agentsview, claude-parser) handles this
the same way: **type-discriminate first, then parse permissively**.
v0.2.2 adopts this:

- `JSONLReader` filters for `type == "assistant"` (or
  `message.role == "assistant"` per ccusage's main fast path) BEFORE
  applying any Pydantic schema. Non-assistant rows are silently skipped.
- The Pydantic `_Row` schema is changed from `extra="forbid"` to
  **`extra="allow"`** so unknown fields do not raise. Schema drift on
  REQUIRED fields still raises; new fields appearing in future Claude
  Code versions are forward-compatible by default.
- Required fields reduced to the minimum cost-relevant set:
  `timestamp`, `message.usage.input_tokens`,
  `message.usage.output_tokens`. All other fields are optional.
- The top-level `costUSD` field is **removed from the spec entirely** —
  cost is computed from `PricingTable × usage` at parse time (per
  CORRECTIONS-Y-2), matching ccusage's default `cost_mode='calculate'`.
- Rows with `isApiErrorMessage == true` continue to be dropped from cost
  aggregation (CORRECTIONS-V `is_error` policy preserved); but
  `isApiErrorMessage` is now Optional (absent → treated as False).

**CORRECTIONS-Y-2 (Cost formula and precision boundary — Reality Checker
BLOCK B; OSS algorithm study finding 3, 4).**

v0.2.1 trusted the JSONL's `costUSD` field as the canonical notional cost
and required exact `Decimal` arithmetic end-to-end (CORRECTIONS-H
tightened reconciliation to exact match). Both decisions are reversed in
v0.2.2:

- **Cost is computed at parse time** as `Σ_cat tokens_cat × rate_cat`
  per the formula in `simulations/dev_ai_cost_v2/anthropic_pricing.PricingTable.__call__`.
- The arithmetic adopts **ccusage's `calculateTieredCost` semantics**:
  for `claude-*` models with the 200k-input-tokens-tier rate change,
  apply the base rate for `input_tokens ≤ 200_000` and the tier rate
  for the excess. ccusage's `fast` speed multiplier is OUT OF SCOPE for
  v0.2.2 (the operator does not use the `fast` mode; if it ever appears
  in a future Claude Code version it becomes a v0.2.3 amendment).
- **Precision boundary: switch from `Decimal` to `float`**. All OSS
  tools use `float`; ccusage matches LiteLLM to within ~1e-6. The
  v0.2.1 reconciliation HALT threshold of "exact-Decimal match"
  (CORRECTIONS-H) becomes **"match ccusage CLI within 0.1%"** via the
  ccusage-parity oracle test (CORRECTIONS-Y-4). The previous Decimal
  infrastructure was over-engineered relative to what real cost
  computation requires; switching reduces complexity, matches OSS
  exactly, and the sub-cent precision was not load-bearing for R5
  variance decomposition or R4-S3 vol-clustering.
- **Ephemeral 5m/1h granularity is preserved in `MessageRecord` but is
  diagnostic-only** for cost computation. v0.2.1 CORRECTIONS-D preserved
  the split because it was empirically present in the JSONL and LiteLLM
  has distinct rates. v0.2.2 discovers that all OSS tools aggregate to
  the flat `cache_creation_input_tokens` field for cost, and that the
  LiteLLM SHA pin (CORRECTIONS-Y-3) is incomplete for the 1h tier on
  the operator's most-used models. Resolution:
  - `MessageRecord.cache_create_5m: int` and
    `MessageRecord.cache_create_1h: int` fields are preserved (no breaking
    change to `_post_init__` invariants)
  - **`PricingTable.__call__` uses only the flat
    `cache_creation_input_tokens` total** for cost (sum of
    `cache_create_5m + cache_create_1h`) at the
    `cache_creation_input_token_cost` rate
  - The split fields remain available for diagnostic inspection in
    notebook EDA cells
- Schema row in §3.5 updates: `MessageRecord.cost_usd_notional: float`
  (was `Decimal`); `DailyNotionalPanel` columns
  `notional_cost_usd: pl.Float64`, `notional_cost_cop: pl.Float64`,
  `trm_cop_per_usd: pl.Float64` (was `pl.Decimal`).

**CORRECTIONS-Y-3 (LiteLLM model-coverage strategy — Reality Checker
BLOCK B; OSS algorithm study finding 4).**

v0.2.1 CORRECTIONS-O pinned LiteLLM SHA
`e58a561caa21169fb02174148444c08509ce7028` and required all five rate
keys to exist for every `claude-*` model at load time. Empirical
verification on that SHA (and a re-check on current `main` 2026-05-17)
found **6/21 `claude-*` models lack `cache_creation_input_token_cost_above_1hr`**,
including `claude-sonnet-4-5` and `claude-sonnet-4-6` — the models the
operator uses most. Bumping the SHA does not fix this.

ccusage's durable strategy (adopted in v0.2.2):

- **All rate fields are `Optional[float] = None`** in `PricingTable`'s
  in-memory representation
- **Load-time validation is RELAXED**: per-model missing keys are warned
  (count tracked in `WARN_missing_keys_count`) but do NOT raise — only
  the model entry is **gated** at `__call__` time: if a model has missing
  rates for a token category the row exercises, the cost for that
  category is **0** (matches ccusage's
  `tiered(N, base, null) = N · base` semantics, which collapses to `0`
  when `base = null`)
- **Model-lookup ladder** for missing models: exact match → provider-
  prefixed lookup (`anthropic/<model>`) → substring fallback (longest
  match). If no entry found, the row is dropped from cost aggregation
  with `dropped_unknown_model_count` warning
- The LITELLM_SHA_PINNED constant value at
  `e58a561caa21169fb02174148444c08509ce7028` is retained (no SHA bump);
  the relaxed-load policy makes the choice of SHA much less brittle

**CORRECTIONS-Y-4 (Integration test floor — Reality Checker FLAG 3; OSS
algorithm study deliverable).**

v0.2.1 had zero integration tests against real `~/.claude/projects/`
JSONL. BLOCK A would have been caught by a single such test. v0.2.2
mandates a minimum integration-test floor:

- Test fixture: `simulations/tests/fixtures/real_claude_jsonl/` —
  small (≤1 KB) sample of real Anthropic JSONL covering all 9 `type`
  values, hand-curated from the maintainer's local sessions with PII
  redacted (model names + token counts preserved; prompt content
  replaced with `<REDACTED>` placeholder)
- Test: `simulations/tests/test_real_jsonl_integration.py` — gated on
  fixture existence with `pytest.skip("fixture not present")` until
  fixture is committed, then **HARD-FAIL** thereafter (no `pytest.skip`
  bypass once the file is in the repo)
- Required assertions: (a) no exception on any line; (b) `assistant`
  rows are extracted; non-assistant rows are skipped; (c) per-message
  cost matches independent ccusage CLI invocation on the same fixture
  to within **0.1%** (the **ccusage-parity oracle test**)
- The ccusage parity oracle requires Node.js + `npx ccusage@<version>`
  available at test time; if absent, test xfails with explicit message
- The fixture is the canonical "things must keep working" regression
  contract; future schema drift in Claude Code's JSONL surfaces as a
  test failure here before it reaches production

**Reverted v0.2.1 elements (housekeeping):**

- `_Row.uuid: str` REQUIRED → relaxed to `_Row.uuid: str | None = None`.
  R6 v0.1.3 CORRECTIONS-RR/-TT requires uuid for pool canonicalization,
  but if a row legitimately lacks uuid (newer Claude Code may move it),
  fall back to `(file_path, line_no)` for that row's dedupe identity. The
  `MessageRecord.uuid: str` field's `__post_init__` empty-string
  rejection is preserved (synthesized identity is non-empty by
  construction).
- Spec §3.5 contract row for `JSONLReader.__call__` adds two new
  Optional returns: `WARN_missing_keys_count: int` and
  `dropped_unknown_model_count: int` — surfaced in the panel-builder
  output and DATA_PROVENANCE for monitoring rate-coverage drift.
  (NOTE: ownership of these counters is pinned per CORRECTIONS-Y-5 in
  §0.3 below — v0.2.2 was ambiguous between JSONLReader and PricingTable
  as carrier; v0.2.3 resolves.)

## 0.3 v0.2.2 → v0.2.3 CORRECTIONS (architectural-pin patch)

v0.2.2 closed both v0.2.1 implementation BLOCKs (A: JSONL parsing; B:
LiteLLM coverage) via CORRECTIONS-Y-1 through Y-4. Wave 2 Code Reviewer's
closure-only review on v0.2.2 surfaced 6 NEW BLOCKs (CR-Z-1 through -6) —
all spec-rooted architectural ambiguities that v0.2.2 introduced when
amending §3.5 contracts. v0.2.3 is a contract-only patch resolving these
+ folding in Wave 2 Model QA's non-blocking π̂ diagnostic FLAG. No
methodology change.

**CORRECTIONS-Y-5 (Architectural pins for v0.2.2 contracts — 6 sub-pins
addressing CR-Z-1 through CR-Z-6).**

**Y-5a (CR-Z-1: WARN_missing_keys_count ownership).** v0.2.2 §3.5 claimed
this counter on both `JSONLReader` and `PricingTable`. Per tier discipline
they cannot share state. **Resolution**: the counter lives on
**`PricingTable`** (the layer that knows about LiteLLM rate-key absence).
`JSONLReader` carries an analogous but DIFFERENT counter
`dropped_non_assistant_count: int` (number of JSONL rows skipped because
`type != "assistant"`). The two counters are surfaced separately in
`DailyNotionalPanel` and DATA_PROVENANCE. §3.5 contract rows updated
accordingly.

**Y-5b (CR-Z-2: JSONLReadResult tier assignment).** v0.2.2 introduced
`JSONLReadResult` as a frozen-dc return from `JSONLReader.__call__`
without §3.5 row or tier placement. **Resolution**: `JSONLReadResult` is a
**types-tier** frozen-dc defined in `simulations/dev_ai_cost_v2/types.py`
alongside `MessageRecord`, `TokensByCategory`, and `DailyNotionalPanel`.
Fields: `records: Sequence[MessageRecord]`, `dropped_non_assistant_count:
int`. (The `WARN_missing_keys_count` and `dropped_unknown_model_count`
counters live on `PricingTable` per Y-5a, NOT on `JSONLReadResult`.) §3.5
gains a new row for `JSONLReadResult`.

**Y-5c (CR-Z-3: cache 5m+1h aggregation locus).** v0.2.2 said the
ephemeral split is preserved in `MessageRecord` but aggregated for cost
without specifying WHERE the aggregation happens. **Resolution**:
aggregation happens **inside `PricingTable.__call__` body only**.
`TokensByCategory.__init__` does NOT mutate inputs (Value-tier
immutability rule). `PricingTable.__call__(model, ts, toks)` reads
`toks.cache_create_5m + toks.cache_create_1h` and multiplies by the single
`cache_creation_input_token_cost` rate per CORRECTIONS-Y-2. The
`TokensByCategory` Value carries the split intact for any consumer that
wants it (diagnostic notebooks).

**Y-5d (CR-Z-4: longest-substring tiebreaker).** v0.2.2 §3.5 specified a
model-lookup ladder ending in "longest-substring fallback" without
disambiguating equal-length matches. **Resolution**: when multiple model
keys in the LiteLLM table share the maximum substring overlap with the
requested model, **the alphabetically-smallest key wins** (Python
`min(candidates)` semantics). This is deterministic across runs.
Documented in §3.5 PricingTable row + emit a `multiple_substring_match_warning`
counter on `PricingTable` for any row where the tiebreaker was invoked.

**Y-5e (CR-Z-5: uuid synthesis hardened).** v0.2.2 §3.5 said
`MessageRecord.uuid` synthesizes from `(file_path, line_no)` when absent
in JSONL. This breaks under directory or file rename → R6 v0.1.3
CORRECTIONS-RR/-TT pool canonicalization hash drift (false positive).
**Resolution**: synthesized uuid =
`"synth-sha256:" + sha256(file_basename + ":" + line_no_zfill_8).hexdigest()[:16]`
where `file_basename` strips both directory path and any user-specific
prefix (so `~/.claude/projects/<some-uuid>/session.jsonl` → `session`).
The `synth-` prefix flags the uuid as parser-synthesized vs
Anthropic-emitted, so R6 canonicalization can split-and-warn instead of
silently mixing the two. Per CORRECTIONS-Y-1 the JSONL `uuid` field is
treated as optional (`uuid: str | None`) at the Pydantic layer; if absent,
the synthesis above runs in `JSONLReader._construct_message_record`. R6
v0.1.3's canonicalization invariant is preserved because basename + line_no
is stable under rename of containing directories (which is what Claude
Code does over time as it reorganizes `~/.claude/projects/`).

**Y-5f (CR-Z-6: migration enumeration + Task 9.5).** v0.2.2 amends §3.5
contracts but does not enumerate which v0.2.1-implementation files (Tasks
1-8 committed code) must change to comply. **Resolution**: v0.2.3 inserts
a new **Task 9.5** in the v0.2.1 plan (to be added by a follow-up
plan-emission task) covering the migration:

| File to modify | What changes |
|---|---|
| `simulations/dev_ai_cost_v2/jsonl_io.py` | Add type-discriminator (`type == "assistant"` filter); switch `_Row` Pydantic to `extra="allow"`; reduce required fields to `timestamp + message.usage.{input_tokens, output_tokens}`; remove `_Row.costUSD`; make `_Row.uuid: str \| None`; add `_construct_message_record` with uuid-synthesis fallback per Y-5e; return new `JSONLReadResult` dataclass with `records` + `dropped_non_assistant_count` |
| `simulations/dev_ai_cost_v2/types.py` | Change `MessageRecord.cost_usd_notional: Decimal → float`; add `JSONLReadResult` frozen-dc; change `DailyNotionalPanel` schema cols (`notional_cost_usd`, `notional_cost_cop`, `trm_cop_per_usd`) to `pl.Float64`; **add `MessageRecord.ephemeral_pi_share` Optional field** for Y-6 π̂ diagnostic |
| `simulations/dev_ai_cost_v2/anthropic_pricing.py` | All rate fields `Optional[float] = None`; relax load-time validation (WARN-not-raise on missing key); add model-lookup ladder with alphabetical tiebreaker (Y-5d); add `WARN_missing_keys_count`, `dropped_unknown_model_count`, `multiple_substring_match_warning` counters; aggregate `cache_create_5m + cache_create_1h` inside `__call__` body (Y-5c); apply 200k-tier pricing per Anthropic; remove dead `_content_digest_unused` lines (Task 6 I-1) |
| `simulations/dev_ai_cost_v2/panel_builder.py` | Update `DailyNotionalPanel` schema validation for Float64 cols; thread `dropped_non_assistant_count` from `JSONLReadResult` and `WARN_missing_keys_count` / `dropped_unknown_model_count` / `multiple_substring_match_warning` from `PricingTable` into the returned panel + DATA_PROVENANCE |
| `simulations/tests/strategies.py` | Update `message_records` strategy: `cost_usd_notional` strategy switches to `st.floats(min_value=0.0, max_value=1000.0)`; `uuid` strategy may emit `None` to exercise the synthesis path |
| `simulations/tests/test_dev_ai_cost_v2_*.py` | Update fixtures for new schemas; add tests for the 6 CR-Z pins (counter ownership; aggregation locus; tiebreaker determinism; uuid synthesis stability under rename; etc.) |
| `simulations/tests/fixtures/real_claude_jsonl/` | NEW: small PII-redacted sample per CORRECTIONS-Y-4 |
| `simulations/tests/test_real_jsonl_integration.py` | NEW: ccusage-parity oracle |
| `scripts/build_notional_cost_panel.py` | Rename CLI internal `records` variable → `read_result`; update docstring to reflect `JSONLReadResult` return + counter threading; thread the 4 PricingTable counters (`WARN_missing_keys_count`, `dropped_unknown_model_count`, `multiple_substring_match_warning`) + `JSONLReadResult.dropped_non_assistant_count` into the `[OK]` print line and into DATA_PROVENANCE.md per Y-5a (RC v0.2.3 closure note: signature of `PricingTable.from_litellm_sha` is unchanged so no positional-arg breakage) |

Task 9.5 exit criteria: (i) all 6 CR-Z BLOCKs verified closed by spec-compliance review; (ii) regression suite green; (iii) ccusage-parity oracle passes on the real JSONL fixture; (iv) impl-review checkpoint re-runs with updated code.

**CORRECTIONS-Y-6 (Model QA π̂ ephemeral diagnostic — non-blocking
FLAG closure).** Wave 2 Model QA noted that aggregating cache_create_5m
and cache_create_1h at the 5m rate produces a **multiplicative scale bias
on cost levels** (underestimates by ~2× the fraction of cache_create_1h
in the total). The variance of log-returns is scale-invariant so R5
FX-share and R4-S3 HAC coefficients are unaffected; however cost-burden
*magnitudes* in §2.1 outputs are biased downward by the corresponding
factor. **Resolution**: surface
$\hat\pi \equiv \Sigma \text{cache\_create\_1h} / \Sigma (\text{cache\_create\_5m} + \text{cache\_create\_1h})$
as a DATA_PROVENANCE diagnostic and as a panel-level scalar attached to
`DailyNotionalPanel.ephemeral_pi_share`. The §2.1 R5 headline output
narrative gains a sentence: "Reported cost magnitudes apply the 5m
ephemeral rate to total cache-creation tokens; the true cost is up to a
factor of (1 + π̂·(rate_1h/rate_5m − 1)) higher (rate_1h ≈ 2·rate_5m per
LiteLLM published rates where present). The point estimate for the
FX-share is variance-based and is NOT affected by this bias."

## 0.4 v0.2.3 → v0.2.4 CORRECTIONS (real-data HALT patch)

v0.2.3 closed all 6 CR-Z architectural BLOCKs. The first production run of
`scripts/build_notional_cost_panel.py` against the operator's real
`~/.claude/projects/` corpus surfaced one more spec-vs-data contradiction:
filesystem-level partial-write corruption produces JSONL files with valid
prefix lines + trailing null-byte blocks. Our parser raised
`JSONLSchemaError` on the first such file (`agent-af5e1160f7be358ba.jsonl`
line 586 = ~3 KB of `\0`). Disposition memo:
`notebooks/dev_ai_cost_v2/dispositions/2026-05-17-task10-trailing-null-bytes.md`.
User-selected pivot: **Option A (ccusage-mirror)**. v0.2.4 is a contract-only
patch closing this gap.

**CORRECTIONS-Y-7 (Line-level malformed-skip — Task 10 production HALT).**

v0.2.3 CORRECTIONS-Y-1 made the Pydantic schema permissive (`extra="allow"`)
for *valid* JSON lines, but the OSS algorithm study (ccusage) also handles
line-level malformed input via `try { JSON.parse(line) } catch { continue }`.
Our v0.2.3 mirror inherited only the schema half; the line-level half is
added here. The contract:

- `JSONLReader.__call__` wraps the per-line `json.loads` in a
  `try/except json.JSONDecodeError` that **silently skips** the offending
  line and increments a new counter `dropped_malformed_line_count: int`.
  Schema errors on *valid* JSON (missing required fields, wrong types) still
  raise `JSONLSchemaError` — the relaxation is scoped to lines that aren't
  even parseable as JSON.
- The blank-line skip continues to apply BEFORE the JSON-decode attempt, so
  empty / whitespace-only lines still cost zero counter ticks. Lines made of
  null bytes (`\0\0...`) are NOT stripped by `str.strip()`, so they fall
  through to the JSON-decode attempt → fail → increment
  `dropped_malformed_line_count`. This is intentional: distinguishing
  "filesystem corruption" from "producer-side malformed JSON" is not
  empirically tractable (a partial-write can also produce truncated
  printable JSON like `{"foo`), so we treat both as the same operational
  signal.
- The counter is surfaced on `JSONLReadResult` (Y-5b tier placement —
  types-tier), threaded through `panel_builder.build_daily_panel` into the
  returned `DailyNotionalPanel`, and emitted in
  `scripts/build_notional_cost_panel.py`'s `[OK]` print line and the
  DATA_PROVENANCE.md record. The 6 existing counters (3 panel-builder
  drops + 3 PricingTable counters) become 7.

**Risk and observability.** Silent-skip can mask genuine producer-side
schema regressions (e.g., a future Claude Code release that emits a new
top-level structure that our `_Row` schema rejects). Mitigation is the
counter itself: if `dropped_malformed_line_count > 0` on the first
production run, that is operationally OK (filesystem corruption is
real-world). If the counter starts trending up across reruns, that is the
signal to investigate producer-side schema drift — Y-4's
`test_real_jsonl_integration.py` will catch genuine producer regressions
because the canonical fixture lines are valid JSON.

**Test surface added** (Task 10.5 — minor migration):

- `test_jsonlreader_skips_trailing_null_bytes` — file with 3 valid
  assistant lines + trailing `b"\x00" * 3000` parses cleanly, returns 3
  records, `dropped_malformed_line_count == 1`.
- `test_jsonlreader_skips_truncated_json` — file ending mid-JSON
  (`{"type":"assistant","timestamp":"2026-...`) returns valid prefix,
  `dropped_malformed_line_count == 1`.
- `test_dropped_malformed_line_count_threaded_through_panel` — counter
  surfaces on `DailyNotionalPanel.dropped_malformed_line_count`.
- `test_jsonlreader_blank_lines_do_not_increment_malformed_counter`
  (RC FLAG-4a non-over-correction commitment) — file with mix of blank
  and valid lines leaves `dropped_malformed_line_count == 0`.
- `test_jsonlreader_valid_json_invalid_schema_still_raises` (RC FLAG-4b
  non-over-correction commitment) — file with valid JSON but missing
  required field still raises `JSONLSchemaError`; the JSONDecodeError
  catch did NOT widen to swallow schema errors.
- `test_jsonlreader_line_conservation_property` (CR-7-N2 Hypothesis) —
  for any random byte-string input, the invariant
  `dropped_malformed_line_count + len(records) + dropped_non_assistant_count + dropped_blank == total_input_lines`
  holds; the reader never loses or double-counts a line.

**Deferred to v0.2.5 (RC FLAG-5a / FLAG-5b — out of scope for the HALT
patch).** No quantitative hard-fail threshold on
`dropped_malformed_line_count / total_lines` is pinned here because there
is no corpus-baseline yet to non-arbitrarily set the threshold; the first
run on the operator's real corpus establishes that baseline and v0.2.5
will fold in a threshold informed by the empirical distribution. The
DATA_PROVENANCE schema row enumerating Y-7's new counter is left to the
v0.2.5 housekeeping amendment alongside the threshold pin.

**Anti-fishing invariant carried.** This is a spec-vs-data contradiction
patched per the HALT chain (HALT → disposition → user pivot → CORRECTIONS
block → 2-wave review → impl + tests → re-run Task 10 → post-hoc
impl-review). No iteration parameters change (R5 / R4-S3 framework intact;
N_MIN floor intact; MDES intact). Methodology is unchanged.

## 0.5 v0.2.4 → v0.2.5 CORRECTIONS (reliability-convergence patch)

v0.2.4 closed the line-level robustness gap and Task 10 produced its first
production panel. Direct comparison of that panel to `npx ccusage daily`
on the operator's `~/.claude/projects/` corpus surfaced a **~2.11× cost
overcount** (ours $5,903.87 vs ccusage $2,789.64 on 27 overlapping days).
That gap is far outside the v0.2.2 CORRECTIONS-Y-2 / Y-4 ccusage-parity
target of 0.1%. Empirical investigation (saved at
`scratch/2026-05-17-v0_2_5-dedup-discovery/findings.md`) identified the
single dominant root cause and validated the fix; v0.2.5 is a contract-only
patch closing it.

**CORRECTIONS-Y-8 (uniqueHash dedup — Task 10 reliability HALT).**

Direct inspection of ccusage's compiled source (`data-loader-LJFbLyZj.js`,
function `Wr` for the key, `Sr` + `$` for the keep-larger rule, `ui` for
per-file dedup and `pi` for cross-file dedup) shows that **every Anthropic
message id is logged multiple times** by Claude Code (streaming chunks +
iteration entries within a single tool-use loop), and ccusage's dedup
discipline keeps **only one row per `${message.id}:${requestId}` —
specifically the row with the largest sum of all four token fields**
(`input + output + cache_creation + cache_read`). Our v0.2.4 `JSONLReader`
counts every row, so on the operator's corpus we overcount by ~2×.

Empirical validation on the operator's real `~/.claude/projects/` corpus:

- Per-file uniqueness ratio on a single representative session: 1,079
  assistant rows → 551 unique hashes (1.96× duplication WITHIN a single
  file); subagents 5,387 rows → 3,085 unique hashes (1.75×); union
  6,466 → 3,636 (1.78×). Cross-file UUID overlap (Anthropic-emitted
  `uuid`) is 0; the duplication is keyed on `message.id:requestId`, not on
  `uuid`.
- Corpus-wide with dedup: cost $5,037.52 vs ccusage $5,155.80 →
  **ratio 0.977** (was 2.11). Output / cache_create / cache_read all
  converge to within ~2.3% of ccusage as well.
- One residual anomaly (Y-8 does NOT close): input_tokens is 0.10× of
  ccusage post-dedup, an order-of-magnitude shortfall. Hypothesis (filed
  to v0.2.6 backlog Y-9): ccusage may aggregate `usage.iterations[i].input_tokens`
  across the inner array; our parser reads only top-level
  `usage.input_tokens`. The R5 / R4-S3 framework's cost magnitudes are
  dominated by output + cache tokens (input is ~0.02% of total cost in
  the empirical data), so this residual does NOT block the v0.2.5
  cost-reliability convergence. Surfaced for follow-up.

**Spec change (contract-only):**

- `JSONLReader.__call__` adds an in-memory dedup map keyed on
  `_unique_hash(message.id, requestId)` → index of currently-kept entry.
  `_unique_hash` = `f"{message.id}:{requestId}"` when `requestId` is
  present; else `message.id`; else `None` (row skipped from dedup but
  still admitted into output for fault-tolerance — a missing message.id
  is rare in real data and our v0.2.3 Y-1 already requires assistant
  rows to be parseable). **Mutability scope (CR NIT-1)**: the dedup map
  is a local variable inside `__call__`, *not* instance state on
  `JSONLReader`; the reader remains stateless per IO Boundary tier
  discipline — each call produces an independent dedup map that goes out
  of scope when the call returns.
- Keep-largest rule per ccusage `Sr` + `$`:
  `tokenTotal = input + output + (cache_creation_input_tokens ?? 0) + (cache_read_input_tokens ?? 0)`.
  When a duplicate hash appears with **strictly larger** `tokenTotal`,
  replace the kept entry; when equal `tokenTotal` and the new entry has
  `usage.speed != None` while the kept does not, replace (ccusage
  `hasSpeed` tiebreaker); otherwise skip.
- New counter `dropped_duplicate_count: int` on `JSONLReadResult`
  (types-tier, Y-5b precedent). **Increment rule (CR NIT-3 — pinned for
  the impl patch's field docstring)**: the counter increments on EVERY
  collision of a `_unique_hash` that has been seen before, whether the
  new row supersedes the kept entry (replacement) or is dropped (the
  kept entry was larger or tied without `hasSpeed`). Equivalently:
  `dropped_duplicate_count == raw_assistant_rows_admitted - len(records)`.
  Threaded through `panel_builder.build_daily_panel` →
  `DailyNotionalPanel.dropped_duplicate_count` → CLI emission and
  DATA_PROVENANCE per Y-5a discipline. The 7 existing counters
  (`dropped_rows_count`, `dropped_error_count`,
  `dropped_non_assistant_count`, `dropped_malformed_line_count`,
  `WARN_missing_keys_count`, `dropped_unknown_model_count`,
  `multiple_substring_match_warning`) become 8; π̂ unchanged.

**OSS-mirror provenance.** The OSS algorithm study at
`scratch/2026-05-16-ai-cost-impl-review/oss_algorithm_study.md` correctly
identified ccusage's permissive parsing (v0.2.2 Y-1) but did NOT identify
the cross-file dedup discipline (it was not load-bearing for the
operator's earlier small-corpus tests, but is the dominant correctness
issue at production scale). Y-8 is the closure for that gap. ccusage
source citations: `Wr` (uniqueHash function), `Sr` (tokenTotal), `$`
(keep-larger), `ui` (per-file dedup), `pi` (cross-file dedup +
aggregation), all in `node_modules/ccusage/dist/data-loader-LJFbLyZj.js`
at ccusage version 19.0.3.

**Test surface added** (Task 10.6 — minor migration):

- `test_jsonlreader_dedup_within_file` — single file with 3 rows sharing
  `message.id=msg_1, requestId=req_1` but differing `tokenTotal`
  (200/500/300). Assert 1 record kept; the one with `tokenTotal=500`.
  `dropped_duplicate_count == 2`.
- `test_jsonlreader_dedup_across_files` — two files each with the same
  uniqueHash; row in file B has larger tokenTotal. Assert single kept
  entry == row from file B (regardless of file-traversal order).
  `dropped_duplicate_count == 1`.
- `test_jsonlreader_dedup_hasspeed_tiebreaker` — two rows with same hash
  and same tokenTotal; one has `usage.speed="standard"`, the other has
  no `speed` field. Assert kept entry is the one with `speed`.
- `test_jsonlreader_dedup_no_request_id_falls_back_to_message_id` —
  rows with `requestId=None` dedup by `message.id` alone.
- `test_jsonlreader_dedup_traversal_order_invariant` (Hypothesis) —
  generate a multi-file fixture with arbitrary uniqueHash collisions;
  permute the file-traversal order; assert the kept-entry set is
  identical across permutations (the "best entry per uniqueHash"
  invariant).
- `test_dropped_duplicate_count_threaded_through_panel` — counter
  surfaces on `DailyNotionalPanel.dropped_duplicate_count`.
- `test_jsonlreader_dedup_field_atomicity` (RC FLAG-A) — two rows with
  the same uniqueHash but DIFFERING `model`, `timestamp`, and token
  fields; the row with the larger `tokenTotal` wins on EVERY field
  (no Frankenstein-mixing across rows). Mirrors ccusage `i[p] = h`
  whole-record replacement semantics.
- `test_jsonlreader_dedup_missing_message_id_admitted_without_counter`
  (RC FLAG-B / CR optional-7th) — rows with `message.id == None` are
  admitted into the output without dedup AND do NOT increment
  `dropped_duplicate_count` (the counter only ticks on actual hash
  collisions; `None`-hash rows bypass the dedup map entirely).

**Anti-fishing invariant carried.** This is a spec-vs-data contradiction
patched per the HALT chain (production data parity check → empirical
root-cause investigation → user pivot → CORRECTIONS block → 2-wave review
→ impl + tests → re-run Task 10 → post-hoc impl-review). No iteration
parameters change (R5 / R4-S3 framework intact; N_MIN floor intact; MDES
intact). Methodology unchanged; reliability discipline strengthened.

**Backlog (Y-9, v0.2.6 candidate).** The residual ~2.3% gap on
output/cc/cr (uniform across categories) and the 0.10× input_tokens
anomaly need separate investigation. Working hypotheses: (a) ccusage may
sum `usage.iterations[i].input_tokens` across the inner iteration array;
(b) the 136 `dropped_unknown_model` rows may be priced by ccusage via a
fallback that we drop; (c) `hasSpeed` tiebreaker behavior on equal
tokenTotals may select differently in edge cases. None are load-bearing
for v0.2.5's primary cost-convergence goal; filed for follow-up after Y-8
lands and is verified.

**Parity-target status (CR NIT-4).** v0.2.5 Y-8 closes the dominant root
cause and brings cost from 211% over to 2.3% over ccusage — but the
v0.2.2 CORRECTIONS-Y-2 / Y-4 ccusage-parity-0.1% criterion is **NOT yet
satisfied**. Y-9 must close the residual before §2.1 R5 verdict-table
eligibility (the R5 stationary-bootstrap output must be backed by data
that matches ccusage to within 0.1% on cost, per the spec contract). Task
10 produces a working panel for downstream EDA / power-measurement at
v0.2.5; verdict-eligible R5/R4-S3 outputs require Y-9 closure.

## 1. Purpose and framework placement

### 1.1 Goal

Quantify the COP-denominated cost-burden risk that a **non-subscribed LATAM
developer** would face for AI-tooling usage equivalent to the pilot
subject's pattern, and isolate the share of that risk attributable to
COP/USD volatility.

### 1.2 Why "non-subscribed"

The framework's target population (LATAM wage-earners attempting the
wage→capital transition) cannot afford Pro/Max subscriptions; their relevant
cost rail is pay-per-API. The pilot subject (repo maintainer) is on
subscription, so their *actual* USD cost is flat per month and FX exposure
collapses to subscription_fee × USDCOP at monthly billing day — too few
observations for daily-frequency econometrics and not the binding risk for
the target population.

Their **notional** cost path (rate card × token usage = `costUSD` in JSONL)
serves as a **fair proxy** for what a non-subscribed dev would have paid for
the same usage pattern. The proxy assumes equivalent demand under both
billing regimes — which is itself a strong assumption documented in §6
threats.

### 1.3 Stage in the (Y, M, X) framework

This iteration is a **candidate-X identification step**, not a (Y, M, X)
triple. PASS opens the M-design step (Panoptic-eligible long-USDCOP-vol
position funded by COP-wage premium); FAIL closes the FX-vol channel of the
AI-cost transmission only, not the broader AI-cost transmission channel.

### 1.4 Connection to prior dev-AI FAIL

The dev-AI Stage-1 iteration on Section J narrow ICT employment share
(`memory/project_dev_ai_section_j_fail.md`) closed FAIL 2026-05-06 with sign-
flipped β. That iteration tested whether COP devaluation **expands**
sectoral employment; this iteration tests whether COP vol drives sectoral
**cost burden**. Distinct transmission channels, distinct LHSs, distinct
econometric machinery.

## 2. Pre-registered framework

### 2.1 R5 — descriptive counterfactual risk quantification (PRIMARY)

**Role (CORRECTIONS-R, pinned)**: R5's role is **(A) individual-sizing**.
The headline output quantifies "for this usage pattern at this notional
dollar volume, the M-design hedge position must absorb $Y$ COP of monthly
cost-burden variance" — a quantity the M-design step consumes directly. R5
does NOT claim to establish channel existence; that follows from R4-S3-USD
behavioral evidence (§2.2.B) if $\alpha_1 \neq 0$.

**Goal**: a number with bootstrap confidence interval describing the FX-vol
share of monthly COP cost-burden risk for the proxy usage pattern.

**Inputs (constructed, not estimated)**:

- $\text{NotionalCost}^{USD}_t$ — daily notional USD cost computed as
  $\sum_{\text{msg} \in t} \text{rate}_{\text{model}, \text{cat}}(t) \cdot
  \text{tokens}_{\text{cat}}$ over the five token categories preserved per
  message: input, output, cache_creation_ephemeral_5m,
  cache_creation_ephemeral_1h, cache_read — using the LiteLLM
  SHA-pinned rate table (§5.2), with $t$-dependent rate lookups capturing
  the table's price-step structure over time.
- $\text{NotionalCost}^{COP}_t = \text{NotionalCost}^{USD}_t \cdot
  \text{USDCOP}_t$
- $\text{USDCOP}_t$ — daily Banrep TRM (prerequisite: §3.4 daily fetcher).

**Outputs (each with 90% stationary-bootstrap CI, $B = 10{,}000$,
Politis-Romano with expected block length $\lceil T^{1/3} \rceil$ —
CORRECTIONS-P)**:

1. $\hat\sigma_{\Delta\ln\text{NotionalCost}^{COP}}$ — realized vol of daily
   notional COP cost burden.
2. $\hat{\text{VaR}}_{0.05}^{\text{monthly}}$ — empirical 5% monthly VaR of
   COP cost burden over the observed window.
3. **Variance decomposition** with **conservative covariance attribution
   (CORRECTIONS-Q)** — the covariance term is reported **separately**, not
   attributed to either share:
   $$\text{Var}(\Delta\ln\text{NotionalCost}^{COP}) =
   \underbrace{\text{Var}(\Delta\ln\text{NotionalCost}^{USD})}_{\text{usage
   share}} + \underbrace{\text{Var}(\Delta\ln\text{USDCOP})}_{\text{FX
   share}} +
   \underbrace{2\,\text{Cov}(\Delta\ln\text{NotionalCost}^{USD},
   \Delta\ln\text{USDCOP})}_{\text{covariance, reported separately}}$$
   Headline FX share = $\text{Var}(\Delta\ln \text{USDCOP}) /
   \text{Var}(\Delta\ln\text{NotionalCost}^{COP})$ **excluding** the
   covariance term. Rationale: conservative for the M-design gate; positive
   covariance under alternative attributions would inflate the apparent FX
   share. The covariance is reported as a separate diagnostic with its own
   bootstrap CI.
4. **Counterfactual scenarios** (held-constant analyses):
   - "FX held constant at sample mean" → token/model-only vol path
   - "Tokens held constant at sample-mean daily usage" → FX-only vol path,
     informationally equivalent to Banrep's TRM panel scaled by a constant;
     used for **individual-sizing of the M-design hedge** (Role A per
     CORRECTIONS-R), not for channel existence.
5. **Headline output**: "for $X notional monthly burn, the FX-vol-induced
   share of monthly COP cost-burden variance is $Y\%$, 90% stationary-
   bootstrap CI $[a, b]$. Covariance term separately = $Z$ percentage
   points (positive ⇒ FX and usage co-move, additional risk; negative ⇒
   natural hedge effect)."

**Why R5 avoids the v0.1.0 identification trap**: no $\beta$ is being
estimated. Outputs are summary statistics of a deterministic transformation;
the algebraic identity that doomed v0.1.0 is here a feature (it makes
$\hat\sigma$ exactly computable) rather than a bug. Descriptive statistics
are well-defined at n=1; the stationary bootstrap (Politis & Romano 1994)
absorbs small-sample uncertainty while respecting serial correlation in the
daily absolute-return series.

**Verdict logic (R5)**: there is no PASS/FAIL on R5 because no hypothesis is
tested. R5 produces a number that the M-design step consumes. Pre-pinned
quality thresholds for the number to be M-design-usable:

| Criterion | Threshold | Source |
|---|---|---|
| Stationary-bootstrap CI half-width on FX-vol share | $\leq 0.15$ ($\pm 15$ pp) — CORRECTIONS-T | tighter than v0.2.0's $\leq 0.20$; required for non-coin-flip discrimination |
| Sample size | $N \geq 38$ weekday-days (§2.3) | CORRECTIONS-G |
| Reconciliation between own-parser raw totals and panel-builder daily aggregates | **ccusage-parity within 0.1%** on cost (per CORRECTIONS-Y-2 / Y-4; supersedes v0.2.1 exact-Decimal); exact-Decimal still required on token counts (integers) | §4 |

### 2.2 R4-Stage-3 — vol-clustering regressions (AUXILIARY)

v0.2.1 splits R4-S3 into **two specifications** per CORRECTIONS-S
(addressing Model QA FLAG 7): R4-S3-COP (consistency check, NOT a novel
finding) and R4-S3-USD (the actual behavioral test that the framework
cares about).

#### 2.2.A R4-S3-COP — consistency check (NOT a novel finding)

**Specification:**
$$|\Delta\ln\text{NotionalCost}^{COP}_t| = \alpha_0^{COP} + \alpha_1^{COP}
|\Delta\ln\text{USDCOP}_{t-k}| + \alpha_2^{COP} |\Delta\ln\text{Tokens}_{t-k}|
+ u_t^{COP}$$

with $k = 1$ primary, $k = 5$ sensitivity. **Pre-pinned**:
$\alpha_1^{COP} > 0$ one-sided.

**Why this is a consistency check and not a novel finding (CORRECTIONS-S)**:
under subscription regime the NotionalCost$^{USD}$ side has bounded
variation (token elasticity to FX is the open question, not the test
content), so $|\Delta\ln\text{NotionalCost}^{COP}|$ is dominated by
$|\Delta\ln\text{USDCOP}|$. Confirming $\alpha_1^{COP} > 0$ here recovers a
well-established USDCOP vol-clustering stylized fact (independent of AI-cost
transmission). The arm is included to verify pipeline integrity (vol
properly propagates through the panel-builder); it has **no framework-
graduation authority**.

**Verdict on R4-S3-COP**: CONSISTENCY-PASS if $\hat\alpha_1^{COP} > 0$ at
$p_{\text{one-sided}} < 0.05$; CONSISTENCY-FAIL otherwise. A consistency-
fail HALTs the pipeline (suspect data corruption), not the framework.

#### 2.2.B R4-S3-USD — behavioral subscription-inelasticity test (the framework-relevant arm)

**Specification** (CORRECTIONS-S):
$$|\Delta\ln\text{NotionalCost}^{USD}_t| = \alpha_0^{USD} + \alpha_1^{USD}
|\Delta\ln\text{USDCOP}_{t-k}| + \alpha_2^{USD}
|\Delta\ln\text{Tokens}_{t-k}| + u_t^{USD}$$

with $k = 1$ primary, $k = 5$ sensitivity.

**Pre-pinned null and test geometry**:

| Coefficient | Null | Test geometry | Interpretation |
|---|---|---|---|
| $\alpha_1^{USD}$ | $= 0$ | **two-sided** primary test | subscription regime → zero marginal cost → behavior should NOT respond to FX vol. **Rejecting the null** (either direction) reveals a behavioral channel despite zero marginal cost. **Failing to reject** confirms subscription-regime token inelasticity (framework prior). |
| $\alpha_0^{USD}$ | $> 0$ | n/a | baseline USD-side cost vol from daily token-volume variation |
| $\alpha_2^{USD}$ | ambiguous | two-sided diagnostic | past token vol predicts USD-side cost vol (mechanical) |

**Test inversion is deliberate**. Under the project's anti-fishing protocol
the pre-registered direction is "null cannot be rejected" (inelasticity). A
two-sided rejection is itself an informative finding (behavioral channel
exists). Neither outcome triggers FAIL routing in the (Y, M, X) framework;
both inform the M-design step's behavioral assumptions.

**HAC bandwidth (CORRECTIONS-I)**: Newey-West with $L = \lfloor T^{1/3}
\rfloor$ pinned ex-ante. At $T = 38$, $L = 3$. At $T = 75$, $L = 4$. The
v0.1.0 fixed $L = 12$ is rejected because it was mis-transferred from
monthly-cadence Pair-D precedent.

**Power calculation (CORRECTIONS-J + CORRECTIONS-U)**: power Monte-Carlo'd
on **residual SD** of $|\Delta\ln\text{NotionalCost}^{USD}|$ after
partialling out $|\Delta\ln\text{Tokens}|$. Power-HALT checkpoint in
`01_data_eda.ipynb` if measured power at MDES = 0.40 residual-SD with
current $T$ falls below 0.50. Per CORRECTIONS-U, **expect the power-HALT to
fire at $T = 38$** (~0.54–0.66 with HAC small-sample inflation); §8 routes
this anticipated event through a pre-enumerated disposition memo at
`notebooks/dev_ai_cost_v2/dispositions/power_halt_template.md`.

**Verdict logic (R4-S3-USD)**:

- **REJECT_NULL** = $|\hat\alpha_1^{USD}| > 0$ at $p_{\text{two-sided}} <
  0.05$ with HAC ($L = \lfloor T^{1/3} \rfloor$), AND $N \geq 38$ weekdays,
  AND measured power $\geq 0.50$ at MDES = 0.40 residual-SD. Interpretation
  = behavioral channel exists despite subscription.
- **FAIL_TO_REJECT** = $p_{\text{two-sided}} \geq 0.05$ with all other gates
  passed. Interpretation = subscription-regime inelasticity confirmed
  (framework prior).
- **HALT** = power-floor violated (anticipated per CORRECTIONS-U); any
  data-reconciliation or file-existence check fails.

### 2.3 Sample floor

$N = \max(\text{weekday days observed}) \approx 38$ at v0.2.0 spec
write time, growing with maintainer's continued Claude Code usage.

CORRECTIONS-G documents this deviation from the project default $N = 75$.
The deviation is permissible because:

- R5 (primary) is descriptive with bootstrap CIs; no hypothesis test, no
  power floor.
- R4-S3 (auxiliary) has a one-sided pre-pinned hypothesis; power floor
  lowered to $0.50$ with mandatory power-measurement HALT-checkpoint.

The pilot is explicitly **demonstration-grade**. Population inference is
deferred to the cohort-recruitment sub-project.

### 2.4 Sensitivity arms (pre-registered, diagnostic-only — no verdict authority)

CORRECTIONS-K (addressing Model QA BLOCK 8 / prior-FAIL §5.5/§9.6
contradiction): all sensitivity arms in v0.2.0 are explicitly classified
DIAGNOSTIC. They do not have escalation authority; they cannot rescue a
FAIL into a PASS or flip a PASS to a FAIL. Their role is to surface
robustness or measurement-error concerns for the disposition memo.

| Arm | Spec | Role |
|---|---|---|
| Lag $k=5$ | R4-S3 with $k=5$ instead of $k=1$ | weekly-horizon robustness |
| Model-fixed subset | R4-S3 restricted to days with single dominant model | model-mix endogeneity check |
| Pre-/post-price-step regime split | R4-S3 split at documented LiteLLM SHA-pinned price-step dates | rate-card-change robustness |
| Outlier-trimmed | R4-S3 with top/bottom 1% of $|\Delta\ln\text{Tokens}|$ trimmed | usage-spike sensitivity |

No arm has verdict authority. Period.

## 3. Data architecture

### 3.1 Tooling decision (locked v0.2.1)

**Parser substrate = own Python parser** (~150 LoC, sub-package
`simulations/dev_ai_cost_v2/`). CORRECTIONS-N: v0.2.0's primary substrate
`claude-parser==2.0.0` failed the 30-min ephemeral-split verification gate
(its `NormalizedMessage` schema lacks `usage` / `cache_creation` /
ephemeral fields entirely; billing uses a hardcoded Jan-2025 dict with a
125%-of-input cache heuristic). The own-parser is the only viable
substrate.

Implementation scope: 1 Python module reads `~/.claude/projects/**/*.jsonl`,
parses each line with `json.loads`, validates against a Pydantic model that
mirrors Anthropic's documented JSONL schema (`extra="forbid"`), and emits
typed `MessageRecord` instances. The Anthropic field-name targets:

- `timestamp` (ISO8601 UTC)
- `sessionId`, `requestId` (`str | None` for legacy compatibility)
- `isApiErrorMessage` (`bool`)
- `message.model`
- `message.usage.input_tokens`
- `message.usage.output_tokens`
- `message.usage.cache_creation.ephemeral_5m_input_tokens`
- `message.usage.cache_creation.ephemeral_1h_input_tokens`
- `message.usage.cache_read_input_tokens`

Tools rejected with rationale:

- **`claude-parser`** (CORRECTIONS-N): schema lacks usage/cache fields;
  unfit.
- **ccusage** — CLI emits session aggregates only; library mode not
  publicly exported; schema drops ephemeral split.
- **cc-lens** — drops `model`; hardcoded price table with dangerous fuzzy
  fallback.
- **agentsview, sniffly, splitrail, ccstats, token-scope, toki** —
  dashboard-first; no documented programmatic schema with required fields.
- **All AI-observability platforms** (Helicone, LangSmith, Langfuse,
  Phoenix, LiteLLM proxy, PromptLayer, Weave, OpenLLMetry) — live-proxy
  architecture; cannot ingest existing JSONL.
- **Anthropic Admin API** — wrong billing rail for consumer subscription
  users (CORRECTIONS-F).

### 3.2 Ephemeral-cache granularity (CORRECTIONS-D + CORRECTIONS-O)

The JSONL preserves
`message.usage.cache_creation.ephemeral_5m_input_tokens` and
`message.usage.cache_creation.ephemeral_1h_input_tokens` per assistant row.
v0.2.1 preserves this through the entire pipeline because LiteLLM's price
table at the pinned SHA has distinct rates for the two ephemeral windows;
aggregating to a single `cache_creation` bucket would introduce avoidable
measurement error in $\text{NotionalCost}^{USD}_t$.

**LiteLLM key-name correction (CORRECTIONS-O).** The actual LiteLLM JSON
keys at the pinned SHA (`e58a561caa21169fb02174148444c08509ce7028`,
BerriAI/litellm main, 2026-05-14) are:

| Token category | LiteLLM JSON key |
|---|---|
| input | `input_cost_per_token` |
| output | `output_cost_per_token` |
| cache_creation (5m, default) | `cache_creation_input_token_cost` |
| cache_creation (1h) | `cache_creation_input_token_cost_above_1hr` |
| cache_read | `cache_read_input_token_cost` |

45 Anthropic models in the table carry the split. `PricingTable` (§3.5)
loads each model's rates by these exact keys.

### 3.3 Pipeline

```
[NEW] simulations/dev_ai_cost_v2/jsonl_io.py
      IO-Boundary class (per functional-python tier discipline)
      OWN-PARSER: reads ~/.claude/projects/**/*.jsonl directly
      validates each row with Pydantic against Anthropic JSONL schema
      (extra="forbid"); raises JSONLSchemaError on drift
      emits Sequence[MessageRecord] (materialized list, not Iterator)
                          │
                          ▼
[NEW] simulations/dev_ai_cost_v2/anthropic_pricing.py
      pure Callable tier — frozen-dc PricingTable + __call__
      input: (model_id, ts, tokens_by_category)
      output: USD notional cost (exact Decimal)
      LiteLLM JSON pinned by commit SHA (§5.2)
      handles ephemeral_5m / ephemeral_1h distinct rates per correct keys
      ts is USED for time-varying price-step lookups
                          │
                          ▼
[NEW] simulations/dev_ai_cost_v2/panel_builder.py
      pure Callable tier
      per-message MessageRecord → developer-day aggregate (UTC half-open)
      drops is_error=True rows from cost aggregation (retains count)
      joins USDCOP_t (daily Banrep TRM from extended fetcher §3.4)
      returns tidy DailyNotionalPanel (frozen-dc wrapper)
                          │
                          ▼
[NEW] scripts/build_notional_cost_panel.py
      thin Tier-3 CLI wrapper; single orchestration point
                          │
                          ▼
       data/panels/notional_cost_panel.parquet  (dir created at first run)
                          │
                          ▼
       notebooks/dev_ai_cost_v2/  (R5 + R4-S3-COP + R4-S3-USD)

[NEW dependency, prerequisite] scripts/fetch_banrep.py extension
      add daily TRM endpoint; preserve existing monthly endpoint
      writes data/raw/banrep_trm_daily.parquet

[NEW errors module] simulations/dev_ai_cost_v2/_errors.py
      JSONLSchemaError(SchemaMismatchError) — sub-package convention
      matches repo style (existing _errors.py files in stochastic_fx,
      saas_builder/cohort_N, etc.)
```

### 3.4 Banrep daily TRM extension (prerequisite work item)

Extend `scripts/fetch_banrep.py` to fetch daily TRM (Tasa Representativa del
Mercado) from Banrep's official series. Confirm source URL / endpoint
matches what was used for the prior dev-AI iteration's monthly fetcher;
preserve fetcher style and provenance metadata. Output: tidy parquet with
schema `(date: Date, trm_cop_per_usd: Decimal)`.

### 3.5 Component contracts (v0.2.5 — CORRECTIONS-Y-1/-2/-3 + Y-5a/b/c/d/e/f + Y-6 + Y-7 + Y-8 applied)

| Unit | Tier | Signature |
|---|---|---|
| `dev_ai_cost_v2.jsonl_io.JSONLReader` | utils (IO Boundary) | `__call__(since, until, projects_root) -> JSONLReadResult` (see JSONLReadResult row below for tier placement per Y-5b). **Type-discriminates** by `type == "assistant"` before applying Pydantic schema (CORRECTIONS-Y-1); non-assistant rows skipped and counted in `JSONLReadResult.dropped_non_assistant_count` (Y-5a). Pydantic `extra="allow"`; only `timestamp + message.usage.input_tokens + message.usage.output_tokens` required. Raises `JSONLSchemaError` on missing required field. **Line-level malformed-skip (Y-7)**: per-line `json.loads` wrapped in `try/except json.JSONDecodeError` → silently skip + increment `JSONLReadResult.dropped_malformed_line_count`; covers trailing-null-byte filesystem corruption + truncated partial-writes. **UniqueHash dedup (Y-8)**: per-message dedup keyed on `_unique_hash = f"{message.id}:{requestId}"` (or `message.id` alone if requestId absent); keep-larger rule on `tokenTotal = input + output + cache_creation + cache_read` with `hasSpeed` tiebreaker on equal tokenTotals. Duplicate rows (including supersedences) increment `JSONLReadResult.dropped_duplicate_count`. UUID synthesis fallback per Y-5e: when JSONL `uuid` is absent, `_construct_message_record` synthesizes `"synth-sha256:" + sha256(file_basename + ":" + line_no_zfill_8).hexdigest()[:16]`. |
| `dev_ai_cost_v2.types.JSONLReadResult` | **types** (Y-5b) | frozen-dc: `records: Sequence[MessageRecord]` (materialized list per CR FLAG A; half-open UTC `[00:00:00, 24:00:00)`; deduplicated per Y-8), `dropped_non_assistant_count: int` (Y-5a), `dropped_malformed_line_count: int` (Y-7), `dropped_duplicate_count: int` (Y-8). Does NOT carry rate-coverage counters — those belong to `PricingTable` (Y-5a). |
| `dev_ai_cost_v2.types.MessageRecord` | types | frozen-dc: `ts: datetime (UTC), model: str, input_tok: int, output_tok: int, cache_create_5m: int, cache_create_1h: int, cache_read: int, cost_usd_notional: float, session_id: str, request_id: str \| None, is_error: bool, uuid: str` (R6 v0.1.3 CORRECTIONS-RR/-TT). `cost_usd_notional: float` per CORRECTIONS-Y-2. `request_id = None` for legacy pre-2.0 Claude Code; `JSONLReader` emits warning per None. `uuid` is either Anthropic-emitted or `"synth-sha256:..."` per Y-5e (R6 canonicalization gates on the `synth-` prefix and splits-or-warns to preserve hash stability). |
| `dev_ai_cost_v2.types.TokensByCategory` | types | frozen-dc: `input: int, output: int, cache_create_5m: int, cache_create_1h: int, cache_read: int`. **IMMUTABLE Value-tier type** (Y-5c): `__init__` does NOT mutate inputs; cache 5m+1h aggregation for cost happens INSIDE `PricingTable.__call__` body, NOT here. Split is preserved intact for diagnostic-only consumers. |
| `dev_ai_cost_v2.anthropic_pricing.PricingTable` | modules | frozen-dc with the following **counters owned per Y-5a**: `WARN_missing_keys_count: int` (per-model rate-key absences); `dropped_unknown_model_count: int` (model-lookup ladder exhausted); `multiple_substring_match_warning: int` (Y-5d tiebreaker invoked). Constructor `from_litellm_sha(sha) -> PricingTable` — load-time validation RELAXED per Y-3: all rate fields `Optional[float] = None`; missing keys WARNED, not raised. `__call__(model, ts, toks) -> float`: ccusage `calculateTieredCost` semantics; `tiered(N, base, null) = N · base`; 200k-input-tier for `claude-*`; **aggregates `toks.cache_create_5m + toks.cache_create_1h → cache_creation_input_tokens_total` inside this body** (Y-5c) and multiplies by single `cache_creation_input_token_cost`. Model-lookup ladder per Y-5d: exact → `anthropic/<model>` → longest-substring (**tiebreaker = alphabetically-smallest** when multiple equal-length candidates exist; counter `multiple_substring_match_warning` incremented). Missing rate → that category contributes 0. All arithmetic `float`; ccusage-parity within 0.1%. |
| `dev_ai_cost_v2.panel_builder.build_daily_panel` | modules | pure: `(read_result: JSONLReadResult, pricing: PricingTable, trm_panel: pl.DataFrame) -> DailyNotionalPanel`. Drops `is_error=True` from cost aggregation (count → `dropped_error_count`). Inner join on weekday subset; weekends dropped (count → `dropped_rows_count`). Threads ALL counters into panel + DATA_PROVENANCE: `dropped_rows_count`, `dropped_error_count`, `dropped_non_assistant_count` + `dropped_malformed_line_count` + `dropped_duplicate_count` (from `JSONLReadResult` per Y-5a/Y-7/Y-8), `WARN_missing_keys_count`, `dropped_unknown_model_count`, `multiple_substring_match_warning` (from `PricingTable` per Y-5a). Also computes `ephemeral_pi_share` (Y-6) and surfaces on the panel + DATA_PROVENANCE. |
| `dev_ai_cost_v2.types.DailyNotionalPanel` | types | frozen-dc wrapping `pl.DataFrame` with declared schema (`notional_cost_usd: pl.Float64`, `notional_cost_cop: pl.Float64`, `trm_cop_per_usd: pl.Float64`; others Int64). Carries the 8 counters above + `ephemeral_pi_share: float` per Y-6 (= `Σ cache_create_1h / Σ (cache_create_5m + cache_create_1h)`; if denominator = 0, set to 0.0). Wrapper frozen, inner df not. |

Tier-import rule (per CLAUDE.md): types/ imports neither modules/ nor
utils/; modules/ imports types/ but not utils/. Only `jsonl_io.py` performs
IO. The Tier-3 CLI script `scripts/build_notional_cost_panel.py` is the
**single orchestration point** that imports both utils-tier (`jsonl_io`)
and modules-tier (`anthropic_pricing`, `panel_builder`); no other call site
imports across both tiers (CR FLAG closure).

**Precision boundary (v0.2.2 — CORRECTIONS-Y-2)**: cost arithmetic is
`float` end-to-end. All OSS tools (ccusage, cc-lens, agentsview) use
`float`; ccusage matches LiteLLM-published rates to within ~1e-6. v0.2.1's
Decimal infrastructure was over-engineered relative to what real cost
computation requires. Reconciliation is verified by the **ccusage-parity
oracle test** (CORRECTIONS-Y-4): our Python pipeline matches `npx
ccusage@<pinned-version>` output on real `.jsonl` fixtures to within
**0.1%** per-message and per-day. This is a stronger guarantee than v0.2.1's
"exact-Decimal" because Decimal exactness across two independent code
paths is unrealistic, while parity-to-0.1% against an OSS reference
implementation catches every meaningful algorithmic divergence.

**Forward-compat — `extra="allow"` (v0.2.2 — CORRECTIONS-Y-1)**: Pydantic
schema in `dev_ai_cost_v2/jsonl_io.py` uses `extra="allow"` (was
`extra="forbid"`). Unknown fields appearing in future Claude Code versions
are forward-compatible by default. Schema drift on REQUIRED fields
(`timestamp`, `message.usage.input_tokens`, `message.usage.output_tokens`)
still raises `JSONLSchemaError`. The LiteLLM SHA pin (§5.2) plus the
ccusage-parity oracle (§4) provide the drift-detection floor in lieu of
strict schema validation.

## 4. Notebook structure

`notebooks/dev_ai_cost_v2/` mirrors `notebooks/dev_ai_cost/`:

- `01_data_eda.ipynb` — trio-disciplined EDA per
  `feedback_notebook_trio_checkpoint`. Required cells:
  - **Reconciliation cell**: panel-builder daily aggregates re-summed back
    to per-message totals; compared against `JSONLReader` raw per-message
    totals for the same window. **ccusage-parity within 0.1%** (CORRECTIONS-Y-2
    supersedes the v0.2.1 exact-Decimal requirement in CORRECTIONS-H, per
    Wave 1 RC housekeeping fix). Any drift > 0.1% HALTs to disposition
    (suspect aggregation bug, `is_error` mis-filter, or algorithm divergence
    from ccusage).
  - **Power-measurement HALT-checkpoint** (CORRECTIONS-J + CORRECTIONS-U):
    compute residual SD of $|\Delta\ln\text{NotionalCost}^{USD}|$ after
    partialling out $|\Delta\ln\text{Tokens}|$; Monte-Carlo measured power
    at MDES = 0.40 residual-SD with current $T$. If power < 0.50, route to
    `dispositions/power_halt_template.md` — **expected to fire at $T = 38$
    per Model QA's independent calc**.
- `02_r5_descriptive.ipynb` — R5 outputs with 90% **stationary-bootstrap**
  (Politis-Romano, expected block length $\lceil T^{1/3} \rceil$,
  CORRECTIONS-P) CIs at $B = 10{,}000$. Headline output cell (§2.1).
  Variance-decomposition with **separately-reported covariance term**
  (CORRECTIONS-Q).
- `03_r4s3_cop_consistency.ipynb` — R4-S3-COP **consistency check** (NOT a
  novel finding per CORRECTIONS-S); OLS + HAC with $L = \lfloor T^{1/3}
  \rfloor$. Cell preamble explicitly disclaims framework-graduation
  authority.
- `04_r4s3_usd_behavioral.ipynb` — R4-S3-USD **behavioral subscription-
  inelasticity test** (CORRECTIONS-S); two-sided $\alpha_1^{USD}$ test.
  Decision-citation block precedes each test choice per
  `feedback_notebook_citation_block`.
- `05_sensitivity.ipynb` — four diagnostic sensitivity arms from §2.4. No
  verdict authority documented in every cell preamble.

Every trio is a HALT-checkpoint for human review per
`feedback_notebook_trio_checkpoint`.

## 5. Reproducibility pins

CORRECTIONS-H (Code Reviewer BLOCK 5) required the actual pins be committed
in the spec, not deferred to plan-emission. Pins below are placeholders for
the **review-time confirmation step** before plan emission — Wave 1 RC must
verify each pin is reachable and current.

### 5.1 Parser substrate — REMOVED

v0.2.0 §5.1 pinned `claude-parser==2.0.0`. v0.2.1 removes external parser
substrate entirely per CORRECTIONS-N (the 30-min ephemeral-split gate
failed). Own-parser is in-repo at `simulations/dev_ai_cost_v2/jsonl_io.py`;
no external pin needed. Pydantic is pinned via existing
`pyproject.toml`/`requirements.txt`.

### 5.2 LiteLLM price table commit SHA pin (COMMITTED v0.2.1)

- Repo: `BerriAI/litellm`
- File path: `model_prices_and_context_window.json` (at repo root)
- Commit SHA: **`e58a561caa21169fb02174148444c08509ce7028`** (BerriAI/litellm
  main, 2026-05-14, verified by Wave 1 RC at v0.2.0 review)
- Key names (corrected per CORRECTIONS-O):
  - `input_cost_per_token`
  - `output_cost_per_token`
  - `cache_creation_input_token_cost` (5m default)
  - `cache_creation_input_token_cost_above_1hr` (1h)
  - `cache_read_input_token_cost`
- 45 Anthropic models in the file carry the cache-creation split
- File fetched once at panel-build time and cached locally;
  `PricingTable.from_litellm_sha` enforces SHA match on the cached file
  (hash check) and refuses to load if drift is detected.

### 5.3 ccusage / claude-parser pins — REMOVED

v0.1.0 §5.1 pinned ccusage. v0.2.0 removed ccusage and replaced with
`claude-parser`. v0.2.1 removes `claude-parser` and replaces with the
in-repo own-parser (CORRECTIONS-N). No external parser pin survives.

### 5.4 Data-provenance file

`notebooks/dev_ai_cost_v2/data/DATA_PROVENANCE.md` records:

- LiteLLM commit SHA pin (§5.2)
- Banrep daily TRM raw file sha256
- final `notional_cost_panel.parquet` sha256
- date window (since / until)
- session-log scope (which `~/.claude/projects/*/` directories)
- `dropped_rows_count` from §3.5 panel-builder for N-floor audit
- `dropped_error_count` from §3.5 panel-builder for is_error diagnostic
- own-parser git commit SHA at panel-build time

## 6. Threats, identification, mitigations

| Threat | Mitigation |
|---|---|
| Subscription-vs-pay-per-API regime mismatch (subscribed user as proxy for pay-per-API population) | §1.2 explicit assumption: equivalent demand under both regimes. **Bias direction (CORRECTIONS-V / Model QA FLAG 6)**: subscribed users use *more* tokens than pay-per-API users would (zero marginal cost), so the *level* of notional cost OVERSTATES true pay-per-API demand — but the FX-vol *share* output is **conservative** under this bias (the level overstatement is in the denominator AND the FX-channel numerator approximately proportionally; share understates if anything). M-design hedge sizing per Role A (CORRECTIONS-R) therefore over-provisions slightly, which is safe. Documented as ASSUMPTION; testable post-cohort. |
| `claude-parser` failed ephemeral-split gate at v0.2.0 review | Resolved: own-parser is primary substrate (CORRECTIONS-N) |
| LiteLLM price-table backfill changes historical price retroactively | SHA pin `e58a561c...` (§5.2); `PricingTable.from_litellm_sha` enforces hash check on cached file |
| Forward-fill on weekends would smuggle FX vol into idle days | Weekends dropped on both LHS and RHS in §3.5 panel-builder; **forward-fill is forbidden**. CORRECTIONS-M: code-level enforcement via Hypothesis property test on `build_daily_panel` that raises if any output day lacks source rows on either side |
| Own-parser / panel-builder reconciliation drift | **ccusage-parity within 0.1%** required (§4 reconciliation cell + CORRECTIONS-Y-2; supersedes v0.2.1 Exact-Decimal); any drift > 0.1% HALTs to disposition (suspect aggregation bug, `is_error` mis-filter, or algorithm divergence from ccusage) |
| Anthropic price-step changes mid-window | Step function captured in LiteLLM SHA; `PricingTable.__call__(model, ts, toks)` uses `ts` for time-varying lookup (CORRECTIONS-V); sensitivity arm in §2.4 drops ±5d windows around documented step dates |
| n=1 selection (one developer's logs) | Pilot framing pre-declared (§1.2); no population claim from this iteration; cohort recruitment is separate sub-project |
| HAC bandwidth mis-sized for $T$ | $L = \lfloor T^{1/3} \rfloor$ pinned (§2.2 CORRECTIONS-I) |
| Power at MDES = 0.40 on raw vs residual SD | Power measured on residual SD with mandatory HALT-checkpoint (§2.2 CORRECTIONS-J + CORRECTIONS-U); **HALT expected at $T = 38$** — routed through `dispositions/power_halt_template.md` |
| EIV from blended pricing across ephemeral windows | Eliminated by preserving the split with correct LiteLLM keys (§3.2 CORRECTIONS-D + CORRECTIONS-O) |
| Sensitivity arms acquiring verdict authority | Pre-classified DIAGNOSTIC only (§2.4 CORRECTIONS-K); recreates and resolves the prior-FAIL §5.5/§9.6 contradiction |
| Bootstrap CI under serial correlation | Stationary bootstrap (Politis-Romano) with expected block length $\lceil T^{1/3} \rceil$ pinned (CORRECTIONS-P); IID bootstrap explicitly rejected |
| Variance-decomposition covariance attribution ambiguity | Conservative rule pinned (CORRECTIONS-Q): covariance reported separately, NOT attributed to either share; FX-share excludes covariance |
| R4-S3-COP capturing well-known USDCOP vol clustering rather than AI-cost transmission | Reclassified as consistency check, NOT a novel finding (CORRECTIONS-S / Model QA FLAG 7); R4-S3-USD added as the framework-relevant behavioral arm |
| `DailyNotionalPanel` wrapper frozen but inner DataFrame mutable | Acknowledged. Mitigation: panel consumers use `.lazy()` / `.collect()` or `.clone()` before mutation. Hypothesis-property-tested `__post_init__` to verify schema |
| Iterator silently empty on second pass | `JSONLReader` returns `Sequence` (materialized list), not `Iterator` (CR FLAG A / CORRECTIONS-V); Hypothesis-property-tested for double-iteration equivalence |
| `is_error=True` rows inflating cost-burden estimates | Dropped from cost aggregation; retained as `dropped_error_count` diagnostic (CR partial-CLOSE / CORRECTIONS-V) |

## 7. Anti-fishing invariants (carried forward + adjusted)

Per CLAUDE.md and `feedback_pathological_halt_anti_fishing_checkpoint`.

- $N$-floor: $\max(\text{weekday days observed})$ at spec write time
  (CORRECTIONS-G), starting at 38, growing with usage. Documented
  deviation from project-default 75.
- Power-floor: 0.50 at MDES = 0.40 **residual SD** for R4-S3 (CORRECTIONS-J
  + lowered from project-default 0.80 for pilot demonstration-grade).
- Sign expectations pinned ex-ante for R4-S3 (§2.2).
- Lag structure pinned ex-ante: $k=1$ primary, $k=5$ sensitivity
  (diagnostic only).
- HAC bandwidth pinned ex-ante: $L = \lfloor T^{1/3} \rfloor$ — not the
  v0.1.0 fixed 12.
- No post-hoc trim or outlier rule beyond what is pinned in §2.4.
- Sensitivity arms have no verdict authority (CORRECTIONS-K).

## 8. Workflow / agent assignment

Per `feedback_two_wave_doc_verification` and
`feedback_implementation_review_agents`.

| Phase | Owner / Reviewer | Audit-pass chain |
|---|---|---|
| Spec finalization | orchestrator | `structural-econometrics` → `latex-econ-model` |
| Spec review — Wave 1 | Reality Checker | — |
| Spec review — Wave 2 | Model QA Specialist + Code Reviewer (parallel) | — |
| Plan emission | orchestrator via `superpowers:writing-plans` | — |
| Plan goal-backward check | gsd-plan-checker | — |
| Banrep daily fetcher extension | Data Engineer | `try-except` + `contract-docstrings` + `hypothesis-tests` |
| Own-parser (`jsonl_io.py`) | Data Engineer (after interface contract from Backend Architect) | `tighten-types` + `contract-docstrings` + `hypothesis-tests` + `try-except` |
| Pricing module | Data Engineer | `functional-python` + `hypothesis-tests` |
| Panel builder | Backend Architect designs ‖ Data Engineer implements | `pre-mortem` + `mutation-testing` + `hypothesis-tests` (incl. forward-fill-forbidden property) |
| Notebooks 01–05 | orchestrator with trio-checkpoints | `python-panel-data` + `statsmodels` |
| **Anticipated power-HALT routing** (CORRECTIONS-U) | orchestrator → user disposition memo | `dispositions/power_halt_template.md` pre-enumerates pivots |
| Implementation review | Code Reviewer + Reality Checker + Backend Architect | — |
| Pre-verdict end-to-end audit | Delphi panel via `audit-econ` skill | — |
| Write-up (LaTeX) | orchestrator reviewed by Technical Writer | `latex-doc` + `latex-econ-model` |

## 9. Out of scope

- Population inference (cohort recruitment is separate sub-project)
- M-design (Panoptic position construction) — gated on R5 producing
  M-design-usable output and R4-S3 PASS
- Estimated demand response (rejected: subscription regime → demand
  inelastic to price by construction)
- Forecast-error LHS spec — rejected per prior `fx_vol_cpi` FAIL precedent
- Anthropic Admin API integration — wrong billing rail for consumer
  subscription; cohort-scaling work item
- Cross-developer or cross-IDE panels
- HTTP-API exposure of the data feeder — library + CLI only at pilot scale

## 10. Open questions for v0.2.1 closure-only reviewers

The v0.2.0 open questions 1–5 were addressed by v0.2.0 reviewer Wave 1 RC
and Wave 2 Model QA findings (see scratch reports). v0.2.1 has these
remaining questions for closure-only re-review:

1. **(For Wave 1 RC)** Verify that CORRECTIONS-N (own-parser primary) and
   CORRECTIONS-O (LiteLLM key names + SHA pin `e58a561c...`) are completely
   integrated; no residual `claude-parser` or wrong-key-name language
   anywhere in the spec.
2. **(For Wave 2 Model QA)** Verify that CORRECTIONS-P (stationary
   bootstrap), CORRECTIONS-Q (conservative covariance attribution),
   CORRECTIONS-R (R5 Role A pinning), CORRECTIONS-S (R4-S3 split into COP
   consistency + USD behavioral), CORRECTIONS-T (CI threshold 0.15), and
   CORRECTIONS-U (power-HALT anticipated) are completely integrated and
   internally consistent.
3. **(For Wave 2 Code Reviewer)** Verify that CORRECTIONS-V (Iterator →
   Sequence, ts param policy, is_error policy, UTC half-open, request_id
   nullable) and CORRECTIONS-W (file paths, sub-package errors convention)
   are completely integrated.
4. **(Open philosophical question for Wave 2 Model QA — not blocking)**: at
   $T = 38$ with power likely below 0.50 (CORRECTIONS-U anticipates this),
   should v0.2.1 just skip R4-S3-USD entirely until $T$ grows, and ship a
   v0.3.0 R5-only spec? My take: keep R4-S3-USD in the design even if the
   first run HALTs at power, because the disposition memo + waiting for $T$
   to grow is itself a meaningful framework outcome. Reviewer may
   disagree.

## 11. Cited files (status verified by Wave 1 RC at v0.2.0 review; updated v0.2.1)

| File / directory | Status | Role |
|---|---|---|
| `memory/feedback_two_wave_doc_verification.md` | EXISTS | governing review protocol |
| `memory/feedback_implementation_review_agents.md` | EXISTS | implementation panel composition |
| `memory/feedback_notebook_trio_checkpoint.md` | EXISTS | notebook HALT discipline |
| `memory/feedback_notebook_citation_block.md` | EXISTS | decision-citation block convention |
| `memory/feedback_pathological_halt_anti_fishing_checkpoint.md` | EXISTS | anti-fishing HALT protocol |
| `memory/project_dev_ai_section_j_fail.md` | EXISTS | prior FAIL precedent |
| `notebooks/dev_ai_cost/` | EXISTS | sibling iteration directory |
| `scripts/fetch_banrep.py` | EXISTS | to be **extended** for daily TRM (§3.4) |
| `simulations/dev_ai_cost_v2/_errors.py` | **TO CREATE** | new sub-package errors file per repo convention (matches `simulations/stochastic_fx/_errors.py`, `simulations/saas_builder/cohort_*/_errors.py` pattern). v0.2.0 §11 erroneously cited `simulations/_errors.py` at top level which does NOT exist (CORRECTIONS-W). |
| `data/panels/` | **TO CREATE** | created by `scripts/build_notional_cost_panel.py` on first run. v0.2.0 §11 erroneously listed as existing (CORRECTIONS-W). |
| `notebooks/dev_ai_cost_v2/` | **TO CREATE** | new iteration directory |
| `notebooks/dev_ai_cost_v2/dispositions/power_halt_template.md` | **TO CREATE** | pre-enumerated disposition for anticipated power-HALT (CORRECTIONS-U) |
| `simulations/tests/fixtures/real_claude_jsonl/` | **TO CREATE** in v0.2.2 (CORRECTIONS-Y-4) | small PII-redacted sample of real `~/.claude/projects/*.jsonl` covering all 9 `type` values; canonical regression contract |
| `simulations/tests/test_real_jsonl_integration.py` | **TO CREATE** in v0.2.2 (CORRECTIONS-Y-4) | ccusage-parity oracle test + real-JSONL no-exception test |

## 12. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-05-16 | Initial draft (USD-then-COP factor-model framing) |
| 0.1.0 review | 2026-05-16 | REJECTED by Wave 1 RC (5 BLOCKs), Wave 2 Model QA (5 BLOCKs), Wave 2 Code Reviewer (NEEDS_WORK, 6 BLOCKs). Reviews at `scratch/2026-05-16-ai-cost-spec-review/wave{1,2}_*.md`. |
| 0.2.0 | 2026-05-16 | Pivot to R5 descriptive + R4-S3 vol-clustering. CORRECTIONS-A through -M itemized in §0. |
| 0.2.0 review | 2026-05-16 | All v0.1.0 BLOCKs CLOSED. Wave 1 RC NEEDS_WORK (BLOCKs 6+7: claude-parser unfit, LiteLLM keys); Wave 2 Model QA NEEDS_WORK (BLOCKs 8+9+12: bootstrap, covariance, R5 role); Wave 2 Code Reviewer ACCEPT_WITH_FLAGS (Iterator, ts param, is_error). Reviews at `scratch/2026-05-16-ai-cost-spec-review/wave{1,2}_*_v0_2_0.md`. |
| 0.2.1 | 2026-05-16 | Integration patch: CORRECTIONS-N through -W in §0.1. Own-parser primary substrate (claude-parser removed). LiteLLM SHA committed `e58a561c...`. Stationary bootstrap (Politis-Romano) pinned. Conservative covariance attribution. R5 Role A pinned. R4-S3 split into COP-consistency + USD-behavioral. CI threshold tightened to 0.15. Power-HALT anticipated. Iterator → Sequence. |
| 0.2.1 closure-only review | 2026-05-16 | All three channels CLOSE_ALL. Plan emission approved. v0.2.1 plan (17 tasks) emitted at `docs/plans/2026-05-16-ai-cost-factor-model-plan.md`. Tasks 1-8 implemented at `iter/ai-cost-2026-05` HEAD `010df55`, 796/796 unit tests passing. |
| 0.2.1 impl-review checkpoint | 2026-05-17 | Code Reviewer NEEDS_FIXES (2 Important + 5 Minor); Backend Architect APPROVED (2 Important for Task 10); **Reality Checker REJECTED** with 2 production BLOCKs (spec-rooted): JSONLReader cannot parse any real `~/.claude/projects/*.jsonl` (no type-discriminator; `extra="forbid"` rejects 9 type values + 6 message.usage extras; required `costUSD` absent from 0/355 real assistant rows); LiteLLM SHA pin incomplete (6/21 claude-* models lack `cache_creation_input_token_cost_above_1hr` including `claude-sonnet-4-5`/`claude-sonnet-4-6`). OSS algorithm study at `scratch/2026-05-16-ai-cost-impl-review/oss_algorithm_study.md` reveals our schema policy is the outlier; all OSS tools (ccusage, cc-lens, agentsview, claude-parser) type-discriminate first + `extra="allow"` + compute cost from rate-table at parse time + ignore ephemeral 5m/1h split + tolerant LiteLLM load. |
| 0.2.2 | 2026-05-17 | Amendments: CORRECTIONS-Y-1 (JSONL parsing — type-discriminate; `extra="allow"`; drop `costUSD` required; minimum required field set); Y-2 (cost formula — ccusage `calculateTieredCost` semantics; switch Decimal → float; ephemeral split preserved in MessageRecord as diagnostic but aggregated for cost; 200k tiered pricing); Y-3 (LiteLLM strategy — all rate fields Optional; per-model gating at call time; model-lookup ladder; missing key → 0); Y-4 (integration test floor — real .jsonl fixture + ccusage-parity oracle test, hard-fail once fixture committed). |
| 0.2.2 two-wave review | 2026-05-17 | Wave 1 RC PARTIAL_CLOSE (BLOCK A + B both closed; 2 housekeeping items: §4 + §6 stale-Decimal language → ccusage-parity 0.1% — LANDED in v0.2.2 directly without re-review per RC explicit approval). Wave 2 Model QA CLOSE_ALL (1 non-blocking FLAG: π̂ ephemeral diagnostic recommended — folded into v0.2.3 as Y-6). Wave 2 Code Reviewer PARTIAL_CLOSE — WITHHELD plan-amendment approval; 6 architectural BLOCKs (CR-Z-1 counter ownership; CR-Z-2 JSONLReadResult tier-orphan; CR-Z-3 cache aggregation locus; CR-Z-4 longest-substring tiebreaker non-determinism; CR-Z-5 uuid synthesis breaks under rename → R6 false drift; CR-Z-6 missing migration enumeration + Task 9.5). Reports at `scratch/2026-05-16-ai-cost-spec-review/{wave1_reality_checker,wave2_model_qa,wave2_code_reviewer}_v0_2_2.md`. |
| 0.2.3 | 2026-05-17 | Contract-only patch resolving all 6 CR-Z BLOCKs in §0.3 CORRECTIONS-Y-5 (a–f sub-pins) + Y-6 π̂ ephemeral diagnostic. §3.5 contracts table updated: `JSONLReadResult` now a types-tier frozen-dc with `dropped_non_assistant_count` only; `PricingTable` owns `WARN_missing_keys_count`, `dropped_unknown_model_count`, `multiple_substring_match_warning`; cache 5m+1h aggregation pinned to `PricingTable.__call__` body (not TokensByCategory); longest-substring tiebreaker = alphabetical min; uuid synthesis = `synth-sha256:` prefix on basename-based hash for rename-stability; Task 9.5 migration enumerated. |
| 0.2.3 closure-only re-review | 2026-05-17 | Wave 2 Model QA CLOSE_ALL (π̂ folded properly; CR-Z pins have no econometric implications). Wave 2 Code Reviewer CLOSE_ALL — **plan-amendment-cycle APPROVED**. Wave 1 RC PARTIAL_CLOSE on 2 trivial doc fixes (§2.1 verdict-logic table row still said exact-Decimal — corrected to ccusage-parity-0.1%-on-cost + exact-Decimal-on-tokens; Y-5f migration table missing `scripts/build_notional_cost_panel.py` — added) → both landed inline making all three channels CLOSE_ALL. Reports at `scratch/2026-05-16-ai-cost-spec-review/{wave1_reality_checker,wave2_model_qa,wave2_code_reviewer}_v0_2_3.md`. Task 9.5 implementation migration landed in 6 atomic commits (`31a4d5d..d6da500`); 109/109 dev_ai_cost_v2 tests green, 793/793 cross-suite green. Two-stage impl review: RC APPROVE (7/7 pins PASS), CR APPROVE_WITH_NITS (zero BLOCKs, 9 NITs). |
| 0.2.4 | 2026-05-17 | Real-data HALT patch (§0.4 CORRECTIONS-Y-7). First production run of `scripts/build_notional_cost_panel.py` raised `JSONLSchemaError` on filesystem partial-write corruption (trailing null-byte block in `agent-af5e1160f7be358ba.jsonl`). User-selected Option A (ccusage-mirror): line-level malformed-skip + `JSONLReadResult.dropped_malformed_line_count` counter threaded through panel + CLI. Closes the line-level half of OSS-mirror permissive parsing that v0.2.3 Y-1 only addressed at the Pydantic-schema level. Disposition: `notebooks/dev_ai_cost_v2/dispositions/2026-05-17-task10-trailing-null-bytes.md`. |
| 0.2.5 | 2026-05-17 | Reliability-convergence patch (§0.5 CORRECTIONS-Y-8). First Task-10 panel run on real corpus showed ~2.11× cost overcount vs `npx ccusage daily`. Empirical investigation (`scratch/2026-05-17-v0_2_5-dedup-discovery/findings.md`) identified missing OSS-mirror uniqueHash dedup as the dominant root cause (single-session 1.78× duplication factor on `${message.id}:${requestId}`). Post-dedup cost converges to 0.977× of ccusage (within 2.3%); residual gaps filed as Y-9 backlog. Spec change: in-memory dedup map in `JSONLReader.__call__` with keep-larger-tokenTotal + hasSpeed-tiebreaker (mirrors ccusage `Sr` + `$`); new `dropped_duplicate_count` counter on `JSONLReadResult` (8 panel counters total). |
