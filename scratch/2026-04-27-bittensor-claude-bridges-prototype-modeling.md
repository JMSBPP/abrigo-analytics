# Bittensor / Olas / x402 → proprietary AI cost: prototype-modeling substrate scan

Date: 2026-04-27
Author: Empirical bridge research (companion to `2026-04-27-onchain-proxies-for-proprietary-ai-cost.md`)
Question: Which existing on-chain protocol most directly mediates flow between proprietary AI providers (especially Anthropic Claude) and decentralized AI economies, and is that bridge clean enough to support prototype-modeling of a Claude-cost hedge instrument under ideal conditions?
Output scope: BRIDGE-IDENTIFICATION + PROTOTYPE-MODELING FEASIBILITY only — not VENUE, not instrument design.

---

## 1. Executive summary

There are exactly **two on-chain protocols today that directly bridge Claude/GPT-4 inference into a decentralized AI economy with non-trivial economic flow**: (1) Bittensor **Subnet 18 / Cortex.t**, where the published miner+validator software *requires* an OpenAI key and supports Anthropic Claude3 + Google Gemini as additional backends — i.e. miners are *protocol-mandated* to proxy proprietary providers; and (2) **Olas Mech Marketplace**, where individual mechs increasingly self-disclose Claude/GPT-4 backends in their on-chain agent metadata and IPFS-stored deliver-event payloads. **x402** is the broadest payment rail (35M+ tx on Solana alone, Stripe live Feb 2026) but its receipt schema does NOT carry model-version metadata on-chain — only `(amount, recipient, resource_url)` — so it functions as a *volume* signal, not an *attribution* signal.

Of these, **Subnet 18 / Cortex.t is the cleanest prototype substrate.** Its dTAO subnet token (SN18 alpha) trades a CPMM with daily price discovery, miners have a hard cost floor equal to the proprietary API spend they must front, and the Maymin (2026) methodology gives us a published econometric template for subnet-event studies. A 12-month event-study on `α_18` returns vs. dated Anthropic / OpenAI / Google pricing-and-rate-limit changes is feasible NOW with public data.

**Honest read up front:** even in ideal conditions, the SN18 prototype is unlikely to produce statistically tight elasticities. The signal is contaminated by SN18-specific governance shocks, Bittensor protocol-internal events (Dec 2025 halving, Nov 2025 flow-based emission redesign), and the cross-subnet rotation of dTAO speculative capital. The prototype's value is **directional** (does the channel exist at all?) not **calibration-grade**.

---

## 2. Bittensor subnet survey — focused on proprietary-API proxying

### 2.1 Architecture and economics primer

Bittensor (`docs.learnbittensor.org`) is a Substrate-based L1 with a hub-and-spoke topology: one root chain plus N independent **subnets**, each of which is an isolated incentive economy producing a specific digital commodity. As of April 2026 there are **128 active subnets** with a slot ceiling that has expanded under dTAO. The economic primitives that matter for our prototype:

- **TAO** is the root token (4-year halving cadence; first halving Nov-Dec 2025 cut block emission from 1 TAO → 0.5 TAO, daily emission dropped 7,200 → 3,600 TAO).
- **dTAO** (Dynamic TAO, launched Q1 2025) gives each subnet its own **alpha token (`α_n`)** that trades against TAO via a constant-product AMM (the "subnet pool"). Staking TAO into subnet `n` is a swap into `α_n`; unstaking is the reverse swap.
- **Yuma Consensus** distributes per-tempo emissions (~72 minutes) across miners, validators, and subnet owner. Default split per subnet: **18% owner / 41% miners (via validator scoring) / 41% validators+stakers**.
- **Flow-based emissions ("Taoflow", Nov 2025)** allocate cross-subnet TAO emission by the **86.8-day EMA of net TAO inflow** (staking minus unstaking) per subnet, with linear (p=1) normalization. *Subnets with negative net flow get zero emission.* This replaced the prior price-based allocation that was vulnerable to "TAO treasury" spoofing.
- **Subnet pool depth** = liquidity for `α_n ↔ TAO` swaps. Maymin (2026) shows this CPMM mechanic generates a `1.01% daily small-minus-big size premium` across 128 subnets (Newey-West t = 3.28); the December 2025 halving cut that premium from 1.17% → 0.51% (p=0.044). The premium is implementable only below ~$10K AUM — i.e. retail-scale.
- **Concentration:** Lui & Sun (2025, arXiv:2507.02951) document on data from all 64 active subnets (their cohort) that *rewards are overwhelmingly driven by stake, not contribution quality*, and that an 88th-percentile stake cap would meaningfully raise 51%-attack coalition size. This is the reflexivity hazard for any subnet-level signal.

