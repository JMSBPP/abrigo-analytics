# STAGE_2_RESULTS Anchor — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Code-agnostic plan.** Per repo memory `feedback_no_code_in_specs_or_plans` (NON-NEGOTIABLE), this plan does NOT contain code blocks. The deliverable is a Markdown notes file authored by a Technical Writer agent.
>
> **Foreground orchestrates, never authors.** Per repo memory `feedback_specialized_agents_per_task` (NON-NEGOTIABLE). This plan's author also does NOT author the deliverable.

**Plan version:** v0.2 (CORRECTIONS-α applied; 2 RC BLOCKs + 6 FLAGs resolved — see §"CORRECTIONS-α v0.1 → v0.2" at end)
**Status:** READY-FOR-REVERIFY
**Emit timestamp:** 2026-05-08

**Goal:** Author `notes/STAGE_2_RESULTS.md` — the math-results-and-verification anchor that captures the Stage-2 frozen state of the SaaS-builder iteration and serves as the single import point for Stage-3 work.

**Architecture:** Hybrid math-claim-indexed backbone with cohort cross-references. Each math primitive / pin / forward-fix claim from `notes/PRIMITIVES.md` and `notes/SaaS_Builders_AI_NativeBuilders.md` becomes one §2 subsection citing (a) source `file:line`, (b) pytest test name, (c) sha256 of the supporting `audit_block`. §3 cohort cross-cut, §4 anti-fishing case studies, §5 reproducibility cert, §6 Stage-3 hand-off, §7 references.

**Tech stack:** Markdown only. No code. Verification uses `git grep` / `pytest --collect-only` / `sha256sum` against the frozen HEAD `9fd92e5`.

**Predecessor chain:** `notes/PRIMITIVES.md` → `notes/SaaS_Builders_AI_NativeBuilders.md` → **`notes/STAGE_2_RESULTS.md`** (this deliverable). Stage-3 will produce `notes/STAGE_3_RESULTS.md` following the same pattern.

**Stage-2 freeze pin:** HEAD `9fd92e5` ("deliverable(saas-cohort): Stage-2 modeling memo + Phase-4 schema-bump audit") — confirm at Phase 0 via `git merge-base --is-ancestor 9fd92e5 HEAD` (true) AND `git diff 9fd92e5 HEAD -- simulations/ docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (empty). The verdict-memo commit `9fd92e5` is the canonical Stage-2 freeze marker; the upstream CORRECTIONS-α v0.4 marginalization closure is at `80f4ed4` (an ancestor of `9fd92e5`).

**Out of scope:** introducing any new claim not already in spec / PRIMITIVES / code; magnitude promises about real-data scale-up; Stage-3 implementation work.

---

## Strategic delegation map

| Phase | Owner | Mode |
|---|---|---|
| 0 — Pre-flight | foreground (this plan author) | inline verify |
| 1 — Structure pin | foreground | inline (this plan locks structure) |
| 2 — Implementation | `Technical Writer` | single-agent dispatch |
| 3 — Re-verify | `Reality Checker` + `Model QA Specialist` | 2-wave parallel |
| 4 — Commit + push | foreground | inline |

---

## File structure

Single file deliverable:

```
notes/
└── STAGE_2_RESULTS.md   (to be created by Technical Writer in Phase 2)
```

No code, no tests, no fixtures. The file is a results anchor; verification is by re-running the citation/sha256 chain in Phase 3, not by adding tests.

---

## Phase 0 — Pre-flight

### Task 0.1 — Confirm Stage-2 freeze pin
- [ ] **Step 1** — Verify freeze-pin is in our history AND no Stage-2 substantive code/spec changed since:
  - `git merge-base --is-ancestor 9fd92e5 HEAD` MUST exit 0 (freeze pin is an ancestor of current HEAD).
  - `git diff 9fd92e5 HEAD -- simulations/ docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` MUST be empty (no Stage-2 substantive code or spec drift since the freeze).
  - Cosmetic post-freeze commits outside those paths (memory hygiene, README updates) are PERMITTED.
  - If either check fails → HALT and surface to user.
- [ ] **Step 2** — Run `git status --short`. Expect no modified files in `notes/`, `simulations/`, `docs/specs/`. Untracked acceptable.
- [ ] **Step 3** — Run `git branch --show-current`. Expect `iter/saas-builder-stage-2`.

### Task 0.2 — Verify source artifacts exist (HALT on missing)

Each item below MUST resolve. If any is missing, HALT and surface to user per `feedback_pathological_halt_anti_fishing_checkpoint`.

- [ ] **Step 1** — Predecessor notes:
  - `notes/PRIMITIVES.md`
  - `notes/SaaS_Builders_AI_NativeBuilders.md`
- [ ] **Step 2** — Spec + verdict memo:
  - `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (v1.2.1 expected)
  - Stage-2 verdict memo (hard-pinned path): `docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md`
