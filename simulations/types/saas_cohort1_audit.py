"""Audit Value tier — frozen-dataclass mirror of `_AUDIT.json` schema.

Hosts the existing `_AUDIT.json` schema as a frozen-dataclass Value type.
Created by SaaS-Builder Stage-2 verify sub-package Phase 0; consumed by
`simulations.utils.json_io.AuditReader` and threaded into the trio audit
chain through `simulations.saas_builder.verify.io.CommittedArtifactLoader`.

Math pin: not directly involved. The hosted `audit_block` is the same
64-char lowercase hex sha256 produced by
`simulations.utils.audit_block.compute_audit_block`.
"""
from __future__ import annotations

from dataclasses import dataclass


class AuditValueError(ValueError):
    """Raised when an Audit Value fails post-init validation."""


@dataclass(frozen=True)
class AuditVerdict:
    """C1 posterior diagnostic block (six gate metrics)."""

    rhat_max: float
    ess_bulk_min: float
    ess_tail_min: float
    divergence_frac: float
    ci_width_ratio_max: float
    n_chains: int
    n_draws_per_chain: int

    def __post_init__(self) -> None:
        if self.n_chains <= 0:
            raise AuditValueError(f"n_chains must be positive, got {self.n_chains}")
        if self.n_draws_per_chain <= 0:
            raise AuditValueError(
                f"n_draws_per_chain must be positive, got {self.n_draws_per_chain}"
            )


@dataclass(frozen=True)
class Audit:
    """C1 audit block — input-data lineage + posterior diagnostic verdict."""

    audit_block: str
    schema_version: str
    synthetic_tau_path: str
    cohort_prior_path: str
    month: int
    n_rows_synthetic: int
    verdict: AuditVerdict

    def __post_init__(self) -> None:
        if len(self.audit_block) != 64:
            raise AuditValueError(
                f"audit_block must be 64-char lowercase hex sha256; "
                f"got len={len(self.audit_block)}"
            )
        try:
            int(self.audit_block, 16)
        except ValueError as e:
            raise AuditValueError(f"audit_block is not valid hex: {e!s}") from e
        if self.audit_block != self.audit_block.lower():
            raise AuditValueError("audit_block must be lowercase hex")
        if self.n_rows_synthetic < 0:
            raise AuditValueError(
                f"n_rows_synthetic must be non-negative, got {self.n_rows_synthetic}"
            )
        if self.month < 1 or self.month > 12:
            raise AuditValueError(f"month must be in [1, 12], got {self.month}")
