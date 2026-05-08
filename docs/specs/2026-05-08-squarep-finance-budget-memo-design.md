# SquareP Finance — Marketing & Infrastructure Budget Memo

**Date**: 2026-05-08
**Author**: JMSBPP (founder)
**Scope**: May 2026 + June 2026 budget cycles
**Envelope**: $400/month new-spend cap × 2 months = **$800**

**Sunk cost (excluded from envelope)**: Existing Cloud Code $100 top-up
already paid; $17 session credit remaining as of memo date. Future Cloud Code
top-ups *do* count against the envelope as a contingent line item.
**Hard deadline**: UHI9 capstone Hookathon submission **June 11, 2026** (34 days from memo date) — Atrium Academy / Uniswap Foundation cohort 9, theme "Impermanent Loss & Yield Systems," Reactive Network as named sponsor track.

## 1. Purpose

Allocate the $800 marketing/infrastructure envelope across competing claims —
brand surface, hackathon-critical infra, agent compute buffer, and research-paper
data — with each line tied to an explicit recovery channel and trigger condition.

The memo is not a wishlist. Anything not funded here is **deferred** with a
named trigger to revisit, not silently dropped.

## 2. Operating principle

Every dollar in May/June must be defensible as either:

- (a) directly improving the **UHI9 June 11 Hookathon submission** (primary), or
- (b) serving a **secondary recovery channel** at near-zero marginal cost on
  top of (a).

The brand surface (domain, email, X presence) qualifies under (b) — same
artifacts serve hackathon credibility, Celo Proof of Ship public-shipping
reputation, future grant applications, and the eventual research paper. Paid
Colombian macro data does *not* qualify under (b) — single-channel benefit at
high marginal cost. Therefore deferred.

## 3. Recovery-channel architecture

The cycle has **multiple concurrent recovery channels** sharing one codebase
and one brand surface:

| Channel | Type | Deadline | Status |
|---|---|---|---|
| **UHI9 capstone Hookathon** | Primary, single-shot | June 11 | User enrolled in cohort |
| **Celo Proof of Ship** | Continuous, monthly | Rolling ($5k cUSD/mo) | User enrolled |
| **Somnia Agentathon** | Secondary reskin | TBD (URL pending) | Provisional — same reactive-contract codebase as UHI9 |
| **UHI10 application** (reserve) | Cohort gate | May 15 / June 21 late | Fires only if June 11 missed |
| **Algebra / Panoptic / Mento direct** | Partner outreach | After June 19 demo day | Free; post-demo grant/partnership pitch |

| Spend category | What's in it | Funded? |
|---|---|---|
| Hookathon-critical | Solidity hook + reactive contract, RPC, AWS for control proofs, agent compute | Primary claim on funds |
| Brand surface | `squarep.finance` domain + email, Vercel host, X Basic | Small fixed cost; serves all channels |
| Research-paper data | Paid Colombian macro feeds | **Deferred** — single-channel, out of cycle |
| Operating buffer | Cross-vendor float so jobs don't die | All channels (continuity) |

## 4. Recovery-channel rationale

**UHI9 capstone (June 11) — primary.** Concentrated single-shot. UHI9 theme
"Impermanent Loss & Yield Systems" is verbatim Abrigo's premium-funded ratchet
over a Panoptic-style LP position. Reactive Network is a named sponsor; their
reactive smart contract primitive is architecturally central to the
ratchet (oracle/time-triggered position management). Judges include Variant,
a16z, Dragonfly, USV — narrative legibility for VC audience matters.

**Celo Proof of Ship — continuous.** $5k cUSD/month, AI-evaluated on shipping
cadence via Karma GAP + Farcaster. Tension with UHI9: Proof of Ship rewards
public progress shipping; UHI9 rewards a final reveal. Resolution: ship the
*Celo/Mento-side infrastructure* (cCOP integration, agent identity primitives,
deployment scripts) publicly for Proof of Ship reputation; hold the *Panoptic
settlement / capstone hook narrative* for the June 11 reveal. Two artifacts,
one codebase.

