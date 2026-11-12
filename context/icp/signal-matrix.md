# Rave — Signal Matrix

**Status:** WORK IN PROGRESS, built 2026-11-13 by an agent in a non-interactive run. Not reviewed by
Neil yet. Every approval gate in `/signal-matrix` was decided by the agent; see
"Decisions made without review" at the bottom. Method: `knowledge-base/playbooks/signal-matrix-framework.md`.

Labels: **Confirmed** = checked in a repo file or a source fetched by the research agent (path given).
**Likely** = consistent with sources, not checked at primary level. **Unverified** = no source; do not quote.

## Read this first

1. The strongest signal Rave can build today is **strong Google reviews + a weak website**, read from
   Localpipe fields plus one free site fetch. It is a STATE signal (true for months), not an event. The
   only real time-bound event in reach is **weather** (NOAA / NWS / FEMA), and it only fits five verticals.
2. Rave does **not** use Clay, Apollo, LinkedIn or any people database for these trades. Every lead comes
   from Google Maps through Localpipe (`CLAUDE.md`; `context/docs/state.md`: "Localpipe only"). So the
   course's universal B2B signals (hiring via Apollo, new leadership, headcount growth, funding) are
   killed below, with the reason.
3. No site-quality check is built yet. `tools/localpipe-pipeline/` has no PageSpeed, HTTPS or copyright
   check (Confirmed: grep of `scripts/` and `engine/`, 2026-11-13). Every site-gap signal below is a
   spec, not a working column.
4. Volume per cell is **Unverified** until a site-check pass runs on a pool. The open question it settles
   is open item 6 ("your site needs improving" is unverified at scale).

---

## Phase 0: Company understanding (agent's summary)

| | |
|---|---|
| What Rave sells | A finished, conversion-focused website for a local trade, shown before purchase, built in days. $2,000 one-time + $97/mo care plan. One person, not an agency (`context/messaging/facts.md`, Confirmed) |
| Pain solved | The owner's reputation is earned (reviews, referrals) but the site undersells it, so some homeowners who search Google go elsewhere (`context/icp/icp.md`; the loss itself is Likely, not measured by Rave) |
| Who buys | The owner of a US, owner-run local trade, 1 to 25 staff, $2,000 to $30,000+ jobs (`icp.md`) |
| Market | United States only (CAN-SPAM). Canada and UK blocked (open item 15) |
| Competitors | Trade marketing agencies (Scorpion, Hibu, Thryv, Roofing Webmasters), DIY builders (Wix, Squarespace, GoDaddy), low-cost subscriptions (Rebolt), freelancers. Rave's gap: "see the finished sample before paying, flat price, no lock-in" (`context/docs/research/competitors.md`) |
| Products | Single product. Matrix 1 therefore has no product columns; the angle changes per cell instead |

## Phase 1: Matrix 1, segments

### 1a. Wide net (all buyer groups considered)

US owner-run local trades that sell to homeowners and are listed on Google Maps with reviews:
foundation / waterproofing, water damage restoration, moving, tree service, fencing, decking,
roofing, paving, concrete, vehicle wrapping, driving schools, pool builders, HVAC, pest control,
landscaping, plumbing, auto detailing (`icp.md` vertical ranking). Adjacent groups considered and left
out: franchises (corporate owns the site), multi-state chains (agency already in place, Likely),
B2B trades (not the homeowner-search pain).

### 1b. Axes chosen

- **Columns: vertical**, the seven priority-1 verticals in `icp.md` (score 20+). Fencing and decking are
  one column, paving and concrete are one column, matching the scrape categories already held.
- **Rows: website state**, read from the Localpipe `website` field plus one free fetch of the homepage:
  - **A. No website**: Localpipe `website` empty (`has_website: false` filter).
  - **B. Weak website**: a site exists and at least one site-gap check fires (no HTTPS, footer year
    2022 or older, PageSpeed mobile performance under 50). Definitions in Matrix 2.
  - **C. Current website**: a site exists and no check fires.

