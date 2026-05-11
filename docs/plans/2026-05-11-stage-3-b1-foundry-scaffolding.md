# STAGE-3 B1 — Foundry scaffolding against forked Panoptic (Implementation Plan)

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Code-agnostic plan.** Per repo memory `memory/feedback_no_code_in_specs_or_plans.md` (NON-NEGOTIABLE), this plan does NOT contain Python or Solidity code blocks. Each task dispatches a specialized agent who authors code per the functional-python skill (analytics-side) + type-driven-development / evm-tdd skills (Solidity-side, in the cross-repo).
>
> **Foreground orchestrates, never authors.** Per repo memory `memory/feedback_specialized_agents_per_task.md` (NON-NEGOTIABLE).
>
> **Cross-repo plan.** B1 spans two repos: `abrigo-analytics` (this repo) provides the JSON-artifact contract + a stable handoff doc; `thetaSwap-core-dev` (separate repo) houses the Solidity / Foundry implementation. This plan canonicalizes the handoff and the analytics-side guarantees; the Foundry implementation is scoped via the linked plan in `thetaSwap-core-dev` and is dispatched per its OWN review cycle. The Wave-2 RC+MQ review on B1 in THIS repo verifies the handoff contract; the cross-repo plan has its own RC+MQ.

**Plan version:** v0.1 (initial draft — awaiting RC + MQ Wave-1 review per master-spec §6.1)
**Master spec:** `docs/specs/2026-05-11-stage-3-first-wave-design.md` v0.2
**Predecessor:** `simulations/saas_builder/cohort_5_strip/` (commit `3442852`); `IronCondor_strip.json` v1.0 (audit `94150326…`)
**Cross-repo target:** `thetaSwap-core-dev` (Solidity + Foundry harness; out of this plan's commit scope)
**Status:** DRAFT — Wave-1 review dispatch pending
**Estimated wall-time:** 3–5 days analytics-side; cross-repo Foundry work tracked separately

---

## §0 Goal

**One sentence.** Define the analytics-side contract that the contract-side Foundry test harness consumes (JSON schema, audit-block validation, FX-path generator interface, envelope-assertion formula), and produce a cross-repo handoff document that pins everything `thetaSwap-core-dev` needs to write a `forge test` suite asserting net LP P&L tracks the cohort_5_strip's centered-strip envelope within the Pin-S6 35% tolerance.

## §1 Architecture

B1's analytics-side contribution is a **handoff doc + a deterministic FX-path generator** exposed via a tiny CLI so the contract-side Foundry test harness can shell out to it (or alternatively, the FX paths are pre-computed into a JSON fixture that the Foundry test reads). The analytics side does NOT author Solidity.

The cross-repo handoff doc names the exact `thetaSwap-core-dev` commit sha that B1's Wave-2 review checks against. The expectation is that the contract-side team produces (i) a JSON-loader fixture, (ii) the 12-leg position provisioner, (iii) the 24-bracket envelope assertion, and emits a forge-test verdict that this plan's Wave-2 review consumes.

## §2 Tech stack

**Analytics side (in scope of this commit):**
- Python 3.13, functional-python skill.
- Existing `simulations/saas_builder/cohort_5_strip/` package (READ-ONLY consumption).
- New thin CLI module: `simulations/saas_builder/cohort_5_strip/fx_path_emit.py` (additive).

**Contract side (cross-repo, OUT of this commit's scope):**
- Solidity (Foundry / forge), forked-Panoptic fixture.
- evm-tdd skill (`evm-tdd:phases:01-specify`, `02-implement`, `03-verify`).

---

## §3 Cross-spec references

| Master-spec section | What this plan must satisfy |
|---------------------|-----------------------------|
| §2.3 phase 1 (schema-binding) | JSON loader asserts `schema_version == "v1.0"` and `audit_block` matches |
| §2.3 phase 2 (position provisioning) | Document the leg-to-Panoptic-primitive routing convention |
| §2.3 phase 3 (FX-path simulation) | FX generator implements PRIMITIVES.md §6 eq. (6) over the 24-bracket parameter family (Stage-2 spec §5.2) |
| §2.3 phase 4 (envelope assertion) | Centered-strip / β-fit / peak-normalized form per MQ-FLAG-1 disposition |
| §5 P-B1.1 / P-B1.2 | Pin coverage per Wave-2 review |
| §6.1 Wave-1 review | This plan dispatches RC + MQ before execution |
| §8.1 limitation acknowledgement | Cross-repo coordination is light; analytics side does NOT author Solidity |

---

## §4 File structure

```
docs/plans/2026-05-11-stage-3-b1-foundry-scaffolding.md     ← THIS plan
scratch/2026-05-11-b1-foundry-handoff/
├── HANDOFF.md                  Cross-repo coordination doc (canonical handoff contract)
├── FX_PATH_GENERATOR.md        Math + CLI usage doc for the generator
└── ENVELOPE_ASSERTION_PROOF.md MQ-FLAG-1 disposition trace — the canonical formula + numerical example

simulations/saas_builder/cohort_5_strip/
└── fx_path_emit.py             NEW Callable tier: 24-bracket FX-path JSON emitter

simulations/saas_builder/data/
└── fx_paths_24_brackets.json   NEW fixture: pre-computed FX paths per bracket × time grid
```

The `thetaSwap-core-dev` files (`test/integration/StripReplication.t.sol`, etc.) are tracked OUT-OF-REPO; their sha is recorded in HANDOFF.md and verified at B1's Wave-2 review.

---

## §5 Phase 1 — Handoff contract authoring

### Task 1.1 — Draft the cross-repo handoff document

**Files:**
- Create: `scratch/2026-05-11-b1-foundry-handoff/HANDOFF.md`

**Agent dispatch:** `general-purpose` agent (orchestration / coordination authoring; no code).

**Acceptance:**
- §1 Consumed analytics artifacts: full path to `simulations/saas_builder/data/IronCondor_strip.json` + the current audit_block (`94150326…`); pinned commit sha (`3442852`).
- §2 Required Foundry behavior: enumerated as a numbered list — JSON-load + schema_version check, audit_block re-hash, position-provision against forked Panoptic, run all 24 FX-bracket scenarios, assert envelope per Phase-4 formula.
- §3 Envelope assertion formula: the EXACT centered-strip / β-fit / peak-normalized form from master-spec §2.3 phase 4 + `simulations/saas_builder/cohort_5_strip/replication.py:1-28`. NOT the v0.1-spec relative-error form (which had denominator collapse — MQ-FLAG-1).
- §4 FX-path generator: pointer to `fx_path_emit.py` CLI (authored in Task 2.1) + `fx_paths_24_brackets.json` fixture path.
- §5 Cross-repo sha pinning: a `thetaSwap_core_dev_commit_sha` field reserved (populated at B1 Wave-2 review time after the contract-side team merges).
- §6 Out-of-scope clarifier: Streamia premium plumbing (B2 in the master spec deferred list) is NOT part of B1; B1 tests replication mechanics only.
- §7 Anti-pattern callouts: the Foundry test must NOT (i) re-derive the 35% tolerance from PRIMITIVES.md §12 row 1's 5%, (ii) silently relax the tolerance, (iii) reduce the 24-bracket family to a subset without master-spec amendment.

**Commit message:** `handoff(stage-3-b1): cross-repo coordination doc + envelope-assertion formula pin`

---

### Task 1.2 — Author the envelope-assertion proof trace

**Files:**
- Create: `scratch/2026-05-11-b1-foundry-handoff/ENVELOPE_ASSERTION_PROOF.md`

**Agent dispatch:** `general-purpose` (mathematical writeup; no code).

**Acceptance:**
- Walks through the centered-strip / β-fit / peak-normalized form step by step using the canonical TP1 fixture; produces the same `max_relative_error ≈ 0.28` number that `CarrMadanEnvelopeVerifier` reports on the current emitted strip (the run output recorded in `simulations/saas_builder/cohort_5_strip/IronCondor_strip.STRIKES.md` is the reference).
- Includes a §"Why not |Π−K̂σ|/|K̂σ|" section explaining the denominator-collapse failure mode (MQ-FLAG-1 historical record); references the spec v0.1 → v0.2 CORRECTIONS-α v9.1 entry.
- Includes a §"σ_T computation contract" that pins the realized-variance formula PRIMITIVES.md eq. (7) over each bracket × time-grid; this is the formula the Foundry test must use to compare `K̂·σ_T` against centered-strip P&L.

**Commit message:** `proof(stage-3-b1): canonical envelope-assertion formula + numerical example`

---

## §6 Phase 2 — FX-path generator (analytics side)

### Task 2.1 — Author the FX-path emitter

**Files:**
- Create: `simulations/saas_builder/cohort_5_strip/fx_path_emit.py`
- Create: `simulations/tests/test_saas_cohort5_fx_path_emit.py`
- Create: `scratch/2026-05-11-b1-foundry-handoff/FX_PATH_GENERATOR.md` (usage doc)

**Agent dispatch:** `Senior Developer` (frozen-dc Callable tier authoring per functional-python skill).

**Acceptance:**
- `FXPathEmitter` frozen-dc with `__call__(brackets: tuple[ParameterBracket, ...], time_grid: TimeGrid) -> Mapping[BracketId, FloatArray]`.
- `ParameterBracket` Value type with `(tier, alpha_arm, cache_regime, kappa_arm)` matching Stage-2 spec §5.2 24-bracket parameter family.
- The FX-path generator implements PRIMITIVES.md §6 eq. (6) verbatim: $(X/Y)_t(\varepsilon, \omega) = (1 + \varepsilon\,(\cos^2(\omega t) - 1/2))\,\overline{X/Y}$.
- The (ε, ω) mapping from each bracket is derived from the Stage-2 spec §5.2 index sets (Phase 1 Task 1.1 acknowledges this is a known mapping pinned at cohort_2; the generator MUST re-import the mapping from `simulations.saas_builder.cohort_2.types` if it exists, NOT re-derive it).
- One Hypothesis property test: for any valid `(ε, ω, t)` triple, the emitted FX value lies in `[(1 - ε/2), (1 + ε/2)] · X̄/Ȳ` (PRIMITIVES.md §6 eq. (6) constraint).
- One regression test: emit at the canonical TP1 bracket and compare against a hard-coded fixture array (pin-fixture pattern — locks the FX-path values bit-reproducibly).
- A `simulations/saas_builder/cohort_5_strip/__init__.py` re-export of `FXPathEmitter` + `ParameterBracket`.

**Commit message:** `feat(cohort_5_strip): 24-bracket FX-path emitter for B1 Foundry handoff`

---

### Task 2.2 — Pre-compute and emit fx_paths_24_brackets.json

**Files:**
- Create: `simulations/saas_builder/data/fx_paths_24_brackets.json` (gitignored; reproducible-from-source)
- Create: a one-shot script entry-point on the `FXPathEmitter` IO Boundary (Task 2.1 frozen-dc is Callable; the IO Boundary wrapper that writes JSON lives in a new `fx_path_io.py` file).
- Modify: `simulations/saas_builder/cohort_5_strip/__init__.py` to export the IO Boundary class.

**Agent dispatch:** `Senior Developer`.

**Acceptance:**
- `FXPathJSONEmitter` IO Boundary class with `__init__(emit_dir, ...)` + `__call__()` that runs `FXPathEmitter` over the 24 brackets and emits a deterministic JSON fixture.
- JSON schema:
  ```
  {
    "schema_version": "v1.0",
    "primitives_anchor": "PRIMITIVES.md §6 eq. (6)",
    "n_brackets": 24,
    "time_grid": {"t_start_months": <float>, "t_end_months": <float>, "n_points": <int>},
    "brackets": [
      {"bracket_id": "<str>", "tier": "<str>", "alpha_arm": <int>, "cache_regime": "<str>", "kappa_arm": <int>,
       "epsilon": <float>, "omega": <float>, "x_over_y_bar": 4000.0,
       "fx_path": [<float>, <float>, ...]}, ...
    ],
    "audit_block": "<sha256>"
  }
  ```
- `audit_block` hashes the serialized payload sans the audit_block field (mirrors cohort_5_strip's `_compute_strip_audit_block` convention).
- Round-trip read-back equality enforced.
- 24 brackets emitted; one Hypothesis property test confirms `len(brackets) == 24` and the (tier × α × cache × κ) factorization is `3 × 2 × 2 × 2`.

**Commit message:** `data(cohort_5_strip): fx_paths_24_brackets.json fixture for B1 Foundry handoff`

---

## §7 Phase 3 — Cross-repo dispatch + handoff sha pin

### Task 3.1 — Open the cross-repo plan in `thetaSwap-core-dev`

**Files (cross-repo, OUT of this commit's scope):**
- `thetaSwap-core-dev/docs/plans/2026-05-{NN}-stage-3-b1-strip-replication-foundry.md`

**Agent dispatch:** N/A — this is a coordination step. The plan in `thetaSwap-core-dev` is authored via its own brainstorming → writing-plans cycle under the evm-tdd skill chain (`evm-tdd:evm-tdd` → `evm-tdd:phases:01-specify`). The HANDOFF.md from Task 1.1 is the canonical input.

**Acceptance:**
- The cross-repo plan exists and cites HANDOFF.md's commit sha as its master spec.
- The cross-repo plan's first phase reads `IronCondor_strip.json` + `fx_paths_24_brackets.json` and asserts audit_block matches.
- The cross-repo plan's exit deliverables match master-spec §2.3 exit-deliverables list: forge test 24/24 PASS at 35% envelope tolerance.

This task is a coordination handoff; this repo's Wave-2 review verifies via `HANDOFF.md::thetaSwap_core_dev_commit_sha` that the cross-repo plan was authored.

**Commit message:** N/A — this is a cross-repo action; HANDOFF.md is updated with the cross-repo plan sha when known.

---

### Task 3.2 — Wait for cross-repo Wave-2 verdict; record outcome

**Files:**
- Modify: `scratch/2026-05-11-b1-foundry-handoff/HANDOFF.md` (append §"Cross-repo Wave-2 verdict")

**Agent dispatch:** N/A — orchestrator records the cross-repo verdict (PASS / FAIL).

**Acceptance:**
- HANDOFF.md §"Cross-repo Wave-2 verdict" lists: cross-repo commit sha, forge test outcome (24/24 PASS or N/24 FAIL), envelope max-rel-error per bracket if FAIL.
- If FAIL on ≥ 2 brackets, route per master-spec §2.3 HALT-trigger #2 to cohort_5_strip-level (geometry / strategy fix; route to A1).
- If PASS, B1 closes; both Wave-2 RC+MQ on THIS plan dispatch.

**Commit message:** `coord(stage-3-b1): record cross-repo Wave-2 verdict in HANDOFF.md`

---

## §8 Pin coverage (per master spec §5)

| Pin | This plan's coverage |
|-----|-----------------------|
| P-B1.1 (JSON schema + audit_block validation in Foundry) | Task 1.1 HANDOFF.md §2 enumerates the Foundry-side schema check requirements; Task 3.2 records the cross-repo verdict. |
| P-B1.2 (envelope assertion at 35% on the canonical metric) | Task 1.2 ENVELOPE_ASSERTION_PROOF.md pins the canonical metric form; cross-repo Foundry test must cite this proof; Task 3.2 records the per-bracket envelope verdicts. |

## §9 HALT routing

| Trigger | Route |
|---------|-------|
| Task 1.1 HANDOFF.md cites a non-canonical envelope formula (e.g., the v0.1-spec relative-error form) | HALT — RC Wave-1 catches this. |
| Task 2.1 FX-path generator fails its Hypothesis property test | HALT — Senior Developer iterates; do NOT relax. |
| Task 2.2 fx_paths_24_brackets.json round-trip fails or bracket count ≠ 24 | HALT — generator drift; route to cohort_2 spec §5.2 reconciliation. |
| Task 3.2 cross-repo forge test FAILS on ≥ 2 brackets at 35% tolerance | HALT — route to A1 (strategy / geometry fix, not a B1-level fix per master-spec §2.3 HALT-trigger #2). |
| Cross-repo Foundry deployment can NOT provision any leg of the 12-leg strip on forked Panoptic | HALT — route to A1 (Panoptic strategy is unsupported; strategy swap required). |
| Wave-1 or Wave-2 RC+MQ on this plan returns BLOCK | HALT per master-spec §6.1; CORRECTIONS-α landed in this plan's §11. |

## §10 Artifacts emitted

| Artifact | Phase | Schema | Lineage parent |
|----------|-------|--------|-----------------|
| `scratch/2026-05-11-b1-foundry-handoff/HANDOFF.md` | 1/3 | markdown + commit-sha pin fields | `IronCondor_strip.audit_block` |
| `scratch/2026-05-11-b1-foundry-handoff/ENVELOPE_ASSERTION_PROOF.md` | 1 | markdown | `cohort_5_strip/replication.py` lines |
| `scratch/2026-05-11-b1-foundry-handoff/FX_PATH_GENERATOR.md` | 2 | markdown | `fx_path_emit.py` |
| `simulations/saas_builder/cohort_5_strip/fx_path_emit.py` | 2 | code (Callable tier) | (additive, no parent) |
| `simulations/saas_builder/cohort_5_strip/fx_path_io.py` | 2 | code (IO Boundary tier) | (additive) |
| `simulations/saas_builder/data/fx_paths_24_brackets.json` | 2 | v1.0 (new) | sha over emitter inputs |
| Cross-repo: `thetaSwap-core-dev/test/integration/StripReplication.t.sol` | 3 (cross-repo) | Solidity / Foundry | HANDOFF.md sha |

## §11 CORRECTIONS-α (reserved)

v0.1 has no corrections. Wave-1 RC+MQ on this plan may land v0.2 → §11.1.

## §12 References

- `docs/specs/2026-05-11-stage-3-first-wave-design.md` v0.2 — master spec (§2.3 for this plan; §9.1 MQ-FLAG-1 disposition rationale; §8.1 cross-repo coordination acknowledgement).
- `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` §5.2 — 24-bracket parameter family (input to Task 2.x).
- `notes/PRIMITIVES.md` §6 eq. (6) — FX-path generator (Phase 2 mathematical anchor); eq. (7) — realized variance (Foundry-side anchor); §11 — discrete strip; §12 — tolerance ledger.
- `simulations/saas_builder/cohort_5_strip/replication.py:1-28` — canonical envelope-verifier docstring; the formula the Foundry test must implement.
- `simulations/saas_builder/cohort_5_strip/types.py:57-74` — `REPLICATION_REL_TOL = 0.35` rationale.
- `simulations/saas_builder/cohort_5_strip/__init__.py` — Pin S1–S8 framing that B1 verifies in-the-large.
- `memory/feedback_no_code_in_specs_or_plans.md` — plan-as-orchestration-only.
- `memory/feedback_specialized_agents_per_task.md` — foreground-orchestrates-never-authors.
- `evm-tdd:evm-tdd` skill — cross-repo Solidity / Foundry methodology anchor (consumed by `thetaSwap-core-dev`, NOT by this plan).

---

*End of B1 plan v0.1. Wave-1 RC+MQ review dispatch before any task execution.*
