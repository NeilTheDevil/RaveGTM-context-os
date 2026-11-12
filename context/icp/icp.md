# Rave — Ideal Customer Profile

Source: `context/docs/source/icp-and-offer-digest.md` (Outbound Strategy Brief, July 2026),
`context/docs/state.md` (measured rates through 2026-10-03), and the research in
`context/docs/research/`. Last updated 2026-11-13.

## In one line

US owner-run local service businesses with **high job values**, **real customer reviews**
and **a website that undersells them**, in trades that web agencies email less often.

## The five layers

| Layer | Rave's ICP | Source |
|---|---|---|
| 1. Firmographic | US, owner-operated local trade, 1-25 staff, job value $2k-$30k+, independent (not a franchise), priority verticals below | Internal: brief digest; franchise rates measured (decision log #24-28) |
| 2. Technographic | Has a website that undersells them: no HTTPS, copyright footer 2022 or older, or PageSpeed mobile score under 50. Listed on Google Maps. Builder (Wix/GoDaddy) is a weak marker: under 1% of the clean pool (open item 6) | `signal-matrix.md` U2-U5; `research/signals-and-market.md` |
| 3. Intent signals | Strong reviews (4.5+ rating, 25+ reviews) with a weak site; storm, freeze or flood events in their county; the weeks before their busy season | `signal-matrix.md` priority signals |
| 4. Persona | The owner decides and pays. Office manager or spouse often reads the inbox first | `personas.md` |
| 5. Engagement readiness | Recent reviews (busy now, so more people are checking them out); business email on a work domain, not Gmail; owner named in the listing | `signal-matrix.md` U8; state.md (owner-email pivot, decision 38) |

**Challenge pass (sceptical sales lead, 2026-11-13).** Weakest part: "a website that undersells
them" was a feeling, not a filter. Fixed by tying layer 2 to three checks a script can run. Still
weak, and left as open questions: roofing ticket size is inferred, and nobody has measured how
many strong-review businesses actually have weak sites.

## Firmographics

| Attribute | ICP | Why |
|---|---|---|
| Geography | United States only | CAN-SPAM permits B2B cold email with unsubscribe. Canada (CASL) and UK (PECR) are blocked until consent and footer rules are settled |
| Business type | Local service trade, sells to homeowners | Jobs come from people searching Google in a hurry |
| Owner | Owner-operated, owner reads the inbox | Owner-run businesses reply about 3x as often as employees of bigger firms (brief's claim; **Likely**, not measured by Rave yet) |
| Size | 1 to 25 staff, single location or small multi-location | Too small for an in-house marketer, big enough to pay $2,000 |
| Job value | $2,000 to $30,000+ per job | A $2,000 site is small against one job |
| Google presence | Listed on Google Maps with reviews | Reviews are the personalization fuel and the proof the business is real |
| Website | Has a site that is dated, slow, templated or hides the reviews | The pitch is "not broken, but losing you jobs" |
| Not a franchise | Independent owner | Franchise sites are controlled by corporate; owner can't buy |

## Vertical ranking

Scored 1-5 on job value, urgency, weakness of competitors' sites, owner reachability, and how
little agency competition exists (max 25). 20+ go first.

| Priority | Vertical | Score | Status (state.md) |
|---|---|---|---|
| 1 | Foundation / waterproofing | 23 | Not started |
| 1 | Water damage / restoration | 22 | **Live since 2026-08-30**, 2,872 loaded, pool exhausted |
| 1 | Moving companies | 22 | Copy written, not live |
| 1 | Tree service / removal | 22 | 1,252 clean, not enriched |
| 1 | Fencing & decking | 21 | 685 fence + 482 deck clean, not enriched |
| 1 | Roofing | 20 | **Live since 2026-09-20**; 956 named owner emails pending load |
| 1 | Paving / concrete / driveways | 20 | 637 concrete + 418 paving clean |
| 2 | Vehicle wrapping, driving schools, pool builders | 19-20 | Later |
| 2 | HVAC, pest control, landscaping | 18 | Later: inboxes flooded by agencies |
| 3 | Plumbing, auto detailing | 17 | Later |

**Why HVAC and plumbing are not first:** they are the most-emailed local businesses. Every web
agency and lead-gen shop hits them. Go where it is quiet first, return once messaging is proven.

## Anti-ICP (skip)

| Who | Why |
|---|---|
| Franchise locations (Servpro, PuroClean, ServiceMaster, Paul Davis, Restoration 1...) | Corporate controls the site. Water damage runs **45-46% franchised**, roofing and tree service **~12-24%** (measured, decision log #24-28) |
| Owners retiring or selling | No reason to invest |
| Already fully booked | Pitch doesn't land |
| Personal Gmail/Yahoo/iCloud as the business address | Kept out of campaign one to protect new sending domains (decision 22) |
| Outlook-hosted inboxes | Neil filters these in the sequencer, never at list-build |
| Non-US | Compliance, see above |

## Measured list economics (Confirmed, `context/docs/state.md`)

```
maps scrape              $1.00 / 1,000 businesses
business email find      $0.005    owner email find $0.02
owner email hit rate     20.9% water damage · 13% roofing
clean -> sendable        ~28%
cost per sendable lead   $0.014 - $0.025
```

## Open questions

- Roofing ticket size was inferred, never measured (open item 16).
- "Your site needs improving" is unverified at scale: under 1% of the clean pool runs
  Wix/Squarespace (open item 6). A 20-minute spot check of live sites would settle it.
