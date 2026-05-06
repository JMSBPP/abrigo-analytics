---
name: No code in specs or implementation plans
description: Specs and implementation plans must be completely code-agnostic -- no Solidity, no interfaces, no function signatures. Implementation is super progressive and supervised.
type: feedback
originSessionId: e63ee238-733d-49df-8015-addce58e2ae7
---
Specs (brainstorming output) AND implementation plans (writing-plans output) must both remain completely code-agnostic. No Solidity interfaces, no function signatures, no code snippets.

**Why:** The user's workflow is super-progressive -- code decisions and design decisions must not be made without supervision. Writing code in specs or plans pre-commits to implementation choices before the user has validated them step by step. The implementation phase is where code appears, and even then it must be incremental and supervised.

**How to apply:**
- In brainstorming/specs: describe components, relationships, properties, and constraints in natural language and diagrams only
- In writing-plans: describe tasks as "what to achieve" not "what code to write" -- e.g., "define the vault's share pricing mechanism" not "implement totalAssets() override"
- During implementation: proceed one small step at a time, getting user approval before each code decision
- Never present Solidity/code in architectural documents even as "examples" -- it anchors decisions prematurely
