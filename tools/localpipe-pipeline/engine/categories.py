#!/usr/bin/env python3
"""
Resolve plain-English business terms to LocalPipe's exact Google Maps category taxonomy.

/maps-search matches `query` against Google's official category list. When it matches
exactly, results are filtered to that category only — which is the difference between
"plumber" (clean) and "plumbing" (hardware stores, supply houses, handymen).

Usage:
    python3 engine/categories.py resolve "plumbers" "hvac" "med spa"
    python3 engine/categories.py expand "restaurant"        # every category containing the term
    python3 engine/categories.py grep "roof"                # raw substring search
"""

import csv
import glob
import json
import os
import re
import sys
from difflib import SequenceMatcher

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Business-speak that isn't in Google's taxonomy, mapped to what actually is.
ALIASES = {
    "hvac": "hvac contractor",
    "heating and cooling": "hvac contractor",
    "ac repair": "hvac contractor",
    "air conditioning": "hvac contractor",
    "med spa": "medical spa",
    "medspa": "medical spa",
    "dental": "dentist",
    "dental practice": "dentist",
    "dental office": "dentist",
    "legal": "law firm",
    "realtor": "real estate agency",
    "real estate agent": "real estate agency",
    "gym owner": "gym",
    "fitness": "gym",
    "salon": "hair salon",
    "barber": "barber shop",
    "landscaper": "landscaper",
    "lawn care": "lawn care service",
    "pest control": "pest control service",
    "auto shop": "auto repair shop",
    "mechanic": "auto repair shop",
    "body shop": "auto body shop",
    "vet": "veterinarian",
    "veterinary": "veterinarian",
    "veterinary clinic": "veterinarian",
    "animal hospital": "veterinarian",
    "fitness studio": "gym",
    "boutique fitness studio": "gym",
    "chiro": "chiropractor",
    "accountant": "accountant",
    "cpa": "certified public accountant",
    "bookkeeper": "bookkeeping service",
    "insurance agent": "insurance agency",
    "mortgage broker": "mortgage broker",
    "moving company": "moving company",
    "cleaner": "cleaning service",
    "cleaning company": "cleaning service",
    "maid service": "house cleaning service",
    "electrician": "electrician",
    "solar": "solar energy contractor",
    "pool company": "swimming pool contractor",
    "tree service": "tree service",
    "garage door": "garage door supplier",
    "flooring": "flooring contractor",
    "remodeler": "remodeler",
    "general contractor": "general contractor",
    "painter": "painter",
    "restaurant owner": "restaurant",
    "med practice": "medical clinic",
    "doctor": "medical clinic",
    "daycare": "day care center",
    "auto detailing": "car detailing service",
    "detailer": "car detailing service",
    "med spa owner": "medical spa",
}

_SUFFIXES = ("ies", "sses", "ses", "es", "s")

# Tokens that carry no taxonomy signal — "landscaping companies" is just "landscaper".
# Never applied if stripping would empty the term.
STOPWORDS = {
    "company", "companies", "business", "businesses", "owner", "owners",
    "local", "near", "me", "small", "independent", "best", "top", "the",
    "a", "for", "in", "and", "of", "practice", "practices", "provider", "providers",
    "office", "offices", "place", "places",
}

# Canonical storefront head-nouns. Given a tie, "pizza restaurant" beats "pizza takeout".
HEAD_NOUNS = {
    "restaurant", "store", "shop", "service", "contractor", "agency", "clinic",
    "salon", "center", "centre", "company", "firm", "supplier", "dealer", "school",
}

# Interchangeable tokens inside the taxonomy. Applied after the exact-string test,
# so genuine categories like "auto repair shop" still match themselves at 1.0.
SYNONYMS = {"auto": "car", "automotive": "car", "automobile": "car", "attorney": "lawyer"}


def categories_csv_path():
    """The taxonomy ships with the repo at data/categories.csv — a fresh clone just works."""
    override = os.environ.get("LOCALPIPE_CATEGORIES_CSV")
    if override and os.path.exists(override):
        return override
    vendored = os.path.join(PROJECT_ROOT, "data", "categories.csv")
    if os.path.exists(vendored):
        return vendored
    # Fallback: a raw LocalPipe dashboard export dropped anywhere in the repo.
    hits = sorted(glob.glob(os.path.join(PROJECT_ROOT, "**", "*business-categories*.csv"),
                            recursive=True))
    if not hits:
        raise SystemExit(
            "Category taxonomy not found. Expected it at data/categories.csv "
            "(it ships with this repo). Re-clone, or set LOCALPIPE_CATEGORIES_CSV "
            "to a LocalPipe category export."
        )
    return hits[-1]