- [ ] **Step 3** — Cohort plans (4 files):
  - `docs/plans/2026-05-08-saas-cohort-1-t1-cost-posterior.md`
  - `docs/plans/2026-05-08-saas-cohort-2-t2-pricing-sign.md`
  - `docs/plans/2026-05-08-saas-cohort-3-revenue-form-loo.md`
  - `docs/plans/2026-05-08-saas-cohort-4-z-cap-derivation.md`
  - `docs/plans/2026-05-09-saas-cohort-close.md`
- [ ] **Step 4** — Cohort independent-audit verdict directories:
  - `scratch/2026-05-08-saas-cohort-1-independent-audit/`
  - `scratch/2026-05-08-saas-cohort-2-independent-audit/`
  - `scratch/2026-05-08-saas-cohort-3-independent-audit/`
  - `scratch/2026-05-08-saas-cohort-4-independent-audit/`
- [ ] **Step 5** — Emitted artifacts:
  - `simulations/saas_builder/data/gate_verdict.json` (must contain `audit_block` with sha256)
  - `simulations/saas_builder/data/PRIMARY_RESULTS.md`
  - `simulations/saas_builder/data/ROBUSTNESS_RESULTS.md`
  - `simulations/saas_builder/data/revenue_form_verdict.json`
  - `simulations/saas_builder/data/Z_cap_pinned.json` (schema v1.1)
  - `simulations/saas_builder/data/Z_cap_pinned.SIGN_VERDICTS.md`
  - `simulations/saas_builder/data/synthetic_tau_t.parquet`
  - `simulations/saas_builder/data/cohort_prior.parquet`
- [ ] **Step 6** — For each parquet/JSON above, run `python -c "import json; print(json.load(open('PATH'))['audit_block']['sha256'])"` (JSON) or `sha256sum` (parquet) and record in a scratch worksheet `scratch/2026-05-09-stage-2-results-preflight/SHA256_INVENTORY.md`. Commit worksheet at end of Phase 0.

### Task 0.3 — Capture sha256 source-of-truth

The two sha256 anchors that STAGE_2_RESULTS.md must cite verbatim:

- [ ] **Step 1** — `Z_cap_pinned.json::audit_block.sha256` — pre-pinned in user brief as `1fb1f7a4...`. Verify via `python -c "import json; print(json.load(open('simulations/saas_builder/data/Z_cap_pinned.json'))['audit_block']['sha256'])"`. If divergent, HALT.
- [ ] **Step 2** — `gate_verdict.json::audit_block.sha256` — pre-pinned as `4da660b5...`. Verify analogously. If divergent, HALT.
- [ ] **Step 3** — Record both full sha256 values in the worksheet from Task 0.2 Step 6.

### Task 0.4 — Commit pre-flight worksheet

- [ ] **Step 1** — `git add scratch/2026-05-09-stage-2-results-preflight/`
- [ ] **Step 2** — `git commit -m "preflight(stage-2-results): sha256 inventory + source artifact verification"`

---

## Phase 1 — Structure pin (foreground; locks the §-skeleton)

This phase produces no new files; it locks the structure that the Technical Writer brief in Phase 2 will require verbatim. The structure below is pre-pinned by the user brief and is NON-NEGOTIABLE.

### Task 1.1 — Lock §0–§7 skeleton

The Technical Writer must produce `notes/STAGE_2_RESULTS.md` with exactly these top-level sections, in this order:

- **§0 Preface** — relationship to `notes/PRIMITIVES.md` and `notes/SaaS_Builders_AI_NativeBuilders.md`; status as Stage-2-frozen anchor pinned at HEAD `9fd92e5`; explicit statement that the doc does not auto-update.
- **§1 Empirical verdict** — one paragraph, anchor-citing the verdict memo §1. No magnitude editorialization.
- **§2 Math claims index** — one subsection per claim enumerated in Task 1.2. Each subsection follows the 4-part citation format defined in Task 1.3.
- **§3 Cohort cross-cut** — four subsections (§3.1 C1, §3.2 C2, §3.3 C3, §3.4 C4) listing which §2 claims each cohort consumed/verified. Pure cross-reference; no new claims.
- **§4 Anti-fishing case studies** — three worked examples for Stage-3 implementers:
  - §4.1 C1 marginalization fix (sum-out of `tier_idx + n_per_day + n_month`)
  - §4.2 C2 bracket re-orientation (24-cell parameter family per spec §5.2; NOT (ε,ω) sweep)
  - §4.3 C4 1/κ correction in π(t) closed form
