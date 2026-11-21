# Audiences and Workflows in Clay (GTM Engineering course, Week 2B)

- Date: 2026-11-15 (Sunday)
- Title: Audiences and Workflows in Clay (Week 2B, Treford GTM Engineering Bootcamp)
- Teacher: Sandra Uche (Founder of Auto8B2B / "Automate B2B", Clay Club Lagos lead, Clay cohort coach). Bolaji Anifowose (Week 1 lead) filled in for roughly 10 minutes while her internet failed.
- Attendees: cohort (names not listed)
- Recording length: 196 minutes (plain-text whisper transcript, no timestamps)
- Source: whisper auto-transcript with many recognition errors, cross-checked against Sandra's slides with speaker notes (deck2b), her PDF "Clay Audience, Workflow & CLI Resource" (res2b), and Clay's agent-plugin docs (wf-audiences.md, routines.md). Normalized: "Clay/play/cle" = Clay, "Cloud Code" = Claude Code, "Codecs" = Codex, "C framework" = SEA, "Fiti/PT/Fetch" = FETE/FETC, "Sculptor" = Clay's in-app AI assistant (inferred, named Sculptor in the UI), "Palaji" = Bolaji, "Rex" = a third-party Clay CLI toolkit.
- Caveats: about 400 lines of the transcript are one looping phrase ("switch my internet") and `[BLANK_AUDIO]`, so some live steps were not captured. The planned breakouts, the break and the reflection block did not happen on the recording. The assignment was never read out in the recording (see section 7).

## TL;DR

- Tables are for testing a play on a small list (50,000 row cap). Audiences are the production layer: a workspace-wide data universe (People, Companies) that holds millions of records, with segments as filtered slices and Workflows as the repeatable process attached to a segment.
- Frameworks: FETE/FETC is the process, Jigsaw is the data strategy (corner pieces = identifiers first), SEA (Segment, Enrich, Act) applies it to Audiences. She told the room not to overthink which framework: define the job to be done first.
- Live build for PaidHR: natural-language people search ("HR leaders, new in role in last 3 months"), saved to an audience through a workflow that has a Write to Audiences step, a 10-person segment, an enrich-person workflow with field mapping, then a work-email waterfall. The email step failed because company domain (a corner piece) was missing. Codex (via Rex) and then Claude Code inspected and repaired the workflow; the Claude Code V2 (domain-not-empty condition, test on 3 records, publish) ran 11 of 14 records for 3.2 credits and returned about 2 emails.
- Clay CLI path: paste "Set up the Clay plugin by following the steps in https://github.com/clay-run/agent-plugins" into Claude Code or Codex, `clay login`, then ask the agent to inspect, fix and add workflow steps. She found Claude Code more direct than Codex. MCP in Claude/ChatGPT is a separate connection and was only described, not demoed.
- Advice repeated by Sandra and a facilitator: build by hand first so you can judge the agent's output; test on 5 to 10 rows; audiences are live so mistakes cost credits.

## Key concepts

