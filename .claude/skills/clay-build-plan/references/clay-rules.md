# Clay rules for build guides

Facts and conventions every guide must follow. Sources: Clay University "Actions & Data Credits", Rex `LEARNINGS.md` / `action-registry.md` (`tools/rex/`), and the PaidHR example guide. If something here conflicts with what Clay shows today, trust Clay and update this file.

## What costs what

| Free (0 Actions) | Paid |
|---|---|
| People and company searches, and importing their results | Enrichments (Enrich Company, Enrich Person, any provider): about 1 Action per row per run |
| CSV imports | Use AI and Claygent: 1 Action per row plus AI cost (Claygent costs more: it browses) |
| Formulas, filters, views | Email waterfalls: Actions plus Data Credits for each provider step that actually runs |
| Lookups (single row, multiple rows) | HTTP API calls |
| Send table data (rows between Clay tables) | Pushing a lead to a sequencer: 1 Action per lead (Clay's own sequencer: 1 Action per lead added to a campaign, not per email) |

- **Unused Actions expire** at the end of the month and can't be topped up. Only a plan upgrade adds more.
- **Never state a cost from memory** that isn't in this table. Write "about" and tell the reader to watch the Actions counter.

## Build order (always)

1. Free sources, then free gates (formulas, lookups) before anything paid.
2. Company-level checks **once per company**, in a Companies table fed by Send table data with dedupe on domain.
3. Every paid column gets a **run condition** so it only runs on rows that passed every check before it.
4. Prove every paid column on **1 real row** (AI columns: 2 or 3 rows you can judge yourself), read the cell, then run the rest.
5. **Auto-run off** on every table before adding columns.
6. Delivery (sequencer push) is built last and **not run** until the spec says the campaign can send.

## Keys and lookups

- **Every lookup matches on domain.** Never on company name: names clash ("Bamboo", "Remote", "MAX") and vary ("Oando", "Oando PLC").
- Domains are written plain: `acme.com`. No `https://`, no `www.`, no trailing slash. The Exclusions CSV uses the same format.
- Person dedupe key: LinkedIn Profile. Company dedupe key: Company Domain.
- Only **formula** columns carry cleanly across a lookup. If another table needs an AI answer, add a one-field formula next to the AI column (e.g. `Deskless?`) and look that up.
- Give domain and URL columns the **URL** data type, email columns the **Email** type.

## People search (Search DSL)

- Clay's people search can filter **current job title (include and exclude)**, **person country**, **company size**, **company industry (exclude)** and **start date of the current job**, all in one search. The preview count is free: use it as the volume check.
- Start dates come as `YYYY-MM`. "180 days" becomes "6 months or less".
- Company size buckets: `1`, `2-10`, `11-50`, `51-200`, `201-500`, `501-1,000`, `1,001-5,000`, … A floor of 10 becomes 11.
- A company location filter matches **any office**, not the HQ. Check HQ country after Enrich Company.
- The search payload holds company domain and start date even when they aren't columns: tell the reader to open a cell and **Add as column**.
- UI labels move. When unsure of a filter or field name, write the likely name and a fallback ("may be called … If you can't find it, …").

## People search scoped to companies

- To find people at a set of companies you already have, start Find people **from a table**: pick the Companies table and a **view** filtered to the companies that passed. Never tell the reader to copy and paste domains: a pasted list is a snapshot and misses companies that qualify later. (Same as Rex's `filter_to_companies` on a view.)
- One domain can match several companies in Clay's database. After the search, compare the number of companies found with the view's row count, and drop people whose company lookup doesn't come back qualified.

## Title filters

- Excluding "Officer" or "Executive" also removes "Chief People Officer" / "Chief Executive". Exclude those words with a formula that keeps titles containing "Chief" or "Director".

## AI columns

- Use AI only when the job can't be done reliably by a formula. Classifying **how staff work**, **what a company actually does** or **whether someone is still employed** needs AI. Matching, counting, routing and copy from approved lines don't.
- **Use AI first** (reads row data already paid for, e.g. the Enrich Company description). **Claygent only as a fallback** (browses the website) when Use AI returns `unclear` or the input is empty.
- Every AI column has: the prompt written out in full, a **JSON output** with named fields, **enums** for any field that routes (e.g. `deskless | office | unclear`), an `evidence` field the reader can check, and a run condition.
- Decide what `unclear` means for routing and write it down (e.g. "unclear counts as office, because the office email is safe for everyone").
- `Still Employed?` (YES / NO / REVIEW) is recommended for role-based outreach. Downstream gates require exactly YES.

## Formulas

- Every formula column comes with a **plain-English description**: the reader pastes it into the formula's Use AI helper, and it stays as the column description.
- In guides, columns are written `{{Column Name}}`; tell the reader to type `/` to insert a column.
- Guard blanks: `({{X}} || "")`.
- Avoid `new Set` and the spread operator `...`: Clay returns empty results silently.

## Copy lines

- Approved line-based copy becomes **formula columns, not AI**: each line picks its approved variant by the routing columns. Copy the wording **verbatim** from the spec.
- Each line starts with `!{{Ready to Contact?}} ? "" :` so rows that won't be emailed stay blank.
- **Spintax stays in the sequencer template.** Sequencers don't process spintax that arrives inside a Clay variable.

## Mailbox provider (MX)

- To split Google / Outlook / other (security gateways like Proofpoint, Mimecast), use an **HTTP API** column per company: `GET https://dns.google/resolve?name={{Company Domain}}&type=MX` (free public DNS, no key; 1 Action per row in Clay). A formula maps the `Answer[].data` hosts: `google`/`googlemail` → Google, `outlook.com`/`protection.outlook` → Outlook, empty → None, else Other.
- After the email waterfall, check the email's domain equals the company domain; mismatches go to a review view (company-level checks didn't cover them).

## Email waterfall

- One native "Find work email" waterfall, own-key providers first, about 4 steps, validation on, strict (no catch-all, no risky).
- Run condition: the final "ready" gate. Never on every sourced row.

## Writing rules for the guide

- Reader has never used Clay. Explain every Clay word the first time (glossary section).
- No em dashes. No "curious".
- Don't invent facts, customer names, domains or numbers. Leave a blank or a `{{placeholder}}` and say what to fill in.
- Spec problems found while writing go in a "Things the spec needs to fix" section. **Don't edit the spec** unless asked.