### 2.2 Candidate subnets ranked by proprietary-API exposure

This is the central evidence for the report. I scored each by (a) *does the canonical software stack require/permit a proprietary API key?*, (b) *would the subnet's economics break if Anthropic/OpenAI/Google revoked access or doubled prices?*, (c) *what's the on-chain observable*.

| Subnet ID | Name | Operator | Proprietary-API exposure | On-chain observable |
|---|---|---|---|---|
| **18** | **Cortex.t** | **Corcel** | **MAXIMAL — README explicitly requires an OpenAI API key, and supports `gpt-3.5-turbo`, `gpt-4`, `gemini`, `claude3` as backends. Verbatim from project docs: "Neither the miner or the validator will function without a valid and working OpenAI API key." Costs come from API calls, not compute.** | dTAO `α_18` price + emission share + miner stake distribution |
| 4 | Targon | Manifold Labs | HIGH — incentivizes miners to operate **OpenAI-compliant endpoints**; validators verify via logprob comparison against their own model. Powers Dippy (4M+ users), TAOBOT, Sybil. The "OpenAI-compliant" framing means open-source models matched against the OpenAI API schema, but a profit-maximizing miner *can* simply proxy GPT-4 to win the speed/quality leg of the score (logprob check filters this only if validator runs the same proprietary model — not the typical case). | dTAO `α_4` |
| 1 | Apex | Macrocosmos | LOW-MODERATE — distributed conversational AI; canonical stack uses LLaMA/Mistral, but no enforcement against proprietary-API proxying. Steffen Cruz (Macrocosmos CTO, ex-OpenTensor CTO) is the original architect. | `α_1` |
| 11 | Dippy Roleplay | Impel Intelligence | LOW-MODERATE — open-source roleplay LLMs; same proxy hazard as SN1 | `α_11` |
| 19 | Nineteen | Rayon Labs | LOW — DSIS framework explicitly emphasizes open-source models (LLaMA 3, Stable Diffusion derivatives). Marketed as open-source-first. | `α_19` |
| **64** | **Chutes** | **Rayon Labs** | LOW (substitute, not proxy) — but **structurally most important comparator**: serverless decentralized inference, pay-per-token in TAO/fiat, **9.1 trillion tokens served lifetime, 50B+ daily peaks**, ~85% lower than AWS for comparable workloads. First subnet over $100M mcap (9 weeks post-dTAO launch). Auto-staking buybacks ($1M+) close the revenue→`α_64` flywheel. | `α_64`, plus Rayon's auto-staking on-chain buyback flow |
| 8 | Proprietary Trading Network | Inference Labs | NONE — confusingly named; is actually a quantitative trading prediction subnet, not a proprietary-AI bridge | n/a |
| 9 | Pretraining | Macrocosmos | NONE — pretrains foundation models; opposite direction of flow | n/a |
| 5 | (Open Kaito / various) | varies | NONE-LOW depending on cohort | n/a |

**Tier-1 candidate is unambiguous: Subnet 18 / Cortex.t.** It is the only subnet whose canonical software *cannot run* without a proprietary API key, and whose miner unit-economics are *literally* (Anthropic-or-OpenAI-or-Google API spend) - (won validator scoring × `α_18` price). Tier-2 fallback is Subnet 4 / Targon (operationally similar, but with logprob verification that *should* but plausibly does not eliminate proprietary-proxying).

### 2.3 Does Subnet 18 economics RESPOND to proprietary-AI cost shocks?

This is the critical empirical question. The mechanism is economically clean:

- Each Cortex.t miner has a **per-call USD cost** equal to whatever Anthropic/OpenAI/Google charges for the model the miner is serving. With Anthropic Claude 4.7 Sonnet at $3/M input + $15/M output and GPT-4o at $5/M input + $15/M output (April 2026 pricing), a single 1K-prompt 1K-completion call costs miners roughly $0.018 (Claude Sonnet) or $0.020 (GPT-4o).
- Miner revenue = pro-rata share of `α_18` emission × spot `α_18` price (in TAO or USD).
- **Break-even condition:** `α_18` USD-emission-per-call ≥ proprietary-API USD-cost-per-call.
- If Anthropic doubles input pricing, EVERY Cortex.t miner using Claude faces a doubled cost floor. They either (a) switch to a cheaper backend, (b) reduce serving volume, (c) exit, or (d) accept lower margin — and (a)-(c) all affect either the validator-scoring quality distribution (if backends differ in score) or the net-stake flow into SN18 (which under Taoflow drives next-period emission).

