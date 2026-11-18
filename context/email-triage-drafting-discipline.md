---
name: email-triage-drafting-discipline
description: "Email triage must NEVER create Gmail drafts — Alan writes his own replies; surface the open question in the report instead"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1633002a-2eed-40b8-a5b7-32fc1d21d465
  modified: 2026-07-29T12:41:39.705Z
---

For the [[email-triage]] scheduled task (and email work generally): **do not create, update, or send Gmail drafts. Ever.** Superseded the earlier "draft carefully" guidance on 2026-07-29 — Alan escalated from constraints to an outright ban.

Instead: apply the tracking label, surface the thread in the report, and state in one line what the open question is and who has it. Don't include suggested reply wording in the report either.

**Why:** Judging *which point in a long thread still needs a response* is unreliable in practice. Alan's words: "your ability to comprehend the right stage of a thread is not optimized and usually results in poor draft messages that I have to read and delete." Two years of failure modes confirmed it — draft to a Brex/Azul thread that had already closed; duplicate Polsinelli draft; stacked drafts on "Sam <> Alan Reconnect"; a PwC draft made moot when Caitlin and Alexandre continued the thread directly. Each guardrail added (no-dupes → OBE check → when-in-doubt-flag) still let bad drafts through. Net cost is negative: reading and deleting a wrong draft costs more than writing the reply fresh.

**One named exception, agreed 2026-09-01 — the `carta-monthly-snapshot` routine.** That task's STEP 6 creates a real Gmail draft each month to Guilherme Barbosa (Controller) at both `guilherme.barbosa@novagestao.digital` and `guilherme.barbosa.ext@rocket.chat`, carrying the derived close extract: share counts and note balances, no attachment, no stakeholder detail. Alan sends it. Alan approved this explicitly when the conflict was put to him.

**Why the exception holds and does not widen the hole:** the ban's reason is that judging *which point in a long thread* still needs a reply is unreliable. That failure mode is absent here — it is a fresh outbound email, on a fixed monthly cadence, with a payload the routine itself just generated and reconciled. There is no thread to misread. Any proposed draft that requires reading a conversation and deciding what it still needs is squarely under the ban, exception or not.

**How to apply:** Never call create_draft / update_draft in triage. Note that no delete_draft tool is exposed either — auto-drafts already sitting in the mailbox must be listed in the report for Alan to discard manually. See [[email-triage-tracker-design]] for the related tracker-signal rules.

**Second exception, 2026-11-06 — explicit per-request asks only.** In an interactive session, when Alan explicitly says "draft these replies directly in Gmail" (he did for the Alexia Ventures and Endeavor/Sam Foster Q3 replies), create the drafts, report the draft links, and leave sending to him. The ban still applies to scheduled/triage runs and to any draft nobody asked for. Don't treat one ask as standing permission.

**Third exception, 2026-11-18 — the triage self-digest draft.** Alan explicitly approved (his words: "Proceed with Option A and create this exception"): each [[email-triage]] run creates or updates exactly ONE draft addressed only to alan.wright@rocket.chat, subject prefix "[Triage digest]", listing My action / Waiting / Other systems / Stale items with a Gmail thread link per item. No reply wording, no third-party recipients, never sent by the routine. Why it holds: it is a self-addressed work list built from the already-verified tracker, with no thread to misread and no wrong draft to send. Any draft that is addressed to someone else or requires judging what a thread needs remains banned.
