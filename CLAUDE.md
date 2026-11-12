# Rave GTM — Context OS

This folder is the go-to-market Context OS for **Rave** (ravegtm.com): website redesigns for
US owner-run local service businesses. Every session starts here. Read this file, then the
file the task needs. Do not work from memory or old chats.

## The company in one line

Rave finds local trades whose website is quietly costing them jobs, emails the owner, and
offers to show them a finished redesign for their trade, free, before any money changes
hands. If they like it, Rave builds the real site within a week.
Offer: **$2,000 one-time build + $97/mo care plan** (hosting, maintenance, changes). Solo
builder, not an agency.

## Where things live

| Need | File |
|---|---|
| Current state (live campaigns, lead inventory, measured rates) | `context/docs/state.md` |
| ICP, anti-ICP, vertical ranking | `context/icp/icp.md` |
| Buyer persona (the owner) | `context/icp/personas.md` |
| Signal matrix (segments x buying signals) | `context/icp/signal-matrix.md` |
| Positioning, value proposition, competitors | `context/positioning/` |
| Core message, pillars, objections | `context/messaging/messaging.md` |
| **The only allowed source of claims in copy** | `context/messaging/facts.md` |
| Tone of voice, signature, phrases | `context/brand-kit/brand.md` |
| Proof we own (and proof we may NOT use) | `context/docs/case-studies.md` |
| Raw research (competitors, customer voice, signals) | `context/docs/research/` |
| Original plan docs this OS was built from | `context/docs/source/` |
| Campaign ideas, workflow specs, copy | `output/campaigns/` |
| Live, Neil-written copy (verbatim, QA only) | `output/campaigns/legacy-copy/` |
| Method docs the skills read | `knowledge-base/playbooks/` |
| Lessons from this build (failure modes) | `knowledge-base/learnings/` |
| Call notes, one file per meeting | `meetings/` |
| This week's priorities / open items | `weekly-priorities/` |
| What happened, timestamped | `work-log/` |
| Lead pipeline (Localpipe scrape, enrich, filter) | `tools/localpipe-pipeline/` |

## Skills (type `/` to list)

Research to copy, in order: `/signal-matrix` → `/campaign-strategy` → `/build-workflow-spec` →
`/campaign-copy` → `/campaign-qa`. Clay skills (`/build-clay` and friends) come from the GTM
Starter Kit and are not used yet: Rave sources from Google Maps through Localpipe, not Clay.

## Tools and how to connect

- **CLI or API first, MCP last.** Bulk work (scraping, enriching, loading thousands of leads)
  goes through an API or CLI so it does not bloat the context window.
- Localpipe: API, scripts in `tools/localpipe-pipeline/`. Data source for every lead.
- PlusVibe: sequencer, API key in `.env`.
- treg.to: CLI, logged in per project. Paid calls need Neil's go first, with the price shown.

## Ground rules

1. **Plan before doing.** Goal, approach, what stays untouched, how success is checked.
2. **Log as you go.** After every finished step, append one timestamped line to this week's
   file in `work-log/` (`YYYY-Www.md`). Tick items in `weekly-priorities/` when done.
3. **Copy facts come only from `context/messaging/facts.md`.** Anything not there renders as
   `{{placeholder}}`. Never invent a result, a client, a number or a review.
4. **Neil's copy is never rewritten.** QA means verify and flag in a QA file. Spacing,
   punctuation and formatting (e.g. `22 %`) are kept character for character.
5. **No em dashes in prospect-facing copy.** Short, plain, one idea per email.
6. **Never commit** `.env`, keys, lead CSVs, `.jsonl` dumps, mailbox lists or prospect names.
   Run `tools/localpipe-pipeline/scripts/secret_gate.sh` on staged changes before a push.
7. **Quote costs in dollars**, not credits. Ask before any paid call.
8. **Label claims:** Confirmed (checked, with source) / Likely / Unverified.
9. Read `knowledge-base/learnings/agent-notes.md` before touching Localpipe or the pipeline.
