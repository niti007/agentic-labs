# Lab 2.2 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab2_2_claude_native.md` (the concept handout). Lab 2.2 is **optional**. This lab is
about **connecting the ecosystem**: wiring multiple MCP servers into one project, and
using Claude Code's built-in tools to explore a codebase surgically.

---

## Why this lab at all? (read this first)

A real Claude Code setup isn't one model with one tool — it's **a hub that pulls tools
from several sources and navigates your code precisely**. Lab 2.2 shows both halves:

- **Multi-source MCP** — you can wire several MCP servers into one project (here a
  database source *and* a docs source) so the agent has the right tool for each kind of
  question, all in one session.
- **Built-in tools** — Glob/Grep/Read/Edit/Write let the agent act on a codebase
  *surgically*: find the exact file, read only it, change one line.
- **Incremental exploration** — the discipline of *narrowing* (locate → read the hit →
  act) instead of pasting the whole repo into the prompt, which keeps the agent fast and
  accurate.

Unlike the other native tracks, **this lab never had a Python twin** — connecting servers
and using built-in tools always happened inside Claude Code. This folder just packages
the three ideas into a hands-on demo. Each demo ends with **"Where this is written (the
files)"**.

Demos continue the lettering from the earlier tracks (A–I), so this lab is **J/K/L**.

---

