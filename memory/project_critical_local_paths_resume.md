---
name: Critical local paths for Rev-5.3.1 resume
description: Plan, design docs, DuckDB, branch, and HEAD anchors required to reload Rev-5.3.1 context after compaction
type: reference
originSessionId: phase0-vb-mvp / 2026-04-25 session close
---

**Fact**: A future agent resuming the Phase-1.5.5 / Rev-5.3.1 thread requires these load-bearing local paths and git anchors:

- **Plan (source-of-truth)**: `contracts/docs/superpowers/plans/2026-04-20-remittance-surprise-implementation.md`
- **X_d design doc (immutable)**: `contracts/docs/superpowers/specs/2026-04-24-carbon-basket-xd-design.md`
- **Y₃ design doc (immutable)**: `contracts/docs/superpowers/specs/2026-04-24-y3-inequality-differential-design.md`
- **DuckDB**: `contracts/data/structural_econ.duckdb` (~42MB; includes `onchain_xd_weekly` + `onchain_y3_weekly` after Task 11.N.2d lands)
- **Branch**: `phase0-vb-mvp` (NOT main)
- **Worktree**: `/home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom`
- **HEAD at session close**: `7afcd2ad6` (Rev-5.3.1 N_MIN relaxation)
- **Predecessor commits worth knowing**:
  - `13cfe5f56` — Rev-5.3 pathological-HALT verdict (precedes Rev-5.3.1)
  - `2855240ae` — Task 11.N.2b.2 Carbon ingestion (8 weekly proxy_kind series)
  - `9f0997ed5` — Task 11.N.1b COPM raw-transfers backfill (110k rows)
  - `b576e7a1a` — Task 11.N.2b.1 basket pre-commitment
  - `17fa79d82` — Rev-5.3 plan fold (large TW edit recovery)
  - `23560d31b` — X_d + Y₃ design docs immutable freeze

**Why**: this is the minimum set a post-compaction agent needs to recover full operational context. Specs and design docs are immutable post-`23560d31b`; the plan is the only mutable methodology document and tracks revision history in CORRECTIONS blocks. The DuckDB file is the load-bearing data artefact and is reproducible via the pipeline scripts but expensive to rebuild — preserve in worktree.

**How to apply**:
1. First action on resume: `git status && git log --oneline -10` from the worktree.
2. Verify HEAD via `git rev-parse HEAD` matches `7afcd2ad6` or a descendant.
3. Activate venv: `source contracts/.venv/bin/activate` (per `feedback_venv_activation.md`).
4. Smoke-check DuckDB: `python -c "from scripts.econ_query_api import load_onchain_xd_weekly; print(len(load_onchain_xd_weekly()))"` from `contracts/`.
5. Read in order: this file → `project_phase15_5_task_chain_post_rev531.md` → `project_duckdb_xd_weekly_state_post_rev531.md` → in-flight task brief in plan.
6. The Y₃ panel may or may not be in DuckDB depending on Task 11.N.2d completion at compaction time; check `onchain_y3_weekly` table existence before assuming.

## Related memory

- `project_phase15_5_task_chain_post_rev531.md` — task chain status this resume anchors
- `project_duckdb_xd_weekly_state_post_rev531.md` — DuckDB content state
- `project_y3_inequality_differential_design.md` — Y₃ design context
- `project_rev51_resume_state.md` — historical predecessor resume anchor (Rev-5.1 11.M.5 cut-off)
