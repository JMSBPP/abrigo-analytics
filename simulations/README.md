# `simulations/` — Global FX-vol simulation infrastructure

This package hosts the global (cross-iteration) infrastructure for every
FX-vol simulation iteration in this repo: SaaS-builder Stage-2,
Pair D, dev-AI, and any future cohort.

It is the implementation of plan
`docs/plans/2026-05-07-sim-infra-0.md` (SIM-INFRA-0).

## Three-tier discipline (NON-NEGOTIABLE)

Per `~/.claude/skills/functional-python/SKILL.md`, every `.py` file in this
package belongs to exactly one tier. Misplacement is a Reality Checker BLOCK.

| Tier | Directory | Construct | Imports allowed from |
|------|-----------|-----------|----------------------|
| **Value** | `types/` | `@dataclass(frozen=True)` + `__post_init__` validation only. Accessors are FREE FUNCTIONS, not methods. | stdlib + numpy + typing only |
| **Callable** | `modules/` | `@dataclass(frozen=True)` + `__call__`. Config in fields, logic in `__call__`. Stateless. | `simulations.types` only |
| **IO Boundary** | `utils/` | Class with `__init__`. The ONLY place mutable state lives. Filesystem / network / opaque external APIs. | `simulations.types` (Pydantic allowed transiently for JSON validation) |

`typing.Protocol` is allowed — for cross-tier interfaces it lives in
`types/` and is implemented in `modules/` or `utils/`.

No inheritance other than `Protocol` (and stdlib `Exception` subclasses).

## `__init__.py` policy (per Phase 1 reconciliation §2.9)

Every `__init__.py` declares an explicit `__all__: list[str]`. No star
imports. No transitive re-exports across tier boundaries — cross-tier
consumers fully-qualify imports
(`from simulations.types.distributions import TruncParetoParams`).

This makes the Reality Checker tier-import grep mechanically reliable:
violations show up as direct submodule imports across tiers.

## Extension model — per-iteration peers without inheritance

Per Phase 1 reconciliation §2.7 + §2.8, future iterations may add a peer
folder beside the global ones:

```
simulations/
├── types/           ← global Value types
├── modules/         ← global Callables
├── utils/           ← global IO boundaries
├── pair_d/
│   ├── types/       ← per-iter Values (optional)
│   ├── modules/     ← per-iter Callables
│   └── utils/       ← per-iter IO (rare)
└── saas_builder/    ← (this iteration uses globals only; no per-iter types/)
```

When a per-iteration Callable needs to extend a global Callable, use one of
three patterns (in preference order). **Inheritance is forbidden.**

1. **Wrap (default).** Per-iter Callable holds the global Callable as a
   frozen field and delegates inside `__call__`.
2. **Protocol-based polymorphism.** Per-iter Callable implements the same
   `typing.Protocol` declared in `simulations/types/`.
3. **Higher-order constructor.** A free function returns a configured
   frozen-dataclass.

The SaaS-builder Stage-2 iteration uses globals only (no
`simulations/saas_builder/types/`).

## Phase ordering

This is implemented per the SIM-INFRA-0 plan in four sub-tasks:

- **Task 2.1** — `simulations/types/` (Value tier) — THIS COMMIT.
- **Task 2.2** — `simulations/modules/` (Callable tier) — depends on 2.1.
- **Task 2.3** — `simulations/utils/` (IO Boundary tier) — depends on 2.1.
- **Task 2.4** — `simulations/tests/` (strategies + math-pin tests).

## Math pins (Phase 2 prelude — see plan §"Phase 2 prelude")

- **M1.** TruncPareto α-floor (α ≥ 1.5 for SaaS-builder cohort, spec §8(6))
  binds at the **sampler Callable** in `modules/`, NOT on
  `types/TruncParetoParams` (which accepts any α > 0). See
  `types/distributions.py` docstring contract.
- **M2.** Softplus β-tightness (L¹ deviation < 1e-3·κ on [0, 2κ]) is
  enforced at the **regularizer Callable** in `modules/`. The free
  function `tightness_l1_deviation` in `types/distributions.py` is the
  computational primitive.
- **M3.** Blended `p_t` formula (spec §5.1) lives in `modules/`.
- **M4.** Parquet + JSON column schemas (spec §10) live in `utils/` as
  TypedDict row schemas; the corresponding Value containers
  (`PosteriorDraws`, `MonthlyCDF`, `ZCapPinned`) live in `types/`.
- **M5.** FX path closed form (PRIMITIVES (6) + (8)) lives in `modules/`;
  the parameter Value `FXPathParams` lives in `types/`.

See each tier's `README.md` for detail.
