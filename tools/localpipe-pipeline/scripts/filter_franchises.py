#!/usr/bin/env python3
"""
Franchise / chain filter for Localpipe scrape results.

Runs BEFORE enrichment. Franchise locations cannot buy a website redesign — their
site belongs to the franchisor (servpro.com/locations/tx/...), so the local owner
has nothing to sell. Filtering here saves the enrichment spend, not just the send.

Measured on a 50-business water-damage-restoration pull across Austin/Dallas/Houston
on 2026-08-14: 20 of 50 dropped (40%), 30 clean.

Usage:
    python3 filter_franchises.py scrape.json \
        --clean clean.json --review review.json --flagged franchises.json

Input: a Localpipe /get-scrape-results payload, or a bare JSON array of businesses.
"""

import json
import re
import sys
import argparse
import collections

# Signal 3 — known national/regional franchise brands in the trades Rave targets.
# Kept deliberately short: signals 1 and 2 catch most chains without a brand list,
# so this only needs the ones that slip through (single-location-domain franchisees).
BRANDS = [
    # restoration
    "servpro", "puroclean", "servicemaster", "service master", "rainbow international",
    "paul davis", "911 restoration", "restoration 1", "belfor", "rytech", "steamatic",
    "alldry", "all dry", "dki", "delta disaster", "first onsite", "cotton gds",
    "voda", "teasdale", "jarvis", "disaster blaster", "blackmon mooring",
    # adjacent trades
    "chemdry", "chem-dry", "roto-rooter", "roto rooter", "mr. rooter", "mr rooter",
    "stanley steemer", "zerorez", "coit", "duraclean", "aire serv", "mr. handyman",
    "true north", "archadeck", "mosquito joe", "lawn doctor", "weed man",
    # multi-location chains caught during the 2026-08-14 test pull
    "spaulding decon", "jenkins restorations", "usa clean master", "the steam team",
]

# Signal 2 — franchisor URL patterns. A location page living under a corporate
# path means corporate owns the site.
PATH_SIGNALS = re.compile(
    r"/(locations?|franchise|find-a-location|our-locations)/"
    r"|/(al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo"
    r"|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy)/"
    r"|/(alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware"
    r"|florida|georgia|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana"
    r"|maine|maryland|massachusetts|michigan|minnesota|mississippi|missouri|montana"
    r"|nebraska|nevada|ohio|oklahoma|oregon|pennsylvania|tennessee|texas|utah"
    r"|vermont|virginia|washington|wisconsin|wyoming)/",
    re.I,
)


def root_domain(url):
    """Strip scheme, www and path — leave the registrable-ish host."""
    if not url:
        return ""
    host = re.sub(r"^https?://", "", url, flags=re.I)
    host = re.sub(r"^www\.", "", host, flags=re.I)
    return host.split("/")[0].split("?")[0].lower()


# Signal 4 (soft) — a city or state slug in the PATH of a brand domain suggests a
# multi-location chain. Deliberately soft: an independent can legitimately have a
# city landing page (example-restoration.com/dallas). Only fires when the city is
# NOT already in the domain — austinwaterdamage.com is a local independent whose
# whole identity is the city, which is the opposite signal.
CITY_PATH = re.compile(
    r"/(city/)?[a-z]{3,}[-_]?(tx|texas|ca|fl|ny|az|ga|nc|pa|oh|il|mi|wa|co|va|nj|ma)\b"
    r"|/(austin|dallas|houston|phoenix|atlanta|chicago|denver|seattle|miami|tampa"
    r"|orlando|charlotte|raleigh|nashville|portland|sacramento|columbus)/",
    re.I,
)


def classify(businesses):
    """
    Three tiers, because binary clean/flagged over-drops or under-drops:

      franchise — confident. Drop before enrichment.
      review    — probable chain, one weak signal only. Eyeball before dropping.
      clean     — independent. Enrich these.

    Flagged items carry `_franchise_reasons` and `_tier`.
    """
    # Signal 1 — a root domain on more than one listing is a chain. Strongest
    # signal: needs no brand list, catches franchises nobody has heard of.
    domain_counts = collections.Counter(
        root_domain(b.get("website")) for b in businesses if b.get("website")
    )
    shared = {d: n for d, n in domain_counts.items() if d and n > 1}

    clean, review, franchise = [], [], []
    for b in businesses:
        name = (b.get("name") or "").lower()
        site = b.get("website") or ""
        root = root_domain(site)
        hard, soft = [], []

        if root in shared:
            hard.append(f"shared-domain({shared[root]}x)")
        if PATH_SIGNALS.search(site):
            hard.append("franchisor-path")
        for brand in BRANDS:
            if brand in name or brand.replace(" ", "").replace(".", "") in root:
                hard.append(f"brand:{brand}")
                break

        # Soft signal only counts when the city is not part of the domain itself.
        if not hard and CITY_PATH.search(site):
            domain_head = root.split(".")[0]
            city_in_domain = CITY_PATH.search("/" + domain_head + "/")
            if not city_in_domain:
                soft.append("city-path-on-brand-domain")

        if hard:
            franchise.append({**b, "_tier": "franchise", "_franchise_reasons": hard})
        elif soft:
            review.append({**b, "_tier": "review", "_franchise_reasons": soft})
        else:
            clean.append(b)

    return clean, review, franchise


def load(path):
    """Accepts a Localpipe payload, a bare JSON array, or a CSV."""
    if path.lower().endswith(".csv"):
        import csv as _csv
        with open(path, encoding="utf-8") as f:
            return list(_csv.DictReader(f))
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        return payload
    return payload.get("data") or payload.get("results") or []


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Localpipe scrape JSON")
    ap.add_argument("--clean", help="write independents here")
    ap.add_argument("--review", help="write probable-chain items here for eyeballing")
    ap.add_argument("--flagged", help="write confident franchises here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    businesses = load(args.input)
    if not businesses:
        print("No businesses found in input.", file=sys.stderr)
        return 1

    clean, review, franchise = classify(businesses)
    n = len(businesses)

    if not args.quiet:
        print(f"total      {n}")
        print(f"clean      {len(clean):>3}  ({len(clean)/n*100:.0f}%)  -> enrich these")
        print(f"review     {len(review):>3}  ({len(review)/n*100:.0f}%)  -> eyeball before dropping")
        print(f"franchise  {len(franchise):>3}  ({len(franchise)/n*100:.0f}%)  -> drop\n")
        for b in franchise:
            print(f"  DROP    {b['name'][:38]:38} {', '.join(b['_franchise_reasons'])}")
        for b in review:
            print(f"  REVIEW  {b['name'][:38]:38} {(b.get('website') or '')[:44]}")

    for path, rows, label in ((args.clean, clean, "clean"),
                              (args.review, review, "review"),
                              (args.flagged, franchise, "franchise")):
        if path:
            json.dump(rows, open(path, "w"), indent=2)
            print(f"\nwrote {len(rows)} {label} -> {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
