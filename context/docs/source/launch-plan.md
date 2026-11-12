# Rave — Cold Email Launch Plan

Business: RaveGTM (brand "Rave" in copy). Website redesign for local service businesses.
Signature: Neil, Founder at Rave
Offer: $2,000 one-time build + $97/mo care plan.
Target capacity: 345 emails/day.
Starting from zero: no domains, no inboxes, nothing set up.

Built from the Launchpad SOPs 04 and 05, with PlusVibe swapped in for Sendkit.
ICP and messaging live in [icp-and-offer-digest.md](icp-and-offer-digest.md).

Last updated: 2026-08-11

---

## 1. The money model

Goal: $10,000 in 90 days. ACV $2,000. Benchmarks: close 25%, qualification 80%,
show 70%, LTA 30%, 75 leads per positive reply, 3-email sequence.

```
$10,000 goal / $2,000 ACV       = 5 deals
5 deals      / 25% close        = 20 qualified calls
20 calls     / 80% qualified    = 25 held calls
25 held      / 70% show         = 36 booked calls
36 booked    / 30% LTA          = 119 positive replies
119 replies  x 75 leads each    = 8,925 leads to contact
8,925 leads  x 3 emails x 0.85  = 22,760 emails over 90 days
22,760 / 3 months               = 7,590 emails per month
7,590 / 22 sending days         = ~345 emails per day
```

**The one sentence: send about 7,590 emails a month to make $10,000 in 90 days.**

Note: these are workshop benchmarks, not Neil's numbers. No personal campaign data
exists yet. Rebuild this model the moment the first 1,000 leads report back.

---

## 2. Infrastructure to buy

```
345 emails/day / 15 per Google inbox  = 23 → 24 inboxes (clean 3 per domain)
24 inboxes / 3 per domain             = 8 domains
```

**Buy: 8 domains, 24 inboxes.**

Go premium (.com), not cheap (.info). The ICP is local trades, many of whom
receive business mail at personal addresses. The deliverability SOP flags that as
burning infrastructure 3-5x faster. Cheap TLDs on top of that means rebuying in
week five.

### Why 24 and not 42

24 inboxes is the **steady-state** requirement — it sustains 345/day once
everything is warm and ramped. It does not deliver 8,925 leads inside a 90-day
window starting today, because the first six weeks produce nothing.

Hitting the full 90-day target from a cold start would take 42 inboxes on 14
domains. That is capacity bought for an unvalidated funnel: zero closed deals,
borrowed proof, and benchmark conversion rates that could be wrong in either
direction.

**Decision: buy 24. Accept that $10k lands nearer day 110-120 than day 90.**
Scaling from 8 domains to 14 is a two-week decision once real reply data exists.

**But buy all 8 domains at once, today.** Never stagger. A domain bought in week 5
does not reach full speed until week 12.

---

## 3. Domain buy list

All verified unregistered by whois on 2026-08-11. Availability changes daily —
buy today.

**Buy these eight:**

```
<sending-domain>
<sending-domain>
<sending-domain>
<sending-domain>
<sending-domain>
<sending-domain>
<sending-domain>
<sending-domain>
```

Each reads as a web design shop to a tradesperson, ties back to "Rave" in the
signature, sits under 35 characters, and has no hyphens or numbers.

**Verified-free alternates** if any get taken before checkout:

```
withrave.com          goravehq.com         myravehq.com
ravewebstudios.com    ravelocalweb.com     raverevamp.com
ravebuildco.com       ravewebify.com       getravestudio.com
tryravestudio.com     joinravestudio.com
```

**Taken, do not bother:** ravestudio.com (reg. 1998), ravemedia.com (reg. 1997),
getrave.com, tryrave.com, joinrave.com, userave.com, ravehq.com, raveweb.com,
ravesites.com, ravedigital.com, ravecreative.com, heyrave.com, raveworks.com,
ravelabs.com, ravepages.com, raveagency.com, theraveco.com, sendrave.com,
ravewebhq.com.

**Separately: ravegtm.com is also unregistered.** Buy it for the actual brand and
website, at a DIFFERENT registrar from the eight above. Never send cold email from
it. That is rule one of the deliverability SOP, no exceptions.

---

## 4. Buying rules

- Registrar: **Dynadot** (default; clean bulk buying and DNS). Spaceship or
  Porkbun price-match.