**What's empirically observable:** I did NOT find a published event-study testing this directly. The Maymin 2026 paper documents protocol-internal halving but explicitly does not test proprietary-AI events. Lui & Sun 2025 examine concentration but not exogenous-cost shocks. **No Bittensor-community Discord thread, GitHub issue, or empirical paper that I can locate publishes a clean response coefficient of `Δα_18` to dated Anthropic/OpenAI events.**

This is the gap a prototype would fill.

### 2.4 Foundation/community stance on proprietary-API proxying

Bittensor Foundation has not issued a public statement banning proprietary-API proxying on text-generation subnets. The community quality consensus (per the 2026 reviews compiled by CoinMarketCap CMC-AI and OAK Research) is:
- **Output quality on most text subnets is below GPT-4o / Claude Sonnet** — i.e. proxies do happen but are not yet pervasive enough to make subnet output indistinguishable from the underlying proprietary model.
- **Validators struggle to distinguish "good outputs" from "outputs gamed to pass scoring"** — a structural problem that lowers the cost of proprietary-proxying because validators often cannot detect it.
- **Subnet 18 is the explicit-design case** where the proxying is not gamed — it's the published architecture. Cortex.t markets itself as a *broker* for proprietary models with on-chain economic settlement.

### 2.5 Maymin 2026 methodology applied to a Claude event study

Maymin (arXiv:2603.29751) regresses daily subnet returns on a small-minus-big size factor across 128 subnets, with Newey-West HAC standard errors. The natural extension for our prototype:

```
α_18,t  = β_0  +  β_1 · CLAUDE_PRICE_CHANGE_t  +  β_2 · OPENAI_PRICE_CHANGE_t
                  +  β_3 · GEMINI_PRICE_CHANGE_t  +  β_4 · MARKET_t (small-minus-big)
                  +  β_5 · TAO_t  +  ε_t
```

with `CLAUDE_PRICE_CHANGE` defined on dated event windows (model release, pricing change, rate-limit notice, deprecation announcement). Newey-West HAC(K) standard errors with K = `floor(4(n/100)^(2/9))`. Events to date: Claude 3.5 Sonnet (Jun 2024), Claude 3.5 Sonnet Oct 24 + Computer Use beta, Claude 3.7 Sonnet (Feb 2025), Claude 4 (May 2025), Claude 4.5 (Sep 2025), Claude 4.6 (Nov 2025), Claude 4.7 (Mar 2026), and the various Opus stealth price hikes (BigGo coverage Dec 2025–Apr 2026). That's ~10-12 dated events over the prototype window — adequate for a directional read, not for tight elasticity estimation.

A positive `β_1` ≠ 0 with t > 2 in either sign would be a non-trivial find. A negative `β_1` (Claude price up → SN18 alpha down) is the substitution-channel story (miners squeezed). A positive `β_1` (Claude price up → SN18 alpha up) is the **monopoly-rents-passthrough** story: if Cortex.t miners can pass cost to Cortex.t API clients, the margin layer thickens.

---

## 3. Olas / Mech Marketplace deep dive

The Mech Marketplace is the second-cleanest substrate. Per the official Olas docs (`docs.olas.network/product/mechkit/`, `marketplace.olas.network`):

