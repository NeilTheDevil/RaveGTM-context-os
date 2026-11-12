#!/usr/bin/env python3
"""
Split leads by recipient mailbox type.

Sending to consumer inboxes (@gmail, @yahoo, @outlook...) burns cold-email
infrastructure 3-5x faster: consumer spam filters are stricter, and warmup pools
contain no consumer accounts, so every send looks cold no matter how long you warmed.

This is NOT the same as choosing business_email over owner_email. For small trades
the LISTED business email is frequently already a Gmail (owner@gmail.com).
The only reliable test is the address domain itself.

Consequence for sending limits:
    consumer dropped   -> 15/inbox/day is available (Workspace baseline)
    consumer mixed in  -> throttle to 20-30% of normal, or isolate on separate domains

Usage:
    python3 scripts/drop_consumer_email.py leads.json \
        --business business.json --consumer consumer.json
"""
import argparse, csv, json, sys

CONSUMER_DOMAINS = {
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.co.uk", "ymail.com",
    "hotmail.com", "hotmail.co.uk", "outlook.com", "live.com", "msn.com",
    "aol.com", "icloud.com", "me.com", "mac.com", "protonmail.com", "proton.me",
    "gmx.com", "gmx.net", "mail.com", "zoho.com", "yandex.com", "comcast.net",
    "verizon.net", "att.net", "sbcglobal.net", "bellsouth.net", "cox.net",
    "charter.net", "earthlink.net", "roadrunner.com", "rr.com", "juno.com",
}

EMAIL_FIELDS = ("business_email", "owner_email", "email", "Email")


def address_of(row):
    for f in EMAIL_FIELDS:
        v = (row.get(f) or "").strip().lower()
        if v and v != "not found" and "@" in v:
            return v
    return ""


def is_consumer(row):
    """Address domain is authoritative. email_provider is a weaker secondary hint."""
    addr = address_of(row)
    if not addr:
        return None                      # no address at all — neither bucket
    domain = addr.rsplit("@", 1)[-1]
    if domain in CONSUMER_DOMAINS:
        return True
    # Secondary: Localpipe classifies the provider. 'google' on a custom domain
    # means Google Workspace, which is fine — only flag it on a known consumer host.
    return False


def load(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    d = json.load(open(path, encoding="utf-8"))
    return d if isinstance(d, list) else (d.get("data") or d.get("results") or [])


def save(rows, path):
    if not path:
        return
    if path.endswith(".csv"):
        if not rows:
            open(path, "w").close()
            return
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader(); w.writerows(rows)
    else:
        json.dump(rows, open(path, "w", encoding="utf-8"), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--business", help="write business-domain leads here (send to these)")
    ap.add_argument("--consumer", help="write consumer-inbox leads here (separate lane)")
    ap.add_argument("--no-email", help="write leads with no usable address here")
    a = ap.parse_args()

    rows = load(a.input)
    biz, cons, none_ = [], [], []
    for r in rows:
        verdict = is_consumer(r)
        (none_ if verdict is None else cons if verdict else biz).append(r)

    total = len(rows) or 1
    print(f"total            {len(rows)}")
    print(f"business domain  {len(biz)}  ({len(biz)/total*100:.0f}%)   <- safe at 15/inbox/day")
    print(f"consumer inbox   {len(cons)}  ({len(cons)/total*100:.0f}%)   <- separate lane or drop")
    print(f"no address       {len(none_)}  ({len(none_)/total*100:.0f}%)")

    save(biz, a.business); save(cons, a.consumer); save(none_, a.no_email)
    if a.business:
        print(f"\nwrote {a.business}")
    if cons and not a.consumer:
        print("\nNOTE: consumer leads were not written anywhere — they are excluded.")


if __name__ == "__main__":
    main()
