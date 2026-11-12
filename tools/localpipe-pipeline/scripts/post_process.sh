#!/usr/bin/env bash
# Post-processing for a completed engine run. Safe to re-run.
#
#   ./scripts/post_process.sh runs/<run-dir>
set -euo pipefail
cd "$(dirname "$0")/.."

RUN="${1:?usage: ./scripts/post_process.sh runs/<run-dir>}"
SRC="$RUN/results.csv"
[ -f "$SRC" ] || { echo "No results.csv in $RUN"; exit 1; }

echo "── franchise filter ─────────────────────────────────────"
python3 scripts/filter_franchises.py "$SRC" \
    --clean "$RUN/step1_independents.json" \
    --flagged "$RUN/rejected_franchises.json" --quiet

echo ""
echo "── reviews (free) ───────────────────────────────────────"
python3 scripts/fetch_reviews.py "$RUN/step1_independents.json" \
    --out "$RUN/step2_with_reviews.json"

echo ""
echo "── consumer inbox split ─────────────────────────────────"
python3 scripts/drop_consumer_email.py "$RUN/step2_with_reviews.json" \
    --business "$RUN/SEND_business_domains.csv" \
    --consumer "$RUN/HOLD_consumer_inboxes.csv" \
    --no-email "$RUN/rejected_no_email.json"

echo ""
echo "════════════════════════════════════════════════════════"
echo "Upload to PlusVibe:   $RUN/SEND_business_domains.csv"
echo "Do NOT upload:        HOLD_consumer_inboxes.csv (separate lane, own domains)"
echo ""
echo "Before upload — strip Localpipe's literal \"not found\" to empty, or"
echo "PlusVibe fallbacks will not fire and emails send as \"Hi not found,\"."
