#!/usr/bin/env bash
# Rave lead pipeline — vendored LocalPipe engine + Rave's three filters.
#
#   ./scripts/pipeline.sh jobs/<job>.json
#
# The engine handles scrape, enrich, batching, retries, pagination and resume.
# Everything after it is Rave-specific and lives in scripts/.
#
# Order matters: franchises are cut BEFORE enrichment spend where possible, and
# reviews are free so they cost nothing wherever they run.
set -euo pipefail
cd "$(dirname "$0")/.."

JOB="${1:?usage: ./scripts/pipeline.sh jobs/<job>.json}"
SLUG="$(basename "$JOB" .json)"

echo "── 1/5  plan ────────────────────────────────────────────"
python3 engine/lp.py plan "$JOB"
echo ""
read -r -p "Credits above are your money. Launch? [y/N] " ok
[ "$ok" = "y" ] || { echo "aborted"; exit 0; }

echo ""
echo "── 2/5  run (detached) ──────────────────────────────────"
python3 engine/lp.py run "$JOB" --detach
echo "Poll with:  python3 engine/lp.py status"
echo "Then re-run this script with --post <run_dir> to finish the filters."
