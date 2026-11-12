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

## Signals: the 5 to build first

| # | Signal | Data source → tool | Why it means "now" |
|---|---|---|---|
| 1 | Strong reviews (4.5+, 25+) + weak website | Google Maps → Localpipe; homepage fetch; PageSpeed API | Reputation has outgrown the site; a fact the owner can check |
| 2 | Hail or high wind in their county | NOAA / NWS / FEMA, free | Homeowners compare contractors online after a storm |
| 3 | Freeze, flood or heavy-rain season | NWS / FEMA / NOAA, free | Emergency searches spike for restoration and basements |
| 4 | Busy season ahead | Calendar per trade | Slow months are when owners have time to fix the site |
| 5 | No website on Google Maps | Localpipe `website` empty | Reviews with nowhere to send people (small test) |

Each scored on the four tests (buying reason, volume, data access, story):
[`context/icp/signal-matrix.md`](context/icp/signal-matrix.md)

## System architecture

```
Context OS → Signals → Find companies (Localpipe) → Enrich (reviews, site checks, PageSpeed)
→ ICP fit check (franchise, rating, US) → Route by site finding → Owner name + email (Localpipe)
→ Sequence (PlusVibe, 24 inboxes) → Reply handling (template + Calendly) → CRM (HubSpot, planned)
→ Weekly feedback into this repo
```

Every step with its tool and decisions: [`context/docs/gtm-system.md`](context/docs/gtm-system.md)

## Target workflow: Strong reviews, weak website (tree service first)

- **Mother intent:** a tree service with strong Google reviews whose website shows a fact that loses
  homeowners (Not secure warning, an old footer year, or slow on phones).
- **ICP filter:** rating ≥ 4.5, reviews ≥ 25, not a franchise, US, site loads.
- **Routing:** first failed check decides the campaign: Not secure → Old footer → Slow on phones.
- **Copy:** 3 emails over 7 days per route, facts-gated (no borrowed results, no "your site is
  already built" claims), PlusVibe export ready.
- **Status:** STRUCTURE-APPROVED by the agent, pending Neil's review. Before sending: build the
  tree-service sample at a live link and measure the thresholds on a real list.

Spec: [`output/campaigns/strong-reviews-weak-website/workflow-spec.md`](output/campaigns/strong-reviews-weak-website/workflow-spec.md)

## More

Positioning, messaging and competitors: [`context/positioning/`](context/positioning/),
[`context/messaging/`](context/messaging/) · 26 campaign ideas:
[`output/campaigns/campaign-strategy.md`](output/campaigns/campaign-strategy.md) · Lessons:
[`knowledge-base/learnings/`](knowledge-base/learnings/)
