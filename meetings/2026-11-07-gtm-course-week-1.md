# GTM Systems Thinking and Context Engineering (GTM Engineering course, Week 1)

- Date: 2026-11-07
- Title: GTM Systems Thinking and Context Engineering
- Teacher: Bolaji Anifowose (lead facilitator; a moderator and other facilitators also spoke)
- Attendees: cohort (names not listed)
- Recording length: 290 minutes (auto-transcript, last timestamp about 4:49:48; the session ran past its scheduled time, per the moderator)
- Source: auto-transcript with recognition errors. Terms normalized here: "cloud code" = Claude Code, "Treg/tregg/trek.co" = treg.to, "PlusVibe" = PlusVibe sequencer, "Payday Child/PageHR/PDHR" = PaidHR (the case-study company).
- Course shape stated in session: 5 weeks. Week 1 Claude + Claude Code + GitHub. Week 2 Clay + PlusVibe (or any sequencer) + Claude. Week 3 post-acquisition (cross-sell, upsell, retention) with Clay + Claude. Week 4 automations and workflow agents. Week 5 everyone presents what they built end to end.

## TL;DR

- A GTM system is designed tool-agnostic and end to end first (inputs, engine, CRM memory, feedback loop); tools change every quarter, the system compounds.
- Claude Code is a harness around a model (files, terminal, permissions, loops, subagents). Its context window is finite, so you manage it with CLAUDE.md, skills, subagents, compacting, and a work log.
- Connect tools in this order of preference for bulk work: API or CLI over MCP, because MCP loads all tool definitions into context ("context bloat"). Keep secrets in .env, gitignored, never pasted into chat.
- The Context OS is a folder (context/, knowledge-base/, meetings/, output/, tools/, weekly-priorities/, work-log/, plus CLAUDE.md) pushed to GitHub so a team can clone, branch, PR, and roll back.
- Live build for PaidHR: scaffold, connect treg.to via CLI (project scope), 4 parallel research subagents, synthesize ICP/positioning/messaging, pull the gtm-starter-kit, signal-matrix, workflow spec, campaign ideas, angle matrix, campaign copy with QA. Assignment: build a Context OS for one B2B company of your choice, push to GitHub, submit a build log and form, "max by Friday".

## Key concepts taught

### GTM systems thinking
- GTM = how a product gets into a customer's hands: what you say, which channels, where you find buyers. Marketing, sales, and customer success all contribute.
- Motions named: sales-led, PLG (product-led growth); lead sources include outbound, inbound, community-led, partnership-led. B2C (example given: PiggyVest) and B2B (example given: a B2B product, name garbled as "Oksports") need different motions.
- A GTM system, as drawn: inputs, an engine that automates parts of the motion, a CRM as memory, and analytics feeding back to improve the process. Illustrated with a fictional outbound system for Reliance HMO: define ICP and signals, find companies, enrich, ICP-fit score (drop non-fits), check staff size and current-HMO indicators to switch the angle, find decision makers, enrich and verify contacts, dedupe against the CRM (name garbled as "upspot/outspots"; HubSpot (inferred)), personalize on signals, send via PlusVibe, tag replies by automation, create deal alerts and a pipeline.
- "Blow out the tool" first: design the system before touching any tool.
- Four pillars: clean data foundation; signals; composable workflows (car analogy: swap the tire or engine and it still runs); feedback loops (ICP is a moving target).
- Be the driver: own the thinking, review each output, do not outsource judgment to the model.

