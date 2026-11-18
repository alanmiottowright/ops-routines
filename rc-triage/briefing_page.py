#!/usr/bin/env python3
"""Render the RC Briefing page from feeds/rc-briefing/*.json (newest 14) into one self-contained HTML file.
Usage: python3 rc-triage/briefing_page.py > /tmp/rc-briefing.html
Shows only the briefing one-liners and links, never full message bodies."""
import glob, html, json, os
files = sorted(glob.glob("feeds/rc-briefing/*.json"), key=os.path.getmtime)
briefs = []
for f in files:
    try: briefs.append(json.load(open(f)))
    except Exception: pass
briefs = sorted(briefs, key=lambda b: b.get("generated_at", ""), reverse=True)[:14]
e = lambda s: html.escape(str(s or ""))
def item(i, kind, key):
    title = f'<a href="{e(i["link"])}" target="_blank" rel="noopener">{e(i["room"])}</a>' if i.get("link") else e(i["room"])
    body = {"needs": lambda: e(i.get("ask")), "missed": lambda: e(i.get("ask")),
            "read": lambda: e(i.get("summary")) + (f'<small>Why: {e(i["why"])}</small>' if i.get("why") else ""),
            "skim": lambda: e(i.get("gist"))}[kind]()
    meta = " · ".join(x for x in [e(i.get("who")), (f'{i["age_days"]}d' if i.get("age_days") is not None else ""),
                                  ("#important" if i.get("important") else "")] if x)
    btn = f'<a class="btn" href="{e(i["link"])}" target="_blank" rel="noopener">Open in RC</a>' if i.get("link") else ""
    return (f'<li class="it"><input type="checkbox" data-k="{e(key)}" aria-label="Done"><div class="tx"><b>{title}</b>'
            f'{f"<span class=meta>{meta}</span>" if meta else ""}<p>{body}</p></div>{btn}</li>')
def section(b, kind, label, cls, rows):
    if not rows: return ""
    lis = "".join(item(i, kind, f'{b["id"]}:{kind}:{n}') for n, i in enumerate(rows))
    return f'<section><h3><span class="pill {cls}">{label}</span><span class="n">{len(rows)}</span></h3><ul>{lis}</ul></section>'
panels, tabs = [], []
for n, b in enumerate(briefs):
    c = b.get("counts", {})
    tabs.append(f'<button type="button" class="tab" data-t="{n}" aria-pressed="{str(n==0).lower()}">{e(b.get("tab") or b.get("label"))}</button>')
    stats = "".join(f'<div><b>{v}</b><small>{l}</small></div>' for v, l in [
        (c.get("needs", 0), "need you"), (len(b.get("possibly_missed", [])), "possibly missed"),
        (c.get("read", 0), "worth reading"), (len(b.get("skim", [])), "rooms to skim"),
        (sum(q.get("count", 0) for q in b.get("quiet", [])), "filtered messages")] if not (l == "possibly missed" and not v))
    quiet = ""
    if b.get("quiet"):
        quiet = ('<section><h3><span class="pill quiet">On call / noise</span></h3><p class="q">' +
                 " · ".join(f'{e(q["room"])} {q["count"]}' for q in b["quiet"]) +
                 (f'. {e(b["quiet_note"])}' if b.get("quiet_note") else "") + "</p></section>")
    wl = ("<section><h3><span class=\"pill skim\">Watchlist</span></h3><ul class=\"plain\">" +
          "".join(f"<li>{e(w)}</li>" for w in b["watchlist"]) + "</ul></section>") if b.get("watchlist") else ""
    body = (section(b, "needs", "Needs you", "act", b.get("needs", [])) +
            section(b, "missed", "Possibly missed", "act", b.get("possibly_missed", [])) +
            section(b, "read", "Worth reading", "read", b.get("read", [])) +
            section(b, "skim", "Skim", "skim", b.get("skim", [])) + quiet + wl)
    panels.append(f'<article data-p="{n}"{"" if n==0 else " hidden"}><header><h2>{e(b.get("label"))}</h2>'
                  f'<p class="sub">{e(b.get("window_text",""))}</p></header><div class="stats">{stats}</div>{body}'
                  f'<p class="integ">{e(b.get("integrity",""))}</p></article>')
