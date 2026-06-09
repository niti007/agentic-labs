---
description: Run the team's standard code-review checklist on the current diff
---

You are running the team's standard review. Look at the current changes
(`git diff`, or the files the user names) and report findings grouped by
severity. Work through this checklist:

## Checklist
1. **Correctness** — logic bugs, off-by-one, wrong conditionals, unhandled None.
2. **Security** — secrets in code/logs, unvalidated input, string-built SQL,
   weak crypto. (Apply `src/auth/CLAUDE.md` rules strictly for auth files.)
3. **Tests** — does every new function have a `test_*.py`? Is the failure path
   covered?
4. **Readability** — clear names, no dead code, docstrings on public functions.
5. **Consistency** — matches the conventions in this repo's `CLAUDE.md`.

## Output format
For each finding:
```
[SEVERITY: critical|major|minor] file:line — issue — suggested fix
```
End with a one-line verdict: **APPROVE** or **REQUEST CHANGES**.
