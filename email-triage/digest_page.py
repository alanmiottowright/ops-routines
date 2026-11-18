#!/usr/bin/env python3
"""Render feeds/email-actions.json into a single self-contained HTML page (the triage digest artifact).
Usage: python3 email-triage/digest_page.py <YYYY-MM-DD> > /tmp/digest.html
Never put message bodies or reply wording in the feed; this page only shows the feed's one-liners."""
import json, sys, html
date = sys.argv[1] if len(sys.argv) > 1 else ""
items = json.load(open("feeds/email-actions.json"))
SECTIONS = [("my-action", "My action"), ("waiting", "Waiting on others"),
            ("elsewhere", "Actions in other systems"), ("stale", "Retired as stale")]
def link(it):
    t = it.get("thread_id")
    return f"https://mail.google.com/mail/u/0/#all/{t}" if t else ""
def row(it):
    e = html.escape
    key = e(it.get("thread_id") or it.get("subject", ""))
    meta = " · ".join(x for x in [e(it.get("who", "")), e(str(it.get("status", ""))),
        (f"{it['elapsed_bd']} bd" if "elapsed_bd" in it else ""),
        (f"due {e(it['due'])}" if it.get("due") else ""),
        (e(it["system"]) if it.get("system") else "")] if x)
    u = link(it)
    title = f'<a href="{u}" target="_blank" rel="noopener">{e(it.get("subject",""))}</a>' if u else e(it.get("subject", ""))
    return (f'<li><label><input type="checkbox" data-k="{key}"><span><b>{title}</b>'
            f'<small>{meta}</small><em>{e(it.get("ask",""))}</em></span></label></li>')
body = ""
for kind, name in SECTIONS:
    rows = [i for i in items if i.get("kind") == kind]
    if rows:
        body += f'<section><h2>{name} <span>{len(rows)}</span></h2><ul>' + "".join(map(row, rows)) + "</ul></section>"
if not body:
    body = "<p>Nothing needs you today.</p>"
print("""<title>Triage Digest</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{--bg:#f6f7f9;--fg:#1d2330;--mut:#5d6677;--card:#ffffff;--line:#dfe3ea;--acc:#2456c8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12161f;--fg:#e8ecf4;--mut:#99a3b8;--card:#1a2030;--line:#2b3347;--acc:#7da2ff;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12161f;--fg:#e8ecf4;--mut:#99a3b8;--card:#1a2030;--line:#2b3347;--acc:#7da2ff;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;padding-block:20px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:760px;margin:0 auto}
h1{font-size:22px;margin:0 0 2px}
.d{color:var(--mut);margin:0 0 18px}
h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin:22px 0 8px}
h2 span{background:var(--line);border-radius:10px;padding:0 7px;margin-left:4px}
ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
li{background:var(--card);border:1px solid var(--line);border-radius:8px}
label{display:flex;gap:12px;padding:12px;cursor:pointer;min-width:0}
input{margin-top:3px;width:18px;height:18px;flex:none}
span{display:flex;flex-direction:column;gap:2px;min-width:0}
small{color:var(--mut)}
em{font-style:normal}
a{color:var(--acc)}
input:checked+span{opacity:.45;text-decoration:line-through}
</style>
<main><h1>Triage digest</h1><p class="d">""" + html.escape(date) + """ · tap a title to open the thread in Gmail</p>""" + body + """</main>
<script>
document.querySelectorAll('input[data-k]').forEach(function(c){
  var k='td:'+c.dataset.k;
  try{c.checked=localStorage.getItem(k)==='1'}catch(e){}
  c.addEventListener('change',function(){try{localStorage.setItem(k,c.checked?'1':'0')}catch(e){}});
});
</script>""")
