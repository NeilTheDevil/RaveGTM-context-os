# Building Your GTM Workflow (GTM Engineering course, Week 2)

- Date: 2026-11-14 (Saturday)
- Title: Building Your GTM Workflow (Clay fundamentals, lists, enrichment, deliverability, live PaidHR build)
- Teacher: Bolaji Anifowose (a moderator spoke at the start and end; this was announced as his last session, new faculty from the next one)
- Attendees: cohort (names not listed)
- Recording length: 229 minutes
- Source: Whisper auto-transcript (2,823 lines, no timestamps, heavy recognition errors) cross-checked against the Week 2 build brief, the session deck and the Clay credits doc. Normalized: "clay/cle/play/click" = Clay, "PD child/PDHR/Patreon/paid HR" = PaidHR, "Claygent" never clearly appears, "votes" = words (inferred), "Zap meal/Ice meal/Scaled meal" = ZapMail, Icemail (inferred), Scaledmail (inferred), "email guard" = EmailGuard, "mail reach" = MailReach, "short last" = Shortlist (inferred, an example company), "Wrong conditions" = run conditions.
- Timestamps below are approximate minutes, estimated from line position in the transcript (line / 2,823 x 229), so treat them as plus or minus 10 minutes (inferred).
- Gap to know: the transcript ends the live build at the email waterfall and the sequencer overview. The Workforce Use AI column, Claygent fallback, satellite table, Cell and Ready to Contact? routing, Email Matches Company?, groups and the Ready to send view are in the written brief and credits doc, not in the recording.

## TL;DR

- Week 2 turns the Week 1 workflow spec into a Clay workbook: folder, workbook, then tables (Exclusions, people, Companies, existing HR team), built in the order Find, Enrich, Transform, Create.
- Cost discipline is the lesson: searches, formulas, lookups and Send table data are free; enrichments, AI and email finders cost. Auto-run off, run conditions on every paid column, prove on one row first.
- The live build used the new `clay-build-plan` skill (pulled from the GTM Starter Kit) to turn the spec into a step-by-step guide plus a swimlane diagram, then followed it click by click.
- The email waterfall runs providers in order, cheapest first, validates at each step and stops at the first valid email, so you pay only for the provider that succeeds (plus the misses before it).
- Deliverability: separate domains, 2 to 3 inboxes each, about 15 sends per inbox per day, 2 to 3 weeks warmup, placement tests, spintax against fingerprinting, short copy. Build due Fri 2026-11-20, 11:59 PM WAT.

## Key concepts taught

### Clay as a platform
- Clay is a "GTM data and orchestration platform": 150+ data providers behind one subscription (find the phone or email with one provider, fall through to the next) plus the ability to act on the data (route, enrich, send). (~5 min)
- Use cases listed: TAM building, finding the right people, signal-based outbound, personalized copy, lookalikes, inbound routing via webhook, scoring, CRM hygiene, research with Claygent, partnerships, recruiting, Google Maps local business lists, fundraising, market maps. (~8 min)
- FETC framework (the old FETE, updated): Find (own data: CRM, sheets, events, webhooks; Clay databases: companies, people, Google Maps, job postings; signals), Enrich (waterfalls across providers, AI research), Transform (normalize, formula, dedupe, score, route; mostly free), Create (sequences, DMs, assets, push to Smartlead, HubSpot, n8n). (~15 min)

### Table architecture
- Hierarchy: folder (one per workflow) > workbook (one workflow) > table (one entity, one row each) > column (one job each). A workbook holds several tables that talk to each other. Overview (bottom left) shows all tables; set a workbook description there. (~30 min)
- Where you start depends on the trigger: companies list = Find Companies; people trigger = Find People; hiring signal = Find Jobs; first-party data = CSV, CRM or webhook; local trades = Google Maps. (~35 min)
- Separate tables keep sources apart (webhook table, third-party table, partner table), and can later be consolidated into one master table. (~40 min)
- Save to: new table, existing table, audiences, or workflows. Audiences and canvas-style Workflows are the new Clay features covered the next day in Week 2B. (~65 min)

### Find People and Find Companies
- Searches and imports are free (the credits doc notes some sources charge Data Credits, so read the panel cost). The count is shown before import. Use it to size the market. (~60 min)
- Industry labels vary (LinkedIn-based): for fintech try financial services plus software development plus technology, then stack description keywords (fintech, payments, neobank). "SaaS" is too broad. Example search: about 16,000 companies on the loose filters, about 1.8K after keywords. (~58 to 72 min)
- Ask Claude for keyword lists to filter descriptions.

