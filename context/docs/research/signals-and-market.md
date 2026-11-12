# Buying signals and market urgency: local trade website redesign (Rave GTM)

Written 2026-11-13. Stats, prices and API quotas change; re-check before quoting in copy.

## Summary (5 lines)
1. Best build-first signals are all free and derivable from the LocalPipe row plus one site fetch: site quality (PageSpeed + HTTPS + copyright year + builder), no website, strong reviews with weak site, storm/disaster events, and running ads.
2. The strongest cited market fact: 54% of consumers visit a business website after reading positive reviews, 97% read reviews (BrightLocal 2026, Confirmed). No primary Google stat on homeowners checking a contractor site was found (Unverified).
3. Most signals are "state" signals (always true) not "event" signals (time-bound). Only storms, hiring, new GBP/registration, ads starting, review spikes and domain expiry are real events; the rest are qualification filters.
4. Seasonality: outreach should land about 4 to 8 weeks before spring (Feb to Mar) for roofing, tree, fencing, paving, moving; restoration and foundation are event driven. Data is mostly contractor blogs (Likely, not Confirmed).
5. Biggest caveat: a bad site does not equal intent to buy; owner-run trades get leads from GBP and referrals and may not care. Treat all signals as ranking, not proof.

## Labels
Confirmed = source fetched this session (URL given). Likely = consistent with search results or common knowledge but not fetched at primary level. Unverified = no source found; do not quote.

## 1 and 2. Candidate signals

Type column: STATE = true continuously (a filter). EVENT = time-bound (a true trigger).

