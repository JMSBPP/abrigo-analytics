---
name: RAN pipeline session state and continuation reference
description: Complete session state for the ran-growth-pipeline Python backend — resume from here after compaction or new session
type: project
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
## Session Purpose

This session builds the **off-chain Python backend** for the RAN vault:
- Data pipelines (fetch globalGrowth from Alchemy archive RPC → DuckDB)
- Query APIs (for Solidity FFI fork tests + notebook EDA)
- Analytics/EDA (notebooks for test vector discovery)
- NO Solidity — scripts-only scope

## Current State (as of 2026-04-11)

### What's DONE and MERGED on `ran-growth-pipeline` branch:

1. **Pipeline infrastructure** (101 tests passing):
   - `scripts/ran_utils.py` — shared utilities, slot derivation, hex encoding, pool config
   - `scripts/ran_growth_pipeline.py` — bulk fetcher with combined batches (storage + block timestamps), retry, smart resume, CLI
   - `scripts/ran_growth_query.py` — JSON query by block number
   - `scripts/ran_ffi.py` — FFI script with `len` + `row` subcommands (0x ABI-encoded for Solidity)
   - `scripts/freeze_ran_snapshots.py` — refactored, tick functions stubbed
   - `scripts/tests/conftest.py` — 6 fixtures, mock transport with eth_getBlockByNumber support

2. **DuckDB data** (`data/ran_accumulator.duckdb`):
   - 37,678 rows, block 22,972,937 → 24,856,787
   - Schema: `(block_number, pool_id, global_growth, block_timestamp, sampled_at, stride)`
   - All timestamps backfilled, verified 20/20 against Alchemy
   - Pool: USDC_WETH (`0xe500...a657`)

3. **Notebook** (`notebooks/growthGlobal.ipynb`):
   - Kernel: `ran-venv` (Python 3.13)
   - Has basic EDA cells but needs update to use `ran_data_api`

### What's IN PROGRESS (spec written, awaiting review):

**`ran_data_api.py`** — shared query API module. Spec at:
`docs/specs/2026-04-11-ran-data-api-design.md`

This adds:
- Pure query functions: `dataset_len`, `get_row`, `get_by_timestamp`, `get_range`, `get_min`, `get_max`, `get_all`
- Frozen `Row` dataclass
- New FFI subcommands: `row-by-ts`, `range`, `min`, `max`
- Notebook EDA using the API (no raw SQL)

**3-way spec review dispatched** (Code Reviewer + Reality Checker + Technical Writer). Results pending.

### What's NEXT after ran_data_api:

1. **Implementation plan** (`/superpowers:writing-plans`) for ran_data_api
2. **Data Engineer implements** with strict TDD
3. **2-way review** (Code Reviewer + Reality Checker)
4. **Notebook EDA** — Analytics Reporter builds visualizations later
5. **Timestamp backfill pipeline re-run** if new blocks accumulated

## Key Reference Files

| File | Purpose |
|------|---------|
| `docs/specs/2026-04-10-ran-growth-pipeline-design.md` | Original pipeline spec |
| `docs/specs/2026-04-11-ran-ffi-query-api-design.md` | FFI + schema upgrade spec |
| `docs/specs/2026-04-11-ran-data-api-design.md` | Data query API spec (LATEST) |
| `docs/plans/2026-04-10-ran-growth-pipeline.md` | Original pipeline plan |
| `docs/plans/2026-04-11-ran-ffi-query-api.md` | FFI + schema upgrade plan |
| `contracts/TODO_DATA_ANALYSIS.md` | Solidity fuzz test reference (the target consumer) |
| `scratch/competing-agents-research.md` | Research on multi-agent patterns |
| `scratch/angstrom-indexer-globalGrowth-research.md` | Why archive RPC is the only data source |

## How to Resume

1. Read this memory file + the MEMORY.md index
2. Read the LATEST spec: `docs/specs/2026-04-11-ran-data-api-design.md`
3. Check if 3-way review results are pending or need re-dispatch
4. If approved: transition to `/superpowers:writing-plans` for implementation
5. Follow all NON-NEGOTIABLE rules from memory (TDD, scripts-only, real data, 2-way review)

## Agent Roles (NON-NEGOTIABLE)

- **Data Engineer**: implements ALL code and fixes
- **Code Reviewer + Reality Checker**: review implementations (2-way)
- **Code Reviewer + Reality Checker + Technical Writer**: review specs/plans (3-way)
- **Analytics Reporter**: notebook visualizations (future session)
