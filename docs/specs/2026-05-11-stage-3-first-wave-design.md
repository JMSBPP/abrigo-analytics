---
spec_id: stage-3-first-wave-design
spec_version: v0.1 (initial draft — awaiting RC + MQ 2-way review)
emit_timestamp_utc: 2026-05-11
parent_framework: notes/PRIMITIVES.md (a_s / a_l / CPO primitives)
cohort_note: notes/SaaS_Builders_AI_NativeBuilders.md (cohort instantiation of §4.2)
stage_2_verdict: docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md (PASS; ideal-scenario clause invoked)
stage_2_results_anchor: notes/STAGE_2_RESULTS.md (R1–R8 closed-form identities)
strip_emit_anchor: simulations/saas_builder/cohort_5_strip/ (IronCondor_strip.json — schema v1.0)
authority: CLAUDE.md anti-fishing invariants (NON-NEGOTIABLE); brainstorming flow; feedback_pathological_halt_anti_fishing_checkpoint
predecessor: none (first Stage-3 spec)
status: DRAFT — awaiting §6.1 Wave-1 RC+MQ 2-way review (both reviewers per wave)
---

# Stage-3 first-wave readiness portfolio — master design spec

This spec defines the **master framing** for the first wave of Stage-3
readiness work following the SaaS-Builder Stage-2 PASS (verdict memo
`docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md`). It scopes
three independently-executable tracks (A1, A2, B1), establishes the
cross-track dependency graph, fixes the per-track exit criteria, and
pins the **two-way RC + MQ review protocol** that every track-level
plan must clear before execution.

The tracks themselves are written as three separate plans
(`docs/plans/2026-05-11-stage-3-{a1,a2,b1}-...md`) that consume this
master spec. Per CLAUDE.md anti-fishing discipline, none of the three
plans dispatches for execution before both RC and MQ verdicts on its
plan are ACCEPT / ACCEPT_WITH_FLAGS.

## §0 Scope statement

**In scope.** Three first-wave Stage-3 readiness tracks, all unblocked
TODAY by the Stage-2 PASS verdict and the cohort_5_strip emit
(commit `3442852`):

- **Track A1** — Panoptic strategy re-survey and IronCondor-alternative
  comparison. The Stage-2 strip used reverse-IC because it was the
  longest-leg Panoptic primitive at the Stage-2 horizon, NOT because it
  is the mathematically-optimal discretization of √σ_T. A1 produces a
  comparison memo + a selection verdict (KEEP / REPLACE) and, if
  REPLACE, a delta-spec for the cohort_5_strip strategy swap.

- **Track A2** — Real-data conditioning of cohort distributions
  (TODO-COHORT-1, deferred at Stage-2). DevSurvey-style sourcing on
  LATAM solo AI-builders produces empirical
  $(\bar C^{P10}, \bar C^{P50}, \bar C^{P90})$ that replace the
  synthetic Pareto-tier mix. C1 re-fits; Z_cap re-pins; cohort_5_strip
  re-emits against the refreshed K⋆.

- **Track B1** — Contract-side Foundry test scaffolding against a
  forked Panoptic deployment. Reads `IronCondor_strip.json`,
  provisions the 12-leg position, simulates FX-excursion paths per
  PRIMITIVES.md §6, asserts net LP P&L tracks K̂·σ_T within the strip
  replication envelope (PRIMITIVES.md §12 row 1). B1 lives in the
  `thetaSwap-core-dev` repo; analytics-side coordination is via the
  JSON artifact and this spec.

**Out of scope (deferred to a follow-up Stage-3 wave).** A3 (per-tier
θ_k differentiation), B2 (Streamia premium plumbing), C1 (stochastic-FX
variant), C2 (hierarchical pooling for C3). These items are deferred
to a second Stage-3 wave once A1/A2/B1 close.

