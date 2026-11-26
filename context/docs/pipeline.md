# Pipeline: stages and lifecycle definitions

How a Rave lead moves through HubSpot (portal 149830192), and what each stage means. Claude reads this
before touching the CRM. How the data gets there: [`gtm-system.md`](gtm-system.md). The build story:
[`../../HOW-WE-GOT-HERE.md`](../../HOW-WE-GOT-HERE.md).

## Contact lifecycle (who the person is to us)

| Stage | Means | Set by | Entry rule |
|---|---|---|---|
| Lead | A tree service owner Clay found and qualified | Clay creates the contact (Lead is the starting stage) | ICP Fit = Fit, Ready to Contact? = true, an email on the company's domain |
| **Marketing Qualified Lead (MQL)** | Fits the ICP **and** has a known website gap to pitch | HubSpot workflow "Rave GTM Hubspot set up" | ICP Fit = "Meets Criteria" AND Angle is known |
| Sales Qualified Lead (SQL) | Replied with interest (wants to see the free redesign) | Neil, by hand, from the PlusVibe reply | A positive reply |
| Opportunity | Has seen the sample design and is talking price | Neil | Sample sent, call or reply about the build |
| Customer | Paid the $2,000 build | Neil | Payment received |

MQL is the only automatic jump today. Everything after it is a human decision, because it depends on a
reply. (Confirmed: the workflow sets `lifecyclestage = marketingqualifiedlead`; 20 of 20 contacts at MQL
on 2026-11-21.)

## Deal pipeline (the money)

Every MQL gets one deal, created by the workflow: **"{Company} – Website rebuild"**, amount **$2,000**,
owner Neil, with the contact's **Angle** copied on. The $97/mo care plan is added at Closed won.

Pipeline: **Outbound Sales Pipeline** (the default). Stage names and win chances are as set in HubSpot
(read 2026-11-26). The "Means" and "Moves on when" columns are Rave's working definitions.

| # | Stage | Win % | Means | Moves on when |
|---|---|---|---|---|
| 0 | **Prospecting** | 10 | Fit company with a known angle; not emailed yet. **The workflow creates every deal here.** | The lead is loaded into the PlusVibe campaign for its angle (the task is done) |
| 1 | Initial Outreach | 20 | In the email sequence | They reply with interest |
| 2 | Discovery Call Scheduled | 40 | Asked to see the free redesign, or booked a call | The call happens or the sample is sent |
| 3 | Qualified Meeting Held | 60 | Saw the sample for their trade and wants to talk | Price and scope agreed in principle |
| 4 | Proposal Sent | 75 | $2,000 build + $97/mo care plan sent | They respond to the proposal |
| 5 | Negotiation | 90 | Working out changes or timing | Paid, or said no |
| 6 | Closed Won | 100 | Paid the build; care plan starts | |
| 7 | Closed Lost | 0 | Said no, went silent after the sequence, or not a fit after all | |

Only stage 0 is automatic today. Every move after it is Neil's, because it depends on a reply. Three other
pipelines in the portal ("Test", "test v2 rave", "ravegtm deal pipeline") are leftovers from setup and are
not used.

## The properties that drive it

| Property | On | Values | Written by |
|---|---|---|---|
| ICP Fit (`icp_fit`) | Contact | Meets Criteria | Clay |
| ICP Reason (`icp_reason`) | Contact | Plain English, e.g. "Independent US tree service, 4.8 stars from 116 reviews." | Clay |
| Angle (`angle`) | Contact, Deal | Review callback, Outdated site, Quote form, Not secure | Clay (contact), workflow (deal) |

Angle picks the copy: each deal gets a task "Add to PlusVibe campaign: {Angle} copy".

## Snapshot (2026-11-21)

20 deals at $2,000 (17 Review callback, 2 Outdated site, 1 Quote form), 20 contacts at MQL, 20 tasks.
Re-checked 2026-11-26: 22 contacts, the 20 above at MQL, plus HubSpot's 2 sample contacts (no Angle, so
the workflow never enrolls them).

## Known warning
The "Set lifecycle to MQL" step shows "The lifecycle stage couldn't be updated because it would have been
set backwards." HubSpot never moves a lifecycle stage backwards. Likely cause: a test run on the sample
contact that is already at Opportunity. Confirmed: all 20 real contacts are at MQL, so none is affected. If a contact is already past
MQL (for example a client who replied), leaving them where they are is the right result.
