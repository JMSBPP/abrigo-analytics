---
name: Notebook decision-citation block (NON-NEGOTIABLE)
description: Every decision, test, and spec choice in any estimation/sensitivity notebook must be preceded by a four-part citation block — no code runs without a reference-backed justification
type: feedback
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
NON-NEGOTIABLE: every test, cleaning decision, specification choice, or plot selection in a Jupyter notebook intended as a deliverable must be preceded by a markdown justification block with exactly four parts:

1. **Reference** — paper, URL, section/equation. The published precedent the choice rests on.
2. **Why used** — brief explanation of what the test/choice answers in the current pipeline.
3. **Relevance to our results** — how a pass/fail or a specific estimate changes the reported β̂, CI, or gate verdict.
4. **Connection to the simulator** — how the output feeds Layer 2 (RAN payoff / pool-parameter simulator). If it doesn't, say so explicitly.

**Why:** The user requires every design decision to be backed by a citation and an explicit chain to downstream artifacts. The notebook is a research deliverable; unreferenced choices invalidate the output. Unbacked tests also lose the audit trail needed for the Layer 2 simulator — disagreements between OLS and GARCH-X, regime-specific β̂s, and the T3b gate verdict all require reviewers to trace each choice back to its foundation.

**How to apply:** Applies to NB1 (cleaning decisions, plot conventions, stationarity tests), NB2 (OLS primary, GARCH-X, decomposition, Student-t alternative, subsample splits, bootstrap sleeve), NB3 (T1–T7, A1–A9, final gate). Format is a dedicated markdown cell above each code cell/decision anchor. A shared `references.bib` or inline URL citations both acceptable; cross-reference consistency matters more than format. Analytics Reporter must enforce this on every cell before commit; reviewers reject any unreferenced decision.