| # | Signal | Type | Why it implies urgency | Data source and cost | Refresh | Reliability | Copy angle (one line) |
|---|---|---|---|---|---|---|---|
| 1 | Slow or poor mobile site | STATE | Most local search starts on mobile (BrightLocal, see section 3); a slow site loses the call | PageSpeed Insights API, free. Default quota reported as 25,000 requests/day per project (Likely: only third-party pages found; Google's get-started page did not state quota. Confirm in Cloud Console). Free API key | Re-run monthly | Medium. Lab scores vary run to run; small-site CrUX field data often absent | "Your site scored X on mobile; here is what it costs in missed calls" |
| 2 | No HTTPS / "Not secure" | STATE | Browser warning scares off a homeowner ready to submit a form | Free: request http/https, check cert (curl/Python). Cost 0 | Monthly | High (binary, easy to verify) | "Chrome flags your site as Not secure on the quote form" |
| 3 | Stale copyright year or last-updated footer | STATE | Signals abandoned site to buyers; also easy hook | Free: fetch homepage, regex footer year | Monthly | Medium. Many sites have no year or a static one; false positives from dynamic footers | "Your footer still says 2019" |
| 4 | Dying/weak builder (Wix, GoDaddy Website Builder, Weebly, old WordPress theme) | STATE | Template sites are the natural redesign target; also slow and weak local SEO | Wappalyzer/BuiltWith. BuiltWith free lookup is per-domain; bulk is paid (price Unverified). Free DIY alternative: fetch HTML and grep generator meta tags/script URLs (wixstatic, godaddy, weebly). Cost 0 DIY | Quarterly | Medium to high for builder fingerprint; "dying" is a judgment. Note Weebly is owned by Square (Likely), not shut down as far as found (Unverified) | "Built on a drag-and-drop template; here is what a custom trade site converts" |
| 5 | No website on Google Maps listing | STATE | Business has no owned asset; relies only on GBP | LocalPipe field (website empty). Cost: already in LocalPipe credits | Per pull | High that field is empty; but may have Facebook-only page or site not listed (verify by search) | "You have 140 reviews and nowhere to send people who want to see your work" |
| 6 | Strong reviews, weak site | STATE | Reputation is already earned; site is the leak. Best qualifier | LocalPipe rating + review count joined to PSI/HTTPS/builder score. Cost 0 extra | Per pull | High as a rank score | "4.9 stars from 200 customers, then a site that undersells you" |
| 7 | Review velocity spike | EVENT | Growing, busy or newly investing business, more traffic hitting the site | Needs two LocalPipe pulls over time (diff review count). Cost: second pull credits (price Unverified for this repo). Alternative: Places API (paid, Unverified price) | Monthly diffs | Medium. Spike can be a review-gating campaign or storm season | "You added 30 reviews this quarter; traffic from them lands on this site" |
| 8 | New GBP / new business registration | EVENT | New businesses need a site and have budget intent | State Secretary of State business filings (free in many states, formats differ, scraping effort high; Likely). Cost 0 but engineering heavy | Weekly to monthly by state | Medium. Many filers are LLC shells, not operating trades | "Congrats on the new business; most trades launch with a template. Here is a $2,000 proper one" |
| 9 | New location | EVENT | New market needs a location page and local SEO | Appears as new GBP at a different address under same name; weak free detection (Unverified) | Monthly | Low | "Opening in [city]? Your site needs a page for it" |
| 10 | Hiring (estimators, techs, crew) | EVENT | Growth, cash flow, and a need to look credible to applicants | Indeed postings. Indeed has no free public API for this (Likely); Google Jobs or direct career page scraping is possible. Cost 0 with effort; ToS risk (Unverified) | Weekly | Low to medium; match of posting to the Maps business is messy | "Hiring crews? Applicants check your site first" |
| 11 | Running Google Local Services Ads or Google Ads | EVENT/STATE | Paying for clicks that land on the site; weak site wastes spend | Google Ads Transparency Center (adstransparency.google.com) is free and searchable by advertiser or domain (Confirmed: Google support page via search). Whether LSA appear there was NOT confirmed. Scraping it is not an official API (Unverified). LSA badge visible on Google results (manual) | Weekly | Medium for Search ads; LSA coverage Unverified | "You pay for every click; here is what your landing page does with it" |
| 12 | Storm, hail, flood events | EVENT | Roofing, restoration, tree, fencing demand spikes; owners have pressure to capture calls | NOAA Storm Events Database: free CSV bulk downloads, no key; data through Oct 2025 per NOAA page (Confirmed: ncei.noaa.gov/stormevents). Lag means historical, not same-day. FEMA OpenFEMA DisasterDeclarationsSummaries: free, no key (Confirmed: fema.gov/about/openfema/api). NWS alerts API is free for real time (Likely) | Storm events monthly; FEMA as declared | High for "event happened in county"; low for "this business benefits" | "Hail hit [county] on [date]; the next wave of homeowners will Google you first" |
| 13 | Moving season (calendar) | EVENT (predictable) | Peak is May to August for at least one national mover (see section 4) | Calendar only. Cost 0 | Annual | High as timing, low as individual intent | "Peak season starts in weeks; fix the quote form before it does" |
| 14 | Domain about to expire | EVENT | Neglected site or owner who can be reached when renewing | WHOIS/RDAP: free per lookup (RDAP), rate limits, many registrars redact (Likely). Bulk is poor | Weekly | Low: privacy redaction hides dates for many; expiry may not mean intent | "Your domain renews on [date]; good moment to replace the site" |
| 15 | Recent negative review about not reaching them | EVENT | Direct pain: missed calls and slow response. Not a website problem unless the contact form is broken | Google reviews text via LocalPipe if it provides recent reviews (field availability Unverified) or Places API (paid) | Weekly | Medium on pain, weak link to website | "A recent reviewer could not reach you; a click-to-call, form and chat fix that" |

Not covered by any source here: the true dollar cost of the Wappalyzer/BuiltWith bulk plans, Indeed scraping legality, and Transparency Center LSA coverage. Treat as Unverified.

## 3. Market urgency facts

- 97% of consumers read reviews for local businesses; 41% always do (29% in 2025). Confirmed. BrightLocal Local Consumer Review Survey 2026, published 2026-02-11, 1,002 US adults. https://www.brightlocal.com/research/local-consumer-review-survey/
- 54% visit a business's website after reading positive reviews (32% in 2019). 66% do further research after a positive review, 34% are ready to buy or book. Confirmed, same page.
- 74% want reviews from the last three months; 32% from the last two weeks. 85% more likely to use a business after positive reviews. Confirmed, same page.
- Share of local searches starting on mobile (BrightLocal figure of 73% appeared in a search summary, exact survey and year not checked). Unverified.
- Google-commissioned Ipsos study: 50% of mobile users who did a local search visited a store within a day (about 2014). Likely accurate but very dated; do not use as current. https://www.searchenginewatch.com/article/2343577/Google-Local-Searches-Lead-50-of-Mobile-Users-to-Visit-Stores-Study
- "84% of homeowners search Google before hiring a contractor" (attributed to WatsonCo). Unverified, original not found.
- "Homeowners visit 35 contractor websites" (attributed to Angi). Unverified, implausible-sounding, do not use.
- A 2025 survey of 422 HVAC buyers: about 16.7% go directly to contractor websites. Unverified (single secondary mention).
- Consumers using AI tools to discover local businesses: reported at 45% in 2026 vs 6% in 2025. Unverified at primary level (secondary blogs only; the BrightLocal page fetch did not return it). Do not quote until checked.
- No home-services breakdown of BrightLocal found.

## 4. Seasonality by vertical

No national dataset was found for any trade; sources are contractor marketing blogs and one mover's data. All rows are Likely or Unverified. Region matters (snow belt vs sun belt).

| Vertical | Busy season | Outreach window (suggested) | Evidence |
|---|---|---|---|
| Roofing | Summer busy; winter (Dec to Feb) slow in cold regions; plus storm-driven surges | Jan to Mar, and within days of a hail/wind event | Likely. JobNimbus, ServiceTitan blogs (summary only; the ServiceTitan "40% revenue swing" claim is Unverified) |
| Water damage restoration | Event driven (storms, freezes, pipe bursts); winter freeze and spring storms | Anytime; trigger on freeze/flood events; pre-winter (Oct to Nov) | Likely. No source fetched |
| Foundation / waterproofing | Wet spring and fall rain; inspections before spring sales | Feb to Mar, Aug to Sep | Unverified. No source found |
| Moving | May to August peak; slowest Dec to Feb (one company, 2024 data) | Feb to Apr | Likely. All My Sons Moving & Storage blog (one company only) |
| Tree service | Starts April; slows from October (Ontario analysis, climate dependent) | Feb to Mar; storm cleanup events | Likely. webmarketers.ca (Canadian) |
| Fencing / decking | Spring to early summer | Jan to Mar | Unverified. Inferred from general spring leads claims (linknow.com) |
| Paving / concrete | Warm months, roughly Apr to Oct in the north | Feb to Mar | Unverified |

Today is 2026-11-13: the near-term windows are restoration (winter freeze prep), and a Jan to Mar push for everything else. Note a redesign takes time, so owners will want it done before spring: Nov to Feb is a plausible "get it done in the slow season" pitch (Assumed).

## 5. Ranked shortlist: build these first

1. Strong reviews plus weak site score (signal 6, built from 1, 2, 3, 4). Free, uses LocalPipe fields already in hand, gives a rank, and the copy is honest and specific. Build one composite "site gap" score.
2. No website on Maps (signal 5). Zero engineering; highest clarity of need; small volume per city but cheapest list.
3. Site quality fingerprint: HTTPS, copyright year, builder, PSI mobile score (signals 1 to 4). Cheap, free APIs, personalizable proof for email line one.
4. Storm/disaster events by county (signal 12) for roofing, restoration, tree, fencing. Real time-bound event; free NOAA/FEMA data; matches list by county. Best true trigger.
5. Running Google ads (signal 11). Shows existing spend and urgency; free to check manually; automate once the site-score loop works.

Held back: review velocity (needs repeat pulls and credits), hiring and new registrations (messy matching), domain expiry (redaction), new location (no clean detector).

## 6. Caveats: arguing against the shortlist

- Site-gap signals are STATE, not EVENT. Nothing says this is the week the owner decides to buy; the class method asks for time-bound triggers and only #4 is one. Most of the list may be "always true" filters that produce the same weak reply rates as plain volume.
- Owner-run trades often get work from referrals, Google Business Profile and Local Services Ads. A bad site may not hurt them, so the pain may be invisible to the owner. The 54% website-visit stat is across all local consumers, not home services (Confirmed scope).
- PSI scores are noisy and technical; telling an owner a number like 38 may be ignored or read as an insult. Builder detection can also flag sites that are fine.
- "No website" firms may not be reachable by email; LocalPipe email coverage for these may be low (Unverified), and these owners may be the least likely to spend $2,000.
- Storm data is county level, lags weeks, and a hail event helps roofers who are already swamped, so they may have no appetite for a website project during the surge. The right pitch timing may be after the surge, which breaks the "land just before" logic.
- Running ads is rare among the smallest operators, so volume is thin, and Transparency Center LSA coverage is not confirmed.
- Price anchoring: $2,000 plus $97/mo is cheap versus agency rates, which helps, but we have no verified benchmark of what these owners pay now (Unverified).
- Most seasonality evidence is blog-level; plan windows as hypotheses and test with small sends.

## Sources checked this session
- BrightLocal 2026 survey: https://www.brightlocal.com/research/local-consumer-review-survey/ (fetched)
- OpenFEMA API: https://www.fema.gov/about/openfema/api (fetched)
- Google PSI get-started: https://developers.google.com/speed/docs/insights/v5/get-started (fetched; no quota stated)
- NOAA Storm Events: https://www.ncei.noaa.gov/stormevents/ftp.jsp (search result only, not fetched)
- Seasonality: JobNimbus, All My Sons, webmarketers.ca (search results only, not fetched)
