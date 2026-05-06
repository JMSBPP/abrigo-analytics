---
name: FX-vol-econ reviewer + silent-test-pass agent lessons
description: Agent-facing process lessons from Phase 2/3 three-way reviews — the five silent-test-pass patterns caught by Reality Checker, the three integration-test guards now installed, and a taxonomy of what each reviewer (Model QA / Reality Checker / Technical Writer) uniquely catches that the others miss.
type: project
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---

# Agent-facing lessons from FX-vol-econ 3-phase pipeline

This file captures process + methodology lessons for future agents orchestrating notebook pipelines or any multi-phase scientific-artifact project under strict TDD + three-way review discipline. Peer files hold substantive findings and strategic content; this file holds **HOW** lessons.

## Silent-test-pass pattern — 5 confirmed instances across Phase 2+3

**Definition:** a green pytest that does not actually exercise the behavior it claims to cover. Source of every instance: asymmetry between how the test constructs inputs and how production code receives inputs.

### Catalogue

1. **Task 22 E1 — `nb2_serialize.py` date coercion.** Tests constructed synthetic fit objects with already-serialized date strings. Production code received real datetime objects from fit runs; serialization path tripped on them. Caught by Reality Checker review of Task 22. Fix: add test that reads actual pickled fit from disk and round-trips through serialize.

2. **Task 25 cell 10 — NB3 `panel` variable undefined.** Tests parsed notebook cell source looking for expected tokens like `panel[`. Never actually executed the cell chain. `panel` had been loaded in an earlier cell's local scope; cell 10 referenced it without re-loading. Caught by Reality Checker review. Fix: add execution-path test that runs cell-chain subset.

3. **Task 27 follow-up — NB3 §1 never unpacked PKL into bare-name variables.** Cell loaded `nb2_params_full.pkl` into a dict but downstream cells referenced `results_cpi_ppi` etc. as bare names. Parser tests saw the names; executor would have failed. Caught by Reality Checker review. Fix: add unpacking-loop + sanity-assert cell.

4. **Task 24 `from scripts import cleaning` at NB1 cell 116.** Bootstrap cell at index 3 didn't add `contracts/` to sys.path, only `scripts/`. Parser tests passed (import statement present); execution would have ImportError. Caught by Reality Checker review. Fix: add `contracts/` to sys.path in bootstrap.

5. **Task 31 R2 — `test_nb3_section10_gate.py`.** Test synthesized a gate_verdict dict and asserted structure. Never executed live cell 31 that actually writes `gate_verdict.json`. Caught by Reality Checker review at Task 31 remediation. Fix: R2 integration test executes cell 31 directly and asserts on emitted JSON.

### Common failure mode

In every case, the test constructed its inputs in a way that **coincidentally satisfied the schema** but did NOT exercise the transition point where production would fail. The test author wrote assertions that felt thorough because they matched what they expected the cell to emit; they did not trace back to whether the cell would emit anything at all under realistic execution.

### Guard now installed (THREE INTEGRATION TESTS)

Post Task 31:
- `contracts/scripts/tests/test_nb1_end_to_end_execution.py`
- `contracts/scripts/tests/test_nb2_end_to_end_execution.py`
- `contracts/scripts/tests/test_nb3_end_to_end_execution.py`

Each runs `jupyter nbconvert --execute` on its notebook and fails on any runtime error. Slow tests (30-60s each) but non-optional. These are the backstop: a cell chain that can't execute end-to-end will fail CI regardless of what any upstream parser-test asserts.

### Rule for future notebook work

**Always include at least one end-to-end execution test per notebook.** Source-parser tests are allowed but not sufficient. If you can't write an execution test because the cell takes too long to fit, split the cell and test the pure-function core separately (or mark the execution test `slow` and run it on a nightly CI tier).

## Three-way review: what each reviewer uniquely catches

The 3-phase pipeline ran 12 three-way reviews (spec + plan + implementation). The distribution of findings is not uniform — each reviewer has a distinct signal.

### Model QA reviewer

**Signal:** econometric label-vs-implementation drift; identification validity; boundary-case inference.

