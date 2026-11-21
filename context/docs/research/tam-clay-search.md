# TAM from Clay's company search

Checked 2026-11-21 in the Treford Clay workspace with `clay searches query-mode`. Filters on every
row: US headquarters, company size 1, 2-10 or 11-50. Counts are unique companies. Free (0 credits).

| Trade | Clay filter (industry + description keywords) | Companies | Label |
|---|---|---|---|
| Tree service | Landscaping Services + "tree" | 886 | Confirmed (full count) |
| Foundation / waterproofing | Construction industries + "foundation repair", "waterproofing" | 3,538 | Confirmed |
| Fencing / decking | Construction + Landscaping + "fence", "fencing", "deck", "decking" | 13,034 | Confirmed |
| Roofing | Construction industries + "roofing", "roofer" | 18,956+ | Lower bound (stopped at 20,000 results) |
| Water damage / restoration | Construction + services + "water damage", "restoration" | 18,150+ | Lower bound |
| Paving / concrete | Construction + highway + landscaping + "paving", "asphalt", "concrete", "driveway" | 19,222+ | Lower bound |
| Moving | Not counted: search-result quota ran out | — | — |
| **ICP trades, unique** | | **60,871+** | |

Caveats:
- Keyword matches are loose ("restoration" and "concrete" catch adjacent businesses). Expect a fit
  check to cut these, as it did for tree service: of 22 strong-review tree-service rows checked by
  AI, 12 were landscapers with tree work as an add-on.
- Clay's company data comes from professional profiles. Owner-run trades are under-covered:
  Clay finds 886 US tree services, while one partial Google Maps pull (Localpipe) returned 1,252
  clean ones. Treat these as a floor, not the market.
- Paging through results to count them used the workspace's monthly search-result quota
  (83,904 results). Use a server-side count next time.
