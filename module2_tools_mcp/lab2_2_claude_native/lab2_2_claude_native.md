# Lab 2.2 — Claude-native track *(optional — connecting the ecosystem)*

Lab 2.2 is the one lab that was **already** Claude-native — connecting MCP servers and
using the built-in tools both happen *inside* Claude Code, so there was never a Python
script to convert. This folder simply **packages** the three Lab 2.2 ideas into the same
self-contained, hands-on format as the other native tracks: a real **multi-source** MCP
setup (a database server *and* a docs server) plus a small sample codebase to explore.

> **Setup:** launch Claude Code **from this folder**
> (`module2_tools_mcp/lab2_2_claude_native/`) so `./.mcp.json` auto-loads, and **approve
> both the `db` and `docs` servers** when prompted. Requires the `mcp` package (already in
> the repo `requirements.txt`). Full step-by-step is in `RUNBOOK.md`.

The three concepts:

| Concept                                   | Where it lives                          | Demo |
|-------------------------------------------|-----------------------------------------|------|
| Wire multiple MCP servers (multi-source)  | `.mcp.json` + `db_server.py`/`docs_server.py` | J |
| Built-in tools (Glob/Grep/Read/Write/Edit) | `sample_app/` codebase                 | K    |
| Explore incrementally, don't dump          | `sample_app/` codebase                 | L    |

Demos are lettered **J/K/L**, continuing A–I from the earlier native tracks. (The
original Module 2.2 assets — `lab2_2_mcp_server.py`, `module2_tools_mcp/.mcp.json`,
`lab2_2_builtin_tools.md` — still work unchanged; this folder is the packaged version.)

---

## Demo J — wire up multiple MCP servers (multi-source)
Two separate local MCP servers are registered in one `.mcp.json`: **`db`** (`query_db`)
and **`docs`** (`search_docs`). Approve both and they're available together in the same
session. **Point at:** `/mcp` listing two connected servers, a user question routing to
`db` and a docs question routing to `docs` — one project drawing on multiple sources.

---

## Demo K — built-in tools for precise codebase actions
Claude Code ships with `Glob` (find files by name), `Grep` (search file contents),
`Read` (one file), `Edit` (surgical exact-string replace), and `Write` (new file). The
`sample_app/` folder gives them something real to act on — including three `*.test.ts`
files so you can "glob all test files before a bulk refactor." **Point at:** each tool
doing one precise thing, no whole-repo dumping.

---

## Demo L — explore incrementally (narrow, don't dump)
The discipline behind the tools: **Glob** to find → **Grep** to locate a symbol → **Read**
only the hit → **Edit** one line. Each step narrows scope and keeps the context window
small. **Point at:** finding `validateToken`, reading only `auth.ts`, editing one line —
versus pasting the whole project into the prompt.

---

## Talking point
This is what "connecting the ecosystem" means in practice: a project pulls tools from
several MCP sources at once, and the agent navigates code surgically with built-in tools
instead of swallowing the repo. Multi-source wiring + incremental exploration are how a
Claude Code setup stays both powerful and fast.
