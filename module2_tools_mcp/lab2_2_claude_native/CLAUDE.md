# Lab 2.2 (Claude-native) — ecosystem & exploration rules

This lab demonstrates **connecting the ecosystem**: wiring multiple MCP servers into one
project, and using Claude Code's built-in tools to explore a codebase surgically.

## Tool sources (Demo J)
Two local MCP servers are wired in via `.mcp.json`:
- **`db`** (`query_db`) — look up a user record by id.
- **`docs`** (`search_docs`) — search the product documentation by keyword.
Route a user/account question to `db` and a "how does X work / what's the limit" question
to `docs`. Both are available in the same session — that's the multi-source point.

## Explore incrementally (Demos K & L)
When working in `sample_app/`, **narrow before you read**:
1. `Glob` to find files by name/pattern (e.g. `**/*.test.ts`).
2. `Grep` to locate a symbol by content (e.g. a function name).
3. `Read` only the file(s) the search pointed at — not the whole tree.
4. `Edit` surgically (exact-string replace); `Write` only for brand-new files.
Do not dump the entire codebase into context — locate, read the hit, act.
