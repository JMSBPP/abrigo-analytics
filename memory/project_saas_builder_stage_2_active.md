---
name: SaaS-builder Stage-2 — REVERIFY-PASSED, sub-task dispatch paused
description: 2026-05-07 cohort instantiation of PRIMITIVES.md §4.2 for solo AI-native LATAM builders; spec v1.1.1 LOCKED + Wave-1+2 reverify ACCEPT_WITH_FLAGS PROCEED; sub-task plans paused on functional-python skill stabilization; iter/saas-builder-stage-2 branch + draft PR wvs-finance/abrigo-analytics#3
type: project
---

**Iteration ID.** `saas_builder_stage_2`
**Status.** Pre-reg LOCKED (v1.1.1 REVERIFY-PASSED). Sub-task dispatch authorized but PAUSED on functional-python skill stabilization (per user 2026-05-07).
**Kickoff.** 2026-05-07.

## Branch + PR
- Branch: `iter/saas-builder-stage-2` (origin: JMSBPP/abrigo-analytics)
- Draft PR: https://github.com/wvs-finance/abrigo-analytics/pull/3 (closes when modeling deliverable lands)
- HEAD as of 2026-05-07 evening: `bb84026` (v1.1.1 + reverify verdicts committed)

## (Y, M, X)
- **Population:** Colombian solo AI-native SaaS builders (post-revenue, pre-scale; COP MRR + USD AI tooling cost; cross-border-USD-revenue OUT of cohort scope).
- **Y (per-user):** $a_s^{(T)} = \sum \Upsilon_t - \sum q_t/(X/Y)_t$ per PRIMITIVES (5'); rolling 12-month horizon.
- **X:** COP/USD spot, realized variance $\sigma_T$ over monthly rolling window. Primary FX path: PRIMITIVES (6) deterministic perturbation; sensitivity arms = GBM, OU, jump-diffusion, empirical-calibrated, bank-spread overlay.
- **M:** Panoptic CPO with $\sqrt{\sigma_T}$ payoff (PRIMITIVES (13)), 12-leg IronCondor strip (PRIMITIVES §11), streamed premium $\pi(t)$.
- **Workflow class W:** terminal-based agentic AI coding services (Claude Code as canonical exemplar; Aider, Cursor agent mode, Codex CLI, Gemini CLI, Cline, Continue, Open Interpreter, Devin in class).

## Methodology evolution
- **Kickoff (2026-05-07 AM):** A (CRRA welfare heatmap) + B (utility-indifference $\pi(t)$ + ratchet hitting time), additive on PRIMITIVES.md. **Superseded by post-research design.**
- **Current (2026-05-07 PM):** Cohort instantiation of PRIMITIVES.md §4.2 with workflow-derived cost dynamics:
  - **(T1) token-consumption process:** $\tau_t = \sum_j \sum_i \tau_{j,i}$, $N_j \sim$ NegBin($r,p$), $\tau_{j,i} \sim$ TruncPareto($\alpha, x_m, \kappa$) with $\alpha \in [1.5, 2.5]$ bracket.
  - **(T2) two-regime pricing (softplus-regularized):** $q_t^{\text{USD}} = \bar p_{\text{sub}} + p_t \cdot \text{softplus}_\beta(\tau_t - \kappa)$.
  - **Tier-prior:** Categorical($\pi_{\text{Pro}} = 0.20, \pi_{\text{Max-5x}} = 0.50, \pi_{\text{Max-20x}} = 0.30$) per builder, Dirichlet $\alpha_0 = 10$.
  - **Blended $p_t$:** input/output weighted (0.539/0.461) × cache discount (95% hit) × model mix (Sonnet 0.70 / Opus 0.20 / Haiku 0.10).

## Spec history
- **v1.0** (2026-05-07): pre-reg lock with §5.2 brackets landed post-research. **REJECTED** by both 2-wave verify agents.
  - Wave-1 RC: 3 BLOCKs + 5 FLAGs (dev-AI Stage-1 FAIL silently ignored; N_MIN/POWER/MDES mis-imported into synthetic-Bayesian regime; bank-spread overlay vs §3 FX-path lock).
  - Wave-2 MQ: 7 BLOCKs + 6 FLAGs (Pareto unbounded mean; LogNormal $N_j$ mis-spec; $x_m(i)$ unpinned; (T2) ReLU kink; primary-tier vs tier-mix inconsistency; AICc on PyMC; stationary-bootstrap mis-applied).
  - **Total: 10 BLOCKs + 11 FLAGs.** Cleared CORRECTIONS-η sibling 8-BLOCK precedent.
- **v1.1** (2026-05-07): CORRECTIONS-α addresses all 10 BLOCKs. Option α with γ-flavored brackets per disposition memo.
- **v1.1.1** (2026-05-07): §8(6) Pareto-α floor rationale fix per Wave-2 MQ reverify FLAG-G (truncation bounds moments for any α > 0; floor binds for tail-shape plausibility + $(\alpha, x_m, \kappa)$ joint identifiability, not moment existence).
- **Reverify status:** Wave-1 RC ACCEPT_WITH_FLAGS PROCEED + Wave-2 MQ ACCEPT_WITH_FLAGS PROCEED. **6 residual non-blocking flags.**

## Reverify residual flags (non-blocking, addressable in v1.2 or sub-task plan-time)
- RC F1: Section M β=+0.455 cited via memory file; needs primary-source line cite.
- RC F2: Blended $p_t$ in §5.1 lacks explicit $/MTok unit annotation.
- MQ F-H: Dirichlet $\alpha_0 = 10$ called "mild" — actually moderately informative (ESS = 10).
- MQ F-I: PSIS-LOO-CV PASS threshold pinned at 4·SE (stricter than canonical Vehtari 2017 2·SE).
- MQ F-J: TruncPareto $(\alpha, x_m, \kappa)$ joint identifiability — partial mitigation via §8(7) CI-width gate; recommend posterior-correlation diagnostic in TODO-COHORT-1.
- MQ F-G: Pareto-α floor rationale stale → **FIXED in v1.1.1.**

## Sub-task pipeline (TODO-COHORT-1..4)
**Status: AUTHORIZED but PAUSED on functional-python skill stabilization.**

- **TODO-COHORT-1:** Posterior over (T1) parameters $(r, p, \alpha, x_m, \pi, h_{\text{cache}})$ + tier mix; $\$/$mo CDF at p10/p50/p90/p99.
- **TODO-COHORT-2:** (T2) softplus fit + sign certification of $\Delta^{(a_s)} < 0$ at all §5.2 bracket points.
- **TODO-COHORT-3:** $\Upsilon_t$ form selection via PSIS-LOO-CV (martingale vs AR(1)-log-MRR vs det+churn); thresholds Δelpd > 4·SE PASS / < 2·SE INDISTINGUISHABLE.
- **TODO-COHORT-4:** $\pi(t)$ derivation + Z cap pin; certification at 5 test points straddling cap-kink at $\kappa \pm 0.5\kappa$; emit `Z_cap_pinned.json`.

**Dependencies:** C1 + C3 parallel; C2 ⟵ C1; C4 ⟵ C2 ∧ C3.

**Pause rationale:** sub-task plans must specify functional-python skill incorporation pattern (Value / Callable / IO three-tier + lint gate). Skill is mid-fix per user 2026-05-07; do not commit incorporation pattern until skill stabilizes.

## Critical local paths

| Artifact | Path |
|---|---|
| Math primitives anchor | `notes/PRIMITIVES.md` |
| Cohort instantiation note | `notes/SaaS_Builders_AI_NativeBuilders.md` |
| Pre-reg lock spec (current) | `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (v1.1.1) |
| Cost-process research | `scratch/2026-05-07-claude-code-cost-research/RESEARCH.md` (22 refs incl. arxiv 2604.22750, 2603.24582, 2601.14470) |
| Wave-1 RC verdicts | `scratch/2026-05-07-prereg-review/wave1_reality_checker.md` (v1.0) + `wave1_reality_checker_v1.1_reverify.md` |
| Wave-2 MQ verdicts | `scratch/2026-05-07-prereg-review/wave2_model_qa.md` (v1.0) + `wave2_model_qa_v1.1_reverify.md` |
| Disposition memo | `scratch/2026-05-07-prereg-review/disposition_memo.md` (α/β/γ/δ pivots; user picked α with γ-brackets) |
| Planning (bespoke names) | `.planning/` |

## Cross-iteration relationships
- **Pair D Stage-2 PASS** (2026-04-28; β=+0.137 on broad services Section G-T; `memory/project_pair_d_phase2_pass.md`): independent population; Pair D's CPO math (Carr-Madan, IronCondor, $K_l = K_s$) is REUSED here, only cohort-specific $\Delta^{(a_s)}$ is NEW.
- **dev-AI Stage-1 FAIL** (2026-05-06; β=−0.146 sign-flip on Section J narrow ICT; `memory/project_dev_ai_section_j_fail.md`): reconciled in spec §0.1 via (i) population mismatch (Section J narrow ICT ≠ SaaS-builder cohort), (ii) Section M counter-evidence (β=+0.455, p=1.13e-06), (iii) CLAUDE.md ideal-scenario clause invocation. HALT trigger if Stage-2 synthetic regime returns $\Delta^{(a_s)} \ge 0$.
- **PRIMITIVES.md inheritance:** CPO math (sign requirements §2; vault instantiations §3–§4; FX generator §5; variance inversion §6; $\Delta$ closed forms §7; CPO derivation §8; Carr-Madan §10; IronCondor strip §11) inherited wholesale; cohort-specific work is the (T1)+(T2) workflow cost model + per-user calibration only.

## Tooling commitment (Option 1 from earlier brainstorm)
Python 3.13 + uv + sympy + numpy + scipy + pandas + PyMC. functional-python skill (frozen-dataclass three-tier; no inheritance; comprehensions; full typing) for any code-touching work — **but skill incorporation into sub-task plans is paused per user 2026-05-07.** Re-read SKILL.md from disk when pause lifts (skill is being modified by user).

No Lean / Aristotle / Mathematica / Julia. Slice-B sign + equilibrium claims accept numerical certification (Path A v0 tolerances). Formal-proof hardening is Phase-2 only if a referee challenges.

## Anti-fishing posture
Pre-reg locks 10 Stage-2-applicable invariants (§8): sign pre-pin, convexity expectation, bracket immutability, tier-cap immutability, candidate-set closure, Pareto-α floor at 1.5, posterior CI-width threshold, sim-count floor (≥4000 draws across ≥4 chains), prior-sensitivity sweep, HALT cascade discipline.

CLAUDE.md $N_{\text{MIN}}=75 / $POWER_MIN$=0.80 / $MDES_SD$=0.40$ thresholds bind **Stage-3 cohort survey only** (Option γ), **not** Stage-2 synthetic-Bayesian regime (per RC-BLOCK-2 fix).

Pre-pins also live at `.planning/04-anti-fishing-prepins.md`.

## Open threads (post-reverify state)
1. **v1.2 residual-flag patch** — addresses 6 non-blocking flags (RC F1, F2; MQ F-H, F-I, F-J). Free-to-move.
2. **Z-cap derivation memo** — TODO-COHORT-4 prerequisite; symbolic derivation of $Z$ from (T1)+(T2)+$\pi(t)$. Free-to-move; sympy-skill-based.
3. **Stage-1-FAIL reconciliation hardening** — promote §0.1 to dedicated memo for external-scrutiny defensibility. Free-to-move.
4. **Functional-python skill stabilization** — user-side; sub-task plans gated.
5. **TODO-COHORT-1..4 sub-task plans** — gated on (4); lock-in pattern is Option I + (c) per earlier brainstorm (type-catalog header per plan + shared `_common/` primitives module).

## How to apply (cold-start checklist)
1. Read `notes/PRIMITIVES.md` §4.2 for the per-user $a_s$ framework + cohort-specific reinterpretation.
2. Read `notes/SaaS_Builders_AI_NativeBuilders.md` for the cohort instantiation + 4 labeled cohort-calibration TODOs.
3. Read `docs/specs/2026-05-07-saas-builder-stage-2-prereg-lock.md` (v1.1.1) for the locked pre-reg.
4. Read `scratch/2026-05-07-claude-code-cost-research/RESEARCH.md` for empirical brackets backing.
5. Check `scratch/2026-05-07-prereg-review/` for both reverify verdicts before proposing changes — those audits set the ceiling.
6. Re-read `~/.claude/skills/functional-python/SKILL.md` from disk (user-modified) before any code-touching task.
