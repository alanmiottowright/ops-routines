---
name: email-triage-tracker-design
description: "Design rules that keep the email-triage follow-up tracker meaningful — truncated search output, act-elsewhere notifications, stale retirement, no fake-unread, identity aliases"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5584b1e6-48ec-48df-a55a-f22bf9bcf068
  modified: 2026-07-29T12:41:57.738Z
---

Reviewed ~20 runs of the [[email-triage]] task on 2026-07-29 and rewrote the skill. The tracker had degraded into a graveyard: 21 threads labeled "Needs My Action", 21 labeled "Follow-up Due" — i.e. essentially everything tracked was permanently overdue, including items from Jan 2026 and Feb 2025. Four rules fix the signal:

1. **Act-elsewhere notifications get no tracking labels.** Drata, Zoho CRM/Expense/Sign, DocuSign/D4Sign, Google Docs comments, TeamGuide, Standard Metrics, Ipreo/IHS Markit, Insperity — the action happens in a portal, so no email reply will ever arrive to resolve them and they were immortal. They now go to a "🔔 Actions waiting in other systems" checklist (action / system / due date). Generalizes the existing Jira/Confluence rule.
2. **Retire stale items at 15 business days.** List once under "🗄 Stale — close or act", then strip the labels. An item that survived three weeks of nudges needs a decision, not another reminder.
3. **Bubbling must not re-apply UNREAD.** It added INBOX + UNREAD, so 4 of 7 "unread" inbox threads were old bubbles, not new mail — unread stopped meaning anything. Now INBOX only; the report carries the urgency.
4. **Define "me" explicitly.** Alan sends from alan.wright@, cfo@, legal@, orders.partners@, accounts.payable@, accounts.receivable@, contracts@rocketchat.com. Direction detection was ambiguous on alias-sent mail. Colleagues (Mayra, Gabriel, et al.) are NOT him — but a thread a colleague has taken over while Alan is only Cc is "delegated" and gets untracked with an owner named.

**5. Never judge a thread from `search_threads` output (added 31-Aug-2026 — the most consequential rule here).** `search_threads` truncates each thread's `messages` array at 5. The routine had been taking the last element as "the latest message", which silently INVERTS direction on any thread longer than five messages — i.e. on precisely the threads that matter. Measured on the 31-Aug-2026 run: of 6 tracked threads returning exactly 5 messages, **3 were reported wrong** — the NEA carve-out reported as Alan's overdue action when he had delivered 6 days earlier and NEA owed him three items; Solera INV4191 marked resolved and dropped when Alan wrote last; the Baker Tilly VA thread reported 59 business days stale when it had been active the previous business day. Fix: `search_threads` discovers candidate thread IDs ONLY; direction, latest sender and dates come from `get_thread METADATA_ONLY`, one call per tracked thread. A thread whose search message count equals the cap is presumed truncated.

**6. The arithmetic is deterministic, so code does it.** Business-day math, tier lookup and SLA comparison now run through `~/.claude/scheduled-tasks/email-triage/sla.py` (`--selftest` for its fixture). Doing ~20 threads of date math by hand in prose every run is where drift hides. Report the helper's `status` verbatim; disagree in the report rather than substituting a number silently.

**7. Verify, then report; surface failures rather than hiding them.** After mutations, re-query the three labels and assert membership matches intent, and open the report with a "🧪 Run integrity" line covering connector failures, retries and the verification result. Borrowed from Tomasz Tunguz's harness write-up: his measured error rate went 0% → 34% when the system stopped concealing failures. A tracker reporting "all good" while mis-deriving direction is worse than one reporting a fault. Rejected from that same write-up as inapplicable here: model/tier routing, redrive and dead-letter queues, auto-revert, and separate maker/verifier agents — the 31-Aug failures were bad input data, not bad judgment, so a second model reading the same truncated array would have agreed with the first.

**Why:** Alan reads this report once each morning. A tracker where every row is red, and where half the rows are portal notifications he can't action by email, has no signal.

**How to apply:** Report leads with "🔄 Since last run" (the delta) and keeps the unchanged overdue backlog compact — one line each, not full detail re-rendered every run. Cadence is now once daily 8 AM weekdays (`0 8 * * 1-5`), down from 8 AM + 4 PM; the second run rarely had new mail. Also two tool facts worth keeping: Gmail `search_threads` ignores label IDs (`label:Label_1` → empty) so query `label:"Waiting on Reply"` by display name, one label per query; and `get_thread` with FULL_CONTENT blows the token limit on long threads — use MINIMAL/METADATA_ONLY.

**2026-11-27 (Alan):** Virginia sales tax (Baker Tilly) thread 19e74bdb2f07ce8d closed out — labels removed, pin retired, no longer reported. **MD FAMLI registration** (thread 1a1c08ac0decedca, Mayra's "Action Required: Register with FAMLI") starred + unread + inbox; Alan wants it top priority on Mon 2026-11-30 — lead the report's "Needs me today" with it that day, then resume normal act-elsewhere handling.
