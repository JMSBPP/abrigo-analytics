# Panoptic Primitive Comparison Table — Stage-3 A1 Phase 1

**Author:** general-purpose implementer (Stage-3 A1 Task 1.1)
**Date:** 2026-05-11
**Plan anchor:** docs/plans/2026-05-11-stage-3-a1-panoptic-restrategy.md v0.2
**Consumed strip audit_block:** 94150326332b90e50cfe02b580e6d05280100b430de0089ea9197c8fa4aaf329
**Anti-fishing posture:** factual catalogue ONLY; no pre-ranking; no recommendation.

## §1 Methodology

Sources consulted on 2026-05-11 via WebFetch against the public `panoptic.xyz` documentation, research, and blog surfaces. Three pages drove the primitive enumeration: the research piece "18 Options Strategies Every Trader Should Know" (which enumerates the explicit named strategies the Panoptic product layer surfaces to traders), the `/docs/contracts/smart-contracts-overview` page (which constrains every Panoptic position to at most four legs via the Semi-Fungible Position Manager wrapping up to 4-legged Uniswap v3 positions), and the `/docs/product/streamia` and `/docs/product/timescales` pages (which establish that Streamia is a funding-rate mechanism applied universally to all positions and Timescales is a per-position width parameter — neither is a primitive in its own right). The liquidity-status column is anchored to the July-2025 corporate blog post "Panoptic: Your Next DeFi Alpha", which is the most recent reachable status statement; it confirms live deployments on Ethereum mainnet, Unichain, and Base, with cumulative trading volume above USD 25M since the December 2024 launch.

Scope limits I want to be explicit about. I did not access the Solidity source on GitHub, the V2-beta technical paper, or any Dune dashboard for per-primitive open-interest. The "on-chain liquidity status" column therefore reflects *protocol-level* liquidity reachability (live / limited / inactive at the venue), not per-primitive OI. Where the named strategy in the research article exceeds the contract-layer 4-leg ceiling (ZEEHBS has 6 legs), I mark the on-chain status as "constructible only as multi-position bundle" rather than as a single SFPM-wrapped position — this is a factual contract constraint, not an opinion on tradability. Streamia and Timescales are catalogued as non-primitives in §3 rather than as table rows.

## §2 Comparison table

| primitive_id | leg_count | payoff_shape | convexity_class | on-chain_liquidity | admits_strip_emit? | source_url | access_timestamp |
|---|---|---|---|---|---|---|---|
| long_call | 1 | piecewise-linear, convex above strike | long-vol (directional bullish) | live (Ethereum, Unichain, Base) | yes — single strike, single weight is a trivial ladder | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| long_put | 1 | piecewise-linear, convex below strike | long-vol (directional bearish) | live (Ethereum, Unichain, Base) | yes — single strike, single weight | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| short_call | 1 | piecewise-linear, concave above strike | short-vol (directional bearish) | live (Ethereum, Unichain, Base) | yes — single strike, single weight (negative) | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| short_put | 1 | piecewise-linear, concave below strike | short-vol (directional bullish) | live (Ethereum, Unichain, Base) | yes — single strike, single weight (negative) | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| long_straddle | 2 | piecewise-linear, convex (V-shape at strike) | long-vol | live (Ethereum, Unichain, Base) | yes — two coincident strikes, equal weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| long_strangle | 2 | piecewise-linear, convex (flat between strikes) | long-vol | live (Ethereum, Unichain, Base) | yes — two separated strikes, equal weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| call_spread | 2 | piecewise-linear, bounded | directional bullish (mixed-vol) | live (Ethereum, Unichain, Base) | yes — two strikes, one long one short | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| put_spread | 2 | piecewise-linear, bounded | directional bearish (mixed-vol) | live (Ethereum, Unichain, Base) | yes — two strikes, one long one short | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| call_calendar_spread | 2 | mixed (path-dependent on timescale) | short-vol | live (Ethereum, Unichain, Base) | no — payoff depends on timescale, not strikes alone; no deterministic strike-ladder | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| diagonal_spread | 2 | mixed (path-dependent on timescale + strike) | directional bullish (mixed) | live (Ethereum, Unichain, Base) | no — timescale is the second axis, not a strike | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| jade_lizard | 3 | piecewise-linear, asymmetric (capped upside, unlimited downside) | short-vol | live (Ethereum, Unichain, Base) | yes — three strikes (one short put, one short call, one long call), three weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| big_lizard | 3 | piecewise-linear, asymmetric | short-vol | live (Ethereum, Unichain, Base) | yes — three strikes, three weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| super_bull | 3 | piecewise-linear, asymmetric | directional bullish | live (Ethereum, Unichain, Base) | yes — three strikes, three weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| super_bear | 3 | piecewise-linear, asymmetric | directional bearish | live (Ethereum, Unichain, Base) | yes — three strikes, three weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| call_ratio_spread | 3 | piecewise-linear (ratio-asymmetric) | mixed | live (Ethereum, Unichain, Base) | yes — three strikes; weights are non-unit ratios | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| zebra | 3 | piecewise-linear, leveraged-replication | directional bullish (mixed-vol) | live (Ethereum, Unichain, Base) | yes — three strikes with documented 2:1 ratio weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| iron_condor | 4 | piecewise-linear, symmetric (flat middle, capped wings) | short-vol | live (Ethereum, Unichain, Base) | yes — four strikes, four weights (sign-alternating) | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| iron_butterfly | 4 | piecewise-linear, symmetric (peak at center) | short-vol | live (Ethereum, Unichain, Base) | yes — four strikes (two coincident at the body) | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| bats | 4 | piecewise-linear, asymmetric | short-vol | live (Ethereum, Unichain, Base) | yes — four strikes, four weights | https://panoptic.xyz/research/essential-options-strategies-to-know | 2026-05-11 |
| zeehbs | 6 | piecewise-linear, leveraged-strangle replica | long-vol | constructible only as multi-position bundle (exceeds 4-leg SFPM ceiling) | yes — six strikes, six weights, but emit must span ≥2 SFPM positions | https://panoptic.xyz/research/essential-options-strategies-to-know · https://panoptic.xyz/docs/contracts/smart-contracts-overview | 2026-05-11 |

