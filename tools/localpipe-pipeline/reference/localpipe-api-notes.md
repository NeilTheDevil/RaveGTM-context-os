# Localpipe API — Working Notes

Reviewed against `localpipe-api-docs.md` (v2, 1,071 lines) and
`localpipe-business-categories.csv` (4,284 categories). Updated 2026-08-14.
These are the parts that matter for Rave. Full docs are alongside this file.

Auth: `x-api-key` header. Key lives in `.env` as `LOCALPIPE_API_KEY` — **gitignored**.

---

## Three endpoints

```
POST /maps-search         Google Maps business search  → task_id, async
POST /enrich              owner name / email / phone   → job_id, async
POST /scrape-reviews-api  Google reviews by place_id   → synchronous, FREE
```

The first two are async and need polling or a webhook. Reviews are synchronous —
results come back in the response body.

---

## /maps-search

**Batching is the whole game.** 5 keywords × 25 locations in ONE request = 125
query-location pairs. Do not loop one city at a time.

```javascript
{
  query:    ["water damage restoration service", "fire damage restoration service"],
  location: ["Austin, TX", "Dallas, TX", "Houston, TX"],
  limit:    "all",          // removes the 100-lead cap
  filters:  { has_website: true, min_rating: 3.5, min_reviews: 10 }
}
```

⚠️ `limit` is **per pair**, not total. 5 queries × 10 locations at `limit: 400` is up
to 20,000 leads, not 400.

### Filters — do the qualifying here, before spending credits

| Filter | Use for Rave |
|---|---|
| `has_website` | **The campaign split.** `true` = revamp campaign (primary). `false` = no-website campaign. Docs literally say "useful for web-design prospecting" |
| `min_rating` | Quality floor. 3.5+ |
| `min_reviews` | **A-tier proxy.** High review count = has money and cares about reputation |
| `max_reviews` | Optional ceiling to skip the biggest players |
| `has_phone` | `true` only. **Never pass `false`** — it excludes every listing with a phone and collapses yield |
| `radius_km` | 5-80, ZIP/postcode locations only. Ignored for city/state names |

### Returned fields

```
name · phone · full_address · city · rating · review_count · website
types · matched_category · price_level · place_id · business_id
latitude · longitude · is_claimed · working_hours
```

No review text here — but `place_id` feeds `/scrape-reviews-api`, which returns
reviewer names and full review bodies for free. See that section below.

---

## /enrich

```javascript
{
  business_name:     "Acme Restoration",
  business_website:  "acme.com",
  business_location: "Chicago, IL",
  want_email:         true,    // owner email — 2 credits
  want_general_email: true,    // business email — 1 credit
  want_phone:         false    // 5 credits — skip
}
```

### Returned fields — use these names verbatim

```
business_name · business_website · business_location
owner_name · owner_first_name · owner_last_name
owner_email · owner_phone · business_email
email_provider · decision_maker_title · owner_role · extra_columns
```

**Negative results return the literal string `"not found"`** — never null, never
empty, never missing. Parse accordingly.

**Field name traps** (from the docs, these do NOT exist):
```
❌ general_email  → ✅ business_email
❌ personal_email → ✅ owner_email
❌ first_name     → ✅ owner_first_name
❌ phone          → ✅ owner_phone
❌ name           → ✅ owner_name
```

### `email_provider` — the useful one

Classifies the returned email as `Google Workspace`, `Microsoft 365`, etc. Lets you
identify consumer-Gmail recipients **before sending** and segment them onto separate
domains, instead of finding out by burning mailboxes. Directly addresses the 3-5x
personal-inbox burn risk.

