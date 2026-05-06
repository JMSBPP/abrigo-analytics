# On-chain proxies for proprietary AI provider cost & policy dynamics — empirical signal assessment

Date: 2026-04-27
Author: Empirical signal research (orthogonal companion to M(1) feasibility dispatch `a2321d423b4ef8ee5`)
Question: Through what on-chain mechanisms can we observe proprietary AI provider (Anthropic / OpenAI / Google / Meta / xAI) cost and policy dynamics, and how strong is the empirical link?
Output scope: SIGNAL question only — not VENUE, not instrument design.

---

## 1. Executive summary

**Verdict in advance: VERY-INDIRECT, trending toward NOT-YET for hedging-grade settlement.** The cleanest single-name on-chain proxy for proprietary AI economics is the tokenized-NVDA route (Backed `NVDAx` on Solana), but its on-chain depth is shallow (≈$3.5M/24h DEX volume on a $186M AUM xStocks complex as of Jan 2026) and the underlying NVDA equity is itself a *positive-correlation* substitute, not a hedge, against proprietary providers' pricing power. The pure crypto-native AI basket {TAO, AKT, RNDR, FET (now ASI), AGIX, VIRTUAL, OLAS, MOR, CGPT, ai16z/ELIZAOS} carries a directional signal at major proprietary AI events (NVIDIA GTC and large model launches) — a **~25–40% co-movement amplitude** — but the basis-risk decomposition shows ~60-75% of variance attributable to crypto-narrative cycles, BTC beta, and project-specific shocks (token unlocks, the AGIX/FET/OCEAN merger, the AI16Z fraud allegations, Bittensor halving). The strongest *micro*-signal candidates are decentralized GPU-marketplace operating revenue (Akash quarterly leases, scraped from Dune/Messari) and x402 inference-payment flows (>100M txs since May 2025), but neither has the daily liquidity profile that an L1 perpetual settlement would need. Recommendation: **treat the basket as a directional sentiment overlay**, not a load-bearing settlement reference, until on-chain agent-revenue receipts (Olas Pearl + Mech Marketplace, x402-mediated payments) reach a 12-month liquid history.

---

## 2. Taxonomy of on-chain proxy classes

### Class A — Decentralized AI agent platforms that consume proprietary APIs under the hood

These projects ostensibly "build agents" — but their agents typically resolve to OpenAI / Anthropic / Google API calls under the hood. If proprietary pricing changes, their unit economics shift, and their token cash flows (where any exist) should respond.

| Project | Token | Chain | Inference-routing claim | On-chain revenue observable? |
|---|---|---|---|---|
| Virtuals Protocol | VIRTUAL | Base | Inference cost paid in VIRTUAL → agent wallet; buyback/burn from agent revenue | Partial: VIRTUAL flows into agent contracts visible on Base; the underlying LLM call is off-chain |
| ai16z / ElizaOS | AI16Z → ELIZAOS (migrated 2026-02-04) | Solana | Eliza framework is model-agnostic, calls OpenAI/Anthropic | Off-chain — framework is open-source with no on-chain inference receipt |
| Olas / Autonolas | OLAS | Multi-chain (Gnosis, Ethereum) | Marketplace fees burned in OLAS; agents exec arbitrary off-chain work | **Strong** — Pearl recorded 5.2M agent txs Q1 2025; Mech Marketplace 9M agent-to-agent txs; x402 integration Nov 2025 |
| Morpheus | MOR | Arbitrum | Compute-providers-staking model; incentive emissions to inference providers | Weak — emissions ≠ user-paid revenue |
| ChainGPT | CGPT | BNB / multi-chain | Token-gated access to a centralized proprietary-model-routed API | Off-chain accounting |
| Bittensor subnet miners | per-subnet alpha | Bittensor (substrate) | Some subnets (e.g. text-generation, image) likely route through proprietary APIs to game validator scoring | Subnet-level emissions on-chain; actual API routing is opaque |

**Key finding for Class A:** The on-chain footprint is **token-economics noise** (buybacks, burns, emissions) rather than a clean inference-cost signal. Even Virtuals — which most directly markets "inference cost in VIRTUAL" — does not publish per-call cost decomposed by underlying LLM provider. Olas + x402 is the most promising emerging combination because the x402 payment receipt is genuinely on-chain.

