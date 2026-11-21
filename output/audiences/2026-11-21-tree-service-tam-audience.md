# Week 2B: Tree service TAM in Clay Audiences + enrichment workflow

Built 2026-11-21 in the Treford Clay workspace (1102039) with the Clay CLI, following Sandra's
SEA method: **Segment** the universe, **Enrich** the slice, **Act** by routing and writing back.

## What was built

| Piece | Name | Id |
|---|---|---|
| Ingest workflow (draft) + routine | Rave \| Save tree services to Audiences (ingest) | `wf_0touw7kXPtz2zEmc5ZZ` |
| Custom fields (companies) | ICP Trade, Google Rating, Google Review Count, Rave Route | `audf_...` |
| **TAM segment** | Rave TAM \| US tree services, 1-50 staff | `audseg_0touwf8rocCp5cmhMkg` |
| Work-queue segment (workflow trigger) | Rave \| Tree services with no route yet | `audseg_0touwfaxky4M7gWBhpR` |
| Result segment | Rave \| Ready for review (strong Google reviews) | `audseg_0touwfcTnXUKXsBBVTG` |
| **Enrichment workflow (draft, unpublished)** | Rave \| Tree services: Google reviews, route, write back (2B) | `wf_0touwgjmmD4zniydQdt` |

Links: Audiences https://app.clay.com/workspaces/1102039/companies/all/records ·
workflow https://app.clay.com/workspaces/1102039/terracotta/tc-workflows/wf_0touwgjmmD4zniydQdt

## How records got into Audiences

In class the search panel's "Save to audience" built a Write to Audiences workflow. Here the
workspace's search-result quota was used up, so the same thing was done with Clay's documented
ingest pattern: a manual-trigger workflow with one **Create or update Audiences record** node
(matched on domain), registered as a routine and run in bulk over the 840 tree services (with a
domain) from the free Clay search. Tested on 1 record first. **0 data credits, 0 actions.**

## TAM

| Segment | Count |
|---|---|
| **TAM: US tree services, 1-50 staff** | **837** |
| No route yet (the queue) | 836 |
| Ready for review | 1 (after the 1-record test) |

The other ICP trades were sized with the same free search but not saved to Audiences (see
`context/docs/research/tam-clay-search.md`): ~60,900 companies across six trades.

## The enrichment workflow

```
Audience segment trigger: "no route yet"
  → Google reviews (0.2 credits)
  → Route by Google reviews (rules, first match wins)
       ├─ no rating found              → write back Rave Route = needs-research
       ├─ 4.5+ stars and 25+ reviews   → write back route = ready-for-review + rating + count
       └─ otherwise (default route)    → write back route = not-a-fit + rating + count
```

Each write-back matches the record by its Audiences id. The route label comes from the branch the
record took. Records leave the queue segment once a route is written, so the queue drains itself.

**Tested on 1 record** (a Washington tree service): rating 4.8 from 116 reviews → routed
ready-for-review; the record read back with Rave Route, Google Rating and Google Review Count
filled; the Ready segment went 0 → 1 and the queue 837 → 836. Cost: 0.2 credits, 1 action.

**Not published.** Publishing would run all 836 queued records: about 167 data credits (0.2 each).
That needs Neil's go.

## Lessons

- Write-to-Audiences fields must be mapped from a workflow value; a fixed text value is silently
  dropped. The route label is taken from the branch's node name.
- `inputMappingConfig` goes inside the tool entry, not on the node.
- Segment counts lag a few seconds behind write-backs.
- Paging a search to count it uses the workspace's search-result quota: 83,904 results did it.
  Count with Audiences `search-count` instead.
