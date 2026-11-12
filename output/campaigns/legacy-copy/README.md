# copies/ — the source of truth for Rave campaign copy

**This directory is where copy lives. Check here first, always — never from memory or from a
chat transcript.** If copy is needed for anything (upload, QA, spintax conversion, variable
mapping), read the file. Neil confirmed this rule on 2026-08-30.

Source document: `_Rave GTM Pilot Copies.pdf`, downloaded 2026-08-30.

## Rules for this directory

1. **Copy is transcribed verbatim.** Spacing, punctuation, capitalisation, `22 %`, typos —
   all preserved character-for-character. Nothing is normalised or "improved".
2. **QA means verify and flag, not rewrite.** Problems go in `QA-FLAGS.md`. The copy files
   themselves are never edited without Neil naming the change.
3. New copy versions get added as new files; old ones are not overwritten.

## Files

| File | Tab | Status |
|---|---|---|
| `01-copy-template.md` | ⚙️ Copy | Un-filled template — niche words still variables |
| `02-water-damage.md` | ⚙️ Water damage | Verbatim source — the pilot niche |
| `02-water-damage-PLUSVIBE.md` | ⚙️ Water damage | PlusVibe format, constants still variables |
| **`02-water-damage-FINAL.md`** | ⚙️ Water damage | **UPLOAD THIS ONE — job + signature baked in** |
| `03-moving-company-new-test.md` | 🚒 Moving Company New Test | Not in use |
| `04-moving-company-spintaxed.md` | 🛻 Moving company (Spintaxed) | Not in use |
| `05-reply-template.md` | ✉️ Reply Template | Reply handling + Calendly |
| `06-rave-gtm-pilot-copy-1.md` | Rave GTM Pilot Copy 1 | Review-based angle, has/no-review split |

| Support file | Purpose |
|---|---|
| `VARIABLES.md` | Every variable, mapped to a real scrape field. What we can fill vs cannot. |
| `QA-FLAGS.md` | Defects found. 4 critical, 3 minor, 4 judgment calls. Nothing auto-fixed. |

## Launch status — read before sending

The launch tab is fully resolved as of 2026-08-30. All 5 things it needed are done.

- Baked in as literal text: `job` = **water damage**, `signature` = **Neil Uko / Rave Web Studios**
- Live merge fields, using PlusVibe's confirmed real field names (see `VARIABLES.md` —
  the earlier camelCase names were wrong): `{{first_name}}`, `{{company_name}}`, `{{city}}`
- Spintax: **converted** — every block is `{{random|...}}`, including the subject line
- `first_name`: enrichment is done (2,007-lead list). 1,831 rows have a real name; the
  other 176 have the literal word `there` baked directly into the CSV — not a merge-time
  fallback, so nothing depends on `{{fallback|...}}` firing correctly
- `city`: stripped to the bare city name, no state abbreviation

Details in `QA-FLAGS.md`.