- **Do not use the same registrar for sending domains and ravegtm.com.**
- Enable **WHOIS privacy** on all eight.
- **Turn auto-renew OFF.** Cold email domains burn out. Do not get auto-charged in
  12 months for domains abandoned in month three.
- Buy all eight in one transaction so they warm on the same clock.
- Keep under ~250 domains per registrar account.

Cost: ~$88 one-time for the eight, plus ~$12 for ravegtm.com.

---

## 5. Inbox provisioning

Do not configure SPF, DKIM and DMARC by hand. The SOP is unambiguous: outsource it.

| Provider | Price | Note |
|---|---|---|
| **InboxKit** (Launchpad rate) | $3.00/inbox/mo = **$72/mo** | Cheapest. Buy domains yourself, import, they handle DNS + provisioning + warmup + export |
| PlusVibe Done-For-You | $4.00/inbox/mo = $96/mo | One less vendor, costs $24/mo more |

**Recommended: InboxKit at $3/inbox.**

Setup:
- 24 inboxes, 3 per domain, **Google Workspace only.** No Microsoft, no Azure for
  the first 90 days.
- Name inboxes as real people (neil@, not info@ or sales@).
- Confirm SPF, DKIM and DMARC are correct on all eight domains before any sending.

---

## 6. PlusVibe setup

**Plan: Personal.** $30.80/mo billed annually, $37/mo billed monthly.

All paid PlusVibe plans include **unlimited connected email accounts** — the
3-account cap applies only to the 14-day free trial. Personal gives 25,000
emails/month and 30,000 active leads. Usage will be ~7,590 emails and ~2,975 leads
per month, so there is 3x headroom. Do not pay for Business ($64.20-77/mo) yet.

Upgrade to Business only if deliverability suffers. Business adds Advanced Warm-Up
and Advanced ESP Matching, which matter for personal-Gmail recipients. That is a
month-two decision.

**Setup order:**

1. Start the 14-day free trial. Test with 2-3 inboxes first.
2. **Connect inboxes** — Google Workspace connects via one-click OAuth. SMTP/IMAP
   with an app password also works. Add all 24 once InboxKit hands them over.
3. **Enable warm-up on every inbox.** PlusVibe warms against a private pool of
   250,000+ accounts. Included free on all plans, no per-inbox charge.
4. **Warm-up settings:**
   - Cold-to-warmup ratio: **1:2** for brand new domains. 1:1 is the floor. Warm
     should always outnumber cold.
   - Enable **warm-up ramp-up** (+1 email/day until target).
   - Enable **randomized warm-up limits.** Fixed daily volumes create a detectable
     pattern.
   - Leave warm-up running permanently. It never fully stops.
5. **Set daily sending limits per inbox.** Start at 3/day. Never 15 on day one.
6. Turn on **auto-rotation of sender emails** so volume spreads across all 24.
7. Use **spintax** on subject lines and openers.
8. Build the 3-email sequence while warmup runs.

---

## 7. Timeline

Warm-up and ramp-up are two separate phases. This is what catches people out.

```
Week 0        Buy domains, provision inboxes             0 cold emails
Weeks 1-4     Warm-up (28 days)                          0 cold emails
Week 5        Ramp: 3/day per inbox                      ~72/day
Week 6        Ramp: 6/day per inbox                     ~144/day
Week 7        Ramp: 10/day per inbox                    ~240/day
Week 8+       Full speed: 15/day per inbox              ~360/day
```

**Full capacity lands around week 8, roughly day 56 from purchase.** Buying more
inboxes does not speed this up. Ramp is a time constraint, not a capacity one.

Warm-up length: the Launchpad SOP says 14-21 days. PlusVibe's own FAQ says 3-4
weeks for new accounts. Domains are brand new AND the ICP burns infrastructure
fast, so take the longer number: **28 days**.

Weeks 1-4 are not downtime. That is when the five sample designs, the lead list,
and the copy get built.

---

## 8. Monthly cost

```
InboxKit    24 inboxes x $3.00        = $72.00
PlusVibe    Personal (annual)         = $30.80
Localpipe   Growth (5,000 credits)    = $97.00
Maps scrape ~5,000 businesses @ $1/k  =  $5.00
Verification MillionVerifier          ~ $10-30
-------------------------------------------------
monthly total                         ~ $215-235
one-time    8 domains + ravegtm.com   ~ $100
```