### ICP and signals
- ICP = ideal customer profile: companies that get the most value, buy fastest, and stay longest. Go beyond job titles. Filters prioritize accounts (qualifiers first, the rest lower in a waterfall).
- ICP doc contents: industry, size, location (demographics), plus technographics (example sites named for tech-stack lookup, spelled in the transcript "Wapalizer" and "BuildSuite" (inferred: Wappalyzer and BuiltWith)), signals, and engagement readiness (events attended, LinkedIn engagement).
- ICP comes from CRM data (who closed, who stayed, who churned) or, for early startups, from market research and beta customers. It evolves; test other segments over time.
- Buyer personas: who owns the budget, influencer, champion. Persona changes with company size (founder at about 20 people; HR/people function as companies grow; finance as final sign-off).
- Signals tell you who to reach now. Examples given: hiring (multiple roles), headcount growth, funding, new HR or finance leader, vendor changes, product or market launches, intent searches, Q4 renewals.
- Data types: first-party (own site traffic, CRM), second-party (shared via webinar or partnership), third-party (public web, job posts, X posts, tools like Apollo).
- Signal quality = volume, refresh cadence, reliability, and ease of surfacing. Hiring refreshes weekly (run a campaign every week); new-leadership is rarer (about monthly). Run a quick test to see volume.
- Signal-based workflow anatomy: pick one "mother intent" signal, pull everyone who fits, ICP-filter, then stack secondary signals (for example 30 percent headcount growth, a funding round) so each person gets a different line. At scale this reads as "you did your homework".
- Signal-based (granular, refreshing) vs volume or broad-based campaigns (creative ideas, a strong offer to a segment, simple copy). Run a balance of both and keep testing multiple angles weekly.

### Context window and context engineering
- Tokens: roughly 4 characters per token; models are priced per million input and output tokens. Cheaper models suit simple tasks (a GPT-5-nano-class model was shown at fractions of a dollar per million tokens versus about 10 dollars for a top model).
- Context window = working memory for a session. Near 99 to 100 percent the model forgets, lags, or degrades. `/context` shows usage (the demo session showed 1M tokens, 6 percent used at one point). `/compact` summarizes; `/clear` starts fresh; auto-compact happens near full.
- Context engineering = deciding what is loaded and when: CLAUDE.md pointers, skills invoked on demand, subagents with their own windows, a work log to recover history.
- On "too much context hurts quality": the teacher's view was that giving the model needed context is fine; it gets chaotic when you dump everything in. You build the OS yourself and point the model at specific files.
- Other commands shown: `/init`, `/memory`, plan mode, `/rewind`, `/mcp`, remote control (drive your laptop session from your phone), hooks.

### CLAUDE.md
- A markdown project-instruction file that loads at the start of every session.
- Contains: company/client name, where things live (ICP, signals, skills), ground rules (for example "never use em dashes in copy"), "read this file before task X".
- Keep it lean; point to files instead of pasting content ("do not overbloat your CLAUDE.md").

### Skills
- A skill is a playbook packaged so it runs on its own. Invoke with `/` and pick from the project's list. Build one for anything repetitive (social posts, video edits, campaign analysis, cold email).
- Skills are project-scoped; the course provides a pack via the gtm-starter-kit repo (see live build).

### MCP vs CLI vs API
- All three are connectors from the agent to a tool. Most platforms offer at least one: MCP first, else CLI, else API.
- MCP (Anthropic protocol): pre-packaged tool instructions for the agent; loads all tool definitions and conversation into context, so it bloats the window and is slower.
- CLI (command line interface): defined commands run in the terminal; agent-executable, repeatable, works across agents (any agent can run CLI commands). Example: GitHub CLI.
- API: an endpoint plus method (GET, POST); no context bloat, "garbage in, garbage out". Best for bulk work (for example enriching 5,000 people). PlusVibe was shown offering both API and MCP; teacher defaults to the API key.
- Rule of thumb stated: bulk tasks go to API; CLI for repeatable work; use MCP only when it is the sole option. Preference order given: CLI and API over MCP when offered.
- Least privilege: when creating keys, grant read-only if you only need to read.

