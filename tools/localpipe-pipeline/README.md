# Localpipe lead pipeline

How Rave builds lead lists for local trades: Google Maps search → filter → enrich owner or
business email → drop consumer domains and franchises → build a PlusVibe send list.
Standard B2B databases miss these businesses, so every lead comes from Google Maps listings.

Read `knowledge-base/learnings/agent-notes.md` first. It lists the failure modes already hit
(flat-looking async jobs that are not stalled, `"not found"` as a literal string, owner email
costing 4x business email, and more).

## Layout

```
engine/lp.py              job runner: submit, poll, collect (reads LOCALPIPE_API_KEY and LOCALPIPE_ANON_KEY from .env)
engine/categories.py      Google Maps category handling
jobs/examples/*.json      example job specs (real jobs/ and runs/ are gitignored: lead data)
scripts/
  pipeline.sh             end-to-end run
  post_process.sh         clean a finished run
  filter_franchises.py    drop franchise locations
  drop_consumer_email.py  drop Gmail/Yahoo/iCloud addresses (decision 22)
  fetch_reviews.py        pull Google reviews by place_id (free endpoint)
  build_send_list.py      final PlusVibe CSV, strips "not found" to empty
  preview_csv.py          eyeball a CSV
  secret_gate.sh          run on staged changes before every push
reference/                Localpipe API docs and working notes, Google Maps category list
```

## Measured costs (from `context/docs/state.md`)

Maps scrape $1 per 1,000 businesses · business email $0.005/find · owner email $0.02/find ·
cost per sendable lead $0.014-$0.025.

## Not yet run in this public copy

The code is copied as-is from the private build, with one change: the Localpipe public anon key
is read from `.env` instead of being hardcoded. Known open bugs: open items 12 and 13 in
`weekly-priorities/open-items.md`.