**No Clay.** The lead-list SOP routes local and physical businesses to Localpipe
(Google Maps scrape), not Clay. That removes $446/mo. Clay is a workbench for
complex enrichment waterfalls; this is pulling tradespeople off Google Maps.

Localpipe and PlusVibe pricing verified against their own sites on 2026-08-11.

---

## 9. Lead list build — Localpipe

**Plan: Growth, $97/mo, 5,000 credits.**

```
Starter  $57/mo   2,000 credits   (too small at 345/day)
Growth   $97/mo   5,000 credits   ← this one
Pro     $157/mo  10,000 credits

Google Maps scrape       $1 per 1,000 businesses
Business email           1 credit
Owner email (personal)   2 credits
Owner phone             10 credits
```

At ~2,975 leads/month, business-email-only costs ~2,975 credits. Growth covers it
with room to add owner emails on A-tier accounts later.

The scrape is nearly free. Credits are only spent on contact data, so pull wide and
filter hard before enriching.

**Fields returned:** business name, address, rating, review count, website presence,
phone, business email, owner name, owner email, owner phone.

### Review text — RESOLVED

Confirmed directly with the Localpipe founder (2026-08-11): **there is a review
scraping feature in business lists.** No second source needed. The highest-converting
angle (quoting a real customer review back to the owner) is supported natively, and
the data line in section 8 stands.

Open: account signup failed, founder contacted. Once access is live, review the API
key and documentation to map exactly what the export returns and which fields feed
the copy.

### Business email vs owner email

| | Cost | Reply rate | Infra burn |
|---|---|---|---|
| Business email | 1 credit | Lower (generic inbox) | Normal |
| Owner email | 2 credits | Higher (decision maker) | **3-5x faster** |

Localpipe labels owner email as *personal* — exactly the address type the
deliverability SOP says burns infrastructure 3-5x faster and cannot be warmed
against.

**Start with business email.** Eight brand-new domains with no reputation cannot
absorb personal-inbox burn. Add owner email for A-tier accounts only, after three
clean months.

### Drop @gmail recipients — campaign one

Personal Gmail is **30-50% of local business lists** and burns infrastructure 3-5x
faster. Warmup pools contain no @gmail accounts, so every send to one looks cold no
matter how well the mailbox is warmed.

Reaching them properly needs isolated infrastructure at roughly 2-3x cost. That is
not a spend to make against an unproven offer on brand-new domains.

**So: filter them out before sending.**

`/enrich` returns **`email_provider`** — `google`, `microsoft`, etc. Use it as a hard
filter at list-build time. Also drop any address whose domain is literally
`gmail.com`, `yahoo.com`, `outlook.com`, `aol.com`, `hotmail.com`, or `icloud.com`.

This is a filtering step, not an infrastructure change. All 8 domains stay one pool.
A separate Gmail lane is a decision for after the offer converts — see decision 22.

**Volume consequence:** cutting 30-50% of the list means roughly **2x the scrape
volume** for the same contactable-lead count. Plan **8-10 metro-vertical
combinations per month**, not 5-7.

Caveat worth checking early: for small trades the listed business email is often
already a Gmail. Hand-check 20 records before committing to volume — if the drop rate
is far above 50%, the geography plan needs widening again.

### Build order (never vary this)

```
Accounts → Qualify → Enrich and Score → Contacts → Emails (last)
```

Each step filters the next, so spend only lands on companies that already qualified.

1. Scrape accounts only. Wide pull, dedupe by business name + address.
2. Pre-pull QA: hand-check 5-10 results, confirm fields, estimate credit cost
   before hitting run.
3. Filter on website presence. **Primary target is businesses WITH a weak site** —
   the offer is a redesign, and the proven copy critiques an existing site.
   No-website businesses are a separate, smaller campaign with different copy.
4. AI qualification pass: read each site, judge whether it is genuinely weak (no
   mobile layout, no SSL, copyright 2016 or earlier, generic template). Drop the
   fails. Never enrich a company that did not qualify.
5. Score and tier. Review count and rating are proxies for "has money and cares
   about reputation." High review count + weak site = A-tier.
