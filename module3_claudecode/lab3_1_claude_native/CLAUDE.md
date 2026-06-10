# Project rules (repo level) — Lab 3.1 (Claude-native)

This is the **repo-level** `CLAUDE.md` that Claude Code loads automatically when you open
this folder. It sits in the middle of the **CLAUDE.md hierarchy**:

```
~/.claude/CLAUDE.md                       <- GLOBAL (your personal style, all projects)
        v  (inherited)
lab3_1_claude_native/CLAUDE.md            <- THIS FILE (repo conventions)
        v  (@import below pulls in path-specific rules)
src/auth/CLAUDE.md                        <- STRICT security rules, only under src/auth/**
src/utils/CLAUDE.md                       <- relaxed rules, only under src/utils/**
```

Each lower level **adds to / overrides** the one above for files in its scope. The global
file is your own `~/.claude/CLAUDE.md` (applies to every project on your machine).

## Testing conventions (repo-wide)
- Every new function in `src/` ships with a `pytest` test.
- Test files are named `test_*.py` and live next to the code.
- Run the suite with `py -m pytest` before committing.

## Modular rules via @import
The line below pulls the auth module's stricter rules into context:

@./src/auth/CLAUDE.md
