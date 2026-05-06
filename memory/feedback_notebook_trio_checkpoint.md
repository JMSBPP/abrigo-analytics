---
name: Notebook X-trio checkpoint review (NON-NEGOTIABLE)
description: Analytics Reporter authoring any notebook must stop and await human review after every (why-markdown, code-cell, interpretation-markdown) trio — never bulk-author multiple trios without review
type: feedback
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
NON-NEGOTIABLE: when an Analytics Reporter (or any subagent) is authoring a Jupyter notebook that is part of a research/estimation deliverable, the cell output must be structured as a sequence of trios. Each trio is:

1. A markdown cell explaining WHY the next code cell runs (may be — and in the econ-notebook pipeline IS — the four-part citation block; the "Why used" part of the citation block satisfies the why-explanation minimum, and the citation block's other three parts are still required)
2. A code cell executing the analysis
3. A markdown cell interpreting the results the code cell just produced

After completing exactly one trio and verifying the code cell executes without error, the subagent HALTS and requests human review. It does not bulk-author multiple trios and does not advance to the next trio without explicit approval.

**Why:** The user requires granular oversight of notebook progress. Bulk authoring produces trios whose results the subagent hasn't reflected on, and whose interpretations may contradict later trios the reviewer will never see until all have been written. Trio-by-trio review preserves the reviewer's ability to redirect early before downstream cells compound on a wrong interpretation.

**How to apply:**
- Applies to every notebook-authoring task in plans like `2026-04-17-econ-notebook-implementation.md` (NB1, NB2, NB3) and any future estimation/research notebook.
- Does NOT replace the parent plan's task structure — a single task may contain many trios; the subagent simply pauses after each trio within that task rather than completing all trios in one dispatch.
- Does NOT replace the citation-block rule; it layers on top. The citation block is still required as the markdown-cell-before-code; what this rule adds is the mandatory STOP after the interpretation markdown.
- Does NOT apply to infrastructure tasks (scaffold creation, lint scripts, justfile recipes, env.py, references.bib) — only to notebook cells authored into `.ipynb` files.
- The parent task's overall TDD structure (write failing test → fail → implement → pass → commit) is preserved; the trio checkpoint happens *during* the implement step, interleaved with test-pass verification at trio boundaries when appropriate.
