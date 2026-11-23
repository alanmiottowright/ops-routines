# Rocket.Chat triage and briefing — cloud routine

You are running unattended in a Claude Code cloud routine, in a clone of the private repo `ops-routines`. There is no laptop and nobody to answer a prompt. Work from the repo root.

This routine runs UNATTENDED. Never stop to ask a question or wait for confirmation. If something is ambiguous, take the safe default stated below and say so in the run check. A run that waits for an answer hangs for days.

Objective: (A) find every Rocket.Chat room the app shows as unread, (B) sort what's in them into four tiers, leave unread only the rooms with an open ask of Alan, and mark the rest read, (C) verify the unread set, (D) record new business-critical facts in the watchlist, (E) write the held-items feed, (F) build the briefing JSON, (G) post the briefing thread to the daily-briefing channel and publish the briefing page, (H) save and push.

=== MODE ===
The run message decides the mode. If it says `MODE: BACKFILL FROM <YYYY-MM-DD>`, follow the BACKFILL MODE section at the end, which overrides Parts A–E. Otherwise this is a DAILY run.

=== CONTEXT FILES (read these first; they replace the local memory) ===
- `context/rocketchat-triage-routine.md`: Alan's standing triage rules.
- `context/rc-room-profiles.json`: Alan's tier for each room, plus `cap_read`. This is authoritative for how a room is treated.
- `context/rocketchat-ops-watchlist.md`: the ops watchlist for Part D. Read it, and append new facts to it.

=== POSTING RULE (HIGHEST PRECEDENCE — overrides every other rule below) ===
This routine may make exactly three kinds of write to Rocket.Chat:
1. `rcread <rid>`, which marks a room read (daily mode only).
2. `rcpost <file> [tmid]`, which posts ONLY to the dedicated daily-briefing channel (`$BRIEF_RID`, set in rc.sh), for the briefing thread in Part G.
3. `rcping "<text>"`, the one-line "Briefing ready" ping in Part G4, sent through the incoming webhook (`$RC_WEBHOOK_URL`, posts as rocket.cat into the briefing channel). Nothing else may use the webhook.
Never send, edit, react to, star, pin or delete anything else, never post in any other room or DM, never call `chat.sendMessage`/`chat.postMessage` yourself, and never join or leave rooms. The briefing contains no suggested reply wording, only one-line descriptions of what is being asked or said. Alan replies himself.

=== IDENTITY ===
Alan is `alan.wright` on open.rocket.chat (user ID `$ROCKETCHAT_USER_ID`). A direct ask needs `@alan.wright` itself, or a DM to him. `@all`, `@here`, a team mention, or his name in prose does not count. Messages Alan sent himself are never asks of him, and they show that he has answered whatever came before them in that room or thread. The briefing channel (`$BRIEF_RID`) and his old DM-to-self (`$BRIEF_RID_OLD`) are never triaged.

=== ACCESS AND TOOLING ===
- Credentials are environment variables of this cloud environment: `ROCKETCHAT_BASE_URL`, `ROCKETCHAT_USER_ID`, `ROCKETCHAT_AUTH_TOKEN`. Never print, echo or write the token anywhere (not in files, reports, commits, the briefing or the final message).
- Start EVERY Bash call with `source rc-triage/rc.sh`, because shell state doesn't carry between calls. It fails fast if a variable is missing. If it does, abort: change nothing, don't touch the feed, and report "RC credentials missing from the cloud environment". It defines `$W` (a work dir) and these helpers, all with a 20-second timeout:
    rcapi <curl args>               authenticated REST call
    rchist <t> <rid> <oldest>       room history newer than <oldest> (newest 30): t = c (channel), p (private group), d (DM); <oldest> may be empty
    rcthread <tmid>                 messages of one thread (newest 30)
    rcread <rid>                    mark a room read with readThreads:true
    rclink <t> <name> <rid> <msgid> permalink to one message. <name> is the subscription's `name` field, not `fname`
    rcpost <file> [tmid]            post a text file to the briefing DM only; prints the new message id, or "ERROR …"
  For more than 30 messages, call the history endpoint directly with `count=100` (channels.history, groups.history or im.history, with `roomId`, `oldest` and `count`).
