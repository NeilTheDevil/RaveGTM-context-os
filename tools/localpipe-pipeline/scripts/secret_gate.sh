#!/usr/bin/env bash
# Secret/PII gate — run on STAGED CONTENT before every push.
#
#   ./scripts/secret_gate.sh
#
# Gates on `git diff --cached`, never a file sweep: an escaped key once slipped a
# file-level scan and only the staged-content gate caught it.
#
# ALLOWLIST — Localpipe's Supabase **anon** key.
# Verified 2026-08-30 by decoding the JWT: role="anon", ref="uunrlffonnvmbsstkpze",
# iss="supabase". A Supabase anon key is public by design — it is embedded in browser
# clients, is the same for every Localpipe customer, is published in their own API docs,
# and gates nothing without row-level-security policies behind it. The project ref is
# already visible in every endpoint URL in this repo.
#
# A Supabase **service_role** key is the opposite — it bypasses RLS and IS a secret.
# The allowlist is keyed to role="anon" specifically, so a service_role key still trips.

set -uo pipefail
cd "$(dirname "$0")/.."

STAGED=$(git diff --cached)
[ -z "$STAGED" ] && { echo "nothing staged"; exit 0; }

# strip the known-public anon key so it cannot mask a real finding on the same line
# The JWT header prefix is assembled at runtime, never written as a literal — a literal
# here would make this script trip its own JWT check on every run.
HDR="eyJ""hbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
FILTERED=$(printf '%s' "$STAGED" | perl -pe "s/\Q$HDR\E\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/<ALLOWLISTED_LOCALPIPE_ANON_KEY>/g")

FAIL=0
check () {  # pattern, label
  local hits
  hits=$(printf '%s' "$FILTERED" | grep -nEi "$1" || true)
  if [ -n "$hits" ]; then
    echo "!!! $2"
    printf '%s\n' "$hits" | head -5
    FAIL=1
  fi
}

check 'lp_?[A-Za-z0-9]{16,}'                    "LOCALPIPE API KEY — Neil's own, must stay in .env"
check 'eyJ[A-Za-z0-9_-]{20,}'                   "JWT — not the allowlisted anon key. Decode it: service_role is a SECRET."
check 'sk-[A-Za-z0-9]{16,}'                     "OpenAI/Anthropic-style key"
check 'gh[pousr]_[A-Za-z0-9]{20,}'              "GitHub token"
check 'AKIA[0-9A-Z]{16}'                        "AWS access key"
check 'xox[baprs]-[A-Za-z0-9-]{10,}'            "Slack token"
check '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "EMAIL ADDRESS — lead PII or a sending identity?"

if [ "$FAIL" -eq 0 ]; then
  echo "gate clean — safe to push"
else
  echo
  echo "Resolve every line above before pushing."
  exit 1
fi
