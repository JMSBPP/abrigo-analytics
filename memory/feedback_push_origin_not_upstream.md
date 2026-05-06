---
name: Push to origin (JMSBPP), never upstream
description: Git push must target origin (JMSBPP's fork), never upstream (wvs-finance) — protects upstream repo from accidental writes
type: feedback
originSessionId: 7b0cb94b-a263-4b06-8904-1f09af81cfd5
---
Always push to `origin` (JMSBPP's repo), NEVER to `upstream` (wvs-finance).

**Why:** The wvs-finance repo is the upstream source. JMSBPP's fork is where all development happens. Pushing to upstream would write directly to the shared/org repo without a PR.

**How to apply:** Before any `git push`, verify the remote is `origin`. If a command defaults to `upstream`, explicitly specify `origin`. Never use `git push upstream`.
