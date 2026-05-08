# SquareP Finance — Marketing & Infrastructure Budget Memo

**Date**: 2026-05-08
**Author**: JMSBPP (founder)
**Scope**: May 2026 + June 2026 budget cycles
**Envelope**: $400/month new-spend cap × 2 months = **$800**

**Sunk cost (excluded from envelope)**: Existing Cloud Code $100 top-up
already paid; $17 session credit remaining as of memo date. Future Cloud Code
top-ups *do* count against the envelope as a contingent line item.
**Hard deadline**: Uniswap hackathon submission **June 11, 2026** (34 days from memo date)

## 1. Purpose

Allocate the $800 marketing/infrastructure envelope across competing claims —
brand surface, hackathon-critical infra, agent compute buffer, and research-paper
data — with each line tied to an explicit recovery channel and trigger condition.

The memo is not a wishlist. Anything not funded here is **deferred** with a
named trigger to revisit, not silently dropped.

## 2. Operating principle

Every dollar in May/June must be defensible as either:

- (a) directly improving the **June 11 hackathon submission**, or
- (b) serving the **research-paper / grants channel** at near-zero marginal
  cost on top of (a).

The brand surface (domain, email, X presence) qualifies under (b) — same
artifacts serve both channels. Paid Colombian macro data does *not* qualify
under (b) — it serves only the paper channel and at high marginal cost.
Therefore deferred.

## 3. Recovery-channel architecture

| Category | What's in it | Recovery channel | Funded? |
|---|---|---|---|
| Hackathon-critical | Solidity demo infra, RPC, AWS for control proofs, Cloud Code buffer | Uniswap prize (June 11) | Primary claim |
| Brand surface | `squarep.finance` domain + email, Vercel host, X Basic | Shared: hackathon credibility + paper + grants | Small fixed cost |
| Research-paper data | Paid Colombian macro feeds | Paper / grants | **Deferred** — out of cycle |
| Operating buffer | Cross-vendor float so jobs don't die | All channels (continuity) | Explicit 18.75% of envelope |

## 4. Recovery-channel mapping rationale

**Uniswap hackathon (June 11)** — concentrated, single-shot remuneration.
Funds: Solidity prototype, demo UI, on-chain data (Alchemy/RPC), control-proof
compute (AWS bursts), agent compute (Cloud Code).

**Research paper / grants** — diffuse, longer horizon. Funds: paid Colombian
macro data when paper deadline becomes concrete. Not in this cycle.

**Shared overhead (brand surface)** — `squarep.finance` domain, Cloudflare
email routing, Vercel hobby site, X Basic — serves both channels at low total
cost. Built now because the hackathon submission benefits from a public
landing page and an X account with 4+ weeks of post history before judging.

## 5. May 2026 allocation (cap $400 new spend)

Today is 2026-05-08; May has ~3 weeks of remaining spend. Existing $17
Cloud Code session credit covers early-May agent work; first new top-up
likely mid-to-late May.

| Line | Amount | Rationale |
|---|---|---|
| `squarep.finance` domain (annual, paid May) | ~$50 | One-time annual; `.finance` TLD ~$30–80 (Cloudflare ~$45) |
| X Basic | $8 | Start posting cadence now to seed before June 11 |
| Vercel Hobby | $0 | Free tier sufficient for hackathon demo site |
| Email (Cloudflare Email Routing → Gmail; Resend free for outbound) | $0 | Skip Workspace seat; hackathon-volume appropriate |
| Alchemy Free tier | $0 | Sufficient until rate limits hit during demo polish |
| AWS | $0 | Don't spin up until a control-proof job is queued |
| Cloud Code top-up (contingent, when $17 session depletes) | $100 | Fires when balance < $10; likely mid-to-late May |
| Hackathon-discretionary slack | ~$242 | Unallocated; absorbs unexpected May needs and rolls forward |
| **May spend ceiling** | **$400** | |
| **May spend floor** (if Cloud Code top-up defers to June) | **$58** | Domain + X only |

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
| X Basic | $8 | Recurring |
| Vercel Hobby | $0 | Still free |
| Email infra | $0 | Cloudflare + Resend stay free |
| Alchemy Growth | $49 | **Committed** (was conditional) — removes RPC-throttling risk in polish week |
| AWS control-proof bursts | $100 | **Committed budget** (was $50–100 conditional) — symbolic verification headroom |
| Cloud Code top-up (contingent, if needed) | $0–100 | Only if May top-up depletes before June 11 |
| Submission-week emergency reserve (June 4–11) | $50 | Last-week bug fixes, surprise paid tooling |
| Hackathon-discretionary slack | ~$93–193 | Absorbs Cloud Code top-up if it fires; rolls forward otherwise |
| **June spend ceiling** | **$400** | |
| **June spend floor** (no Cloud Code top-up) | **$207** | Predictable committed lines only |

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
| X Premium upgrade ($8 → $16) | Single thread crosses ~5k impressions; checkmark becomes ROI-positive |
| Workspace email seats ($6/mo) | Second team member joins, OR judges start emailing alias regularly |
| Vercel Pro ($20/mo) | Demo site needs custom analytics, password protection, or team seat |
| AWS commitment plans | Compute usage stable across 2+ months |
| LinkedIn Premium / sponsored | B2B-grant pipeline opens |

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
| Cloud Code top-ups (contingent — likely 1, possibly 2) | $0–100 | $0–100 | $100–200 |
| Submission-week reserve | $0 | $50 | $50 |
| Discretionary slack | $242–342 | $93–193 | $335–535 |
| **Total per month ceiling** | **$400** | **$400** | **$800** |
| **Total per month floor** | **$58** | **$207** | **$265** |

**Realistic point estimate** (one Cloud Code top-up across cycle, full
committed June infra used, ~$100 of slack absorbs misc surprises):
**~$465 of $800** = **58% utilization**, ~$335 underspend rolling to
post-hackathon cycle.

Underspend is **expected and intentional**, not a planning failure. The
$335 rolling forward is what funds the *next* cycle's first-look at paid
Colombian macro data once the paper deadline becomes concrete.

## 11. Decision points needing live confirmation

- [ ] X tier: Basic ($8) recommended; upgrade to Premium ($16) override-able
- [ ] Domain registrar: Cloudflare Registrar (~$45/yr) recommended; Namecheap or
      Porkbun comparable
- [ ] Email outbound: Resend free tier (3k/mo) recommended; alternatives
      Postmark, AWS SES if Resend's deliverability proves weak

## 12. Out of scope for this memo

- The hackathon project's *technical* design (Solidity scope, demo
  architecture) — separate spec.
- The research paper's submission target and editorial timeline — separate
  doc.
- Legal entity / tax handling for hackathon prize money — premature; revisit
  if/when prize is awarded.
- Post-hackathon cycle (July+) budget — separate memo when this cycle closes.