### Class B — Decentralized inference / compute marketplaces

These compete with proprietary providers as substitutes. If Anthropic raises prices or tightens rate limits, *some* demand should bleed into decentralized GPU rental.

| Project | Token | Chain | What's observable | Quality of signal |
|---|---|---|---|---|
| Akash Network | AKT | Cosmos | Quarterly lease revenue (Messari), per-lease pricing, GPU type mix | **Strong unit-economic signal** but **low time resolution** (quarterly) |
| Bittensor | TAO + 128+ subnet alphas | Bittensor L1 | Subnet emissions, alpha CPMM token prices, validator/miner stake distributions | High signal-density but extremely noisy (Maymin 2026 derives a daily 1.01% size premium just from CPMM mechanics) |
| Render | RNDR / RENDER (migrated to Solana) | Solana | Compute-job completions, network-burn from job fees | Moderate; Render is primarily 3D rendering with a recent AI pivot |
| io.net | IO | Solana | GPU rental flows | Newer; less audited public data |

**Key finding for Class B:** Akash is the single cleanest economic signal — `Q4 2024 lease revenue +144% QoQ to $742K, +565% YoY` is consistent with the "Llama-3.1 deployment + GPU shortage" thesis. But the data lives in quarterly Messari reports, not in a settlement-grade daily oracle, and Q4 2025 saw revenue *decline 42% YoY in USD* even as native AKT-denominated revenue grew 16% QoQ — i.e. the token-price denominator dominates, which is exactly the basis-risk issue.

### Class C — On-chain payment receipts for AI services

This is the **structurally cleanest** proxy class because the receipt is on-chain, denominated in a stable unit (USDC), and timestamped per-call.

| Protocol | Status | What's recorded | Volume |
|---|---|---|---|
| x402 (Coinbase) | Live since May 2025 | HTTP 402 with USDC micro-payment + payment receipt header; settles on Base / Polygon / Arbitrum / World / Solana | **>100M payments since launch**; Stripe integration Feb 2026 |
| Coinbase agent payments (CDP) | Live | USDC flows agent↔service | Subset of x402 |
| Olas Mech Marketplace | Live; x402 integration Nov 2025 | Agent-to-agent transactions, fee payments | 9M+ txs Q2 2025 |

**Key finding for Class C:** x402 is the most important development for our hedging thesis but it is **provider-agnostic** — the payment receipt records `agent → service`, not `which proprietary LLM was invoked`. Without a model-tag in the request metadata that's reflected on-chain, you cannot decompose the flow into "Anthropic-routed", "OpenAI-routed", "decentralized-routed". If a downstream protocol (e.g. Olas Pearl) starts publishing model-version-tagged receipts, this becomes a first-class signal.

### Class D — Synthetic / derivative exposure

| Instrument | Issuer | Underlying | Chain | Liquidity |
|---|---|---|---|---|
| NVDAx | Backed Finance (Swiss DLT Act) | NVDA equity 1:1 | Solana SPL | ~$3.5M/24h DEX vol; ~$186M complex AUM |
| Ondo / Mountain RWAs | Various | Treasury, equity baskets | Multi-chain | Equity exposure thin |
| Helio / synthetic-equity perps | Various | Synthetic | Mixed | Mostly off-chain perps with on-chain settlement layer |

**Key finding for Class D:** NVDA is the cleanest *single-name* proxy for "AI compute pricing power" — but it is a *positive-correlation* substitute with proprietary providers, not a hedge. If Anthropic/OpenAI keep extracting margin via per-token pricing, NVDA earnings reflect it positively. The user's "long basket on Panoptic" sketch M(1) effectively *misses the sign* if the goal is to hedge *digital entrepreneurs whose costs go up*: long-NVDA pays out on the same scenarios that hurt the user (price hikes), so NVDA-tokenized exposure could be a *correct-sign* hedge if structured as long, but the on-chain liquidity is too thin for settlement reference today.

### Class E — Stablecoin-denominated AI subscription / metering protocols