> **CORRECTION 2026-09-05 — it is NOT owner-email-only.** This file previously said
> `email_provider` classifies `owner_email`, and decision 31 was built on the belief that
> the field is unavailable when you skip owner email. **Wrong.** The
> `wd-final-401-enrich` run used `want_email: false` / `want_general_email: true` — no
> owner email requested, none returned — and `email_provider` came back **populated on
> the business emails**:
>
> ```
> 180 business emails found from 396 enriched
>   Google Workspace 87 · Microsoft 365 51 · (null) 34
>   Yahoo Mail 3 · Rackspace/Hostinger/Proofpoint/Amazon SES/iCloud 1 each
> ```
>
> Practical consequence: **you do not need the free DNS MX pre-filter to know the ESP.**
> Localpipe hands it to you with the address. The MX pre-filter still has one distinct
> use — it is the only way to know the provider *before* paying, so it stays useful if
> the goal is to spend exclusively on Google domains. If the goal is just to segment
> Google vs Microsoft after the fact, `email_provider` alone is enough and the MX pass
> is redundant work.
>
> Note ~19% of found emails come back with `email_provider: null`, so the field is not
> a complete classifier — treat null as unknown, not as non-Google.

---

## Credits

```
owner email (want_email)            2 credits
business email (want_general_email) 1 credit
owner phone (want_phone)            5 credits
Google Maps scrape                  $1 per 1,000 businesses
```

Scraping is nearly free. Credits only go on contact data — so **pull wide, filter
hard, enrich last.**

**Rave is on usage-based billing** with a $100 starting credit, not the credit plans.
Per-find rate is not documented — confirm with the founder. Usage-based accounts also
receive **pre-verified business emails**, where credit-based plans return them
unverified.

---

## Category strings — verified against their taxonomy

`query` matches Google's category taxonomy exactly. Plausible words return the wrong
industry.

**Traps found:**
```
❌ "fencing"    → fencing salon, fencing school      (the sword sport)
❌ "foundation" → research foundation, national health foundation
```

**Correct strings for Rave's verticals:**
```
water damage restoration service     roofing contractor
fire damage restoration service      tree service
building restoration service         fence contractor
waterproofing company                deck builder
damp proofing service                paving contractor
moving company                       concrete contractor
mover                                excavating contractor
moving and storage service           gutter cleaning service
```

---

## /scrape-reviews-api — RESOLVED, live and verified 2026-08-14

Shipped by the founder same-day. **Live-tested against a real place_id and working.**

```javascript
POST /scrape-reviews-api
{
  place_ids:  ["ChIJ...", "ChIJ..."],   // up to 10 per call
  max_reviews: 20,                       // 1-40, newest first, default 20
  rating_min:  4,                        // optional, default 1
  rating_max:  5                         // optional, default 5
}
```

**Synchronous.** No task_id, no polling — results are in the response body.
Measured ~2.7s for one business.

### Response

```json
{
  "status": "completed",
  "requested": 2,
  "total_reviews": 34,
  "duration_ms": 3120,
  "results": [{
    "place_id": "ChIJ...",
    "review_count": 20,
    "reviews": [{
      "user_name":   "Jane D.",
      "rating":      5,
      "review_text": "Great service, fast turnaround.",
      "review_time": "2 months ago"
    }]
  }]
}
```

### Why this matters

**`user_name` + `review_text` are exactly what the highest-converting angle needs.**
Real verified output from the test call:

> **Barbara Beyer** (5★, a month ago): *"I want to sincerely thank Jorge, Oscar, and
> Uriel for the excellent work they did rebuilding our two bedrooms after they were
> damaged by flooding. Jorge was always friendly, quick to answer my calls..."*

Named employees, specific jobs, real detail — the raw material for proving you
actually looked at their business.

### Cost: free

> "Reviews are **not billed as enrichment**; the call counts against your normal API
> request limits."

Reviews can be pulled across the entire list without touching the usage-based
balance. At 10 businesses per call and ~2.7s each, 3,000 leads is roughly 15 minutes.

### Gotchas

- Rating filtering is applied **after** fetching, so a narrow range can return fewer
  than `max_reviews`
- A business with no reviews returns `review_count: 0` and an empty array — the call
  still succeeds, so handle empty rather than assuming a review exists
- `400` if more than 10 place_ids, `429` on daily/monthly limit
- Pipeline: `/maps-search` → `place_id` → batch 10 into `/scrape-reviews-api` → join