## §3 Strip-emit-eligibility summary

Per master-spec §2.1 HALT-trigger #1, a primitive admits a strip-emit iff its payoff is fully specified by a finite, deterministic tuple of strikes and weights — i.e., the payoff at any underlying price is reconstructible from `{(K_i, w_i)}_{i=1..n}` without reference to time-of-entry or per-leg timescale parameters.

**Admit strip-emit (deterministic strike-ladder + weight vector exists):**
`long_call`, `long_put`, `short_call`, `short_put`, `long_straddle`, `long_strangle`, `call_spread`, `put_spread`, `jade_lizard`, `big_lizard`, `super_bull`, `super_bear`, `call_ratio_spread`, `zebra`, `iron_condor`, `iron_butterfly`, `bats`, `zeehbs` (subject to the 4-leg SFPM caveat: a single `zeehbs` emit must produce ≥2 SFPM-position payload entries).

**Do NOT admit strip-emit (HALT candidates):**
- `call_calendar_spread` — payoff depends on two *timescales* (short-term short leg, longer-term long leg), not on two strikes; a `{(K_i, w_i)}` tuple cannot capture the time-axis asymmetry. Rationale: Panoptic Timescales are a per-leg width parameter that determines streamia accrual range, not a strike.
- `diagonal_spread` — same time-axis issue as the calendar spread, compounded with a strike offset; the payoff surface is two-dimensional in (strike, timescale) and not reducible to a one-dimensional strike ladder.

Two non-primitive mechanisms appear in Panoptic but are out of scope for the strip-emit table because they are not standalone payoff objects:
- **Streamia** — funding-rate mechanism applied to every position; modifies cashflow timing of any primitive above but produces no independent payoff.
- **Timescales** — per-position width parameter (1H, 1D, 1W, 1M, 1Y presets) that fixes the streamia-accrual range; not a primitive.

## §4 References

- Panoptic. "18 Options Strategies Every Trader Should Know (With Emojis)." Research. https://panoptic.xyz/research/essential-options-strategies-to-know — accessed 2026-05-11.
- Panoptic Docs. "Streamia." https://panoptic.xyz/docs/product/streamia — accessed 2026-05-11.
- Panoptic Docs. "Timescales." https://panoptic.xyz/docs/product/timescales — accessed 2026-05-11.
- Panoptic Docs. "Smart Contracts Overview." https://panoptic.xyz/docs/contracts/smart-contracts-overview — accessed 2026-05-11. (Source for the 4-leg SFPM ceiling.)
- Panoptic Blog. "Panoptic: Your Next DeFi Alpha" (dated 2025-07-25). https://panoptic.xyz/blog/panoptic-your-next-defi-alpha — accessed 2026-05-11. (Source for live-on-Ethereum/Unichain/Base status and cumulative volume figure.)

## §5 Filtered candidate set

**Filter rule (rule-driven, anti-fishing).** A row from §2 enters this set iff it satisfies BOTH of the following predicates simultaneously:

1. `admits_strip_emit = yes` (deterministic `{(K_i, w_i)}` tuple exists, per §3).
2. `convexity_class != "short-vol"` (LP side `a_l` is structurally LONG variance per PRIMITIVES.md §3; pairing a short-vol primitive with a long-vol LP collapses the hedge convexity sign).

The reverse-IC baseline is a special case: the `iron_condor` row in §2 is classed `short-vol` under the *standard* (debit-paid) leg orientation, but the cohort_5_strip baseline uses the LONG-vol leg orientation (credit-collected wings flipped to debit-paid wings — see `simulations/saas_builder/__init__.py` package docstring describing the cohort-5 strip as a long-vol Carr-Madan 3-condor). Under the cohort_5_strip's reverse-IC orientation the convexity class becomes long-vol, so it qualifies. It is listed below as the explicit baseline.

**Rows filtered OUT and why** (recorded for auditability — these are NOT candidates):
- `short_call`, `short_put`, `call_calendar_spread`, `diagonal_spread`, `jade_lizard`, `big_lizard`, `iron_butterfly`, `bats` — fail one or both predicates: short-vol classification (per §2), or no strip-emit (calendar/diagonal per §3), or both.
- `iron_condor` in its *standard* (short-vol) orientation fails predicate 2; it re-enters only under the reverse-IC long-vol orientation as the baseline anchor.

**Candidate set (rule-pass rows; not pre-ranked, per anti-fishing):**

| primitive_id | role | one-line rationale (strip-emit eligibility · convexity-class qualification) |
|---|---|---|
| reverse_iron_condor (cohort_5_strip) | BASELINE — comparison anchor | Strip-emit eligible: four strikes, four sign-alternating weights, same SFPM 4-leg footprint as standard IC. Convexity qualification: cohort_5_strip flips the credit-wings → debit-wings leg orientation, producing a long-vol Carr-Madan 3-condor (per `simulations/saas_builder/__init__.py` package docstring); long-vol qualifies. |
| long_call | candidate | Strip-emit eligible: trivial single-strike, single-weight ladder. Convexity qualification: classed long-vol (directional bullish, convex above strike) in §2 — not short-vol. |
| long_put | candidate | Strip-emit eligible: trivial single-strike, single-weight ladder. Convexity qualification: classed long-vol (directional bearish, convex below strike) in §2 — not short-vol. |
| long_straddle | candidate | Strip-emit eligible: two coincident strikes, equal weights. Convexity qualification: classed long-vol in §2 — pure long-vol, not short-vol. |
| long_strangle | candidate | Strip-emit eligible: two separated strikes, equal weights. Convexity qualification: classed long-vol in §2 — pure long-vol, not short-vol. |
| call_spread | candidate | Strip-emit eligible: two strikes, one long / one short weight pair. Convexity qualification: classed mixed-vol (directional bullish) in §2 — not pure short-vol, so predicate 2 (`!= "short-vol"`) passes literally. |
| put_spread | candidate | Strip-emit eligible: two strikes, one long / one short weight pair. Convexity qualification: classed mixed-vol (directional bearish) in §2 — not pure short-vol; predicate 2 passes. |
| super_bull | candidate | Strip-emit eligible: three strikes, three weights. Convexity qualification: classed directional bullish in §2 — not short-vol; predicate 2 passes. |
| super_bear | candidate | Strip-emit eligible: three strikes, three weights. Convexity qualification: classed directional bearish in §2 — not short-vol; predicate 2 passes. |
| call_ratio_spread | candidate | Strip-emit eligible: three strikes with non-unit ratio weights. Convexity qualification: classed mixed in §2 — not short-vol; predicate 2 passes. |
| zebra | candidate | Strip-emit eligible: three strikes with documented 2:1 ratio weights. Convexity qualification: classed mixed-vol (directional bullish) in §2 — not short-vol; predicate 2 passes. |
| zeehbs | candidate (with caveat) | Strip-emit eligible: six strikes, six weights — BUT emit payload must span ≥2 SFPM positions because 6 > 4-leg SFPM ceiling (§2 on-chain_liquidity column). Convexity qualification: classed long-vol in §2 — qualifies. |

**Count after filter:** 11 candidates + 1 baseline = 12 rows. This exceeds the plan's expected "2–4" upper bound. Per anti-fishing, no primitive is excluded for any reason other than failing the filter rule, so the full rule-pass list is reported here. Phase 2 numerical evaluation (and Phase 3 ranking) will narrow the set; that narrowing is NOT performed in this section.