**Somnia Agentathon — secondary reskin.** The `reactive-smart-contracts`
skill explicitly covers dual-instance deployment to both Reactive Network
(UHI9 sponsor target) and Somnia L1. Marginal engineering cost is low —
chain-specific deployment differences only. Conditional on (a) URL confirming
deadline gives ≥4 days post-June 11, and (b) Somnia's specific track fitting
the architecture.

**UHI10 reserve.** May 15 application deadline; September capstone. Fires
*only* if June 11 capstone is missed. Application costs $0; no budget impact.

**Direct partner outreach (Algebra, Panoptic, Mento).** None has an active
hackathon in the May–July 2026 window. Channel = direct grant/partnership
pitch *after* June 19 demo day, leveraging the UHI9 capstone artifact.
Highest fit: Mento (cCOP/COPm alignment with Pair-D positioning); they
explicitly seek builders deploying with their local-currency stablecoins.
Zero budget cost; pure attention/outreach work.

## 5. May 2026 allocation (cap $400 new spend)

Today is 2026-05-08; May has ~3 weeks of remaining spend. Existing $17
Cloud Code session credit covers early-May agent work; first new top-up
likely mid-to-late May.

| Line | Amount | Rationale |
|---|---|---|
| `squarep.finance` domain (annual, paid May) | ~$50 | One-time annual; `.finance` TLD ~$30–80 (Cloudflare ~$45) |
| X (free tier — paid sub postponed) | $0 | Free account, multi-post threads; paid sub deferred to Section 7 trigger |
| Vercel Hobby | $0 | Free tier sufficient for hackathon demo site |
| Email (Cloudflare Email Routing → Gmail; Resend free for outbound) | $0 | Skip Workspace seat; hackathon-volume appropriate |
| Alchemy Free tier | $0 | Sufficient until rate limits hit during demo polish |
| AWS | $0 | Don't spin up until a control-proof job is queued |
| Cloud Code top-up (contingent, when $17 session depletes) | $100 | Fires when balance < $10; likely mid-to-late May |
| thirdweb free tier | $0 | Faucets, contract deploy SDK, on-chain tooling — sufficient at hackathon volume |
| Mainnet deploy gas — Celo (Proof of Ship) | $10 | Initial deploys + monthly cadence updates; <$1/deploy on Celo |
| Hackathon-discretionary slack | ~$232 | Unallocated; absorbs unexpected May needs and rolls forward |
| **May spend ceiling** | **$400** | |
| **May spend floor** (if Cloud Code top-up defers to June) | **$60** | Domain + Celo gas only (X paid sub postponed) |

**Key choices:**

- **Email via Cloudflare Email Routing + Resend free tier** instead of
  Workspace ($0 vs $6/mo). Routes `you@squarep.finance` into existing Gmail;
  sends from `squarep.finance` via Resend (3k emails/mo free). Trigger to
  upgrade: judges or grant orgs start emailing the alias regularly, OR a
  second team member joins.
- **Domain hits May, not June**, because annual TLD registration is a one-time
  charge, not amortized.
- **Hackathon-discretionary slack of ~$92 is intentional** — the highest-
  uncertainty week of any solo build is week 3 (last week before submission).
  Holding May slack is cheaper than emergency June reallocation.

## 6. June 2026 allocation (cap $400 new spend)

Reflects the $100 unlocked headroom from treating Cloud Code as
contingent-not-recurring: Alchemy and a portion of AWS shift from
*conditional* to *committed* lines.

| Line | Amount | Rationale |
|---|---|---|
| X (free tier) | $0 | Paid sub still deferred; multi-post threads continue |
| Vercel Hobby | $0 | Still free |
| Email infra | $0 | Cloudflare + Resend stay free |
| Alchemy Growth | $49 | **Committed** (was conditional) — removes RPC-throttling risk in polish week |
| AWS control-proof bursts | $100 | **Committed budget** (was $50–100 conditional) — symbolic verification headroom |
| Cloud Code top-up (contingent, if needed) | $0–100 | Only if May top-up depletes before June 11 |
| Mainnet deploy gas — Celo + occasional Unichain L2 polish | $30 | $10 Celo + $20 reserve for Unichain mainnet demo polish if judges request it |
| Submission-week emergency reserve (June 4–11) | $50 | Last-week bug fixes, surprise paid tooling |
| Hackathon-discretionary slack | ~$63–163 | Absorbs Cloud Code top-up if it fires; rolls forward otherwise |
| **June spend ceiling** | **$400** | |
| **June spend floor** (no Cloud Code top-up) | **$237** | Predictable committed lines only |

