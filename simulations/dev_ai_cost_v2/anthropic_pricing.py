"""modules-tier pure Callable: notional USD cost from token counts.

Spec ref: ``docs/specs/2026-05-16-ai-cost-factor-model-design.md`` v0.2.1
§3.2, §3.5, §5.2 (LiteLLM SHA pin), §0.1 CORRECTIONS-O (key names),
CORRECTIONS-V (``ts`` policy).

Tier rule: ``modules/`` may import ``types/`` but NOT ``utils/`` nor
``_errors``. ``PricingTable`` performs a single bounded JSON read at
construction (via ``Path.read_bytes`` in the classmethod); the resulting
instance is a frozen-slots dataclass with immutable ``MappingProxyType`` rate
dicts. ``__call__`` is purely arithmetic — no IO, no mutation.

Decimal-precision policy: rate values are converted via ``Decimal(str(x))`` to
avoid IEEE-754 float→Decimal precision loss. ``Decimal(float(x))`` is
FORBIDDEN.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from types import MappingProxyType

from simulations.dev_ai_cost_v2.types import TokensByCategory


# ─── Pinned LiteLLM rate-card constants ──────────────────────────────────────
#
# Per spec v0.2.1 §5.2 / CORRECTIONS-O: every ``claude-*`` model in the
# LiteLLM ``model_prices_and_context_window.json`` snapshot must carry all
# five required keys. Missing key → KeyError at load time (Wave 1 RC hint).

_REQUIRED_KEYS: tuple[str, ...] = (
    "input_cost_per_token",
    "output_cost_per_token",
    "cache_creation_input_token_cost",
    "cache_creation_input_token_cost_above_1hr",
    "cache_read_input_token_cost",
)

LITELLM_SHA_PINNED: str = "e58a561caa21169fb02174148444c08509ce7028"


# ─── PricingTable ────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class PricingTable:
    """Frozen rate-card lookup: ``(model, ts, toks) -> Decimal USD cost``.

    Fields:
        rates: nested immutable mapping
            ``{model: {required_key: Decimal rate}}`` (``MappingProxyType``
            at both levels). Only ``claude-*`` models are retained at load
            time; non-claude models in the source JSON are silently skipped
            (the v0.2.1 spec scopes the panel to Anthropic).
        sha: the LiteLLM commit SHA the rate card was loaded at. Pinned by
            ``LITELLM_SHA_PINNED`` for reproducibility audits.

    Invariants:
        - ``rates`` is immutable (``MappingProxyType``) — load-time only.
        - Every model present in ``rates`` carries all five
          ``_REQUIRED_KEYS`` (enforced at ``from_litellm_sha`` load).
        - Every rate value is a ``Decimal`` constructed via
          ``Decimal(str(...))`` to preserve source-string precision.
    """

    rates: Mapping[str, Mapping[str, Decimal]]
    sha: str

    @classmethod
    def from_litellm_sha(
        cls,
        sha: str,
        cached_json_path: Path,
        *,
        skip_sha_check: bool = False,
    ) -> "PricingTable":
        """Load the cached LiteLLM ``model_prices_and_context_window.json``.

        Per spec v0.2.1 §5.2 + CORRECTIONS-O: every ``claude-*`` model must
        carry all five required keys (``input_cost_per_token``,
        ``output_cost_per_token``, ``cache_creation_input_token_cost``,
        ``cache_creation_input_token_cost_above_1hr``,
        ``cache_read_input_token_cost``); missing key raises ``KeyError`` at
        load time (Wave 1 RC hint — fail-fast at boundary).

        Per CORRECTIONS-V, the pinned SHA captures one historical price-step
        snapshot. The downstream ``__call__(ts=...)`` argument is the
        sentinel for the multi-step dispatch path; for v0.2.1 single-snapshot
        loads, ``ts`` is accepted but does not alter the lookup.

        Args:
            sha: LiteLLM commit SHA the rate card is supposed to be at.
                Must equal ``LITELLM_SHA_PINNED`` unless ``skip_sha_check``.
            cached_json_path: filesystem path to the cached LiteLLM JSON
                blob (``Path.read_bytes`` is the single IO call).
            skip_sha_check: testing escape hatch. When ``True``, the SHA
                comparison is bypassed (so test fixtures with synthetic
                tables can be loaded). Production callers MUST pass
                ``False`` (the default).

        Returns:
            A frozen ``PricingTable`` with ``MappingProxyType`` rate
            mappings.

        Raises:
            ValueError: when ``skip_sha_check`` is ``False`` and the
                supplied ``sha`` does not equal ``LITELLM_SHA_PINNED``.
            KeyError: when any ``claude-*`` model in the source JSON is
                missing one of the five required keys.

        Errors from external state:
            FileNotFoundError: when ``cached_json_path`` does not exist.
            json.JSONDecodeError: when the cached file is not valid JSON.
            OSError: for other filesystem read failures.

        Silenced errors:
            None. The only intentional silencing is the skip of non-dict
            and non-``claude-*`` entries in the source JSON (the v0.2.1
            spec scopes the panel to Anthropic models only); this is a
            *filter*, not a swallowed error.
        """
        raw: bytes = cached_json_path.read_bytes()
        if not skip_sha_check:
            # Sanity-check that the caller's commit-SHA argument matches the
            # pinned snapshot. (Content-hash verification against a stored
            # digest in DATA_PROVENANCE.md is a separate provenance step;
            # this is a guard against accidental SHA-arg drift in callers.)
            _content_digest_unused = hashlib.sha256(raw).hexdigest()
            del _content_digest_unused
            if sha != LITELLM_SHA_PINNED:
                raise ValueError(
                    f"PricingTable refuses load: requested SHA {sha} != "
                    f"pinned {LITELLM_SHA_PINNED}"
                )

        table = json.loads(raw)
        out: dict[str, Mapping[str, Decimal]] = {}
        for model, rates in table.items():
            if not model.startswith("claude-"):
                continue
            if not isinstance(rates, dict):
                continue
            for k in _REQUIRED_KEYS:
                if k not in rates:
                    raise KeyError(
                        f"LiteLLM SHA {sha}: model {model} missing required "
                        f"key {k!r}"
                    )
            out[model] = MappingProxyType(
                {k: Decimal(str(rates[k])) for k in _REQUIRED_KEYS}
            )
        return cls(rates=MappingProxyType(out), sha=sha)

    def __call__(
        self,
        model: str,
        ts: datetime,
        toks: TokensByCategory,
    ) -> Decimal:
        """Notional USD cost for one message at exact-Decimal precision.

        Per CORRECTIONS-V, ``ts`` is accepted as a sentinel for time-varying
        price-step lookups. The pinned LiteLLM SHA captures one snapshot;
        when the table is upgraded to multi-step (effective-from dated
        entries), this method dispatches based on ``ts``. For v0.2.1
        single-snapshot loads, ``ts`` is accepted but does not alter the
        lookup.

        Args:
            model: Anthropic model identifier (must be a ``claude-*`` key
                present in ``self.rates``).
            ts: timezone-aware UTC datetime of the message (sentinel —
                see above; no tz-validation performed here because
                ``MessageRecord`` already enforces tz-awareness at the
                upstream boundary).
            toks: per-category token counts.

        Returns:
            ``Decimal`` USD cost — exact arithmetic, no float
            intermediates. Non-negative (``TokensByCategory`` enforces
            non-negative inputs; rates are non-negative by source).

        Raises:
            KeyError: when ``model`` is not present in ``self.rates``
                (either an unknown model or a non-claude model that was
                filtered out at load time).

        Errors from external state:
            None. Pure arithmetic against the frozen ``self.rates`` table.

        Silenced errors:
            None.
        """
        if model not in self.rates:
            raise KeyError(f"PricingTable has no rates for model {model!r}")
        r = self.rates[model]
        return (
            Decimal(toks.input) * r["input_cost_per_token"]
            + Decimal(toks.output) * r["output_cost_per_token"]
            + Decimal(toks.cache_create_5m) * r["cache_creation_input_token_cost"]
            + Decimal(toks.cache_create_1h)
            * r["cache_creation_input_token_cost_above_1hr"]
            + Decimal(toks.cache_read) * r["cache_read_input_token_cost"]
        )


__all__ = [
    "LITELLM_SHA_PINNED",
    "PricingTable",
]
