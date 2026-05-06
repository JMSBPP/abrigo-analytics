---
name: Abrigo two-tier field rule for application forms
description: Story fields hide crypto per positioning rules; tech-disclosure fields disclose stack factually when audience is crypto-aware
type: project
originSessionId: bc613a18-50d4-4456-83d1-ae746e1240e0
---
When the branding agent fills any application form (hackathon, accelerator, grant, directory), it classifies every field into one of two tiers and applies different rules:

**Tier 1 \u2014 Story fields.** One-liner, problem, target audience, value proposition, challenges, long-term vision, pitch deck, demo script, landing page copy, tagline, any field whose answer is user-readable. All positioning rules apply without exception: crypto fully abstracted, painkiller framing, no named protocols (Angstrom / Panoptic / Mento / Uniswap / Ethereum), no "decentralization" selling, no Greek letters or jargon.

**Tier 2 \u2014 Tech-disclosure fields.** Tech stack, hosting provider, web3 ecosystem affiliation, AI tools used, verticals, infrastructure, integrations. These are administrative fields \u2014 the audience is the form operator (e.g., Crecimiento Foundation), not an end-user. Factual, specific disclosure is appropriate and often load-bearing: the Crecimiento form explicitly says it uses this data to negotiate credits (Claude Code, etc.) on behalf of startups. Under-disclosing costs real value.

**Boundary rule:** if a field could arguably be either tier, classify as Tier 1. The story must never be contaminated by tech jargon. When in doubt, err toward mainstream-readable.

**Why:** the positioning principles apply to how the product presents to its users, not to how the company presents its infrastructure to partners who need to know what's under the hood. One story, audience-appropriate tech surface.

**How to apply:** agent prompt template includes a field-classification step before answering. For each form field, agent decides tier, then applies tier rules. Disclosure in Tier 2 never feeds back into Tier 1 copy.
