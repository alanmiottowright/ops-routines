#!/usr/bin/env python3
"""Turn a briefing JSON (feeds/rc-briefing/<id>.json) into the DM thread: one parent message
plus one reply per section, written as numbered text files. Formatting follows the
[Ops Team] sprint thread: bold headline parent, then *Section (n)* / rule / bullets.
Usage: python3 rc-triage/briefing_dm.py <briefing.json> <outdir> <page-url>
Prints the file names in posting order (00-parent first)."""
import json, os, sys
b = json.load(open(sys.argv[1])); out = sys.argv[2]; page = sys.argv[3] if len(sys.argv) > 3 else ""
os.makedirs(out, exist_ok=True)
RULE = "_______"
LIMIT = 3800
def lnk(it): return f"[{it['room']}]({it['link']})" if it.get("link") else it["room"]
def age(it): return f" · {it['age_days']}d" if it.get("age_days") is not None else ""
c = b["counts"]
head = f"*[RC Briefing] {b['label']} | {c['needs']} need{'s' if c['needs']==1 else ''} you · {c['read']} worth reading*"
sub = [f"{c.get('rooms_triaged',0)} rooms reviewed"]
if b.get("possibly_missed"): sub.append(f"{len(b['possibly_missed'])} possibly missed")
if b.get("watchlist"): sub.append(f"{len(b['watchlist'])} watchlist addition{'s' if len(b['watchlist'])!=1 else ''}")
parent = head + "\n" + " · ".join(sub) + (f" · [Open the briefing page]({page})" if page else "")
sections = []
def sec(title, lines):
    if lines: sections.append((title, lines))
sec(f"Needs you ({len(b.get('needs',[]))})", [f"- {lnk(i)}: {i.get('who','')}: {i['ask']}{age(i)}" for i in b.get("needs", [])])
sec(f"Possibly missed ({len(b.get('possibly_missed',[]))})", [f"- {lnk(i)}: {i.get('who','')}: {i['ask']}{age(i)}" for i in b.get("possibly_missed", [])])
sec(f"Worth reading ({len(b.get('read',[]))})", [f"- {lnk(i)}: {i['summary']}" + (f" _Why: {i['why']}_" if i.get('why') else "") for i in b.get("read", [])])
sec("Skim", [f"- {lnk(i)}: {i['gist']}" for i in b.get("skim", [])])
q = b.get("quiet", [])
if q:
    sec("On call / noise", [" · ".join(f"{i['room']} {i['count']}" for i in q) + (". " + b["quiet_note"] if b.get("quiet_note") else "")])
tail = []
if b.get("watchlist"): tail.append("Watchlist: " + "; ".join(b["watchlist"]))
if b.get("integrity"): tail.append("_Run check: " + b["integrity"] + "_")
sec("Watchlist and run check", tail)
files = []
def write(name, text):
    p = os.path.join(out, name); open(p, "w").write(text); files.append(p)
write("00-parent.txt", parent)
n = 1
for title, lines in sections:
    chunk, part = [], 1
    def flush():
        global n
        t = title if part == 1 else f"{title} (cont.)"
        write(f"{n:02d}-reply.txt", f"*{t}*\n{RULE}\n" + "\n".join(chunk)); n += 1
    for ln in lines:
        if chunk and len("\n".join(chunk + [ln])) > LIMIT:
            flush(); chunk, part = [], part + 1
        chunk.append(ln)
    if chunk: flush()
print("\n".join(files))
