#!/usr/bin/env python3
"""
LocalPipe GTM Engine — job spec in, enriched CSV out.

One self-contained process owns the whole chain: submit batched /maps-search,
poll to terminal, paginate every offset, dedupe, fan out one /enrich per lead
with bounded concurrency and 429 retry, poll every job to completion, merge to CSV.

Per LocalPipe's agent guidance: the long waits live inside THIS process, never
inside an agent tool call. Launch with --detach and read `status` between turns.

Commands
    plan   <job.json>                Resolve categories, chunk batches, estimate volume + max credits.
    run    <job.json> [--detach]     Execute end-to-end. Resumable. No timeouts, ever.
    status [run_dir]                 Progress of the newest (or given) run.
    resume <run_dir>  [--detach]     Continue an interrupted run.
    cancel <run_dir>                 Cancel in-flight scrape + enrich jobs (partials preserved).
    csv    <run_dir>                 Re-emit results.csv from whatever has completed so far.
    doctor                           Verify Python, taxonomy, key, TLS, API. Zero credits.
"""

import collections
import csv
import json
import os
import random
import re
import ssl
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import categories as CAT  # noqa: E402

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_BASE = os.environ.get(
    "LOCALPIPE_API_BASE", "https://uunrlffonnvmbsstkpze.supabase.co/functions/v1"
)
ANON_KEY = os.environ.get("LOCALPIPE_ANON_KEY", "")  # Localpipe public anon key, from their docs; set in .env

# API-enforced batching ceilings (400 "Too many queries" / "Too many locations" above these).
MAX_QUERIES_PER_REQUEST = 5
MAX_LOCATIONS_PER_REQUEST = 25

# Hard ceiling is 500 req/min. Run under it and retry every 429 — a 429 is a dropped record.
RATE_LIMIT_PER_MIN = 460
SUBMIT_CONCURRENCY = 8
POLL_CONCURRENCY = 24          # polling endpoints are exempt from all rate limits
SCRAPE_PAGE_SIZE = 5000        # documented max
SCRAPE_POLL_INTERVAL = 15      # seconds between scrape status polls
STALL_WARN_SECONDS = 1200      # log a "still holding" note; never exit on a timer
MAX_RETRIES = 8

# Credit costs, per the pricing section at localpipe.io:
#   owner email (want_email)          2 credits
#   owner phone (want_phone)         10 credits
#   business email (want_general)     1 credit
#   Google Maps scraping              free
# Credits are spent only when contact data is successfully found, so MAX CREDITS is a
# ceiling rather than a bill. Override with LOCALPIPE_CREDITS_* env vars if your plan differs.
CREDITS_PER_EMAIL = int(os.environ.get("LOCALPIPE_CREDITS_EMAIL", 2))
CREDITS_PER_PHONE = int(os.environ.get("LOCALPIPE_CREDITS_PHONE", 10))
CREDITS_PER_GENERAL_EMAIL = int(os.environ.get("LOCALPIPE_CREDITS_GENERAL_EMAIL", 1))

NOT_FOUND = "not found"        # the API's literal negative-result sentinel

# Server-side filters — applied by /maps-search, so you never pay for excluded leads.
VALID_FILTERS = {
    "min_rating", "max_rating", "min_reviews", "max_reviews", "has_website",
    "has_phone", "price_level", "opens_before", "closes_after", "radius_km",
}

# Client-side filters — the API returns these fields but cannot filter on them. Applied
# after the scrape and BEFORE enrichment, so they still save the expensive credits.
POST_FILTER_KEYS = {
    "is_claimed": "bool — false finds unclaimed Google Business Profiles",
    "exclude_name_contains": "list[str] — drop franchises/chains by name",
    "include_name_contains": "list[str] — keep only names matching these",
    "exclude_categories": "list[str] — drop matched_category values",
    "require_phone": "bool — lead must have a phone number",
}

SCRAPE_TERMINAL_OK = {"success", "done", "completed"}
SCRAPE_TERMINAL_BAD = {"failed", "error", "cancelled", "canceled"}
ENRICH_TERMINAL_OK = {"completed", "success", "done"}
ENRICH_TERMINAL_BAD = {"failed", "error", "cancelled", "canceled"}

# Statuses that mean "legitimately still working" — wait on these forever, jobs never expire.
IN_FLIGHT = {"pending", "processing", "queued", "running", "in_progress", "interrupted"}
# Anything else (not_found, http_error, garbage) is unrecognized. Wait a long while in case
# it's an eventual-consistency blip, then give up on that ID alone rather than the whole run.
MAX_UNRECOGNIZED_POLLS = 20


class AuthError(Exception):
    """Bad key or no credits — fail fast and loud; retrying cannot help."""


# --------------------------------------------------------------------------- utils

def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "job").lower()).strip("-")[:60] or "job"


def api_key():
    key = os.environ.get("LOCALPIPE_API_KEY", "").strip()
    if key:
        return key
    for name in (".env", "engine/.env"):
        path = os.path.join(PROJECT_ROOT, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("LOCALPIPE_API_KEY"):
                    return line.split("=", 1)[1].strip().strip("'\"")
    raise SystemExit(
        "No API key. Put LOCALPIPE_API_KEY=... in ./.env or export it in your shell."
    )


class RateLimiter:
    """Global minimum spacing between submissions — holds the whole process under the cap."""

    def __init__(self, per_minute):
        self.interval = 60.0 / per_minute
        self.lock = threading.Lock()
        self.last = 0.0

    def acquire(self):
        with self.lock:
            wait = self.interval - (time.monotonic() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.monotonic()


LIMITER = RateLimiter(RATE_LIMIT_PER_MIN)


def _ssl_context():
    """
    Verified TLS, even on a python.org install whose cert bundle was never linked
    (macOS ships no OpenSSL CA file for the framework build until you run
    'Install Certificates.command'). Falls back to certifi's bundle.
    Verification is never disabled — we send an API key over this connection.
    """
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) > 0:
        return ctx
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ctx


SSL_CONTEXT = _ssl_context()


def _request(url, method="GET", payload=None, headers=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=120, context=SSL_CONTEXT) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:  # network blip, DNS, timeout
        return 0, json.dumps({"error": "transport", "message": str(exc)})


# Live tally of everything the API pushed back on, so a run can report its own error profile.
ERRORS = collections.Counter()
ERROR_LOCK = threading.Lock()


def note_error(kind):
    with ERROR_LOCK:
        ERRORS[kind] += 1


def post(path, payload, log=print):
    """POST with throttling and mandatory 429 retry. A 429 means the record was NOT accepted."""
    url = f"{API_BASE}/{path.lstrip('/')}"
    headers = {"Content-Type": "application/json", "x-api-key": api_key()}
    for attempt in range(MAX_RETRIES + 1):
        LIMITER.acquire()
        status, body = _request(url, "POST", payload, headers)
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body[:500]}

        if status in (200, 202):          # 202 is success, not an error
            if attempt:
                note_error(f"{path}:recovered_after_retry")
            return parsed
        note_error(f"{path}:{status}" + (f":{parsed.get('error')}" if parsed.get("error") else ""))
        if status == 429:
            retry_after = parsed.get("retry_after") or 60
            backoff = float(retry_after) + attempt * 1.0 + random.random() * 0.5
            log(f"  429 rate limit — retry {attempt + 1}/{MAX_RETRIES} in {backoff:.0f}s")
            time.sleep(backoff)
            continue
        if status in (0, 500, 502, 503, 504):
            backoff = min(60, 2 ** attempt) + random.random()
            log(f"  HTTP {status} on {path} — retry {attempt + 1}/{MAX_RETRIES} in {backoff:.0f}s")
            time.sleep(backoff)
            continue
        if status in (401, 402):
            # Retrying will never help: bad key, or the account is out of credits.
            raise AuthError(
                {401: "Invalid or inactive API key — check the key in the LocalPipe dashboard.",
                 402: "Out of credits / usage balance depleted — top up to continue."}[status]
                + f"  (API said: {parsed.get('message') or body[:160]})")
        raise RuntimeError(f"HTTP {status} on {path}: {body[:400]}")
    raise RuntimeError(f"{path}: exhausted {MAX_RETRIES} retries (last status {status})")


