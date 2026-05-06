---
name: Tests must prioritize real data over mock data
description: NON-NEGOTIABLE — tests should use real on-chain data, real RPC responses, real DuckDB when possible; mocks only as last resort
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**NON-NEGOTIABLE:** Tests must prioritize real data over mock data. Always.

**Priority order:**
1. **Real data** — actual on-chain values, real RPC responses from fixtures, real DuckDB operations
2. **Recorded data** — frozen snapshots of real RPC responses (like `ran_accumulator_snapshots.json`)
3. **Mock data** — only when real data is impossible (e.g., simulating HTTP 429 errors, timeout exceptions)

**Why:** Mock-based tests can pass while the real system fails. Real data catches integration issues that mocks hide.

**How to apply:**
- Use the existing `ran_accumulator_snapshots.json` fixture data (real on-chain values) in tests
- For DuckDB tests, use real DuckDB operations (not mocked DB interfaces)
- For RPC tests, use real response formats with real `globalGrowth` values from the fixture
- Mock ONLY the HTTP transport layer (to avoid hitting Alchemy), but feed it real response data
- Mock HTTP error codes (429, 500, timeout) since those can't be reproduced reliably
