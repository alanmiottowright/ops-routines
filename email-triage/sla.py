#!/usr/bin/env python3
"""Deterministic SLA arithmetic for the email-triage routine.

The routine must not compute business-day math or tier lookups by hand: that is
where silent drift lives. Feed it a JSON list on stdin, get a JSON list back.

Input item fields:
  thread_id        (str)  required - opaque, echoed back
  subject          (str)  optional - echoed back for readability
  last_date        (str)  required - ISO date or datetime of the latest message
  counterparty     (str)  optional - email, domain, or name; used for tier lookup
  tier             (str)  optional - explicit tier override, wins over lookup
  stated_deadline  (str)  optional - YYYY-MM-DD, an explicit deadline in the text
  dated_item       (str)  optional - YYYY-MM-DD, the calendar date the ask hangs on
  cross_channel    (bool) optional - workstream that closes on calls/chat

SLA precedence mirrors SKILL.md rule A4, first match wins:
  1. stated_deadline
  2. dated_item        -> escalate 2 business days BEFORE the date; EXPIRED once past
  3. counterparty tier

Cross-channel threads never report overdue; they report "quiet - confirm".

Usage:
  echo '[{...}]' | python3 sla.py
  python3 sla.py --today 2026-08-31 < items.json
  python3 sla.py --selftest
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta

# Business days allowed before a thread is overdue, by tier.
TIER_SLA = {
    "internal": 3,      # RC team and contractors
    "advisor": 5,       # investors, board, counsel, bankers, auditors, tax
    "vendor": 5,        # vendors, suppliers, platforms, agencies
    "collections": 10,  # external customer collections / AR dunning
}

# Counterparty -> tier. Matched against the domain first, then a substring of the
# whole string, so "ajain@nea.com", "nea.com" and "NEA" all resolve.
TIER_MAP = {
    # internal / contractors
    "rocket.chat": "internal",
    "novagestao.digital": "internal",
    # investors, board, counsel, auditors, tax advisors, bankers
    "nea.com": "advisor",
    "polsinelli.com": "advisor",
    "bakertilly.com": "advisor",
    "mossadams.com": "advisor",
    "drummondadvisors.com": "advisor",
    "valorcapitalgroup.com": "advisor",
    "dadco.com": "advisor",
    "matheson.com": "advisor",
    "carta.com": "advisor",
    # vendors / platforms / agencies
    "insperity.com": "vendor",
    "box.com": "vendor",
    "wow24-7.io": "vendor",
    "loom.com": "vendor",
    "xserver": "vendor",
    "qbs": "vendor",
    # external customer collections
    "solera.com": "collections",
    "qikify.com": "collections",
    "fabulor.eu": "collections",
    "sanwa": "collections",
}

DEFAULT_TIER = "vendor"


def parse_day(value):
    """Accept a date, an ISO datetime, or a Z-suffixed timestamp."""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()


def business_days_between(start, end):
    """Weekdays strictly after `start` through `end` inclusive.

    A message sent Friday has elapsed 1 business day by the following Monday.
    Negative if `end` precedes `start`.
    """
    if end < start:
        return -business_days_between(end, start)
    count = 0
    cursor = start
    while cursor < end:
        cursor += timedelta(days=1)
        if cursor.weekday() < 5:
            count += 1
    return count


def shift_business_days(day, n):
    """Move `n` business days back (n<0) or forward (n>0) from `day`."""
    step = 1 if n > 0 else -1
    remaining = abs(n)
    cursor = day
    while remaining > 0:
        cursor += timedelta(days=step)
        if cursor.weekday() < 5:
            remaining -= 1
    return cursor


def resolve_tier(item):
    explicit = item.get("tier")
    if explicit:
        return explicit, "explicit"
    raw = (item.get("counterparty") or "").strip().lower()
    if not raw:
        return DEFAULT_TIER, "default"
    domain = raw.split("@")[-1] if "@" in raw else raw
    if domain in TIER_MAP:
        return TIER_MAP[domain], "domain"
    for key, tier in TIER_MAP.items():
        if key in raw:
            return tier, "substring"
    return DEFAULT_TIER, "default"


def evaluate(item, today):
    last = parse_day(item["last_date"])
    elapsed = business_days_between(last, today)
    tier, tier_source = resolve_tier(item)
    sla = TIER_SLA.get(tier, TIER_SLA[DEFAULT_TIER])

    out = {
        "thread_id": item["thread_id"],
        "subject": item.get("subject", ""),
        "last_date": last.isoformat(),
        "elapsed_bd": elapsed,
        "tier": tier,
        "tier_source": tier_source,
        "sla_bd": sla,
    }

    # Cross-channel workstreams: email silence is not evidence. Never overdue.
    if item.get("cross_channel"):
        out["clock"] = "cross-channel"
        out["status"] = "quiet - confirm"
        return out

    # (1) An explicit deadline in the text overrides everything.
    stated = item.get("stated_deadline")
    if stated:
        due = parse_day(stated)
        out["clock"] = "stated deadline"
        out["due_date"] = due.isoformat()
        if today > due:
            out["status"] = "overdue"
        elif today == due:
            out["status"] = "due today"
        else:
            out["status"] = "due in %d days" % business_days_between(today, due)
        return out

    # (2) A dated item escalates 2 business days BEFORE the date, and EXPIRES after.
    dated = item.get("dated_item")
    if dated:
        event = parse_day(dated)
        trigger = shift_business_days(event, -2)
        out["clock"] = "dated item"
        out["event_date"] = event.isoformat()
        out["due_date"] = trigger.isoformat()
        if today > event:
            out["status"] = "expired"
        elif today >= trigger:
            out["status"] = "overdue"
        else:
            out["status"] = "expiring %s" % event.isoformat()
            out["days_to_trigger"] = business_days_between(today, trigger)
        return out

    # (3) Counterparty tier is the default clock.
    out["clock"] = "tier"
    out["due_date"] = shift_business_days(last, sla).isoformat()
    if elapsed >= sla:
        out["status"] = "overdue"
        out["stale"] = elapsed >= 15  # A5 retirement threshold
    else:
        out["status"] = "due in %d days" % (sla - elapsed)
    return out


SELFTEST_ITEMS = [
    # Hand-checked against the 31 Aug 2026 run. Today = Mon 31 Aug 2026.
    {"thread_id": "nea", "subject": "NEA carve-out", "last_date": "2026-08-24",
     "counterparty": "ajain@nea.com", "stated_deadline": "2026-09-04"},
    {"thread_id": "solera", "subject": "Solera INV4191", "last_date": "2026-08-28",
     "counterparty": "daniel.fagan@solera.com"},
    {"thread_id": "va", "subject": "Baker Tilly VA sales tax", "last_date": "2026-08-28",
     "counterparty": "bakertilly.com"},
    {"thread_id": "box", "subject": "Box compilation reports", "last_date": "2026-08-24",
     "counterparty": "Daisy.Gao@bakertilly.com"},
    {"thread_id": "qikify", "subject": "Qikify collections", "last_date": "2026-08-21",
     "counterparty": "ketoan@qikify.com"},
    {"thread_id": "bigsky", "subject": "Big Sky Tech Summit", "last_date": "2026-08-06",
     "counterparty": "gabriel.engel@rocket.chat", "dated_item": "2026-09-08"},
    {"thread_id": "dadsync", "subject": "D.A. Davidson sync (expired)", "last_date": "2026-08-18",
     "counterparty": "JEvezard@dadco.com", "dated_item": "2026-08-24"},
    {"thread_id": "payoneer", "subject": "Payoneer (cross-channel)", "last_date": "2026-08-18",
     "counterparty": "karine.dourado.ext@rocket.chat", "cross_channel": True},
    {"thread_id": "polsinvoice", "subject": "Polsinelli invoice", "last_date": "2026-08-12",
     "counterparty": "mayra.lima@rocket.chat"},
]

SELFTEST_EXPECTED = {
    "nea": ("due in 4 days", "advisor", 5),
    "solera": ("due in 9 days", "collections", 10),
    "va": ("due in 4 days", "advisor", 5),
    "box": ("overdue", "advisor", 5),
    "qikify": ("due in 4 days", "collections", 10),
    "bigsky": ("expiring 2026-09-08", "internal", 3),
    "dadsync": ("expired", "advisor", 5),
    "payoneer": ("quiet - confirm", "internal", 3),
    "polsinvoice": ("overdue", "internal", 3),
}


def selftest():
    today = date(2026, 8, 31)
    failures = []
    for item in SELFTEST_ITEMS:
        got = evaluate(item, today)
        want_status, want_tier, want_sla = SELFTEST_EXPECTED[item["thread_id"]]
        if got["status"] != want_status or got["tier"] != want_tier or got["sla_bd"] != want_sla:
            failures.append((item["thread_id"], want_status, want_tier, want_sla,
                             got["status"], got["tier"], got["sla_bd"]))
        print("%-12s %-22s elapsed=%-3s tier=%-11s %s"
              % (item["thread_id"], got["status"], got["elapsed_bd"], got["tier"], got["clock"]))
    if failures:
        print("\nFAIL")
        for tid, ws, wt, wsla, gs, gt, gsla in failures:
            print("  %s: want (%s / %s / %s), got (%s / %s / %s)" % (tid, ws, wt, wsla, gs, gt, gsla))
        return 1
    print("\nOK - %d cases" % len(SELFTEST_ITEMS))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD) for testing")
    ap.add_argument("--selftest", action="store_true", help="run the built-in fixture")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    today = parse_day(args.today) if args.today else date.today()
    items = json.load(sys.stdin)
    if isinstance(items, dict):
        items = [items]
    print(json.dumps([evaluate(i, today) for i in items], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
