---
name: Pipeline work is scripts-only — never touch contracts or foundry config
description: NON-NEGOTIABLE — pipeline agents may ONLY modify scripts/, data/, .gitignore, and test fixtures. NEVER touch src/, test/*.sol, foundry.toml, or any Solidity file
type: feedback
originSessionId: e966a106-4cc4-4964-b846-9be41adb5539
---
**NON-NEGOTIABLE:** The globalGrowth pipeline is **scripts-only** work. Agents must NEVER touch:
- `contracts/src/` (any Solidity source)
- `contracts/test/**/*.sol` (any Solidity test)
- `contracts/foundry.toml`
- `contracts/remappings.txt`
- Any `.sol` file anywhere
- Any forge/foundry configuration

**Allowed files (exhaustive):**
- `contracts/scripts/*.py` (pipeline modules)
- `contracts/scripts/tests/*.py` (Python tests)
- `contracts/scripts/__init__.py` and `contracts/scripts/tests/__init__.py`
- `contracts/data/` (DuckDB files, .gitkeep)
- `contracts/.gitignore` (adding Python/DuckDB patterns only)
- `contracts/requirements.txt` (if deps change)

**PR enforcement:** When opening a PR, the diff must contain ONLY files from the allowed list above. Any PR that modifies Solidity files, foundry.toml, or anything outside `scripts/` and `data/` must be rejected.

**Why:** User explicitly scoped this as non-intrusive to the smart contract development workflow. The pipeline is a Python-only backend layer that reads from chain — it does not modify, compile, test, or deploy contracts.

**How to apply:** Before every commit, run `git diff --name-only` and verify every file is in the allowed list. Before opening a PR, verify the same. Reject any agent output that includes disallowed files.
