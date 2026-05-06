---
name: Implementation review uses Code Reviewer + Reality Checker + Senior Backend Developer
description: 3-way implementation review replaces Technical Writer with Senior Backend Developer; Data Engineer implements and fixes
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**NON-NEGOTIABLE. For implementation reviews (code already written)**, the 3-way review panel is:

1. **Code Reviewer** (`superpowers:code-reviewer`) — spec compliance, TDD, functional-python
2. **Reality Checker** (`Reality Checker`) — runs tests, verifies math, finds what breaks
3. **Senior Developer** (`Senior Developer` / Backend Architect) — code quality, architecture, downstream integration

**NOT Technical Writer** — that role is for spec/plan reviews (writing problems), not implementation reviews (code problems). This is NON-NEGOTIABLE.

**Implementation agent:** Data Engineer writes ALL code and fixes ALL issues found by reviewers. This is NON-NEGOTIABLE.

**Why:** Technical Writer reviews clarity of documents for agent consumption. Once code is written, a Senior Backend Developer provides more relevant feedback on code structure, API design, and integration concerns.

**How to apply:**
- Spec/plan reviews: Code Reviewer + Reality Checker + Technical Writer (document quality)
- Implementation reviews: Code Reviewer + Reality Checker + Senior Developer (code quality)
- Fixes: Data Engineer implements corrections
