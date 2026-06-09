# Project rules (repo level)

These are the repo-wide conventions Claude Code loads automatically when you
open this folder. This file sits in the middle of the **CLAUDE.md hierarchy**:

```
~/.claude/CLAUDE.md          <- GLOBAL (your personal style, all projects)
        v  (inherited)
module3_claudecode/CLAUDE.md <- THIS FILE (repo conventions)
        v  (@import below pulls in path-specific rules)
src/auth/CLAUDE.md           <- STRICT security rules, only under src/auth/**
src/utils/CLAUDE.md          <- relaxed rules, only under src/utils/**
```

## Testing conventions (repo-wide)
- Every new function in `src/` ships with a `pytest` test.
- Test files are named `test_*.py` and live next to the code.
- Run the suite with `py -m pytest` before committing.

## Modular rules via @import
The line below pulls the auth module's stricter rules into context:

@./src/auth/CLAUDE.md
