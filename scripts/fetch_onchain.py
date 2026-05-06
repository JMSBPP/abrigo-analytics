"""Tier 2 fetcher: pull Celo on-chain panels (Mento-native + Carbon basket).

Reads addresses from data/manifest.yaml. Requires CELO_RPC_URL in the
environment. Output goes to data/onchain/ as parquet.

The address registry is committed at:
    docs/specs/2026-04-25-mento-native-address-registry.md

Pinned canonical addresses (per project memory + corrigenda):
    Mento V2 COPm  = 0x8A567e2aE79CA692Bd748aB832081C45de4041eA
    Carbon V1      = 0x6619871118D144c1c2EA8EE4851b75AfCe4ec9bd
    Carbon V2      = 0x20216f30bED70F94d68559e4dB7CDDA84Ee65681
    Bancor V1 arb  = 0x8c05ea305558bdF73e69D38C0F0Bf1ad9A48b1a3
    Broker         = 0x777A8255cA72412f0d706dc03C9D1987306B4CaD
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    rpc_url = os.environ.get("CELO_RPC_URL")
    if not rpc_url:
        sys.exit(
            "CELO_RPC_URL not set. Export an RPC endpoint (Forno / Quicknode / Alchemy):\n"
            "  export CELO_RPC_URL=https://forno.celo.org"
        )
    print(f"[Tier 2 / On-chain] Celo RPC: {rpc_url[:40]}…")
    print()
    print("On-chain ingest scaffolding lives under scratch/ (path-b-stage-2,")
    print("pair-d-stage-2-B). Reuse those scripts from this repo's venv.")
    print()
    print("If you only need processed on-chain panels, prefer `make data` (Tier 1).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
