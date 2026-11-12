# PlusVibe Spintax — Syntax Reference

Source: https://help.plusvibe.ai/en/articles/8606174-spintax-guide
Verified 2026-08-13.

---

## Syntax

```
Spin variation   {{random|option1|option2|option3}}
Merge variable   {{variable_name}}
Fallback         {{fallback|{{first_name}}|Sir}}
Empty option     {{random||Hello}}
```

- `random` and `fallback` keywords are **case-insensitive**
- Spaces inside options are **preserved** in the output
- Options separated by pipes `|`

---

## ⚠️ Do NOT use SendKit spintax format here

PlusVibe uses **double braces with a `random|` prefix** — the Instantly-style format.
SendKit uses single braces with no prefix. They are not interchangeable.

```
❌ SendKit    {Hello|Hey|Hi}          → PlusVibe renders this literally
✅ PlusVibe   {{random|Hello|Hey|Hi}}
```

**The installed `spintax-sendkit` skill outputs the wrong format for this stack.**
Do not run it on PlusVibe copy.

---

## ⚠️ Fallback will NOT fire on Localpipe data

This is the one that will actually bite.

`{{fallback|{{first_name}}|there}}` only substitutes when the variable is **missing
or empty**.

Localpipe returns the **literal string `"not found"`** for any field it couldn't
resolve — never null, never empty, never absent. From their API docs:

> "Negative results are returned literally as the string `"not found"`"

So a missing owner name arrives as the text `not found`, the field is populated,
fallback does not trigger, and the email sends as:

```
Hi not found,
```

**Fix at list-build time, not in the copy.** Before uploading to PlusVibe, replace
every `"not found"` value with an empty string. Then fallback works as intended.

Applies to every enriched field: `owner_name`, `owner_first_name`, `owner_last_name`,
`owner_email`, `owner_phone`, `business_email`.

---

## Nesting limit: one variable per spin section

```
✅ {{random|Hello {{first_name}}|Hi there}}
❌ {{random|Hello {{first_name}} {{last_name}}|Hi there}}
```

Only **one** variable is supported inside a single spintax section. Two variables in
the same spin block fails.

Workaround — pull the second variable outside the spin:

```
{{random|Hello {{first_name}}|Hi there}} at {{company}}
```

Nesting spintax inside spintax is not documented either way. Assume unsupported until
tested.

---

## Before any send

PlusVibe's own guidance, quoted:

> "It's imperative to use the 'Preview Email' & 'Test Email' functions before
> finalizing or sending your actual campaign email."

Preview renders a real row. Test sends to a real inbox. Do both — spintax and merge
failures are invisible until rendered.

---

## QA checklist for copy going into PlusVibe

1. All spin blocks use `{{random|...}}`, not single braces
2. No spin block contains more than one `{{variable}}`
3. Every variable name matches a column in the uploaded list exactly
4. `"not found"` values stripped to empty before upload, or fallbacks won't fire
5. Fallbacks present on every variable that can be missing
6. Preview Email run against several real rows, including a row with missing data
7. Test Email sent to a live inbox and read on mobile

---

## Confirmed real field names — 2026-08-30

The names above (`{{first_name}}`, etc.) are illustrative in PlusVibe's own help docs, but
worth stating exactly: Neil confirmed via PlusVibe's own variable-insert dropdown in the
campaign editor that the actual system fields are:

```
{{email}}          {{first_name}}      {{last_name}}       {{address_line}}
{{city}}           {{state}}           {{country}}         {{country_code}}
{{phone_number}}   {{job_title}}       {{department}}      {{company_name}}
```

**snake_case, not camelCase.** This project initially built copy and CSVs using
`{{firstName}}` / `{{companyName}}` — close enough to read as correct, wrong enough to
never merge. Every campaign copy file and CSV column must use the exact names above.

**Unconfirmed:** whether a custom CSV column outside this list works as a merge variable
at all, or only these twelve fixed fields are recognized. Verify before ever introducing a
variable name not on this list.
