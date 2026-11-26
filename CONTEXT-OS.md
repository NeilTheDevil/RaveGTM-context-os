# Rave GTM Context OS — the one-page reference

The living reference file for Rave's GTM system: ICP, signals, architecture and target workflow
in one place. Each section links to the full file. Read `CLAUDE.md` for how the folders work.
Last updated 2026-11-13.

## Company

**Rave** (ravegtm.com) builds websites for US owner-run local trades. It cold-emails owners, offers
to show a finished design for their trade free, and has the real site live within a week.
**$2,000 build + $97/mo care plan.** One person, founder Neil Uko. Cold email live since August 2026
(water damage, roofing). Facts: [`context/docs/research/company.md`](context/docs/research/company.md)

## ICP

**US owner-operated local trades (1-25 staff, $2k-$30k+ jobs, not franchises) whose Google reviews
are stronger than their website.**

| Layer | Rave |
|---|---|
| Firmographic | US, owner-run, 1-25 staff, independent. Verticals first: foundation/waterproofing, water damage, moving, tree service, fencing/decking, roofing, paving/concrete |
| Technographic | Listed on Google Maps; website with no HTTPS, a 2022-or-older footer, or a slow mobile score |
| Intent signals | Strong reviews + weak site; storm/freeze/flood in their county; busy season ahead |
| Persona | The owner decides and pays; office manager or spouse often reads the inbox |
| Engagement readiness | Recent reviews, work-domain email, owner named in the listing |
| Not a fit | Franchises (water damage is 45% franchised), retiring owners, fully booked, Gmail-only businesses, non-US, HVAC/plumbing for now (most-emailed inboxes) |

Full: [`context/icp/icp.md`](context/icp/icp.md) · Personas: [`context/icp/personas.md`](context/icp/personas.md)

**TAM (Clay company search, US HQ, 1-50 staff):** tree service 886 · foundation/waterproofing 3,538 ·
fencing/decking 13,034 · roofing 18,956+ · water damage 18,150+ · paving/concrete 19,222+ (≈60,900+, a
floor: Google Maps finds more of these businesses). Tree service saved as a Clay Audience: **837**.
[`context/docs/research/tam-clay-search.md`](context/docs/research/tam-clay-search.md)

## Signals: the 5 to build first

| # | Signal | Data source → tool | Why it means "now" |
|---|---|---|---|
| 1 | Strong reviews (4.5+, 25+) + weak website | Google reviews (Clay or Localpipe); homepage scrape; AI site-gap check (reviews not shown, no click-to-call, no quote request) | Reputation has outgrown the site; a fact the owner can check. In the Clay test, 25 of 28 ready rows show none of their reviews on the homepage |
| 2 | Hail or high wind in their county | NOAA / NWS / FEMA, free | Homeowners compare contractors online after a storm |
| 3 | Freeze, flood or heavy-rain season | NWS / FEMA / NOAA, free | Emergency searches spike for restoration and basements |
| 4 | Busy season ahead | Calendar per trade | Slow months are when owners have time to fix the site |
| 5 | No website on Google Maps | Localpipe `website` empty | Reviews with nowhere to send people (small test) |

Each scored on the four tests (buying reason, volume, data access, story):
[`context/icp/signal-matrix.md`](context/icp/signal-matrix.md)

## System architecture

```
Context OS → Signals → Find companies (Localpipe or Clay search) → Clay Audiences (TAM segment)
→ Enrich (Google reviews, homepage scrape, AI fit + site-gap checks) → ICP Fit (franchise, rating, US,
independent) → Route by site gap → Email (homepage, Hunter, ZeroBounce) → Sequence (PlusVibe)
→ Reply handling (template + Calendly) → CRM (HubSpot, via Clay webhook) → Weekly feedback into this repo
```

Every step with its tool and decisions: [`context/docs/gtm-system.md`](context/docs/gtm-system.md)
HubSpot pipeline stages and lifecycle definitions: [`context/docs/pipeline.md`](context/docs/pipeline.md)

## Target workflow: Strong reviews, weak website (tree service first)

- **Mother intent:** a tree service with strong Google reviews whose website shows a fact that loses
  homeowners (Not secure warning, an old footer year, or slow on phones).
- **ICP filter:** rating ≥ 4.5, reviews ≥ 25, not a franchise, US, site loads.
- **Routing:** first failed check decides the campaign: Not secure → Old footer → Slow on phones.
- **Copy:** 3 emails over 7 days per route, facts-gated (no borrowed results, no "your site is
  already built" claims), PlusVibe export ready.
- **Built in Clay (2026-11-21):** 100 rows → 99 pass free checks → 60 strong reviews → 38 ICP Fit
  (independent tree services) → **28 Ready** (C4 reviews not shown 25, C2 old footer 2, C6 no quote
  request 1) → 20 emails → **9 Send Ready**. 79.4 credits. Website signal is the AI site-gap check
  (Neil, 2026-11-21). [`clay-build/README.md`](output/campaigns/strong-reviews-weak-website/clay-build/README.md)
- **Before sending:** build the tree-service sample at a live link; write copy for C4-C6.

Spec: [`output/campaigns/strong-reviews-weak-website/workflow-spec.md`](output/campaigns/strong-reviews-weak-website/workflow-spec.md)

## More

Positioning, messaging and competitors: [`context/positioning/`](context/positioning/),
[`context/messaging/`](context/messaging/) · 26 campaign ideas:
[`output/campaigns/campaign-strategy.md`](output/campaigns/campaign-strategy.md) · Lessons:
[`knowledge-base/learnings/`](knowledge-base/learnings/)
