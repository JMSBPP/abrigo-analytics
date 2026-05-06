---
name: Auto-mode default = proceed without asking
description: When user has authorized auto mode in a session, default to proceeding through plan/dispatch milestones without surfacing pause-or-continue questions; prefer action over interruption
type: feedback
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
When auto mode is active in a session AND the user has explicitly said "proceed without asking" (or equivalent), do NOT ask "want me to proceed?" / "pause for milestone review?" at natural milestone points. Just proceed.

**Why:** User stated 2026-04-25 during Task 11.O Rev-2 / Phase 5 dispatch: "yes, proceed on auto mode without asking from now on." Surfacing milestone-pause questions interrupts forward progress when the user has already pre-authorized continuation.

**How to apply:**
- Default = dispatch the next plan task / next agent / next review cycle
- Course-correct on user input mid-stream, not pre-emptive milestone gates
- Continue surfacing course-correction-relevant findings (BLOCKERs, anti-fishing triggers, HALT conditions, branch-tracking footguns) — these aren't "asking permission to proceed," they're surfacing decisions the user must make
- Do NOT skip risk surfacing (per auto-mode item 5: destructive/shared-system actions still need confirmation); just skip courtesy-pause asks
- This applies to the current session; carry forward to future sessions when auto mode is re-authorized