### Note on the endpoint name

This is **`/scrape-reviews-api`**, not `/scrape-reviews`. The latter exists but
rejects API keys — it is the dashboard's internal endpoint. Use the `-api` suffix.

---

## Running it — read this before writing any script

The docs have an explicit section for AI coding agents. The rule:

> **Write a detached script that logs to a file. Do not drive the poll loop from the
> agent's tool calls.**

A scrape takes longer than any agent's shell timeout. The working pattern:

1. Script submits the scrape, then polls forever, writing status to a log file
2. Run it detached (`nohup … &`)
3. Agent checks the log with short `tail` calls every 30-60s
4. Exit only on a terminal status

Also:
- Rate limits return **429** — back off and retry, don't hammer
- Polling endpoints are excluded from the rate limit
- Use **unlimited polling** (the docs flag this as required)
- `/cancel-scrape-job` and `/cancel-enrich-job` accept up to 500 IDs per call, and
  already-scraped leads are preserved on cancel

---

## Build order (from the lead-list SOP)

```
Accounts → Qualify → Enrich and Score → Contacts → Emails (last)
```

1. Scrape wide with `has_website: true`, dedupe by name + address
2. Hand-check 5-10 rows before any full run
3. AI-qualify: read each site, is it genuinely weak? Drop the fails
4. Score and tier on review count + rating
5. Enrich **qualified accounts only** — business email first
6. Verify with MillionVerifier **2-3 days before launch**, not weeks ahead
7. Drop catch-all-only addresses

---

## Doc version & provenance

`reference/localpipe-api-docs.md` is the **vendored copy of Localpipe's official API docs** —
committed so any session can read the source instead of working from memory. Neil asked for
this explicitly on 2026-08-30.

**Read the vendored docs before answering anything about the API.** Do not recall endpoint
names, parameter names, limits or response fields.

| | |
|---|---|
| Current version | downloaded **2026-08-24**, installed 2026-08-30 |
| Previous | 2026-08-13 |
| Scrub | the Supabase anon key is replaced with `<SUPABASE_ANON_KEY — see original docs>` (10 occurrences). Never commit the raw key. |

### What changed 08-13 -> 08-24

**Rate limit doubled: 500 -> 1000 requests / rolling minute** on `/enrich` and
`/maps-search`. The docs now also spell out that a 429 is always retryable and that the
client, not the server, must throttle.

`engine/lp.py` line 57 still sets `RATE_LIMIT_PER_MIN = 460`, sized against the old 500 cap.
That is **safe but conservative** — submissions could run roughly twice as fast. Not changed:
it works, and the 450-lead batch submitted in about a minute regardless.

### Cost data is NOT in these docs

Verified 2026-08-30 against the API responses and the full doc: there is **no cost, price or
balance field** anywhere — not in `/enrich`, not in `/get-job-results` or its `stats` block,
and there is no balance endpoint. The only dollar reference is the 402 error, "Usage billing
balance is $0". Dollar figures come from the Localpipe dashboard only.

---

## Confirmed per-find pricing — usage-based billing (Rave's account)

Read directly from the Localpipe billing dashboard, 2026-08-30. This is the first
confirmed dollar figure since the account was opened — every prior cost estimate in this
repo (`~$8-15` scrape quotes, `0.62 credits/lead`) was a credit count or a rough guess,
never a verified dollar rate. Supersedes those.

| Field | Rate | Notes |
|---|---|---|
| Owner Names | $0.005 / find | Returned whenever a decision-maker name is found — see the open question below on whether this is avoidable |
| Owner Emails | **$0.02 / find** | 4x the business-email rate. Requested via `want_email: true` |
| Business Emails | $0.005 / find | Requested via `want_general_email: true`. **Pre-verified on usage-based accounts** — same verification guarantee as owner email, 4x cheaper |
| Phone Number | $0.05 / find | Never requested in this project (`want_phone: false` throughout) |
| LinkedIn Profiles | $0.005 / find | Not a field this project has requested |
| Location Counts | $0.002 / find | Not a field this project has requested |
| Business Exports | $1.00 / 1,000 | This is the `/maps-search` **scrape** cost, not enrichment — separate from every rate above |

