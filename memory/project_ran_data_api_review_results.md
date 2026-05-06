---
name: ran_data_api spec 3-way review results (pending fixes)
description: Review results for ran_data_api spec — Code Reviewer PASS, Tech Writer 8 issues, Reality Checker pending
type: project
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
## 3-Way Review Results for `2026-04-11-ran-data-api-design.md`

### Code Reviewer: PASS — 0 BLOCK, 2 FLAG
- F1: `pool_id` parameter type — state explicitly it's raw hex, not friendly name
- F2: Negative index rejection — should happen at API layer

### Tech Writer: PASS WITH ISSUES — 3 blocking, 3 important, 2 moderate
- B1: `global_growth` in Row — clarify it's bytes32-width hex string (32 bytes = 64 hex + 0x)
- B2: `QueryError` — nail down exact name, location, base class (no "e.g.")
- B3: Who opens DuckDB? API takes `conn`, but error table says API raises "file not found" — resolve boundary
- I1: `get_by_timestamp` tie-breaking when multiple rows share timestamp — define ORDER BY
- I2: Notebook "flag" — define output format (print count + first 10 violating indices)
- I3: "Long flat region" — define threshold (e.g., 10+ consecutive zero-delta strides)
- M1: Deviation from TODO Solidity pattern (combined tuple vs 3 separate calls) — add note
- M2: Conftest fixture for API tests — need `populated_db_conn` or guidance to open from path

### Reality Checker: NEEDS WORK — 1 HIGH, 2 MEDIUM, 5 LOW
- H1: `populated_db_path` has only 6 rows — cannot test 1000-row limit independently
- M1: `dataset_len` counts NULLs but `get_row` errors on NULLs — inconsistency
- M2: No query strategy/index guidance for `get_by_timestamp` nearest-lower
- L1: FFI wrapper connection lifecycle not documented
- L2: No multi-range access pattern guidance
- L3: `from == to` treated as error vs empty result
- L4: Notebook raw SQL migration scope larger than described
- L5: Stale notebook "PENDING" note not called out

## ALL Fixes to Apply (deduplicated from 3 reviewers)

### From Code Reviewer:
1. `pool_id` is raw `0x`-prefixed hex in API; name resolution at caller layer

### From Tech Writer:
2. `QueryError(Exception)` defined in `ran_data_api.py`, just message string — drop "e.g."
3. API takes open `conn` — "DuckDB file not found" is FFI-layer only, remove from API error table
4. `get_by_timestamp` tie-breaking: highest `block_number` wins (`ORDER BY block_number DESC LIMIT 1`)
5. Notebook "flag" = print summary count + first 10 violating indices
6. "Long flat region" = 10+ consecutive strides with zero growth delta
7. Add note: Solidity test uses combined tuple from `row` (deviation from TODO example)
8. Tests open `duckdb.connect(populated_db_path, read_only=True)` — no new fixture needed

### From Reality Checker:
9. Add a large fixture (1001+ rows) or test validation ordering for 1000-row limit
10. Resolve `dataset_len` counting NULLs vs `get_row` rejecting NULLs — add note that callers must handle QueryError within valid index range
11. Add note: timestamp scan acceptable at current scale (~37K rows), no secondary index needed
12. Negative index rejection at API layer (not just FFI)
13. `from == to` → empty list (not error). Only `from > to` → error
