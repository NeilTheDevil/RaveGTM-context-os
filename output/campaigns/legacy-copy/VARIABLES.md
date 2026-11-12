# Variables — what the copy asks for vs what we actually have

> **UPDATE 2026-08-30 — read this before the table below.** Everything under "The launch
> tab" section uses `{{firstName}}`/`{{companyName}}`, which are **wrong** — PlusVibe's
> real fields are snake_case: `{{first_name}}`/`{{company_name}}`. Also, enrichment has
> since run in full; `first_name` is no longer missing. See the "UPDATE 2026-08-30" section
> at the bottom of this file for the full correction. The body below is left as the
> historical record of the original state, not current status.

Pulled 2026-08-30 against `runs/all-verticals-supply-20260823-133047` (the live scrape).
Water damage restoration subset: **1,383 raw -> 738 clean independents** (628 franchise, 45%).

---

## The launch tab (`02-water-damage.md`) needs exactly 5 variables

| Variable | Uses | Source | Status |
|---|---|---|---|
| `{{firstName}}` | 9 | enrichment (owner name) | **MISSING — not scraped** |
| `{{companyName}}` | 8 | scrape field `name` | ready |
| `{{signature}}` | 6 | constant | needs Neil's signature block |
| `{{city}}` | 6 | scrape field `city` | ready, **but see format note** |
| `{{job}}` | 2 | not scraped — a constant for this niche | **needs a decision** |

That is a small surface. Three of the five are solved; two are not.

---

## Blockers

### 1. `{{firstName}}` does not exist in the scrape

The Localpipe maps scrape returns `name, phone, full_address, city, rating, review_count,
website, types, matched_category, price_level, place_id, business_id, latitude, longitude,
is_claimed, working_hours`. **No owner name and no email.**

Both come from the enrichment step, which has not been run. `{{firstName}}` appears 9 times
across the sequence — it is the single most-used variable in the copy.

Note also the PlusVibe trap already documented in `reference/plusvibe-spintax.md`:
Localpipe returns the literal string `"not found"` for unresolved fields, never null. So
`{{fallback|{{firstName}}|there}}` will **not** fire — it renders `Hi not found,`. Values
must be stripped to empty at list-build time.

### 2. `{{job}}` is undefined

Used in the subject lines (`{{job}} job` / `{{job}} request`) and nowhere in the body of the
water damage tab. It is not a scrape field. For a single-niche campaign it is a constant, so
it needs a value chosen — e.g. `restoration`, `water damage`, `water damage restoration`.

Subject renders as, respectively: "restoration job" / "water damage job" / "water damage
restoration job".

### 3. `{{city}}` carries the state

Scrape returns `"Houston, TX"` — 673 of 738 clean rows include `, ST`; 65 do not.

The copy reads "was looking for water damage restoration services in {{city}}" which becomes
"...in Houston, TX". Readable, slightly formal. Splitting to bare city is a one-line
transform if preferred. **Not changed — flagging only.**

---

## Variables used by the OTHER tabs (not needed for this launch)

These appear in tabs 1, 3, 4 and 6. Listed so nothing is a surprise if a tab is swapped in.

```
{{ICP}}                {{Jobs}}               {{Situation}}
{{TIMESLOT1}}          {{TIMESLOT2}}          {{TIMEZONE}}
{{company name}}       {{company}}            {{first_name}}
{{niche}}              {{results}}            {{reviewer's name}}
{{reviewerName}}       {{reviewline}}         {{specific review insight}}
{{the moving industry}}                       {{theirNiche}}
{{theirniches e.g-movers}}                    {{typeof businesses}}
{{types of companies}} {{whatReviewIsAbout}}
{{service/productTheyOffer}}
{{service/productTheyOffer e.g: bookkeeping software}}
{{their service/productTheyOffer}}
```

**Three naming collisions to be aware of** — the same value under different names, which
will silently render empty if the list column does not match:
`{{firstName}}` vs `{{first_name}}` · `{{companyName}}` vs `{{company}}` vs `{{company name}}`
· `{{reviewerName}}` vs `{{reviewer's name}}`

Several are clearly notes-to-self rather than real merge fields
(`{{service/productTheyOffer e.g: bookkeeping software}}`, `{{the moving industry}}`,
`{{theirniches e.g-movers}}`). They would send literally if uploaded as-is.

**The review variables** (`{{reviewline}}`, `{{reviewerName}}`, `{{whatReviewIsAbout}}`) are
fillable — `scripts/fetch_reviews.py` pulls them free via `/scrape-reviews-api`. Not run yet.

---

## UPDATE 2026-08-30 — real PlusVibe field names confirmed, and enrichment is done

Two things changed since this file was first written.

### 1. Everything above used the wrong variable name format

Neil screenshotted PlusVibe's own variable-insert dropdown. The real fields are
**snake_case**, not camelCase:

```
{{email}}          {{first_name}}      {{last_name}}       {{address_line}}
{{city}}           {{state}}           {{country}}         {{country_code}}
{{phone_number}}   {{job_title}}       {{department}}      {{company_name}}
```

Every `{{firstName}}` and `{{companyName}}` in this project's copy and CSVs was wrong —
close enough to look right, but not a real PlusVibe field, so it would not have merged.
Fixed everywhere in `02-water-damage-PLUSVIBE.md`, `02-water-damage-FINAL.md`,
`scripts/build_send_list.py`, and both send-list CSVs. `{{city}}` was already correct by
coincidence.

**Open question, not yet resolved:** whether PlusVibe accepts a custom CSV column name
outside this list as a merge field, or only recognizes the fixed set shown in its picker.
Didn't need to answer it this time — `first_name`, `company_name`, and `city` are all
standard fields already on the list. Worth confirming before ever adding a variable that
isn't one of the twelve above.

### 2. `first_name` is no longer blocked — enrichment ran

The original blocker below (no owner-name data) was resolved by a full nationwide
enrichment push the same day. The final 2,007-lead send list has a real first name for
1,831 rows (91%); the other 176 have the literal word **`there`** written directly into the
CSV — not a runtime merge fallback. See `decisions/decision-log.md` #26-29 for the full
supply and enrichment history.