### Tables vs Audiences vs Workflows
- Table: a workspace for one list or process; best for testing enrichment, formulas and qualification logic, with full row/column visibility. Her claim: tables are "static" with a 50,000 row cap; once full you cannot add matching records (the deck itself hedges this, see section 8).
- Audience: "unified GTM data layer" or "data universe" of the whole workspace, all users' data combined. Two types: People (contacts) and Companies (accounts). Holds millions of records. Records arrive from imports, integrations, searches, webhooks, Clay tables or CSV (section 4).
- Segment: a filtered slice of an audience. Records are not copied; one record can sit in several segments. Further filters narrow the slice. Example given: 41,000 people, filter job title contains CEO, rename the segment "CEOs", add country filters, save.
- Workflow: trigger starts it, each step takes inputs and gives outputs, a decision routes the record (back to the audience, to a campaign, to the CRM). Her pitch: test the process on 20 companies in a table, then attach it to a segment so new qualifying records run through the same process (for example next month's HR-leader campaign without duplicating a table template).
- "Dynamic": once an audience is live, new records that match the segment criteria get added and run through the workflow automatically. Auto-dedupes. She called audiences risky for the same reason: they are live, so mistakes spend credits.
- Data hub (audience-level pages): coverage counts per field (first name, job title, email, domain, country), sources, exports, reporting, number of tables, workflows and signals attached, credits spent. Pitched as governance for enterprise teams and managers.
- Segments page columns include an "Orchestration" column (= the workflow attached, per Sandra) and actions to add a signal or export (to a workflow, ad platform, or email sequence).

### SEA, FETE/FETC, Jigsaw
- FETE = Find, Enrich, Transform, Export. FETC replaces Export with Create (AI produces copy, a brief). From Bolaji's Week 2A.
- Jigsaw (data strategy): find corner pieces first, enrich the edges, fill the puzzle. Accounts: domain, company name, company LinkedIn. Contacts: LinkedIn profile, or full name plus company. "Garbage in, garbage out": AI invents data without the right inputs. Enrich edges = basic attributes (exact employee count instead of a range, tenure in role). Fill the puzzle = waterfalls (100+ email providers for coverage, her example: Apollo finds 600 of 1,000, the next provider fills gaps), Claygent or other AI/scrapers. If a build breaks, ask "which corner piece is missing".
- SEA: Segment your audience, Enrich your audience, Act on it (send to campaign or CRM). Reason: you will not enrich or email a million records at once.

### Signals and custom signals
- Covered briefly; the audience data hub and segments can carry signals ("add signal" on a segment). The detail (signal treasure hunt, custom signals, company and people signal lists) is in res2b pages 4 and 5 and was pointed to, not taught live. She said the resource explains custom signals for people and companies.

### Workflows
- Trigger: what starts the workflow. In the demo the trigger node was the segment ("segment added to the workflow is the trigger"). Other triggers named: a webhook URL (form submit), adding a person to a segment.
- Enrichment steps: Enrich Person, Find Work Email (waterfall of "over 22 providers" shown), phone, AI/Claygent, API store or custom enrichment. Run options: whole list or each item one at a time (use one at a time for large lists).
- Branching and conditions: run conditions (run email step only if domain not empty; run phone step only if email empty). Conditional formula nodes exist.
- Runs and versions: "Save and test on 10 rows" vs "save without running"; then "Publish and run". Workflows have version control (V1, V2). Draft (unpublished) vs published was shown via the V2 publish.
- Write-back: enrichment results must be mapped back into audience fields (Write to Audiences).

### Clay Agent Plugin + CLI vs MCP
- CLI (in Claude Code or Codex): you describe the build, the agent works through Clay's command-line interface, reads the plugin's skills, then queries and edits workflows. She judged it the easiest way to build and QA at scale ("1,000 workflows, you cannot QA by hand").
- MCP (in Claude or ChatGPT chat): connect Clay as a connector; she said it is mostly used by sales reps. Described, not demoed.
- Rex: an independent CLI/toolkit "somebody created" that is cloned as a repo; included in the course's GTM starter kit. Codex and Claude Code used it automatically.
- Sculptor (in-app assistant): good for beginners to chat a search into existence; still needs QA, and she believes it has less depth than the CLI (she had not tried it for QA).
- AI Context (admin only): enter the company domain and Clay scrapes it to fill what the company does, ICP and personas. Clay cannot read your Claude Code Context OS, so Clay-side AI uses this field. A facilitator added that GitHub context travels across tools, Clay's stays in Clay.

## The live build, in order

1. Orientation in the UI. Left nav: Home > Audiences > People or Companies; also segments, data hub. Her personal workspace showed 41,000 people and 21,000 company records (all created via Clay's free company search) with sources, exports, segments and drafts. The course workspace was new and empty (0 people, 0 segments).
2. Audience sources shown (how data can get in): imports from Salesforce, Snowflake, HubSpot, Google (BigQuery, inferred), Databricks, Gong; Clay searches ("find people", "find companies" save options); importing a Clay table into an audience; CSV upload; webhooks. The sources page lists each source and its last sync status.
3. Segment from existing records (demo A, personal workspace): New segment > attributes where job title contains "CEO" > rename "CEOs" > optionally add country or enriched-field filters > save. She said you can then enrich the segment and find emails.
4. Records entering the course audience (demo B, PaidHR). Path used: Find leads (left nav) > People > chat with Sculptor in natural language (request: HR leaders, roughly "similar to HR directors", start date on or after 3 months ago). Sculptor translates to filters (job title similar to HR director; started on or after 3 months ago), she checked them and clicked Continue.
5. The save screen offered: save to audience (up to 5 million people results), send to table (50k rows), start a new workflow (up to 5 million results into a workflow), add enrichment. She saved 15 found records to the audience.
6. What happened next (this is the answer on ingestion): in the new UI, choosing to save a search to an audience created a workflow first, with a Write to Audiences ("send to audiences") node. She did not expect this ("why am I in workflows?") and called it a weird flow. The first attempt failed (the Write to Audiences node needed field selections/mapping). Sculptor diagnosed it; she set the rule so new data always overrides, ran "Save and test on 10 rows", then Publish. So records went in by: search, then a workflow that writes them with an upsert-style write step, not by a plain import. This matches the docs' "ingest shape" (section 8).
7. She suspected admin rights blocked "add people to audience" and was ready to switch workspaces. A new people segment then appeared containing 10 people (15 found, 10 in the segment; she did not explain the gap). Segment renamed.
8. Data check: the 10 records had job title but no first/last name, email or LinkedIn for some. Gap-filling started via Enrich on the segment, which opens a workflow view (trigger = the segment).
9. Enrich Person step added; run option: whole list (only 10 people). Save and test on 10 rows; reviewed test data; Next.
10. Field mapping (Write to Audiences): audience fields are not auto-created. She deleted unwanted mappings (logo, region, education, etc.) to keep the audience light, and created new audience fields as needed with a type each: company name (text), company domain (text), job title (text), current experience, person LinkedIn (URL), start date (date), Clay company ID. Only a few default fields exist (email, phone, seniority, department, email 1 to 4 in her words). She said you do this once per audience, not every time. Rationale: you control what gets written; 25 auto columns would bloat the audience.
11. Publish and run. The run showed cost "one action per person and 0.5 credits per row"; 10 of 10 completed, 0 failed. The segment view then showed first/last name, city, state, country, LinkedIn, current experience, company name/domain, job title, start date. Some LinkedIn URLs were missing.
12. Second enrichment, Find Work Email, added in the same workflow after the write-back (she explained you click plus and add another enrichment; example: phone step only when email is empty). It auto-mapped first name, last name, domain and social profile. She added a run condition on LinkedIn, then ran a test: no email found. Cause she named: no company domain, a required corner piece (Jigsaw). She noted that fixing it meant fixing company domain first.
13. Run stats she read on the sources/runs view: 36 progressed, 20 failed, "50.6 credits" (figure is garbled, see section 5). The work-email segment appeared as a second live segment, and she was unsure why it showed manual.
14. Switch to the CLI (break skipped). Screen share of VS Code. Codex was set up with the plugin prompt (below). It reported the plugin already installed, CLI on path, auth and workspace verified, but not connected to the Treford workspace; she ran the login in the browser and authorized it. She had about six workspaces; the CLI needs the right one active.
15. Prompt to Codex (paraphrased from the recording): find the people workflow named "HR new leaders"; for the senior HR leaders enrich-person workflow the email enrichment did not work, explain what is wrong and what to do. Codex (via Rex) found two issues: 20 records failed the audience write because a required field-selection array was missing, and after that was corrected a one-record test returned only name/country fields while the lookup/email step never ran; it also reported duplicate workflows. She asked it to add the work-email step and run all 10. Run counts it reported (4 complete, 16 processing, then 20 complete or 20 failed) did not match 10 records and she could not reconcile them.
16. Same task on Claude Code (auto mode on, plugin installed via the same prompt; it reused credentials from Codex). Prompt: query the "senior HR enrich person" workflow, then "add an enrichment to find the work email for these 10 people and add a conditional logic where it runs only if domain is not empty". Claude Code read its skills, found the workflow, listed its structure and run history, built the enrichment (trigger gives LinkedIn URL and location; the domain is a trigger output; condition: company domain present; work email from full name + company name + company domain; write back to the audience segment), removed a duplicate, validated, and showed cost (about 0.8 credit, one action execution per record).
17. Test before publish: she told it to test first. It ran 3 records; the email attempt started as a draft test run, steps passed ("domain found, condition pass, work email, write to audience"); one verified test. Then Publish: version 2 live.
18. Verification in the Clay UI: Workflows list shows V2 published; Runs: 11 done, 3 failed (the transcript says "the one that failed"), cost 3.2 credits; table view of the segment showed emails for about two people (she searched one person by name and found an email).
19. Not built: MCP in Claude/ChatGPT demo, breakout rooms, peer building, reflections. She described the MCP connect path and promised the resource PDF after class.

Other live prompts and UI paths mentioned:
- Clay plugin setup: workspace > "AI and CLI" > copy the API and CLI command and give it to Claude Code or Codex; or paste the repo prompt (see section 6).
- Segment filter: "attributes > where job title contains".
- Windows: the CLI did not run natively for two learners; Claude Code suggested a Linux layer (WSL, inferred). Sandra said it is a Mac vs Windows technical matter and to ask the agent how to set it up.

## Sizing a TAM, limits and costs

- No dedicated TAM-sizing exercise was done. Counting methods shown: segment record counts in the segments list; data hub coverage per field (how many have domain, job title, email, country); filters on attributes (title contains, country, start date). Bolaji's example: import 200,000 travel agents (an example named in the recording, inferred) into an audience, then slice to about 2,000, and build a workflow on that slice.
- Limits stated: table cap 50,000 rows; saving a search to an audience, or into a workflow, up to 5 million results; her claim of audiences holding "millions". Table row import at 100,000 TAM needs multiple tables (the old way).
- Costs stated: enrich-person run "one action per person, 0.5 credits per row" (10 people). A learner asked whether each mapped field costs credits; she said no, mapping fields costs nothing and the enrichment is "one credit" (loosely stated; the 0.5 figure on screen contradicts it). Claude Code estimated about 0.8 credit and one action execution per record for the work-email step. V2 run: 3.2 credits for 11 done. Runs view: 36 progressed, 20 failed, "50.6 credits" (garbled, may be 5.06 or 50.6). Cost preview: the workflow shows estimated cost before running; she said she would show where, and the CLI printed costs.
- Always test on 5 to 10 rows before deploying on the audience; do not enrich a million records; review cost and only enrich what you need.

## Rules and tips she stressed

- Think "job to be done" and outline the steps first; the frameworks are fundamentals, do not agonize over which one (facilitator and Sandra).
- Garbage in, garbage out: check corner pieces (domain, LinkedIn) before an enrichment. Missing domain made the whole email waterfall fail.
- Test before production: use tables to prove the play, audiences to run it. Test on a small sample, read the result, then publish.
- Do not write back fields you do not need; keep audiences lean. Create each field with the right type (text, URL, date).
- Do not trust "done"; open the workflow and the segment and check the data (she checked the runs, cost, and table view after Claude Code reported success).
- Use conditional run rules to avoid wasted spend (email only if domain exists; phone only if email empty).
- Clay changes its UI constantly; understand the data flow, not the buttons.
- Package anything that works into a skill (facilitator).
- Common mistakes seen: expecting audience save to be a plain import (it routed via a workflow); missing required field selection on the audience write; running the work-email step without a domain; duplicate workflows created by the agent; confusing run counts; Windows without a Linux layer; workspaces not upgraded to see Audiences.
- Use the Clay CLI only after you know the manual build; a facilitator stated this directly (beginners build by hand first, then scale with the CLI, otherwise you cannot spot AI slop).

## The assignment

- Not stated in the recording. The recording only mentions breakouts and "move forward in your assignments", and the closing tells learners to drop a message if their workspace is not upgraded. Sandra said she would share the resource after the call and asked for feedback.
- From her written materials (not from the recording). Goal and inputs, res2b page 10, verbatim:

> Build one Audience segment connected to a Workflow that enriches and routes records. Bring your Week 1 ICP and workflow context, your Week 2A Clay build, and access to the relevant workspace features.

- Build steps (res2b): 1 write the audience criteria in one sentence and explain exclusions; 2 create the segment and inspect a small sample; 3 choose one enrichment that affects qualification or the next action, preserve the record identifier; 4 connect a workflow with an explicit rule and visible destinations for ready records and records needing research; 5 review the estimate, test a small authorized sample, inspect the data and routing, save evidence and links.
- Deadline (res2b and deck): Friday, November 20, 2026 at 11:59 PM WAT. Today's date is after this, so check with faculty before submitting.
- Submission format (deck/res2b): a Build Log with the audience and workflow links, a short explanation of criteria, enrichment and routing rule, and a test result or screenshots. CLI use is optional. No Loom or share-link instruction is in the materials or the recording.
- Review: the deck notes say Sandra reviews Week 2B builds after the deadline. If blocked, save the draft and record the exact blocker for faculty; this does not replace the build requirement.
- Time estimate: about 45 to 60 minutes.

## New information not in the written materials

- Tables 50,000 row cap vs audiences millions; saving a search to an audience allows up to 5 million results; "audiences launched earlier this year" and Bolaji's account of why they exist (tables crash at 200,000 records). The deck only says "workspace data".
- In the live UI, saving a people search to an audience went through a workflow with a Write to Audiences node and failed on first try (missing field selection). Not in the slides or PDF; consistent with wf-audiences.md.
- Audience fields are not auto-created on write; defaults are only email, phone, seniority, department and numbered emails (her statement). wf-audiences.md also says to create fields in the CLI.
- She believed admin rights are needed to add people to an audience and that AI Context is visible only to admins; unverified.
- Data hub, sources, exports, reporting pages and the list of import sources (Salesforce, Snowflake, HubSpot, Google, Databricks, Gong).
- Per-run costs seen: 0.5 credits per row (enrich person), about 0.8 credit (work email), 3.2 credits for the V2 run; run outcomes (11 of 14 and about 2 emails).
- Observed that one enrichment needed an extra workflow (she said so at one point, then showed adding another step in the same workflow); her statement is contradictory and unverified.
- Claims that audiences "automatically add net new matching records and run workflows" and that tables cannot take new records even if they match. The deck explicitly avoids both claims; wf-audiences.md says ongoing automation needs a chosen trigger (segment membership, signal, schedule), and an `audience_segment` trigger can backfill members.
- Codex vs Claude Code comparison (her opinion: Claude Code more direct), Claude Code reusing Codex credentials, Rex used automatically.
- Windows needs a Linux layer for the CLI; Audiences needs an upgraded workspace.
- Her stated purpose of Audiences for enterprise governance and that Clay is becoming more agentic.
- In wf-audiences.md but not said in class: the dedicated routine path for bulk ingest (`upsert-audiences-record` workflow with a manual trigger, `clay routines create workflow <id>`, run via `clay routines runs start workflow:<id>`; 1 to 100 items inline, JSONL for larger batches), `audience_segment` trigger with `clay workflows runs test <workflowId> --audience-segment <segmentId> --limit N`, and the backfill shape (save audience with an Empty filter, trigger on it, enrich, upsert back by email, linkedin_url or domain). Lookup keys: contacts id/email/linkedin_url/phone/external_source_id; accounts id/domain/linkedin_url/clay_company_id/external_source_id.

## Action items for Neil

- [ ] Confirm our Clay workspace is upgraded and shows Audiences (People, Companies, Segments, Data hub); if not, ask the Treford group (she said unupgraded workspaces cannot use these features).
- [ ] Decide the Week 2B deliverable and whether a late submission after Nov 20 is accepted; ask faculty (the Build Log link, criteria, enrichment, routing rule, test evidence).
- [ ] Build the segment-plus-workflow once by hand in the UI first (her advice), then repeat with the plugin.
- [ ] Install the Clay plugin with the repo prompt, run `clay --version`, `clay login`, `clay whoami`, confirm the right workspace is active.
- [ ] Test the ingest path directly: search, then a workflow with `upsert-audiences-record`, see whether it matches what the UI created; check field creation with `clay audiences fields list` and `create`.
- [ ] Before any enrichment, check corner pieces (domain or LinkedIn) are present; add run conditions; test on 3 to 10 rows and read the cost estimate.
- [ ] Verify her claims against docs: dynamic add of net-new records and trigger choice, the table 50k cap, per-run credit figures.
- [ ] Skim res2b signal pages and Clay University "How Audiences Works"; decide which custom signal to monitor.
- [ ] Skip or confirm later: MCP in Claude/ChatGPT setup (not demoed), Windows setup (not needed on Mac).
