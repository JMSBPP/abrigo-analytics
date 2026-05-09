# Simulations Notebooks — SaaS-Builder Stage-2 (Math × Code Anchor) — Design

**Iteration**: SaaS-Builder (Y, M, X) Stage-2 — post-cycle anchor artifact
**Branch**: `iter/saas-builder-stage-2`
**Date**: 2026-05-09
**Status**: DESIGN v0.2 (awaiting Wave-1 RC+MQ verify before writing-plans hand-off)
**Version**: v0.2 (verify/ sub-package added per user question 2026-05-09)
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

## 3a. Verify-API sub-package (`simulations/saas_builder/verify/`)

The notebooks do not reach into internal modules directly. Instead, a
purpose-built verify-API surface is added under
`simulations/saas_builder/verify/`, sized exactly for the verify-only
contract of §5. This keeps notebook code cells minimal (math density
stays in WHY/INTERPRETATION markdown), centralizes assertion logic so
it is pytest-able, and gives Stage-3 a stable surface so internal
module restructuring does not break the math anchor.

### 3a.1 Layout (three-tier discipline preserved)

```
simulations/saas_builder/verify/
├── __init__.py     ← explicit __all__: 8 verify_r{1..8}_* + 4 load_*
├── types.py        ← Value tier   — frozen Verdict dataclasses
├── checks.py       ← Callable tier — free pure functions, one per R-tag
└── io.py           ← IO Boundary  — committed-artifact loader + sha256
```

Tier-import discipline (NON-NEGOTIABLE per `simulations/README.md`):
`types.py` imports stdlib + numpy only; `checks.py` imports
`simulations.saas_builder.verify.types` and the relevant
`simulations.modules` callables; `io.py` imports `verify.types` and
performs the only filesystem reads. No tier inversion; no inheritance
beyond `Protocol` / `Exception`.

### 3a.2 Value-tier contract

```
@dataclass(frozen=True)
class RTagVerdict:
    r_tag: str                    # "R1" .. "R8"
    passed: bool
    expected: float | None        # closed-form / pinned value
    actual: float | None          # computed-or-loaded value
    residual: float | None        # |expected - actual|, when meaningful
    audit_sha256: str | None      # tamper-trail anchor
    message: str                  # human-readable summary

@dataclass(frozen=True)
class TrioRollup:
    verdicts: tuple[RTagVerdict, ...]   # length 8 in canonical order
    all_passed: bool
```

`RTagVerdict` is the single Value type returned by every verifier;
notebooks bind one per cell and `assert v.passed, v.message`.
`TrioRollup` is consumed only at notebook end-of-trio summary cell.

### 3a.3 Callable-tier contract — one free pure function per R-tag

| Function | Inputs | Source of truth |
|---|---|---|
| `verify_r1_sigma_0_anchor` | `x_bar, y_bar, eps, expected, tol` | PRIMITIVES (8); verdict memo §1 σ₀ = 20,000 |
| `verify_r2_kappa_eliminated_in_pi_t` | (none — sympy live) | `feedback_post_hoc_fit_anti_fishing_pattern` free-symbol audit |
| `verify_r3_perpetual_identity_residual` | `tol` | Verdict memo §1: residual ≤ 6.31e-9 |
| `verify_r4_bracket_cardinality` | `brackets` | spec v1.2.1 §5.2 (3 × 2 × 2 × 2 = 24) |
| `verify_r5_marginalization_match` | `posterior_path, tol` | C1 v0.4 marginalization (memo §6) |
| `verify_r6_softplus_l1_tightness` | `kappa, tol_factor` | M2 pin: `tightness_l1_deviation < 1e-3·κ` |
| `verify_r7_s_t_pin` | `gate_verdict` | spec v1.2.1 §6.1: `S_t = (1-λ)^t`, `λ ~ Beta(4.5, 95.5)` |
| `verify_r8_z_cap_closed_form` | `z_cap_pinned` | Verdict memo §1: 4,687.94 COP/mo, 95% CI [168.17, 14,606.14] |

All eight return `RTagVerdict`. None mutate. None do filesystem I/O —
loaders in §3a.4 produce the dict inputs.

### 3a.4 IO-Boundary-tier contract

```
class CommittedArtifactLoader:
    def __init__(self, data_root: Path) -> None: ...
    def load_z_cap_pinned(self) -> ZCapPinnedDict: ...
    def load_gate_verdict(self) -> GateVerdictDict: ...
    def load_revenue_form_verdict(self) -> RevenueFormVerdictDict: ...
    def load_audit(self) -> AuditDict: ...
```

The TypedDict row schemas are reused from
`simulations.utils.parquet_io` / `simulations.utils.json_io` per Phase 2
M4 pin — no schema duplication. `audit_sha256` is computed once at
load time and threaded through every `RTagVerdict.audit_sha256`.

### 3a.5 Notebook code-cell shape (post-API)

