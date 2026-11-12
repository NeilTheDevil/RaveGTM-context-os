# Rave — GTM System Architecture

Rave's outbound system end to end, from signal to booked call and back into this Context OS.
Designed tool-agnostic first; the tool column is today's choice and can be swapped.
Status per step: **Live** (running since Aug-Sep 2026), **Built** (exists, not yet run here),
**Planned**. Last updated 2026-11-13.

```
Context OS ─► Signals ─► Find companies ─► Enrich ─► ICP fit check ─► Route by segment
    ▲                                                                       │
    │                                                                       ▼
Weekly feedback ◄─ CRM ◄─ Reply handling ◄─ Sequence ◄─ Verify email ◄─ Find person/email
```

## Steps

### 1. Context OS
- **What:** ICP, signals, facts, copy rules and lessons in this repo. Every session starts from `CLAUDE.md`.
- **Tool:** Claude Code + GitHub. **Status:** Live.
- **Decision:** Is a claim in `context/messaging/facts.md`? Yes → may appear in copy. No → renders as `{{placeholder}}` until Neil approves it.

### 2. Buying signals
- **What:** Pick which signal drives this week's list (`context/icp/signal-matrix.md`, top 5).
- **Tool:** Signal matrix; NOAA/NWS/FEMA for weather; calendar for season. **Status:** Planned (workflow 1 specced).
- **Decisions:**
  - Storm, freeze or flood event in a county in the last 30-60 days? Yes → weather workflow for that county's roofing, tree, fencing, foundation or restoration. No → the always-on workflow (strong reviews + weak site).
  - Within 4-8 weeks of a trade's busy season? Yes → add the season angle. No → plain site-gap angle.

### 3. Find companies
- **What:** Pull every business in a trade and region from Google Maps. B2B databases miss these businesses.
- **Tool:** Localpipe `/maps-search` ($1 per 1,000), `tools/localpipe-pipeline/`. **Status:** Live.
- **Decisions:**
  - Already pulled before (place_id seen)? Yes → skip. No → keep.
  - Job still shows "processing 0/N" after an hour? Keep polling; that is the queue, not a failure (agent note 1).

### 4. Enrich (company)
- **What:** Reviews for personalization; site checks for routing.
- **Tool:** Localpipe `/scrape-reviews-api` (free); homepage fetch script (HTTPS, footer year, builder); PageSpeed Insights API (free). **Status:** Reviews Live; site checks Planned.
- **Decision:** Site loads? No → exclude (cannot state a fact about it). Yes → record the three checks.

### 5. ICP fit check
- **What:** Drop anything outside the ICP before spending on emails.
- **Tool:** `filter_franchises.py` + rules in the workflow spec. **Status:** Live (franchise filter), Planned (rating gate).
- **Decisions:**
  - Franchise brand? Yes → drop (corporate controls the site).
  - Rating ≥ 4.5 and reviews ≥ 25? No → drop from workflow 1 (may go to broad campaigns). Yes → continue.
  - Non-US? Yes → drop (CASL/PECR).

### 6. Route by segment
- **What:** Each lead goes to the first site check it fails; each route is its own campaign with its own angle.
- **Tool:** Script on the enriched CSV. **Status:** Planned.
- **Decisions:** No HTTPS → "Not secure" campaign. Else footer year ≤ 2022 → "Old footer" campaign. Else PageSpeed mobile < 50 → "Slow on phones" campaign. Else (site passes all three) → not in workflow 1; held for broad campaigns.

### 7. Find the person
- **What:** The owner's name, so the email is to a person.
- **Tool:** Localpipe `/enrich` (owner name, $0.005/find). **Status:** Live.
- **Decision:** Owner name found? Yes → `{{first_name}}`. No → fallback "there" (and blank Localpipe's literal `"not found"` first, or it sends "Hey not found,").

### 8. Find and verify the email
- **What:** One email per business, on a work domain.
- **Tool:** Localpipe `/enrich` (owner email $0.02, business email $0.005; usage-based accounts get pre-verified business emails). **Status:** Live.
- **Decisions:**
  - Owner email found? Yes → use it (decision 38, owner emails only). No → business email or drop, per open item on decision 38.
  - Gmail/Yahoo/iCloud address? Yes → drop from campaign one (protects new domains, decision 22).
  - Outlook-hosted? Neil filters in PlusVibe, never at list-build.

### 9. Sequence (email; LinkedIn not used)
- **What:** 3 emails over 7 days per route (`output/campaigns/strong-reviews-weak-website/`).
- **Tool:** PlusVibe, 24 mailboxes on 8 domains, warm-up running. **Status:** Live for water damage and roofing; workflow 1 Planned.
- **Decisions:**
  - Bounce rate under 3%? Yes → ramp send rate per the plan (3 → 6 → 10 → 15/day per inbox). No → hold and check lists.
  - LinkedIn? No: owners of these trades are rarely active there (ICP digest). Phone (from the Maps listing) is the second channel, planned.

### 10. Reply handling
- **What:** Answer fast, book a 10-20 minute call, customize the sample with their name, city and a real review before the call.
- **Tool:** PlusVibe inbox, reply template (`legacy-copy/05-reply-template.md`), Calendly. **Status:** Live, with a gap: reply alerts to Slack are unbuilt (open item 2; one positive reply waited a day).
- **Decisions:** Positive → send booking link same day, build the custom sample. Objection → answer from the objection map in `personas.md`. Unsubscribe/negative → remove at once (CAN-SPAM).

### 11. CRM
- **What:** One record per business: source signal, route, replies, call, outcome, deal value.
- **Tool:** HubSpot (course week 3). Today: PlusVibe lead status only. **Status:** Planned.
- **Decisions:** Call booked → deal stage "Call booked". Showed and liked the sample → "Proposal". Paid → "Won", add to case-study candidates. No show → one reminder, then "Lost: no show".

### 12. Weekly feedback loop into the Context OS
- **What:** Every Friday, read reply and booking rates per route and per signal; write what changed.
- **Tool:** PlusVibe analytics → `knowledge-base/learnings/`, `context/icp/signal-matrix.md`, `weekly-priorities/`, `work-log/`. **Status:** Planned (the decision log did this informally, 38 entries).
- **Decisions:**
  - A route replies no better than broad copy after ~1,000 sends? Yes → drop it to a filter, lead with weather (steelman in the signal matrix). No → keep and scale.
  - First 1,000 leads reported back? Rebuild the money model with real rates (state.md).
  - New objection seen twice? Add it to `personas.md` and the facts file.

## Four pillars check

| Pillar | How this system meets it | Gap |
|---|---|---|
| Clean data | Franchise filter, consumer-domain drop, `"not found"` stripped, dedupe on place_id | Thresholds not yet measured on a real list |
| Always-on signals | Site-gap signal runs on every new scrape; weather checked weekly by county | Site-gap is a state, not an event |
| Composable workflows | Same pipeline for every trade; only the query string and trade word change; tools swappable per step | Routing script not built |
| Tight feedback loops | Weekly review step writes back into this repo | No CRM yet; reply alerts unbuilt |