### Formulas and lookups (free)
- Formula column: describe the logic in plain English, type `/` to pick columns (shown in purple), Clay writes the JavaScript. Keep the plain-English description. Boolean formulas return true/false. (~55 min, ~165 min)
- Lookup (single row, other table): match on domain with "equals", never "contains" (flutterwave.com would match flutterwave-hq.com). "No record found" means not on the list. (~170 min)
- Column types: imports arrive as text; change domains to URL type (clickable). (~140 min)

### Credits: actions vs data credits
- Two meters. Data credits = the cost of the data or AI itself. Actions = one per row for the act of running an enrichment, AI run or push. Clay changed its pricing earlier this year (deck: March 2026, actions plus data credits); older tutorials say only "credits". (~105 min)
- Example in the room: verifying an email shows 0.1 data credits plus 1 action per row. Own API keys (for example Apollo, Prospeo) cost 0 data credits but still 1 action. (~106 min)
- Credits doc: cohort has 30,000 Data Credits, 50,000 Actions and Enterprise access. The PaidHR build used about 210.5 Data Credits for 94 people; enrichment was 70% of the bill. Optional workbook credit limit (Manage > Enable workbook credit limit, admins only).
- Teacher: Claude Code can conserve action credits by doing programmatic work; he promised a recorded video if time did not allow it. (~108 min)

### Claygents vs Use AI (from the written materials; not explained live)
- Use AI on data already in the row: about 0.2 credits per row on GPT-4.1 mini. Claygent browses the web and costs several times more, so it runs only where Use AI cannot tell (2 rows in PaidHR). Teacher described Claygent in the session only as Clay's research agent.

### Run conditions and auto-run
- Auto-run on means a new or changed column runs on every row immediately; it is the top cause of burned credits. Turn it off first on every table (toggle top left, next to the view tabs).
- Leave auto-run on only for always-on signal tables (hiring, new hire) where Clay re-checks on a schedule (Manage settings > on a schedule, daily or weekly) and you already know the cost per row. Static lists stay off. (~95 to 100 min, ~140 min)
- Run condition (Edit column > Add run condition > "only run when"): even with auto-run on, a column runs only on rows that meet it, for example `company domain is not empty` or `ICP Pass is checked`. "true" and "checked" are the same for a Boolean.

### Routing and Ready to Contact? gate (from the brief)
- Routing matrix becomes two formulas: Cell (which angle each row gets) and Ready to Contact? (true only when every check passes and the cell is one you send to; held cells stay false in the table). Not shown live.

### Email waterfall and email-domain check
- A waterfall tries providers in sequence until one returns a valid email, validating at each step; it stops at the first valid result. It does not run providers in parallel. (~212 to 214 min)
- Order providers cheapest first; switch off expensive ones (in the demo a 6-credit provider and a 1-credit provider were turned off, about 8 providers left, costs from 0.2 to 0.5 shown per provider). Connect your own key first if you have one. (~158 to 162 min)
- Run the waterfall only on rows that passed the ICP check (run condition), on one row, then 10, then the rest. The same pattern works for phone numbers (much more expensive).
- Email Matches Company? (email domain equals company domain) is a free check from the brief; in PaidHR it caught 6 emails at people's old employers. Not shown live.

### Views and groups
- A view is a saved filter. Duplicate the default view, rename it (for example "ICP fits", or an exclusion example view), filter on a Boolean column. Keep the default view unfiltered. (~172 min, ~200 min)
- Groups (right-click selected columns > Group), column descriptions and views Ready to send, Held and Dropped are required by the brief (Part 11); not shown live.

