---
name: clay-build-plan
description: Turn an approved workflow spec into a beginner-friendly, step-by-step Clay build guide (Markdown) plus a swimlane flow diagram (PNG) showing every table, the numbered build order and which steps are free or paid. Use when someone asks for a "Clay build plan", "Clay build guide", "how do I build this spec in Clay", "step-by-step Clay instructions", or wants a workflow spec explained so someone who has never used Clay can build it. Writes instructions only; it never touches Clay itself (that is /build-clay).
argument-hint: [path to workflow-spec.md] [optional: where to save]
---

# Clay Build Plan

Produce two things from one approved workflow spec:

1. **`<slug>-clay-build-guide.md`**: a step-by-step guide someone who has never opened Clay can follow alone. Every step says **why**, **what to click**, **what to type**, **how to check it worked** and **what it costs**.
2. **`<slug>-clay-flow.png`** (+ `.html` source): a swimlane diagram, one lane per Clay table, numbered steps in build order, each tagged FREE or PAID, arrows showing how rows move between tables. Embedded at the top of the guide.

The quality bar is `references/example-guide.md` and `references/example-flow.png` (PaidHR, "New HR Leader, First 6 Months"). Match their depth, tone and structure.

**This skill writes instructions, not Clay tables.** To build in Clay through the API, use `/build-clay`.

## Inputs

- **Required:** the path to an approved workflow spec (from `/build-workflow-spec` or `/workflow-spec`). Check its status line. If it isn't approved, or the routing matrix has no angle per cell, stop and say what's missing. Don't invent segment, persona or routing logic to fill gaps.
- **Ask if not given:**
  - **Where to save.** Never write into a repo or folder that will be built live in front of an audience (for example, a repo you'll build live in a workshop: keep its guide somewhere else). If unsure, ask. Never commit.
  - **Test size** for the first import (default 25 rows).
- **Read if present:** the client's `context/messaging/facts.md` (for copy lines), any approved copy in the spec, the exclusions or suppression lists.

## Procedure

### 1. Read (silently)
- The whole spec, every section.
- `references/clay-rules.md`: costs, keys, search filters, AI-column contract, copy-line rules. **Every guide must follow it.**
- `references/guide-template.md`: the section skeleton and step patterns.
- `references/example-guide.md`: the finished example.

### 2. Design the build
Decide, then write it down at the top of the guide ("What you are building"):
- **Architecture.** People-first when the trigger happens to a person (new hire, job change). Account-first when the ICP starts from companies. Signal-first when a dated company event triggers it (funding, job posts).
- **Tables** (aim for 3 to 5): the main table (one row per person or company), a Companies table when company checks apply to people (checks happen **once per company**), an Exclusions table from the spec's exclude list (keyed on **domain**), and a satellite table only when a count or second search needs one.
- **Map each spec section to Parts:** sources (spec §3) → search and enrichment steps; signals (§4) → formula or AI columns, each with its role; routing matrix (§5) → a `Cell` formula and a `Ready to Contact?` gate; variables contract (§6) → helper formulas and copy-line formulas; cadence (§7) → sequencer step and views.
- **Order:** free before paid, cheapest gate first, every paid column behind a run condition. Any company-level gate that can hold a company back (mailbox provider, vertical check, legal headcount) runs **before** finding people, so people and emails are never paid for at a company that can't be sent to.
- **AI vs formula:** follow `clay-rules.md`. Use AI for semantic judgements the spec routes on (workforce type, what the company does, still employed), with Claygent only as the fallback. Everything deterministic stays a formula.

### 3. Make the diagram
1. Write `<slug>-clay-flow.json` (format: `references/example-flow.json`):
   - one lane per table, top to bottom in the order rows first touch them; the main table gets `"main": true`; reference tables get `"dashed": true`
   - steps numbered in build order (0 for anything uploaded first), **9 columns at most** (merge small steps), each with a 3 to 5 word title, a one-line description and `"cost": "free" | "paid"`
   - `"highlight": true` on the routing step (where cells are decided)
   - arrows for every hand-off between tables, labelled when the meaning isn't obvious ("checked against", "company facts go back to each person")
2. Render: `python3 .claude/skills/clay-build-plan/scripts/render_flow.py <json> <out.png>` (needs Google Chrome and `pip install selenium`; writes the `.html` next to the PNG). If it can't run, keep the `.html`: opening it in a browser shows the same diagram.
3. **Look at the PNG** with Read. Fix overlapping labels, boxes wrapping into 6+ lines or arrows crossing text, then re-render.

### 4. Write the guide
Follow `references/guide-template.md` section by section. Non-negotiables:
- Glossary of Clay words before the first step.
- Every step uses the step pattern: **Why** (tied to a spec section), numbered click path, values to type, **Check**, **Cost**.
- Every formula column: name, **plain-English description** (to paste into Clay's formula AI helper and keep as the column description), formula, check.
- Every AI column: full prompt, JSON output fields with enums, run condition, "prove on 2 to 3 rows you can judge", and what `unclear` means for routing.
- **Every lookup keyed on domain.** Exclusions CSV is `Company Name | Domain | Type`; leave domains blank rather than guess them, and say how to fill them in.
- Copy lines from the spec become formulas, verbatim, each guarded by `Ready to Contact?`. Spintax stays in the sequencer.
- **No routing (static spintax copy, only `{FIRST_NAME}` / `{COMPANY}`-style tokens):** don't build copy formulas. Clay cleans the variables (first name, company name); the copy goes into the sequencer step, pasted verbatim. Generate those copy blocks from the spec text in code and check every variant appears in the guide (missing = 0).
- Held cells (spec says build, don't send) stay in the table with `Ready to Contact?` false.
- The sequencer step is built and **not run** unless the spec says the campaign can send.
- Cost table with a worked example for the test size.
- Final checklist, troubleshooting table, and "Things the spec needs to fix" (don't edit the spec).
- Where you aren't sure of a Clay UI label, give the likely name plus a fallback instruction.
- No em dashes, no "curious". No invented facts, names, domains or numbers.

### 5. QA before handing over
- [ ] Every table in the diagram has a Part, and every Part's table is in the diagram.
- [ ] Step numbers in the diagram match the Parts' order.
- [ ] Every paid column has a run condition and a 1-row (or 2 to 3 row for AI) proof.
- [ ] Every lookup matches on domain.
- [ ] Copy lines match the spec word for word.
- [ ] Cost table lists every paid step in the guide.
- [ ] `grep -c "—"` on the guide returns 0.
- [ ] The image path in the guide resolves next to the guide file.

### 6. Hand over
Save the `.md`, `.png`, `.html` and `.json` together in the agreed folder. Show the PNG in chat, summarise the build (tables, parts, paid steps, rough cost for the test size) and list the spec fixes. Log the work in the relevant work log with a timestamp. Don't commit, don't publish, don't edit the spec unless asked.

## Files
- `scripts/render_flow.py`: JSON → HTML → PNG swimlane renderer (Treford palette, Rubik).
- `references/clay-rules.md`: Clay facts and conventions the guide must follow.
- `references/guide-template.md`: section skeleton and step patterns.
- `references/example-guide.md`, `references/example-flow.json`, `references/example-flow.png`: the PaidHR example.
