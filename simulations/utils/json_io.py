"""JSON IO boundaries for the M4 ``Z_cap_pinned.json`` schema (spec §10).

Per Phase 1 reconciliation §2.2, **Pydantic appears ONLY here**. The
private ``_ZCapPinnedJsonModel`` is a *transient* validation container:
it is constructed by ``model_validate_json`` on read, immediately
converted to the frozen-dc ``ZCapPinned`` Value, and then discarded. It
is never returned to consumers and never exported.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Final, cast

from pydantic import BaseModel, ConfigDict, Field

from simulations.types.posterior import DEFAULT_SCHEMA_VERSION, ZCapPinned
from simulations.types.tier import TIER_IDS, TierID
from simulations.utils.errors import SchemaMismatchError

#: M4 ``Z_cap_pinned.json`` field set (spec §10 + Phase 1 reconciliation §2.4).
Z_CAP_PINNED_FIELDS: Final[tuple[str, ...]] = (
    "Z_cop_per_month",
    "ci_95_lo",
    "ci_95_hi",
    "audit_block",
    "tier_mix",
    "schema_version",
)


class _ZCapPinnedJsonModel(BaseModel):
    """Transient Pydantic validator for ``Z_cap_pinned.json`` (private).

    Not exported; never returned to consumers. Constructed by the JSON
    reader, converted to ``ZCapPinned`` (frozen-dc Value), then discarded
    per Phase 1 reconciliation §2.2.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    Z_cop_per_month: float
    ci_95_lo: float
    ci_95_hi: float
    audit_block: str = Field(min_length=64, max_length=64)
    tier_mix: dict[str, float]
    schema_version: str = Field(default=DEFAULT_SCHEMA_VERSION, min_length=1)


def _coerce_tier_mix(raw: Mapping[str, float]) -> dict[TierID, float]:
    """Narrow string keys back into the ``TierID`` Literal set; raise on drift."""
    admissible = set(TIER_IDS)
    keys = set(raw.keys())
    if keys != admissible:
        raise SchemaMismatchError(
            f"Z_cap_pinned.json: tier_mix keys must be exactly {admissible};"
            f" got {keys}"
        )
    # ``raw`` keys are str-typed at the JSON layer; we have just verified
    # set-equality with the TierID literal set, so the cast is safe.
    return cast(
        "dict[TierID, float]",
        {k: float(v) for k, v in raw.items()},
    )


class ZCapPinnedReader:
    """Read ``Z_cap_pinned.json`` (M4); return a ``ZCapPinned`` Value."""

    def __init__(self) -> None:
        pass

    def __call__(self, path: str | Path) -> ZCapPinned:
        target = Path(path)
        if not target.is_file():
            raise FileNotFoundError(f"ZCapPinnedReader: missing JSON at {target}")
        raw_text = target.read_text(encoding="utf-8")
        # Pre-check the JSON's field set so consumers get a SchemaMismatchError
        # (rather than a Pydantic ValidationError) on column drift.
        parsed = json.loads(raw_text)
        if not isinstance(parsed, dict):
            raise SchemaMismatchError(
                f"Z_cap_pinned.json: top-level value must be an object;"
                f" got {type(parsed).__name__}"
            )
        actual = set(parsed.keys())
        expected = set(Z_CAP_PINNED_FIELDS)
        if actual != expected:
            raise SchemaMismatchError(
                f"Z_cap_pinned.json: field set mismatch."
                f" missing={sorted(expected - actual)!r}"
                f" extra={sorted(actual - expected)!r}"
            )
        validated = _ZCapPinnedJsonModel.model_validate_json(raw_text)
        # Convert transient Pydantic model → frozen-dc Value before returning.
        return ZCapPinned(
            Z_cop_per_month=validated.Z_cop_per_month,
            ci_95_lo=validated.ci_95_lo,
            ci_95_hi=validated.ci_95_hi,
            audit_block=validated.audit_block,
            tier_mix=_coerce_tier_mix(validated.tier_mix),
            schema_version=validated.schema_version,
        )


class ZCapPinnedWriter:
    """Write a ``ZCapPinned`` Value to a JSON file (M4)."""

    def __init__(self) -> None:
        pass

    def __call__(self, z: ZCapPinned, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, object] = {
            "Z_cop_per_month": z.Z_cop_per_month,
            "ci_95_lo": z.ci_95_lo,
            "ci_95_hi": z.ci_95_hi,
            "audit_block": z.audit_block,
            "tier_mix": dict(z.tier_mix),
            "schema_version": z.schema_version,
        }
        target.write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
