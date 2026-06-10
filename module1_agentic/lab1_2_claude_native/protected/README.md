# protected/ — off-limits directory (Demo D)

This folder stands in for a sensitive location (think secrets, prod config, infra).

Any attempt to **Write** or **Edit** a file under `protected/` is intercepted by the
**PreToolUse hook** (`.claude/hooks/guard.py`) and **blocked before it happens**. Try
it in the demo: ask Claude to write `protected/secrets.env` — the hook denies it and
tells Claude why.

Writes to allowed locations (e.g. `output/`) pass through and are recorded by the
**PostToolUse** logger (`.claude/hooks/audit_log.py`).