def get(path, params, log=print):
    """GET a polling endpoint. Uses the Supabase anon key; exempt from rate limits."""
    url = f"{API_BASE}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"
    for attempt in range(MAX_RETRIES + 1):
        status, body = _request(url, "GET", None, {"apikey": ANON_KEY})
        if status == 200:
            try:
                return json.loads(body)
            except Exception:
                return {"status": "unparseable", "raw": body[:1000]}
        note_error(f"poll {path}:{status}")
        if status in (0, 429, 500, 502, 503, 504):
            time.sleep(min(30, 2 ** attempt) + random.random())
            continue
        return {"status": "http_error", "http_status": status, "raw": body[:400]}
    return {"status": "http_error", "message": "poll retries exhausted"}


def chunk(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def clean(value):
    """The API returns the literal string 'not found' — never write that into a CRM."""
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() == NOT_FOUND else text


# ---------------------------------------------------------------------- job + plan

# Export CSVs use Title Case headers; the API and our own results.csv use snake_case.
# Normalize both to one internal shape so any LocalPipe CSV can be re-enriched.
CSV_ALIASES = {
    "business_name": "name", "name": "name", "company": "name", "company_name": "name",
    "website": "website", "business_website": "website", "url": "website", "domain": "website",
    "address": "full_address", "full_address": "full_address", "street_address": "full_address",
    "business_location": "full_address",
    "city": "city", "state": "state", "province": "state", "zip_code": "zip", "zip": "zip",
    "postal_code": "zip", "phone": "phone", "phone_number": "phone",
    "rating": "rating", "review_count": "review_count", "reviews": "review_count",
    "business_type": "matched_category", "matched_category": "matched_category",
    "types": "types", "category": "matched_category",
    "price_level": "price_level", "google_place_id": "place_id", "place_id": "place_id",
    "google_business_id": "business_id", "business_id": "business_id",
    "latitude": "latitude", "longitude": "longitude",
    "claimed": "is_claimed", "is_claimed": "is_claimed",
}


def normalize_header(h):
    return re.sub(r"[^a-z0-9]+", "_", (h or "").strip().lower()).strip("_")


def read_source_csv(path):
    """Load any LocalPipe export (or prior results.csv) into internal lead dicts."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise SystemExit(f"{path}: no header row")
        mapping = {}
        for col in reader.fieldnames:
            key = CSV_ALIASES.get(normalize_header(col))
            if key and key not in mapping.values():
                mapping[col] = key
        leads, skipped = [], 0
        for row in reader:
            lead = {}
            for col, key in mapping.items():
                val = (row.get(col) or "").strip()
                if val:
                    lead[key] = val
            if not lead.get("name"):
                skipped += 1
                continue
            # /enrich wants a location string; the export splits it across columns.
            if not lead.get("full_address"):
                parts = [lead.get("city"), lead.get("state")]
                lead["full_address"] = ", ".join(p for p in parts if p)
            leads.append(lead)
    return leads, mapping, skipped


DEFAULT_ENRICH = {
    "enabled": True,
    "want_email": True,
    "want_phone": False,
    "want_general_email": True,
    "general_email_fallback_only": True,
    "decision_maker_title": None,
    "require_website": False,
    "max_leads": None,
}


def load_job(path):
    with open(path, encoding="utf-8") as fh:
        job = json.load(fh)

    enrich = dict(DEFAULT_ENRICH)
    enrich.update(job.get("enrich") or {})

    # Source mode: enrich an existing CSV instead of scraping. No search block needed.
    source_csv = (job.get("source") or {}).get("csv")
    if source_csv:
        source_csv = os.path.expanduser(source_csv)
        if not os.path.exists(source_csv):
            raise SystemExit(f"source.csv not found: {source_csv}")
        job["name"] = job.get("name") or slugify(os.path.basename(source_csv))
        job["source"] = {"csv": source_csv}
        job["enrich"] = enrich
        job["dedupe"] = job.get("dedupe", True)
        job["post_filters"] = job.get("post_filters") or {}
        job["_filter_warnings"] = []
        job["search"] = None
        return job

    search = job.get("search") or {}
    queries = search.get("queries") or search.get("query") or []
    locations = search.get("locations") or search.get("location") or []
    if isinstance(queries, str):
        queries = [queries]
    if isinstance(locations, str):
        locations = [locations]
    if not queries or not locations:
        raise SystemExit("Job needs search.queries and search.locations (or source.csv).")

    raw_filters = search.get("filters") or {}
    filters = {k: v for k, v in raw_filters.items() if k in VALID_FILTERS}

    # A silently-dropped filter runs a FULL unfiltered scrape the user never asked for and
    # pays for. Surface every rejected key instead of swallowing it.
    job["_filter_warnings"] = []
    for key in raw_filters:
        if key not in VALID_FILTERS:
            hint = POST_FILTER_KEYS.get(key)
            job["_filter_warnings"].append(
                f"'{key}' is not a server-side filter and was dropped"
                + (f" — use post_filters.{key} instead" if hint else
                   f" (valid: {', '.join(sorted(VALID_FILTERS))})"))

    if filters.get("has_phone") is False:
        # Documented trap: false excludes every listing that HAS a phone.
        filters.pop("has_phone")
        job["_filter_warnings"].append(
            "has_phone:false excludes every listing WITH a phone — dropped")

    # Contradiction: a no-website search whose enrichment then discards no-website leads
    # deletes 100% of the run after paying for the scrape.
    if filters.get("has_website") is False and (job.get("enrich") or {}).get("require_website"):
        job["_filter_warnings"].append(
            "has_website:false + enrich.require_website:true would discard EVERY lead "
            "— forcing require_website:false")
        # Must patch the merged dict: it is what gets assigned to job["enrich"] below.
        # Writing to job["enrich"] here would be silently overwritten.
        enrich["require_website"] = False

    job["name"] = job.get("name") or slugify(f"{queries[0]}-{locations[0]}")
    job["search"] = {
        "queries": [str(q).strip() for q in queries if str(q).strip()],
        "locations": [str(l).strip() for l in locations if str(l).strip()],
        "limit": search.get("limit", "all"),
        "filters": filters,
        "relevance_filter": search.get("relevance_filter", "off"),
        "resolve_categories": search.get("resolve_categories", True),
    }
    job["enrich"] = enrich
    job["dedupe"] = job.get("dedupe", True)
    job["post_filters"] = job.get("post_filters") or {}
    return job


def build_plan(job):
    enrich = job["enrich"]
    per_lead_credits = (
        (CREDITS_PER_EMAIL if enrich["want_email"] else 0)
        + (CREDITS_PER_PHONE if enrich["want_phone"] else 0)
        # Fallback-only general email fires just on owner-email misses, but a ceiling
        # must assume the worst case: every lead falls back.
        + (CREDITS_PER_GENERAL_EMAIL if enrich["want_general_email"] else 0)
    )

    if job.get("source", {}).get("csv"):
        leads, mapping, skipped = read_source_csv(job["source"]["csv"])
        keyed = {lead_key(l) for l in leads}
        cap = enrich.get("max_leads")
        billable = min(len(keyed), cap) if cap else len(keyed)
        return {
            "job_name": job["name"],
            "mode": "csv",
            "source_csv": job["source"]["csv"],
            "csv_rows": len(leads) + skipped,
            "csv_skipped_no_name": skipped,
            "csv_unique": len(keyed),
            "csv_no_website": sum(1 for l in leads if not l.get("website")),
            "column_mapping": mapping,
            "resolved_queries": [], "original_queries": [], "category_warnings": [],
            "locations": [], "pairs": 0, "limit_per_pair": None,
            "maps_search_requests": 0, "requests": [],
            "max_leads": len(keyed),
            "credits_per_lead": per_lead_credits,
            "max_credits": billable * per_lead_credits,
            "filters": {}, "post_filters": job.get("post_filters") or {},
            "filter_warnings": job.get("_filter_warnings") or [], "enrich": enrich,
        }

    search = job["search"]
    resolved, warnings = [], []
    if search["resolve_categories"]:
        for term in search["queries"]:
            best, best_score = CAT.resolve(term, k=4)[0]
            resolved.append(best)
            if best_score < 0.90:
                alts = [c for c, _ in CAT.resolve(term, k=4)[1:]]
                warnings.append(
                    f"'{term}' -> '{best}' (confidence {best_score}); alternatives: {alts}"
                )
    else:
        resolved = list(search["queries"])

    seen, queries = set(), []
    for q in resolved:
        if q not in seen:
            seen.add(q)
            queries.append(q)

    q_batches = chunk(queries, MAX_QUERIES_PER_REQUEST)
    l_batches = chunk(search["locations"], MAX_LOCATIONS_PER_REQUEST)
    requests = [{"query": qb, "location": lb} for qb in q_batches for lb in l_batches]

    pairs = len(queries) * len(search["locations"])
    limit = search["limit"]
    per_pair = None if limit in ("all", None) else int(limit)
    max_leads = None if per_pair is None else pairs * per_pair

    cap = enrich.get("max_leads")
    if cap:
        billable = cap if max_leads is None else min(max_leads, cap)
    else:
        billable = max_leads  # None under Find ALL — genuinely unbounded

    return {
        "job_name": job["name"],
        "mode": "search",
        "resolved_queries": queries,
        "original_queries": search["queries"],
        "category_warnings": warnings,
        "locations": search["locations"],
        "pairs": pairs,
        "limit_per_pair": limit,
        "maps_search_requests": len(requests),
        "requests": requests,
        "max_leads": max_leads,
        "credits_per_lead": per_lead_credits,
        "max_credits": None if billable is None else billable * per_lead_credits,
        "filters": search["filters"],
        "post_filters": job.get("post_filters") or {},
        "filter_warnings": job.get("_filter_warnings") or [],
        "enrich": enrich,
    }


def print_credits(plan):
    e = plan["enrich"]
    want = [k.replace("want_", "") for k in
            ("want_email", "want_phone", "want_general_email") if e[k]]
    print(f"  ENRICH       {', '.join(want)}"
          + (f" | title: {e['decision_maker_title']}" if e.get("decision_maker_title")
             else " | target: owner")
          + (f" | cap {e['max_leads']} leads" if e.get("max_leads") else ""))
    mc = plan["max_credits"]
    print(f"  MAX CREDITS  {mc:,}" if mc is not None else
          "  MAX CREDITS  unbounded (Find ALL + enrich)")
    print(f"               @ {plan['credits_per_lead']} credits/lead — ceiling, not a bill;")
    print("               credits are only charged when data is actually found.")


def print_plan(plan):
    if plan.get("mode") == "csv":
        print(f"\n  JOB          {plan['job_name']}")
        print(f"  SOURCE       {os.path.basename(plan['source_csv'])}")
        print(f"  ROWS         {plan['csv_rows']:,} in file")
        if plan["csv_skipped_no_name"]:
            print(f"               {plan['csv_skipped_no_name']:,} skipped (no business name)")
        dupes = plan["csv_rows"] - plan["csv_skipped_no_name"] - plan["csv_unique"]
        print(f"  UNIQUE       {plan['csv_unique']:,} after dedupe"
              + (f"  ({dupes:,} duplicate rows dropped)" if dupes else ""))
        print(f"  NO WEBSITE   {plan['csv_no_website']:,} "
              f"(enriched via name + location lookup)")
        print(f"  MAPPED       {', '.join(sorted(set(plan['column_mapping'].values())))}")
        submit_min = plan["csv_unique"] / RATE_LIMIT_PER_MIN
        print(f"  THROTTLE     {RATE_LIMIT_PER_MIN}/min -> ~{submit_min:.0f} min to submit "
              f"all {plan['csv_unique']:,}")
        print_credits(plan)
        print()
        return

    print(f"\n  JOB          {plan['job_name']}")
    print(f"  CATEGORIES   {plan['resolved_queries']}")
    for w in plan["category_warnings"]:
        print(f"    ! low confidence: {w}")
    locs = plan["locations"]
    shown = ", ".join(locs[:8]) + (f" (+{len(locs) - 8} more)" if len(locs) > 8 else "")
    print(f"  LOCATIONS    {len(locs)} — {shown}")
    print(f"  FILTERS      {plan['filters'] or 'none'}")
    if plan.get("post_filters"):
        print(f"  POST-FILTERS {plan['post_filters']}  (applied before enrichment)")
    for w in plan.get("filter_warnings", []):
        print(f"    ! {w}")
    print(f"  BATCHING     {plan['pairs']} keyword x location pairs "
          f"-> {plan['maps_search_requests']} /maps-search request(s)")
    cap = plan["limit_per_pair"]
    print(f"  LIMIT        {cap} per pair"
          + ("  (Find ALL mode — no cap)" if cap in ("all", None) else ""))
    print(f"  MAX LEADS    {plan['max_leads'] if plan['max_leads'] is not None else 'unbounded'}")

    if not plan["enrich"]["enabled"]:
        print("  ENRICH       disabled (scrape only)")
    else:
        print_credits(plan)
    print()


# ------------------------------------------------------------------------ run state

class Run:
    def __init__(self, run_dir):
        self.dir = run_dir
        os.makedirs(run_dir, exist_ok=True)
        self.log_path = os.path.join(run_dir, "run.log")
        self.state_path = os.path.join(run_dir, "state.json")
        self.leads_path = os.path.join(run_dir, "leads.jsonl")
        self.jobs_path = os.path.join(run_dir, "enrich_jobs.jsonl")
        self.enriched_path = os.path.join(run_dir, "enriched.jsonl")
        self.csv_path = os.path.join(run_dir, "results.csv")
        self._lock = threading.Lock()
        self.state = self._load_state()
        # When detached, stdout IS run.log — don't write every line twice.
        self._echo = True
        try:
            if os.path.exists(self.log_path):
                self._echo = os.fstat(sys.stdout.fileno()).st_ino != os.stat(self.log_path).st_ino
        except (OSError, ValueError):
            pass

    def _load_state(self):
        if os.path.exists(self.state_path):
            with open(self.state_path, encoding="utf-8") as fh:
                return json.load(fh)
        return {"phase": "init", "started_at": utcnow(), "scrape_tasks": []}

    def save(self):
        with self._lock:
            self.state["updated_at"] = utcnow()
            tmp = self.state_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(self.state, fh, indent=2)
            os.replace(tmp, self.state_path)

    def log(self, msg):
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        with self._lock:
            with open(self.log_path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
                fh.flush()
        if self._echo:
            print(line, flush=True)

    def append(self, path, obj):
        with self._lock:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(obj) + "\n")
                fh.flush()

    def read_jsonl(self, path):
        if not os.path.exists(path):
            return []
        out = []
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return out

def dump_debug(run, name, obj):
    """Save the first raw response of each phase — makes field-name surprises debuggable."""
    path = os.path.join(run.dir, name)
    if os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)


# --------------------------------------------------------------------------- phases

def lead_key(lead):
    pid = (lead.get("place_id") or "").strip()
    if pid:
        return pid
    return f"{(lead.get('name') or '').lower()}|{(lead.get('full_address') or '').lower()}"


def phase_search(run, job, plan):
    """Submit every batched /maps-search. Arrays, never one request per city."""
    done = {t["index"] for t in run.state.get("scrape_tasks", [])}
    todo = [(i, r) for i, r in enumerate(plan["requests"]) if i not in done]
    if not todo:
        run.log(f"SEARCH  already submitted {len(done)} request(s) — skipping")
        return

    run.log(f"SEARCH  submitting {len(todo)} batched /maps-search request(s) "
            f"({plan['pairs']} keyword x location pairs)")

    def submit(item):
        idx, req = item
        payload = {"query": req["query"], "location": req["location"]}
        if plan["limit_per_pair"] not in ("all", None):
            payload["limit"] = int(plan["limit_per_pair"])
        else:
            payload["limit"] = "all"
        if plan["filters"]:
            payload["filters"] = plan["filters"]
        resp = post("maps-search", payload, run.log)
        task_id = resp.get("task_id")
        if not task_id:
            raise RuntimeError(f"no task_id in /maps-search response: {json.dumps(resp)[:300]}")
        run.log(f"  task {task_id}  <- {len(req['query'])} kw x {len(req['location'])} loc")
        return {
            "index": idx, "task_id": task_id, "query": req["query"],
            "location": req["location"], "status": "pending", "leads": 0,
        }

    with ThreadPoolExecutor(max_workers=SUBMIT_CONCURRENCY) as pool:
        for task in pool.map(submit, todo):
            run.state.setdefault("scrape_tasks", []).append(task)
            run.save()

    run.state["phase"] = "scrape_poll"
    run.save()


def phase_scrape_poll(run, job):
    """Poll every task to terminal, then paginate every offset. No timeout — ever."""
    tasks = run.state["scrape_tasks"]
    relevance = job["search"].get("relevance_filter", "off")
    seen = {lead_key(l) for l in run.read_jsonl(run.leads_path)}
    run.log(f"POLL    {len(tasks)} scrape task(s); {len(seen)} lead(s) already on disk")

    pending = [t for t in tasks if t.get("status") not in ("collected", "failed")]
    round_no = 0
    last_progress = time.monotonic()

    while pending:
        round_no += 1
        still = []
        for task in pending:
            resp = get("get-scrape-results",
                       {"task_id": task["task_id"], "limit": SCRAPE_PAGE_SIZE, "offset": 0,
                        "relevance_filter": relevance}, run.log)
            dump_debug(run, "debug_first_scrape_poll.json", resp)
            status = str(resp.get("status", "")).lower()

            if status in SCRAPE_TERMINAL_BAD:
                task["status"] = "failed"
                run.log(f"  task {task['task_id']}: FAILED ({resp.get('error') or status})")
                continue
            if status not in SCRAPE_TERMINAL_OK:
                if status in IN_FLIGHT:
                    task["unrecognized"] = 0
                else:
                    task["unrecognized"] = task.get("unrecognized", 0) + 1
                    if task["unrecognized"] >= MAX_UNRECOGNIZED_POLLS:
                        task["status"] = "failed"
                        run.log(f"  task {task['task_id']}: gave up after "
                                f"{MAX_UNRECOGNIZED_POLLS} polls returning '{status}' "
                                f"— other tasks continue")
                        continue
                prog = resp.get("progress") or {}
                if round_no == 1 or round_no % 4 == 0:
                    run.log(f"  task {task['task_id']}: {status or '?'} "
                            f"{prog.get('completed_work_units', '?')}/{prog.get('total_work_units', '?')} units, "
                            f"{prog.get('leads_found', 0)} leads")
                still.append(task)
                continue

            total = resp.get("total_results")
            contract = (resp.get("enrichment_contract") or {}).get("total_leads_to_enrich")
            collected, offset, page = 0, 0, resp
            while True:
                rows = page.get("data") or page.get("results") or []
                for lead in rows:
                    lead["_task_id"] = task["task_id"]
                    key = lead_key(lead)
                    if job["dedupe"] and key in seen:
                        continue
                    seen.add(key)
                    run.append(run.leads_path, lead)
                    collected += 1
                pag = page.get("pagination") or {}
                has_more = pag.get("has_more")
                if has_more is None:
                    has_more = len(rows) >= SCRAPE_PAGE_SIZE
                if not has_more:
                    break
                offset = pag.get("next_offset", offset + SCRAPE_PAGE_SIZE)
                page = get("get-scrape-results",
                           {"task_id": task["task_id"], "limit": SCRAPE_PAGE_SIZE,
                            "offset": offset, "relevance_filter": relevance}, run.log)
                if str(page.get("status", "")).lower() not in SCRAPE_TERMINAL_OK:
                    run.log(f"  ! page at offset {offset} returned {page.get('status')} — retrying once")
                    time.sleep(5)
                    page = get("get-scrape-results",
                               {"task_id": task["task_id"], "limit": SCRAPE_PAGE_SIZE,
                                "offset": offset, "relevance_filter": relevance}, run.log)
                    if str(page.get("status", "")).lower() not in SCRAPE_TERMINAL_OK:
                        break

            task["status"] = "collected"
            task["leads"] = collected
            task["total_results"] = total
            task["enrichment_contract"] = contract
            run.log(f"  task {task['task_id']}: DONE  total_results={total} "
                    f"new_after_dedupe={collected}")
            last_progress = time.monotonic()

        pending = still
        run.save()
        if pending:
            if time.monotonic() - last_progress > STALL_WARN_SECONDS:
                run.log(f"  ...still waiting on {len(pending)} task(s) after 20+ min "
                        f"(fair-share queue; jobs never expire server-side — holding)")
                last_progress = time.monotonic()
            time.sleep(SCRAPE_POLL_INTERVAL)

    leads = run.read_jsonl(run.leads_path)
    run.state["leads_total"] = len(leads)
    run.state["scrape_reported_total"] = sum(
        (t.get("total_results") or 0) for t in tasks if t.get("status") == "collected")
    run.state["phase"] = "enrich_submit"
    run.save()
    run.log(f"POLL    complete — {len(leads)} unique lead(s) collected "
            f"(API reported {run.state['scrape_reported_total']} across tasks, pre-dedupe)")


def phase_ingest_csv(run, job, plan):
    """Load an existing export into leads.jsonl — the same shape the scrape phase writes."""
    if os.path.exists(run.leads_path):
        existing = len(run.read_jsonl(run.leads_path))
        if existing:
            run.log(f"INGEST  {existing} lead(s) already on disk — skipping re-ingest")
            run.state["leads_total"] = existing
            run.state["phase"] = "enrich_submit"
            run.save()
            return

    leads, mapping, skipped = read_source_csv(job["source"]["csv"])
    run.log(f"INGEST  {os.path.basename(job['source']['csv'])}")
    run.log(f"  mapped columns: {json.dumps(mapping)}")
    if skipped:
        run.log(f"  ! {skipped} row(s) skipped — no business name, cannot enrich")

    seen, dupes = set(), 0
    for lead in leads:
        key = lead_key(lead)
        if job["dedupe"] and key in seen:
            dupes += 1
            continue
        seen.add(key)
        run.append(run.leads_path, lead)

    run.state["leads_total"] = len(seen)
    run.state["csv_rows"] = len(leads) + skipped
    run.state["csv_dupes_dropped"] = dupes
    run.state["phase"] = "enrich_submit"
    run.save()
    run.log(f"INGEST  {len(seen)} unique lead(s) ready"
            + (f" ({dupes} duplicate row(s) dropped)" if dupes else ""))


def apply_post_filters(leads, post, log=print):
    """
    Filter on fields the API returns but cannot filter on (is_claimed, name matching).
    Runs before enrichment so excluded leads never cost a credit.
    """
    if not post:
        return leads
    before = len(leads)
    out = leads

    if "is_claimed" in post:
        want = bool(post["is_claimed"])

        def claimed(lead):
            v = lead.get("is_claimed")
            if isinstance(v, str):
                return v.strip().lower() in ("true", "yes", "1")
            return bool(v)

        out = [l for l in out if claimed(l) == want]
        log(f"  post_filter is_claimed={want}: {len(out)} of {before} kept")

    if post.get("require_phone"):
        n = len(out)
        out = [l for l in out if (l.get("phone") or "").strip()]
        log(f"  post_filter require_phone: {len(out)} of {n} kept")

    for key, keep in (("exclude_name_contains", False), ("include_name_contains", True)):
        terms = [t.lower() for t in (post.get(key) or [])]
        if not terms:
            continue
        n = len(out)
        out = [l for l in out
               if any(t in (l.get("name") or "").lower() for t in terms) == keep]
        log(f"  post_filter {key} {terms}: {len(out)} of {n} kept")

    terms = [t.lower() for t in (post.get("exclude_categories") or [])]
    if terms:
        n = len(out)
        out = [l for l in out
               if not any(t in (l.get("matched_category") or "").lower() for t in terms)]
        log(f"  post_filter exclude_categories: {len(out)} of {n} kept")

    if len(out) != before:
        log(f"  post_filters: {before} -> {len(out)} leads "
            f"({before - len(out)} excluded before spending any credits)")
    return out


def phase_enrich_submit(run, job):
    """One /enrich per lead. Submission count MUST equal the lead count."""
    e = job["enrich"]
    leads = run.read_jsonl(run.leads_path)
    leads = apply_post_filters(leads, job.get("post_filters"), run.log)

    if e.get("require_website"):
        before = len(leads)
        leads = [l for l in leads if (l.get("website") or "").strip()]
        run.log(f"ENRICH  require_website=true dropped {before - len(leads)} lead(s) without a site")

    cap = e.get("max_leads")
    if cap and len(leads) > cap:
        run.log(f"ENRICH  ! CAPPED at {cap} of {len(leads)} leads by enrich.max_leads "
                f"— {len(leads) - cap} lead(s) NOT enriched")
        leads = leads[:cap]

    already = {r["key"] for r in run.read_jsonl(run.jobs_path)}
    todo = [l for l in leads if lead_key(l) not in already]
    run.state["enrich_target"] = len(leads)
    run.save()
    run.log(f"ENRICH  target {len(leads)} lead(s); {len(already)} already submitted; "
            f"{len(todo)} to submit")

    failures = []
    accepted = []          # list (not int) so worker threads can append without a lock
    abort = threading.Event()
    abort_reason = []

    def submit(lead):
        # A fatal auth/credit error means every remaining call is doomed — stop the fleet
        # instead of hammering the API once per lead and reporting nothing until the end.
        if abort.is_set():
            return None
        key = lead_key(lead)
        payload = {
            "business_name": lead.get("name") or "",
            "want_email": bool(e["want_email"]),
            "want_phone": bool(e["want_phone"]),
            "want_general_email": bool(e["want_general_email"]),
            "general_email_fallback_only": bool(e["general_email_fallback_only"]),
            "clay_row_id": key,
        }
        if lead.get("website"):
            payload["business_website"] = lead["website"]
        loc = lead.get("full_address") or lead.get("city")
        if loc:
            payload["business_location"] = loc
        if e.get("decision_maker_title"):
            payload["decision_maker_title"] = e["decision_maker_title"]
        try:
            resp = post("enrich", payload, run.log)
        except AuthError as exc:
            if not abort.is_set():
                abort.set()
                abort_reason.append(str(exc))
                run.log(f"ENRICH  !! FATAL: {exc}")
                run.log("ENRICH  !! aborting submission — no further calls will be made")
            return None
        except Exception as exc:
            failures.append({"key": key, "error": str(exc)})
            # Surface failures as they happen, not in a silent pile at the end.
            if len(failures) <= 5 or len(failures) % 250 == 0:
                run.log(f"  ! submit failed ({len(failures)} so far): {str(exc)[:160]}")
            # Everything failing and nothing succeeding = systemic; don't grind through 10k.
            if len(failures) >= 25 and not accepted and not abort.is_set():
                abort.set()
                abort_reason.append(
                    f"first {len(failures)} submissions all failed: {str(exc)[:200]}")
                run.log(f"ENRICH  !! aborting — {len(failures)} consecutive failures, "
                        f"0 accepted. Nothing is reaching the queue.")
            return None
        job_id = resp.get("job_id")
        if not job_id:
            failures.append({"key": key, "error": f"no job_id: {json.dumps(resp)[:200]}"})
            return None
        accepted.append(1)
        run.append(run.jobs_path, {"job_id": job_id, "key": key, "name": lead.get("name")})
        return job_id

    with ThreadPoolExecutor(max_workers=SUBMIT_CONCURRENCY) as pool:
        for i, _ in enumerate(pool.map(submit, todo), 1):
            # Report accepted, not attempted — "submitted 1700" while every call 401s is a lie.
            if i % 100 == 0:
                run.log(f"  attempted {i}/{len(todo)}  accepted {len(accepted)}")

    total_submitted = len(run.read_jsonl(run.jobs_path))
    run.state["enrich_submitted"] = total_submitted
    run.state["api_errors"] = dict(ERRORS)
    run.save()

    if abort.is_set():
        if failures:
            run.append(os.path.join(run.dir, "enrich_failures.jsonl"), {"failures": failures[:50]})
        raise AuthError(
            f"{abort_reason[0]}  |  {len(accepted)} accepted / {len(todo)} attempted. "
            f"Nothing was queued, so no credits were spent. Fix the cause and run "
            f"`resume {os.path.relpath(run.dir, PROJECT_ROOT)}` — it resubmits only the gap.")

    if failures:
        run.append(os.path.join(run.dir, "enrich_failures.jsonl"), {"failures": failures})
        run.log(f"ENRICH  ! {len(failures)} submission(s) failed — see enrich_failures.jsonl")

    # Count assertion: submitting fewer /enrich calls than leads is silent data loss.
    if total_submitted != len(leads):
        run.log(f"ENRICH  !! COUNT MISMATCH: {total_submitted} submitted vs {len(leads)} leads. "
                f"Re-run `resume` to submit the remainder.")
    else:
        run.log(f"ENRICH  count assertion OK — {total_submitted} submissions == {len(leads)} leads")

    run.state["phase"] = "enrich_poll"
    run.save()


def phase_enrich_poll(run, job):
    """Poll every enrichment job to terminal. Polls are unmetered; no timeout."""
    submissions = run.read_jsonl(run.jobs_path)
    done_ids = {r.get("job_id") for r in run.read_jsonl(run.enriched_path)}
    pending = {s["job_id"]: s for s in submissions if s["job_id"] not in done_ids}
    run.log(f"POLL    {len(pending)} enrichment job(s) outstanding "
            f"({len(done_ids)} already collected)")

    interval = 5 if len(submissions) <= 2000 else 10
    workers = POLL_CONCURRENCY if len(submissions) <= 2000 else POLL_CONCURRENCY * 2
    last_count, last_change = len(pending), time.monotonic()
    unrecognized = {}
    collected = len(done_ids)

    while pending:
        def poll(job_id):
            resp = get("get-job-results", {"job_id": job_id}, run.log)
            return job_id, resp

        finished = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for job_id, resp in pool.map(poll, list(pending.keys())):
                dump_debug(run, "debug_first_enrich_poll.json", resp)
                status = str(resp.get("status", "")).lower()
                if status in ENRICH_TERMINAL_OK:
                    records = (resp.get("records") or resp.get("results")
                               or (resp.get("data") or {}).get("records") or [])
                    run.append(run.enriched_path, {
                        "job_id": job_id,
                        "key": pending[job_id]["key"],
                        "clay_row_id": resp.get("clay_row_id"),
                        "records": records,
                    })
                    finished.append(job_id)
                elif status in ENRICH_TERMINAL_BAD:
                    run.append(run.enriched_path, {
                        "job_id": job_id, "key": pending[job_id]["key"],
                        "records": [], "error": resp.get("error_message") or status,
                    })
                    finished.append(job_id)
                elif status in IN_FLIGHT:
                    unrecognized.pop(job_id, None)
                else:
                    unrecognized[job_id] = unrecognized.get(job_id, 0) + 1
                    if unrecognized[job_id] >= MAX_UNRECOGNIZED_POLLS:
                        run.log(f"  ! job {job_id} returned '{status}' "
                                f"{MAX_UNRECOGNIZED_POLLS}x — abandoning this record")
                        run.append(run.enriched_path, {
                            "job_id": job_id, "key": pending[job_id]["key"],
                            "records": [], "error": f"unresolvable status: {status}",
                        })
                        finished.append(job_id)

        for job_id in finished:
            pending.pop(job_id, None)

        collected += len(finished)
        run.state["enrich_completed"] = collected
        run.state["api_errors"] = dict(ERRORS)
        run.save()
        run.log(f"  enriched {collected}/{len(submissions)}  ({len(pending)} pending)"
                + (f"  [api errors: {dict(ERRORS)}]" if ERRORS else ""))

        if pending:
            if len(pending) != last_count:
                last_count, last_change = len(pending), time.monotonic()
            elif time.monotonic() - last_change > STALL_WARN_SECONDS:
                run.log("  ...no movement in 20+ min. Jobs never expire server-side — holding.")
                last_change = time.monotonic()
            time.sleep(interval)

    run.state["phase"] = "output"
    run.save()


SCRAPE_COLS = [
    "name", "website", "phone", "full_address", "city", "rating", "review_count",
    "matched_category", "types", "price_level", "is_claimed", "place_id",
    "latitude", "longitude",
]
ENRICH_COLS = [
    "owner_name", "owner_first_name", "owner_last_name", "owner_email", "owner_phone",
    "business_email", "email_provider", "owner_role", "decision_maker_title",
]


def phase_output(run, job):
    # The CSV must describe what was actually targeted. If post_filters cut the list down to
    # unclaimed listings, the deliverable is those listings — not every lead the scrape saw.
    leads = apply_post_filters(run.read_jsonl(run.leads_path), job.get("post_filters"),
                               log=lambda _m: None)
    by_key = {}
    for row in run.read_jsonl(run.enriched_path):
        recs = row.get("records") or []
        by_key[row["key"]] = recs[0] if recs else {}

    header = ["business_name"] + SCRAPE_COLS[1:] + ENRICH_COLS + ["enriched"]
    hits = {c: 0 for c in ("owner_name", "owner_email", "owner_phone", "business_email")}

    with open(run.csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for lead in leads:
            rec = by_key.get(lead_key(lead))
            row = [clean(lead.get("name"))]
            for col in SCRAPE_COLS[1:]:
                val = lead.get(col)
                row.append(", ".join(val) if isinstance(val, list) else clean(val))
            for col in ENRICH_COLS:
                val = clean((rec or {}).get(col))
                if col in hits and val:
                    hits[col] += 1
                row.append(val)
            row.append("yes" if rec else "no")
            writer.writerow(row)

    run.state["phase"] = "done"
    run.state["api_errors"] = dict(ERRORS)
    run.state["stats"] = {
        "leads": len(leads),
        "enriched": sum(1 for l in leads if by_key.get(lead_key(l))),
        **{f"{k}_found": v for k, v in hits.items()},
    }
    run.save()
    with open(os.path.join(run.dir, "DONE"), "w") as fh:
        fh.write(utcnow())

    s = run.state["stats"]
    run.log("OUTPUT  " + run.csv_path)
    run.log(f"RESULT  {s['leads']} leads | {s['owner_name_found']} owner names | "
            f"{s['owner_email_found']} owner emails | {s['owner_phone_found']} phones | "
            f"{s['business_email_found']} business emails")
    if ERRORS:
        run.log(f"ERRORS  {json.dumps(dict(ERRORS))}")
    else:
        run.log("ERRORS  none — no 429s, no 5xx, no rejected submissions")
    run.log("DONE")


# ------------------------------------------------------------------------ commands

def cmd_plan(args):
    job = load_job(args[0])
    plan = build_plan(job)
    print_plan(plan)
    return plan


def new_run_dir(job):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(PROJECT_ROOT, "runs", f"{slugify(job['name'])}-{stamp}")
    os.makedirs(path, exist_ok=True)
    return path


def detach(argv, run_dir):
    log_path = os.path.join(run_dir, "run.log")
    with open(log_path, "a") as out:
        proc = subprocess.Popen(
            [sys.executable] + argv, stdout=out, stderr=subprocess.STDOUT,
            start_new_session=True, cwd=PROJECT_ROOT,
        )
    with open(os.path.join(run_dir, "run.pid"), "w") as fh:
        fh.write(str(proc.pid))
    print(f"detached pid={proc.pid}\nrun_dir={run_dir}\n"
          f"watch: python3 engine/lp.py status {os.path.relpath(run_dir, PROJECT_ROOT)}")


def execute(run, job):
    plan = build_plan(job)
    run.state["job"] = job
    run.state["plan"] = {k: v for k, v in plan.items() if k != "requests"}
    run.save()
    try:
        if job.get("source", {}).get("csv"):
            if run.state["phase"] in ("init", "ingest"):
                run.state["phase"] = "ingest"
                phase_ingest_csv(run, job, plan)
        else:
            if run.state["phase"] in ("init", "search"):
                run.state["phase"] = "search"
                phase_search(run, job, plan)
            if run.state["phase"] == "scrape_poll":
                phase_scrape_poll(run, job)
        if not job["enrich"]["enabled"]:
            run.log("ENRICH  disabled — scrape only")
            run.state["phase"] = "output"
        if run.state["phase"] == "enrich_submit":
            phase_enrich_submit(run, job)
        if run.state["phase"] == "enrich_poll":
            phase_enrich_poll(run, job)
        if run.state["phase"] == "output":
            phase_output(run, job)
    except AuthError as exc:
        run.state["phase"] = "failed"
        run.state["error"] = str(exc)
        run.save()
        run.log("FAILED  " + str(exc))
        with open(os.path.join(run.dir, "FAILED"), "w") as fh:
            fh.write(str(exc))
        sys.exit(1)
    except Exception as exc:
        import traceback
        run.state["phase"] = "failed"
        run.state["error"] = str(exc)
        run.save()
        run.log("FAILED  " + str(exc))
        run.log(traceback.format_exc())
        with open(os.path.join(run.dir, "FAILED"), "w") as fh:
            fh.write(str(exc))
        sys.exit(1)


def cmd_run(args):
    job_path = args[0]
    job = load_job(job_path)
    plan = build_plan(job)
    run_dir = new_run_dir(job)
    with open(os.path.join(run_dir, "job.json"), "w", encoding="utf-8") as fh:
        json.dump(job, fh, indent=2)
    with open(os.path.join(run_dir, "plan.json"), "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=2)

    run = Run(run_dir)
    if plan.get("mode") == "csv":
        run.log(f"START   {job['name']}  (csv source: {plan['csv_unique']:,} unique leads, "
                f"max {plan['max_credits']:,} credits)")
    else:
        run.log(f"START   {job['name']}  ({plan['maps_search_requests']} search request(s), "
                f"{plan['pairs']} pairs, limit={plan['limit_per_pair']}/pair)")
    if "--detach" in args:
        detach([os.path.abspath(__file__), "resume", run_dir], run_dir)
        return
    execute(run, job)


def cmd_resume(args):
    run_dir = os.path.abspath(args[0])
    if not os.path.exists(os.path.join(run_dir, "job.json")):
        raise SystemExit(f"No job.json in {run_dir}")
    with open(os.path.join(run_dir, "job.json"), encoding="utf-8") as fh:
        job = json.load(fh)
    if "--detach" in args:
        detach([os.path.abspath(__file__), "resume", run_dir], run_dir)
        return
    run = Run(run_dir)
    if run.state.get("phase") not in (None, "init"):
        run.log(f"RESUME  phase={run.state.get('phase')}")
    for sentinel in ("DONE", "FAILED"):
        path = os.path.join(run_dir, sentinel)
        if os.path.exists(path):
            os.remove(path)
    execute(run, job)


def latest_run():
    root = os.path.join(PROJECT_ROOT, "runs")
    if not os.path.isdir(root):
        return None
    dirs = [os.path.join(root, d) for d in os.listdir(root)
            if os.path.isdir(os.path.join(root, d))]
    return max(dirs, key=os.path.getmtime) if dirs else None


def cmd_status(args):
    run_dir = os.path.abspath(args[0]) if args else latest_run()
    if not run_dir:
        raise SystemExit("No runs yet.")
    state_path = os.path.join(run_dir, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {}
    done = os.path.exists(os.path.join(run_dir, "DONE"))
    failed = os.path.exists(os.path.join(run_dir, "FAILED"))

    print(f"run      {os.path.relpath(run_dir, PROJECT_ROOT)}")
    print(f"phase    {state.get('phase', '?')}"
          + ("  [DONE]" if done else "  [FAILED]" if failed else "  [running]"))
    tasks = state.get("scrape_tasks", [])
    if tasks:
        collected = sum(1 for t in tasks if t.get("status") == "collected")
        print(f"scrape   {collected}/{len(tasks)} task(s) collected")
    if state.get("leads_total") is not None:
        print(f"leads    {state['leads_total']}")
    if state.get("enrich_submitted") is not None:
        print(f"enrich   {state.get('enrich_completed', 0)}/{state['enrich_submitted']} complete"
              f" (target {state.get('enrich_target', '?')})")
    if state.get("stats"):
        print(f"stats    {json.dumps(state['stats'])}")
    if state.get("api_errors"):
        print(f"api errs {json.dumps(state['api_errors'])}")
    if state.get("error"):
        print(f"error    {state['error']}")
    log_path = os.path.join(run_dir, "run.log")
    if os.path.exists(log_path):
        print("\n--- last 12 log lines ---")
        with open(log_path, encoding="utf-8") as fh:
            for line in fh.readlines()[-12:]:
                print(line.rstrip())


def cmd_cancel(args):
    run_dir = os.path.abspath(args[0]) if args else latest_run()
    run = Run(run_dir)
    task_ids = [t["task_id"] for t in run.state.get("scrape_tasks", [])
                if t.get("status") not in ("collected", "failed")]
    if task_ids:
        resp = post("cancel-scrape-job", {"task_ids": task_ids[:500]}, run.log)
        run.log(f"CANCEL  scrapes: {json.dumps(resp)[:300]}")
    done_ids = {r.get("job_id") for r in run.read_jsonl(run.enriched_path)}
    job_ids = [s["job_id"] for s in run.read_jsonl(run.jobs_path) if s["job_id"] not in done_ids]
    totals = collections.Counter()
    # Docs allow 500 ids/call, but the endpoint 500s at that size in practice; 100 is instant.
    for batch in chunk(job_ids, 100):
        resp = post("cancel-enrich-job", {"job_ids": batch}, run.log)
        counts = {k: len(resp.get(k) or []) for k in
                  ("cancelled", "already_terminal", "not_found", "failed")}
        totals.update(counts)
        run.log(f"CANCEL  enrich batch of {len(batch)}: {counts}")
    if job_ids:
        run.log(f"CANCEL  totals across {len(job_ids)} job(s): {dict(totals)}")
        run.state["cancel_totals"] = dict(totals)
        run.save()
    pid_path = os.path.join(run.dir, "run.pid")
    if os.path.exists(pid_path):
        try:
            os.kill(int(open(pid_path).read().strip()), 15)
            run.log("CANCEL  stopped local runner")
        except (ProcessLookupError, ValueError):
            pass
    run.log("CANCEL  done — partial results are preserved and still retrievable")


def cmd_csv(args):
    run_dir = os.path.abspath(args[0]) if args else latest_run()
    run = Run(run_dir)
    with open(os.path.join(run_dir, "job.json"), encoding="utf-8") as fh:
        job = json.load(fh)
    phase_output(run, job)


OK, BAD, WARN = "  OK ", "  XX ", "  !! "


def cmd_check(args):
    """Verify every prerequisite end-to-end. Costs zero credits."""
    print("\nLocalPipe GTM Engine — doctor\n")
    failures = []

    # 1. Python
    v = sys.version_info
    if v >= (3, 8):
        print(f"{OK}python       {v.major}.{v.minor}.{v.micro}")
    else:
        print(f"{BAD}python       {v.major}.{v.minor} — need 3.8+")
        failures.append("Install Python 3.8 or newer: https://www.python.org/downloads/")

    # 2. Taxonomy
    try:
        cats = CAT.load_categories()
        rel = os.path.relpath(CAT.categories_csv_path(), PROJECT_ROOT)
        print(f"{OK}taxonomy     {len(cats):,} categories · {rel}")
    except SystemExit as exc:
        print(f"{BAD}taxonomy     {exc}")
        failures.append("data/categories.csv is missing — re-clone the repo.")

    # 3. API key present
    key = None
    try:
        key = api_key()
        src = "environment" if os.environ.get("LOCALPIPE_API_KEY") else ".env"
        shape = "OK" if key.startswith("lp_") else "does not start with 'lp_'"
        print(f"{OK if key.startswith('lp_') else WARN}api key      "
              f"...{key[-4:]} ({len(key)} chars, from {src}) — {shape}")
    except SystemExit:
        print(f"{BAD}api key      not found")
        failures.append(
            "Add your key:  cp .env.example .env  then paste your lp_... key into .env\n"
            "       Get one at https://localpipe.io → the API section of the app")

    # 4. TLS trust store
    store = ("system store" if ssl.create_default_context().cert_store_stats().get("x509_ca")
             else "certifi bundle")
    print(f"{OK}tls          verified via {store}")

    # 5. Reachability (unauthenticated, one shot, no retry storm)
    status, body = _request(f"{API_BASE}/get-scrape-results?task_id=connectivity-check",
                            "GET", None, {"apikey": ANON_KEY})
    if status == 0:
        print(f"{BAD}api reach    transport error: {body[:120]}")
        failures.append("Cannot reach the API. Check your network/VPN/firewall.")
    else:
        print(f"{OK}api reach    HTTP {status} · {API_BASE}")

    # 6. Key actually valid — authenticated probe that cannot spend credits.
    #    Cancelling a non-existent job id is free: 200 + not_found, or 401 if the key is bad.
    if key:
        status, body = _request(
            f"{API_BASE}/cancel-enrich-job", "POST",
            {"job_ids": ["00000000-0000-4000-8000-000000000000"]},
            {"Content-Type": "application/json", "x-api-key": key})
        if status == 200:
            print(f"{OK}key valid    authenticated (zero-cost probe — no credits used)")
        elif status == 401:
            print(f"{BAD}key valid    HTTP 401 — key is invalid or has been deactivated")
            failures.append(
                "Your API key was rejected. Generate a fresh one at\n"
                "       https://localpipe.io → the API section of the app, then update .env")
        elif status == 402:
            print(f"{BAD}key valid    HTTP 402 — out of credits")
            failures.append("Account is out of credits. Top up at https://localpipe.io")
        else:
            print(f"{WARN}key valid    unexpected HTTP {status}: {body[:120]}")

    if failures:
        print("\n  Fix these before running a job:\n")
        for f in failures:
            print(f"    → {f}")
        print()
        sys.exit(1)

    print("\n  All checks passed. Try your first list:\n")
    print("    python3 engine/lp.py plan jobs/examples/01-austin-plumbers.json\n")


COMMANDS = {
    "plan": cmd_plan, "run": cmd_run, "resume": cmd_resume, "status": cmd_status,
    "cancel": cmd_cancel, "csv": cmd_csv, "check": cmd_check, "doctor": cmd_check,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