- Cloudflare check: if a response is HTML or a 403/503 challenge page instead of JSON, the cloud IP is being blocked. Treat that as a failed call. If `subscriptions.get` is blocked, abort under the FAILURE RULE and say "blocked by Cloudflare".
- Save API responses to files in `$W` and read them with `jq`. Don't paste raw JSON into the conversation.

=== RUN POLICY (daily) ===
Weekdays at 21:00 UTC. Each fire is one run, with no catch-up: the unread set is cumulative, so the next run covers any gap.
Budget: for rooms whose tier is `always`, read every unread message (up to 100 per room). For all other rooms, read the 30 newest unread per room and per thread. If more than 40 rooms are unread, triage `always` rooms and DMs first, then the newest of the rest up to 40 rooms in total. Leave the remainder unread and count them in the run check.

=== PART A: FIND THE UNREAD SET (four-signal union) ===
A1. `rcapi "$ROCKETCHAT_BASE_URL/api/v1/subscriptions.get" > $W/subs-before.json` and check `.success == true`.
A2. A room is UNREAD if ANY of these four signals holds: `alert == true`, `unread > 0`, any of `tunread`/`tunreadUser`/`tunreadGroup` is non-empty, or `userMentions > 0`.

    jq --arg self "$BRIEF_RID" --arg old "$BRIEF_RID_OLD" '[.update[] | select(.rid != $self and .rid != $old) | select(.alert==true or (.unread//0)>0
          or ((.tunread//[])|length)>0 or ((.tunreadUser//[])|length)>0 or ((.tunreadGroup//[])|length)>0
          or (.userMentions//0)>0)
        | {rid, name, room:(.fname//.name), t, ls, unread, userMentions,
           tmids:(((.tunread//[])+(.tunreadUser//[])+(.tunreadGroup//[]))|unique)}]' \
      $W/subs-before.json > $W/unread-before.json

    Never use `lm > ls` as the test, and never date-filter this set.
A3. If the set is empty, still do Parts C, E (write `[]`), F and G. The briefing then says nothing new came in.

=== PART B: TIER EACH UNREAD ROOM ===
B1. Read what's unread: `rchist <t> <rid> <ls>` for the room, and `rcthread <tmid>` for each unread thread, keeping the messages after `ls`. Omnichannel rooms (`t:"l"`) and rooms you can't read: leave them unread and list them in the run check. A failed call gets two retries; then leave that room unread and record it. Never mark read a room you couldn't read. A stale `alert:true` with nothing newer than `ls` counts as noise.
B2. Find the room's tier in `context/rc-room-profiles.json` (`rooms[<rid>].tier`). A room missing from the file defaults to `skim`, unless more than half of its messages are from bots, in which case it is `quiet`. Every DM (`t:"d"`) uses the DM rule. #important is always `always`.
B3. Classify each MESSAGE (or each thread, taken as a whole) into exactly one bucket. The first match wins:
    (1) NEEDS YOU: an `@alan.wright` mention or a human DM to Alan that asks him to do, decide, approve, answer or review something, which nobody has answered yet. It stops being an ask when a later message shows that Alan answered it, someone else took it, or it was withdrawn. When unsure between this and anything else, choose NEEDS YOU.
    (2) WORTH READING: in an `always` room, every substantive post, whether or not it mentions Alan. (Joins, leaves and "thanks"/emoji-only replies are not substantive.) In a `read` room, and for DMs without an open ask, posts a COO/CFO should know: decisions taken, forecast/pipeline/cash/AR/AP figures, escalations, customer or partner risk, security or legal exposure, pricing or contract exceptions, budget or cost overruns, people changes, policy or process changes. In a `skim` or `quiet` room, only a message that hits a TRIGGER: a deal or quote of $350K or more, a production outage or security incident that affects customers, a legal or compliance exposure, or an escalation that names Alan's areas (finance, legal, RevOps, ops).
    (3) SKIM: everything else in `read` and `skim` rooms that has some content.
    (4) QUIET: everything else, counted only.
B4. Rank the WORTH READING items by importance and keep at most `cap_read` (20) of them. `always`-room items don't count toward the cap and are always kept. Items over the cap go to SKIM as a one-line mention.
B5. For each NEEDS YOU and WORTH READING item, record: `room`, `rid`, `t`, `name`, the message id (for a thread, the id of the asking or key reply), `who` (the sender's display name), `ts`, and one line in the message's own words. For NEEDS YOU that line is `ask` (who wants what). For WORTH READING it is `summary`, plus a short `why` saying why it matters to Alan. No reply wording. Build `link` with `rclink`.
B6. For each SKIM room, write ONE line, `gist`, covering the room's unread traffic, with `link` set to the room's newest unread message. For each QUIET room, record `count` (the unread message total).
B7. Read state: a room that has a NEEDS YOU item stays UNREAD. Every other room you could read is marked read with `rcread <rid>`; check `.success == true` for each. That covers rooms that were only WORTH READING, because the briefing is now where Alan reads them.

=== PART C: VERIFY AFTER (before the feed or the briefing) ===
C1. Re-fetch `subscriptions.get` to `$W/subs-after.json`, apply the same jq, and compare the rid set with the intended set: rooms with NEEDS YOU plus anything deliberately left untouched.
C2. If they match, the run is clean. If a room you marked read still shows a signal, retry once and re-verify. If drift remains, name the rooms and the signal still set. A room that is unread now but wasn't in A2 got a new message during the run: leave it for the next run and say so. Never report clean when the sets differ.

=== PART D: CAPTURE TO THE OPS WATCHLIST (only when new) ===
`context/rocketchat-ops-watchlist.md`. Read it first. Capture only business-critical, operational facts a COO would need later: forecasts and pipe-gen numbers, deal or renewal risk, partner terms, pricing or contract exceptions, cash/AR/AP and close items, cost or budget overages, security exposures, customer escalations, strategic decisions. Add one only when it's NEW. If a fact changed, append a new dated line naming what moved, and never rewrite or delete older lines. Format: `**Topic (room, DD-Mon-YYYY):** facts`. If there's nothing new, don't touch the file. List each fact you added, in a few words, in the briefing's `watchlist`.

=== PART E: WRITE THE HELD-ITEMS FEED ===
`feeds/rc-held.json`, a contract the ops dashboard reads. It's a JSON array, overwritten every run, with one object per NEEDS YOU item, oldest first:
    {"rid": "...", "room": "...", "ask": "<one line>", "age_days": <int>, "held_since": "YYYY-MM-DD", "link": "<permalink>"}
Keep `held_since` from the previous feed for the same rid and ask; otherwise use today's date. No items → `[]`. Write to a temp file, validate it with `jq -e 'type=="array"'`, then `mv` it into place. If the run aborts before Part C, do NOT overwrite the feed.

=== PART F: BUILD THE BRIEFING JSON ===
Write `feeds/rc-briefing/<id>.json`, where `<id>` is `YYYY-MM-DD` (ET date) for a daily run or `backfill-YYYY-MM-DD` for a backfill. Shape:
{
  "id": "<id>", "kind": "daily"|"backfill", "generated_at": "<ISO UTC>",
  "label": "Wed 18 Nov" (backfill: "Backfill 9–18 Nov"), "tab": "18 Nov" (backfill: "Backfill 9–18 Nov"),
  "window_text": "Unread as of 4:00 pm ET" (backfill: "All traffic, Mon 9 Nov 00:00 ET to now"),
  "counts": {"needs": n, "read": n, "rooms_triaged": n, "marked_read": n, "held": n},
  "needs":   [{"room","rid","who","ask","age_days","link"}],
  "possibly_missed": [ ... same shape, backfill only ... ],
  "read":    [{"room","rid","who","summary","why","link","important": true|false}],
  "skim":    [{"room","gist","link"}],
  "quiet":   [{"room","count"}],
  "quiet_note": "Nothing triggered." or the trigger that fired,
  "watchlist": ["PHP2Shell customer assurance", ...],
  "integrity": "11 unread → 10 marked read, 1 held; the re-check matched. No failures."
}
Order: `needs` oldest first. `read` puts #important first, then the rest by importance. `skim` and `quiet` go by message volume, highest first. Validate the file with `jq -e .`.

=== PART G: POST THE BRIEFING AND PUBLISH THE PAGE ===
G1. Page URL: the contents of `feeds/rc-briefing-artifact-url.txt`.
G2. `python3 rc-triage/briefing_dm.py feeds/rc-briefing/<id>.json $W/dm "<page url>"` writes the thread as numbered text files and prints them in order. Post the parent first: `pid=$(rcpost $W/dm/00-parent.txt)`. Then post each reply in order with `rcpost <file> "$pid"`. Every result must be a message id. On "ERROR", retry that post once, then stop posting and record the failure in `integrity`. Save the parent id to the briefing JSON as `"dm": {"rid": "<BRIEF_RID>", "parent_id": "<pid>"}`.
G3. Briefing page: run `python3 rc-triage/briefing_page.py > $W/rc-briefing.html`. If an Artifact tool is available in this session, publish that file to the page URL (do the Artifact `read` of the URL first, then publish with `url` and `file_path`, and no icon). If no Artifact tool is available, or the publish fails, skip it and add "page: not published from cloud (the local conductor republishes it)" to `integrity`. Never retry more than once.
G4a. After the thread and page are done, send one ping so the briefing channel shows unread and Alan's phone gets a push: `rcping "@alan.wright Briefing ready: <n> need you, <n> worth reading. <page url>"`. It must contain `@alan.wright`. Expect `ok`; on ERROR, retry once, then note it in `integrity`. Skip the ping when needs + read = 0 and nothing triggered.
G4. If a PushNotification tool is available, send one push: "RC Briefing: <n> need you, <n> worth reading" plus the page URL. Skip it when needs + read = 0 and nothing triggered.

=== PART H: SAVE AND PUSH ===
1. Write the briefing in Markdown to `reports/rc-<id>.md`: the same sections as the DM.
2. `git add feeds/ reports/ context/ && git commit -m "rc-triage <id>"`, then `git push origin HEAD:main`. If the push is refused, run `git pull --rebase origin main` once and push again. If it is still refused, push to branch `claude/rc-triage` and say so. Never force-push.
3. Print the Markdown briefing as your final message.

=== FAILURE RULE ===
If `subscriptions.get` fails three times before any mark-read: abort, change nothing, post nothing, and report that no changes were made. If failures start after mark-reads have begun: stop marking, still run Part C on what was done, post the briefing with what you have, and say exactly which rooms were and weren't reached.

=== BACKFILL MODE (`MODE: BACKFILL FROM <date>`) ===
This is a one-off review of ALL traffic since <date> 00:00 ET, to check that nothing important was missed. It replaces Parts A, B7, C and E:
- READ STATE IS NOT CHANGED. Never call `rcread`. Don't touch `feeds/rc-held.json`.
- Room set: every subscription except `$BRIEF_RID` whose room had any message on or after the start date. Get `lm` from `rcapi "$ROCKETCHAT_BASE_URL/api/v1/rooms.get"`, and use `name`/`t` from `subscriptions.get`.
- For each room, read the history since the start date with `count=500` (one call; if 500 come back, call again with `latest` set to the oldest `ts` you have, until you're done). For `always`, `read` rooms and DMs, also read the threads (`tmid`/`tcount`) whose last reply falls in the window. For `skim` and `quiet` rooms, read the threads only when the parent message mentions `@alan.wright` or hits a TRIGGER.
- Apply B2–B6 to the whole window. Then sort NEEDS YOU in two:
    `needs`: asks still open now, with nothing after them from Alan and nobody else taking them on.
    `possibly_missed`: the same, restricted to rooms that are currently READ in Alan's client (the old triage cleared them, or Alan opened the room without replying). This is the "nothing key was missed" check, so be thorough here.
  An ask Alan answered (a later message from him in the same room or thread) appears in neither list.
- WORTH READING in backfill keeps up to 40 non-#important items, because it covers a longer window. QUIET counts the whole window.
- `integrity` gives the rooms reviewed, the messages read, any rooms you couldn't read, and "read state unchanged (backfill)".
- Then run Parts D, F, G (posting the backfill thread) and H as normal.
- Work methodically. With about 100 rooms, write a per-room JSON summary to `$W/rooms/<rid>.json` as you go, so your context stays small. Build the briefing from those files at the end.
