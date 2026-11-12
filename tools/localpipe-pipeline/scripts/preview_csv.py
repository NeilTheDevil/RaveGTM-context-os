#!/usr/bin/env python3
"""
Summarize a results.csv without opening it: hit rates, sample rows, and the
send-readiness split that decides what you can actually email.

    python3 scripts/preview_csv.py runs/<run>/results.csv
    python3 scripts/preview_csv.py runs/<run>/results.csv --sample 20
"""

import csv
import os
import sys
from collections import Counter


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def pct(n, d):
    return f"{n / d * 100:5.1f}%" if d else "    -"


def bar(n, d, width=28):
    filled = round(width * n / d) if d else 0
    return "█" * filled + "·" * (width - filled)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    path = args[0]
    sample_n = 8
    if "--sample" in sys.argv:
        sample_n = int(sys.argv[sys.argv.index("--sample") + 1])

    rows = load(path)
    if not rows:
        raise SystemExit(f"{path} has no data rows.")
    n = len(rows)
    cols = rows[0].keys()

    def has(row, col):
        return bool((row.get(col) or "").strip())

    print(f"\n  {os.path.basename(path)}  —  {n:,} rows\n")

    print("  COVERAGE")
    for col in ("owner_name", "owner_email", "owner_phone", "business_email",
                "website", "phone", "rating"):
        if col in cols:
            k = sum(1 for r in rows if has(r, col))
            print(f"    {col:16} {bar(k, n)} {k:6,} {pct(k, n)}")

    # What you can actually send to, and how confident you can be in it.
    if "owner_email" in cols:
        owner = sum(1 for r in rows if has(r, "owner_email"))
        biz_only = sum(1 for r in rows
                       if not has(r, "owner_email") and has(r, "business_email"))
        none = n - owner - biz_only
        print("\n  SEND-READINESS")
        print(f"    verified owner email   {owner:6,} {pct(owner, n)}   send now")
        print(f"    business email only    {biz_only:6,} {pct(biz_only, n)}   "
              f"VERIFY FIRST — unverified on credit plans")
        print(f"    no email               {none:6,} {pct(none, n)}   phone or skip")

    if "email_provider" in cols:
        prov = Counter((r.get("email_provider") or "").strip()
                       for r in rows if has(r, "email_provider"))
        if prov:
            top = ", ".join(f"{k} {v}" for k, v in prov.most_common(6))
            print(f"\n  EMAIL PROVIDERS   {top}")

    # 'not found' must never reach a CRM — the engine blanks it, so this is a tripwire.
    leaked = sum(1 for r in rows for v in r.values()
                 if (v or "").strip().lower() == "not found")
    if leaked:
        print(f"\n  !! {leaked} cell(s) contain the literal string 'not found' — do not import")
    else:
        print("\n  OK  no 'not found' strings — safe to import")

    best = [r for r in rows if has(r, "owner_name") and has(r, "owner_email")][:sample_n]
    if best:
        print(f"\n  SAMPLE (owner name + verified email)\n")
        w = max(len(r.get("business_name", "")[:30]) for r in best)
        for r in best:
            print(f"    {r.get('business_name','')[:30]:{w}}  "
                  f"{r.get('owner_name','')[:20]:20}  {r.get('owner_email','')[:34]}")
    print()


if __name__ == "__main__":
    main()
