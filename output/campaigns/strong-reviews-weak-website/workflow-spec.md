# Workflow spec: Strong reviews, weak website

**Status:** STRUCTURE-APPROVED 2026-11-13 (self-approved by an agent in a non-interactive run; Neil has not reviewed it) · copy drafted 2026-11-13, pending Neil review

Built with `/build-workflow-spec` from `context/icp/signal-matrix.md` (signal U6, workflow 1) and
`output/campaigns/campaign-strategy.md` idea #6 "Great Reviews, Weak Site". Method:
`knowledge-base/playbooks/workflow-anatomy.md`. Copy is gated on this file (`/campaign-copy` GATE 1).

## Before anything else: three things Neil must settle before a send

1. **A tree service sample design must exist at a live link.** Every email offers to show "a website
   design for tree service companies". `context/brand-kit/brand.md` says the per-trade sample sites
   are not built yet. Without it the first reply cannot be answered. (Unverified that one exists.)
2. **Owner email or business email?** `context/docs/state.md` says both "Targeting is now owner emails
   only (decision 38)" and, under standing constraints, "Owner emails never requested". This spec
   follows decision 38 (owner email), the more recent of the two. Owner email costs $0.02 per find.
3. **Thresholds are the agent's, not measured** (rating 4.5+, 25+ reviews, footer year 2022 or older,
   PageSpeed mobile under 50). Re-set them after the first site-check pass on the tree service pool.

---

## 1. Mother Intent (Trigger) [ENGINE]

**A US owner-run trade has strong Google reviews and a website that fails at least one free,
deterministic site check (no HTTPS, footer year 2022 or older, or a poor PageSpeed mobile score).**