6. Pull business emails on qualified accounts only.
7. **Drop @gmail and other consumer-domain recipients** using `email_provider` plus a
   domain blocklist. Expect to lose 30-50% here — that is intended.
8. Verify every address with MillionVerifier 2-3 days before launch, not weeks
   ahead. Email data goes stale fast. Drop catch-all-only addresses.

### Source split by vertical

Priority verticals from the strategy brief, all strong Google Maps plays:
foundation/waterproofing, restoration, movers, tree service, fencing & decking,
roofing, paving/concrete.

HVAC and plumbing are deliberately deferred — flooded inboxes. Manufacturers are
not a Maps ICP and are out of scope.

### Volume planning

After the Gmail drop, a single city-vertical scrape yields roughly 100-300 businesses, and only a
fraction have a qualifying weak site. To sustain ~2,975 leads/month, plan for
roughly 15-20 city-vertical combinations per month. With 5-7 priority verticals
that is about 3-4 new metros a month. Build the geography list up front.

---

## 10. What this earns

**First 90 days** (ramp-limited — weeks 1-4 send nothing):

```
24 inboxes x ~545 emails each      = ~13,080 emails
13,080 / (3 x 0.85)                = ~5,130 leads contacted
5,130 / 75                         = ~68 positive replies
68 x 30% LTA                       = ~20 booked calls
20 x 70% show x 80% qual           = ~11 qualified calls
11 x 25% close                     = ~2.9 deals
2.9 x $2,000                       = ~$5,800
```

**Steady state after ramp** (~7,590 emails/month):

```
~2,975 leads/mo → ~40 positive → ~12 booked → ~7 qualified → ~1.7 deals/mo
1.7 x $2,000                       = ~$3,400/mo
plus care plan at 60% attach       = +~$100/mo recurring, compounding
```

Against ~$225/mo cost, that is roughly 15x at steady state. The care plan alone
covers the entire stack after three clients.

**The cheapest lever is not more inboxes — it is leads-per-positive-reply.** The
75:1 benchmark assumes generic outbound. A finished redesign plus a real quoted
review should beat it substantially. Cut 75:1 to 40:1 and revenue nearly doubles at
identical cost.

---

## 11. Volume rule

About **1,000 leads contacted per campaign** before the data means anything. At
345/day that is roughly 3 sending days at full speed. Do not judge a campaign
before then.

Watch two numbers after launch:
- **Reply rate.** A steady 2.5% dropping to 1.5% with nothing else changed means
  something broke deliverability-side. Pause and investigate.
- **Bounce rate.** Under 3% healthy. Over 5% list quality dropped. Over 10% is an
  emergency — pause immediately or burn domains.

---

## 12. This week's checklist

- [ ] Buy the 8 sending domains at Dynadot. Privacy on, auto-renew off.
- [ ] Buy ravegtm.com at a different registrar.
- [ ] Sign up for InboxKit, import the 8 domains, order 24 Google inboxes.
- [ ] Start the PlusVibe 14-day trial, connect 2-3 inboxes to learn the UI.
- [ ] Confirm SPF/DKIM/DMARC land on all 8 domains.
- [ ] Enable warmup on every inbox at a 1:2 ratio, randomized, with ramp-up on.
- [ ] Start the 28-day warmup clock.
- [ ] Chase Localpipe account access (signup failed, founder contacted). Review
      review text is confirmed available.
- [x] Employment agreement checked — no restriction, project is separate from work.
- [ ] Line up 3 businesses for free builds (see below).

During warmup (weeks 1-4): five sample designs, ICP geography list, Localpipe pull,
copy. Skills 06 through 10.

### Also during warmup: build 3 real case studies

Borrowed agency results are out of the copy entirely (see
[icp-and-offer-digest.md](icp-and-offer-digest.md)). Replace them with proof that is
100% Neil's, inside the same 28-day window:

Build 3 sites free or near-free for nameable local businesses. Agree up front:
written permission to use their name, a testimonial, and before-and-after numbers.
**Record the baseline before launch** — Google Business Profile reports calls and
direction requests; also capture form submissions and quote requests. Re-measure at
30 days.

By week 5, when sending starts, that is three named case studies in the same
verticals being emailed. Costs time already budgeted for sample designs.

---

Built from the Launchpad SOPs. Legacy GTM x Revenue Boost.