_CACHE = None


def load_categories():
    global _CACHE
    if _CACHE is None:
        with open(categories_csv_path(), newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        cats = []
        for i, row in enumerate(rows):
            if not row:
                continue
            val = row[0].strip().strip('"').strip()
            if not val or (i == 0 and val.lower() == "category"):
                continue
            cats.append(val.lower())
        _CACHE = sorted(set(cats))
    return _CACHE


def normalize(text):
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s&/+-]", " ", text)
    text = text.replace("/", " ").replace("&", " and ")
    return re.sub(r"\s+", " ", text).strip()


def stem(token):
    """Light stemmer so 'roofer' / 'roofing' / 'roofs' collapse to one key."""
    token = SYNONYMS.get(token, token)
    if len(token) <= 3:
        return token
    for suf in ("ing", "ers", "er", "ors", "or"):
        if token.endswith(suf) and len(token) - len(suf) >= 3:
            return token[: -len(suf)]
    for suf in _SUFFIXES:
        if token.endswith(suf) and len(token) - len(suf) >= 3:
            return "y" + token[:-3] if suf == "ies" else token[: -len(suf)]
    return token


def stems(text, drop_stopwords=False):
    toks = [t for t in normalize(text).split() if t]
    if drop_stopwords:
        kept = [t for t in toks if t not in STOPWORDS]
        toks = kept or toks
    return {stem(t) for t in toks}


def score(term, category):
    tn, cn = normalize(term), normalize(category)
    if tn == cn:
        return 1.0
    ts, cs = stems(tn, drop_stopwords=True), stems(cn)
    if ts == cs:
        return 0.97
    if ts and ts <= cs:  # query fully inside the category: "hvac" -> "hvac contractor"
        return max(0.90 - 0.06 * (len(cs) - len(ts)), 0.60)
    if cs and cs <= ts:  # category fully inside the query: "landscaping co" -> "landscaper"
        return max(0.88 - 0.07 * (len(ts) - len(cs)), 0.58)
    union = ts | cs
    jaccard = len(ts & cs) / len(union) if union else 0.0
    fuzzy = SequenceMatcher(None, tn, cn).ratio()
    return min(0.84, 0.55 * jaccard + 0.45 * fuzzy)


def _ranked(term, cats):
    """Score every category, tie-broken toward canonical storefront nouns then brevity."""
    out = []
    for c in cats:
        s = score(term, c)
        if s < 1.0 and c.split()[-1] in HEAD_NOUNS:
            s = min(0.96, s + 0.02)
        out.append((-s, len(c), c))
    out.sort()
    return [(c, -negs) for negs, _, c in out]


def _alias_for(term):
    key = normalize(term)
    if key in ALIASES:
        return ALIASES[key]
    target = stems(key, drop_stopwords=True)
    for alias_key, alias_val in ALIASES.items():
        if stems(alias_key, drop_stopwords=True) == target:
            return alias_val
    return None


def resolve(term, k=5):
    """Return [(category, score)] best-first for one plain-English term."""
    cats = load_categories()
    alias = _alias_for(term)
    out = [(c, round(s, 3)) for c, s in _ranked(term, cats)[: max(k, 5) * 4]]
    if alias and alias in cats:
        out = [(alias, 1.0)] + [(c, s) for c, s in out if c != alias]
    return out[:k]


def expand(term, limit=None):
    """Every category whose stems contain the term — 'restaurant' -> 100+ cuisines."""
    ts = stems(term, drop_stopwords=True)
    hits = [c for c in load_categories() if ts and ts <= stems(c)]
    hits.sort(key=lambda c: (len(c.split()), c))
    return hits[:limit] if limit else hits


def grep(sub):
    s = normalize(sub)
    return [c for c in load_categories() if s in c]


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]

    if cmd == "resolve":
        out = {}
        for term in args:
            matches = resolve(term)
            out[term] = [{"category": c, "score": s} for c, s in matches]
            best, bs = matches[0]
            flag = "OK " if bs >= 0.90 else "?? "
            print(f"{flag}{term!r:28} -> {best!r} ({bs})")
            if bs < 0.90:
                alts = ", ".join(f"{c!r}" for c, _ in matches[1:4])
                print(f"{'':31}alternatives: {alts}")
        print("\n" + json.dumps(out, indent=2))
    elif cmd == "expand":
        hits = expand(" ".join(args))
        print(f"{len(hits)} categories\n" + "\n".join(hits))
    elif cmd == "grep":
        hits = grep(" ".join(args))
        print(f"{len(hits)} categories\n" + "\n".join(hits))
    elif cmd == "count":
        print(len(load_categories()), "categories from", categories_csv_path())
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