- **§5 Reproducibility certificate** — the audit_block sha256 set; how to verify unchanged at HEAD `9fd92e5`.
- **§6 Stage-3 hand-off** — what `STAGE_3_RESULTS.md` will need to import; explicit enumeration of Stage-2 assumptions Stage-3 must test (synthetic-Bayesian only; single trajectory; no real-data calibration; etc.). NO magnitude promises.
- **§7 References** — bibliography-style; pointers to PRIMITIVES.md, SaaS note, spec v1.2.1, verdict memo, the 4 cohort plans, all cohort independent-audit verdict files (count to be confirmed at write-time; user brief estimates 31), and all relevant codepaths.

### Task 1.2 — Lock §2 claim enumeration

The Technical Writer brief MUST include §2 subsections in this order. Each entry below identifies (a) what the claim is, (b) where its math lives in PRIMITIVES.md / spec / SaaS note, (c) which cohort consumed/verified it.

**§2.A Math primitives extended/specialized during Stage-2:**

- §2.A.1 — Eq. (6) FX path closed form (PRIMITIVES.md §6 / Eq. 6) — consumed by C1 emit pipeline.
- §2.A.2 — Eq. (7) Realized variance (PRIMITIVES.md §7 / Eq. 7) — consumed by C1 fit.
- §2.A.3 — Eq. (8) Variance proxy `σ_T = (X̄/Ȳ)²·ε²/8` (PRIMITIVES.md §6 / Eq. 8) — invoked by C4 σ₀ anchor (post-FLAG-4 fix).
- §2.A.4 — Eq. (10) Δ closed form (PRIMITIVES.md §10) — specialized to saas cohort by C2 (24-bracket sign cert).
- §2.A.5 — Eq. (11) Γ closed form (PRIMITIVES.md §11) — used by C2.
- §2.A.6 — §6 variance-proxy section — referenced by C4.
- §2.A.7 — §10 Carr-Madan replication reference — invoked by C4 π(t) chain.
- §2.A.8 — §11 — C2 reference. *(Note: the user brief's primitive enumeration explicitly listed "§6, §10". §11 is included here as a faithful expansion — it is the natural Carr-Madan replication anchor for C4 and is C2-adjacent. This is documented as a minimal scope extension, not a covert addition.)*

**§2.B Math pins M1–M5** (from spec §"Math pins"):

- §2.B.1 — M1: TruncPareto α-floor (≥1.5) — sampler-Callable enforcement.
- §2.B.2 — M2: Softplus β-tightness (L¹ < 10⁻³·κ) — regularizer-Callable.
- §2.B.3 — M3: Blended p_t formula (Sonnet $7.1495/MTok).
- §2.B.4 — M4: Parquet schemas per spec §10.
- §2.B.5 — M5: FX path `[4200, 3800, 4200]` at t∈{0, π/2, π}.

**§2.C Forward-fix claims:**

- §2.C.1 — C1 marginalization: `tier_idx + n_per_day + n_month` sum-out exactness; numerical-equivalence Property #7.
- §2.C.2 — C2 bracket re-orientation: 24-cell parameter family per spec §5.2.
- §2.C.3 — C2 Δ_analytic = −1.02e-8 reconciliation (β·κ ≈ 2.33e4 → softplus underflows; cos² near-cancellation).
- §2.C.4 — C3 Det+churn `S_t = (1-λ)^t` with `λ ~ Beta(4.5, 95.5)` per spec v1.2.1 §6.1.
- §2.C.5 — C3 ELPD ranking + INDISTINGUISHABLE verdict + HALT-on-flip preservation.
- §2.C.6 — C4 π(t) post-fix closed form: `K⋆·ε²·(X̄/Ȳ)²·(4ωt·cos(4ωt) − sin(4ωt)) / (64·ω·√σ₀·t²)`.
- §2.C.7 — C4 perpetual identity sympy exact zero + numerical residual 6.31e-9.
- §2.C.8 — C4 5-test-point sign cert PASS magnitudes Z = 4453–4922 COP/mo.

**§2.D Empirical artifacts (each gets a cite-block, not a new claim):**

- §2.D.1 — `synthetic_tau_t.parquet` (3 months × 712k draws × 3 tiers).
- §2.D.2 — `cohort_prior.parquet`.
- §2.D.3 — `gate_verdict.json` (24/24 PASS primary; cite full sha256).
- §2.D.4 — `PRIMARY_RESULTS.md`.
- §2.D.5 — `ROBUSTNESS_RESULTS.md`.
- §2.D.6 — `revenue_form_verdict.json` (INDISTINGUISHABLE).
- §2.D.7 — `Z_cap_pinned.json` (schema v1.1; 5/5 sign-cert PASS; cite full sha256).
- §2.D.8 — `Z_cap_pinned.SIGN_VERDICTS.md` (sidecar; deprecation pending — note in cite-block).

### Task 1.3 — Lock §2 4-part citation format

Every §2 subsection MUST conform to this 4-part format. The Technical Writer brief MUST require it verbatim:

1. **Claim verbatim** — exact restatement (math expression or pin) from PRIMITIVES.md / spec / SaaS note. No paraphrase.
2. **Post-cycle form** — what the Stage-2 forward-fix cycle did to the claim (specialized / corrected / extended / unchanged). One sentence.
3. **Code pointer** — `file:line` (resolved against HEAD `9fd92e5`) where the math is encoded, AND the pytest test name verifying it. Both required; either missing → MQ BLOCK in Phase 3.
4. **Artifact pointer** — sha256 of the supporting `audit_block` from the relevant emitted artifact (when applicable). Cite full sha256 (no truncation in §5; truncation acceptable in §2 with last-4-char tail kept consistent). The two anchor tails are pinned: `Z_cap_pinned.json::audit_block` ends in `...5d31`; `gate_verdict.json::audit_block` ends in `...2173`. Any §2 truncation MUST preserve those exact 4-char tails (head-prefix + `...` + tail).

### Task 1.4 — Lock §4 case-study format

Each §4.X case study MUST include:

- The pre-fix claim (verbatim from earlier scratch / first-attempt notes if available; from spec otherwise).
- The pathology that surfaced (citation: which independent-audit verdict file flagged it, FLAG/BLOCK ID).
- The detection heuristic that caught it — explicitly enumerate one of: free-symbol audit / derivation-anchor citation check / tautological-identity audit / sign-target retro-fit audit (mirroring `feedback_post_hoc_fit_anti_fishing_pattern.md`). The early signal (test, sanity check, dimensional analysis) that surfaced the pathology pre-merge.
- The fix applied (citation: CORRECTIONS-α version + the specific cohort plan §).
- The numeric or symbolic evidence the fix worked (citation: pytest test name + sha256 anchor).
- The lesson for Stage-3 implementers — one sentence, no magnitude promises.

### Task 1.5 — Lock §6 Stage-3 hand-off invariants

The §6 hand-off MUST explicitly enumerate (the Technical Writer brief lists these as required bullets):

- Stage-2 used **synthetic-Bayesian only** — no real-data calibration; Stage-3 must test against real data.
- Stage-2 emitted a **single FX trajectory** (M5 pin); Stage-3 must extend to a trajectory family.
- Stage-2 froze pricing at Sonnet $7.1495/MTok (M3); Stage-3 must re-pin with current pricing.
- Stage-2 24-cell sign cert is over a parameter family per spec §5.2; Stage-3 must verify whether real-data parameters fall inside the certified bracket.
- Stage-2 Z = 4453–4922 COP/mo magnitudes are **synthetic and certify only sign**; Stage-3 must NOT inherit these as magnitude predictions.
- Stage-2 INDISTINGUISHABLE revenue-form verdict (C3) is a HALT-on-flip preservation; Stage-3 must re-run on real data and respect the HALT semantic.

The §6 must NOT promise that "real data will scale up," "magnitudes will increase," or any equivalent. Anti-fishing.

### Task 1.6 — Verification matrix (8-row)

The §2 backbone has 8 claim-classes. The Technical Writer brief MUST include this matrix and the §3 re-verify must walk through it:

| # | Claim class | Phase 1 (structure pin) | Phase 2 (implementation) | Phase 3 (re-verify) |
|---|---|---|---|---|
| 1 | Eq. (6)–(11) primitives (§2.A.1–.5) | listed in Task 1.2 | TW resolves `file:line` in `simulations/` + pytest name | RC: `git grep` confirms line; MQ: math correctness |
| 2 | §6 / §10 / §11 references (§2.A.6–.8) | listed | TW resolves PRIMITIVES.md `file:line` | RC: anchor exists; MQ: pointer faithful |
| 3 | M1 TruncPareto α≥1.5 (§2.B.1) | listed | TW resolves sampler-Callable + property test | RC: `pytest --collect-only` finds test; MQ: floor enforced |
| 4 | M2 Softplus L¹<10⁻³·κ (§2.B.2) | listed | TW resolves regularizer-Callable + test | RC: line resolves; MQ: bound symbolically correct |
| 5 | M3/M4/M5 pins (§2.B.3–.5) | listed | TW resolves spec line + emit-test | RC: spec line at HEAD `9fd92e5` matches; MQ: pin literal matches |
| 6 | C1/C2/C3/C4 forward-fix claims (§2.C.1–.8) | listed | TW resolves cohort plan § + test name + sha256 | RC: sha256 matches `audit_block`; MQ: derivation correct. *(This row applies to all 8 §2.C entries; per-claim verification is per the §2.C.{1..8} subsections — RC + MQ Wave-1 briefs (Task 3.1) MUST emit per-§2.C.{1..8} verdicts, not a single aggregate verdict, to avoid roll-up masking.)* |
| 7 | Empirical artifacts (§2.D.1–.8) | listed | TW cites full sha256 from inventory worksheet | RC: re-hash matches; MQ: schema v1.1 compliance for Z_cap_pinned.json |
| 8 | §5 reproducibility cert (the two anchor sha256: `1fb1f7a4...`, `4da660b5...`) | pre-pinned in Task 0.3 | TW transcribes verbatim | RC: both sha256 re-hash matches at HEAD `9fd92e5` |

### Task 1.7 — Commit Phase-1 structure-pin record

- [ ] **Step 1** — Append the Phase-1 locked skeleton (Tasks 1.1–1.6) to the worksheet `scratch/2026-05-09-stage-2-results-preflight/STRUCTURE_PIN.md`.
- [ ] **Step 2** — `git add scratch/2026-05-09-stage-2-results-preflight/STRUCTURE_PIN.md`
- [ ] **Step 3** — `git commit -m "structure-pin(stage-2-results): §0–§7 skeleton + 8-row verification matrix locked"`

---

## Phase 2 — Implementation (Technical Writer dispatch)

### Task 2.1 — Author the Technical Writer brief

**Files:** Create: `scratch/2026-05-09-stage-2-results-preflight/TECHNICAL_WRITER_BRIEF.md`.

The brief MUST contain (foreground assembles; no agent dispatch yet):

- [ ] **Step 1** — Output path: `notes/STAGE_2_RESULTS.md`.
- [ ] **Step 2** — Required §-skeleton: copy Task 1.1 verbatim.
- [ ] **Step 3** — Required §2 subsection list: copy Task 1.2 verbatim.
- [ ] **Step 4** — Required 4-part citation format: copy Task 1.3 verbatim.
- [ ] **Step 5** — Required §4 case-study format: copy Task 1.4 verbatim.
- [ ] **Step 6** — Required §6 hand-off invariants: copy Task 1.5 verbatim, with the explicit anti-magnitude-promise constraint emphasized.
- [ ] **Step 7** — sha256 source-of-truth: cite the worksheet from Task 0.3 + the two anchor values (`Z_cap_pinned.json::audit_block` → `1fb1f7a4...`; `gate_verdict.json::audit_block` → `4da660b5...`). Brief states: any divergence from these two values during authoring → HALT, do not proceed.
- [ ] **Step 8** — Source-file map: brief lists candidate codepaths the TW must resolve to `file:line`:
  - `simulations/saas_builder/priors.py`, `model.py`, `diagnostics.py`, `emit.py`
  - `simulations/saas_builder/cohort_2/`, `cohort_3/`, `cohort_4/`
  - `simulations/modules/`, `simulations/types/`, `simulations/utils/`
  - `simulations/tests/` (for pytest names)
  - `notes/PRIMITIVES.md` (line anchors for Eq. 6/7/8/10/11 and §6/§10/§11)
  - `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (for M1–M5 + §5.2 + §6.1 + §10)
- [ ] **Step 9** — Anti-fishing constraint block (verbatim in brief): "STAGE_2_RESULTS.md cannot introduce any new claim not already in spec / PRIMITIVES.md / SaaS note / code at HEAD `9fd92e5`. Anything resembling a new claim → HALT. Each citation must be verified at authoring-time (`file:line` resolves; test exists in `pytest --collect-only` output; sha256 matches inventory worksheet)."
- [ ] **Step 10** — Style constraints: prose for §0, §1, §6; tables/structured-cites for §2, §3, §5; case-study narrative for §4; bibliography for §7. No emojis. No magnitude editorialization.
- [ ] **Step 11** — Commit the brief.
  - `git add scratch/2026-05-09-stage-2-results-preflight/TECHNICAL_WRITER_BRIEF.md`
  - `git commit -m "brief(stage-2-results): Technical Writer dispatch brief — locked §-skeleton + 4-part cite format + anti-fishing constraint"`

### Task 2.2 — Dispatch Technical Writer

- [ ] **Step 1** — Foreground dispatches a single `Technical Writer` agent with the brief from Task 2.1 as its task description.
- [ ] **Step 2** — Wait for agent completion. Agent output: `notes/STAGE_2_RESULTS.md`.
- [ ] **Step 3** — Foreground sanity-check (NOT a re-verify; that is Phase 3): file exists, non-empty, top-level §0–§7 headers present in correct order, no obvious placeholder strings (`TBD`, `TODO`, `FIXME`, `[fill in]`).
- [ ] **Step 4** — If sanity-check fails: re-dispatch Technical Writer with sanity-check failure list. Do NOT foreground-edit the file.
- [ ] **Step 5** — On sanity-check pass, commit:
  - `git add notes/STAGE_2_RESULTS.md`
  - `git commit -m "feat(stage-2-results): notes/STAGE_2_RESULTS.md — math claims + cohort cross-cut + reproducibility cert (PENDING-REVERIFY)"`

---

## Phase 3 — Independent re-verify (RC + MQ 2-wave)

### Task 3.1 — Wave-1 dispatch (parallel)

- [ ] **Step 1** — Foreground dispatches `Reality Checker` with brief: "Verify every `file:line` pointer in `notes/STAGE_2_RESULTS.md` resolves at HEAD `9fd92e5`. Verify every pytest test name resolves via `pytest --collect-only`. Verify every sha256 cited in §2.D and §5 matches a re-hash of the cited artifact. Output: `scratch/2026-05-09-stage-2-results-reverify/RC_WAVE_1.md` with per-citation PASS/FLAG/BLOCK verdicts."
- [ ] **Step 2** — In parallel, foreground dispatches `Model QA Specialist` with brief: "Verify each §2 claim's mathematical correctness (does the cited code/test actually encode the claimed math?). Verify §4 case-study derivations (C1 marginalization sum-out exactness; C2 bracket re-orientation matches spec §5.2; C4 1/κ correction). Verify §6 hand-off makes no magnitude promise. Output: `scratch/2026-05-09-stage-2-results-reverify/MQ_WAVE_1.md`."
- [ ] **Step 3** — Wait for both. Read both verdicts.

### Task 3.2 — Adjudicate Wave-1

- [ ] **Step 1** — Foreground writes `scratch/2026-05-09-stage-2-results-reverify/WAVE_1_ADJUDICATION.md` summarizing union of BLOCKs and FLAGs.
- [ ] **Step 2** — If BLOCK count = 0 and FLAG count = 0: skip to Task 3.4.
- [ ] **Step 3** — Otherwise: dispatch Technical Writer (CORRECTIONS pass) with the union list as input. TW produces revised `notes/STAGE_2_RESULTS.md` + a CORRECTIONS-α appendix (§8) listing each fix. Commit.

### Task 3.3 — Wave-2 dispatch (parallel; only if Task 3.2 made changes)

- [ ] **Step 1** — Same dispatch pattern as Task 3.1, but agents re-read the post-CORRECTIONS doc. Output paths: `RC_WAVE_2.md`, `MQ_WAVE_2.md`, `WAVE_2_ADJUDICATION.md`.
- [ ] **Step 2** — Termination rule: convergence on zero BLOCKs (FLAGs may carry forward as documented limitations in §6). If Wave-2 still has BLOCKs, dispatch one more CORRECTIONS pass; if Wave-3 still has BLOCKs, HALT and surface to user.

### Task 3.4 — Re-verify completion record

- [ ] **Step 1** — Append final verdict (ACCEPT / ACCEPT_WITH_FLAGS) to `scratch/2026-05-09-stage-2-results-reverify/FINAL.md`.
- [ ] **Step 2** — Commit re-verify artifacts:
  - `git add scratch/2026-05-09-stage-2-results-reverify/`
  - `git commit -m "reverify(stage-2-results): RC+MQ 2-wave — <ACCEPT|ACCEPT_WITH_FLAGS>; <N> BLOCKs resolved, <M> FLAGs documented"`

---

## Phase 4 — Commit + push

### Task 4.1 — Final state commit

- [ ] **Step 1** — Confirm `notes/STAGE_2_RESULTS.md` is the post-Wave-N (terminal-Wave) version; check via `git log --oneline notes/STAGE_2_RESULTS.md`.
- [ ] **Step 2** — Update CLAUDE.md "Active iterations" snapshot if a STAGE_2_RESULTS pointer should appear there. (Optional; foreground decides at Phase 4 time. If yes, separate commit.)

### Task 4.2 — Push branch

- [ ] **Step 1** — `git push origin iter/saas-builder-stage-2`. (No `--force`; no main/master push.)
- [ ] **Step 2** — Optionally open PR via `gh pr create` if user requests; not auto.

---

## Anti-fishing posture

NON-NEGOTIABLE constraints carried throughout:

1. **No new claims.** STAGE_2_RESULTS.md is a results anchor; it CANNOT introduce any claim not already in spec / PRIMITIVES.md / SaaS note / code at HEAD `9fd92e5`. Anything resembling a new claim during authoring or re-verify → HALT.
2. **Citation verification at authoring-time.** Every `file:line` resolves; every pytest name resolves via `pytest --collect-only`; every sha256 matches a re-hash. Phase 2 sanity-check + Phase 3 RC enforce this.
3. **Frozen freeze pin.** Stage-2 is frozen at HEAD `9fd92e5`. STAGE_2_RESULTS.md captures that frozen state and does not auto-update. Future commits beyond `9fd92e5` MUST NOT silently retro-edit STAGE_2_RESULTS.md; they go in STAGE_3_RESULTS.md.
4. **No magnitude promises in §6.** The Stage-3 hand-off section MUST NOT contain phrases like "real data will scale up," "magnitudes are expected to increase," or equivalents. Sign certs are sign certs; magnitudes are synthetic.
5. **HALT semantics preserved.** The C3 INDISTINGUISHABLE / HALT-on-flip semantic must be preserved as a HALT instruction for Stage-3, not softened to a recommendation.
6. **No truncated sha256 in §5.** §5 reproducibility cert cites the two anchor sha256 values in full. Truncation only permitted in §2 cite-blocks with consistent last-4-char tail.

---

## Self-review checklist

Run this before declaring the plan ready:

- [ ] **Spec coverage.** Every item in the user brief's "Document content scope" appears in Task 1.2 (8 primitives + 5 pins + 8 forward-fix claims + 8 artifacts = 29 §2 entries).  ✓
- [ ] **Spec coverage.** Every item in the user brief's "Plan structure" appears as a Phase 0–4 task: pre-flight (Phase 0), structure pin (Phase 1), implementation/Technical Writer dispatch (Phase 2), independent re-verify (Phase 3), commit + push (Phase 4).  ✓
- [ ] **Spec coverage.** Strategic delegation map present (top of plan).  ✓
- [ ] **Spec coverage.** Anti-fishing posture enumerates all 4 user-brief constraints (no new claims; citation verification; frozen freeze pin; no magnitude promises).  ✓
- [ ] **Spec coverage.** Verification matrix is 8-row (Task 1.6).  ✓
- [ ] **Placeholder scan.** No `TBD`, `TODO`, `fill in`, `similar to Task N`, "add appropriate error handling," or naked references to undefined methods.  ✓
- [ ] **Type/citation consistency.** sha256 anchor values cited identically in Task 0.3, Task 1.6 row 8, Task 2.1 Step 7: `Z_cap_pinned.json::audit_block` head `1fb1f7a4...` tail `...5d31`; `gate_verdict.json::audit_block` head `4da660b5...` tail `...2173`.  ✓
- [ ] **Type/citation consistency.** Output path `notes/STAGE_2_RESULTS.md` cited identically in goal, file structure, Task 2.1, Task 2.2, Task 3.1, Task 4.1.  ✓
- [ ] **Type/citation consistency.** Freeze-pin HEAD `9fd92e5` cited identically in goal, Task 0.1, Task 1.6, Task 3.1, anti-fishing §3.  ✓
- [ ] **Code-agnostic.** No code blocks except shell commands (allowed by precedent `2026-05-07-sim-infra-0.md`).  ✓
- [ ] **Foreground-no-author rule.** Phase 2 dispatches Technical Writer; Phase 3 dispatches RC + MQ; foreground only orchestrates and does sanity-checks (no editing of `notes/STAGE_2_RESULTS.md`).  ✓

---

## References

- Format precedent: `docs/plans/2026-05-07-sim-infra-0.md`
- Predecessor notes: `notes/PRIMITIVES.md`, `notes/SaaS_Builders_AI_NativeBuilders.md`
- Spec: `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` v1.2.1
- Cohort plans: `docs/plans/2026-05-08-saas-cohort-{1,2,3,4}-*.md` + `docs/plans/2026-05-09-saas-cohort-close.md`
- Skill: `superpowers:writing-plans`
- Repo memories: `feedback_no_code_in_specs_or_plans`, `feedback_specialized_agents_per_task`, `feedback_pathological_halt_anti_fishing_checkpoint`, `feedback_post_hoc_fit_anti_fishing_pattern`

---

## CORRECTIONS-α v0.1 → v0.2

Wave-1 plan-doc verify (RC + MQ, 2026-05-08) returned `ACCEPT_WITH_FLAGS` from both reviewers — RC with 2 BLOCKs + 3 FLAGs; MQ with 3 FLAGs. Anti-fishing posture: this revision is strictly tightening; no fix relaxes any pin or invariant. The two BLOCKs are factual corrections (sha attribution + git-semantic); the FLAGs are documentation precision. Architectural soundness was acknowledged by both reviewers.

**Verdict file citations:**
- RC: `scratch/2026-05-09-stage-2-results-anchor-plan-review/rc-verdict.md`
- MQ: `scratch/2026-05-09-stage-2-results-anchor-plan-review/mq-verdict.md`

### BLOCK resolutions

- **BLOCK-1 — Freeze-pin commit subject misattributed (RC L16–26, plan L20).** The plan v0.1 quoted the subject of `9fd92e5` as the CORRECTIONS-α v0.4 marginalization line; that subject actually belongs to `80f4ed4`. Resolution: keep `9fd92e5` as the freeze pin (it is the canonical Stage-2 verdict-memo commit), correct the quoted subject to `"deliverable(saas-cohort): Stage-2 modeling memo + Phase-4 schema-bump audit"`, and explicitly note that `80f4ed4` (CORRECTIONS-α v0.4 marginalization closure) is an ancestor of `9fd92e5`. Applied at "Stage-2 freeze pin" line of plan front-matter.
- **BLOCK-2 — `git rev-parse HEAD` collides with current HEAD (RC L28–35, plan L54).** Current HEAD is two cosmetic commits past `9fd92e5` (memory hygiene + sim-README), so a literal HEAD-equals-pin check would spuriously HALT. Resolution: replaced Phase 0 Task 0.1 Step 1 with the ancestor-check + path-scoped diff-empty check (`git merge-base --is-ancestor 9fd92e5 HEAD` AND `git diff 9fd92e5 HEAD -- simulations/ docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` empty). Cosmetic post-freeze commits outside those paths are explicitly permitted.

### FLAG resolutions

- **RC-FLAG-1 — cohort-close plan reference (RC L41–43).** ACK only — the cohort-close plan inclusion in Phase 0 Task 0.2 Step 3 is a correct expansion of the user brief and is already cross-referenced in §7. No code change.
- **RC-FLAG-2 — verdict memo path resolution (RC L45–47, plan L67).** Replaced fuzzy `find scratch ... -iname '*verdict*memo*'` with hard-pinned path `docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md`.
- **RC-FLAG-3 — sha256 truncation tail policy (RC L49–51, plan L177).** Added explicit 4-char anchor tails to the §2 citation format spec: `Z_cap_pinned.json::audit_block` ends in `...5d31`; `gate_verdict.json::audit_block` ends in `...2173`. Any §2 truncation MUST preserve those exact tails. Self-review checklist row also updated with both head + tail.
- **MQ-FLAG-1 — §2.A.8 §11 scope extension (MQ L18–21).** Added a one-line note at §2.A.8 documenting that §11 is a faithful, minimal expansion of the user brief's "§6, §10" enumeration (it is the natural Carr-Madan replication anchor for C4 and is C2-adjacent). Not a covert addition.
- **MQ-FLAG-2 — §4 case-study detection-heuristic bullet (MQ L26–28, plan Task 1.4).** Inserted an explicit "detection heuristic" bullet between (b) pathology and (c) fix applied. The bullet enumerates the four detection patterns from `feedback_post_hoc_fit_anti_fishing_pattern.md`: free-symbol audit / derivation-anchor citation check / tautological-identity audit / sign-target retro-fit audit.
- **MQ-FLAG-3 — verification matrix row 6 granularity (MQ L38–39, plan Task 1.6).** Added an in-row note to row 6 stating that the row applies to all 8 §2.C entries and that RC + MQ Wave-1 briefs (Task 3.1) MUST emit per-§2.C.{1..8} verdicts, not a single aggregate verdict, to avoid roll-up masking.

### Re-verify expectation

RC + MQ Wave-2 plan-doc reverify dispatch on v0.2 will be triggered by the orchestrator before Phase 0 execution. Convergence target: zero BLOCKs from both reviewers. FLAGs may carry forward as documented limitations.
