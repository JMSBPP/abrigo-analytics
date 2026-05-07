"""Posterior + prior parquet emission for SAAS-COHORT-1.

Orchestrates spec §10 emission:

- ``synthetic_tau_t.parquet`` — Hive-partitioned by ``tier_id`` × ``month``;
  τ_t / q_t_usd / q_t_cop populated from ``pm.sample_posterior_predictive``
  per spec §7 (MQ-B4 fix); r / p / α / x_m populated from ``idata.posterior``
  with the (μ, φ) → (r, p) reparameterization applied at emission time
  (NegBin parameterization pin per MQ-B2).
- ``cohort_prior.parquet`` — five percentiles (5/25/50/75/95) for each prior
  parameter; ``source = "spec-v1.1.1-§5.1-§5.2"``; ``fetched_at_utc =
  datetime.now(UTC).isoformat()``; ``schema_version`` from
  :data:`simulations.types.posterior.DEFAULT_SCHEMA_VERSION`.

Diagnostic gate (spec §8(7) + §8(8)) is enforced before any emission via
:class:`simulations.saas_builder.diagnostics.PosteriorDiagnostic`. Failed
verdict raises :class:`simulations.saas_builder._errors.DiagnosticGateError`
— NO partial emission.

Tier-import discipline: writes through
:class:`simulations.utils.parquet_io.SyntheticTauWriter` and
:class:`simulations.utils.parquet_io.CohortPriorWriter` ONLY. No direct
pandas / pyarrow calls. Hive layout (``tier_id=*/month=*/``) is enforced
by the writer per ``SYNTHETIC_TAU_PARTITION_COLS``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

import arviz as az
import numpy as np
import pymc as pm

from simulations.saas_builder._errors import DiagnosticGateError
from simulations.saas_builder.diagnostics import (
    DiagnosticVerdict,
    PosteriorDiagnostic,
)
from simulations.saas_builder.priors import (
    CohortPriors,
    negbin_mu_phi_to_r_p,
    tier_id_at_index,
)
from simulations.types.posterior import DEFAULT_SCHEMA_VERSION
from simulations.types.tier import TIER_IDS, TierID
from simulations.utils.audit_block import compute_audit_block
from simulations.utils.parquet_io import (
    CohortPriorRow,
    CohortPriorWriter,
    SyntheticTauRow,
    SyntheticTauWriter,
    cohort_prior_row,
    synthetic_tau_row,
)

# ─── Module-level constants ───────────────────────────────────────────────────

#: Spec §10 cohort_prior.parquet percentile grid. Strings (parquet column
#: dtype is "string" per ``COHORT_PRIOR_DTYPES``).
COHORT_PRIOR_PERCENTILES: tuple[str, ...] = ("5", "25", "50", "75", "95")

#: Numeric percentile grid corresponding to ``COHORT_PRIOR_PERCENTILES``.
_COHORT_PRIOR_QUANTILES: tuple[float, ...] = (0.05, 0.25, 0.50, 0.75, 0.95)

#: Spec-source string for cohort_prior.parquet provenance.
_PRIOR_SOURCE_TAG: str = "spec-v1.1.1-§5.1-§5.2"

#: Names of model.py parameters to emit cohort priors for. The TruncPareto
#: ``alpha_pareto`` is renamed to ``alpha`` at emission time so its column
#: name matches the synthetic_tau_t schema.
_PRIOR_PARAM_EMISSION_NAMES: tuple[str, ...] = (
    "mu",
    "phi",
    "alpha_pareto",
    "x_m",
)


# ─── Emission summary TypedDict ───────────────────────────────────────────────


class EmissionSummary(TypedDict):
    """Return shape of :meth:`CohortEmitter.__call__`.

    Pinned at the IO Boundary (consumed by callers as a documentation
    surface for what an emission produced). NOT a Pydantic model — this
    structure does not cross a system boundary requiring validation.
    """

    verdict: "DiagnosticVerdict"
    synthetic_tau_path: Path
    cohort_prior_path: Path
    audit_path: Path
    audit_block: str
    n_rows_synthetic: int


# ─── Posterior-predictive driver ──────────────────────────────────────────────


def run_posterior_predictive(
    model: pm.Model,
    posterior_idata: az.InferenceData,
    *,
    var_names: tuple[str, ...] = ("tau_t", "q_t_usd", "q_t_cop"),
    random_seed: int | None = 42,
) -> az.InferenceData:
    """Call ``pm.sample_posterior_predictive`` for the τ_t emission columns.

    Spec §7 line 415 + MQ-B4 fix: ``tau_t``, ``q_t_usd``, ``q_t_cop`` are
    functions of latent parameters AND new draws of the per-turn τ_{j,i}
    random variates; they MUST be populated from posterior-predictive,
    not from raw ``idata.posterior`` slicing (which would yield zero
    within-row variance at fixed parameter draws).

    Args:
        model: the ``pm.Model`` from
            :func:`simulations.saas_builder.model.T1ModelFactory.__call__`.
        posterior_idata: posterior :class:`arviz.InferenceData` from
            ``pm.sample(...)``.
        var_names: names to sample. Default: the three emission columns.
        random_seed: optional RNG seed for reproducibility.

    Returns:
        An :class:`arviz.InferenceData` with the ``posterior_predictive``
        group populated for ``var_names``.
    """
    with model:
        pp = pm.sample_posterior_predictive(
            posterior_idata,
            var_names=list(var_names),
            random_seed=random_seed,
            progressbar=False,
        )
    return pp


# ─── Emission orchestrator ────────────────────────────────────────────────────


@dataclass(frozen=True)
class CohortEmitter:
    """Spec §10 emission Callable.

    Attributes:
        base_dir: filesystem root for emission. ``synthetic_tau_t/`` and
            ``cohort_prior.parquet`` are written under this root. Defaults
            to ``simulations/saas_builder/data/``.
        diagnostic: the §8(7) + §8(8) gate Callable. Default uses
            :data:`~simulations.saas_builder.diagnostics.DEFAULT_MONITORED_PARAMS`.

    Behavior contract:

    - ``__call__(priors, model, posterior_idata, prior_idata)`` first
      runs ``diagnostic`` on the (posterior, prior) pair; raises
      :class:`DiagnosticGateError` on ``passed=False``.
    - Then runs ``pm.sample_posterior_predictive`` for τ_t / q_t_usd /
      q_t_cop (MQ-B4).
    - Then emits both parquet artifacts via the shipped writers.
    - Returns an emission summary dict with verdict + paths.
    - Idempotent: re-running over the same ``(tier_id, month)`` partition
      overwrites cleanly (writer-controlled).
    - Audit-block sha (from :mod:`simulations.utils.audit_block`) is
      recorded for every emission and written into a sidecar
      ``_AUDIT.json`` under ``base_dir``.
    """

    base_dir: Path = field(default_factory=lambda: Path("simulations/saas_builder/data"))
    diagnostic: PosteriorDiagnostic = field(default_factory=PosteriorDiagnostic)

    def __post_init__(self) -> None:
        # Coerce base_dir to Path defensively (callers may pass str).
        if not isinstance(self.base_dir, Path):
            object.__setattr__(self, "base_dir", Path(self.base_dir))

    def __call__(
        self,
        *,
        priors: CohortPriors,
        model: pm.Model,
        posterior_idata: az.InferenceData,
        prior_idata: az.InferenceData,
        month: int,
        tier_assignments: np.ndarray | None = None,
        random_seed: int | None = 42,
    ) -> EmissionSummary:
        """Run the gate, posterior-predictive, and parquet emission.

        Args:
            priors: prior pin bundle (used for cohort_prior.parquet rows).
            model: the ``pm.Model`` from ``T1ModelFactory().__call__()``.
            posterior_idata: ``arviz.InferenceData`` from ``pm.sample(...)``.
            prior_idata: ``arviz.InferenceData`` from
                ``pm.sample_prior_predictive(...)`` (required by §8(7) gate).
            month: integer month identifier (e.g. ``1``..``12``); becomes
                Hive partition key ``month=N``.
            tier_assignments: optional 1-D array of per-row ``TIER_IDS``
                indices (0/1/2). If ``None``, the emitter pulls ``tier_idx``
                samples from the posterior (this is the production path).
            random_seed: optional seed for the posterior-predictive draw.

        Returns:
            :class:`EmissionSummary` TypedDict with verdict, paths,
            audit-block hex, and row count.

        Contract:
            Preconditions:
                - ``month > 0`` (explicit guard, line ~218; raises
                  ``ValueError``).
                - ``posterior_idata`` must satisfy the
                  :meth:`PosteriorDiagnostic.__call__` preconditions
                  (posterior + sample_stats groups).
                - ``prior_idata`` must satisfy the §8(7) CI-width gate
                  preconditions (non-None; prior group present).
                - ``model`` must be a ``pm.Model`` whose unobserved RVs
                  match the names in ``posterior_idata.posterior`` so
                  ``pm.sample_posterior_predictive`` can resolve them.
                  A mismatch surfaces as a ``KeyError`` from PyMC at
                  the ``run_posterior_predictive`` step (implicit).
                - The shipped writer ``SyntheticTauWriter`` requires a
                  non-empty row list; if posterior + pp idata flatten
                  to zero rows (impossible for valid sample-output
                  shapes), it raises ``ValueError`` (implicit
                  fallthrough).
                - ``self.base_dir`` must be writable; otherwise
                  ``OSError`` propagates from
                  ``parent.mkdir(parents=True, exist_ok=True)`` and
                  ``DataFrame.to_parquet(...)``.

            Raises:
                DiagnosticGateError: explicit, line ~228. Fires iff the
                    spec §8(7) + §8(8) gate yields ``passed=False`` —
                    NO partial emission, NO sidecar audit-block. Caller
                    HALTs.
                ValueError: explicit, line ~218 (month ≤ 0); also
                    propagated from writers on dtype-cast failure.
                SchemaMismatchError: from
                    ``simulations.utils.parquet_io._check_columns``
                    if the row TypedDicts somehow diverge from
                    ``SYNTHETIC_TAU_COLUMNS`` / ``COHORT_PRIOR_COLUMNS``
                    (defensive — the row factories
                    ``synthetic_tau_row`` / ``cohort_prior_row``
                    construct the exact column set).
                OSError: filesystem write failure (mkdir / parquet
                    write / sidecar JSON write).
                pymc.SamplingError / pytensor.* errors: from
                    ``pm.sample_posterior_predictive`` if the model
                    surface is malformed (caller responsibility).

            Silences: none. NO partial emission means: if any step
                after the gate raises, the ``_AUDIT.json`` sidecar is
                NOT written, signaling caller that the parquet may be
                partial. Re-emission to the same partition path is
                idempotent (writer-controlled).
        """
        if month <= 0:
            raise ValueError(f"CohortEmitter: month = {month} must be > 0")

        # 1) Spec §8(7) + §8(8) gate.
        verdict = self.diagnostic(posterior_idata, prior_idata)
        if not verdict.passed:
            raise DiagnosticGateError(
                f"SAAS-COHORT-1 emission HALTED on diagnostic gate failure:"
                f" {verdict!r}"
            )

        # 2) Posterior-predictive draws for τ_t / q_t_usd / q_t_cop (MQ-B4).
        pp_idata = run_posterior_predictive(
            model,
            posterior_idata,
            random_seed=random_seed,
        )

        # 3) Build synthetic_tau_t rows.
        rows = self._build_synthetic_tau_rows(
            posterior_idata=posterior_idata,
            pp_idata=pp_idata,
            month=month,
            tier_assignments=tier_assignments,
        )
        writer_tau = SyntheticTauWriter(base_dir=self.base_dir)
        synthetic_tau_path = writer_tau(rows)

        # 4) Build cohort_prior.parquet rows from the prior_idata percentiles.
        prior_rows = self._build_cohort_prior_rows(
            priors=priors,
            prior_idata=prior_idata,
        )
        writer_prior = CohortPriorWriter(base_dir=self.base_dir)
        cohort_prior_path = writer_prior(prior_rows)

        # 5) Audit block sidecar. Hash the cohort_prior parquet file plus
        # every parquet leaf under the synthetic_tau Hive tree (the
        # synthetic_tau_path is a directory; compute_audit_block requires
        # regular files only).
        synthetic_tau_files = sorted(synthetic_tau_path.rglob("*.parquet"))
        audit_block = compute_audit_block(
            [cohort_prior_path, *synthetic_tau_files]
        )
        audit_path = self.base_dir / "_AUDIT.json"
        audit_payload: dict[str, object] = {
            "audit_block": audit_block,
            "schema_version": DEFAULT_SCHEMA_VERSION,
            "synthetic_tau_path": str(synthetic_tau_path),
            "cohort_prior_path": str(cohort_prior_path),
            "month": month,
            "n_rows_synthetic": len(rows),
            "verdict": {
                "rhat_max": verdict.rhat_max,
                "ess_bulk_min": verdict.ess_bulk_min,
                "ess_tail_min": verdict.ess_tail_min,
                "divergence_frac": verdict.divergence_frac,
                "ci_width_ratio_max": verdict.ci_width_ratio_max,
                "n_chains": verdict.n_chains,
                "n_draws_per_chain": verdict.n_draws_per_chain,
            },
        }
        audit_path.write_text(json.dumps(audit_payload, indent=2))

        return EmissionSummary(
            verdict=verdict,
            synthetic_tau_path=synthetic_tau_path,
            cohort_prior_path=cohort_prior_path,
            audit_path=audit_path,
            audit_block=audit_block,
            n_rows_synthetic=len(rows),
        )

    # ─── Private builders ────────────────────────────────────────────────

    def _build_synthetic_tau_rows(
        self,
        *,
        posterior_idata: az.InferenceData,
        pp_idata: az.InferenceData,
        month: int,
        tier_assignments: np.ndarray | None,
    ) -> list[SyntheticTauRow]:
        """Construct the ``SyntheticTauRow`` list for one month emission.

        Pulls posterior parameter draws (mu, phi, alpha_pareto, x_m) and
        posterior-predictive emission draws (tau_t, q_t_usd, q_t_cop) and
        zips them into one row per (chain × draw). NegBin (μ, φ) → (r, p)
        reparameterization applied at the boundary per MQ-B2.

        Tier assignment: if ``tier_assignments`` is None, samples are
        drawn from the posterior ``tier_idx`` group (production path).
        Each row's ``tier_id`` is the corresponding ``TIER_IDS[idx]``.
        """
        post = posterior_idata["posterior"]
        pp = pp_idata["posterior_predictive"]
        # Flatten (chain, draw) → row.
        mu_arr = np.asarray(post["mu"].values).ravel()
        phi_arr = np.asarray(post["phi"].values).ravel()
        alpha_arr = np.asarray(post["alpha_pareto"].values).ravel()
        x_m_arr = np.asarray(post["x_m"].values).ravel()
        n_rows = mu_arr.shape[0]

        tau_arr = np.asarray(pp["tau_t"].values).ravel()[:n_rows]
        qusd_arr = np.asarray(pp["q_t_usd"].values).ravel()[:n_rows]
        qcop_arr = np.asarray(pp["q_t_cop"].values).ravel()[:n_rows]

        if tier_assignments is None:
            tier_idx_arr = np.asarray(post["tier_idx"].values).ravel()[:n_rows]
        else:
            tier_idx_arr = np.asarray(tier_assignments, dtype=np.int64)
            if tier_idx_arr.shape[0] != n_rows:
                raise ValueError(
                    f"tier_assignments length {tier_idx_arr.shape[0]}"
                    f" must match flattened posterior rows {n_rows}"
                )

        rows: list[SyntheticTauRow] = []
        for sim_id in range(n_rows):
            mu_v = float(mu_arr[sim_id])
            phi_v = float(phi_arr[sim_id])
            r_v, p_v = negbin_mu_phi_to_r_p(mu_v, phi_v)
            idx = int(tier_idx_arr[sim_id]) % len(TIER_IDS)
            tier_id: TierID = tier_id_at_index(idx)
            rows.append(
                synthetic_tau_row(
                    month=int(month),
                    simulation_id=int(sim_id),
                    tier_id=tier_id,
                    r=r_v,
                    p=p_v,
                    alpha=float(alpha_arr[sim_id]),
                    x_m=float(x_m_arr[sim_id]),
                    tau_t=float(tau_arr[sim_id]),
                    q_t_usd=float(qusd_arr[sim_id]),
                    q_t_cop=float(qcop_arr[sim_id]),
                )
            )
        return rows

    def _build_cohort_prior_rows(
        self,
        *,
        priors: CohortPriors,
        prior_idata: az.InferenceData,
    ) -> list[CohortPriorRow]:
        """Construct ``CohortPriorRow`` list — five percentiles per param."""
        prior = prior_idata["prior"]
        fetched_at = datetime.now(timezone.utc).isoformat()
        rows: list[CohortPriorRow] = []
        for param in _PRIOR_PARAM_EMISSION_NAMES:
            if param not in prior:
                # Defensive: skip params absent from the prior idata
                # (e.g. emission name mismatch); never silently emit
                # zero values.
                continue
            samples = np.asarray(prior[param].values).ravel()
            finite = samples[np.isfinite(samples)]
            if finite.size == 0:
                continue
            for pct_str, q in zip(
                COHORT_PRIOR_PERCENTILES, _COHORT_PRIOR_QUANTILES
            ):
                value = float(np.quantile(finite, q))
                rows.append(
                    cohort_prior_row(
                        param=param,
                        percentile=pct_str,
                        value=value,
                        source=_PRIOR_SOURCE_TAG,
                        fetched_at_utc=fetched_at,
                    )
                )
        # Also emit the Dirichlet α-vector concentration as a documentary row.
        for i, a in enumerate(priors.tier.alpha_vector):
            rows.append(
                cohort_prior_row(
                    param=f"dirichlet_alpha[{i}]",
                    percentile="50",
                    value=float(a),
                    source=_PRIOR_SOURCE_TAG,
                    fetched_at_utc=fetched_at,
                )
            )
        # And the active-days-per-month constant (M1 anchor).
        rows.append(
            cohort_prior_row(
                param="active_days_per_month",
                percentile="50",
                value=float(priors.active_days_per_month),
                source=_PRIOR_SOURCE_TAG,
                fetched_at_utc=fetched_at,
            )
        )
        return rows


__all__ = [
    "COHORT_PRIOR_PERCENTILES",
    "CohortEmitter",
    "EmissionSummary",
    "run_posterior_predictive",
]
