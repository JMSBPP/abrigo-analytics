# Simulations Notebooks — SaaS-Builder Stage-2 (Math × Code Anchor) — Design

**Iteration**: SaaS-Builder (Y, M, X) Stage-2 — post-cycle anchor artifact
**Branch**: `iter/saas-builder-stage-2`
**Date**: 2026-05-09
**Status**: DESIGN (awaiting user approval before writing-plans hand-off)
**Audience**: future Stage-3 implementer; supervisor / advisor review;
contributor onboarding into the `simulations/` package

---

## 1. Purpose

Author a notebook trio under `simulations/notebooks/saas_builder_stage_2/`
that pairs the math anchors of `notes/STAGE_2_RESULTS.md` (R1–R8) against
the actual Phase 2 simulation code committed under
`simulations/saas_builder/`. Each R-tag becomes a HALT-checkpoint trio
(why-markdown / code-cell / interpretation-markdown) per
`memory/feedback_notebook_trio_checkpoint.md`. The trio's primary
contract is: **the closed forms documented in STAGE_2_RESULTS.md hold
numerically at the committed artifact values**. If they don't, the
notebook breaks loudly and Stage-3 contributors are forced to update the
math anchor or the artifact in lockstep.

This is not data exploration; the data-EDA tree at
`notebooks/saas_builder_stage_2/` was deliberately empty for this cycle
and remains so. This trio anchors **math against committed simulation
output**, which is why it lives inside the `simulations/` package.

## 2. Location and naming

```
simulations/
├── notebooks/
│   └── saas_builder_stage_2/
│       ├── 01_math_anchors.ipynb
│       ├── 02_cohort_runs.ipynb
│       ├── 03_z_cap_synthesis.ipynb
│       ├── env.py
│       ├── references.bib
│       ├── estimates/         (gitignored; re-emitted JSONs for tamper check)
│       └── figures/           (committed; PDF figures linked from STAGE_2_RESULTS.md)
```

Naming mirrors the canonical trio convention in
`notebooks/dev_ai_cost/`: `01_*.ipynb`, `02_*.ipynb`, `03_*.ipynb`.
`env.py` carries path setup + `np.random.seed(0)` + an
`assert_clean_state()` helper. `references.bib` carries `@PRIMITIVES`,
`@spec_v121`, `@verdict_memo`, `@stage2_results` as citekeys.

## 3. Trio split — R-tag clusters

| Notebook | R-tags | What it loads | Heavy compute? |
|---|---|---|---|
| `01_math_anchors.ipynb` | R1 (σ₀ anchor), R2 (π(t) closed form), R3 (perpetual identity), R4 (24-bracket family enumeration), R5 (C1 marginalization sum-out) | sympy + numpy only; no parquet | No (<30s) |
| `02_cohort_runs.ipynb` | R6 (softplus + M2 tightness), R7 (S_t = (1−λ)^t with λ ~ Beta(4.5, 95.5)) | `gate_verdict.json`, `revenue_form_verdict.json` from `simulations/saas_builder/data/` | No (<30s) |
| `03_z_cap_synthesis.ipynb` | R8 (Z_cap closed form + boxed key result) | `Z_cap_pinned.json`, `_AUDIT.json` | No (<10s) |

The R-tag → notebook mapping is **chosen to keep each notebook
self-contained**: 01 needs only the math primitives, 02 needs C2 + C3
verdicts, 03 needs the C4 emit. No notebook depends on another's
in-memory state.

## 4. Section API per R-tag (the math×code pairing pattern)

Each R-tag produces one trio (one HALT-checkpoint):

```
## §N — Rk: <name>            ← header verbatim from STAGE_2_RESULTS.md §N

### Decision-citation block    ← 4-part per
                                  feedback_notebook_citation_block.md:
                                  reference / why / relevance / connection

### WHY (markdown)             ← LaTeX equation copied verbatim from
                                  STAGE_2_RESULTS.md; predecessor lineage
                                  cited (e.g. PRIMITIVES (8), spec §6.1)

### CODE (cell)                ← imports from simulations.{types, modules,
                                  utils, saas_builder}; loads the committed
                                  artifact OR derives via sympy; asserts the
                                  closed form holds; prints the key value

### INTERPRETATION (markdown)  ← what the assertion proved; numeric residual;
                                  link back to artifact audit_block sha256;
                                  HALT-checkpoint if drift detected
```

R-tag → assertion contract:

| R | Code-cell asserts |
|---|---|
| R1 | `σ₀ = (X̄/Ȳ)²·ε²/8` numerically; reference σ₀ = 20,000 (per verdict memo §1) within tolerance |
| R2 | `κ ∉ free_symbols(π(t))` (sympy free-symbol audit — anti-fishing detection); π(t) reduces to the boxed (4ωt cos − sin) form |
| R3 | Perpetual identity `Δ^{(a_s)}_∞ = lim_{t→∞} Δ^{(a_s)}_t` residual ≤ 1e-8 (memo §1: 6.31×10⁻⁹) |
| R4 | `len(brackets) == 24`; product is `3 tiers × 2 α × 2 cache × 2 κ`; matches spec §5.2 verbatim |
| R5 | Marginalization sum-out: empirical posterior mean from saved chain trace matches analytic marginal at the same nodes (Phase 2 N_draws ≥ 712k) |
| R6 | softplus L¹ deviation < 1e-3·κ on [0, 2κ] (M2 pin); load `revenue_form_verdict.json` and re-derive |
| R7 | `gate_verdict.json` contains `lambda_prior: Beta(4.5, 95.5)` and `S_t_form: "(1-lambda)^t"`; HALT-on-flip token unchanged |
| R8 | `Z_cap_pinned.json::Z_cap == 4687.94` (within parquet tolerance); 95% CI lower bound > 0 |

