#!/usr/bin/env python3
"""
Fetch Google reviews for scraped businesses via LocalPipe /scrape-reviews-api.

The vendored engine does not support this endpoint — it shipped 2026-08-14, after
the repo. Reviews are FREE (not billed as enrichment), so this runs across the whole
list without touching the usage balance.

Adds to each record:
    review_user_name   reviewer's display name
    review_text        the review body
    review_rating      1-5
    review_time        "2 months ago"

Records with no usable review get empty strings — they are NOT dropped here.
Filter them out downstream if the copy requires a review.

Usage:
    python3 scripts/fetch_reviews.py leads.json --out leads_with_reviews.json
    python3 scripts/fetch_reviews.py leads.csv  --out leads_with_reviews.csv
"""
import argparse, csv, json, os, re, sys, time, urllib.request, urllib.error

API_BASE = os.environ.get("LOCALPIPE_API_BASE",
                          "https://uunrlffonnvmbsstkpze.supabase.co/functions/v1")
BATCH = 10          # hard API limit: 10 place_ids per call
MAX_RECENT_MONTHS = 12

# A reviewer name only works in copy if it reads like a person. "Neechie_Baby"
# and "J" do not. Reject handles, digits, underscores and single initials.
BAD_NAME = re.compile(r"[_\d]|^.{0,2}$|^[A-Z]\.?$")


def api_key():
    key = os.environ.get("LOCALPIPE_API_KEY", "").strip()
    if key:
        return key
    for name in (".env", "engine/.env"):
        if os.path.exists(name):
            for line in open(name, encoding="utf-8"):
                if line.startswith("LOCALPIPE_API_KEY"):
                    return line.split("=", 1)[1].strip().strip("\"'")
    sys.exit("No API key. Put LOCALPIPE_API_KEY=... in ./.env")


def usable_name(name):
    if not name:
        return False
    name = name.strip()
    first = name.split()[0] if name.split() else ""
    return not BAD_NAME.search(first)


def recent(review_time):
    """Keep reviews inside ~12 months. Quoting a 3-year-old review reads as stale."""
    t = (review_time or "").lower()
    if "year" in t:
        m = re.search(r"(\d+)", t)
        return not m or int(m.group(1)) < 1      # "a year ago" is borderline; keep
    return True                                   # days / weeks / months


def pick_review(reviews):
    """Best review for copy: recent, usable reviewer name, enough substance."""
    scored = []
    for r in reviews or []:
        text = (r.get("review_text") or "").strip()
        if len(text) < 60:                        # too thin to quote a detail from
            continue
        if not usable_name(r.get("user_name")):
            continue
        if not recent(r.get("review_time")):
            continue
        scored.append((len(text), r))
    if not scored:
        return None
    scored.sort(key=lambda x: -x[0])              # longest = most specific detail
    return scored[0][1]


def fetch(place_ids, key, max_reviews, rating_min):
    payload = json.dumps({"place_ids": place_ids,
                          "max_reviews": max_reviews,
                          "rating_min": rating_min}).encode()
    req = urllib.request.Request(f"{API_BASE}/scrape-reviews-api", data=payload,
                                 method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("x-api-key", key)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            sys.stderr.write(f"  HTTP {e.code}: {e.read().decode()[:200]}\n")
            return None
        except Exception as e:
            sys.stderr.write(f"  transport: {e}\n")
            time.sleep(3)
    return None


def load(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    data = json.load(open(path, encoding="utf-8"))
    return data if isinstance(data, list) else (data.get("data") or data.get("results") or [])


def save(rows, path):
    if path.endswith(".csv"):
        if not rows:
            return
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
    else:
        json.dump(rows, open(path, "w", encoding="utf-8"), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-reviews", type=int, default=8)
    ap.add_argument("--rating-min", type=int, default=4)
    a = ap.parse_args()

    rows = load(a.input)
    rows = [r for r in rows if r.get("place_id")]
    key = api_key()
    print(f"fetching reviews for {len(rows)} businesses ({BATCH} per call, free)")

    by_id = {}
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        res = fetch([r["place_id"] for r in chunk], key, a.max_reviews, a.rating_min)
        if res:
            for item in res.get("results", []):
                by_id[item.get("place_id")] = item.get("reviews", [])
        done = min(i + BATCH, len(rows))
        print(f"  {done}/{len(rows)}", end="\r", flush=True)
    print()

    hit = 0
    for r in rows:
        best = pick_review(by_id.get(r["place_id"]))
        if best:
            hit += 1
            r["review_user_name"] = best.get("user_name", "")
            r["review_text"] = (best.get("review_text") or "").strip()
            r["review_rating"] = best.get("rating", "")
            r["review_time"] = best.get("review_time", "")
        else:
            r["review_user_name"] = r["review_text"] = ""
            r["review_rating"] = r["review_time"] = ""

    save(rows, a.out)
    pct = hit / len(rows) * 100 if rows else 0
    print(f"usable review found: {hit}/{len(rows)} ({pct:.0f}%)")
    print(f"wrote {a.out}")
    if hit < len(rows):
        print(f"NOTE: {len(rows)-hit} rows have no usable review "
              f"(too short, stale, or unusable reviewer name). They are kept, not dropped.")


if __name__ == "__main__":
    main()