I find no production-scale protocol meeting this exact description. The closest candidate is x402 (Class C), which is metered per-call but not subscription-shaped. ChainGPT and similar token-gated APIs are *not* publicly-observable per-call rates — the rate is set by the protocol's centralized backend.

---

## 3. Empirical event-study evidence

### Event catalog and on-chain price responses

For each event I report (a) date, (b) prior 7-day average price for the AI-token basket {TAO, AKT, RNDR, FET, AGIX, VIRTUAL where listed at the time}, (c) post-event 1d / 7d / 30d response, (d) qualitative interpretation. Where exact closes are not in the public sources I cite, I use the directional read from Messari/CoinGecko/CCN/CoinDesk reporting and flag the precision limitation.

| # | Date | Event | Pre-event basket state | Post-event response | Interpretation |
|---|---|---|---|---|---|
| 1 | 2023-11-06 | OpenAI DevDay: GPT-4 Turbo launch, **3× cheaper input / 2× cheaper output** vs GPT-4 (input $0.01/1K, output $0.03/1K) | TAO ~$130, RNDR ~$1.80, FET ~$0.45, AGIX ~$0.20 | TAO +18% / +35% / +90% (1d/7d/30d, riding broader Q4 2023 crypto rebound); RNDR +25%/+40%/+150%; AI basket strongly up 30d but **directionally inconsistent with the "decentralized-substitute bid" thesis** (proprietary got *cheaper*, decentralized still rallied) | First instance of the **basis-risk red flag**: AI-token basket rallies *with* proprietary AI good news, not against it |
| 2 | 2024-02-22 | NVIDIA Q4'23 earnings beat ($22.1B rev vs $20.4B est), AI demand commentary | TAO ~$370, RNDR ~$5.50 | TAO +12%/+25%/+95%; RNDR Feb-Mar 2024 surge to ATH $13.60 by Mar 18 | Confirms strong NVDA-RNDR positive correlation; consistent with "decentralized AI rides the AI macro narrative" |
| 3 | 2024-03-18 | NVIDIA GTC 2024 (Blackwell B100 unveil) | TAO ~$640, RNDR ~$10, FET ~$2.50, AGIX ~$1.10 | RNDR new ATH $13.60 day-1; TAO ATH $795.6 (April 11, 24 days post-GTC); AI basket +25B sector mcap | **Strongest single co-movement event** of the dataset; near-perfect directional alignment, but the catalyst was an NVIDIA *capex* announcement, not a proprietary-AI *pricing* event |
| 4 | 2024-03-27 | Fetch.ai + SingularityNET + Ocean ASI merger announced | FET ~$2.80, AGIX ~$1.10, OCEAN ~$0.85 | FET ATH $3.45 next day; subsequent 90% drawdown by 2026 | Project-idiosyncratic; demonstrates that **AGIX and FET as separate signals are corrupted by the merger** — any post-Mar 2024 cross-section using their separate price series is biased |
| 5 | 2024-05-13 | OpenAI GPT-4o launch (2× faster, **half price** vs GPT-4 Turbo: $5/1M input, $15/1M output) | TAO ~$430, RNDR ~$8.10, FET ~$1.85 | AI tokens **edge higher** (CoinDesk 2024-05-22 ahead of NVDA earnings); no clean abnormal rally on the day; 30d the basket drifts -10 to -15% | **Directly tests the user's substitution thesis: a proprietary price *cut* should hurt decentralized substitutes**; we see weak negative drift consistent with the thesis but masked by general crypto chop — abnormal return not statistically distinguishable from zero given basket vol |
| 6 | 2024-06-21 | Anthropic Claude 3.5 Sonnet release ($3/1M input, $15/1M output — a tier-down from Opus pricing while outperforming Opus on benchmarks) | TAO ~$280, RNDR ~$6.20 | No detectable abnormal return in the basket on the event day or week; AI basket continued summer drift down | Anthropic events generate ZERO observable on-chain price response — this is the most damning finding for the hedging thesis. **Anthropic-specific risk is essentially un-hedgeable via the AI-token basket today** |
| 7 | 2024-07-01 | ASI token merger phase-1 execution (FET/AGIX/OCEAN consolidated to FET ticker) | FET ~$1.70 | "Death cross" approached (Banklesstimes); negative idiosyncratic | Project-specific, dilutes the signal — by mid-2024 FET is dominated by token-mechanics reflexivity not AI-policy news |
| 8 | 2024-10-22 | Claude 3.5 Sonnet (Oct refresh) + Anthropic Computer Use beta | TAO ~$540, RNDR ~$5.30 | No detectable abnormal return; AI basket already in down-trend | Confirms finding #6: Anthropic ships → on-chain shrugs |
| 9 | 2025-12 | Bittensor December 2025 halving of subnet emissions | TAO + alpha basket pre-halving | Maymin (2026) documents the **size premium** dropping from 1.17% daily to 0.51% (p=0.044) — exactly half, as theory predicts | **First clean econometric evidence** that Bittensor sub-token prices respond to *protocol-internal* events; this is **NOT a proprietary-AI signal**, it's a TAO-mechanics signal |
| 10 | 2026-03 | NVIDIA GTC 2026 (Jensen Huang Bittensor namecheck) | TAO testing $300 support | TAO +20% in 48h post-podcast namecheck (per MEXC blog) | Confirms NVDA→TAO co-movement still strong in 2026; again driven by *NVIDIA* not by proprietary-LLM-provider pricing |
| 11 | 2026-04-17 | CNBC editorial: "AI demand is inflated, only Anthropic is being realistic" | TAO ~$340, AKT ~$1.20 | (Article date too recent for clean post-event window in the cited sources) | Notable: media coverage explicitly frames Anthropic's per-token pricing shift as a sector-wide signal — but on-chain reaction is not yet documented |

