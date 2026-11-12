# Decision log summary

Sanitized summary of the private Rave decision log (38 entries, 2026-08 to 2026-10). Full log is kept private.

Context: Rave sells a $2,000 website redesign (plus a $97/mo care plan) by cold email to US local trades. Stack: Google Workspace mailboxes provisioned through InboxKit, PlusVibe as the sequencer, Localpipe (Google Maps scrape plus enrichment) for leads, Calendly for booking. Owner: Neil Uko. Dates below are approximate to the month or day the entry was written.

## Decisions

| # | Date | Decision | Why | Still true? |
|---|---|---|---|---|
| 1 | 2026-08 | Size infrastructure for 200/day first (24 inboxes, not 42), later raised target to 345/day | Money model rests on workshop benchmarks, not Rave data; do not buy capacity for an unvalidated funnel | yes |
| 2 | 2026-08 | Pay about $11 per premium .com sending domain instead of about $3.50 cheap TLDs | Local contractors burn infrastructure 3-5x faster and cheap TLDs burn faster too; two multipliers would force a rebuy in week five; delta was about $40 | yes |
| 3 | 2026-08 | Warm-up (28 days, 0 cold) and ramp-up (3, 6, 10, then 15/day per inbox) are separate; full capacity at week 8; buy all domains at once | First model merged the phases and understated time-to-capacity by 4 weeks; staggered purchases push full speed to week 12 | yes |
| 4 | 2026-08 | Use a 28-day warm-up, not the SOP's 14-21 days | Vendor FAQ says 3-4 weeks; brand-new domains plus a fast-burning ICP; under-warming kills mailboxes, over-warming costs days | superseded by #30 (first send went out on day 19) |
| 5 | 2026-08 | Warm-up limit 25/day, cold limit 3/day | Warm-up goes only to the vendor's private pool so it carries no burn risk; throttling it leaves a "warmed" mailbox with no reputation | yes |
| 6 | 2026-08 | PlusVibe Personal ($37/mo) over SendKit ($97/mo) | Same job, unlimited warm-up included (removes a $72/mo warm-up add-on). Own error caught: claimed Personal capped at 3 inboxes from a page summary; the cap is only the free trial | yes |
| 7 | 2026-08 | Skip the PlusVibe free trial, go straight to paid | Trial connects 3 of 24 mailboxes; idle infra cost about $41 vs $37 saved, plus a 2-week delay | yes |
| 8 | 2026-08 | Drop Clay, use Localpipe only | Local and physical businesses come from a Maps scrape; Clay is for enrichment waterfalls; saves $446/mo | yes |
| 9 | 2026-08 | Start with business email (1 credit), not owner email (2 credits) | Owner emails are mostly personal addresses, which burn new domains faster; add owner email later for top accounts | superseded by #38 |
| 10 | 2026-08 | Drop HVAC, plumbing and manufacturers from the opening push | Strategy brief's own scoring: HVAC and plumbing are the most-emailed trades and are being rolled up; manufacturers are not a Maps ICP | yes |
| 11 | 2026-08 | Primary campaign targets businesses with a weak existing site, not no-website businesses | The copy critiques an existing site; you cannot show a redesign of a site that does not exist | yes (premise still untested, see #27) |
| 12 | 2026-08 | Open with restoration, foundation and tree service; defer movers, fencing, paving to spring | October start; those verticals peak in summer or spring | superseded by #26, #27 (roofing and tree service chosen on data) |
| 13 | 2026-08 | Price $2,000 one-time plus $97/mo care plan, single price, no tiers | Job values are $2k-$30k so $1,500 gains no conversions; cheap reads as a scam; tiers turn a short call into a comparison; care plan funds the stack | yes (revisit after about 10 closes) |
| 14 | 2026-08 | Remove borrowed agency client case studies from copy | Attribution risk; an unverifiable claim looks like a scam email; replace with a working design at a live link and build real proof | unknown (#30 says the borrowed claims were still in the live sequence) |
| 15 | 2026-08 | Move DNS to Cloudflare, keep registration at Dynadot | Dynadot is not auto-integrated with InboxKit; 24+ manual records invite silent typos. Each domain needs its own Cloudflare zone | yes |
| 16 | 2026-08 | Brand domain at a different registrar than sending domains; auto-renew off for sending, on for brand | A flagged cold-email account must not contain the brand domain; sending domains are disposable | yes |
| 17 | 2026-08 | Calendly on a Workspace address, booking windows 7-8am and 5-7pm, notifications to the phone calendar app | Consistent sender identity through booking; contractors are on site midday; mailbox is full of warm-up traffic | yes |
| 18 | 2026-08 | Use exact Google Maps category strings in Localpipe queries | Query matches Maps taxonomy exactly: "fencing" returns the sport, "foundation" returns charities | yes |
| 19 | 2026-08 | Review text is not in the Localpipe API (open issue) | Search and enrich return rating and count only; the best angle needs review text | superseded by #21, #23 |
| 20 | 2026-08 | Use the enrichment email_provider field to spot consumer-Gmail recipients before sending | Lets you segment them instead of discovering burn after the fact | yes (caveat: only populated after a paid find, see #31) |
| 21 | 2026-08 | Verified by control test that the review scrape is dashboard-only | Endpoint returned 401 with and without a key while a control endpoint changed response with a key | superseded by #23 |
| 22 | 2026-08 | Drop @gmail recipients entirely in campaign one; no Gmail lane yet | Vendor-founder and practitioner guidance: 30-50% of local lists, 3-5x burn, isolation costs 2-3x infra. Throttle numbers are a heuristic, not measured | yes |
| 23 | 2026-08 | Review scrape shipped to the API and live-tested; review-callback angle goes in v1 | Returns reviewer name and review text, 10 places per call, not billed as enrichment | yes |
| 24 | 2026-08 | Filter franchises and chains before enrichment using shared root domain, franchisor URL paths and a brand list, in three tiers | A franchisee cannot buy a site corporate owns; 40% of one restoration pull; city in the path is suspicious, city in the domain is a local signal | yes |
| 25 | 2026-08 | Drop the no-review and few-review segment; two review-based openers only | Review count is the ability-to-pay proxy; many 1-review businesses were not real prospects | yes |
| 26 | 2026-08 | Supply is not the constraint; restoration was the wrong lane to lead with | Sized one vertical against a portfolio target; roofing alone had 3x the clean pool of restoration; also wrongly declared a running job dead after 63 minutes at 0 progress, then it finished in about 4 minutes | yes |
| 27 | 2026-08 | First two verticals: roofing, then tree service | Largest and cleanest pools (12% franchised vs 45% for water damage). Ticket size is inference; under 1% use DIY site builders so "no real website" is not an opener | yes (premise checks still open) |
| 28 | 2026-08 | Full 10-category, 25-metro sweep gave 7,535 clean independents but zero emails | Enrichment had been left off to avoid unapproved spend; list was ahead of nothing, enrichment became the blocker | yes |
| 29 | 2026-08 | Default enrichment to business email only after seeing real per-find prices | Billing showed $0.005 business vs $0.02 owner per find; owner email had been over-used | superseded by #38 |
| 30 | 2026-08 | Launch water damage campaign: 2,007 leads, 2/day per inbox on 24 inboxes (about 48/day), warm-up left on | Conservative opening on day 19; warm-up never fully stops | yes |
| 31 | 2026-09 | Pre-filter by free DNS MX lookup before paying to enrich; scrape with a lower review floor; owner-name lookup cannot be switched off | Provider field is only visible after paying; owner name fires even with owner email off | superseded in part by #34 (MX under-counts) |
| 32 | 2026-09 | Retract "water damage niche is exhausted" | Earlier runs were one keyword at state level with a 20-review floor; a re-run returned 100% net-new places | yes |
| 33 | 2026-09 | Run a 26-keyword, 3-country sweep with category auto-resolution off; always preview with the free plan step | Auto-resolution mapped 22 of 26 keywords to wrong categories (a board game club, accountants). "Unlimited exports" is not free: $1 per 1,000. Planning number: about $0.021 per usable email. CA and UK flagged as separate legal regimes | yes |
| 34 | 2026-09 | Depth beats breadth: only an unlimited per-pair limit walks past the top of the Maps ranking | Numeric-limit runs returned 29% and 4% net-new; deep Texas run 54%. MX pre-filter classified only 11% as Google or Microsoft; trust the provider field | yes |
| 35 | 2026-09 | Water damage is done at 2,872 sendable; move to roofing next, tree service second; blocker is copy, not leads | Leftover pool measured 92% franchise, not the assumed 20%; a 10x overstatement avoided by measuring first | yes |
| 36 | 2026-09 | Launch roofing with about 800 leads at 7/day per inbox, no first names | Cost per sendable lead $0.0145; UI job asked for business email only so every lead is "there", which confounds the vertical test | yes |
| 37 | 2026-09 | Split state from history (short STATE file, open-items table); reject the rest of an external template repo | Open items were raised three times with no closure; the log did two jobs. Rejected content-marketing structure, CI ingestion, and a writing skill that conflicts with preserve-the-copy rules. Audited GREEN first | yes |
| 38 | 2026-10 | Pivot to owner emails only | Business email is a role inbox 40% of the time and free-provider 46%; owner email is 99% named, 94% work domain. Costs about 17% more per named contact. Evidence is one positive reply, so "named converts better" is still a hypothesis | yes |

## Top 10 lessons

1. **Do not buy capacity for a guess.** Size infrastructure and spend to what the unvalidated funnel can justify, but buy it all at once because ramp time is the real constraint (#1, #3, #7).
2. **Warm-up is separate from ramp, and the two levers point opposite ways.** Warm-up volume high, cold volume low; plan time-to-capacity from both phases (#3, #4, #5, #30).
3. **Stack burn multipliers deliberately.** Personal-inbox recipients, cheap TLDs and brand-new domains each burn infrastructure faster; pay a small premium or exclude the segment until the offer is proven (#2, #9, #20, #22).
4. **Verify against the primary source.** Page summaries, vendor docs and your own earlier claims were wrong repeatedly (plan limits, review API, a "dead" job, "exhausted" niche). Test with a control (#6, #21, #23, #26, #32).
5. **A search is not a market.** Before calling a niche tapped, state keywords, location granularity, filters and limit mode, and check whether a re-run returns duplicates (#32, #33, #34).
6. **Always preview before you pay.** The free plan step caught category auto-resolution mapping to unrelated businesses; the franchise filter on a leftover pool turned a $34 plan into a $3.40 one (#33, #35, #38).
7. **Filter before enrichment, not before sending.** Franchises, duplicates and consumer domains are cheaper to drop first, and each pool's clean rate must be measured, never carried over from another pool (#24, #35, #38).
8. **Optimize unit cost against a value denominator.** Cost per find looked best at $0.005; cost per named person reached told a different story, and the one positive reply came from the "expensive" field. Treat it as a hypothesis until more replies arrive (#29, #33, #38).
9. **Size each lane against its own target, and match the offer to the buyer.** Pick verticals on measured pool size, franchise rate and ticket size; price above the scam-signal zone; use demonstration instead of unattributable case studies (#10, #12, #13, #14, #26, #27).
10. **Give open items and current state a home.** Keep a short state file and an append-only log; a flagged problem raised three times with zero closures means it had nowhere to live. Also log confounds (such as missing first names) so you do not blame the vertical (#36, #37).
