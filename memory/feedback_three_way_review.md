---
name: Three-way review for all specs and plans
description: Every spec and plan must be reviewed by Code Reviewer + Reality Checker + Technical Writer agents before approval
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
All design specs and implementation plans must pass a **three-way external review** before proceeding to implementation:

1. **Code Reviewer** (`superpowers:code-reviewer`) — reviews against orchestration constraints, TDD completeness, functional-python compliance, and general spec quality. Produces PASS/FLAG/BLOCK verdicts.

2. **Reality Checker** (`Reality Checker`) — finds what will actually break. Verifies math, checks assumptions against real service limits, identifies missing failure modes, validates dependency installation paths. Defaults to "NEEDS WORK".

3. **Technical Writer** (`Technical Writer`) — reviews clarity for agent consumption, interface completeness, ambiguity between modules, terminology consistency, and whether agents can implement independently without asking clarifying questions.

**Why:** Single-reviewer specs miss blind spots. The code reviewer catches structural issues, the reality checker catches practical breakage, and the technical writer catches ambiguity that causes agents to produce incompatible code. Discovered during the RAN growth pipeline spec where all three found distinct issues.

**How to apply:** After writing any spec or plan, dispatch all three reviewers in parallel. Consolidate their findings, fix all BLOCK items, address FLAG items, then present the updated spec for user approval. Do NOT proceed to implementation until all three have reported and fixes are applied.