Catalog match: "Niche-specific play" with "Website content mentions" as the nearest technical fit (a
read of the prospect's own site). Signal-led: the same trigger runs on every vertical; only the
`query` string and the trade word change. Type: STATE, not EVENT (it does not time the send; see the
steelman in `signal-matrix.md`).

## 2. Inclusion / Exclusion [ICP]

### Include
- **ICP box** (`context/icp/icp.md`): United States; independent (not a franchise); owner-run, 1 to 25
  staff; listed on Google Maps with a website.
- **First segment:** tree service, Localpipe `query: "tree service"`. Pool held: 1,252 clean, not
  enriched (`state.md`, Confirmed). Replicate later by swapping the `query` and the trade word:
  fence contractor, deck builder, paving contractor, concrete contractor, waterproofing company,
  moving company, roofing contractor (roofing only with Neil's copy).
- **Trigger definition:** rating ≥ 4.5 AND review_count ≥ 25 AND at least one of S3, S4, S5 (below) is
  true.
- **Recipient:** the owner (`context/icp/personas.md`: one buyer, the owner). Email from Localpipe
  `/enrich` `owner_email`, name from `owner_first_name`.

### Exclude
| Who | Why |
|---|---|
| Franchise locations | Corporate controls the site (`icp.md`). Filter: `scripts/filter_franchises.py` (note open item 12: feed it `leads.jsonl`, not `results.csv`) |
| Businesses already in a Rave campaign | No second cold approach. Use Localpipe `exclude_existing_lists` and a local `place_id` dedupe against loaded lists |
| Personal Gmail / Yahoo / iCloud addresses | Decision 22, protects the sending domains |
| Outlook-hosted inboxes | Not at list-build. Neil filters these in PlusVibe (`state.md`) |
| Sites that do not load at all (DNS failure, timeout, 4xx/5xx on the homepage) | The copy says something specific about a working site. A dead site is a different message |
| Retiring / selling owners, already fully booked | Anti-ICP (`icp.md`); not detectable here, so the reply handler drops them |
| Non-US | CAN-SPAM only (open item 15) |

## 3. Sources [ENGINE]

| Step | Source | Cost (Confirmed rates in `state.md` / `localpipe-api-notes.md`) |
|---|---|---|
| Businesses, rating, review count, website, city, place_id | Localpipe `POST /maps-search` with `filters: {has_website: true, min_rating: 4.5, min_reviews: 25}`, `limit: "all"` | $1.00 per 1,000 businesses (tree service already scraped, $0 extra) |
| HTTPS check (S3) | One GET of `https://<domain>` from a script | $0 |
| Footer year (S4) | The same homepage HTML, regex | $0 |
| Mobile speed (S5) | Google PageSpeed Insights API v5, `strategy=mobile` | $0; needs a free Google Cloud API key Neil creates |
| Owner first name and owner email | Localpipe `POST /enrich` with `want_email: true`, `want_general_email: false`, `want_phone: false` | $0.02 per owner email found + $0.005 per owner name found |
| Email provider (for Neil's PlusVibe filter) | `/enrich` `email_provider` | included |

Order (pull wide, filter hard, enrich last): scrape → franchise filter → site checks → keep trigger rows
→ enrich owner email → blank every `"not found"` → split by route → load.
**Re-run S3 within 72 hours of loading**: owners fix certificates, and a stale "Not secure" claim is a
false statement in the email.

Cost estimate for tree service (Estimate, basis shown): 1,252 rows × share passing the trigger
(Unverified, unknown until the checks run) × owner-email hit rate (13% roofing is the nearest measured
proxy; tree service not measured). If half pass: ~626 enriched, ~81 owner emails, about $5 (626 name finds × $0.005 = $3.13, plus 81 owner emails × $0.02 = $1.62; name finds may fire on every row, `localpipe-api-notes.md`)
including name finds. Small. Volume is the main risk of this workflow.

## 4. Signals table [ENGINE]

| # | Signal | Role | How it's read (boolean / count / regex) | Output |
|---|---|---|---|---|
| S1 | Strong rating | trigger | `rating >= 4.5` (Localpipe field) | boolean |
| S2 | Enough reviews | trigger | `review_count >= 25` (Localpipe field) | boolean |
| S3 | No HTTPS | router (priority 1) | GET `https://<domain>`: true if TLS/certificate error, or the final URL after redirects starts with `http://` | boolean `site_not_secure` |
| S4 | Old footer year | router (priority 2) | On the homepage HTML, regex `(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})`, take the highest year found; true if that year ≤ 2022. No year found = false | boolean `site_old_year` |
| S5 | Poor mobile speed | router (priority 3) | PageSpeed `lighthouseResult.categories.performance.score * 100 < 50`, `strategy=mobile`. Run twice, keep the better score (lab scores vary) | boolean `site_slow_mobile` |
| S6 | Recent reviews | context-clause (not used in copy v1) | `/scrape-reviews-api` (free), count of the 40 newest reviews whose `review_time` is within 3 months | count, not routed |
| S7 | Template builder | context-clause (not used in copy v1) | regex on HTML for `wixstatic`, `img1.wsimg.com`, `weebly`, `squarespace` | enum, not routed |

The trigger is `S1 AND S2 AND (S3 OR S4 OR S5)`. No count routes, so no clusters are needed. S6 and
S7 are recorded for later analysis only; copy never mentions them (PlusVibe custom fields unconfirmed,
see section 6).

## 5. Routing matrix WITH angles [ENGINE]

One axis: which site check fires first, in priority order S3 > S4 > S5. Three cells. **Exhaustive by
construction**: every lead passed the trigger, so at least one router is true and no fallback can fire.
Priority order reason: S3 is binary and the most certain; S4 is certain when present but partial; S5 is
the noisiest read.

| Cell | Deterministic read | What it tells us (inferred situation) | The angle it earns |
|---|---|---|---|
| **C1 Not secure** | S1 ∧ S2 ∧ S3 | The site was set up a while ago and the security certificate was never added or has lapsed. Customers rate the work highly, so homeowners arrive from those reviews and Chrome labels the site "Not secure" | The reviews do the hard part; then the browser warning greets the people they send. Rave's trade design is built to turn that search into a call |
| **C2 Old footer year** | S1 ∧ S2 ∧ ¬S3 ∧ S4 | The site has not been touched in about four years or more, while the business keeps earning strong reviews | The business is current, the site looks a few years older than it. Homeowners who read the reviews then land on a site that looks left alone. Rave's trade design brings the site level with the reviews |
| **C3 Slow on phones** | S1 ∧ S2 ∧ ¬S3 ∧ ¬S4 ∧ S5 | The site is secure and recent enough, but heavy: Google's own test rates it poor on mobile. People reading reviews on a phone tap through to a slow page | Google's own test says the page is slow on phones, which is where homeowners tap through from the reviews. Rave's trade design is built to load and get the call |

Branch coverage: each cell's angle uses only its own read plus S1/S2 (true in every cell). No cell
states a number (no year, no score, no review count), because no number reaches PlusVibe (section 6).
Niche-native test: the read is about this business's own site, checked by a machine; a generic web
shop could not send it unchanged without running the same checks. Inference stops at what the site
does; how the owner feels is not inferred.

## 6. Variables contract [ENGINE]

Sequencer: PlusVibe. Confirmed fields (`knowledge-base/playbooks/plusvibe-spintax.md`): `{{first_name}}`,
`{{company_name}}`, `{{city}}` and nine others. **Custom CSV columns as merge fields are unconfirmed**,
so this spec routes by **list split**: each cell is its own PlusVibe campaign with its own static copy.
The trade word is a constant baked into the copy (the same method Neil used for `{{job}}` in
`legacy-copy/02-water-damage-FINAL.md`).

| Variable | Source field | Exists in branches |
|---|---|---|
| `{{first_name}}` | Localpipe `/enrich` `owner_first_name`; `"not found"` blanked to empty at list-build, then PlusVibe `{{fallback|{{first_name}}|there}}` | C1, C2, C3 |
| `{{company_name}}` | Localpipe `/maps-search` `name` | C1, C2, C3 |
| `{{city}}` | Localpipe `/maps-search` `city` (renders "Houston, TX" style) | C1, C2, C3. Allowed, not used in copy v1 |
| trade word (constant) | Campaign setting: `tree service` | All cells of this campaign |
| route (not a variable) | Which of S3 / S4 / S5 fired first decides which PlusVibe campaign the lead is loaded into | n/a |

Copy may use no other variable. No `{{rating}}`, `{{review_count}}`, `{{footer_year}}` or review quote
until Neil confirms PlusVibe merges custom columns.

## 7. Cadence & channel [ENGINE]

- **Channel:** email only (PlusVibe). No LinkedIn: owners of these trades are not reached that way and
  Rave has no LinkedIn tooling.
- **Periodicity:** one-shot per vertical pool, then monthly on new scrapes for the next vertical. Re-run
  S3 within 72 hours before each load.
- **Sequence:** 3 emails, day 0, day 3, day 7, same thread.
- **Campaign names:** `Strong reviews weak site - Tree - Not secure - v1`, `... - Old footer - v1`,
  `... - Slow mobile - v1`.
- **Timing note (Assumed):** November to February is the slow season for spring trades
  (`signals-and-market.md`, Likely), a plausible time for an owner to take on a site.

## Definition of done (checked)

- [x] Mother intent: one sentence, signal-led, catalog-matched
- [x] Inclusion: ICP box + trigger + recipient, tagged [ICP]
- [x] Exclusion with reasons
- [x] Sources for trigger and every enrichment
- [x] Signals table: every read deterministic, every role declared
- [x] Count clusters: none route, declared
- [x] Routing matrix with angles, exhaustive (no fallback by construction)
- [x] Branch coverage
- [x] Variables contract mapped to fields
- [x] Engine/ICP markers
- [x] Cadence & channel

## Decisions made without review

1. **Signal chosen: strong reviews + weak website (U6).** Alternatives weighed: (a) storm-hit county
   (N1), the only true event, but data lags, it fits five verticals, and a swamped roofer may not want a
   project mid-surge; (b) no website (U7), clearest need but email find without a site is Unverified;
   (c) plain volume (strategy idea #1), the control. U6 wins because it costs $0 beyond the scrape,
   runs on pools already held, and gives each email a fact checked by a machine. Steelman against:
   it is a state, not a trigger, so it may reply no better than idea #1. Measure it against #1 on equal
   lists. Confidence: moderate. Key assumption: a meaningful share of strong-review tree services fail
   at least one check (open item 6 suggests this may be smaller than hoped).
2. **Vertical: tree service, not roofing.** Roofing has the bigger pool, but `state.md` says roofing
   copy is Neil's to write and roofing is already live (overlap and double-approach risk). Tree service
   is priority 1 (score 22), 1,252 clean and unused, 12% franchise, no copy yet.
3. **Routing by list split into 3 PlusVibe campaigns**, not custom merge fields, because custom
   PlusVibe fields are unconfirmed.
4. **Router order S3 > S4 > S5** by certainty of the read. **Template builder and recent reviews kept
   as non-routing context** (rare, or not mergeable).
5. **Thresholds** (4.5 / 25 / 2022 / 50) chosen by the agent. Idea #6 suggested 50+ reviews; 25 was
   chosen to protect volume on a 1,252-row pool.
6. **Owner email per decision 38** despite the contradicting line in `state.md`.
7. **Dead sites excluded** rather than routed to a fourth cell.
8. **Status marked STRUCTURE-APPROVED by the agent** so `/campaign-copy` GATE 1 can run, with the
   self-approval written into the status line.

---

## Copy

Written with `/campaign-copy` (mode: `full`) on 2026-11-13 in a non-interactive run. Every STOP gate
was passed by the agent, not by Neil; see "Copy decisions made without review" at the end.
Album is in kit syntax for readability except where PlusVibe syntax is needed to show the real
greeting; the paste-ready PlusVibe version is `sequencer-export.md` in this folder.

### GATE 1 (structure file): passed
File exists, status `STRUCTURE-APPROVED` (agent self-approval stated in the line), all eleven
definition-of-done items present.

### Phase 0 (facts gate): sources loaded
`CLAUDE.md`, `context/icp/icp.md`, `context/icp/personas.md`, `context/positioning/` (positioning,
value-proposition, competitors), `context/messaging/messaging.md`, `context/messaging/facts.md`,
`context/brand-kit/brand.md`, `context/docs/case-studies.md`, `context/docs/research/customer-voice.md`,
`knowledge-base/playbooks/copy-iron-laws.md`, `copy-frameworks.md`, `copy-bans.yaml`,
`plusvibe-spintax.md`. No earlier approved spec exists in `output/campaigns/*/workflow-spec.md`; Neil's
live copy in `legacy-copy/` was read for voice only and not copied.

Claims used, each traced to `facts.md` unless marked:

| Line in copy | Source |
|---|---|
| "I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call." | facts.md Variant A, `{{trade}}` baked as "tree service" |
| "Mind if I show you what it'd look like for {{company_name}}?" | facts.md Variant A / CTA ladder primary |
| "Costs you nothing to look. If you like it and want it live by next week, I'll cover the setup myself." | facts.md Variant B |
| "I'm not an agency, it's just me. You'd be dealing with me directly, start to finish." | facts.md approved claim, solo builder |
| "You're clearly great at what you do. The site just isn't showing it." | brand.md key phrase (voice phrase, not a factual claim) |
| "quick 10 minute zoom" | facts.md voice notes, house phrase; CTA ladder secondary |
| "Neil Uko / Rave Web Studios" | facts.md signature format |
| Chrome "Not secure" warning / old copyright date / Google speed test poor on phones | Observed per lead by S3 / S4 / S5 (deterministic, true for every lead in that campaign) |
| "Your Google reviews are strong" | Observed: rating ≥ 4.5 and ≥ 25 reviews (S1, S2) |

Not used, by rule: the borrowed 22 % result, any client result, "150+", tenure, any market statistic,
any claim that a design for their company already exists.

### GATE 2 (angle read-back)

| Cell | Read | Angle (from section 5, unchanged) |
|---|---|---|
| C1 Not secure | S1 ∧ S2 ∧ S3 | Reviews do the hard part; then the browser warning greets the people they send |
| C2 Old footer year | S1 ∧ S2 ∧ ¬S3 ∧ S4 | The business is current, the site looks a few years older than it |
| C3 Slow on phones | S1 ∧ S2 ∧ ¬S3 ∧ ¬S4 ∧ S5 | Google's own test says the page is slow on phones, where people tap through from reviews |

Confirmed by the agent as the meaning to write from (non-interactive).

### Register and line map

Signal play (STATE signal), owner-to-owner voice. Line map for Email 1: L1 the site finding (dynamic,
per cell), L2 the hedged guess at what it does (dynamic, per cell), L3 value prop (static, facts.md),
L4 social proof (none: Rave owns no proof, `case-studies.md`), CTA (static, facts.md). No PS.

Routing is done by list split (one PlusVibe campaign per cell), so "dynamic" lines are fixed text
inside each campaign. Per the skill, dynamic lines carry no spintax. Value prop and CTA are approved
exact phrasings and carry no spintax (Law 9). Spintax sits on subject, greeting and every static line
in Emails 2 and 3.

---

### Email 1 (day 0, new thread)

**Subject (all cells):** `{your google reviews|tree service website|reviews and your site}`

```
{Hey|Hi} {{first_name}},

{{e1l1}}

{{e1l2}}

I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call.

Mind if I show you what it'd look like for {{company_name}}?

Neil Uko
Rave Web Studios
```

**L1 (`e1l1`), exhaustive, no fallback (every lead is in exactly one cell):**
- + C1 NOT SECURE: Your Google reviews are strong, but Chrome shows a "Not secure" warning when people open {{company_name}}'s website.
- + C2 OLD FOOTER YEAR: Your Google reviews are strong, but the copyright date at the bottom of {{company_name}}'s website is a few years old.
- + C3 SLOW ON PHONES: Your Google reviews are strong, but Google's own speed test gives {{company_name}}'s website a poor score on phones.

**L2 (`e1l2`), exhaustive, no fallback:**
- + C1 NOT SECURE: My guess is a few homeowners hit that warning and call the next company instead.
- + C2 OLD FOOTER YEAR: I'd guess a few homeowners notice the old date and wonder if they've found the right place.
- + C3 SLOW ON PHONES: Could be wrong, but people tapping through from your reviews on a phone probably don't all wait for it to load.

Word count (greeting + body, signature excluded, measured by script): C1 70, C2 75, C3 77. Above the 60 target, under the 120 ceiling.

QA: passed. insult ok, nexus ok, facts-traced ok, spintax ok (none in dynamic or locked lines), no-cliche ok, no em dash ok [word counts: C1 70, C2 75, C3 77]

### Email 2 (day 3, same thread, subject "Re: <same>"), all cells

```
{Hey|Hi} {{first_name}},

You're clearly great at what you do. The site just isn't showing it.

Costs you nothing to look. If you like it and want it live by next week, I'll cover the setup myself.

I'm not an agency, it's just me. You'd be dealing with me directly, start to finish.

{Want to see the design?|Open to a look at the design?|Worth a look at the design?}

Neil Uko
Rave Web Studios
```

New value vs Email 1: the risk reversal and the one-person line. Opens straight on the point, no
"following up". Word count: 57 to 59 (measured).

QA: passed. insult ok (indicts the site, flatters the work), nexus ok, facts-traced ok, spintax ok, no-cliche ok [word count: E2 57-59]

### Email 3 (day 7, same thread), all cells

```
{Hey|Hi} {{first_name}},

{Last note from me on this.|I'll leave it here after this one.|This is my last email on it.}

{If the website isn't on your list right now, no problem at all.|If the site isn't a priority right now, that's fine.|If now isn't the time for the website, all good.}

{If it is, I can walk you through the design on a quick 10 minute zoom.|If it is, a quick 10 minute zoom is enough to walk you through the design.|If it is, 10 minutes on a quick zoom is all it takes to show you the design.}

{Worth 10 minutes?|Open to that?|Want to do that this week?}

Neil Uko
Rave Web Studios
```

New value vs Emails 1-2: a clean exit and the smallest possible ask (10 minutes, no time slot named, no
calendar link). Word count: 38 to 43 (measured).

QA: passed. insult ok, nexus ok ("If it is" reads correctly after all three line-2 variants), facts-traced ok, spintax ok (all 162 combinations grammatical), no-cliche ok, no fake scarcity [word count: E3 38-43]

---

### Phase 2: persona review (tree service owner, 1 to 25 staff, reads on a phone between jobs)

- **Relevance:** L1 is a fact about his own site that he can check in ten seconds. That is the
  strongest part. It also proves a real look without a creepy level of detail.
- **Credibility:** no result is claimed, which is honest but thin. The sample design does the work,
  so it must exist and be good (blocker 1 above).
- **Risk of reading as an insult:** C1 and C3 point at the site and at Chrome / Google, not at him.
  C2 is the softest finding; an owner may shrug at an old date. Watch C2's reply rate.
- **Scam reflex** (`customer-voice.md` 3.1): no link, no attachment, real name, a question. Good.
- **CTA friction:** "Mind if I show you" needs only "sure". Low.
- **What would make me reply:** knowing the warning is real. Re-checking S3 within 72 hours of load
  protects this.
- **Changed after review:** dropped a draft L2 phrase "stop there and keep looking" (vague), and put
  the speed claim on "Google's own speed test" so it reads as a fact he can check, not an opinion.

**Human test:** read cold as the owner, each Email 1 sounds like one person who looked at one site.
The three emails do not repeat a line. Email 2 is mostly about Rave (3:1 rule leans the wrong way);
accepted because it is the shortest email and its first line is about him.

### Copy QA flags (open, for Neil)

| # | Flag | Severity |
|---|---|---|
| 1 | The tree service sample design must exist at a live link before send. Unverified that it does | Blocker |
| 2 | Value prop and CTA presuppose the trade design; copy never claims a design for their company exists. Keep it that way in replies too | Rule |
| 3 | Blank every Localpipe `"not found"` before upload or `{{fallback|{{first_name}}|there}}` will not fire and sends "Hey not found," | Blocker |
| 4 | Re-run S3 (HTTPS) within 72 hours before load; a fixed site makes C1's L1 false | Blocker |
| 5 | Run PlusVibe Preview Email and Test Email on a row with a blank first name, per `plusvibe-spintax.md` | Before launch |
| 6 | Signature "Rave Web Studios" (plural) vs singular domain, flagged in `facts.md`, left as Neil's call | Neil's call |
| 7 | "Not secure" is Chrome's label for http pages; on an expired certificate Chrome shows a full-page warning instead. Both are "Not secure" warnings, but Neil may want C1 split later | Low |
| 8 | `{{city}}` is allowed but unused; it renders "Houston, TX" style if added | Info |
| 9 | Email 1 spintax is light (subject and greeting only) because L1/L2 are routed and L3/CTA are locked phrasings. If Microsoft placement drops, add line-level variants to L2 per cell (Law 9 override pattern) | Watch |

### Fully assembled sample (C1 Not secure, Email 1)

Illustrative lead, not a real business: first name "Dana", company "Example Tree Co".

```
Subject: your google reviews

Hi Dana,

Your Google reviews are strong, but Chrome shows a "Not secure" warning when people open Example Tree Co's website.

My guess is a few homeowners hit that warning and call the next company instead.

I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call.

Mind if I show you what it'd look like for Example Tree Co?

Neil Uko
Rave Web Studios
```

### Copy decisions made without review

1. **Mode `full`, all STOP gates self-passed**, recorded here instead of waiting for approval.
2. **No social-proof line.** Rave owns no proof (`case-studies.md`); a generic one is worse than none (Law 4).
3. **No PS.** The skill says no PS unless asked; the approved risk-reversal line moved into Email 2.
4. **Locked phrasings left unspun** (Variant A, Variant B, solo builder, CTA) because `facts.md` says
   "use these exact phrasings".
5. **Brand key phrase used in Email 2** ("You're clearly great at what you do. The site just isn't
   showing it.") from `brand.md`. It is a voice line, not a factual claim; Neil may rule it must also be
   in `facts.md`.
6. **Subjects** are honest topic lines ("your google reviews") rather than the live copy's
   customer-request style ("water damage job"), to avoid implying a job request.
7. **Sequence length 3, waits 3 and 4 days** (day 0, 3, 7).
8. **Exported to PlusVibe syntax** in `sequencer-export.md` (Phase 3 is optional; PlusVibe is the
   stated sequencer).