Why these axes: the website state is what decides fit and message (A = "you have nowhere to send
people", B = "not broken, but losing you jobs", C = little to say). It is observable without a person
looking, the rows do not overlap (A has no site; B and C split on a fixed rule), and every row is
actionable. Volume per cell is the weak rule: unknown until checks run.

### 1c. Grid

All cells share the ICP box: US, independent (franchise filter `scripts/filter_franchises.py` applied),
Localpipe rating 3.5+ and 10+ reviews at scrape, owner-run. **Company examples:** none are named in this
file. Rave holds real scraped businesses for most cells under the gitignored `runs/` folder, and
`CLAUDE.md` rule 6 forbids committing prospect names. Each cell instead gives the exact Localpipe pull.

| Vertical (Localpipe `query` string) | Pool held today (`state.md`, Confirmed) | A. No website | B. Weak website | C. Current website |
|---|---|---|---|---|
| Foundation / waterproofing (`waterproofing company`, `damp proofing service`) | None scraped. Not started | Medium. Unknown pool | **High** if the pool exists; score 23 is the top in `icp.md` | Low |
| Water damage (`water damage restoration service`) | ~150 left; 92% of leftovers are franchise | Low. Pool exhausted | Low. Pool exhausted, 45% franchise | Low |
| Moving (`moving company`, `mover`) | Not stated in `state.md`; Neil's copy written, not live | Medium | **High**. Copy exists to compare against | Low |
| Tree service (`tree service`) | 1,252 clean, not enriched | Medium | **High**. Largest unused non-roofing pool, 12% franchise | Low |
| Fencing & decking (`fence contractor`, `deck builder`) | 685 fence + 482 deck clean, not enriched | Medium | **High** | Low |
| Roofing (`roofing contractor`) | ~6,460 clean not enriched; ~800 + 956 loaded or pending | Medium | **High**, but roofing copy is Neil's to write and roofing is already live | Low |
| Paving & concrete (`paving contractor`, `concrete contractor`) | 418 paving + 637 concrete clean | Medium | **High** | Low |

Row-level priority reasoning:
- **B (weak site) is the main row.** It is the offer's premise in one read, and the copy can show the
  homework honestly ("Chrome marks your site Not secure").
- **A (no website)** is the cleanest need, but Localpipe's `/enrich` takes a `business_website` and the
  email hit rate without one is Unverified (likely low). Second priority, test small.
- **C (current site)** is deprioritized. Nothing deterministic to say; volume play only.

## Phase 2: Assess and prioritize

Scores High / Medium / Low. US data, so penetrability is high wherever Localpipe returns emails.

| Cell | Signal density | Product fit | Penetrability | Rank |
|---|---|---|---|---|
| B × Tree service | High (all universal site checks + storms) | High | High (1,252 held; email hit Unverified, roofing's 13% is the nearest measured proxy) | **1** |
| B × Roofing | High (site checks + hail/wind) | High | High (largest pool) | 2 (held for Neil: his copy, live campaign) |
| B × Fencing & decking | High (site checks + wind) | High | High (1,167 held) | 3 |
| B × Paving & concrete | Medium (site checks, no event) | High | High (1,055 held) | 4 |
| B × Foundation / waterproofing | High (site checks + heavy rain / flood) | High (score 23) | Unknown (nothing scraped) | 5 (scrape first, $1 per 1,000) |
| B × Moving | Medium (site checks + season) | High | Medium (pool not counted) | 6 |
| A × any vertical | Low (one read) | High | Low (email find without a site, Unverified) | 7 |

Selected priority cells for Matrix 2: the B row across all seven verticals, with tree service as the
first build. Reason: same build for every column (only the `query` string and the trade word change).

## Phase 3: Matrix 2, signals

### 3a-3b. Every signal with Iron Law detail

Forcing question, adapted: "Could I hand this to someone running the Localpipe pipeline RIGHT NOW with
zero ambiguity?" Rave's equivalent of "Clay action" is the **build** column: a Localpipe field, a script
step on the free homepage fetch, or a free public dataset. Costs in dollars.

| # | Signal | Type | Data source | Build | Key filter | Volume estimate | Cost | Status |
|---|---|---|---|---|---|---|---|---|
| U1 | Strong reviews | STATE | Localpipe `/maps-search` fields `rating`, `review_count` | Server-side filter `min_rating`, `min_reviews`; then local filter | rating ≥ 4.5 AND review_count ≥ 25 | Unverified share of each pool; 0 extra cost to measure on data held | $0 (in scrape) | VERIFIED (fields Confirmed in `localpipe-api-notes.md`) |
| U2 | No HTTPS | STATE | One GET of `website` | Request `https://<domain>`; fail if TLS error, no response, or redirect to `http://` | boolean | Unverified | $0 | VERIFIED (method); not built |
| U3 | Stale footer year | STATE | Same homepage HTML | Regex `(©|&copy;|copyright)\s*(\d{4})`, take the highest year on the page | year ≤ 2022 | Unverified; many sites print no year, so partial coverage | $0 | VERIFIED (PARTIAL) |
| U4 | Slow on phones | STATE | Google PageSpeed Insights API v5, `strategy=mobile` | Read `lighthouseResult.categories.performance.score` × 100 | score < 50 | Unverified. Quota reported 25,000/day per project (Likely, `signals-and-market.md`). Needs a free Google Cloud API key Neil creates | $0 | VERIFIED (PARTIAL: lab scores vary run to run) |
| U5 | Template builder | STATE | Same homepage HTML | Regex for `wixstatic`, `img1.wsimg.com` (GoDaddy), `weebly`, `squarespace`, `generator` meta tag | builder in list | Under 1% of the clean pool runs Wix/Squarespace (open item 6, Confirmed) | $0 | VERIFIED (COMPOUND, context only; too rare and a template site can be fine) |
| U6 | **Strong reviews + weak site** (composite) | STATE | U1 AND (U2 OR U3 OR U4) | Join of the above per row | as above | Unverified; the first site-check pass on tree service sets it | $0 | VERIFIED (COMPOUND). **Mother intent of the first workflow** |
| U7 | No website | STATE | Localpipe `website` empty | `has_website: false` at scrape | boolean | Unverified | $1 / 1,000 scraped | VERIFIED; email find without a site is Unverified |
| U8 | Recent reviews (busy now) | EVENT proxy | Localpipe `/scrape-reviews-api` (free), `review_time` | Count reviews whose `review_time` reads "a week ago" to "3 months ago" among the 40 newest | 5+ in last 3 months | Unverified | $0 (counts against request limits only, Confirmed) | VERIFIED |
| U9 | Review mentions reaching or finding them | STATE | Same review pull, `review_text` | Keyword regex: `website`, `couldn't reach`, `call back`, `hard to find` | ≥ 1 match | Low (Likely) | $0 | VERIFIED (PARTIAL); weak link to the website |
| N1 | Hail / high wind in the county | EVENT | NOAA Storm Events (free CSV, data lags; Confirmed in research), NWS alerts API (real time, Likely), FEMA OpenFEMA declarations (Confirmed) | Localpipe `latitude`/`longitude` → county FIPS (free Census geocoder) → join to events in last 60 days | event type Hail ≥ 1", Thunderstorm Wind, Tornado | Seasonal; spring-summer heavy (Likely) | $0 | VERIFIED. Roofing, tree, fencing |
| N2 | Hard freeze / flood | EVENT | NWS freeze warnings, FEMA declarations | Same county join | warning or declaration in last 30 days | Seasonal, winter | $0 | VERIFIED. Water damage, foundation |
| N3 | Heavy rain / flood season | EVENT | NOAA Storm Events `Flood`, `Heavy Rain` | Same county join | event in last 60 days | Seasonal | $0 | VERIFIED. Foundation / waterproofing |
| N4 | Moving season ahead | EVENT (calendar) | Calendar; peak May to August for one national mover (Likely, `signals-and-market.md`) | Send window Feb to Apr | date | All movers | $0 | VERIFIED as timing only |
| K1 | Running Google Ads | EVENT/STATE | Google Ads Transparency Center | No official API; scraping unverified; LSA coverage unconfirmed | | Thin among small operators | $0 | **KILLED** for now: manual research only. Keep as a hand spot-check on replies |
| K2 | Hiring crews | EVENT | Indeed / Google Jobs | No free API; matching a posting to a Maps listing is messy | | Low | | **KILLED**: fails the forcing question |
| K3 | New business registration | EVENT | State Secretary of State filings | Formats differ per state; LLC shells | | | | **KILLED** for now: engineering heavy |
| K4 | Domain expiry | EVENT | RDAP / WHOIS | Many registrars redact dates | | | | **KILLED**: unreliable |
| K5 | New location | EVENT | No clean detector | | | | | **KILLED** |
| K6 | Hiring via Apollo, new leadership, headcount growth, LinkedIn engagement | EVENT | Clay / Apollo / LinkedIn | Rave does not use Clay or LinkedIn databases for these trades; owner-run trades are thinly covered there (Likely) | | | | **KILLED**: wrong data source for this market |
| K7 | Fundraising | EVENT | Crunchbase | Not a VC market | | | | **KILLED** |

### 3c. Universal vs niche-specific

- **Universal (build once, swap the `query` string):** U1 to U9. Nine of thirteen live signals.
  One site-check script plus one review pull serves every vertical.
- **Niche-specific:** N1 to N4. Each is one free public dataset joined by county.
- The compounding point for Rave: the whole site-gap engine is one script on the homepage fetch.
  Adding a vertical costs one $1-per-1,000 scrape and a new trade word in the copy.

### 3d. Matrix 2 grid (signal × priority segment)

Play = how the signal is read for that segment. Product is always the same (the redesign), so the
product column is dropped (single-product company).

| Type | Signal | Tree service | Roofing | Fencing & decking | Paving & concrete | Foundation / waterproofing | Moving | Water damage |
|---|---|---|---|---|---|---|---|---|
| Universal | U6 Strong reviews + weak site | Mother intent, workflow 1 | Same build (Neil's copy) | Same build | Same build | Same build after first scrape | Same build | Same build, pool exhausted |
| Universal | U2 / U3 / U4 site reads | Routers in workflow 1 | Same | Same | Same | Same | Same | Same |
| Universal | U7 No website | Separate small test | Same | Same | Same | Same | Same | Same |
| Universal | U8 Recent reviews | Context only | Same | Same | Same | Same | Same | Same |
| Niche | N1 Hail / wind | Storm cleanup demand | Hail and wind roof claims | Wind-damaged fences | n/a | n/a | n/a | n/a |
| Niche | N2 Freeze / flood | n/a | n/a | n/a | n/a | Flood declarations | n/a | Pipe-burst freeze |
| Niche | N3 Heavy rain | n/a | n/a | n/a | n/a | Wet-basement calls | n/a | Flood calls |
| Niche | N4 Season ahead | Spring work starts April (Likely) | Spring (Likely) | Spring (Unverified) | Spring (Unverified) | Spring rain (Unverified) | May to Aug peak (Likely) | n/a |

### Angle matrix (signal × segment → messaging angle)

Angles are meaning, not copy lines. Every angle respects `facts.md`: flatter the work, point at the
site, never the owner; offer to show a design for the trade, never claim one is built for them.

| Signal | Tree service | Roofing | Fencing & decking | Paving & concrete | Foundation / waterproofing | Moving | Water damage |
|---|---|---|---|---|---|---|---|
| U6 + U2 No HTTPS | Homeowners get a browser warning before they can ask for a tree quote | Same warning in front of a roof quote form | Warning on the page where people ask for a fence quote | Warning before a driveway quote | Warning when a worried homeowner checks the basement fix | Warning on the moving quote form people fill in at night | Warning during an emergency search |
| U6 + U3 Old footer year | Reviews are recent, the site looks like it stopped in 20XX; homeowners compare both | Same: recent roof reviews vs a site that looks left alone | Same, with project photos as the thing people want to see | Same | Same | Same | Same |
| U6 + U4 Slow on phones | People call tree services from their phone after a storm; a slow page loses the tap | Storm searches happen on phones | People browse fence styles on their phone | Same | Same | People get moving quotes on phones | Emergency searches on phones |
| U7 No website | Plenty of reviews, nowhere to send people who want to see the work | Same | Same, photos matter most | Same | Same | Same | Same |
| N1 Hail / wind | After the storm, the next homeowners will Google before they call | Hail hit the county; homeowners will compare roofers online | Wind-down fences, same comparison | n/a | n/a | n/a | n/a |
| N2 / N3 Freeze, flood, rain | n/a | n/a | n/a | n/a | Wet season brings the searches; is the site ready | n/a | Freeze season, same |
| N4 Season ahead | Get the site done in the slow months before spring (Assumed timing) | Same | Same | Same | Same | Fix it before peak moving season | n/a |
| U8 Recent reviews (context only) | Busy lately, more people reading those reviews and clicking through | Same | Same | Same | Same | Same | Same |

## Phase 4: Matrix 3, workflow tracker

| W # | Status | Workflow name | Mother intent | Campaigns | Industry | Channel | Copy URL | Total leads |
|---|---|---|---|---|---|---|---|---|
| 1 | Planned (spec + copy drafted) | Strong reviews, weak website | U6 | 3 (one per site finding) | Tree service first | Email | `output/campaigns/strong-reviews-weak-website/` | |
| 2 | Planned | No website on Maps | U7 | | Any priority vertical | Email | | |
| 3 | Planned | Storm-hit county | N1 (+ U6 as filter) | | Roofing, tree, fencing | Email | | |
| 4 | Planned | Freeze and flood season | N2 / N3 (+ U6) | | Water damage, foundation | Email | | |
| 5 | Planned | Before the busy season | N4 (+ U6) | | Moving, then spring trades | Email | | |

Other tracker columns (launch date, persona, enrichment layers, iteration, changelog, steps, emails
sent, progress, bounce) are empty until a campaign launches. Google Sheets push skipped: no
`WORKFLOW_TRACKER_SPREADSHEET_ID` checked, and this run touches no external systems.

## Summary

- Segments: 7 verticals × 3 website states = 21 cells. Priority row: B (weak website).
- Signals: 13 live (9 universal, 4 niche-specific), 7 killed with reasons.
- Workflows planned: 5. Workflow 1 is specced in `output/campaigns/strong-reviews-weak-website/workflow-spec.md`.

## Steelman against this matrix

Most of it is STATE, not timing. A bad site can sit for years while the owner stays busy from referrals
and Google Business Profile. The course's checklist item "signals indicate TIMING" is met only by N1 to
N4. If site-gap volume replies no better than Neil's broad copy, the next move is to lead with weather
(workflow 3) and use the site gap only as a filter. What would change the plan: the first site-check
pass showing that most strong-review tree services have current sites (then row B is thin and row A or
weather leads).

## Decisions made without review

1. **Axes: vertical × website state.** Chosen over "lead source" or "size" because website state is
   what the offer turns on and it is readable from a fetch. Neil may prefer review strength as the row.
2. **No company names in the grid.** The skill asks for 5 to 15 real names per cell via web search.
   Rave already holds the real names in gitignored `runs/`, and `CLAUDE.md` rule 6 bans prospect names
   in committed files. Each cell gives the exact Localpipe pull instead.
3. **"Clay action" replaced by a build column** (Localpipe field, script on the homepage fetch, public
   dataset), because Rave does not use Clay for these trades.
4. **Thresholds set by the agent, not measured:** rating ≥ 4.5 and reviews ≥ 25 for "strong";
   footer year ≤ 2022 for "old"; PageSpeed mobile < 50 for "slow". All three should be re-set after the
   first pass shows the distribution.
5. **Template builder (U5) demoted to context only**, because open item 6 found under 1% of the pool on
   Wix/Squarespace and a template site can be fine.
6. **Google Ads (K1) killed for automation** until an Ads Transparency Center method is verified.
7. **Priority cells:** the B row across all verticals, tree service first. Roofing ranked high but held,
   because roofing copy is Neil's to write and roofing is live.
8. **Google Sheets push skipped.**
