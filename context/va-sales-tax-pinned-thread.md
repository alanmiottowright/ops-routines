---
name: va-sales-tax-pinned-thread
description: "Pinned email thread — Virginia sales tax refund review with Baker Tilly; report STATUS every run (Guilherme owns it), never as Alan's action or as stale"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43586095-7980-46c3-a76e-0f9c467dfb20
  modified: 2026-08-18T23:20:49.819Z
---

The Virginia sales tax matter with Baker Tilly is a **pinned tracked thread**. Alan asked (18-Aug-2026) that it be closely and explicitly tracked on every routine email-triage run **until he confirms it is fully resolved**.

**Thread:** Gmail thread `19e74bdb2f07ce8d` — "rocket.chat - Virginia Sales Tax - Amend/Correct Prior Tax Filing Discussion". Started 29-May-2026, still live.

**Cast:** Anthony Truong (Anthony.Truong@bakertilly.com, doing the work) and Curtis Miyaji (Director, SALT — scoped the engagement) at Baker Tilly, with Todd Wood cc'd; Guilherme Barbosa (guilherme.barbosa.ext@rocket.chat, Controller) drives it on our side; Mayra Lima, Alexandre Naressi, Amanda Oliveira also on the thread.

**What it is:** amending/correcting prior Virginia sales tax filings to recover tax that was wrongly charged. Invoices are staged in a shared Drive folder ("Invoices Virginia") in three groups — 2025–2026, 2023–2024, and invoices identified as potentially having tax charged. Review runs **oldest first, starting with 2023**, because refund claims die on a **3-year statute window** — the 2023 claims are the ones at risk of expiring.

**How to track it — these override the normal tracker rules for this thread only:**

The pin means **report status, not treat as Alan's action**. Corrected 31-Aug-2026: the pin plus a truncated-search bug had the routine reporting this thread as Alan's own overdue item at "59 business days stale". It is nothing of the sort — it is a live, well-run workstream with ~57 messages, last active the previous business day, driven by Guilherme.

- Report it every run in "⏰ Follow-ups" even when nothing changed, as an **owned-by-Guilherme status line** carrying the REAL last-activity date, with who currently holds the ball.
- It must **never** be reported as Alan's action item, and never as stale or overdue. It carries `Needs My Action` for visibility only; it does **not** carry `Follow-up Due`.
- Do **not** clear it under the delegated / "owned by someone else" rule. Guilherme sends most messages and Alan is usually only Cc — keep reporting it anyway, and name Guilherme as the owner.
- Do **not** retire it under the 15-business-day stale rule. Age is not the signal here; a genuine gap in activity is.
- Get the last-activity date from `get_thread METADATA_ONLY` — on a thread this long, search output is truncated and will lie. See [[email-triage-tracker-design]].
- Only Alan closing it out ends the tracking. When he does, remove the labels and delete this memory.
- Related threads that are part of the same matter, worth watching for movement: "Rocket.chat SALT - Amended Indirect Tax Returns", the "Invoices Virginia" Drive share, and the Baker Tilly compliance-calendar thread.

Sits alongside [[email-triage-tracker-design]] and [[email-triage-drafting-discipline]] — still no drafts on this thread, just surface the open question.

**History note:** the 29-May–29-Jul-2026 portion of this thread had been sitting in Gmail's Trash (engagement scoping, Curtis's statute-of-limitations analysis, Alan's authorization to proceed). Restored 18-Aug-2026 at Alan's instruction. The connector's `untrash_thread` / `untrash_message` both return "caller does not have permission" — the working path is `unlabel_thread` removing the `TRASH` label. Use that if it happens again.
