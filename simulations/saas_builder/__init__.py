"""SAAS-COHORT-1 — T1 (subscription-cap) per-user latent-cost posterior.

Implements spec v1.1.1 §5.1 (T1 row) + §5.2 (tier prior + pricing) + §10
(emission schemas) for the Colombian solo AI-native SaaS-builder cohort.

Three-tier package layout (functional-python skill):

- ``priors.py`` — Value tier (frozen-dc prior hyperparameter containers
  with M1 α-floor enforced).
- ``model.py`` — Callable tier (PyMC model factory implementing the
  spec §5.1 (T1) doubly-stochastic compound sum
  ``τ_t = Σ_j Σ_i τ_{j,i}`` with per-active-day NegBin(μ, φ) and
  iid TruncPareto(α, x_m, κ); M3 blended-price assertion at call site).
- ``diagnostics.py`` — Callable tier (arviz r-hat / ESS_bulk / ESS_tail /
  divergence / sim-count / posterior-vs-prior CI-width gate).
- ``emit.py`` — Callable tier (orchestrator — calls
  ``pm.sample_posterior_predictive`` for τ_t / q_t_usd / q_t_cop columns,
  then emits Hive-partitioned parquet via
  ``simulations.utils.parquet_io``).

Tier-import discipline (NON-NEGOTIABLE — plan §3 rule "Any modification
request triggers HALT and a SIM-INFRA follow-up plan"):

- May import: ``simulations.types``, ``simulations.modules``,
  ``simulations.utils``.
- May NOT modify any of the above.
- Cohort-local exceptions (e.g. :class:`DiagnosticGateError`) live in
  ``_errors.py`` to avoid SIM-INFRA-0 surface modification.
"""

from __future__ import annotations
