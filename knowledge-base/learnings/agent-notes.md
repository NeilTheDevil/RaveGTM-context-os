# Agent Operating Notes

Read this before doing anything else in this repo. It is not a project summary —
`decisions/decision-log.md` and `plan/` cover that. This file is operational: mistakes
already made once in this project, verified, and worth not repeating. It is written for
any AI agent working on this repo, on any platform, using any tools — nothing here assumes
a specific agent, model, or harness.

Update this file when you find a new failure mode worth recording, the same way you'd
update code comments. Keep entries short, concrete, and dated. Delete an entry if it turns
out to be wrong or the underlying system changed.

---

## 1. A queued async job is not a stalled job

Localpipe's `/maps-search` and `/enrich` jobs report progress as `processing 0/N units` and
can sit there for over an hour before completing in a burst. This has been measured twice:
a 2,850-unit job held flat for 63 minutes then finished in under 4; a 7,765-unit job held
flat for over 80 minutes then finished the same way. Localpipe's own log line names this
directly: `fair-share queue; jobs never expire server-side — holding`.

**Do not cancel or resubmit a job because progress looks flat.** Poll for an actual
terminal status (their engine's log uses `DONE`). If a wait window closes without seeing
it, re-arm the wait — a closed watch is not evidence the job died. Check the underlying
process is still alive before concluding anything is wrong. This generalizes past
Localpipe to any submit-then-poll async API.

A job that WAS killed on this false assumption (2026-08-23) needed the poller manually
resumed — no data was lost, because the run's log/state files persist independently of the
poller process, but it wasted real time correcting course.

## 2. Verify computed output, not just fetched facts

When comparing a new batch against "everything scraped before it" for deduplication, make
sure the comparison set is built BEFORE the new batch is folded into whatever file you're
reading it from. A file that accumulates multiple tasks' output (e.g. one `leads.jsonl`
across two API tasks) will make a batch trivially match itself if you build the "prior" set
from that same file without filtering by task/source ID first.

This produced a false "0% net-new" result on 2026-08-30 — caught only because the number
was implausible given the inputs (two mostly-disjoint sets of US states shouldn't be 100%
overlapping) and was checked by hand before being reported. **Sanity-check generated
numbers the same way you'd verify a fetched fact** — does this make sense given what you
know about the inputs, before it goes to the user as a real number.

## 3. Franchise/chain rate is vertical-specific — do not generalize it

Measured across three independent geographic samples: water damage restoration runs
**45-46% franchised** (Servpro, PuroClean, ServiceMaster, Restoration 1, Paul Davis all
compete in this category). Roofing and tree service run **~12%** in the same filter, same
methodology. A franchise rate measured on one vertical is not a "local services" number —
state it per-vertical, every time. See `decisions/decision-log.md` #24, #26, #27, #28.

## 4. "Sendable" and "usable" are different numbers — report both, plan on the lower one

Localpipe's `/enrich` finding ANY email (owner or business) runs ~40-46% for local trades
in this project. But local trade listings return a real share of personal Gmail/Yahoo/
iCloud addresses as the "business" contact, and this project's standing policy (decision
22) is to exclude those from campaign one rather than isolate them — sending consumer-
domain volume through brand-new sending infrastructure burns it 3-5x faster.

The number that actually predicts campaign size is *sendable minus consumer-domain*,
measured at **31.1%** combined across 1,000 enriched leads in this project (three
independent batches, consistent). Do not quote the higher "sendable" figure as if it were
what will actually go out.

## 5. Localpipe's `"not found"` is a literal string, never null or empty

Any unresolved enrichment field comes back as the four-character string `"not found"`, not
`null`, not `""`, not absent. This defeats naive truthy checks (`if row.owner_email:`) and
breaks PlusVibe's `{{fallback|...}}` merge syntax, which only fires on a genuinely empty
field. **Strip `"not found"` to an empty string explicitly** before any downstream use —
list upload, fallback logic, or reporting a "found" count. `scripts/build_send_list.py`
does this; anything else touching enrichment output needs to as well.

## 6. Provider cost has no dollar figure anywhere in the API

Verified by reading the full API response schema and docs: there is no cost, price, or
balance field in `/enrich`, `/get-job-results`, or anywhere else. The only dollar reference
in the entire API surface is the 402 error body, `"Usage billing balance is $0"`.

If the account is on usage-based billing (as this one is), **credits are not a valid
substitute for dollars** — quote a dollar figure only when you can actually derive one
(e.g. from a balance the user reports back from their dashboard), and say plainly when you
cannot, rather than reporting a credit count as if it answers the cost question.

## 7. Not every JWT-shaped string is a secret

A Supabase `anon` key is meant to be public — it's embedded in browser clients, identical
for every customer of the service, and gates nothing without row-level-security policies
behind it. Before treating any `eyJ...` string as a credential to redact, decode it
(base64-decode the middle segment) and check the `role` claim. `role: "anon"` from a known
vendor's own published docs is not a secret. `role: "service_role"` is, unconditionally.
`scripts/secret_gate.sh` allowlists this project's specific known-public key by its exact
JWT header and flags everything else, including any `service_role` token.

## 8. A global tool/vendor default does not automatically apply to this project

This project uses **Localpipe only** for data — no AI Ark, no Prospeo, no other
verification vendor, even if a cross-project default elsewhere names them as a standard
waterfall. Check what a project has actually chosen before proposing a "standard" process
from outside it; presenting an unrequested default as if the user had specified it here is
a real error, not a harmless suggestion. See `rave-is-localpipe-only` if your memory system
carries project-specific notes across sessions — this repo intentionally deviates from a
broader default.

## 9. Copy in `copies/` is QA'd, not rewritten

QA on cold-email copy means verify and flag, never silently correct. Spacing, punctuation,
typos, and formatting choices (e.g. `22 %` with a space) are preserved character-for-
character unless the change is explicitly named. Functional syntax fixes (a broken merge
field, wrong spintax format for the target platform) are allowed but must be called out,
not folded in silently. See `copies/README.md` and `copies/QA-FLAGS.md` for the standing
rules and a live example of the distinction.

## 10. Secrets and lead data never enter version control

Gate every commit on `git diff --cached` via `scripts/secret_gate.sh`, never a file-level
sweep — a key can slip a naive scan and only a staged-content diff catches it reliably.
Lead CSVs, raw API dumps, and `.jsonl` data files are gitignored (`runs/`, `*.jsonl`) and
must stay that way; only the reproducible scripts that generate them belong in the repo.

## 11. Owner-email lookup is not "more verified" on usage-based accounts — don't pay for it by default

`want_email: true` (owner email, $0.02/find) was requested by default across ~6,000+
enrichments in this project on the reasoning that owner email is "always verified" while
business email might not be. That reasoning is wrong for usage-based billing accounts
specifically: the API docs state directly that **usage-based accounts receive pre-verified
business emails too** (`business_email` field, `want_general_email` flag, $0.005/find — 4x
cheaper). Neil caught this from his own Localpipe dashboard cost breakdown on 2026-08-30,
after $25.46 had already gone to owner-email lookups whose main effect was picking a
pricier address for businesses where a cheaper one would have worked just as well.

**Default to `want_general_email: true, want_email: false`** unless the campaign has a
specific reason to prefer the owner's personal inbox over a general business address (e.g.
copy that only makes sense addressed to a named individual). Check the account's billing
type before assuming owner-email's verification premium is worth paying for.
