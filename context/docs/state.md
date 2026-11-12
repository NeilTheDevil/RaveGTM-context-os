# Rave — current state

**What is true today.** Read this first; it is the snapshot, not the history.
Dated narrative and reasoning live in `decisions/decision-log.md` (36 entries, append-only)
and `the work log`. Nothing dated goes in this file.

Adopted 2026-09-20 from the `mrdaioff/baby-brain` pattern — see decision 37 for why.
**Keep this under 150 lines.** If it grows, the excess is history and belongs in the log.

Last updated: 2026-10-03

---

## Live campaigns

| Vertical | Launched | Loaded | Send rate | Replies |
|---|---|---|---|---|
| Water damage restoration | 2026-08-30 | 2,872 | 2/day per inbox | 1 positive (a water-damage owner (name withheld), 2026-09-12) |
| Roofing (general emails) | 2026-09-20 | ~800 | 7/day per inbox | — |
| Roofing (owner emails) | pending load | 956 | — | — |

Roofing was cut from 1,291 sendable to ~800 by Neil removing Outlook-hosted addresses in
the sequencer. **ESP filtering is Neil's, done in PlusVibe — never applied at list-build.**

**Targeting is now owner emails only** (decision 38). The 956-lead roofing list is 100%
named and 100% work-domain; the ~800 general-email list is 0% named and 72% role inboxes.

## Infrastructure

```
8 domains · 24 mailboxes (InboxKit)      $88/mo   = $39 plan + 14 extra @ ~$3.50
PlusVibe Personal                        $37/mo   includes free warmup (InboxKit warmup OFF)
Localpipe                                usage-based, no subscription (cancelled; balance still spends)
                                         -------
                                         $125/mo + usage
```

Warm-up began ~2026-08-11. Plan ramp (`plan/rave-launch-plan.md:190`): wk5 3/day, wk6 6/day,
wk7 10/day, wk8+ 15/day. **Gate on bounce rate under 3% — Neil checks; no live access here.**

## Lead inventory

| State | Count | Notes |
|---|---|---|
| Loaded and sending | 3,672 | 2,872 water damage + ~800 roofing |
| Clean, scraped, NOT enriched | ~6,460 | roofing — the 7,420 filtered pool minus 971 enriched |
| Clean, scraped, NOT enriched | 3,474 | tree service 1,252 · fence 685 · concrete 637 · deck 482 · paving 418 |
| Preserved server-side, unprocessed | ~1,900 | the cancelled `wd-depth-b` walk (PA/IL/OH/GA) |
| Consumer-domain, paid for, unused | 1,627 | decision 22 holds them back; revisitable |
| Water damage remaining | ~150 | 537 clean leftovers, 92% of that pool is franchise |

## Measured rates — use these, not estimates

```
business email          $0.005/find      owner email $0.02 — NEVER requested
owner name              $0.005/find      fires regardless when requested; unavoidable
maps scrape             $1.00 / 1,000 businesses ("Business Exports")
cost per sendable lead  $0.021 (water damage) · $0.0145 (roofing general) · $0.025 (roofing owner)
business email hit      ~46%
owner email hit         20.9% water damage · 13% roofing — use 13% for roofing
owner email quality     99.2% named · 94-99% work domain
business email quality  60% named · 53.7% work domain
consumer-domain loss    ~41% of emails found
franchise rate          water damage 45% · roofing 13-24% · tree service 12%
clean -> sendable       ~28%
```

`limit` on `/maps-search` is a **total task budget** (min 50, max 10,000), NOT per-pair —
docs changed 2026-09-20. `limit:"all"` is the only setting that reaches real depth.

## Copy

Source of truth is `copies/`, never memory or chat. `02-water-damage-FINAL.md` is the live
water-damage sequence. **Roofing copy is Neil's to write; QA means verify and flag only.**

Merge fields are PlusVibe snake_case: `{{first_name}} {{company_name}} {{city}}`.
Spintax is `{{random|a|b|c}}`. Localpipe returns the literal string `"not found"`, never
null — strip it at list-build or `{{fallback|...}}` will not fire.

Roofing leads carry **no owner names at all** (`first_name = "there"` on every row).

## Standing constraints

- Business-domain emails only. Owner emails never requested.
- Localpipe only — no AI Ark/Prospeo waterfall on this project.
- Quote costs in dollars, never credits.
- Never commit lead data, CSVs, `.jsonl` or PII. `jobs/` and `runs/` are gitignored.
- Run `scripts/secret_gate.sh` on staged content before every push.
- US only. Canada/UK blocked pending a CASL/PECR unsubscribe decision.
