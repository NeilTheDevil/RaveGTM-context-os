# Rave — open items

Every unresolved thing, in one table. Adopted 2026-09-20 from `mrdaioff/baby-brain`
(decision 37): open items were previously scattered in decision-log prose, which is why
several below were raised three or more times without ever being closed.

**Status:** 🔴 open · 🟡 in progress · ✅ done · ⚪ waiting on someone else · 👤 human-only

**Nothing here is closed by an agent inferring it.** Mark ✅ only when the work was actually
done and verified, and move the row to `## Closed`.

## Open Items

| # | Logged | Owner | Item | Status |
|---|---|---|---|---|
| 1 | 2026-09-08 | 👤 Neil | **Email 3 offers "this Tuesday at 10AM EST" — a slot absent from the Calendly.** Weekly hours are 07:00-08:00 and 17:30-19:30 Mon-Fri, 10:00-14:30 Sat. Live in the water-damage sequence and sending now. Raised 8, 13 and 20 Sep. | 🔴 |
| 2 | 2026-09-08 | 👤 Neil | **Reply notifications unbuilt.** PlusVibe → Slack incoming webhook, event "All Email Replies", campaign-level. ~5 min. A positive reply went a day unanswered on 12 Sep. | 🔴 |
| 3 | 2026-08-30 | 👤 Neil | **The 22 % case study is borrowed** — it belongs to another client (another client (name withheld)) and appears 16 times as the entire proof layer. | 🔴 |
| 4 | 2026-08-30 | 👤 Neil | **Copy asserts a per-company mockup already exists** (Emails 1A, 1C, 2). Every reply asks to see it. Now live across two verticals. | 🔴 |
| 5 | 2026-08-30 | 👤 Neil | **Email 3 promises to send 5 homeowners.** Needs a fulfilment plan before it is quoted back on a call. | 🔴 |
| 6 | 2026-08-30 | 👤 Neil | **"Your site needs improving" premise unverified** — under 1% of the clean pool runs Wix/Squarespace. 20 min spot-checking live sites would settle it. | 🔴 |
| 7 | 2026-09-12 | ⚪ | **a water-damage owner (name withheld) outcome unknown.** Tuesday 10:00 EDT slot was 8 Sep. Did the call happen? | ⚪ |
| 8 | 2026-09-20 | 🔴 | **Roofing runway ~5 days.** ~800 leads at 7/day x 24 inboxes = ~168/day. 2,448 clean roofing leads sit unenriched (~$15 → ~700 more). | 🔴 |
| 9 | 2026-09-20 | 👤 Neil | **Ramp decision.** Water damage still at 2/day after 3 weeks; plan says wk6 = 6/day. Gate is bounce rate under 3%, checkable only in PlusVibe. | 🔴 |
| 10 | 2026-09-13 | 👤 Neil | **1,627 consumer-domain addresses paid for and unused.** Recommendation on file: send from 1-2 throwaway domains kept away from the 8 live ones. | 🔴 |
| 11 | 2026-09-20 | ✅ | **Roofing has zero owner names** — RESOLVED 2026-10-03 by the owner-email pivot; the 956-lead list is 100% named. Original text:  — every row is `first_name = "there"`. Backfill ~$5.20 for ~1,030, or write the copy with no first-name variable. Confounds the vertical test either way. | 🔴 |
| 12 | 2026-09-05 | 🔴 | **`scripts/filter_franchises.py` reads `name`; scrape `results.csv` writes `business_name`.** Brand matching silently no-ops on that input and under-reports franchises. Worked around by feeding `leads.jsonl`. Needs a worktree. | 🔴 |
| 13 | 2026-09-20 | 🔴 | **`engine/lp.py` cost estimates are wrong.** `MAX LEADS = limit × pairs` is the old semantics; `limit` is now a total task budget. `wd-global-sweep` was estimated at 48,750 leads / $48.75 — real answer 25. Needs a worktree. | 🔴 |
| 14 | 2026-08-23 | 👤 Neil | **Git history purge of `reference/inboxkit-mailboxes.csv`.** Commands handed over; classifier blocked the agent. Backup bundle at `a local backup bundle`. | 🔴 |
| 15 | 2026-09-05 | 👤 Neil | **Canada/UK blocked.** CASL needs consent; UK PECR permits B2B to limited companies but not sole traders. Both need an unsubscribe footer and postal address — the sequence has neither. | 🔴 |
| 16 | 2026-08-23 | 👤 Neil | **Roofing ticket size was inferred, never measured.** It was ranked #1 partly on the assumption a $2,000 site is small against a $10-30k roof job. | 🔴 |
| 17 | 2026-09-20 | ⚪ | **`exclude_existing_lists` not yet used.** 28 restoration list IDs cached at `runs/_input/exclude-list-ids.json`. Would have saved the 24% place_id overlap on the roofing pull. | ⚪ |
| 18 | 2026-09-12 | ⚪ | **~1,900 leads from the cancelled `wd-depth-b` walk** are preserved server-side and unprocessed. | ⚪ |
| 19 | 2026-10-03 | 👤 Neil | **Put `{{first_name}}` back in the roofing copy.** It was written without one because the Sept list had zero names. The new 956-lead list is 100% real first names. | 🔴 |
| 20 | 2026-10-03 | 👤 Neil | **Decide whether the ~800 general-email roofing list keeps sending.** It is 0% named and 72% role inboxes; running it alongside the 956 owner-email list means two cold approaches from the same sender to the same vertical. | 🔴 |
| 21 | 2026-10-03 | ⚪ | **~6,460 clean roofing leads still unenriched** from the 7,420 filtered pool. At the measured 13% roofing yield that is ~840 more owner emails for ~$52. | ⚪ |

## Closed

| # | Logged | Owner | Item | Closed | Status |
|---|---|---|---|---|---|
| — | 2026-08-30 | Neil | Water damage vertical exhausted and closed at 2,872 sendable | 2026-09-20 | ✅ |
| — | 2026-09-20 | Neil | Roofing vertical launched, ~800 leads at 7/day | 2026-09-20 | ✅ |
