"""Verify-only API surface for SaaS-Builder Stage-2 notebooks-trio.

Per design v0.3 §3a. Three-tier: types (Value), checks (Callable),
io (IO Boundary). Notebooks import only from this module; no reach
into simulations.modules / simulations.utils internals.
"""
from __future__ import annotations

from simulations.saas_builder.verify.types import RTagVerdict, TrioRollup

__all__: list[str] = [
    "RTagVerdict",
    "TrioRollup",
]
