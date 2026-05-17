# DATA_PROVENANCE — `dev_ai_cost_v2` panel

Spec: `docs/specs/2026-05-16-ai-cost-factor-model-design.md` v0.2.5 §5.4.

## Build date
2026-05-17 (v0.2.5 Y-8 refresh)

## Repo state at build time
- Branch: `iter/ai-cost-2026-05`
- HEAD: `08249b2c5638622821dad5e3be9d585cc7527a5a` (v0.2.5 Y-8 tests; dedup landed)
- Spec version: 0.2.5
- Plan version: 2026-05-16 plan (17 tasks; Task 10 = this build, refreshed post-Y-8)

## Pinned external sources

| Source | Pin | SHA / hash |
|---|---|---|
| LiteLLM `model_prices_and_context_window.json` | commit SHA `e58a561caa21169fb02174148444c08509ce7028` | sha256 `05b050523e4c71581a12605c4bc49cf7049bafe3f51e1506b9da61afb9791db9` |
| Banrep daily TRM panel | Datos Abiertos Socrata (TRM oficial COP/USD), pulled 2026-05-17 | sha256 `4bf90ff093eb553659b23856974db965a0713446fceb28be2006d0c350432fe0` |
| Anthropic Claude Code session logs | local `~/.claude/projects/**/*.jsonl` at build time | (not hashed — operator-private; rooted by `--projects-root`) |

## CLI invocation

```
uv run python scripts/build_notional_cost_panel.py \
    --since 2024-01-01 \
    --until 2026-05-17
```

## Output

| Artifact | Path | Sha256 |
|---|---|---|
| Daily notional cost panel | `data/panels/notional_cost_panel.parquet` | `c002df3b42042bf7db37499482486d1548a72f45bea8ff58d14569fb72d6b6ff` |

### Panel shape (v0.2.5 Y-8 dedup applied)
- Rows: **29** (one row per weekday-UTC date with recorded Claude Code usage that joins against TRM)
- Columns (11): `date_utc, notional_cost_usd, notional_cost_cop, trm_cop_per_usd, input_tok, output_tok, cache_create_5m, cache_create_1h, cache_read, n_messages, ephemeral_pi_share`
- Date window observed: **2026-01-06 → 2026-05-14**

### ccusage parity verdict (apples-to-apples 27-weekday overlap)
- **cost ratio: 0.9994 (within ±0.1%, v0.2.2 CORRECTIONS-Y-2 / Y-4 target MET)**
- input_tok: 1.0125; output_tok: 0.9936; cache_create: 1.0008; cache_read: 1.0010 (all within ±1.3%)
- Reference: ccusage v19.0.3, `daily --since 20240101 --until 20260517 --json`

### Anti-fishing N-floor check
Spec §2.3 / §7 N_MIN = 75 weekday days. **Observed N = 29** → **expected power-HALT at Task 11** per CORRECTIONS-U (already anticipated; disposition template pre-staged at `notebooks/dev_ai_cost_v2/dispositions/power_halt_template.md`).

## Counter audit (v0.2.5 — 8 counters + π̂)

| Counter | Source tier | Value | Interpretation |
|---|---|---|---|
| `dropped_rows_count` | panel_builder (weekday-join drops) | 11,901 | Messages on non-weekday calendar dates (operator works weekends) |
| `dropped_error_count` | panel_builder (`is_error=True`) | 73 | API-error rows excluded from cost aggregation (CORRECTIONS-V) |
| `dropped_non_assistant_count` | JSONLReader (Y-5a / Y-1) | 134,514 | JSONL rows where `type != "assistant"` (user/system/summary lines) |
| `dropped_malformed_line_count` | JSONLReader (Y-7) | **1** | The trailing-null-byte block in `agent-af5e1160f7be358ba.jsonl` that triggered the v0.2.3 → v0.2.4 amendment |
| `dropped_duplicate_count` | JSONLReader (Y-8) | **42,387** | Streaming-chunk / iteration duplicates by `${message.id}:${requestId}`; ccusage-mirror keep-larger-tokenTotal + hasSpeed-tiebreaker. ~63% of raw assistant rows were duplicates (the root cause of pre-v0.2.5's 2.11× cost overcount). |
| `WARN_missing_keys_count` | PricingTable (Y-5a / Y-3) | 6 | claude-* models in LiteLLM SHA pin missing one or more rate keys (e.g., `claude-sonnet-4-5`, `claude-sonnet-4-6` lack `cache_creation_input_token_cost_above_1hr`) |
| `dropped_unknown_model_count` | PricingTable (Y-5a) | 136 | Messages whose model name had no entry after the exact / `anthropic/` / longest-substring ladder (likely test sessions with `model: "claude-3"` shorthand or sentinel values) |
| `multiple_substring_match_warning` | PricingTable (Y-5d) | 0 | Alphabetical-tiebreaker never invoked (longest-substring matches were unique in this corpus) |
| `ephemeral_pi_share` (Y-6) | DailyNotionalPanel scalar | **0.398977** | 39.9% of cache-creation tokens are 1h-tier ephemeral. Cost magnitudes here apply 5m rate to total cache-creation; true cost is up to `1 + π̂·(rate_1h/rate_5m − 1) ≈ 1.40×` higher (rate_1h ≈ 2·rate_5m). FX-share point estimate (variance-based) is unaffected. |

## Project-root scope

`/home/jmsbpp/.claude/projects/` — 1,732 JSONL files across all top-level project directories. No allow-list / deny-list filter applied at this stage (subscription-as-proxy framing per §1.2 treats all sessions as equally representative of the single-developer pilot's pattern).

## Known amendments captured in this build

- **Y-8 (uniqueHash dedup, v0.2.5)**: OSS-mirror dedup by `${message.id}:${requestId}` with keep-larger-tokenTotal + hasSpeed-tiebreaker → 42,387 duplicates skipped (~63% of raw assistant rows). Pre-v0.2.5 this caused 2.11× cost overcount vs ccusage; post-v0.2.5 cost is 0.9994× ccusage.
- **Y-7 (line-level malformed-skip, v0.2.4)**: trailing-null-byte block at `agent-af5e1160f7be358ba.jsonl:586` skipped silently → `dropped_malformed_line_count = 1`. Pre-v0.2.4 this raised `JSONLSchemaError`.
- All 6 CR-Z architectural pins (v0.2.3) active.
- All 4 Y-1/Y-2/Y-3/Y-4 OSS-mirror amendments (v0.2.2) active.

## Deferred (per spec §0.5 Y-9 backlog)

- **Y-9 (v0.2.6 candidate)**: residual ~1.3% input_tok overshoot + ~0.6-0.7% spreads on output/cc/cr post-dedup. Investigate (a) `usage.iterations[i]` aggregation, (b) `dropped_unknown_model_count=136` rows ccusage prices via fallback we drop, (c) `hasSpeed` tiebreaker edge cases.
- Quantitative hard-fail threshold on `dropped_malformed_line_count / total_lines` (v0.2.4 RC FLAG-5a). First baseline empirically established: `1 / 134,514 = 7.4e-6`.
- DATA_PROVENANCE schema pin for Y-7's counter (this document instantiates the freeform shape; v0.2.6+ to formalize).
- ccusage-parity oracle activation pending real PII-redacted fixture replacing the synthetic one at `simulations/tests/fixtures/real_claude_jsonl/synthetic_sample.jsonl`.
