# How we got here: building Rave's GTM system, start to finish

The story of the build, including what went wrong and why the final design looks the way it does.
One-page overview: [`WHAT-I-BUILT.md`](WHAT-I-BUILT.md). Dated detail: [`work-log/`](work-log/).

## Week 1: the Context OS
We copied the private RaveGTM repo into a **new public repo**. We left out the git history, because
it contained a mailbox list and sending domains that shouldn't be public. Then we laid it out the
way the course and Bolaji's starter kit do:

- research
- ICP and personas
- 5 buying signals
- system architecture
- one target workflow spec

**The key decision:** sell to tree services with **strong Google reviews but a weak website**.

## Week 2: the Clay table
We turned the spec into a Clay table with ClayBP, in the Treford workspace.

- **The plan:** the spec said "weak website" meant no HTTPS, an old copyright year, or a slow site.
- **What the data showed:** on the first 50 companies those checks found **nothing**. Every site had
  HTTPS, footers update themselves to the current year, and the speed check needed a Google key.
- **The fix:** an **AI check of the homepage** instead. It found the real gap: **25 of 28 ready
  businesses have great Google reviews and show none of them on their site.** The data corrected
  the plan, and that is what a test should do.

**The funnel:** 100 companies → 38 ICP Fit → 28 ready → 9 with a verified email, for 79 credits.
Every row has an ICP Fit and a plain-English ICP Reason.

## Week 2B: Clay Audiences
We saved all **837 US tree services** into one Audience segment as the market size, and built a
workflow that checks each one's Google reviews and labels it.

## Week 3: HubSpot, where the learning happened

### Attempt 1: Clay → webhook → HubSpot workflow
Clay posted each Fit company to a HubSpot webhook URL. The workflow waited, created a deal, set
MQL, and branched by angle. It looked right, but **no leads showed up.**

What we found, step by step:

1. **The tests could never work.** The branch read the angle from the *webhook data*. A manual test
   on a sample contact has no webhook data, so every test fell to "None met".
2. **The task titles would have come out blank.** They read the Angle from the deal *as it was when
   created*, before Angle was set. They were switched to plain text per path.
3. **The real blocker:** a HubSpot webhook trigger can only enroll a **contact that already exists**.
   HubSpot had only its 2 sample contacts. The Clay data arrived (HTTP 202) but had nobody to
   attach to.
4. Adding the contacts by hand was rejected: a flow that needs manual entry is a dead flow.

### Attempt 2: make Clay create the contact itself
Clay was already connected to HubSpot, so we added columns:

- **Find contact:** look it up by email.
- **Create contact:** only if it's missing, so re-runs never duplicate.
- **Update contact:** writes ICP Fit, ICP Reason and Angle.

Even with the contact in place, the webhook still didn't enroll it, and HubSpot doesn't show why.

### Attempt 3, the final design: drop the webhook trigger
The contact now *carries* everything (ICP Fit, Angle), so the workflow starts from the contact itself:

- **Trigger:** "ICP Fit is Meets Criteria AND Angle is known".
- **Branch:** on the contact's Angle.
- HubSpot's editor couldn't change the existing branch without deleting and rebuilding 7 steps, so
  it was changed in place through HubSpot's API (with permission), keeping every step.

**Result (2026-11-21):** 20 deals at $2,000 each, all with the right Angle
(17 Review callback, 2 Outdated site, 1 Quote form), all contacts at MQL, 20 tasks. Fully automatic.

## Mistakes along the way (worth knowing)
- Counting the TAM by pulling every search result used up Clay's monthly search-result quota.
- A loose condition created 4 extra contacts with no Angle. They were deleted, and the condition now
  requires Ready to Contact.
- HubSpot screens were sometimes guessed at rather than seen.

**The lesson in each:** test small, check what actually happened in the system itself, and don't
trust a "200 OK" until the record shows up.

## Short summary (for submission notes)
> I built Rave's outbound system end to end. A Context OS on GitHub defines the ICP: US tree
> services with strong Google reviews but weak websites. A Clay table qualifies them: 100 companies
> → 38 ICP Fit → 28 ready, each with an ICP Reason and an angle. The data proved my planned website
> checks wrong, so I switched to an AI site check, which found the real gap: 25 of 28 hide their
> reviews. A Clay Audience sizes the market at 837 US tree services. Clay then creates each ready
> lead in HubSpot with ICP Fit, ICP Reason and Angle, and a HubSpot workflow automatically creates a
> $2,000 deal, sets MQL, branches by angle and assigns a follow-up task. Result: 20 deals with no
> manual entry. My first version used a HubSpot webhook trigger, which failed because webhooks can
> only enroll contacts that already exist. Moving contact creation into Clay and triggering on
> contact properties fixed it.
