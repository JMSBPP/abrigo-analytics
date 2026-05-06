---
name: Strict TDD enforcement — no untested code ever
description: NON-NEGOTIABLE — agents must never write implementation code for features whose tests haven't been written and verified to fail first
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**NON-NEGOTIABLE RULE FOR ALL CODING AGENTS:**

Do NOT write implementation code for any feature unless:
1. The test for that specific feature has been written FIRST
2. The test has been run and verified to FAIL
3. Only THEN write the minimal implementation to make that ONE test pass
4. If a test does not pass, do NOT move on to writing code for untested features

This is strict red-green TDD. One feature at a time. No batch implementations.

**Why:** User explicitly enforced this as non-negotiable. Writing untested code defeats the entire TDD approach and leads to bugs that are hard to trace.

**How to apply:** Every implementing agent (Data Engineer, Senior Backend Developer, or any other) must follow this cycle for EACH behavior:
1. Write the failing test
2. Run it — confirm it fails
3. Write minimal code to pass
4. Run it — confirm it passes
5. Only then move to the next behavior's test

NEVER write implementation code for B-P2 if B-P1's test hasn't passed yet. NEVER batch multiple features into one implementation step.