**Key choices:**

- **AWS and Alchemy are conditional, not committed.** Free tiers run until
  they break. Lazy-provisioning pattern saves money in the realistic case.
- **Submission-week reserve ($50) is non-negotiable.** Final-week unblock
  costs (debugger seats, deploy retries, surprise tooling) are where solo
  builders bleed money.

## 7. Deferred items + trigger conditions

| Deferred | Trigger to revisit |
|---|---|
| Colombian macro paid data | Research-paper deadline becomes concrete; reassess in next budget cycle |
| LinkedIn presence | First grant application or B2B-partnership conversation lined up |
| X paid subscription (Basic $8 or Premium $13–16) | Single thread crosses ~5k impressions, OR Hookathon judges click profile and bounce, OR multi-post threads cap distribution; whichever fires first |
| Workspace email seats ($6/mo) | Second team member joins, OR judges start emailing alias regularly |
| Vercel Pro ($20/mo) | Demo site needs custom analytics, password protection, or team seat |
| AWS commitment plans | Compute usage stable across 2+ months |
| LinkedIn Premium / sponsored | B2B-grant pipeline opens |
| Mantle Turing Test submission | Out — engineering scope (Agentic Wallets / ERC-8004) is a third architecture, not a reskin |
| ETHGlobal NY / Lisbon | Out — travel cost from Colombia exceeds full $800 envelope |
| thirdweb paid tier ($99/mo) | Free-tier rate limits hit during demo polish, OR gasless meta-tx volume justifies upgrade |
| Ethereum mainnet deployment | UHI9 judges explicitly request mainnet (rare; testnet is standard for capstones) |
| Unichain mainnet deployment | Mainnet polish becomes a competitive differentiator (rare); $20 budgeted in June already |

## 8. Risk reserves and failure-mode coverage

Two named failure modes, each with explicit cost line:

1. **"Agents stop overnight"** — Cloud Code top-up is a contingent $100 line
   that fires when session balance < $10. Slack in May ($242–342) and June
   ($93–193) absorbs the top-up whenever it lands, including overnight.
2. **"Surprise vendor bill kills float"** — June infra (Alchemy + AWS) is now
   *committed* with explicit caps; no auto-renew traps. Submission-week
   reserve ($50) is catch-all for unanticipated vendors in the June 4–11
   window.

**Total flexible reserves** (slack + submission reserve, excluding committed
infra): ~$427–635 across both months = **53–79% of $800 envelope** held in
flex. The high flex ratio is intentional given solo-builder uncertainty over a
34-day window.

## 9. Out-of-budget risks (flagged, not funded)

These are project risks the memo intentionally does *not* address with cash;
flagged so they're not invisible:

- **Panoptic testnet liquidity realism** — engineering risk. If demo requires
  mocked liquidity, scope transparently in the README; judges deduct less for
  acknowledged mocking than concealed mocking.
- **Superfluid + x402 SDK absorption time** — ~3–7 days each in attention cost.
  With 34 days solo, that's 20–40% of available engineering hours. Pick *one*
  of the two for the June 11 submission; defer the other.
- **Hackathon-judge profile clicks pre-checkmark** — partially mitigated by
  `squarep.finance` domain in bio + GitHub with real commits. Acceptable.
- **Domain DNS / email-deliverability setup time** — first-time SPF/DKIM/DMARC
  config takes a few hours. Schedule in week 1 of May to leave buffer.

## 10. Cumulative envelope check

