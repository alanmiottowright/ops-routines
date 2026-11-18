# Source at the top of every Bash call:  source rc-triage/rc.sh
# Credentials come from the cloud environment's variables. Never echo them.
: "${ROCKETCHAT_BASE_URL:?missing}" "${ROCKETCHAT_USER_ID:?missing}" "${ROCKETCHAT_AUTH_TOKEN:?missing}"
W="${W:-/tmp/rc-triage-$(TZ=America/New_York date +%F)}"; mkdir -p "$W"
rcapi() { curl -sS --max-time 20 -H "X-User-Id: $ROCKETCHAT_USER_ID" -H "X-Auth-Token: $ROCKETCHAT_AUTH_TOKEN" -H "Content-Type: application/json" "$@"; }
# rchist <t> <rid> <oldest-iso-or-empty>  -> unread room history (newest 30)
rchist() {
  case "$1" in c) ep=channels.history;; p) ep=groups.history;; d) ep=im.history;; *) return 2;; esac
  local q="roomId=$2&count=30"; [ -n "$3" ] && q="$q&oldest=$3"
  rcapi "$ROCKETCHAT_BASE_URL/api/v1/$ep?$q"
}
# rcthread <tmid>  -> thread messages (newest 30)
rcthread() { rcapi "$ROCKETCHAT_BASE_URL/api/v1/chat.getThreadMessages?tmid=$1&count=30&sort=%7B%22ts%22%3A-1%7D"; }
# rcread <rid>  -> mark a room read, threads included (the ONLY write allowed)
rcread() { rcapi -X POST "$ROCKETCHAT_BASE_URL/api/v1/subscriptions.read" -d "{\"rid\":\"$1\",\"readThreads\":true}"; }