Representative catches:
- T1 labeled "Mincer-Zarnowitz" but implementation matches Bomfim-Evans-Goncalves (BEG) — different identification assumptions → label must match implementation for reader to evaluate the test
- NB3 §6 labeled "Bai-Perron" but implementation uses `ruptures.Binseg` with RBF kernel — not the same algorithm → label drift
- Regressor spec changes made in green commit without disclosure in row labels (A1/A5 particularly)
- GARCH-X δ̂=0 on boundary: needs Self 1987 boundary-corrected LR, not naïve LRT — caught the correction before green.
- HAC(4) vs HAC(12) bandwidth sensitivity — which to trust when they disagree → bootstrap-HAC agreement check resolves.

**When to dispatch:** any spec or implementation that includes econometric estimators, identification claims, or inference procedures. NOT just for "econ code" — any test with a statistical claim.

### Reality Checker reviewer

**Signal:** spec-commitment violations; silent-test-pass patterns; prose-vs-code drift; structural defects.

Representative catches:
- Task 31 R1: A1 monthly-cadence sensitivity was NOT Decision #1 compliant (used full daily sample rather than 2008+); Reality Checker compared implementation to spec pre-commitments and flagged.
- All 5 silent-test-pass instances above.
- Prose claims results that code does not emit (schema drift in Task 31 README vs `gate_verdict.json`).
- Citation integrity: `Andrews 1999` cited in prose but not in `references.bib`.
- Anti-fishing discipline enforcement: Task 28 §9 spotlight would have tabled A1/A4 significant rows as "material movers"; Reality Checker flagged as anti-fishing violation, §9 HALTED.

**When to dispatch:** ALWAYS as one of the three reviewers on any gated artifact. Reality Checker is load-bearing — it catches the "what the author hoped would be true but isn't" class of error. NO exceptions for implementation reviews; see `feedback_implementation_review_agents.md`.

### Technical Writer reviewer

**Signal:** reader-journey information propagation; honest-caveat visibility; export readiness.

Representative catches:
- Task 30 README auto-render: anti-fishing paragraph present in notebook but not propagated to rendered README → reader lands on README first, gets misleading impression → C2 anti-fishing paragraph inserted (Task 31 `c01ef24c6`)
- PDF export readiness: figure captions, equation rendering, table breakpoints (Task 23 E3-E10 batch)
- Documentation honest-caveat visibility: FAIL verdict must be in first paragraph of README, not buried in §10
- Forest plot secondary rendering drift (cell 25 in-notebook vs cell 33 PNG emit): reader sees inconsistency between notebook and standalone figure → deferred to Task 33 with shared helper refactor

**When to dispatch:** spec reviews (reader onboarding; plan readability); post-README-render steps; PDF exports; anything that produces a reader-facing artifact outside the code itself.

**When NOT to dispatch:** implementation-only reviews where no reader-facing artifact changes. Per `feedback_implementation_review_agents.md`, implementation reviews use Code Reviewer + Reality Checker + Senior Developer, NOT Tech Writer.

## Orchestration anti-patterns observed (avoid)

1. **Dispatching parallel reviewers on overlapping files.** Violates `feedback_no_parallel_agents_same_dir.md`. Always sequence reviewers on the same artifact; parallel only if they touch disjoint artifacts (e.g., spec vs code).

2. **Letting the foreground author patches.** Violates `feedback_specialized_agents_per_task.md`. Foreground orchestrates and verifies; every substantive edit dispatches a specialized subagent (Analytics Reporter, Data Engineer, etc.).

3. **Treating review feedback as optional.** Even CONDITIONAL-PASS from 2 of 3 reviewers triggers remediation cycles. Task 15 ran 4 remediation cycles (A+B+C+D) across 10 commits before achieving full pass.

4. **Skipping TDD "because the change is small."** All Tasks 16-31 followed red → green; even one-line fixes. This is non-negotiable (`feedback_strict_tdd.md`).

## Decision-rule summary for future orchestrators

| situation | dispatch |
|---|---|
| new spec or plan | Code Reviewer + Reality Checker + Technical Writer |
| new implementation | Code Reviewer + Reality Checker + Senior Developer |
| implementation includes econometric estimators or inference | add Model QA (so 4 reviewers) |
| implementation includes reader-facing output (README, figure, PDF) | add Technical Writer to implementation review |
| notebook cell authoring | Analytics Reporter; strict TDD; HALT between trios |
| data pipeline or query API | Data Engineer; strict TDD |
| any gated artifact | always include Reality Checker |

## Persistence note

The three integration tests are the most important guardrail produced by Phase 2+3. If future notebook work ever fails one of them, **DO NOT mute or skip the test.** The silent-test-pass pattern reappears within one dispatch cycle if the guard is removed.