### Context OS folder structure
In-house version (as shown on the slide):
- `CLAUDE.md` (project instructions tying everything together)
- `context/` (facts about the business): `brand-kit/` (logos, colors), `icp/` (ICP, buyer personas), `messaging/`, `positioning/`, `docs/research/` (raw research; research landed here in the live build)
- `knowledge-base/`: `playbooks/` (frameworks you adopt, for example from a newsletter or a transcribed video) and `learnings/` (what happened when you executed; how you like to write copy, build Clay tables, structure waterfalls)
- `meetings/` (raw transcripts and action points, compounding over time)
- `output/` (things you make; subfolders such as outbound, social, data were added live)
- `tools/` (scripts, Python packages, cloned open-source tools)
- `weekly-priorities/` (one dated markdown file per week; can sync to ClickUp, Linear, Basecamp)
- `work-log/` (rawest record of every action; weekly file matching the priorities file; used to resume work in a new chat and to answer "what did I do this week")
- `.gitignore`, `.env`
- Agency or consultant variant: same structure plus a `clients/` folder with a subfolder per client (each with its own context, meetings, outputs), sharing the same tools and skills. A solo consultant needs one main folder with client subfolders. Teacher runs both an in-house and an agency-style repo.
- The structure is a flexible guide; an `inspiration/` folder was added live as an example (for example saved competitor ads).
- Context OS can be kept current automatically (teacher's own OS connects to meetings and Slack and posts daily priorities); anything done in a session should be documented there.
- Slide folder colors were illustration only, not a setting.

### Secrets, .env, .gitignore, 1Password
- API keys are passwords. Put them in `.env`; never commit them; list `.env` (and CSV lead lists) in `.gitignore`.
- Do not paste keys into chat. Ask Claude to scaffold the `.env` entry and add the value yourself.
- Rotate keys after a breach (a Railway incident was cited). Alternative: 1Password and its CLI, plus use for team sharing instead of Slack or WhatsApp.
- Avoid downloading customer data locally; use a database (Postgres, Supabase) and Clay for enterprise governance. Companies on enterprise Claude plans may restrict what Claude can access; do not use a personal Claude account for employer work.
- A hook can block an agent from printing a key (example given).

### GitHub basics
- GitHub = shared repository, version history, rollback ("version control"), collaboration. Private repos (invite only) vs public repos (anyone can clone).
- Commands, all driven by plain-language prompts to Claude Code: clone (copy a repo, public or accessible private), login, create a private repo and push, status or diff (what changed since last commit), stage, commit with a message, push, pull.
- Branch = a duplicate to change without touching main; open a pull request (PR); an admin or manager reviews and merges to main. Teacher works this way at work.
- A marketer can change a raw-code website by branching and opening a PR for engineering review.
- A public repo for the class, "GTM Starter Kit", was shown; clone it by giving Claude Code the link and "clone it for me".

### Subagents and parallel work
- Claude Code is the main agent (CEO/head of marketing analogy); it hands tasks to subagents, which return summaries.
- Each subagent has its own context window, so subagents protect the main window; they consume usage limits instead. In the demo, a 5-hour usage window showed 7 percent used.
- You can pick a cheaper model (for example Sonnet) for subagents while the main agent uses a stronger one.
- Parallel work: open another chat or session while one runs; use a hook to play a sound when a task finishes.

### Model choice and token cost
- Models named in the session (transcript spelling): Opus 5.5, Sonnet, Haiku (cheapest), "Fable 5.1" (garbled; teacher said it burns tokens and avoids it).
- Thinking effort options: low, medium, high; teacher's sweet spot is medium to high. Teacher mostly uses Opus 5.5.
- A Claude paid plan is required for Claude Code (Pro minimum; teacher uses Max). Cost tip: share a plan; the shared-subscription service named is spelled "Subdify/Subify" (inferred). Sharing is workable because work runs locally. Max plan was quoted as 100 dollars; four people splitting it was suggested (the per-person figure in the transcript, "$5", is garbled, so likely about 25 dollars (inferred)).
- Codex (OpenAI) works in the same IDE with the same natural-language approach; teacher sometimes runs Claude Code and Codex in parallel or hands tasks between them.
- Dictation tip: voice-to-text for long prompts (a paid tool and a free open-source alternative, "OpenWhisper" in the transcript (inferred spelling), were mentioned).

### treg.to and OpenRouter
- OpenRouter: one account, API access to many LLMs; route cheap bulk tasks to cheap models (DeepSeek for cleaning 10,000 company names; a small decision model for yes/no ICP classification, name garbled as "Jev" (inferred)).
- treg.to: pay-as-you-go catalog of tools (LinkedIn, X, TikTok, people and company enrichment, company-data providers); credit top-up in dollars; same providers Clay waterfalls use. Does things a plain web search cannot (for example pulling a founder's X posts).
- Mass enrichment (for example 2,000 rows): works at scale; compare cost against Clay subscription and credits or a direct provider API key first. Quality is the same underlying providers.

## The live build (PaidHR case study)

Case study company: PaidHR, an HR and payroll platform for African businesses (multi-currency payroll, tax compliance).

1. Scaffold. Create a folder (named "paid HR GTM OS" in the transcript), open it in VS Code, install and open the official Claude Code extension, and paste a scaffold prompt (from the course prompt pack) describing: this is the GTM Context OS for an in-house GTM team; create the folder structure, `.gitignore`, `.env`, `CLAUDE.md`, weekly priorities, and work log. Claude created it and began logging to the work log with times. Extra folders were then added by prompt (output/outbound, output/social, output/data, inspiration).
2. Connect a tool via CLI, scoped to the project. Asked Claude to research ways to connect treg.to; a subagent found four ways (CLI, API, MCP, and one more). Claude recommended MCP; teacher chose the CLI to avoid context bloat and said "scope everything to this project folder only". Sign-in happened via browser. The same flow works in Codex.
3. Parallel raw research with 4 subagents. Prompt: use free web search first, use the treg CLI only where web search cannot (company data, X posts), budget cap 3 dollars for treg. Four agents ran at once (customers, signals and market urgency, competitors, plus one more (inferred)). Cost reported: about 0.02 dollars of treg credit. Output saved under `research`. Spot-check flagged some numbers as likely wrong ("obviously this is not correct, so it needs to check").
4. Extend the research. Company site had case-study videos on YouTube; Claude transcribed them into a customer-videos markdown for social proof, looked up customer companies, and set up an open-source transcription tool (Whisper-based, from GitHub) in `tools/`. Rule: search GitHub for an existing tool before building one. A LinkedIn video download via treg then saved to `inspiration/` as a demo.
5. Synthesize raw research into context docs: ICP (example: headcount 20 to 100 and 100 plus; logistics, retail, manufacturing, banking; status quo of Excel or Google Sheets), positioning, offer, messaging, personas, signals. CLAUDE.md company details were filled in.
6. Pull in the gtm-starter-kit. Asked Claude to copy all tools, skills, and knowledge-base docs from the public repo into the local folder. Skills then appear under `/`.
7. Signal matrix (skill `signal-matrix`). Produced prioritized segments and signals, for example: HR or people-leader role posted in last 30 days; payroll or HR-ops roles posted; hiring 3 plus people; headcount growth of 15 to 20 percent; funding round; new HR or people leader in last 90 days.
8. Build-workflow-spec for one signal (skill `build-workflow-spec`). Chosen signal: new HR or people leader joined (mother intent). Output covers ICP (HQ country, employees, industry, titles such as Head of HR, HR manager, people operations, HR director, CPO), exclusions (existing customers), and execution parameters. Teacher changed the window from 90 to 180 days and widened geography from Nigeria to include Kenya and Ghana (South Africa also floated). This spec is what gets built in Week 2.
9. Campaign-strategy for broad ideas (skill `campaign-strategy`). Produced about 24 broad or volume campaign ideas to run alongside the signal campaign (for example new tax law, payslips, founder-sale angles).
10. Angle matrix. Mapped messaging angles per route (for example shift or site-based staff vs office-based vs first HR hire; logistics customers and casual-staff pay). Teacher noted a remote-team check could be added.
11. Campaign copy with QA (skill for campaign copy). Wrote subject ideas and line-one variants that route on conditions (first HR hire true/false, shift staff, office-based), social proof, and a soft CTA; teacher approved email 1 and had it write the full sequence. The skill's QA step ran (checks it is not insulting, facts hold, read from an HR manager's point of view). Stopped there for time; building it in tools is Week 2.
12. Teacher's step-by-step approach: break a skill into reviewed steps so you can review outputs and steer, and push everything to a repo (intended at the end; not shown completing in the transcript).

## The assignment

What to build (as stated): pick one company, "does not have to be the company you work at", "a dream company ... could be Stripe", build a Context OS for it, create a GitHub repo, and push everything.

Where to submit: the course document has a build log template to duplicate; add your name, the product, the ICP, the GitHub repo, and the rest. There is also a submission form. A separate feedback form was shared by the moderator (the teacher asked everyone to fill it). Teacher also said all of this would be in the LMS.

Deadline: stated loosely as "max by Friday" (the moderator also said a deadline was "just shared", but its exact date and time are not in the transcript, so confirm it in the course doc or form).

> I want you guys to pick a company that you are going to be building for.
> Pick one company. It does not have to be the company you work at. It could be a dream company that you would have loved working at.
> could be Stripe. It be any company that you want to use for your case study. Build a context OS for them.
> Create a GitHub repo. Push, what's it called? Push everything that you've done there. So as part of these documents, you guys will get, you see where to submit.
> There's a build log template here that you guys will duplicate. Then just add your name. Then you add. The products, the ICP, the GitHub repo, add everything here.
> Then, I've also created like this form, which you can then now use to submit this. I think you should also find all of this in DLMS also too.
> So, deadline, ideally, you guys should, should be done max by Friday. So, that you guys have like Sunday and majority of the week to work on this.
> know that some of you also have work to do during the week. So, take your time during the week to work on this.
> If you guys have any roadblocks, drop it on the community channel.

Note: "max by Friday" with "Sunday and majority of the week" is garbled; read literally the cohort works on it through the week and finishes by a Friday (inferred: Friday 2026-11-13, before next week's session). Verify.

Other homework stated mid-session: "before next week ... I want everybody to become Claude Code savvy" (install and use it).

## Action items for Neil

- [ ] Install Claude Code (VS Code extension, per the setup doc in the course resources) and get a paid Claude plan if not already on one.
- [ ] Read the course resources: setup Claude Code (Mac and Windows guides), MCP/CLI/API crash course, GitHub 101, the prompt pack, the slides.
- [ ] Clone the gtm-starter-kit public repo by giving Claude Code the link.
- [ ] Pick one B2B company with a good public footprint (employer is optional).
- [ ] Scaffold the Context OS folder with the prompt pack (CLAUDE.md, context/, knowledge-base/, meetings/, output/, tools/, weekly-priorities/, work-log/, .gitignore, .env).
- [ ] Connect at least one tool via CLI, scoped to the project; keep keys in `.env` only and confirm `.gitignore` excludes `.env` and lead CSVs.
- [ ] Run raw research with parallel subagents (free web search first, paid tools capped), save under `context/docs/research/`.
- [ ] Synthesize into ICP, positioning, messaging; review outputs yourself.
- [ ] Run `signal-matrix`, `build-workflow-spec` for one signal, `campaign-strategy`, angle matrix, and campaign copy with QA.
- [ ] Keep the work log updated as you go.
- [ ] Create a GitHub repo (private or public as chosen) and push; double check no keys were committed.
- [ ] Duplicate the build log template (name, product, ICP, GitHub repo) and submit via the form by the Friday deadline (confirm exact date and time).
- [ ] Fill in the feedback form.
- [ ] Optional: post the build publicly and tag the teacher (he encouraged build in public).
- [ ] Ask in the community channel if blocked.
- [ ] Recording is to be shared via the LMS (moderator said by Monday at the latest); LMS sign-up came by email.

## Next week preview

- Week 2: Clay plus a sequencer (PlusVibe, interchangeable with others) plus Claude. A Clay facilitator leads Clay content.
- Build the signal-based workflow from this week's workflow spec (the new HR/people leader signal for PaidHR), including Clay tables (also buildable programmatically from Claude Code), the signal and ICP filtering steps, and the campaign copy and angle routing drafted this week.
- The cohort gets Clay access and credits through the course's Clay partnership (stated at the end of the session; the "30K credits" figure was quoted by a moderator).
- Weeks 3 to 5 as listed in the header: post-acquisition, automations and agents, final presentations.
