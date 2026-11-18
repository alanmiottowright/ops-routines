/**
 * Relay for the email-triage digest. Paste into script.google.com while signed in as the mailbox owner.
 * The cloud routine can only create a draft; this sends it so it arrives as a normal inbox email.
 * Safety: sends ONLY a draft whose subject starts "[Triage digest]" addressed solely to you (no cc/bcc).
 * Setup: Triggers > Add trigger > sendTriageDigest > Time-driven > Day timer, ~15 min after the routine
 * (routine fires 13:00 UTC). Weekend runs find no draft and do nothing. Authorize Gmail scope on first run.
 */
function sendTriageDigest() {
  var me = Session.getEffectiveUser().getEmail().toLowerCase();
  var drafts = GmailApp.getDrafts();
  for (var i = 0; i < drafts.length; i++) {
    var m = drafts[i].getMessage();
    if (m.getSubject().indexOf('[Triage digest]') !== 0) continue;
    var to = m.getTo().toLowerCase();
    if (to.indexOf(me) === -1 || to.indexOf(',') !== -1) continue;
    if (m.getCc() || m.getBcc()) continue;
    drafts[i].send();
  }
}
