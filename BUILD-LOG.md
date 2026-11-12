# Build Log — Week 1: Context OS

| | |
|---|---|
| **Name** | Neil Uko |
| **Company** | Rave (ravegtm.com), my own business |
| **Product** | Website redesigns for US owner-run local service businesses. $2,000 one-time build + $97/mo care plan. The owner sees a finished design for their trade, free, before paying; the real site is live within a week. |
| **ICP** | Owner-operated US local trades with high job values ($2k-$30k+), strong Google reviews and a website that undersells them. Priority verticals: foundation/waterproofing, water damage restoration, moving, tree service, fencing/decking, roofing, paving/concrete. Not franchises, not HVAC/plumbing first (most-emailed inboxes). Full ICP: [`context/icp/icp.md`](context/icp/icp.md) |
| **Buyer** | The owner. No committee. [`context/icp/personas.md`](context/icp/personas.md) |
| **GitHub repo** | https://github.com/NeilTheDevil/RaveGTM-context-os |
| **Context OS file** | https://github.com/NeilTheDevil/RaveGTM-context-os/blob/main/CONTEXT-OS.md |
| **Date** | 2026-11-13 |

## What I built

A Context OS in the course layout, filled with real context from Rave's cold-email system
(live since August 2026, two verticals sending).

| Step | Output |
|---|---|
| Scaffold + CLAUDE.md | [`CLAUDE.md`](CLAUDE.md), course folder layout |
| GTM Starter Kit skills, playbooks, tools | `.claude/skills/`, `knowledge-base/playbooks/`, `tools/` |
| Raw research (3 parallel subagents) | [`competitors`](context/docs/research/competitors.md), [`customer voice`](context/docs/research/customer-voice.md), [`signals and market`](context/docs/research/signals-and-market.md) |
| Synthesis | ICP, persona, [positioning](context/positioning/positioning.md), value proposition, [messaging](context/messaging/messaging.md), [facts](context/messaging/facts.md), brand kit, case studies |
| ICP in five layers, three personas | [`icp.md`](context/icp/icp.md), [`personas.md`](context/icp/personas.md) |
| System architecture | [`context/docs/gtm-system.md`](context/docs/gtm-system.md): 12 steps, tool and decisions per step, four-pillar check |
| One-page Context OS | [`CONTEXT-OS.md`](CONTEXT-OS.md) |
| `/signal-matrix` | [`context/icp/signal-matrix.md`](context/icp/signal-matrix.md): top 5 priority signals scored on the four tests; 7 verticals x website state, 13 signals kept, 7 killed, angle matrix |
| `/campaign-strategy` | [`output/campaigns/campaign-strategy.md`](output/campaigns/campaign-strategy.md): 26 ideas, 7 Tier 1 |
| `/build-workflow-spec` | [`strong-reviews-weak-website/workflow-spec.md`](output/campaigns/strong-reviews-weak-website/workflow-spec.md): tree service, rating 4.5+ and 25+ reviews, routed by which free site check fails (no HTTPS / old footer year / slow on phones) |
| `/campaign-copy` | 3-email sequence with facts trace and QA, plus a [PlusVibe export](output/campaigns/strong-reviews-weak-website/sequencer-export.md) |
| Ported from the live system | [state](context/docs/state.md), [open items](weekly-priorities/open-items.md), [agent notes](knowledge-base/learnings/agent-notes.md), [decision summary](knowledge-base/learnings/decision-log-summary.md), live copy, [Localpipe lead pipeline](tools/localpipe-pipeline/) |
| Meeting notes, priorities, work log | [`meetings/`](meetings/), [`weekly-priorities/2026-W46.md`](weekly-priorities/2026-W46.md), [`work-log/2026-W46.md`](work-log/2026-W46.md) |

## Tools and how they connect

Localpipe (Google Maps data, API), PlusVibe (sequencer, API), treg.to (CLI), Claude Code.
CLI/API over MCP for bulk work, per the course.

## What I learned

- These trades aren't in B2B databases, so the signals have to come from Google Maps data and free site checks, not hiring or funding.
- Most "signals" for local businesses are states (a weak site), not events. Storms are the main time-bound trigger. The workflow spec says so and plans to test it against plain volume sends.
- A facts file is what keeps AI-written copy honest. It kept a borrowed case study out of the new copy.

## Open before this workflow can send

1. Build the tree-service sample design at a live link (every email offers to show it).
2. Confirm the thresholds (4.5 / 25 reviews / 2022 / PageSpeed 50) on a real list.
3. Confirm the owner-email vs business-email choice (decision 38).
