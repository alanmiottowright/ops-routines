# ops-routines (private)

Prompts, helpers and outputs for Alan's routines that run as Claude Code cloud routines.

- `email-triage/` — PROMPT.md (the routine's instructions) and sla.py (deterministic follow-up clock)
- `context/` — standing rules the routines read instead of local memory. Edit here; the cloud runs only see this copy.
- `feeds/` — JSON the local ops conductor pulls into the dashboard's home page
- `reports/` — each run's full report

Never put credentials in this repo.