**One dashboard snapshot, for scale (2026-08-30, "Last 7 Days" window):**

```
Owner Names        4,888 found   $24.44
Owner Emails        1,273 found   $25.46
Business Emails     1,706 found    $8.53
Business Exports   12,596 found   $12.60
                                  -------
                                   $71.03
```

### Open question — is Owner Name lookup avoidable?

`reference/localpipe-api-docs.md` describes `owner_name`/`owner_first_name` as returned
"when `want_name=true` (default)" — but `want_name` does not appear anywhere in the
documented request-parameter table. It may fire on every `/enrich` call regardless of
`want_email`, or it may be silently coupled to `want_email`. **Untested.** Confirm with
the founder or by direct experiment (submit one enrich with `want_email: false,
want_general_email: true` and check whether `owner_name` still comes back populated)
before assuming either way.

---

## CORRECTION 2026-09-20 — `limit` semantics were rewritten, and two new features landed

Neil flagged that the founder updated the docs. `reference/localpipe-api-docs.md` is now the
2026-09-20 version (1,383 lines, was 1,071). Two changes matter.

### 1. `limit` is a TOTAL TASK BUDGET, not a per-pair cap — this retro-explains everything

```
OLD: "Maximum results per (query x location) pair ... 5 queries x 10 locations
      with limit:400 -> up to 20,000 leads, not 400."
NEW: "Total budget for the task. Default 100, minimum 50, max 10,000. Values below
      50 are raised to 50. With multiple keywords and/or locations the budget is
      split evenly across every (query x location) pair, and any share a dry pair
      cannot use is redistributed to pairs that still have more matches."
```

Every previously-inexplicable observation fits the new definition exactly:

| run | limit set | result | explained by |
|---|---|---|---|
| `wd-5dollar-scrape` | 2 | tasks of 47, 27, 24 | raised to 50, capped there |
| `wd-5dollar-tranche2` | 3 | two tasks of exactly 50 | raised to 50 |
| `wd-more-supply-capped` | 50 | two tasks, 100 total | 50 budget per task |
| `wd-limit-canary` | 1000 | 284 | budget never exhausted; only 284 existed |

Decision 34 concluded "numeric `limit` is a shallow-sample knob, not a volume knob."
**The conclusion was right; the stated mechanism was wrong**, and I attributed the mismatch
to the API misbehaving rather than to the docs being stale. It was a documented-behaviour
change, not a bug.

**Consequence — `engine/lp.py` cost estimates are now wrong.** `build_plan` computes
`MAX LEADS = limit x pairs` (the old semantics). On `jobs/wd-global-sweep.json` it reported
"MAX LEADS 48,750 / $48.75 ceiling"; under the real semantics that job would have returned
**25 leads total**. Any job config using a numeric `limit` across many pairs is mis-estimated
and will badly under-return. `limit:"all"` is unaffected — it means no budget at all.
Needs a worktree fix.

### 2. `exclude_existing_lists` — server-side dedupe against what you already hold

`POST /maps-search` accepts `exclude_existing_lists: string[]` — Business List IDs to compare
against. Any business already in those lists is removed from the task's results, **matched on
`place_id` OR website domain**. Max 50 lists per request; IDs not on your account return 400.

New companion endpoint `GET /list-business-lists` returns the IDs (free read; no findable
data, so no charge). As of 2026-09-20 the account holds **28 lists, all restoration-related**
— their IDs are cached at `runs/_input/exclude-list-ids.json`.

Two practical notes:

- The exclusion is applied **to the results**, after the budget is spent, so a `limit` of 500
  can return far fewer than 500 rows. Ask for more than you need.
- Domain-matching makes it broader than our local `place_id` dedupe: it also drops a business
  sharing a website domain with something already held. Useful for chains, but it means the
  exclusion is not identical to what `runs/_input/` dedupe would produce.

Also new and not yet evaluated: `POST /location-enrich-api`.
