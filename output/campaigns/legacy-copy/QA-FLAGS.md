# QA flags — `02-water-damage.md` (the launch tab)

> **UPDATE 2026-08-30:** flags 1 and 2 are RESOLVED in
> **`02-water-damage-PLUSVIBE.md`** — the send-ready file. Neil approved the PlusVibe
> conversion and the `there` fallback. The verbatim source file is unchanged.
> Flags 3 and 4 remain open. Flag 3 now has a hard dependency: see "not found" below.

QA'd 2026-08-30. **Verify-and-flag only. Nothing in the copy files has been edited.**
Every line in `copies/` is Neil's text character-for-character, typos included.

---

## CRITICAL — these break on send

### 1. ~~All 66 spin blocks are in SendKit format~~ — RESOLVED in the PLUSVIBE file

The spintaxed sections use single braces: `{Hey|Hi}`.
PlusVibe requires double braces with a `random|` prefix: `{{random|Hey|Hi}}`.

Counted in the launch tab: **66 single-brace spin blocks, 0 in PlusVibe format.**

PlusVibe renders single braces **literally**. Every spintaxed email would arrive with visible
curly braces and pipes — e.g. `{Hey|Hi} Mike, {was looking for|I was searching for}...`

Source: `reference/plusvibe-spintax.md`, verified against PlusVibe's own docs 2026-08-13.

Either convert all 66, or upload the **raw** (non-spintaxed) versions, which are clean and
send fine as-is. Conversion is mechanical and I can do it on your word — it is a format
change only, no wording touched.

### 2. ~~Email 2 opener will not merge — `{[firstName}}`~~ — RESOLVED in the PLUSVIBE file

```
Hey {[firstName}},
```

Square bracket instead of the second brace. This is not a valid merge field in any
sequencer, so it sends **literally as typed**: `Hey {[firstName}},`

Appears in the raw Email 2 of the launch tab. (The spintaxed Email 2 below it is correct —
`{Hey|Hi} {{firstName}},` — so only the raw version is affected.)

Same typo exists in `01-copy-template.md`.

### 3. ~~`{{firstName}}` cannot be filled yet~~ — RESOLVED, and renamed

Was 9 uses of a field that didn't exist yet. Since then: the variable was renamed
`{{firstName}}` -> `{{first_name}}` (PlusVibe's real field name — see `VARIABLES.md`), a
full nationwide enrichment ran, and the `"not found"` string was stripped as part of
building the send list. The 2,007-lead list has a real name for 1,831 rows; the other 176
have the literal word `there` written straight into the CSV, not relying on
`{{fallback|...}}` firing at merge time.

### 4. ~~`{{job}}` has no value~~ — RESOLVED

Baked in as the literal text **water damage** (Neil's choice — reads as the customer's own
word for the problem, not the industry's). Subject lines now read `water damage job` /
`water damage request`, with a spintaxed version added:
`{{random|water damage job|water damage request}}`.

---

## MINOR — cosmetic, will send but read slightly off

| Location | Issue |
|---|---|
| Email 2, raw | `their first 30 days..` — double period |
| Email 2, raw | `not other companies  in {{city}}` — double space before "in" |
| ~~Email 3, spintax~~ | ~~`I will set it up for your teamand send you` — missing space in "teamand"~~ **FIXED 2026-08-30** — Neil named the change. Corrected in `02-water-damage-PLUSVIBE.md` and `02-water-damage-FINAL.md` only. `02-water-damage.md` (the verbatim source) keeps the original typo, since its whole purpose is preserving exactly what was in the PDF. |

**Not corrected.** The remaining two are one-character fixes but they are your text to change.

---

## PRESERVED DELIBERATELY — not errors

- **`22 %` with a space before the percent sign** — 16 occurrences. This matches your
  established formatting style and has been left exactly as written throughout.
- **`Het` instead of `Hey`** in tabs 3 and 4 — preserved verbatim in those files. Not in the
  launch tab.

---

## JUDGMENT — your call, no action taken

### 5. The `22 %` claim is a borrowed case study

Decision 27 flagged this. The result belongs to another client
(another client, name withheld). It appears **16 times** across the
launch sequence — it is the entire proof layer of the campaign, not a garnish.

For water damage specifically the mismatch is smaller than it would be for roofing, since
the source cases are restoration. Still unresolved.

### 6. The copy asserts a mockup already exists

Email 1A: *"Mocked up a full site with the improvements."*
Email 1C: *"Can I show you a website I made for {{company_name}}?"*
Email 2: *"Actually made a mock up with those changes implemented."*

These are stated as completed work, per-company. Any reply asks to see it. At 738 clean
water-damage leads, that promise needs either real per-company mockups or a fast turnaround
when a reply lands.

### 7. The "your site needs improving" premise is still unverified

Email 1A: *"Had a look at your website and saw some improvements you can make."*

Measured in decision 27: **under 1%** of the clean pool runs a Wix/Squarespace/Facebook-page
site. They overwhelmingly own real custom domains. Nothing in the scrape data establishes
that their sites are actually weak. Twenty minutes spot-checking real sites would settle it.

### 8. Email 3 promises lead delivery

*"send you 5 homeowners looking for water damage restoration services you can close into jobs."*

A concrete deliverable on top of the website. Worth confirming you can supply it before it
goes out, since it will be the thing that gets quoted back to you on a call.
