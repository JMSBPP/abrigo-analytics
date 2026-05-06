---
name: Agent scope must match exactly what user specifies
description: When dispatching sub-agents to fix specific files, NEVER include files the user didn't explicitly mention — even if related
type: feedback
originSessionId: 6d731f8a-e8a0-47d1-8267-b6a4ff88dd79
---
When the user says "fix issues in file A and file B", the agent must ONLY modify file A and file B. Do NOT include other files (like adapters, tests, or consumers) even if they are logically related or would benefit from changes.

**Why:** The user often has their own in-progress edits on related files. An agent modifying those files overwrites or conflicts with the user's manual work. The user explicitly called this out as "intruding on non-mentioned code."

**How to apply:** When writing agent prompts, add an explicit constraint like "ONLY modify [file list]. Do NOT modify any other files." and repeat the constraint at the end of the prompt.
