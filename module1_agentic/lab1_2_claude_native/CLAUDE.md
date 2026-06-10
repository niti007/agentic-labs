# Lab 1.2 (Claude-native) — coordinator & lab rules

This lab demonstrates **controlling execution**: hooks, fixed-vs-adaptive
decomposition, and session resume/fork. Claude Code's hooks, slash commands, and
session machinery are the moving parts the trainee is watching.

## Protected paths (Demo D)
The `protected/` directory is off-limits. A **PreToolUse hook**
(`.claude/hooks/guard.py`) blocks any Write/Edit under `protected/` before it happens;
a **PostToolUse hook** (`.claude/hooks/audit_log.py`) logs every write that does go
through to `.claude/hooks/write-audit.log`. Don't try to work around the guard — being
blocked is the expected behavior to demonstrate.

## Decomposition (Demo E)
- **Fixed** work uses the `/invoice-flow` command: always the same three steps
  (`parse_fields → check_totals → mark_for_payment`), in order, no branching.
- **Adaptive** work uses the `/triage` command: decide the next action one step at a
  time from the ticket, branching per case until `resolve` or `escalate_to_human`.
Use fixed flows when the steps are known; use adaptive when the path depends on input.

## Sessions (Demo F)
Resume/fork and `/compact` are driven from the terminal — see `RUNBOOK.md` → Demo F.