if not briefs:
    panels.append('<article><p class="sub">No briefings yet. The first one appears after the next RC triage run.</p></article>')
print("""<title>RC Briefing</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600&display=swap">
<style>
/* Layout: one reading column; date tabs, a stat strip, then one list per tier */
:root{--bg:#f5f6f8;--fg:#1f2329;--mut:#5f6673;--line:#dde1e7;--card:#fff;--link:#1d74f5;--act:#d4283f;--read:#1d74f5;--skim:#5b6472;--quiet:#8a919c;
--ff:"Inter",system-ui,-apple-system,sans-serif;--fh:"Space Grotesk","Inter",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14171c;--fg:#e7e9ee;--mut:#9aa2b1;--line:#2a3039;--card:#1b1f26;--link:#6aa6ff;--act:#ff6b7f;--read:#6aa6ff;--skim:#a0a7b4;--quiet:#737b88;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14171c;--fg:#e7e9ee;--mut:#9aa2b1;--line:#2a3039;--card:#1b1f26;--link:#6aa6ff;--act:#ff6b7f;--read:#6aa6ff;--skim:#a0a7b4;--quiet:#737b88;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.5 var(--ff);padding-block:22px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
h1,h2,h3{font-family:var(--fh);margin:0;text-wrap:balance} h1{font-size:24px} h2{font-size:19px}
h3{display:flex;gap:8px;align-items:center;font-size:14px;margin-bottom:6px}
a{color:var(--link)} p{margin:0}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--card);color:var(--mut);border-radius:999px;padding:3px 11px;cursor:pointer}
.tab[aria-pressed="true"]{border-color:var(--fg);color:var(--fg);font-weight:600}
article{display:flex;flex-direction:column;gap:18px}
.sub,.integ,.q{color:var(--mut);font-size:13px}
.stats{display:flex;gap:22px;flex-wrap:wrap;font-variant-numeric:tabular-nums}
.stats div{display:flex;flex-direction:column}.stats b{font-family:var(--fh);font-size:24px}.stats small{color:var(--mut);font-size:12px}
.pill{font-size:12px;font-weight:600;border:1px solid currentColor;border-radius:4px;padding:1px 7px}
.act{color:var(--act)}.read{color:var(--read)}.skim{color:var(--skim)}.quiet{color:var(--quiet)}
.n{color:var(--mut);font-weight:500;font-size:13px}
ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
ul.plain{list-style:disc;padding-left:20px;gap:4px}
.it{display:grid;grid-template-columns:20px minmax(0,1fr) auto;gap:10px;align-items:start;padding:10px 0;border-top:1px solid var(--line)}
.it input{margin-top:4px;width:16px;height:16px}
.tx{min-width:0;overflow-wrap:anywhere;display:flex;flex-direction:column;gap:2px}
.meta{color:var(--mut);font-size:12px}.tx small{display:block;color:var(--mut);font-size:13px}
.btn{font-size:12px;font-weight:600;border:1px solid var(--line);border-radius:6px;padding:3px 9px;white-space:nowrap;text-decoration:none;color:var(--fg);background:var(--card)}
.it input:checked~.tx{opacity:.45;text-decoration:line-through}
.tab:focus-visible,.btn:focus-visible{outline:2px solid var(--link);outline-offset:2px}
@media (max-width:560px){.it{grid-template-columns:20px minmax(0,1fr)}.btn{grid-column:2;justify-self:start}}
</style>
<main><h1>RC Briefing</h1><div class="tabs" role="group" aria-label="Briefings">""" + "".join(tabs) + "</div>" + "".join(panels) + """</main>
<script>
document.querySelectorAll('.tab').forEach(function(t){t.addEventListener('click',function(){
  document.querySelectorAll('.tab').forEach(function(x){x.setAttribute('aria-pressed',String(x===t));});
  document.querySelectorAll('article[data-p]').forEach(function(a){a.hidden=a.dataset.p!==t.dataset.t;});});});
document.querySelectorAll('input[data-k]').forEach(function(c){var k='rcb:'+c.dataset.k;
  try{c.checked=localStorage.getItem(k)==='1'}catch(e){}
  c.addEventListener('change',function(){try{localStorage.setItem(k,c.checked?'1':'0')}catch(e){}});});
</script>""")