**Anti-fishing scope guard.** This spec is a SCOPE-AND-GATE document.
It does NOT pre-pin scientific outcomes (e.g., "A2 will find Z_cap is
commercially material") and does NOT pre-pin engineering verdicts
(e.g., "A1 will keep IronCondor"). Such pre-pinning would be exactly
the post-hoc-fishing pattern that
`feedback_pathological_halt_anti_fishing_checkpoint` bans. The exit
criteria below are deliverable-existence checks, not outcome-direction
constraints.

## §1 Cross-track invariants

The following invariants apply to all three plans and are NON-NEGOTIABLE.

### §1.1 Anti-fishing carry-forward

Inherited verbatim from CLAUDE.md and the Stage-2 spec lock:

- $N_{\text{MIN}} = 75$, $\text{POWER}_{\text{MIN}} = 0.80$,
  $\text{MDES}_{\text{SD}} = 0.40$ SD-units of Y for any A2 empirical fit.
- Pre-pin sign expectations, lag structure, and primary specification
  BEFORE any data is touched.
- HALT + disposition memo + user-enumerated pivot + CORRECTIONS block +
  post-hoc 3-way review whenever spec contradicts data (per
  `feedback_pathological_halt_anti_fishing_checkpoint`).

### §1.2 Three-tier discipline (analytics-side tracks A1, A2)

Per the functional-python skill: any new module under
`simulations/` follows types (Value) / modules+callable (Callable) /
utils (IO Boundary) tiering. Sub-packages added under
`simulations/saas_builder/` mirror cohort_1/2/3/4/5_strip layout
exactly. No inheritance except Protocol + Exception + private Pydantic
BaseModel (utils/json_io) + TypedDict (utils/parquet_io).

### §1.3 Audit-block lineage

Any artifact emitted by A1 / A2 must extend the existing audit-block
chain:

- A2 outputs (refreshed `Z_cap_pinned.json` v1.2) must include a new
  `parent_audit_block` field referencing the Stage-2 v1.1 audit
  (`1fb1f7a4…5d31`).
- A1 outputs (`STRATEGY_COMPARISON.md` + optional delta-spec) must
  include a `consumed_strip_audit_block` field referencing the
  current `IronCondor_strip.audit_block` (`94150326…`).
- B1 forge tests must load the strip audit_block from the JSON header
  and surface it in test output for cross-repo traceability.

### §1.4 Decision-citation block (per spec/plan section)

Every claim that drives a decision (test choice, threshold, form pin)
carries a 4-part citation: **Reference** (file:line) · **Why**
(motivating constraint) · **Relevance** (downstream consumer) ·
**Connection** (closes which open item / FLAG / BLOCK). Per
`feedback_notebook_citation_block.md`.

## §2 Per-track exit criteria

Exit criterion = deliverable-existence + RC+MQ ACCEPT. No outcome-
direction pinning.

### §2.1 Track A1 — Panoptic strategy re-survey

**Plan path:** `docs/plans/2026-05-11-stage-3-a1-panoptic-restrategy.md`

**Phase shape:**
1. Discovery — current Panoptic primitive set (Streamia, multi-leg
   overlays, strangle, butterfly, condor, custom-leg combos);
   leg-count × payoff-shape × on-chain-liquidity comparison table.
2. Evaluation — for each candidate primitive, instantiate the
   strip-equivalent emitter (a parallel of `cohort_5_strip.StripBuilder`
   adapted to the candidate's leg topology) and run
   `CarrMadanEnvelopeVerifier` against the same log-contract proxy at
   the canonical TP1 fixture $(S_0=4000, \sigma_0=20000, K^\star=4687.94)$.
   Reuse of the shipped verifier ensures cross-candidate envelope
   comparability.
3. Verdict — KEEP_IRONCONDOR (no strategy change; close A1) OR
   REPLACE_WITH_X (emit `STRATEGY_DELTA_SPEC.md` describing the
   cohort_5_strip refactor required to support strategy X, with the
   types-tier addition + emit-tier schema bump).

**Exit deliverables:**
- `docs/plans/2026-05-11-stage-3-a1-panoptic-restrategy.md`
- `scratch/2026-05-11-a1-panoptic-survey/STRATEGY_COMPARISON.md`
- Verdict JSON: `simulations/saas_builder/data/strategy_verdict.json`
  (schema: `{verdict: "KEEP" | "REPLACE", primitive_id, rationale,
  envelope_at_tp1, audit_block, consumed_strip_audit_block}`)
- If REPLACE: `docs/specs/2026-05-{NN}-cohort-5-strip-delta-spec.md`

**HALT triggers:**
- No candidate primitive admits a deterministic strike-ladder + weight
  emit at the cohort_5_strip schema-v1.0 level → HALT, disposition
  memo, user-enumerated pivot to a richer schema or to a non-Panoptic
  venue.
- Pre-pinned envelope-comparison threshold for REPLACE: candidate X
  must beat the existing IronCondor by ≥ 5 percentage points on the
  TP1 envelope metric. Anything inside that margin → KEEP verdict.
  Pre-pinned BEFORE the comparison table is built (anti-fishing per
  §1.1).

### §2.2 Track A2 — Real-data cohort conditioning

**Plan path:** `docs/plans/2026-05-11-stage-3-a2-real-data-conditioning.md`

**Phase shape:**
1. Sourcing — DevSurvey-style instruments deployed across the channels
   listed in `SaaS_Builders_AI_NativeBuilders.md` §"Identification
   strategy" (Twitter/X, Discord, Platzi, GitHub Octoverse LATAM).
   Target $N \ge N_{\text{MIN}} = 75$ for the joint
   $(\bar C, \overline\Upsilon, \text{stickiness})$ instrument.
2. Distribution fit — produce empirical
   $(\bar C^{P10}, \bar C^{P50}, \bar C^{P90})$ for LATAM solo
   AI-builders; check survey-method bias against
   `feedback_pre_pinned_sign_protects_anti_fishing.md`.
3. Re-fit + re-pin — C1 cost posterior re-fits against the empirical
   prior; Z_cap re-pins to v1.2; cohort_5_strip re-emits.

**Exit deliverables:**
- `docs/plans/2026-05-11-stage-3-a2-real-data-conditioning.md`
- `scratch/2026-05-11-a2-devsurvey/SOURCING_PROTOCOL.md` (pre-pinned)
- `simulations/saas_builder/data/cohort_distribution_empirical.parquet`
  (raw + processed survey responses)
- `simulations/saas_builder/data/Z_cap_pinned.json` v1.2 (refreshed)
- Re-emit of `simulations/saas_builder/data/IronCondor_strip.json`
  against the new K⋆
- HALT-on-rank-flip verdict per Stage-2 spec §15.4 semantic:
  if the empirical prior triggers a Υ_t LOO ranking flip against
  det+churn, HALT → disposition memo → user pivot.

**HALT triggers:**
- Sample size shortfall ($N < 75$) — HALT, sourcing extension or
  scope re-pin.
- Rank flip vs Stage-2 det+churn pin (R7) — HALT per pre-existing
  spec safeguard.
- Empirical prior yields posterior $r̂ > 1.01$ or
  $\text{ESS}_{\text{bulk}} < 1{,}000$ — HALT, methodology review.

### §2.3 Track B1 — Foundry scaffolding against forked Panoptic

**Plan path:** `docs/plans/2026-05-11-stage-3-b1-foundry-scaffolding.md`

**Cross-repo note.** B1 lives in `thetaSwap-core-dev`. The
analytics-side plan in this repo pins (i) the input contract
(`IronCondor_strip.json` schema v1.0), (ii) the FX-excursion test
generator (PRIMITIVES.md §6 eq. 6), and (iii) the replication-envelope
target K̂·σ_T (PRIMITIVES.md eq. 17). The Solidity / Foundry
implementation is in the other repo; this spec does NOT
re-author it.

**Phase shape:**
1. Schema-binding — JSON reader in Foundry test harness; assert
   schema_version == "v1.0"; assert audit_block matches the
   analytics-side emit.
2. Position provisioning — for each of the 3 condors, route 4 legs
   onto the appropriate Panoptic primitive (current convention: 4
   long-strangle / short-strangle Panoptic positions per condor).
3. FX-path simulation — generate deterministic paths via
   PRIMITIVES.md §6 eq. (6) at the 24-bracket parameter family from
   Stage-2 spec §5.2; for each path compute realized σ_T and net LP
   P&L.
4. Envelope assertion — assert
   $|\Pi_{\text{realized}} - \hat K \cdot \sigma_T| / |\hat K \cdot \sigma_T| \le 0.35$
   (matching the cohort_5_strip 3-condor envelope tolerance from
   `simulations/saas_builder/cohort_5_strip/types.py::REPLICATION_REL_TOL`).

**Exit deliverables:**
- `docs/plans/2026-05-11-stage-3-b1-foundry-scaffolding.md` (this
  repo)
- In `thetaSwap-core-dev`: `test/integration/StripReplication.t.sol`
  + JSON-loader fixture + the 24 bracket-grid assertions.
- Forge test run verdict: 24/24 PASS at the 35% envelope tolerance.
- Cross-repo cross-reference: `thetaSwap-core-dev` commit sha pinned
  in `scratch/2026-05-11-b1-foundry-handoff/HANDOFF.md`.

**HALT triggers:**
- Any forked-Panoptic primitive does NOT support a leg of the
  cohort_5_strip schema (e.g., short-call at K_4 not provisionable
  under Panoptic's current pool mechanics) → HALT, route to A1
  (strategy-level fix, not a B1-level fix).
- Envelope assertion fails on ≥ 2/24 brackets at 35% tolerance →
  HALT, route to the cohort_5_strip strategy / geometry layer.

## §3 Cross-track dependency graph

```
                    ┌───────────────────┐
                    │ This spec         │
                    │ (master scope +   │
                    │  RC/MQ protocol)  │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │ A1 plan │     │ A2 plan │     │ B1 plan │
        │ ~1-2 d  │     │ ~weeks  │     │ ~3-5 d  │
        └────┬────┘     └────┬────┘     └────┬────┘
             │               │               │
        RC + MQ          RC + MQ          RC + MQ
        2-way review     2-way review     2-way review
             │               │               │
             ▼               ▼               ▼
       (strategy)      (Z_cap re-pin)   (forge tests)
              │              │              │
              └───────┐  ┌───┘              │
                      ▼  ▼                  │
              cohort_5_strip re-emit         │
                       │                    │
                       └──────────┬─────────┘
                                  ▼
                      Stage-3 first-wave close
```

**A1 ↔ B1 soft dependency.** B1 builds against the CURRENT
`IronCondor_strip.json` (audit `94150326…`). If A1's verdict is
REPLACE, B1 needs a follow-up swap (B1.1) to re-bind against the
post-A1 strategy. The schema-binding and test-harness scaffolding
remain reusable; only the position-provisioning leg-mapping changes.

**A2 → cohort_5_strip soft dependency.** A2's Z_cap re-pin triggers
a cohort_5_strip re-emit (the strikes shift as K⋆ shifts). This is a
re-run of the existing emit driver, not a strategy change.

**No hard ordering.** All three plans can dispatch in parallel
(subject to their own RC+MQ review individually).

## §4 Artifact ledger

| Artifact | Owner | Schema | Lineage parent |
|----------|-------|--------|----------------|
| `STRATEGY_COMPARISON.md` | A1 | scratch/markdown | `IronCondor_strip.audit_block` |
| `strategy_verdict.json` | A1 | new v1.0 | strip audit_block |
| `cohort_distribution_empirical.parquet` | A2 | extends cohort_prior.parquet schema | (none — first real-data emit) |
| `Z_cap_pinned.json` v1.2 | A2 | extends v1.1 with `parent_audit_block` field | Stage-2 v1.1 |
| `IronCondor_strip.json` re-emit | cohort_5_strip (via A2 trigger) | v1.0 (unchanged) | refreshed Z_cap v1.2 |
| `StripReplication.t.sol` | B1 (cross-repo) | Foundry | strip audit_block |
| `HANDOFF.md` | B1 | scratch/markdown | cross-repo sha pin |

## §5 Pin coverage

The pins listed here are gates the per-track plans must address.
Per-plan Pin tables refine them.

| Pin | Spec | Owner | Description |
|-----|------|-------|-------------|
| **P-A1.1** | this §2.1 phase 1 | A1 | comparison-table coverage — all Panoptic primitives admitting a deterministic strike+weight emit are listed; absence justified |
| **P-A1.2** | this §2.1 phase 2 | A1 | envelope evaluation reproducible (audit_block on `strategy_verdict.json`) |
| **P-A1.3** | this §2.1 phase 3 | A1 | KEEP/REPLACE verdict carries a citation to the comparison-table row that drives it |
| **P-A2.1** | this §2.2 phase 1 | A2 | sourcing protocol PRE-PINNED before any data touched (anti-fishing) |
| **P-A2.2** | this §2.2 phase 2 | A2 | sample $N \ge 75$ AT EXIT (NOT at pre-registration; pre-registration only commits to the floor) |
| **P-A2.3** | this §2.2 phase 3 | A2 | C1 diagnostic gates re-PASS at re-fit ($r̂ < 1.01$, ESS_bulk ≥ 1000) |
| **P-A2.4** | this §2.2 phase 3 + Stage-2 §15.4 | A2 | rank-flip safeguard armed |
| **P-B1.1** | this §2.3 phase 1 | B1 | JSON loader validates schema_version and audit_block (defense in depth against analytics-side drift) |
| **P-B1.2** | this §2.3 phase 4 | B1 | envelope assertion uses cohort_5_strip-pinned tolerance (35%), NOT a re-derived value (anti-fishing) |
| **P-X.1** | §6 | all | RC + MQ Wave-1 review on each plan ACCEPT / ACCEPT_WITH_FLAGS before execution |
| **P-X.2** | §6 | all | RC + MQ Wave-2 (post-execution verify) on each track's exit deliverables before the track closes |

## §6 Two-way review protocol (RC + MQ)

For each of the three plans (A1, A2, B1), the review protocol is:

### §6.1 Wave-1 — plan-time review (BLOCKING)

**Trigger:** plan author finishes drafting `docs/plans/2026-05-11-stage-3-{slug}.md`.

**Dispatch:** two Opus sub-agents in parallel, both consuming this
master spec + the candidate plan + the relevant `notes/`,
`docs/specs/`, and `simulations/saas_builder/` artifacts:

- **Agent 1 — `reality-checker` (RC)** — verifies the plan's claims are
  evidence-grounded and traceable to repo state. Default posture is
  NEEDS WORK per `feedback_pathological_halt_anti_fishing_checkpoint`.
- **Agent 2 — `math-quality` (MQ)** — verifies the plan's math
  derivations, identifications, and dimensional consistency against
  PRIMITIVES.md, STAGE_2_RESULTS.md, and the cohort_5_strip code.

Each agent emits one verdict file under
`scratch/2026-05-11-{track}-rc-mq-review/`:
- `rc-verdict.md` (RC verdict + ≤ 10 FLAGs, severity-graded)
- `mq-verdict.md` (MQ verdict + ≤ 10 FLAGs, severity-graded)

**Verdict alphabet** (mirrors Stage-2):

- `ACCEPT` — no FLAGs above NIT severity; plan ready to execute.
- `ACCEPT_WITH_FLAGS` — non-BLOCKING FLAGs disposed inline by plan
  author; execution proceeds.
- `BLOCK` — at least one BLOCK-severity finding; plan author HALTS,
  addresses BLOCK, re-dispatches BOTH reviewers (not just the one
  that BLOCKed — Delphi independence preservation).

**Independence safeguard.** RC and MQ agents are dispatched in the
SAME orchestrator message with no cross-agent prompt drift; each
agent sees the same context and writes its own verdict independently.
Plan author MUST NOT preview either verdict before both have landed
(prevents convergence bias).

### §6.2 Wave-2 — post-execution verify (BLOCKING)

**Trigger:** plan author claims plan-exit deliverables are emitted.

**Dispatch:** SAME pair (RC + MQ) re-dispatched, now consuming the
emitted artifacts (the JSON / parquet / markdown files listed in
§2's exit deliverables) AND the codebase changes the plan made.

**Verdict alphabet:** same as Wave-1.

**Track closure rule.** A track closes (its row in the milestone
status table flips to CLOSED) iff BOTH Wave-2 verdicts are
ACCEPT or ACCEPT_WITH_FLAGS. Any BLOCK reopens the plan.

### §6.3 Reviewer briefing context (pinned)

Both RC and MQ agents receive, in order:

1. This master spec (`docs/specs/2026-05-11-stage-3-first-wave-design.md`).
2. The candidate plan (`docs/plans/2026-05-11-stage-3-{slug}.md`).
3. Stage-2 verdict memo (`docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md`).
4. STAGE_2_RESULTS.md and PRIMITIVES.md (cited sections only — the
   reviewer briefs avoid the full file dumps to preserve context).
5. The relevant cohort_5_strip module file
   (`simulations/saas_builder/cohort_5_strip/__init__.py` + the
   track-specific tier file).

The briefing is identical for both agents to preserve Delphi
independence; the only difference is the reviewer-role
specification at the prompt head.

### §6.4 BLOCK-routing escalation

If RC and MQ Wave-1 verdicts converge on the SAME structural BLOCK
(e.g., both flag a master-spec-level scope error), the BLOCK escalates
to this master spec, not the plan. The master spec is patched
(CORRECTIONS-α block in §9), all three plans re-review against the
patched spec.

## §7 Sequencing and milestone close

**Default sequence:**

1. This master spec → §6.1 Wave-1 RC+MQ review.
2. Master spec ACCEPT → three plans drafted in parallel.
3. Each plan → §6.1 Wave-1 RC+MQ review (parallel across three tracks).
4. Plan ACCEPT → execution begins on that track. Tracks execute in
   parallel (A1 ~1-2 d, A2 ~weeks, B1 ~3-5 d).
5. Track exit deliverables emitted → §6.2 Wave-2 RC+MQ review.
6. All three Wave-2s ACCEPT → milestone close memo at
   `docs/specs/2026-{NN}-{NN}-stage-3-first-wave-close.md`.

**Anti-coupling guard.** Tracks do not block each other; a BLOCK in B1
does not stall A1/A2 reviewer turnaround. The only inter-track gate
is §6.4's master-spec-level BLOCK escalation.

## §8 Limitations and acknowledged scope

This spec discloses limitations honestly:

1. **Cross-repo coordination is light.** B1 lives in `thetaSwap-core-dev`;
   this spec pins the analytics-side contract (the JSON artifact) but
   does NOT specify the Foundry implementation. B1's plan in this repo
   is a coordination doc, not the canonical Solidity spec.

2. **A1's evaluation metric is single-fixture.** The envelope evaluation
   is computed at the canonical TP1 fixture only. A robustness pass
   across the 24-bracket parameter family is OUT OF SCOPE for A1 v1
   and explicitly deferred. If A1's verdict is KEEP, the deferred pass
   becomes redundant; if REPLACE, it becomes a Stage-3 second-wave
   item.

3. **A2's sample is convenience-sampled.** DevSurvey channels (Twitter,
   Discord, Platzi) are NOT representative random samples of LATAM solo
   AI-builders; they over-represent the visible-online subset. The
   sample-bias caveat is recorded in A2's exit deliverable
   `SOURCING_PROTOCOL.md` and is the headline limitation when Z_cap
   v1.2 magnitudes are reported.

4. **No outcome pre-pinning.** This spec deliberately does NOT pre-pin
   what A1 will conclude (KEEP vs REPLACE), what A2 will measure
   ($\bar C$ percentiles), or whether B1 will pass at the first
   attempt. Pre-pinning these would be the post-hoc-fishing pattern.
   Exit criteria are deliverable-existence + review-PASS, not outcome-
   direction.

## §9 CORRECTIONS-α (future patch block)

Reserved for in-place CORRECTIONS-α patches if RC/MQ Wave-1 review on
this master spec returns BLOCKs that require structural changes.
v0.1 has no corrections; v0.2 (if needed) lands here.

## §10 References

**Stage-2 anchor artifacts:**
- `docs/specs/2026-05-09-saas-builder-stage-2-verdict-memo.md` —
  Stage-2 PASS verdict, §9 Stage-3 readiness checklist (source list
  for A1, A2, A3, B1, B2).
- `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` —
  spec v1.2.1; §5.2 24-bracket parameter family consumed by B1.
- `notes/STAGE_2_RESULTS.md` — R1–R8 closed-form identities; §5
  Stage-3 open items (overlap with A1/A2/A3/B1/B2/C1/C2).
- `notes/PRIMITIVES.md` — §10 Carr-Madan, §11 discrete strip, §12
  tolerance ledger (consumed by A1 envelope metric and B1 forge
  assertion), §15 open items.
- `notes/SaaS_Builders_AI_NativeBuilders.md` — §"Identification
  strategy" (A2 sourcing channels).

**cohort_5_strip:**
- `simulations/saas_builder/cohort_5_strip/__init__.py` — strategy
  framing note + pin coverage S1–S8.
- `simulations/saas_builder/cohort_5_strip/types.py::REPLICATION_REL_TOL`
  — 35% envelope tolerance consumed by B1.
- `simulations/saas_builder/data/IronCondor_strip.json` — schema v1.0,
  audit_block `94150326…`, B1 input contract.

**Framework:**
- `CLAUDE.md` — operating framework, anti-fishing invariants,
  Stage-1/2/3 gating, ideal-scenario clause.
- `feedback_pathological_halt_anti_fishing_checkpoint.md` — HALT
  routing protocol.
- `feedback_post_hoc_fit_anti_fishing_pattern.md` — anti-fishing
  pattern catalogue (C4 1/κ case study).
- `feedback_notebook_citation_block.md` — 4-part decision-citation
  format.

**Skill anchors:**
- `superpowers:brainstorming` — brainstorming flow that produced this
  spec.
- `superpowers:writing-plans` — flow for the three per-track plans
  that consume this spec.
- `audit-econ` — RC + MQ Delphi-consensus pattern that drives §6.

---

*End of Stage-3 first-wave design spec v0.1. Independent RC + MQ
Wave-1 review dispatch by the orchestrator before plan drafting.*
