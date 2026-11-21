# Guide template

The skeleton every build guide follows. `example-guide.md` is the same template filled in for a real spec: match its depth and tone. Replace everything in `<angle brackets>`. Keep the section order. Drop a Part only if the spec has nothing for it, and say so in one line.

```markdown
# Clay Build Guide: <workflow name> (<client>)

A step-by-step guide to building `<spec path>` in Clay. Written for someone who has never built anything in Clay. Follow the parts in order. Each step tells you **why** it exists, **what to click**, **what to type**, **how to check it worked** and **what it costs**.

> **Don't skip the checks.** <one line on running 1 row before many>

---

## Contents
<linked list of every section below>

---

## What you are building
<2 to 3 sentences: the spec's mother intent, filters, routing, and what gets sent, in plain words>

<N> tables inside 1 workbook:

![<diagram title>](<slug>-clay-flow.png)

Each row of the picture is a table. The numbers are the order you build in.

Why this shape:
- <why this table is the root (people-first / account-first / signal-first)>
- <why company checks happen once per company>
- <why paid steps come last>

What a finished row in **<main table>** looks like, reading left to right:
<one-row example table with made-up but realistic values>

---

## Clay words you need
<glossary table: Workbook, Table, Source, Column (plain / formula / enrichment), Formula, Enrichment, Lookup, Send table data, Run condition, Auto-run, Actions, Data Credits, View, plus any term this build adds>

---

## Before you start
<checklist: account and plan, connections, spec open, CSVs ready, test size>

---

## Part 0. Set up the workbook
## Part 1. <Exclusions / reference table>
## Part 2. <The source: search or import>
## Part 3. <Free gates>
## Part …  <one Part per table or stage, in build order>
## Part …  <Route each row to a cell>
## Part …  <Find and verify the work email>
## Part …  <Write the email lines>
## Part …  <Views for the operator>
## Part …  <Connect the sequencer (build it, don't run it)>

## What it costs
<table of every paid step: runs on / rough cost; free list; worked example for the test size>

## Final checklist
<tick boxes: auto-run off, run conditions, 1-row proofs, no duplicates, exclusions respected, held cells not ready, sample emails read aloud, sequencer paused, spend written down>

## When something goes wrong
<table: what you see / likely cause / fix>

## Things the spec needs to fix
<numbered list: section, problem, suggested change>
```

## The pattern for every step

```markdown
### <n.n> <Step name>

**Why:** <one or two sentences, tied to a spec section>

1. <exact click path, bold for buttons: **+ Add column** → **Formula**>
2. <what to type or select, with values from the spec>
3. **Run condition:** `<formula>` (paid columns only)
4. Run on **1 row**. <what to look at in the cell>
5. Then run on the rest.

**Check:** <a concrete test the reader can do, with expected results>
**Cost:** <free / about N Actions per row / Actions + Data Credits>
```

## The pattern for formula columns

Use a table when there are several short ones:

```markdown
| Column | Plain English | Formula |
|---|---|---|
| `<Name>` | <what it means, as you'd tell the AI helper> | `<formula>` |
```

Use this block for long ones (email lines, routing):

~~~markdown
#### `<Name>`: <what it is> (routes on <column>)

- **Plain English:** *"<description to paste into the AI helper>"*
- **Formula:**
```javascript
<formula>
```
- **Check:** <expected output on a named kind of row>
~~~

## The pattern for AI columns

```markdown
1. **+ Add column** → **Use AI** (or **Claygent** for the fallback).
2. Prompt:
   > *<full prompt with {{columns}}>*
3. Output format: **JSON**, with exactly these fields:
   - `<field>`: text, must be one of `<a>`, `<b>`, `<unclear>`
   - `evidence`: text
4. **Run condition:** `<formula>`
5. Run on **<2 or 3> rows you can judge yourself**: <which kinds>. Fix the prompt and re-run the same rows if any answer is wrong.
```
