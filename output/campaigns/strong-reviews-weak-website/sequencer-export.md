# Sequencer export (PlusVibe): Strong reviews, weak website, tree service

Generated 2026-11-13 from the `## Copy` section of `workflow-spec.md`. Regenerate whenever that copy
changes. Status: drafted by an agent, **not reviewed by Neil, not loaded anywhere**.

PlusVibe syntax (`knowledge-base/playbooks/plusvibe-spintax.md`): spin `{{random|a|b}}`, merge
`{{first_name}}` `{{company_name}}`, fallback `{{fallback|{{first_name}}|there}}`. At most one variable
inside any spin block (checked: the only spin blocks containing a variable hold one).

Recommended settings: plain text ON, open tracking OFF, ignore out-of-office replies ON.
Suggested schedule: Mon-Fri, 08:00-17:00 in the prospect's timezone (confirm).
Custom variables: none. Only built-in fields are used (`first_name`, `company_name`).
List-build: blank every `"not found"` to empty; load each lead into exactly one of the three campaigns
by the first site check that fired (S3, then S4, then S5); re-check S3 within 72 hours of load.

Emails 2 and 3 are identical across the three campaigns. Only Step 1's two routed lines differ.

---

## Campaign A: `Strong reviews weak site - Tree - Not secure - v1`

Step 1 | wait: 0 days | new thread
Subject: {{random|your google reviews|tree service website|reviews and your site}}
Body:
{{random|Hey|Hi}} {{fallback|{{first_name}}|there}},

Your Google reviews are strong, but Chrome shows a "Not secure" warning when people open {{company_name}}'s website.

My guess is a few homeowners hit that warning and call the next company instead.

I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call.

Mind if I show you what it'd look like for {{company_name}}?

Neil Uko
Rave Web Studios

## Campaign B: `Strong reviews weak site - Tree - Old footer - v1`

Step 1 | wait: 0 days | new thread
Subject: {{random|your google reviews|tree service website|reviews and your site}}
Body:
{{random|Hey|Hi}} {{fallback|{{first_name}}|there}},

Your Google reviews are strong, but the copyright date at the bottom of {{company_name}}'s website is a few years old.

I'd guess a few homeowners notice the old date and wonder if they've found the right place.

I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call.

Mind if I show you what it'd look like for {{company_name}}?

Neil Uko
Rave Web Studios

## Campaign C: `Strong reviews weak site - Tree - Slow mobile - v1`

Step 1 | wait: 0 days | new thread
Subject: {{random|your google reviews|tree service website|reviews and your site}}
Body:
{{random|Hey|Hi}} {{fallback|{{first_name}}|there}},

Your Google reviews are strong, but Google's own speed test gives {{company_name}}'s website a poor score on phones.

Could be wrong, but people tapping through from your reviews on a phone probably don't all wait for it to load.

I put together a website design for tree service companies, built around the three things that actually turn a Google search into a phone call.

Mind if I show you what it'd look like for {{company_name}}?

Neil Uko
Rave Web Studios

---

## Steps 2 and 3 (same in all three campaigns)

Step 2 | wait: 3 days | same thread (subject "Re: <same subject>")
Body:
{{random|Hey|Hi}} {{fallback|{{first_name}}|there}},

You're clearly great at what you do. The site just isn't showing it.

Costs you nothing to look. If you like it and want it live by next week, I'll cover the setup myself.

I'm not an agency, it's just me. You'd be dealing with me directly, start to finish.

{{random|Want to see the design?|Open to a look at the design?|Worth a look at the design?}}

Neil Uko
Rave Web Studios

Step 3 | wait: 4 days | same thread
Body:
{{random|Hey|Hi}} {{fallback|{{first_name}}|there}},

{{random|Last note from me on this.|I'll leave it here after this one.|This is my last email on it.}}

{{random|If the website isn't on your list right now, no problem at all.|If the site isn't a priority right now, that's fine.|If now isn't the time for the website, all good.}}

{{random|If it is, I can walk you through the design on a quick 10 minute zoom.|If it is, a quick 10 minute zoom is enough to walk you through the design.|If it is, 10 minutes on a quick zoom is all it takes to show you the design.}}

{{random|Worth 10 minutes?|Open to that?|Want to do that this week?}}

Neil Uko
Rave Web Studios