## Setup (once)
1. Make sure the `mcp` Python package is installed (it's in the repo `requirements.txt`):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs"
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. `cd` into **this** folder and launch Claude Code:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module2_tools_mcp\lab2_2_claude_native"
   claude
   ```
3. **Approve BOTH MCP servers.** Claude Code detects `db` and `docs` in `.mcp.json` and
   asks to approve them — **approve both**. Confirm:
   - Type `/mcp` → both `db` and `docs` should be **connected** (`db` exposes `query_db`,
     `docs` exposes `search_docs`).
   - If a server shows failed, see the Python note below.

> **Python note:** `.mcp.json` starts the servers with `py db_server.py` / `py
> docs_server.py`. If `py` isn't on PATH, edit `.mcp.json` and change `"py"` to
> `"python"`. Sanity check outside Claude Code: `py db_server.py` should start and wait on
> stdio (Ctrl+C to stop).

---

## Demo J — wire up multiple MCP servers (multi-source)

> **Why bother, isn't this automatic?** Claude Code has no project-specific tools until
> *you* connect them. Real projects need more than one source — a database, a docs site,
> a ticketing system. The skill is wiring several MCP servers into one `.mcp.json` so the
> agent has the right tool for each question, side by side.

### What we are doing (the scenario)
We register two separate local MCP servers in one project: a **database** source and a
**docs** source. Then we ask one question of each and watch Claude route to the right
server — proving multiple sources coexist in a single session.

### The files involved
| File             | Role                                                        |
|------------------|-------------------------------------------------------------|
| `.mcp.json`      | Registers both servers (`db`, `docs`) for this project.     |
| `db_server.py`   | The `db` MCP server — `query_db(user_id)`.                  |
| `docs_server.py` | The `docs` MCP server — `search_docs(keyword)`.             |

### Step by step
1. Confirm both are connected: type `/mcp` → `db` and `docs` both listed.
2. **Hit the database source** — paste:
   > Use query_db to look up user 1.
   Watch Claude call `mcp__db__query_db` → returns Nitish / pro.
3. **Hit the docs source** — paste:
   > Search the docs for the rate limit.
   Watch Claude call `mcp__docs__search_docs` → returns the 1000 req/min line.

### Point at the screen (the lesson)
- One project, **two independent tool sources**, both live at once. The user question
  decided which server got called.
- Say: "This is how you assemble a real toolset — wire each source in `.mcp.json` and the
  agent picks the right one. Add a third (filesystem, a ticketing server, …) the same
  way."

### Where this is written (the files)
- **The wiring** — which servers exist and how to start them — is in **`.mcp.json`**
  (`mcpServers.db` and `mcpServers.docs`). A third source (npx `filesystem`) is shown
  there under `_optional_third_source`.
- **Each source's tools** are in **`db_server.py`** and **`docs_server.py`**
  (`@mcp.tool()` functions).
- **Connecting and routing** to them is done by Claude Code — you wrote the wiring and
  the tools; the harness loads the servers and picks the right tool per question.

---

## Demo K — built-in tools for precise codebase actions

> **Why bother, isn't this automatic?** A naive approach pastes the whole repo into the
> prompt and hopes. Claude Code instead gives the agent precise file tools — find by
> name, search by content, read one file, change one line. Knowing these tools (and that
> the agent uses them) is what makes it act like an engineer, not a search box.

### What we are doing (the scenario)
We act on a tiny sample project (`sample_app/`) using the built-in tools, including the
classic "find all the test files before a bulk change."

### The built-in tools (the catalog)
| Tool   | What it does                         | Demo line                                  |
|--------|--------------------------------------|--------------------------------------------|
| `Glob` | Find files by name/pattern           | "Glob all `**/*.test.ts`" → 3 test files   |
| `Grep` | Search file *contents* (ripgrep)     | "Where is `validateToken` defined?"        |
| `Read` | Read one file (or a slice)           | Read only the file Grep pointed at         |
| `Edit` | Exact-string replace in a file       | One surgical change                        |
| `Write`| Create a new file                    | Add a new test file                        |

### Step by step
1. **Glob before a bulk action** — paste:
   > Glob all the `.test.ts` files under `sample_app/`.
   → returns `tests/auth.test.ts`, `cart.test.ts`, `utils.test.ts`. (This is the "find
   everything I'm about to refactor" move — list first, no files loaded yet.)
2. **Grep to locate** — paste:
   > Grep for `validateToken` in `sample_app/`.
   → one hit in `src/auth.ts` (plus its test).
3. **Surgical Edit** — paste:
   > In `sample_app/src/auth.ts`, change `TOKEN_TTL_SECONDS = 3600` to `7200`.
   → a single exact-string Edit, not a rewrite of the file.

### Point at the screen (the lesson)
- Each tool did **one precise thing**. Glob listed; Grep located; Edit changed one line.
- Say: "The agent never loaded the whole project — it used the right tool for each step.
  That's the difference between surgical and sloppy."

### Where this is written (the files)
- **The built-in tools are part of Claude Code** — you don't author them. What you
  provide is the codebase they act on: **`sample_app/src/*.ts`** and
  **`sample_app/tests/*.test.ts`**.
- Tool *availability* can be scoped (permissions, subagent `tools:` lists, as in Lab 2.1
  Demo I), but by default these built-ins are always on.

---

## Demo L — explore incrementally (narrow, don't dump)

> **Why bother, isn't this automatic?** Context is finite and attention is precious.
> Dumping a whole repo in makes the agent slower and *less* accurate. The discipline —
> locate, read only the hit, act — is what keeps it sharp. This demo is the same tools as
> Demo K, but the lesson is the *workflow*, not the tools.

### What we are doing (the scenario)
We answer a "change this function" request the right way: progressively narrowing from
"the whole project" down to one line, touching as little as possible.

### Step by step (one continuous flow)
1. **Glob** — *"What test files exist in `sample_app/`?"* → a list. Nothing read yet.
2. **Grep** — *"Where is `validateToken` defined?"* → one location: `src/auth.ts`.
3. **Read only the hit** — *"Read just `sample_app/src/auth.ts`."* → context stays small;
   you did **not** read `cart.ts`, `utils.ts`, or the tests.
4. **Edit surgically** — *"Add a one-line comment above `validateToken` explaining the TTL
   check."* → a single targeted Edit.

### Point at the screen (the lesson)
- Each step **narrows** scope: Glob → list, Grep → location, Read → one file, Edit → one
  change. The opposite of "paste the whole repo and hope."
- Show the contrast out loud: "We touched exactly one file out of six. The other five
  never entered context — that's why it's fast and accurate."
- Say: "This narrowing instinct matters most on a *big* codebase, where loading
  everything isn't even possible."

### Where this is written (the files)
- **Nothing — this is a workflow, not a file.** The tools are Claude Code's; the
  discipline is the lesson. (The `CLAUDE.md` in this folder nudges it: "narrow before you
  read.")

---

## Closing talking point
- **Multi-source MCP** (Demo J) assembles the right *tools* for a project — wire each
  source in `.mcp.json`.
- **Built-in tools** (Demo K) give the agent precise *actions* on your code — Glob, Grep,
  Read, Edit, Write.
- **Incremental exploration** (Demo L) is the *discipline* that keeps it fast — locate,
  read the hit, act; never dump the whole repo.
- Together that's "connecting the ecosystem": many sources in, surgical actions out.
