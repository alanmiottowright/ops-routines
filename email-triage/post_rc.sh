#!/usr/bin/env bash
# Usage: email-triage/post_rc.sh <text-file>
# Posts the file's text to #amw-email-triage via the incoming webhook in $RC_WEBHOOK_URL.
# The webhook is bound to that channel; do not pass a channel override (it returns 403).
# Never prints the URL. Prints "ok" or "ERROR ...".
set -u
[ -n "${RC_WEBHOOK_URL:-}" ] || { echo "ERROR no RC_WEBHOOK_URL"; exit 1; }
[ -r "${1:-}" ] || { echo "ERROR no text file"; exit 1; }
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -X POST \
  -H 'Content-Type: application/json' \
  -d "$(jq -n --rawfile t "$1" '{text:$t}')" "$RC_WEBHOOK_URL")
[ "$code" = 200 ] && echo ok || echo "ERROR http $code"