### Deliverability infrastructure
- Never cold-send from the primary domain. Use secondary domains (a "try" or "get" prefix, or a different TLD), 2 to 3 inboxes per domain, about 10 to 15 cold sends per inbox per day (deck: 15), so 3 inboxes on one domain is about 45 per day. Optionally forward the secondary domains to the primary site. (~88 to 95 min)
- Warmup 2 to 3 weeks (deck: at least 2, ideally 3 to 4) in a pool of inboxes that exchange and reply to mail. Inbox providers named: ZapMail, Icemail, Scaledmail (all inferred spellings), with Google inboxes quoted at about 10 for $9 per month and Microsoft inboxes also available. Diversify across providers so one failing does not stop sending.
- Placement tests with real campaign copy (EmailGuard, MailReach, or the sequencer's native test): 7 or 8 of 8 is good, under 4 of 8 is fix (deck).
- Sequencers named: Instantly, Smartlead, PlusVibe (teacher's favorite). Full detail in the Sending Infrastructure and Deliverability Playbook (Week 2 tab).

### Sequencer connection
- Clay has its own Sequencer (pull rows in, build a sequence from scratch, connect mailboxes). External sequencers connect through native integrations (Smartlead "add leads to campaign" shown; Close and others also supported). (~207 min)
- Customer-communication tools are not built for cold outbound; do not use them for it (tool name garbled, possibly Customer.io (inferred)).

## The live build (PaidHR, workflow "new HR leaders, last 6 months")

1. Setup (~28 to 32 min on Clay UI; ~116 to 126 min on the Claude side). Open Claude Code, pull the new skill: "pull and save the new skill that we currently don't have" from the GTM Starter Kit repo (`clay-build-plan`). Ask Claude to pull up the workflow spec (saved under `output/campaigns/...`).
2. Generate the plan (~125 min). Invoke `/clay-build-plan` on the spec. It produced a part-by-part guide plus a swimlane diagram showing four tables: Exclusions, the people table (new HR leaders), Companies, and an HR team table used to test "first HR hire". It also lists optional own API keys (for example Apollo) so you do not spend Clay credits.
3. Folder and workbook (~126 min). Folder "WF1 new HR leaders", workbook named for PaidHR with a version suffix (v1, later 1.1 and so on).
4. Exclusions table. Claude generated an exclusions CSV (customers, competitors, partners, investors; for a real employer use a CRM lookup instead). Imported via CSV, domain column changed to URL type, table renamed to an exclusion block list. Pipeline customers and active deals belong here.
5. People search (Find People, free; ~143 to 155 min). Filters: job titles include HR leadership titles (Head of HR, HR Director, People Operations, Chief People Officer and similar; one title-contains filter was set to "doesn't contain" assistant and intern after a student caught the mistake); country in Nigeria, Kenya, South Africa, Ghana (use the person country filter; the experience-country field wrongly pulled Tunisia and India); company size 10 to 1,000; company industry "is not" government administration, non-profit, public sector, education (and human resources); work-experience start date in or after "6 months ago" (relative months only, and pick the work experience, not education). Spot-check a row ("joined four months ago"). Save to new table.
6. Add hidden fields (~155 min). Use Add as column from the matched experience to bring in company domain and start date; company domain becomes the key for all later lookups.
7. Free checks (~160 to 165 min). Boolean formula "true if title contains assistant or intern, otherwise false"; a months-in-role formula (described, not fully shown). All free, zero credits so far.
8. Exclusion lookup (~167 to 172 min). Add Column > Lookup, single row, other table: Exclusions table, target column domain equals {{company domain}}. Ran 10 rows, then the rest; result "no record found" for all. Added run condition `company domain is not empty`.
9. Views (~172 to 175 min). Duplicated the default view to demo filtering out one company; default view left unfiltered.
10. Companies table (~178 to 185 min). Created a blank table "Companies" with Company Domain (URL type) and Company Name; table setting to dedupe on company domain. In the people table, Add Column > Send Table Data to Companies, mapped to existing columns, auto-extract off, tested on one row, deleted the stray auto-added column, then ran all. Reason: two people at one company must not trigger two paid enrichments.
11. Enrich Company (first paid step, ~188 to 192 min). Input: company domain; auto-run off; pulled size, country, industry, description as columns. Cost remarks in the transcript are garbled ("4.5 ... 11 credits"); credits doc gives 82 Data Credits for 83 companies.
12. ICP Pass formula (~192 min). Formula: output true if employees between 10 and 1,000 and country in NG, KE (Ghana, South Africa also mentioned); column renamed ICP Pass; a view "ICP fits" filters on checked. Teacher confirmed the criteria come from the workflow spec's ICP, not invented live.
13. Lookup back (~194 min). In the people table, lookup the Companies table on domain to bring in ICP Pass (free). Teacher noted lookups do not use the selected view, so qualify again with the Boolean.
14. Email waterfall (~196 to 206 min). Add Column > Find work email (waterfall); reordered providers cheapest first; turned off the expensive ones; validation on; auto-run off; run condition `ICP Pass is checked`. One row first, then the first 10. One row found its email at the fourth provider; rows failing the condition did not run.
15. Sequencer (~207 min). Overview only: Clay Sequencer or Smartlead integration. The build was not taken further live.
16. Recommended reading: the build-along doc (with screenshots) holds the remaining parts: Use AI Workforce column, Claygent fallback on 2 rows, satellite HR-team count, Cell, Ready to Contact?, Email Matches Company?, Send Ready?, email lines as formulas, groups, views, sequencer.

Real numbers (from credits doc, not said live): 96 people imported, 66 worth enriching after free checks, 83 companies enriched (82 Data Credits), 66 people enriched (66), Workforce AI about 15, Still Employed AI about 13 (said YES on 61 of 63; cut as low value), waterfall 47 people in, 26 emails out, 31.5 credits, 6 emails at the wrong company, 20 send-ready, total 210.5 Data Credits, about 10.5 per send-ready person; 17 Kenya and Ghana rows held.

## Rules and tips the teacher stressed

- Build from first principles by hand first, then let Claude Code or the API do it; clicking the tables gives the mental model so you can catch what Claude gets wrong. (~150 min)
- Turn auto-run off before adding any column; burning the company's credits is "the worst feeling". Only leave it on for always-on signal workflows, after proving the cost per row. (~95 min)
- Always test one row, check the cell, then run at scale; check filters live for false positives (the Tunisia and "contains assistants" slips). (~148 to 155 min)
- Free first: formulas, lookups and Send table data cost nothing; do all qualification there before any enrichment. (~160 min)
- Match on domain with "equals", never company name and never "contains". (~170 min)
- Run conditions on every paid column; the waterfall's "stop at first valid" only saves money if the cheapest provider is first. (~200 to 214 min)
- Use equal-to for domain lookups so you get an exact match; qualify twice, since a lookup can still pull rows you did not intend. (~194 min)
- Name workbooks per workflow and keep versions (v1, 1.1). Folder per workflow. "Always be testing": ship more workflows to find what performs. (~32 min)
- Plan with spec as architect and build as engineer: hand the spec, guide and build plan to a junior engineer, same as software teams. (~123 min)
- Copy: opener, bridge (routes on a condition), value prop (routes on size or a fact), social proof (can move to the PS), soft CTA with a lead magnet. Under 100 words; for Microsoft recipients under 60 words; shorter is landing better. (~87 to 92 min)
- Spintax gives about 15 variants of the same sentence so a template sent to 1,000 people is not fingerprinted. (~92 min)
- Run pre-send checks: email valid, deduped, ICP aligned, no empty or broken first-name variables (avoid "Hi {first name}" going out blank). (~108 min)
- Common mistakes called out: wrong country field (experience vs person), contains instead of does-not-contain on exclusion titles, leaving auto-run on, forgetting the run condition (the waterfall ran, or would run, on non-ICP rows), pasting keys, fetching 'SaaS' as an industry keyword.
- Judge by replies: 1 to 3% reply rate is healthy; over 3% means copy, infrastructure and signal quality are all good. The transcript's "50%" figures for positive replies and bounces are garbled; the deck says bounces over 3% means pause and under 2% is healthy.
- Salary data is private and not available in Clay; public salary ranges (UK job posts, some companies) can be researched.
- For new companies with no public footprint, context comes from your own research and competitors; outbound itself tests message-market fit. (~128 min)
- Clay works for B2C only where the people are findable on LinkedIn; think "job to be done". (~135 min)
- Clay Playbooks (use case templates, lower left) can be reverse engineered. (~214 min)

## The assignment

Stated in the session (quotes are the transcript's wording, garbled in places):

> Just pull that skill file.
> So yeah, this is something I expect everybody to do.
> Try to submit and update your build log.
> So, try to submit your context to us.
> The build along with you guys are going to be getting is going to contain much more detailed steps.

Stated in the written brief (accurate):
- Build a Clay workbook for your own Week 1 workflow spec: free search list, free checks, company checks once per company, your signal plus one AI column (JSON, allowed answers, evidence field), Cell and Ready to Contact? gate, verified emails, at least 20 enriched rows, readable table (descriptions, groups, views).
- Steps 1 and 2 in Claude Code (spec check, `/clay-build-plan` with test size 25 rows), steps 3 to 10 in Clay; stretch steps 11 to 14 (email lines as formulas, Claygent fallback, satellite table, draft sequencer campaign not launched).
- Submit: share link (or screenshots) in the Build Log Week 2 row, link to the build plan, one funnel line (rows imported, passed, ready, emails found, credits spent). No lead data in the repo.
- Due Friday 2026-11-20, 11:59 PM WAT. The Week 2B build with Sandra goes in the same Build Log by the same time. Plan 4 to 5 hours over two sittings.

What faculty look for: a table that follows the spec column by column; free checks before paid with run conditions everywhere; an AI column with tight prompt, allowed answers and evidence; a gate that holds back rows that should not be emailed; readable columns (descriptions, groups, views); honest numbers (counts, fill rates, cost per row and per send-ready contact). Not: enrichments with no decisions, a paid column run on every row, "write something about this company", every row with an email treated as ready.

## New information not in the written brief

- Word limits for copy: under 100 words, and under 60 words for Microsoft recipients (Google recipients can run a bit longer); about 15 spintax variants to avoid fingerprinting.
- Provider and inbox specifics: ZapMail, Icemail, Scaledmail named (spellings inferred), Google inboxes about 10 for $9 per month, diversify across two providers, forward secondary domains to the primary.
- Placement-test tools named: EmailGuard, MailReach, sequencer-native tests; PlusVibe is the teacher's favorite sequencer.
- Clay UI traps: accounts created before the new UI may only see the old homepage; some cohort accounts could not see Action credits (moderator escalating to Clay; Clay flags multi-account sign-ups); Find People "Experience country" differs from "Country"; start-date filter takes relative months only; lookups do not respect the selected view.
- Waterfall behavior: sequential, validates at each step, stops at first valid, so cost is per provider tried not per provider listed; one row in the demo needed four providers.
- Save-to options after a search (companies/audiences, new table, existing table, workflows) and the idea that webhook, third-party and partner data live in separate tables then consolidate.
- Teacher plans: this was his last session; next week he reviews Week 1 submissions with detailed feedback; Claude Code can cut action-credit use and he may record a video; he will post a longer build-along with screenshots.
- Logistics: Week 2B on Sunday (the moderator said 4 pm in the recording, the deck says 3:00 PM WAT; check the invite); Week 3 on Sat 2026-11-21 is CRM and pipeline design in HubSpot (from the deck); demo day will present the full build logs.
- Auto-run on a schedule (daily or weekly) is the way a signal table keeps finding new HR hires; the same repo-watching idea (a local script pulling new skills from the starter kit) was confirmed possible, runs only while the computer is on.
- Optional: connect Apollo or Prospeo with your own key to avoid Data Credits.

## Action items for Neil

- [ ] Deadline check: the build was due Fri 2026-11-20 11:59 PM WAT and today is 2026-11-21. Confirm with faculty whether late is accepted, then submit in the Build Log Week 2 row.
- [ ] Confirm Clay account via the Treford link, credits showing (30,000 Data Credits, 50,000 Actions); if the Actions meter is missing, escalate in the community or WhatsApp.
- [ ] Re-pull `clay-build-plan` from github.com/bolaji-ships/gtm-starter-kit (the repo skill folder already lists it; verify it is the current version), add to CLAUDE.md, log in this week's work log, start a new session.
- [ ] Create `weekly-priorities` and `work-log` files for ISO week 2026-W47 listing the brief's steps.
- [ ] Check the Rave workflow spec has Status STRUCTURE-APPROVED and a numeric ICP filter; decide people-first vs account-first. Rave's trigger is about local businesses found on Google Maps, so account-first is likely, with a Clay Google Maps source or the existing Localpipe list imported by CSV (inferred; Neil to decide).
- [ ] Run steps 1 to 10 of the brief; record Actions and Data Credits before and after each paid step; cost per row and per send-ready contact.
- [ ] Work in this order: workbook plus exclusions, free search (log the count), free checks, Companies table (domain dedupe), Enrich Company, ICP Pass, signal plus one AI column proven on 2 to 3 rows, Cell and Ready to Contact?, email waterfall (cheapest first, strict validation) with Email Matches Company?, 20+ rows, descriptions, groups, three views.
- [ ] Auto-run off on every table; run condition on every paid column.
- [ ] Do the Week 2B Audiences and Workflows build with Sandra, same deadline.
- [ ] Write the cost per step and counts in the repo (no lead data, no CSVs, no names or emails); run `secret_gate.sh` before push.
- [ ] Read the Sending Infrastructure and Deliverability Playbook and Campaign Benchmarks docs; check Rave's sending set-up against the 8-point check before any sequencer step.
- [ ] Fill the feedback form; ask in the community channel if blocked.
- [ ] Update `BUILD-LOG.md` and the Rave client brain notes as per session rules.
