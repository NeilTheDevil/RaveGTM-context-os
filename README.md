# Rave GTM — Context OS

The go-to-market Context OS for **Rave** (ravegtm.com): website redesigns for US owner-run local
service businesses, sold by cold email by one builder, Neil Uko.

Built for week 1 of the GTM Engineering course (GTM Systems Thinking and Context Engineering,
2026-11-07). It follows the course's Context OS layout and the
[GTM Starter Kit](https://github.com/bolaji-ships/gtm-starter-kit), filled with Rave's real
context from a cold-email system that has been live since August 2026.

Open it in Claude Code and start with [`CLAUDE.md`](CLAUDE.md). The build log for the course is
[`BUILD-LOG.md`](BUILD-LOG.md).

## The business in one line

Find local trades whose website is quietly costing them jobs, email the owner, and offer to
*show* them a finished redesign for their trade, free. If they like it, build the real site in
a week. **$2,000 build + $97/mo care plan.**

## What's inside

```
CLAUDE.md                  project instructions: where everything lives, ground rules
.claude/skills/            Claude Code skills (from the GTM Starter Kit)
context/
  icp/                     icp.md, personas.md, signal-matrix.md
  positioning/             positioning, value proposition, competitors
  messaging/               messaging.md, facts.md (the only source of claims in copy)
  brand-kit/               tone of voice, key phrases
  docs/
    research/              raw research: competitors, customer voice, signals and market
    source/                the original strategy brief digest and launch plan
    state.md               live campaigns, lead inventory, measured rates
    case-studies.md        proof Rave owns, and proof it may not use
knowledge-base/
  playbooks/               method docs the skills read (+ PlusVibe spintax notes)
  learnings/               agent notes (failure modes) and the decision-log summary
meetings/                  call notes, one file per meeting
output/campaigns/          campaign strategy, workflow spec and copy; legacy-copy/ = live copy
tools/
  localpipe-pipeline/      Google Maps → enrich → filter → send list (Rave's lead engine)
  rex/, crawl4ai/, agent-browser/   from the starter kit
weekly-priorities/         one file per week + open items
work-log/                  one file per week, every step logged
inspiration/               swipe file
```

## How it was built (the course's live-build flow)

1. Scaffold the folder structure and `CLAUDE.md`.
2. Raw research with parallel subagents: competitors, customer voice, signals and market urgency.
3. Synthesize into ICP, persona, positioning, value proposition, messaging, facts, brand kit.
4. Pull in the Starter Kit skills, playbooks and tools.
5. `/signal-matrix` → `context/icp/signal-matrix.md`
6. `/campaign-strategy` → `output/campaigns/campaign-strategy.md`
7. `/build-workflow-spec` for the strongest signal → `output/campaigns/<workflow>/workflow-spec.md`
8. `/campaign-copy` from that spec, facts-gated.
9. Log every step in `work-log/`, push to GitHub.

## What was left out of this public copy

This repo was duplicated from Rave's private working repo with fresh git history. Left out or
replaced with placeholders: sending domains and mailbox addresses, the full build-session
transcript, the raw decision log (a summary is in `knowledge-base/learnings/`), prospect names,
other clients' names, and all lead data. `.env`, CSV lead lists and `.jsonl` dumps are gitignored.

## Credits

Skills, playbooks and tools from the [GTM Starter Kit](https://github.com/bolaji-ships/gtm-starter-kit)
by Bolaji Anifowose. Some parts adapted from other open-source projects: see
[THIRD-PARTY.md](THIRD-PARTY.md).