```python
loader = CommittedArtifactLoader(DATA_ROOT)
v = verify_r8_z_cap_closed_form(z_cap_pinned=loader.load_z_cap_pinned())
assert v.passed, v.message
print(f"{v.r_tag}: Z_cap = {v.actual:,.2f} COP/mo  "
      f"(residual {v.residual:.2e}; audit {v.audit_sha256[:8]}…)")
```

### 3a.6 pytest coverage (mandatory)

`simulations/tests/test_verify.py` exercises each verifier with at
least: (a) committed-artifact happy path, (b) injected-drift failure,
(c) for `verify_r2_kappa_eliminated_in_pi_t`, a deliberate `1/κ`
re-introduction that must fail (regression guard for the C4 case
study). ≥ 16 test cases total (≥ 2 per verifier).

### 3a.7 Cost

~250–350 LOC across 4 new files; ~16 new pytest cases. Adds one phase
to the implementation plan (verify-API authoring) before notebook
authoring. Net positive: math cells stay thin and Stage-3 churn cannot
break the math anchor.

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

| R | Verifier function (§3a.3) | Code-cell asserts |
|---|---|---|
| R1 | `verify_r1_sigma_0_anchor` | `σ₀ = (X̄/Ȳ)²·ε²/8` numerically; expected σ₀ = 20,000 (per verdict memo §1) within tolerance |
| R2 | `verify_r2_kappa_eliminated_in_pi_t` | `κ ∉ free_symbols(π(t))` (sympy free-symbol audit — anti-fishing live demo); π(t) reduces to the boxed (4ωt cos − sin) form |
| R3 | `verify_r3_perpetual_identity_residual` | Perpetual identity `Δ^{(a_s)}_∞ = lim_{t→∞} Δ^{(a_s)}_t` residual ≤ 1e-8 (memo §1: 6.31×10⁻⁹) |
| R4 | `verify_r4_bracket_cardinality` | `len(brackets) == 24`; product is `3 tiers × 2 α × 2 cache × 2 κ`; matches spec §5.2 verbatim |
| R5 | `verify_r5_marginalization_match` | Marginalization sum-out: empirical posterior mean from saved chain trace matches analytic marginal at the same nodes (Phase 2 N_draws ≥ 712k) |
| R6 | `verify_r6_softplus_l1_tightness` | softplus L¹ deviation < 1e-3·κ on [0, 2κ] (M2 pin); load `revenue_form_verdict.json` and re-derive |
| R7 | `verify_r7_s_t_pin` | `gate_verdict.json` contains `lambda_prior: Beta(4.5, 95.5)` and `S_t_form: "(1-lambda)^t"`; HALT-on-flip token unchanged |
| R8 | `verify_r8_z_cap_closed_form` | `Z_cap_pinned.json::Z_cap == 4687.94` (within parquet tolerance); 95% CI lower bound > 0 |

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
- [ ] `simulations/saas_builder/verify/` sub-package exists with the
      §3a layout; `__init__.py` declares `__all__` explicitly.
- [ ] `simulations/tests/test_verify.py` covers every R-tag with
      ≥ 2 cases (happy + injected drift); test count ≥ 16.
- [ ] Notebook code cells contain no direct parquet/JSON file reads
      (all I/O routes through `CommittedArtifactLoader`).
- [ ] Notebook code cells import only from
      `simulations.saas_builder.verify` and `env.py` — no reach into
      `simulations.modules` / `simulations.utils` internals.

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

---

## CORRECTIONS-α — v0.1 → v0.2

**Trigger.** User question 2026-05-09: *"Do we need to define [an] API to
abstract away implementation on the modules?"* The v0.1 design had
notebooks reaching directly into `simulations.types` /
`simulations.modules` / raw committed JSON. This created three problems:
(i) Stage-3 internal renames would break notebooks needlessly; (ii)
assertion logic scattered across notebook cells could not be
pytest-tested; (iii) the verify-only contract was implicit rather than
named.

**Patch.** Added §3a — a purpose-built `simulations/saas_builder/verify/`
sub-package with three-tier discipline preserved (Value `types.py` /
Callable `checks.py` / IO Boundary `io.py`), 8 free-pure-function
verifiers (one per R-tag), a `CommittedArtifactLoader` IO class, and a
mandatory `simulations/tests/test_verify.py` with ≥ 16 cases. §4 R-tag
table now references the verifier functions. §9 success criteria gained
4 new bullets covering the verify-API surface.

**Posture.** Strictly tightening: the verify-API is a *named* contract
where v0.1 had implicit cell-scope conventions. Math content unchanged.
R1–R8 set unchanged. Verify-only mode unchanged. No upstream pin
relaxed.

**Anti-fishing impact.** R2's `κ ∉ free_symbols(π(t))` check moves from
"a notebook cell" to "a pytest case in `test_verify.py`" — the C4 1/κ
detection is now part of CI, not just a notebook-execution-time check.
Strictly stronger.

End of design (v0.2).