## 5. Code-playback discipline (NON-NEGOTIABLE)

**Verify-only.** Notebooks never re-run PyMC. They load committed
artifacts under `simulations/saas_builder/data/` and verify the closed
forms at those committed values. Per user decision (Question 1, locked):

> *Notebooks load committed JSON/parquet under
> simulations/saas_builder/data/ and verify each R-tag closed form holds
> numerically. No PyMC, no re-fit. Fast (<60s total), deterministic,
> doubles as tamper detector. Stage-3 contributors break the notebook if
> they change upstream artifacts.*

Consequences:

- Total notebook runtime is bounded at < 60s wall-clock.
- Determinism: any failure is a real artifact drift, not an RNG flake.
- The notebook is **part of the audit chain** — running it is a
  tamper-check on `Z_cap_pinned.json`'s `audit_block` sha256.
- Stage-3 implementers who change upstream parquet must update the
  notebook assertions in the same commit.

There is no opt-in re-execute mode. If a Stage-3 contributor needs the
slow path, they invoke `scripts/run_cohort{1..4}_emit.py` directly.

## 6. Inherited conventions from `notebooks/dev_ai_cost/`

- `env.py` does the `sys.path` setup so `from simulations.types import …`
  works from a notebook kernel; sets `np.random.seed(0)` for any local
  numerical sanity checks; defines `assert_audit_block_sha256(path,
  expected_tail)` to centralize the tamper-check pattern.
- `references.bib` provides citekeys consumed via the `[@…]` markdown
  pattern in WHY cells.
- `estimates/` is gitignored; running the notebook re-emits a small
  JSON sidecar for tamper diff against the committed artifact (helpful
  during Stage-3 churn).
- `figures/` is committed; the trio produces three reference plots that
  Stage-3 docs may reference: π(t) curve over t ∈ [0, 24] months, S_t
  survival under the Beta(4.5, 95.5) prior, σ₀ posterior overlay.

## 7. Anti-fishing posture

- The C4 1/κ case study from the cycle is shown live in
  `01_math_anchors.ipynb` §2 (R2): a sympy free-symbol audit
  (`assert κ not in pi_t.free_symbols`) runs as the first cell after
  the WHY markdown, mirroring the detection heuristic from
  `memory/feedback_post_hoc_fit_anti_fishing_pattern.md`.
- The HALT-on-flip semantic from R7 is preserved: 02 asserts the
  Beta(4.5, 95.5) prior token verbatim from `gate_verdict.json`.
- No magnitude-promise language anywhere in the trio. Verbiage matches
  STAGE_2_RESULTS.md §3 (TODO-COHORT-N closure semantics: DEFERRED /
  CLOSED / INDISTINGUISHABLE).
- Anti-fishing invariants (`N_MIN`, `POWER_MIN`, `MDES_SD`) are not
  re-validated here — that's the verdict memo's job. The trio
  assertions are at the closed-form-identity level, not the gate level.

## 8. Out of scope (deferred / Stage-3)

- Re-execution of cohort drivers — explicitly excluded per §5.
- Real-data conditioning — Stage-3 milestone.
- Hierarchical pooling for C3, Weibull k≠1 falsification, per-tier θ_k
  differentiation — Stage-3 work; the trio anchors the synthetic
  Stage-2 baseline only.
- Panoptic-deployment math (PRIMITIVES §11 discrete-strip replication) —
  out of scope for this artifact.

## 9. Success criteria

- [ ] Three notebooks executable headless with `make notebooks` (or
      `jupyter nbconvert --to notebook --execute`); total wall < 60s.
- [ ] Every R-tag (R1–R8) appears as exactly one trio with the §4 four-cell
      pattern.
- [ ] Each R-tag code cell contains at least one `assert` against a
      committed artifact value or sympy identity.
- [ ] `01_math_anchors.ipynb` §2 contains the explicit
      `κ ∉ free_symbols(π(t))` cell (anti-fishing live demo).
- [ ] `references.bib` resolves all `[@…]` citekeys used in WHY cells.
- [ ] No PyMC import anywhere in the notebook directory.
- [ ] Adding the trio does not change `make verify` semantics (it's
      audit-additive, not gate-altering).

## 10. Open items (for the implementation plan to resolve)

- `make notebooks` target update — does it need a new sub-target for
  `simulations/notebooks/`, or is the existing top-level glob
  sufficient? Plan to verify against the current Makefile during
  Phase 0.
- `references.bib` content — author-year citekeys to be drawn from the
  closest existing `.bib` (likely `notebooks/dev_ai_cost/references.bib`)
  with three additions for PRIMITIVES, spec, verdict memo, and
  STAGE_2_RESULTS.
- Figure generation cell placement — figures live in INTERPRETATION
  cells (per existing trio convention) or as a §"Figures" appendix per
  notebook? Plan to inspect `notebooks/dev_ai_cost/03_*.ipynb` and
  match.

## 11. Cross-references

- `notes/STAGE_2_RESULTS.md` — the math anchor this trio plays code
  against (R1–R8).
- `docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md` — the
  cycle's canonical deliverable; trio assertions check the memo's
  numeric pins.
- `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (spec
  v1.2.1) — §5.2 parameter family enumerated by R4; §6.1 S_t pin
  asserted by R7.
- `simulations/README.md` — user manual section already documents
  reproducibility; the trio is the executable counterpart to that
  narrative.
- `memory/feedback_notebook_trio_checkpoint.md`,
  `memory/feedback_notebook_citation_block.md`,
  `memory/feedback_post_hoc_fit_anti_fishing_pattern.md` — convention
  sources.

End of design.
