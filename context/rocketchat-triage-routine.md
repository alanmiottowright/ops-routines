---
name: rocketchat-triage-routine
description: How Alan wants Rocket.Chat unread messages triaged (email-triage style) via the rocketchat-rocketchat skill
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6dbd17f7-e8fd-47db-9a18-b5faa9b2597a
  modified: 2026-08-12T16:41:39.751Z
---

Alan runs a periodic Rocket.Chat unread triage "like the email triage routine" using the `/rocketchat-rocketchat` skill. Established Aug 2026.

**Why:** He's COO and wants only things needing his action/attention left unread; everything else cleared. Mirrors his aggressive email/Google-doc triage style — see [[google-doc-notification-triage]], [[email-triage-tracker-design]].

**How to apply:**
- Access: skill CLI at `~/.agents/plugins/rocketchat-skills/tools/clis/rocketchat.js` (NOT the `~/.claude/skills/...` path). Creds in `~/.agents/plugins/rocketchat-skills/.env` (keys are prefixed: `ROCKETCHAT_BASE_URL`=https://open.rocket.chat, `ROCKETCHAT_USER_ID` 17-char, `ROCKETCHAT_AUTH_TOKEN` ~43-char PAT — sourcing the file and reading bare `BASE_URL`/`USER_ID`/`AUTH_TOKEN` fails). Personal Access Token needs "Ignore 2FA" ticked (he uses Authy).
- **Detect unread correctly (critical):** the subscription `unread` *counter* under-reports badly. The RELIABLE unread set = any subscription where `alert==true` OR `unread>0` OR `tunread/tunreadUser/tunreadGroup` non-empty (UNREAD THREADS — easy to miss) OR `userMentions>0`. Do NOT rely on `lm>ls`, and do NOT date-filter for reconciliation — the app's Unread list ignores age, so old/stale alerts (some `ls` years old) still show. First attempt missed thread-only rooms + pre-window rooms; user's app showed 12+ still unread.
- **ALWAYS verify after marking read:** re-fetch subscriptions.get and confirm the unread-signal set shrank to exactly the intended keep-set. Marking read uses `POST subscriptions.read {"rid":..,"readThreads":true}` (readThreads clears unread threads too).
- **zsh gotcha:** `for x in $VAR` does NOT word-split in zsh → fires one bad call. Use `printf '%s\n' a b c | while read -r x` or `${=VAR}`. A False/garbage result is silent; the verify step catches it.
- CLI is read-only + Cloudflare blocks python-urllib UA → use `curl` for raw API. History endpoints: channels.history / groups.history / im.history with `oldest=<ls>`.
- **Triage rule:** LEAVE UNREAD only rooms with a direct `@alan.wright` ask/approval. HOLD (leave unread + ask) a small set of strategically significant rooms with no direct ask (pricing/margin, cost anomalies, comp, strategic initiatives). MARK READ everything else (bots, lead/deal alerts, kudos, eng/support ops, status posts).
- **Marking read is a state change** — he pre-authorized auto-marking *pure-FYI* rooms only, via raw `POST /api/v1/subscriptions.read {"rid":...}`. Read-state is per-room, not per-message. Confirm before clearing the "held/significant" set.
- Deliver a scannable COO report: Action / Held-for-review / Personal DM / Marked-read digest + 1-2 awareness one-liners.
