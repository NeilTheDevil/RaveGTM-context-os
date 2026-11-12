#!/usr/bin/env python3
"""
Merge enriched Localpipe batches into one PlusVibe-ready send list.

Steps, in order:
  1. Merge every batch's results.csv
  2. Keep only sendable rows (owner_email or business_email present)
  3. Pick one email per lead: owner_email preferred (verified), else business_email
  4. Strip literal "not found" -> empty everywhere (Localpipe's not-null-not-empty
     convention would otherwise defeat PlusVibe's {{fallback|...}} — see
     reference/plusvibe-spintax.md)
  5. Drop consumer-domain recipients (gmail/yahoo/outlook/...) per decision 22 —
     campaign one eliminates Gmail rather than isolating it
  6. Dedupe by email address
  7. Write PlusVibe columns: first_name, company_name, city, email + tracking columns

Usage:
    python3 scripts/build_send_list.py results1.csv results2.csv ... \
        --out send-list.csv --dropped dropped.csv
"""
import argparse, csv, sys
sys.path.insert(0, "scripts")
from drop_consumer_email import CONSUMER_DOMAINS

NF = lambda v: (v or "").strip().lower() in ("", "not found", "none", "null")
clean = lambda v: "" if NF(v) else v.strip()


def domain_of(email):
    return email.rsplit("@", 1)[-1].lower() if "@" in email else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="enriched results.csv files to merge")
    ap.add_argument("--out", required=True, help="PlusVibe-ready send list")
    ap.add_argument("--dropped", help="rows dropped, with a reason column")
    args = ap.parse_args()

    rows = []
    for path in args.inputs:
        with open(path, newline="", encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))

    seen_email = set()
    send, dropped = [], []

    for r in rows:
        name = clean(r.get("business_name") or r.get("name"))
        city = clean(r.get("city"))
        owner_email = clean(r.get("owner_email"))
        biz_email = clean(r.get("business_email"))
        first = clean(r.get("owner_first_name"))
        website = clean(r.get("website"))

        email = owner_email or biz_email
        if not email:
            dropped.append({**r, "_reason": "no email"})
            continue
        if not name:
            dropped.append({**r, "_reason": "no company name"})
            continue

        dom = domain_of(email)
        if dom in CONSUMER_DOMAINS:
            dropped.append({**r, "_reason": f"consumer domain ({dom})"})
            continue

        key = email.lower()
        if key in seen_email:
            dropped.append({**r, "_reason": "duplicate email"})
            continue
        seen_email.add(key)

        send.append({
            "first_name": first,
            "company_name": name,
            "city": city,
            "email": email,
            "emailSource": "owner_email" if owner_email else "business_email",
            "website": website,
            "place_id": clean(r.get("place_id")),
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["first_name", "company_name", "city", "email", "emailSource", "website", "place_id"])
        w.writeheader()
        w.writerows(send)

    if args.dropped and dropped:
        cols = sorted({k for r in dropped for k in r} | {"_reason"})
        with open(args.dropped, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(dropped)

    named = sum(1 for r in send if r["first_name"])
    print(f"merged input        : {len(rows)}")
    print(f"send list           : {len(send)}  ({named} with first name, {len(send)-named} fallback to 'there')")
    print(f"dropped              : {len(dropped)}")
    from collections import Counter
    reasons = Counter(r["_reason"] for r in dropped)
    for k, v in reasons.most_common():
        print(f"  - {k:28} {v}")
    print(f"\nwrote {args.out}")
    if args.dropped:
        print(f"wrote {args.dropped}")


if __name__ == "__main__":
    main()