- **Architecture:** A "permissionless marketplace for AI skills" where mechs are addressable agents that perform specific tasks for crypto micropayments. Both `request` and `deliver` events are emitted on-chain (Gnosis, Base, Ethereum); the associated payloads are stored on IPFS and CID-referenced from the on-chain event.
- **Volume:** 5.2M agent transactions Q1 2025; 9M Q2 2025 (per the prior research); the cumulative trajectory through Q1 2026 (per Olas's own press) is in the multi-tens-of-millions. x402 integration shipped Nov 2025, expanding the rail.
- **Model-attribution leakage on-chain:** Per the marketplace explorer, individual mechs DO self-publish backend metadata. Documented examples include "Agents With Receipts" mechs running `claude-sonnet-4-6` and `claude-opus-4-5` via the Anthropic agents SDK with on-chain Solidity 0.8.24 receipt contracts. This is the *first* place in the on-chain economy where "Claude was the LLM that produced this output" is **legible from public chain data** (with one IPFS hop).
- **Pricing:** Mech price-per-call is set by the mech operator and published on-chain in the mech registry. A Claude-Opus-routed mech costs more than a Llama-3-routed mech by approximately the underlying API cost differential plus operator margin. In principle, you could sample N mechs grouped by self-declared backend and compute an empirical Anthropic-vs-open-source price spread directly from on-chain data.

**Dataset feasibility for prototype:**
- The marketplace has thousands of agents; you would need to scrape the Olas marketplace API + IPFS payloads to assemble a per-call panel of `(mech_id, backend_model, on_chain_USDC_price, timestamp)`.
- The "self-disclosed backend" field is operator-attested, not protocol-verified. Operators have weak incentives to lie since lying produces objectively worse outputs that hurt their reputation — but the data is still soft.
- **Volume per backend is the missing piece.** Total Olas marketplace volume is large, but the share routed via Claude vs GPT-4 vs open-source is not aggregated anywhere I can find. A Dune dashboard could compute it from `request` events × IPFS payloads in approximately a 2-week engineering sprint.

**Verdict for prototype substrate:** Olas Mech Marketplace is the **second-cleanest substrate** after Subnet 18, and it's the only one where the proprietary-provider attribution is *direct in the data* (one IPFS hop) rather than *inferred from miner economics*. Its weakness is that the attestation is soft.

---

## 4. x402 (Coinbase) — payment rail without attribution

x402 is the broadest rail by volume — 35M+ transactions on Solana since summer 2025, 100M+ across all settlement chains (Base / Polygon / Arbitrum / World / Solana), $10M+ aggregate USDC volume, Stripe-integrated Feb 2026, and Anthropic is a member of the x402 Foundation (alongside Google, Visa, AWS, Circle, Vercel). Per `x402.org` and Coinbase docs:

- **Receipt schema (on-chain):** The settlement transaction carries `(payer, recipient, amount_USDC, payment_id_hash)`. The off-chain HTTP payment-required header carries `(resource_url, description, reason_string, accepts: [scheme, network, amount, asset])`.
- **What's NOT on-chain:** the model identifier, the prompt, the completion, the inferred backend — none of this is settled to chain. The payment server *can* embed model metadata in the `description` field, but that field is (a) optional, (b) operator-controlled, and (c) not protocol-validated. Stantchev (arXiv:2604.11430, "Hardening x402: PII-Safe Agentic Payments") shows the metadata leak is large enough to require a presidio-style filter — confirming that the metadata is rich off-chain but trimmed on-chain.
- **Inference attribution today:** Per the WEEX coverage of DGrid's x402 inference API on BNB Chain and the BlockEden x402 explainer, early adopters are clustering around "pay-per-prompt wrappers around model APIs" — i.e. exactly the use case that *should* let us tag receipts by upstream model. But the on-chain settlement layer does not enforce this tagging.

**Implication for prototype:** x402 is a *volume* signal — total daily USDC payments to known AI-inference endpoints — not an *attribution* signal. You could prototype a "decentralized inference economic activity index" on x402 receipts, and you could correlate it with Anthropic stealth price hikes (does total inference volume drop when Claude prices go up?), but you cannot decompose it by model. This is meaningful as a **complementary basket** to Subnet 18 / Cortex.t, not a standalone prototype substrate.

---

## 5. Other candidate bridges — quick assessments

| Project | On-chain model attribution? | Prototype substrate? | Verdict |
|---|---|---|---|
| **ChainGPT (CGPT)** | NO. Token-gated centralized API; backend-routing is opaque. | NO | Off-chain accounting. Skip. |
| **ai16z / ElizaOS** | NO. Framework is open-source and model-agnostic; no on-chain inference receipt; AI16Z had a 2026 fraud class-action filing. | NO | Skip. |
| **Morpheus (MOR)** | NO. Compute-providers-staking model with emission-based incentive; no observable user-paid revenue. | NO | Token-mechanics not inference economics. |
| **Virtuals Protocol** | PARTIAL. Inference cost flows in $VIRTUAL on Base; per-call cost is on-chain but the LLM call is off-chain. No Anthropic/OpenAI tag. | WEAK | Too contaminated by VIRTUAL agent-token reflexivity (per prior report). |
| **Hyperbolic** | Centralized inference platform, not on-chain settlement. | NO | Off-chain. |
| **Nous Research / Prime Intellect / Pluralis** | Decentralized training research. Mostly compute-allocation, not user-paid inference. | NO | Wrong stage of the value chain. |
| **Akash inference** | Akash has a "Supercloud" inference layer (Llama-3, Mixtral) but it's open-source-served, not proprietary-API-routed. | NO (orthogonal) | Decentralized substitute, not bridge — covered in prior report. |
| **Bittensor Subnet 64 / Chutes** | Pay-per-token in TAO/fiat for *open-source* inference. Not a proprietary-AI bridge. But its on-chain revenue → `α_64` auto-staking flywheel is the cleanest decentralized-inference economic signal in the entire ecosystem. | YES — but as a SUBSTITUTE comparator, not a bridge | Use as the **decentralized substitute leg** of any prototype that pairs SN18 (proxy) with SN64 (substitute). |

The Subnet-18-vs-Subnet-64 pair is structurally interesting: SN18 is the proprietary-pass-through subnet, SN64 is the open-source-substitute subnet. Their relative economics — `α_18 / α_64` price ratio, or relative emission share over time — should respond inversely to proprietary-AI pricing shocks under the substitution hypothesis. **This is the pair-trade structure the prototype should test.**

---

## 6. Prototype-modeling feasibility

This is the load-bearing section. I sketch three prototype designs in increasing ambition.

### 6.1 Prototype P1 — minimum-viable: SN18 alpha event study

**Hypothesis:** Daily returns on the SN18 (`α_18`) subnet token respond to dated Anthropic / OpenAI / Google pricing-and-capability events, controlling for Bittensor protocol-internal events and broad TAO market beta.

**Data:**
- `α_18` daily close from taostats.io (CSV export); start date = dTAO launch (Q1 2025) → ~15 months of daily history through April 2026 ≈ 450 obs.
- TAO daily close (CoinGecko).
- Maymin 2026 small-minus-big factor across all 128 subnets (recoverable from `Δlog(reserves_TAO)` via taostats public data).
- Event dates: Claude 3.5 (Jun 2024), Claude 3.5 Oct 2024, Claude 3.7 (Feb 2025), Claude 4 (May 2025), Claude 4.5 (Sep 2025), Claude 4.6 (Nov 2025), Claude 4.7 (Mar 2026); GPT-4o (May 2024), GPT-4o-mini (Jul 2024), o1 (Sep 2024), o3-mini (Jan 2025), GPT-5 (rumored Q2 2026); Gemini 1.5 Pro / 2.0 Flash / 2.5; the Anthropic stealth price hikes (BigGo Dec 2025, Finout Apr 2026); rate-limit announcements on the Anthropic developer console; the OpenAI Stargate announcement.
- Bittensor protocol events: dTAO launch (Q1 2025), Taoflow flow-based emission redesign (Nov 2025), first halving (Dec 14 2025).

**Method:**
- OLS with HAC(K) standard errors per Newey-West, K computed via Maymin's choice rule.
- 3-day cumulative abnormal return (CAR) per event with bootstrap CIs.
- Falsification: replace event dates with random dates from the same window — abnormal returns should not survive.
- Specification check: include SN64 (`α_64`) returns as a control for "decentralized-AI market beta within Bittensor".

**Required window:** 12 months minimum (need 8-10 events for any directional inference); 18 months ideal (would let you cleanly drop the dTAO-launch transient).

**What success looks like:**
- `β_CLAUDE_PRICE_UP` significantly negative (substitution channel: miners squeezed) OR significantly positive (passthrough channel: margin layer thickens), with t > 2 and HAC-corrected SE.
- Falsification tests fail (random dates produce no signal).
- Pair-trade signal: `α_18 / α_64` ratio responds in opposite directions to proprietary vs. open-source events.

**What would falsify the prototype:**
- All `β` coefficients indistinguishable from zero with HAC SEs.
- Falsification tests "pass" (random dates produce signal of similar magnitude → spurious).
- The Maymin small-minus-big factor + TAO beta + Bittensor protocol-internal dummies absorb >95% of `α_18` variance.

**Effort estimate:** 2-3 weeks for one analyst (data scrape, panel construction, OLS+HAC, event coding, sensitivity).

### 6.2 Prototype P2 — fuller-stack: SN18 ∪ SN4 ∪ Olas Mech

Extends P1 with two additional signals:

- **SN4 (Targon) `α_4`:** the second proprietary-API-exposed subnet. Treating SN4 + SN18 as a 2-asset proprietary-proxy panel improves cross-section variation and lets you test whether the response is consistent across two operationally similar subnets (good external-validity check) or driven by SN18-idiosyncratic governance (bad).
- **Olas Mech Marketplace tagged-backend volume:** scrape `request` events on Gnosis/Base, fetch IPFS payloads, classify backends as `claude / gpt / gemini / open-source`, aggregate weekly USDC volume per class. Test whether weekly volume responds to provider events.

**Method:** SUR (seemingly unrelated regressions) across the SN18, SN4, and Mech-volume series with HAC SEs and a Bonferroni correction across the three equations.

**What this buys you over P1:** triangulation. If all three series move the same direction at Anthropic events, the channel is real. If only SN18 moves, the result is SN18-specific. If Mech volume moves but SN18 alpha doesn't, the dTAO market is missing the signal.

**Effort estimate:** 4-6 weeks (the IPFS scrape and backend classification is the bulk).

### 6.3 Prototype P3 — pair-trade calibration: SN18 vs SN64

The most theoretically clean prototype, because it isolates the substitution channel:

- **Hypothesis:** `log(α_18) - log(α_64)` (proxy minus substitute, in TAO terms) is a direct measure of relative miner economic health, and it should DROP when proprietary providers cut prices (substitute relatively favored) and RISE when proprietary providers raise prices (proxy operators pass through margin).
- **Cointegration test:** Engle-Granger or Johansen on the bivariate VAR `(log α_18, log α_64)` to test whether they share a long-run relationship.
- **VECM** (vector error-correction model) with proprietary-AI pricing shocks as exogenous covariates.
- **Forecast test:** Fit on first 9 months of dTAO history, out-of-sample forecast on the last 6 months.

**What success looks like:** the proprietary-AI exogenous covariate enters the cointegrating equation with a significant, theoretically-signed coefficient, AND the out-of-sample forecast outperforms a naive random-walk benchmark on RMSE.

**What would falsify:** no cointegration (each subnet is its own random walk), or cointegration without sensitivity to proprietary-AI shocks (the spread is driven by Bittensor-internal factors only).

**Effort estimate:** 6-8 weeks (requires careful unit-root testing, structural break detection around dTAO launch and the Dec 2025 halving).

### 6.4 Prototype-modeling honest-conditions checklist

For ANY of P1-P3, the following must be acknowledged as constraints on the prototype's claim:

1. **Sample size is small.** Maximum 18 months of dTAO history × ~10-12 dated proprietary events. Power to detect anything but a >5% per-event abnormal return is limited.
2. **One halving in-sample.** The Dec 2025 Bittensor halving is the largest single shock in the panel and will dominate any naive specification. Must be carefully controlled with a dated dummy.
3. **Taoflow regime change Nov 2025.** The flow-based emission redesign restructured cross-subnet allocation. Pre-November and post-November SN18 emissions are not directly comparable.
4. **dTAO speculative cycles.** Maymin's small-minus-big premium is 1.01% daily — that's a *huge* nuisance factor for any individual subnet's signal. Must be controlled.
5. **Self-attestation soft data.** Olas mech backend tags are operator-claimed. Cortex.t miners' actual API usage is private to the miner. The economic *implication* (cost floor moves with proprietary pricing) holds regardless of attestation, but per-call attribution is soft.
6. **Liquidity regime-shift.** Maymin shows premia are exploitable only sub-$10K AUM. Any production hedge instrument settled on these signals would, by its existence, push notional above $10K and into the regime where transaction costs eat the signal.

Acknowledging these, the prototype's **scientific value is bounded**: it can plausibly establish that a channel exists and estimate its sign, but **it cannot calibrate elasticities tightly enough to underwrite a production hedge instrument** in the current data regime.

---

## 7. Honest assessment — can we extract a Claude-cost signal cleanly enough?

**Short answer: NO, not at production-grade fidelity. YES, at directional-prototype fidelity.**

Long answer in three parts:

### 7.1 What the data CAN support today

- A directional event-study on SN18 `α_18` returns vs. dated Claude / GPT / Gemini events. This is feasible NOW and would be the single most informative experiment we could run for the cost of a few engineer-weeks.
- A SUR triangulation across SN18, SN4, and Olas Mech Marketplace tagged volume. Adds a meaningful independent-validation leg.
- A pair-trade prototype on SN18-vs-SN64 alpha spread, testing the substitution channel structurally. Most theoretically clean of the three.
- An x402 daily AI-inference USDC volume index, used as a contemporaneous control rather than a direct signal.

### 7.2 What the data CANNOT support today

- **Calibration-grade elasticity estimation.** The signal-to-noise ratio in any 12-18 month dTAO history will not pin down `dα_18 / dPrice_Claude` to better than maybe ±50% relative SE. That's fine for direction; not fine for hedge sizing.
- **A production hedge instrument settled on a SN18 oracle.** SN18 has had episodes of governance / scoring controversy (per the structural critiques in Lui & Sun 2025 and the broader CoinMarketCap / OAK Research reviews) and SN18-idiosyncratic shocks would pollute settlement.
- **Real-time intra-day signal.** dTAO subnet pools have CPMM slippage that distorts intra-day price discovery. Maymin shows the size premium is exploitable only sub-$10K — i.e. the on-chain price is a fair-value estimator only in retail-scale regimes.
- **Direct Anthropic-vs-OpenAI-vs-Google decomposition.** Cortex.t miners can flexibly switch backends; the on-chain data does not record which proprietary API was called for which response. The aggregate `α_18` price is a weighted combination of all three providers' cost shocks, with weights that are themselves endogenous and time-varying.

### 7.3 The structural conclusion

The infrastructure for a production-grade Claude-cost on-chain hedge **does not exist yet**. The infrastructure for a *prototype demonstration* of the channel (does flow exist? does it respond to proprietary events at all?) **does exist**, and Subnet 18 / Cortex.t is the cleanest substrate. The prior report's verdict — VERY-INDIRECT, trending toward NOT-YET — is **confirmed**, with the modification that **a falsifiable prototype experiment is now well-defined and cheap to execute**.

The honest commercial framing for any external pitch is: *we have identified the only place in the on-chain economy where Claude usage and on-chain economic settlement are mechanically linked (Cortex.t miners must spend USD on the Anthropic API to earn `α_18` emission); we are running a prototype to measure how strong that linkage is empirically; the linkage is too noisy today to settle a hedge instrument on, but the experiment will tell us what additional infrastructure (model-tagged x402 receipts, Olas Pearl backend disclosure, Bittensor subnet-emission oracles with provider attribution) would be needed for a production instrument to become viable.*

---

## 8. Recommended next step (2-4 week scope)

Execute **Prototype P1** (§6.1). Concretely:

**Week 1 — data assembly.**
- Scrape `α_18` and `α_64` daily price series from taostats.io (or via the official Substrate RPC) for the full dTAO history.
- Pull TAO daily close from CoinGecko.
- Compile event calendar: Claude 3.5 → 4.7 releases + dated price changes (from Anthropic developer changelog + BigGo / Finout coverage); GPT-4o → o3 cadence; Gemini 1.5 → 2.5; Bittensor halving (Dec 14 2025) and Taoflow live (Nov 2025).
- Compile Maymin small-minus-big factor across all 128 subnets — code is recoverable from the published methodology.

**Week 2 — estimation.**
- OLS with HAC(K) per Newey-West.
- 3-day CAR per event with bootstrap CIs.
- Falsification: 10,000 random-date placebos.
- Bonferroni-adjusted joint test on `β_CLAUDE`, `β_OPENAI`, `β_GEMINI`.

**Week 3 — interpretation + write-up.**
- Decision: does the channel exist? (`β` significant, falsification fails)
- Magnitude bound: 90% CI on `β_CLAUDE`, in elasticity units (% change in `α_18` per % change in Claude effective price).
- Triangulation with `α_4` and `α_64` as robustness.
- Output: 2-page memo with verdict, plus a Jupyter notebook reproducible from public sources.

**Week 4 — go/no-go decision.**
- If P1 passes (channel exists, falsification fails): commit to P2 (full Olas Mech triangulation, 4-6 week effort).
- If P1 produces null results: write the null up as an honest finding and fold it into the existing prior-report verdict; pivot the M-track research to other substrate candidates (or accept that the substrate is missing).

This scope is small, falsifiable, and answers the question that matters: *does the channel exist at all, even at retail-prototype scale?*

---

## 9. References / sources

### Bittensor official documentation
- Docs Home: https://docs.learnbittensor.org/
- Emissions (Taoflow): https://docs.learnbittensor.org/learn/emissions
- Subnets overview: https://docs.learnbittensor.org/subnets/understanding-subnets
- Subnet directory (community-maintained JSON): https://github.com/taostat/subnets-infos/blob/main/subnets.json

### Subnet-specific
- Cortex.t (SN18): https://cortex-t.ai/docs ; https://github.com/corcel-api/cortex.t
- Targon (SN4): https://research.tokenmetrics.com/p/targon ; https://taostats.io/subnets/4/metagraph
- Apex (SN1) Macrocosmos: https://docs.macrocosmos.ai/subnets/subnet-1-apex-1 ; https://github.com/macrocosm-os/apex
- Nineteen (SN19): https://subnetalpha.ai/subnet/nineteen/ ; https://bittensor123.com/subnets/sn19/
- Chutes (SN64): https://www.tao.media/the-investors-guide-to-chutes-bittensors-inference-layer/ ; https://taostats.io/subnets/64/chart

### Data + analytics
- taostats.io (Bittensor explorer): https://taostats.io/
- TaoMarketCap: https://taomarketcap.com/
- Subnet Alpha: https://subnetalpha.ai/
- TAO.app: https://www.tao.app/
- Bittensor halving tracker: https://www.bittensor-halving.com/

### Olas / Mech Marketplace
- Mech Marketplace: https://olas.network/mech-marketplace ; https://marketplace.olas.network/base/ai-agents/
- MechKit docs: https://docs.olas.network/product/mechkit/
- mech-client: https://docs.olas.network/mech-client/

### x402
- x402.org standard: https://www.x402.org/ ; https://www.x402.org/x402-whitepaper.pdf
- Coinbase developer docs: https://docs.cdp.coinbase.com/x402/welcome
- Solana x402 deployment: https://solana.com/x402/what-is-x402
- Chainstack overview: https://chainstack.com/x402-protocol-for-ai-agents/
- DGrid x402 inference API on BNB: https://www.weex.com/news/detail/ai-infrastructure-dgrid-launches-ai-inference-api-supporting-x402-protocol-enabling-on-chain-payments-on-bnbchain-704338

### Academic
- Maymin, P. Z. (2026). *Common Risk Factors in Decentralized AI Subnets.* arXiv:2603.29751. https://arxiv.org/pdf/2603.29751v1 — the methodological backbone for any SN18 event study; documents the Dec 2025 halving cutting the size premium from 1.17% → 0.51% (p=0.044).
- Lui, E. & Sun, J. (2025). *Bittensor Protocol: The Bitcoin in Decentralized AI? A Critical and Empirical Analysis.* arXiv:2507.02951. https://arxiv.org/pdf/2507.02951v1 — concentration analysis across 64 subnets; critical for understanding the reflexivity hazard in any subnet-level signal.
- Stantchev, V. (2026). *Hardening x402: PII-Safe Agentic Payments via Pre-Execution Metadata Filtering.* arXiv:2604.11430. https://arxiv.org/pdf/2604.11430v1 — confirms x402 metadata is rich off-chain, trimmed on-chain; relevant to assessing what x402 can and cannot tell us about model attribution.

### Strategy / market reviews
- Grayscale: *Bittensor on the Eve of the First Halving.* https://research.grayscale.com/reports/bittensor-on-the-eve-of-the-first-halving
- CoinGecko: *Top 5 Bittensor Subnets — dTAO Ecosystem.* https://www.coingecko.com/learn/top-bittensor-subnets-dtao
- Yellow.com: *Bittensor's TAO Token And The AI-Crypto Thesis: Where The Network Stands In 2026.* https://yellow.com/news/bittensor-tao-token-ai-crypto-thesis-2026
- OAK Research subnet investing guide: https://oakresearch.io/en/analyses/innovations/bittensor-subnets-best-opportunities-investing-tao
- Alpha Sigma Capital subnet landscape: https://alphasigmacapitalresearch.substack.com/p/evaluating-the-bittensor-subnet-landscape
- Sami Kassab subnet classification framework: https://samikassab.substack.com/p/a-bittensor-subnet-classification

### Companion (this engagement)
- Prior signal report (basis-risk on broad AI baskets): `contracts/.scratch/2026-04-27-onchain-proxies-for-proprietary-ai-cost.md`

---

End of report.