| Category | May | June | Cycle total |
|---|---|---|---|
| Brand surface (domain + X + email + Vercel) | $58 | $8 | $66 |
| Hackathon infra committed (Alchemy, AWS) | $0 | $149 | $149 |
| Mainnet deploy gas (Celo + Unichain reserve) | $10 | $30 | $40 |
| Cloud Code top-ups (contingent — likely 1, possibly 2) | $0–100 | $0–100 | $100–200 |
| Submission-week reserve | $0 | $50 | $50 |
| Discretionary slack | $232–332 | $63–163 | $295–495 |
| **Total per month ceiling** | **$400** | **$400** | **$800** |
| **Total per month floor** | **$68** | **$237** | **$305** |

**Realistic point estimate** (one Cloud Code top-up across cycle, full
committed June infra used, $40 mainnet gas, ~$100 of slack absorbs misc
surprises): **~$505 of $800** = **63% utilization**, ~$295 underspend
rolling to post-hackathon cycle.

Underspend is **expected and intentional**, not a planning failure. The
~$295 rolling forward is what funds the *next* cycle's first-look at paid
Colombian macro data once the paper deadline becomes concrete.

## 10a. Chain deployment policy

Testnet-primary deploys for all Hookathon-side work; mainnet-secondary for
Celo Proof of Ship only.

| Channel | Primary deploy target | Mainnet trigger |
|---|---|---|
| UHI9 capstone | Unichain Sepolia (free) | Judge feedback requests mainnet polish (~$20 reserved June) |
| Reactive Network sponsor track | Reactive testnet (free) | Demo Day mainnet showcase only if explicitly required |
| Somnia Agentathon | Somnia testnet (free) | None — testnet sufficient |
| Celo Proof of Ship | **Celo mainnet** (cents per deploy) | Required — Karma GAP/Farcaster expects real mainnet artifacts |
| Mento integration (post-demo outreach) | Celo mainnet (cents per deploy) | Required for credible Mento conversation |

**thirdweb** (the third-web provider) is the standardization layer across
all chains: free tier provides faucets, deploy SDK, and on-chain tooling
sufficient for hackathon volume. Upgrade triggers are in Section 7.

## 11. Decision points needing live confirmation

- [ ] X tier: Basic ($8) recommended; upgrade to Premium ($16) override-able
- [ ] Domain registrar: Cloudflare Registrar (~$45/yr) recommended; Namecheap or
      Porkbun comparable
- [ ] Email outbound: Resend free tier (3k/mo) recommended; alternatives
      Postmark, AWS SES if Resend's deliverability proves weak

## 12. Out of scope for this memo

- The hackathon project's *technical* design (Solidity hook scope, reactive
  contract architecture, simulation work, analytics) — **user's own domain**;
  not part of this memo or its implementation plan
- The research paper's submission target and editorial timeline — separate doc
- Legal entity / tax handling for hackathon prize money — premature; revisit
  if/when prize is awarded
- Post-hackathon cycle (July+) budget — separate memo when this cycle closes

## 13. Implementation-plan scope

The implementation plan derived from this memo is a **prioritized TODO list**
covering admin / marketing / off-chain backend work *only*. It explicitly does
not cover:

- Solidity hook development (user-driven)
- Reactive contract development (user-driven)
- Simulation / analytics work (user-driven)
- Smart contract testing (user-driven)

It *does* cover, with agents doing the heavy lifting where possible:

- Domain registration, DNS, email routing setup
- Vercel landing page scaffolding and copy
- X account setup, posting cadence, marketing-thread drafts
- Karma GAP project listing + Farcaster account for Celo Proof of Ship
- Alchemy / AWS account provisioning (when triggers fire)
- UHI10 application drafting (reserve)
- Post-demo outreach drafts to Algebra / Panoptic / Mento
- Spend-tracking ledger maintenance against the $800 envelope

Sequencing in the plan respects the user's stated bias: marketing copy, UI,
and off-chain backend are *not* the user's strong suits, so those tasks are
structured as agent-executable TODOs the user reviews and approves rather
than tasks the user authors directly.