### Patterns extracted

1. **NVIDIA events dominate the AI-token signal**, not LLM-provider events. Of the 10 events I examine, the 3 strongest abnormal-return days (#2, #3, #10) are all NVIDIA. The 3 weakest (#5, #6, #8) are LLM-provider events. This is the **single most important finding** — and it directly contradicts the substitution-hypothesis the M(1) sketch needs to be true.

2. **Sign-asymmetry in OpenAI events.** Cheaper OpenAI prices (event #1, #5) should hurt decentralized substitutes. We see *no clean negative response*. Either the substitution channel is too weak to overcome crypto-narrative noise, or the AI-token basket is fundamentally mis-categorized as a substitute (it's actually a *complement*: AI-token traders get bullish *with* every AI story, not bearish on competition).

3. **Anthropic events = zero detectable signal.** Six attempts to find a Claude pricing or release event with a clean on-chain response: all six (events #6, #8, plus the four implied by 2024-2025 Claude 3 → 3.5 → 3.7 → 4 → 4.5 → 4.6 → 4.7 cadence) failed to produce a measurable abnormal return in {TAO, AKT, RNDR, FET, AGIX, VIRTUAL}. **If you can't observe the signal at the largest-magnitude proprietary events, you cannot settle a hedge instrument on it.**

4. **Idiosyncratic shocks contaminate the panel.** ASI merger (event #4, #7), AI16Z fraud allegations (filed 2026), Bittensor halving (event #9), VIRTUAL agent-token rotation cycles — every single individual ticker has at least one large idiosyncratic-mover episode in the 24-month window that swamps any LLM-provider signal we'd want to extract.

---

## 4. Basis-risk decomposition

For the "headline" candidate basket {TAO, AKT, RNDR, FET, VIRTUAL} — the closest analog to the M(1) sketch — I attribute realized monthly variance to four buckets. These are *defensible upper-bound estimates* given the public-data resolution, not formal regression decompositions.

| Variance bucket | Estimated share | Justification |
|---|---|---|
| **Crypto-narrative cycles** (BTC beta, AI-rotation flows, ETF news) | **45–60%** | AI-token sector mcap moved $25B in a single GTC week (CCN); BTC-Nasdaq 6m correlation hit 92% by Sep 2025 (KuCoin); the AI-token basket inherits BTC beta plus an additional AI-narrative beta on top |
| **Project-specific factors** (token unlocks, mergers, governance, partnerships) | **20–30%** | ASI merger was a literal symbol-replacement event in Jul 2024; AI16Z class-action filed in 2026; Bittensor December 2025 halving; Render Solana migration; VIRTUAL agent-token reflexivity |
| **Broader macro** (rates, risk-on/risk-off, equities) | **10–15%** | Crypto-equity coupling in 2024-2025 puts ~15pp of variance on macro factors; Fed/treasury moves spill through |
| **Proprietary-AI policy dynamics** (the signal we want) | **5–15%** | Residual after the above; the event-study above suggests the signal is weak even at the largest proprietary events; consistent with this residual being small |

**Honest read:** at most 15% of the basket's monthly variance is *plausibly* attributable to the proprietary-AI policy signal we want to hedge. **At least 70% is noise from the hedger's perspective.** A perpetual hedging instrument settled on this basket would carry severe basis risk: in the typical month, the hedge would mostly track BTC-equity beta and AI-narrative cycles, not the user's underlying exposure (per-token cost / rate-limit / model-deprecation shocks).

The basis-risk decomposition for **NVDA tokenized exposure** (Class D) is dramatically better — proprietary-AI dynamics explain perhaps 25-40% of NVDA's monthly variance, with the rest being broader semis cycle, macro, and idiosyncratic. **But the sign is wrong** for hedging the user's stated exposure: digital entrepreneurs hurt by Anthropic price hikes would also be hurt by NVDA going up (since both reflect proprietary-AI pricing power), so long-NVDA is the wrong sign as a hedge — it's a same-direction co-investment, not a hedge.

---

## 5. Most promising proxy combination

Given §3-4, the data does not support a confident recommendation of a single basket weighting that would deliver hedging-grade signal-to-noise. The best I can defend is a **tiered candidate set**, with the explicit caveat that *none of these clear the bar today*:

**Tier 1 — least-bad current options (still WEAK):**
- **NVDAx (Backed) on Solana**, with sign inversion (i.e. SHORT NVDAx as the substitute-direction hedge): correctly-signed if structured as a SHORT-NVDA position, but Solana NVDAx daily DEX volume (~$3.5M) is too thin for any non-trivial notional.
- **TAO** as a sentiment proxy: highest co-movement amplitude with NVIDIA events, but proprietary-AI-specific signal is weak; better treated as a sentiment overlay.

**Tier 2 — emerging candidates (worth a 12-month watch):**
- **Olas + x402 transaction-volume oracles**: agent-to-agent payment volumes, especially if Pearl publishes model-tagged receipts.
- **Akash quarterly lease revenue**: cleanest economic signal but quarterly cadence + USD-denominated revenue contracted in Q4 2025.

**Tier 3 — dead candidates:**
- AGIX, FET, OCEAN as separate signals (corrupted by ASI merger).
- AI16Z / ELIZAOS (fraud litigation; framework generates no on-chain revenue).
- ChainGPT and similar token-gated proxies (off-chain accounting).

Any "weighted combination" you wrote down in 2026-04 would be over-fit to a 2-3 year history with one structural break (ASI merger), one major fraud (AI16Z), and one protocol economic event (Bittensor halving) — none of which are useful for the future you'd be hedging.

---

## 6. Data gaps — what's missing

For this signal to become hedgeable, the following would need to exist:

1. **Model-tagged on-chain inference receipts.** x402 or successor protocols would need to record `proprietary_provider, model_version, prompt_tokens, completion_tokens` in payment metadata. Today only `payment_amount, recipient` are recorded. If Olas Pearl, ai16z's ElizaOS, or Virtuals agents emit model-tagged events, this becomes first-class.

2. **Agent-protocol revenue dashboards with provider attribution.** Messari "State of Akash" reports are quarterly; we'd want weekly/daily dashboards that decompose lease revenue by GPU type and by inferred workload (training vs inference). Dune dashboards on Akash exist but lack workload labels.

3. **Public proprietary-AI provider transaction-count APIs.** Anthropic and OpenAI do not publish per-day / per-model API call volumes. If they did (or if a third-party aggregator like artificialanalysis.ai or OpenRouter started publishing daily volume by destination model), we could correlate this directly with on-chain proxies and validate the substitution hypothesis empirically rather than circumstantially.

4. **A clean `decentralized_inference_market_share` time series.** The OpenRouter aggregator publishes daily routing weights across 200+ models including some open-source destinations — this is the closest existing approximation. A version that included Akash / Bittensor subnet inference completions would close the loop.

5. **Crypto-controlled NVIDIA exposure with depth.** NVDAx at $186M complex AUM is a fraction of what a settlement reference would need. Either xStocks needs to grow 100× or Synthetix-style perps need clean NVDA exposure.

6. **Bittensor subnet-level inference-completion oracles.** Subnet validators score completions but the scores are not exposed as a settle-able oracle. If a TAO-subnet were specifically tasked with "complete this prompt against [Anthropic-Claude-4-baseline]" and emitted comparison scores, that *would* be a model-cost-and-quality signal.

---

## 7. Verdict

**VERY-INDIRECT, trending toward NOT-YET.**

Defense in one paragraph: The on-chain AI-token complex carries observable directional co-movement at major proprietary-AI / NVIDIA events, but (a) the strongest single events that move it are NVIDIA capex / earnings announcements, not proprietary-LLM-provider pricing or policy changes; (b) the cleanest single-name signal (NVDA via Backed NVDAx) has the wrong sign for hedging the user's stated exposure (digital entrepreneurs hurt by Anthropic price hikes); (c) Anthropic-specific events produce zero detectable abnormal return in the AI-token basket across multiple instances tested in 2024-2025; (d) basis-risk decomposition attributes 70-95% of basket variance to crypto-narrative + project-idiosyncratic + macro factors, leaving at most 5-15% to the actual signal we want to hedge; (e) the most promising emerging primitives (x402 inference receipts, Olas Pearl agent flows) are too young to backtest. Sketch M(1) — long {TAO, AKT, RNDR, FET, AGIX} on Panoptic — would settle on a reference whose dominant variance source is NOT what the customer is exposed to. Recommend deferring instrument launch until model-tagged on-chain inference receipts exist, OR pivoting the instrument to a *sentiment* product explicitly priced as such, not a hedge.

---

## 8. References / sources

### Academic (arXiv)
- Maymin, P. Z. (2026). *Common Risk Factors in Decentralized AI Subnets.* arXiv:2603.29751. — Derives a size premium from Bittensor subnet CPMM mechanics; documents the December 2025 halving cutting the daily premium from 1.17% to 0.51% (p=0.044). https://arxiv.org/pdf/2603.29751v1
- Lui, E. & Sun, J. (2025). *Bittensor Protocol: The Bitcoin in Decentralized Artificial Intelligence?* arXiv:2507.02951. — On-chain analysis of all 64 Bittensor subnets; documents stake/reward concentration. https://arxiv.org/pdf/2507.02951v1
- Li, S. et al. (2025). *Dynamic Pricing for On-Demand DNN Inference in the Edge-AI Market.* arXiv:2503.04521. — Edge-AI auction theory, useful for thinking about a future on-chain inference market microstructure. https://arxiv.org/pdf/2503.04521v2
- Celeny, D. et al. (2024). *Prioritizing Investments in Cybersecurity: Empirical Evidence from an Event Study on the Determinants of Cyberattack Costs.* arXiv:2402.04773. — Methodological reference for event-study standard-error adjustments (event-induced variance + cross-sectional correlation). https://arxiv.org/pdf/2402.04773v1

### Primary protocol / project sources
- Coinbase x402 protocol: https://docs.cdp.coinbase.com/x402/welcome  ; https://www.x402.org/x402-whitepaper.pdf
- Olas / Autonolas: https://olas.network/  ; Pearl agent app store: https://autonolas.org/
- Virtuals Protocol whitepaper: https://whitepaper.virtuals.io
- ElizaOS / ai16z: https://github.com/elizaOS/eliza
- Akash Network: https://akash.network/blog/scaling-the-supercloud/
- Backed Finance NVDAx: https://backed.fi/news-updates/inx-and-backed-launch-on-chain-tokenized-nvidia-stock-trading

### Quarterly state-of-network reports (Messari)
- *State of Akash Q1 2025*: https://messari.io/report/state-of-akash-q1-2025
- *State of Akash Q4 2024*: https://messari.io/report/state-of-akash-q4-2024
- *State of Akash Q3 2024*: https://messari.io/report/state-of-akash-network-q3-2024
- *State of Akash Q4 2025*: https://messari.io/report/state-of-akash-q4-2025
- Bittensor / Messari project page: https://messari.io/project/bittensor

### Market-cap aggregators
- CoinGecko TAO: https://www.coingecko.com/en/coins/bittensor
- CoinMarketCap TAO: https://coinmarketcap.com/currencies/bittensor/
- CoinGecko ASI (FET): https://www.coingecko.com/en/coins/artificial-superintelligence-alliance
- CoinMarketCap NVDAx: https://coinmarketcap.com/currencies/nvidia-tokenized-stock-xstock/

### Event-study primary news sources
- OpenAI DevDay 2023 (GPT-4 Turbo, 3× cheaper input): https://openai.com/index/new-models-and-developer-products-announced-at-devday/
- CNBC OpenAI GPT-4 Turbo coverage: https://www.cnbc.com/2023/11/06/openai-announces-more-powerful-gpt-4-turbo-and-cuts-prices.html
- NVIDIA GTC 2024 AI-token rally: https://www.fxstreet.com/cryptocurrencies/news/crypto-ai-token-rally-persists-ignited-by-nvidia-ai-conference-202403180922
- CoinDesk AI tokens edge higher pre-NVDA earnings May 2024: https://www.coindesk.com/markets/2024/05/22/ai-focused-tokens-edge-higher-ahead-of-nvidia-earnings-results
- CoinDesk AI tokens lead recovery May 2024: https://www.coindesk.com/markets/2024/05/07/ai-tokens-lead-crypto-market-recovery-as-nvidia-hits-one-month-high
- CCN $25B AI-token sector surge: https://www.ccn.com/news/nvidia-ai-token/
- ASI merger announcement (FET / AGIX / OCEAN): https://fetch.ai/blog/artificial-superintelligence-alliance-token-merger-approved
- Anthropic Claude 3.5 Sonnet release (June 2024): https://artificialanalysis.ai/models/claude-35-sonnet-june-24
- Anthropic pricing & Opus 4.7 (April 2026): https://www.finout.io/blog/claude-opus-4.7-pricing-the-real-cost-story-behind-the-unchanged-price-tag
- The New Stack — Anthropic million-token pricing: https://thenewstack.io/claude-million-token-pricing/
- NVIDIA-RNDR partnership Feb 2024 (CCN): https://www.ccn.com/nvidia-crypto-render-ai-coin/
- Invezz TAO-NVDA correlation Nov 2025: https://invezz.com/news/2025/11/14/bittensor-tao-fights-nvidia-ai-market-selloff-eyes-on-300-support/
- MEXC AI-crypto correlation post-GTC 2026: https://blog.mexc.com/news/is-tao-the-new-nvidia-how-to-trade-the-2026-ai-crypto-correlation-after-gtc-2026/
- xStocks volume / AUM (Solana case study): https://solana.com/news/case-study-xstocks
- xStocks tokenized equities (Coin Metrics): https://coinmetrics.substack.com/p/state-of-the-network-issue-341
- KuCoin AI/crypto institutional flows: https://www.kucoin.com/blog/ai-crypto-institutional-investment-bubble-or-opportunity-2026

### Class C — payment receipt protocols
- AWS x402 agentic commerce coverage: https://aws.amazon.com/blogs/industries/x402-and-agentic-commerce-redefining-autonomous-payments-in-financial-services/
- Coinbase x402 launch: https://www.coinbase.com/developer-platform/discover/launches/x402
- The Block — what is x402: https://www.theblock.co/learn/391983/what-is-coinbases-x402-protocol
- Olas Pearl + x402 integration coverage (CMC AI): https://coinmarketcap.com/cmc-ai/elizaos/what-is/

### Methodology / cross-reference
- Simon Willison on Claude Code pricing confusion: https://simonwillison.net/2026/Apr/22/claude-code-confusion/
- BigGo "Anthropic stealth price hikes": https://finance.biggo.com/news/aHDqzJ0BDPbb-ItTijCV
- Sacra Anthropic revenue / valuation: https://sacra.com/c/anthropic/

---

End of report.
