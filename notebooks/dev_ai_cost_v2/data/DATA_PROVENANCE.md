# DATA_PROVENANCE — `dev_ai_cost_v2` panel

Spec: `docs/specs/2026-05-16-ai-cost-factor-model-design.md` v0.2.4 §5.4.

## Build date
2026-05-17

## Repo state at build time
- Branch: `iter/ai-cost-2026-05`
- HEAD: `07f907fc181b8118dbadf311f680be2ea58df3ae` (v0.2.4 Y-7 tests)
- Spec version: 0.2.4
- Plan version: 2026-05-16 plan (17 tasks; Task 10 = this build)

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
| Daily notional cost panel | `data/panels/notional_cost_panel.parquet` | `32383d5b8b1530c775690f74b158c51eb9ee13db333994342b57604c371d7bc4` |

### Panel shape
- Rows: **29** (one row per weekday-UTC date with recorded Claude Code usage that joins against TRM)
- Columns (11): `date_utc, notional_cost_usd, notional_cost_cop, trm_cop_per_usd, input_tok, output_tok, cache_create_5m, cache_create_1h, cache_read, n_messages, ephemeral_pi_share`
- Date window observed: **2026-01-06 → 2026-05-14**
- Total notional cost USD: **$5,903.87**
- Total notional cost COP: **$21,689,298**
- Total messages: **46,264**

### Anti-fishing N-floor check
Spec §2.3 / §7 N_MIN = 75 weekday days. **Observed N = 29** → **expected power-HALT at Task 11** per CORRECTIONS-U (already anticipated; disposition template pre-staged at `notebooks/dev_ai_cost_v2/dispositions/power_halt_template.md`).

## Counter audit (v0.2.4 — 7 counters + π̂)

| Counter | Source tier | Value | Interpretation |
|---|---|---|---|
| `dropped_rows_count` | panel_builder (weekday-join drops) | 23,216 | Messages on non-weekday calendar dates (operator works weekends) |
| `dropped_error_count` | panel_builder (`is_error=True`) | 74 | API-error rows excluded from cost aggregation (CORRECTIONS-V) |
| `dropped_non_assistant_count` | JSONLReader (Y-5a / Y-1) | 134,102 | JSONL rows where `type != "assistant"` (user/system/summary lines) |
| `dropped_malformed_line_count` | JSONLReader (Y-7) | **1** | The trailing-null-byte block in `agent-af5e1160f7be358ba.jsonl` that triggered the v0.2.3 → v0.2.4 amendment |
| `WARN_missing_keys_count` | PricingTable (Y-5a / Y-3) | 6 | claude-* models in LiteLLM SHA pin missing one or more rate keys (e.g., `claude-sonnet-4-5`, `claude-sonnet-4-6` lack `cache_creation_input_token_cost_above_1hr`) |
| `dropped_unknown_model_count` | PricingTable (Y-5a) | 136 | Messages whose model name had no entry after the exact / `anthropic/` / longest-substring ladder (likely test sessions with `model: "claude-3"` shorthand or sentinel values) |
| `multiple_substring_match_warning` | PricingTable (Y-5d) | 0 | Alphabetical-tiebreaker never invoked (longest-substring matches were unique in this corpus) |
| `ephemeral_pi_share` (Y-6) | DailyNotionalPanel scalar | **0.418827** | 41.9% of cache-creation tokens are 1h-tier ephemeral. Cost magnitudes here apply 5m rate to total cache-creation; true cost is up to `1 + π̂·(rate_1h/rate_5m − 1) ≈ 1.42×` higher (rate_1h ≈ 2·rate_5m). FX-share point estimate (variance-based) is unaffected. |

## Project-root scope

`/home/jmsbpp/.claude/projects/` — 1,732 JSONL files across all top-level project directories. No allow-list / deny-list filter applied at this stage (subscription-as-proxy framing per §1.2 treats all sessions as equally representative of the single-developer pilot's pattern).

## Known v0.2.4 amendments captured in this build

- **Y-7 (line-level malformed-skip)**: trailing-null-byte block at `agent-af5e1160f7be358ba.jsonl:586` skipped silently → `dropped_malformed_line_count = 1`. Pre-v0.2.4 this raised `JSONLSchemaError`.
- All 6 CR-Z architectural pins (v0.2.3) active.
- All 4 Y-1/Y-2/Y-3/Y-4 OSS-mirror amendments (v0.2.2) active.

## Deferred to v0.2.5 (per spec §0.4)

- Quantitative hard-fail threshold on `dropped_malformed_line_count / total_lines` (RC FLAG-5a). First baseline empirically established by this build: `1 / 134,102 = 7.5e-6`.
- DATA_PROVENANCE schema pin for Y-7's new counter (this document instantiates the freeform shape; v0.2.5 to formalize).
- ccusage-parity oracle activation pending real PII-redacted fixture replacing the synthetic one at `simulations/tests/fixtures/real_claude_jsonl/synthetic_sample.jsonl`.
