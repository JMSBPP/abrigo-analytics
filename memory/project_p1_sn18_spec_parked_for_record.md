---
name: P1 SN18 spec finalized + sha256-pinned + PARKED 2026-04-27
description: Slow-lane P1 (Bittensor SN18 Cortex.t alpha event study for proprietary-AI policy hedge feasibility) reached spec-pin with sha256 = f855e036d3c7807e2bef414a91a806caec1279a9d83575020bc2b3e82b47aeab after v1→v2→v3 + 6 verifier dispatches; PARKED per user directive to refocus on fast-lane simple-β. Re-activatable as future iteration.
type: project
originSessionId: d1cfac41-85eb-4cae-ae40-bddd97fffc23
---
**Slow-lane P1 final pin state, 2026-04-27 evening.**

User directive after extensive slow-lane spec work: park P1 and refocus to fast-lane simple-β exercise. Stage goal restated: identify one *empirically-validated* microeconomic risk + simple positive-β confirmation → start protocol design. Behavioral equations + classic models come later. The slow-lane apparatus (3 spec revisions, 9-cell verdict cube, asymmetric placebo gate, robustness denominator decrement paths, multi-wave anti-fishing) was overkill for the stage goal.

**Artifacts pinned for the record (re-activatable later):**
- Plan: `contracts/docs/superpowers/plans/2026-04-27-p1-sn18-event-study-implementation.md`
- Spec: `contracts/docs/superpowers/specs/2026-04-27-p1-sn18-event-study-design.md`
- Spec sha256 = `f855e036d3c7807e2bef414a91a806caec1279a9d83575020bc2b3e82b47aeab` (computed against the file with `decision_hash` field set to the sentinel `<to-be-pinned-after-Task-0.3-v3>`; re-verify by replacing pinned hash with sentinel and recomputing)
- Spec passed v1 (initial) → v2 (15 verifier defects integrated) → v3 (3 v2-blocking + 3 polish integrated); both v3 verifier waves PASS

**Verifier dispatch chain (audit trail):**
- v1 plan: RC `ad0b3d8d2134f0002` + SPM `ad19cc84a99ce8018` (both PASS-WITH-REV)
- v1 spec: RC `a15cb71a71b9c6916` + MQS-fresh `af151c3c08f50dfe9` (both PASS-WITH-REV)
- v2 spec: RC `a9256cd1499ae8191` + MQS-fresh `aa6405d81fc4e32bd` (RC: 5 polish; MQS: 3 BLOCKING)
- v3 spec: RC `a041d533671a5cd01` + MQS-fresh `a81e11712d3b9bbf6` (both PASS, clean)
- Implementer (v1): MQS `ae87002267a35b77d` (DONE_WITH_CONCERNS — length overrun + 2 soft spots later closed)
- Implementer (v2): MQS-fresh `af6b572bd5f96407e` (DONE)

**Substantive content preserved by the pin (worth re-reading if P1 reactivates):**
- N_MIN_EVENTS = 8; α_primary = 0.0167 (Bonferroni 0.05/3 conjunctive family P1+P2+P3); α_robustness = 0.05; two-sided test
- 9-cell verdict tree (verdict-eligibility × robustness-consistency) + SUBSTRATE_TOO_YOUNG 4th outcome + asymmetric R-F1 placebo gate (PASS→INDETERMINATE on placebo rejection; FAIL retained with annotation; INDETERMINATE retained with annotation)
- Three exhaustive N_robustness decrement paths (R-H1 halving underpower; R-T1 Taoflow underpower; R-J1 cross-provider degenerate); admissible runtime values N_robustness ∈ {10, 11, 12, 13}
- Estimation-window leakage extend-backward rule with 60-day cap + cascade-to-N_MIN_EVENTS (no partial credit — 25-day floor binding)
- §8.2(b.i) joint qualifier: §8.2(b) "FAIL strengthened" framing requires explicit memo qualifier when R-H1 or R-T1 decremented
- Maymin (2026, arXiv:2603.29751) verified via mcp__arxiv__get_abstract; methodology baseline with explicit divergences
- Bittensor halving date corrected to **Dec 15 2025** (RC verified — bridge research said Dec 14 in error)
- Cortex.t URL corrected to `https://cortex-t.ai/docs` (RC verified — bridge research GitHub URL stale 404)
- dTAO mainnet activation date 2025-02-13 marked **provisional** with Phase-2 verification protocol
- Power profile pinned (mandatory in Phase-4 memo): at α_primary=0.0167, N=8, df=7, two-sided — power 0.80 vs d=1.4 very large; 0.40 vs d=0.8 large; 0.13 vs d=0.5 medium

**Re-activation conditions:** if fast-lane simple-β succeeds and AI-cost X is added as a second instrument family. The substrate (SN18 Cortex.t/Corcel) and signal-research findings (broad-basket basis-risk dominance; substitution-vs-complement directional asymmetry; Olas Mech + x402 emerging payment-receipt primitives) remain valid context.

**Why parked, not killed:** the spec work (3 revisions, 6 verifier dispatches) is non-trivial intellectual capital that should not be discarded. The directional verdict from the slow-lane signal research (proprietary-AI cost is hedgeable in principle but signal infrastructure is nascent) is also preserved. Killing would require re-authoring this scaffolding from scratch on re-activation; parking preserves it.
