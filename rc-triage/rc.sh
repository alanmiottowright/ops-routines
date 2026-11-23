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

# ---- Briefing (the ONLY room this routine may post in) ----
BRIEF_RID="6b04a6111b0e8554851a02c0"   # dedicated daily-briefing channel (private group)
BRIEF_RID_OLD="W5YZAb7jeTroNAFvf"   # former briefing DM-to-self; still excluded from triage
# rclink <t> <room-name> <rid> <msg-id>  -> permalink to one message
rclink() {
  case "$1" in c) echo "$ROCKETCHAT_BASE_URL/channel/$2?msg=$4";; p) echo "$ROCKETCHAT_BASE_URL/group/$2?msg=$4";;
               *) echo "$ROCKETCHAT_BASE_URL/direct/$3?msg=$4";; esac
}
# rcpost <text-file> [tmid]  -> posts to the briefing DM only; prints the new message id
rcpost() {
  local body; body=$(jq -n --rawfile m "$1" --arg rid "$BRIEF_RID" --arg tmid "${2:-}" \
    '{message:({rid:$rid,msg:$m} + (if $tmid=="" then {} else {tmid:$tmid} end))}')
  rcapi -X POST "$ROCKETCHAT_BASE_URL/api/v1/chat.sendMessage" -d "$body" | jq -r 'if .success then .message._id else ("ERROR " + (.error//"unknown")) end'
}
