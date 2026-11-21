# Clay build: Strong reviews, weak website (tree service)

Course week 2 deliverable. Built 2026-11-21 in the Treford Clay workspace ("Neil's Workspace",
1102039) with ClayBP (Rex + Clay CLI), from [`../workflow-spec.md`](../workflow-spec.md).
Step-by-step guide and flow diagram: `strong-reviews-weak-website-clay-build-guide.md` in this folder.

## Links

| What | Link |
|---|---|
| Workbook (Companies + Exclusions) | https://app.clay.com/workspaces/1102039/workbooks/wb_0toutzxvYv4tVpSdo2S |
| Companies table | https://app.clay.com/workspaces/1102039/workbooks/wb_0toutzxvYv4tVpSdo2S/tables/t_0toutzyVjZznkdoRdwU |

Faculty view access: Share button on the workbook (Neil to set).

## Tables

| Table | Rows | Role |
|---|---|---|
| Companies | 100 | Main table, one row per company (account-first: the trigger is a company state, not a person event) |
| Exclusions | 5 | Franchises and Rave itself, matched on domain |

Auto-run is off on both, read back after creation.

## Column groups, in build order

1. Company (from the free Clay search)
2. Free checks: Exclusions lookup on domain, Size OK?, Franchise Name?, **Pass Free?**
3. Company check: Google reviews (rating, count), **Strong Reviews?** (4.5+ from 25+)
4. Website signal: homepage scrape (proves HTTPS), http fallback, footer year, click-to-call links, quote mention
5. AI columns: **AI Fit Check** (is it an independent tree service, with evidence) and **AI Site Gaps** (reviews shown, click-to-call, quote request, with evidence). Both JSON with fixed answer lists. Fit check proven on 3 rows before the rest.
6. Routing: **Cell**, **Ready to Contact?**
7. Email waterfall: homepage email (free) → Hunter → ZeroBounce (only-safe) → Email Matches Company? → **Send Ready?**

Every paid column has a run condition on the gate before it. Every column has a plain-English description in Clay.

## Funnel (100 rows from the free Clay search)

The search (tree service, US HQ, 1-50 staff) returned 886 companies. 100 imported in two batches of 50; batch 2 took only names containing "tree" or "arbor", a free filter after batch 1 showed half the list were landscapers.

| Step | Rows |
|---|---|
| Imported | 100 |
| Pass free checks | 99 |
| Found on Google | 94 |
| Strong Google reviews (4.5+ from 25+) | 60 |
| Site live (https scrape worked; none were http-only) | 56 |
| AI: independent tree service | 38 of 55 checked (15 not tree service, 1 franchise, 1 unclear) |
| **Ready to Contact** (a sendable site gap) | **28**: C4 reviews not shown 25, C2 old footer 2, C6 no quote request 1 |
| Held (no gap found) | 10 |
| Email found | 20 (14 homepage, 6 Hunter); 8 recorded "Not found" |
| Email on the company's domain | 20 of 20 |
| ZeroBounce | 9 valid, 9 do-not-mail (mostly role inboxes), 2 invalid |
| **Send Ready** | **9** |

Out: reviews not strong 40, not an independent tree service 17, site down 5.

## Cost (data credits, measured from the balance before and after each step)

| Step | Per row | Rows run | Credits |
|---|---|---|---|
| Google reviews | 0.2 | 99 | 19.8 |
| Homepage scrape | 0.1 | ~60 | ~5.5 |
| http fallback scrape | 0.1 | 4 | ~0 |
| AI Fit Check (Gemini 3 Flash) | 0.5 | 55 | ~27 |
| AI Site Gaps (Gemini 3 Flash) | 0.5 | 38 | ~19 |
| Hunter (billed per lookup: 13 x 0.4; found 6) | 0.4 | 13 | 5.2 |
| ZeroBounce | 0.1 | 20 | 2.0 |
| **Total** | | | **79.4** |

About 0.8 credits per imported row, 2.8 per Ready row, 8.8 per Send Ready row. Searches, lookups and formulas were free.

## Findings

- **The spec's free website checks found almost nothing.** Every live site serves HTTPS, and most footers auto-update (2025-2026). Neil switched the website signal to an AI site-gap column (2026-11-21). Supports open item 6.
- **The real gap is reviews.** 25 of 28 ready rows have strong Google reviews and show none of them on the homepage. That is Rave's "real review" angle.
- **Clay's "tree service" list is half landscapers.** The AI Fit Check separated them. A name filter (tree/arbor) cut the waste in batch 2.
- **Clay finds 886 US tree services; Localpipe (Google Maps) already found 1,252 clean ones** from a partial scrape. Google Maps is the better source for this ICP.
- **Emails:** half the ready rows print an email on their own homepage (free). ZeroBounce marks role inboxes (info@) do-not-mail, so owner names matter (decision 38).
- PageSpeed (mobile speed) needs a free Google API key; route C3 is held until then.

## Still to do (Neil)

- Views in the Clay app: **Ready to send** (Send Ready? is checked), **Held** (Cell starts with "Held"), **Dropped** (Cell starts with "Out"). The API ignored view filters.
- Share link (view access) and a Loom walkthrough in the Build Log.
- Copy for cells C4-C6 (the spec's copy covers C1-C3).
