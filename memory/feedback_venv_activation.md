---
name: Activate venv before forge test --ffi
description: Must activate contracts/.venv before running forge test --ffi or any FFI-dependent test
type: feedback
originSessionId: 6d731f8a-e8a0-47d1-8267-b6a4ff88dd79
---
Always activate the Python virtual environment before running forge tests with FFI:

```bash
source /home/jmsbpp/apps/ThetaSwap/thetaSwap-core-dev/.worktree/ranFromAngstrom/contracts/.venv/bin/activate
```

**Why:** FFI tests in BaseTest.sol call `.venv/bin/python3.12` (or the configured path). Without activation the Python executable path resolves incorrectly and FFI tests fail.

**How to apply:** Any time running `forge test --ffi` in the angstrom contracts worktree, activate this venv first in the same shell session.
