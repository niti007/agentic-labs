# Project rules (repo level) — Lab 3.2 (Claude-native)

Repo-wide conventions Claude Code loads when you open this folder. Path-specific rule
files under `src/` load **only** for files in their directory, so context stays relevant.

```
lab3_2_claude_native/CLAUDE.md   <- THIS FILE (repo conventions)
        v  (@import + path-specific files below)
src/auth/CLAUDE.md               <- STRICT security rules, only under src/auth/**
src/utils/CLAUDE.md              <- relaxed rules, only under src/utils/**
```

## Testing conventions (repo-wide)
- Every new function in `src/` ships with a `pytest` test in `tests/`.
- Run the suite with `py -m pytest` before committing.

## Modular rules via @import
The line below pulls the auth module's stricter rules into context:

@./src/auth/CLAUDE.md
