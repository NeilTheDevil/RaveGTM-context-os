# What I built: Rave's GTM system

**Rave** builds websites for US owner-run local trades (tree service first). The system finds the
right businesses, checks they fit, spots what's wrong with their website, and hands them to the CRM
as deals, with the reason they're a fit and the angle to pitch.

```
Context OS (GitHub)  →  Clay: find + qualify  →  Clay Audiences: the market  →  HubSpot: deals
   who we sell to        100 companies tested       837 tree services            Clay sends each
   and why               28 ready, 9 send-ready     in one segment               fit company in
```

## 1. Context OS (week 1)
A GitHub repo Claude Code reads every session: who Rave sells to, the buying signals, the offer, the
system design. One-page version: [`CONTEXT-OS.md`](CONTEXT-OS.md).
**Key decision:** sell to tree services with **strong Google reviews but a weak website**.

## 2. Clay table (week 2)
100 tree services from Clay's free search, checked step by step. Free checks run first; paid steps
only run on companies that passed everything before them.

| Step | What it checks | Left |
|---|---|---|
| Free checks | US, 1-50 staff, not a franchise | 99 |
| Google reviews | 4.5+ stars from 25+ reviews | 60 |
| AI fit check | Is it really an independent tree service? (half were landscapers) | 38 **Fit** |
| AI site check | Does the website show those reviews? Click-to-call? Quote form? | **28 ready** |
| Email | From their own homepage, then Hunter, then verified | **9 send-ready** |

Each row also gets **ICP Fit** and **ICP Reason** in plain English, e.g. *"Independent US tree
service, 4.8 stars from 116 reviews."* Cost: 79 Clay credits.

**The finding:** 25 of the 28 ready businesses have great Google reviews and show **none** of them
on their website. That's the pitch.

## 3. Clay Audiences (week 2B)
Saved all **837** US tree services Clay knows about into one segment: the market size. A workflow
checks each one's Google reviews and labels it *ready for review*, *needs research* or *not a fit*,
writing the answer back onto the record (tested on one company).

## 4. HubSpot (week 3)
Fully automatic. For every ready Fit company, Clay looks the contact up in HubSpot, creates it if
it's missing, and writes **ICP Fit**, **ICP Reason** and the **Angle** onto it. A HubSpot workflow
starts on "ICP Fit is Meets Criteria and Angle is known", waits a minute, then:
creates a deal "{Company} – Website rebuild" ($2,000), sets the contact to MQL, branches by angle,
copies the angle onto the deal and creates a task ("Add to PlusVibe campaign: Review callback copy").

**Result (2026-11-21): 20 deals**, 17 Review callback, 2 Outdated site, 1 Quote form; 20 contacts
at MQL; 20 tasks. No hand-entered data.

## What I learned
- Design the system before touching tools. The spec decided every column.
- Free checks before paid ones. 100 companies cost 79 credits, not hundreds.
- Data can prove an idea wrong. The planned website checks found almost nothing; the real gap was reviews.
- The CRM should know *why* a lead is there (ICP Reason, angle), not just that it exists.
