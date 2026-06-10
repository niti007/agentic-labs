# Agentic Labs — Modules 1–3 (hands-on demos)

Runnable demos for a laptop walkthrough of:
- **Module 1** — Agentic Architecture & Orchestration
- **Module 2** — Tool Design & MCP Integration
- **Module 3** — Claude Code Configuration & Workflows

Each lab is a small, self-contained script or markdown walkthrough. This README
is your **demo guide**: for every lab it says *what it shows*, *the command*,
and *what to point at on screen*.

---

## Setup (once)

```powershell
# from the agentic-labs/ folder
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# add your API key (needed for labs that call Claude)
copy .env.example .env
# then edit .env and paste your key from https://console.anthropic.com/settings/keys
```

> **Which labs need the API key?** Anything that calls Claude (most of Module 1
> & 2). The purely-local demos run with **no key**: `lab1_2_hooks_demo.py`,
> `lab1_2_session_fork.py`, `lab2_1_structured_errors.py`,
> `lab3_3_tdd_ci/` (pytest + parse_output.py).

Run scripts from the `agentic-labs/` folder, e.g.
`py module1_agentic/lab1_1_agentic_loop.py`.

---

## Module 1 — Agentic Architecture & Orchestration

### Lab 1.1 — Agentic loop *(mandatory)*
`py module1_agentic/lab1_1_agentic_loop.py`
**Shows:** the core loop reading `stop_reason`. **Point at:** the
`stop_reason = 'tool_use'` lines (agent keeps acting) flipping to a final
`done()` / `end_turn` (agent halts). That branch is the whole lesson.

### Lab 1.1 — Orchestrator (hub-and-spoke) *(mandatory)*
`py module1_agentic/lab1_1_orchestrator.py`
**Shows:** one lead agent routing to `summarize` / `translate` / `validate`
subagents. **Point at:** the `[LEAD] -> delegating to subagent: X` line and how
each task lands on the right specialist.

### Lab 1.1 — Ordered pipeline *(mandatory)*
`py module1_agentic/lab1_1_pipeline.py`
**Shows:** extraction must finish before analysis, and step 1's output is fed
into step 2. **Point at:** STEP 1 JSON, then STEP 2 reasoning over *that* JSON.

### Lab 1.1 — Claude-native track *(mandatory, no key)*
The **same three concepts above, but driven by Claude Code itself** — no Python,
no `messages.create()`. The harness runs the loop; subagents in `.claude/agents/`
are the spokes; `CLAUDE.md` + a `/pipeline` command enforce ordering. Open
`module1_agentic/lab1_1_claude_native/` in Claude Code and follow
`lab1_1_claude_native.md`:
- **Demo A (loop):** ask the rate-limiting research question → watch repeated
  Grep/Read tool calls (`tool_use` = keep acting) flip to a final answer
  (`end_turn` = halt). Native twin of `lab1_1_agentic_loop.py`.
- **Demo B (hub-and-spoke):** summarize / translate / validate prompts route via
  the Task tool to the matching subagent. Native twin of `lab1_1_orchestrator.py`.
- **Demo C (pipeline):** `/pipeline` runs `extractor` then `analyzer` over *its*
  JSON only, guard halts if extraction is empty. Native twin of `lab1_1_pipeline.py`.

### Lab 1.2 — Hooks *(optional, no key)*
`py module1_agentic/lab1_2_hooks_demo.py`
**Shows:** a PostToolUse hook blocking writes to protected paths. **Point at:**
the `[hook] ... BLOCKED` lines vs `allowed`.

### Lab 1.2 — Decomposition *(optional)*
`py module1_agentic/lab1_2_decomposition.py`
**Shows:** fixed 3-step invoice flow vs. adaptive model-driven triage.
**Point at:** the fixed steps always identical; the adaptive trace branching.

### Lab 1.2 — Session fork *(optional, no key)*
`py module1_agentic/lab1_2_session_fork.py`
**Shows:** forking a session into two paths with isolated state. **Point at:**
base stays unchanged while path A / path B diverge.

### Lab 1.2 — Claude-native track *(optional)*
The **same three controls, but as real Claude Code features** — no Python. Open
`module1_agentic/lab1_2_claude_native/` in Claude Code (approve the project hooks on
first open) and follow `RUNBOOK.md`:
- **Demo D (hooks):** real `settings.json` hooks — a PreToolUse guard blocks writes to
  `protected/` before they happen; a PostToolUse hook logs allowed writes to an audit
  file. Native twin of `lab1_2_hooks_demo.py`.
- **Demo E (decomposition):** `/invoice-flow` runs the same fixed 3 steps every time;
  `/triage` branches per ticket. Native twin of `lab1_2_decomposition.py`.
- **Demo F (resume/fork):** `claude --resume <id> --fork-session` explores two solution
  paths from a shared base; `/compact` makes a structured summary. Native twin of
  `lab1_2_session_fork.py`. (Runs from the terminal across multiple sessions.)

---

## Module 2 — Tool Design & MCP Integration

### Lab 2.1 — Tool interfaces *(mandatory)*
`py module2_tools_mcp/lab2_1_tool_interfaces.py`
**Shows:** good names → correct tool pick (`search_orders` vs
`search_products`). **Point at:** each question routing to the right tool. To
show the failure mode, set `USE_BAD_NAMES = True` at the top and rerun.

### Lab 2.1 — Structured errors *(mandatory, no key)*
`py module2_tools_mcp/lab2_1_structured_errors.py`
**Shows:** `isRetryable=True` (timeout) → retry; `isRetryable=False` (404) →
halt. **Point at:** the `[RETRY]` path succeeding vs the `[HALT]` on 404.

### Lab 2.1 — tool_choice *(mandatory)*
`py module2_tools_mcp/lab2_1_tool_choice.py`
**Shows:** forcing the `label` tool so classification is always clean.
**Point at:** every input returns a structured `sentiment + confidence`.

### Lab 2.1 — Claude-native track *(mandatory)*
The **same three tool-design ideas, but as a real MCP server** wired into Claude Code —
no Python `tools=[...]` arrays. Launch `claude` from
`module2_tools_mcp/lab2_1_claude_native/` (approve the `shop` server on first open) and
follow `RUNBOOK.md`:
- **Demo G (interfaces):** clear MCP tools `search_orders` vs `search_products` → Claude
  picks the right one; swap in the bad-names server to see selection break. Native twin
  of `lab2_1_tool_interfaces.py`.
- **Demo H (structured errors):** the flaky `get_order` tool returns `isError/isRetryable`
  → Claude retries a 504 but halts on a 404 (policy in `CLAUDE.md`). Native twin of
  `lab2_1_structured_errors.py`.
- **Demo I (scoping):** a `classifier` subagent restricted to `tools: mcp__shop__label`
  can only classify — the native analog of forcing `tool_choice`. Native twin of
  `lab2_1_tool_choice.py`.

### Lab 2.2 — MCP server + .mcp.json *(optional)*
**Shows:** a real local MCP server wired into Claude Code.
1. Copy `module2_tools_mcp/.mcp.json` to the repo root (`agentic-labs/.mcp.json`).
2. Open `agentic-labs/` in Claude Code; approve the `demo-db-docs` server.
3. Ask: *"Use query_db to look up user 1"* and *"search_docs for rate limit"*.
**Point at:** Claude calling your server's tools. (Standalone sanity check:
`py module2_tools_mcp/lab2_2_mcp_server.py` — waits on stdio, Ctrl+C to stop.)

### Lab 2.2 — Built-in tools walkthrough *(optional)*
Open `module2_tools_mcp/lab2_2_builtin_tools.md` and run the prompts inside
Claude Code. **Shows:** Glob → Grep → Read → Edit incremental exploration.

### Lab 2.2 — Claude-native track *(optional)*
The same three ideas packaged as one hands-on demo (Lab 2.2 was already native — no
Python twin). Launch `claude` from `module2_tools_mcp/lab2_2_claude_native/` (approve the
`db` and `docs` servers on first open) and follow `RUNBOOK.md`:
- **Demo J (multi-source MCP):** two local servers — `db` (`query_db`) and `docs`
  (`search_docs`) — wired into one `.mcp.json`; a user question routes to `db`, a docs
  question to `docs`.
- **Demo K (built-in tools):** Glob/Grep/Read/Edit/Write on the `sample_app/` codebase —
  e.g. glob all `*.test.ts` before a bulk change.
- **Demo L (incremental exploration):** Grep `validateToken` → Read only `auth.ts` → Edit
  one line; narrow instead of dumping the whole repo.

---

## Module 3 — Claude Code Configuration & Workflows

> Open the **`module3_claudecode/`** folder in Claude Code for these.

### Lab 3.1 — CLAUDE.md hierarchy, commands, skills *(mandatory)*
- **Hierarchy:** open `module3_claudecode/CLAUDE.md` — show global → repo →
  `@import ./src/auth/CLAUDE.md`. **Point at:** the import line pulling auth
  rules into context.
- **Slash command:** run `/review` in Claude Code. **Point at:** the team
  checklist firing on the diff (defined in `.claude/commands/review.md`).
- **Skill:** ask *"generate API docs for src/"* → the `generate-api-docs` skill
  (`.claude/skills/generate-api-docs/SKILL.md`) runs. **Point at:** one
  invocation producing consistent `docs/API.md`.

### Lab 3.1 — Claude-native track *(mandatory)*
The same three config ideas packaged as one self-contained, hands-on demo with a sample
codebase. Launch `claude` from `module3_claudecode/lab3_1_claude_native/` and follow
`RUNBOOK.md`:
- **Demo M (hierarchy):** repo `CLAUDE.md` + `@import` + strict `src/auth/` vs relaxed
  `src/utils/` rules — same repo, different rules per path.
- **Demo N (slash command):** `/review` runs the team checklist with an APPROVE / REQUEST
  CHANGES verdict.
- **Demo O (skill):** "generate API docs for `src/`" fires the `generate-api-docs` skill →
  consistent `docs/API.md`.

### Lab 3.2 — Path rules + Plan mode + Explore *(mandatory)*
Follow `module3_claudecode/lab3_2_planmode.md` live. **Shows:** strict rules
firing only under `src/auth/**`; Plan mode designing before any edit lands; the
Explore subagent mapping code first.

### Lab 3.2 — Claude-native track *(mandatory)*
The same three workflow ideas packaged as one self-contained demo with a multi-file auth
app. Launch `claude` from `module3_claudecode/lab3_2_claude_native/` and follow
`RUNBOOK.md`:
- **Demo P (path rules):** edit `src/utils/` (relaxed) vs `src/auth/` (strict) → different
  rules load by glob path.
- **Demo Q (Plan mode):** plan a `sha256 → bcrypt` migration across `login.py` + callers +
  tests → a blueprint lands, no edits until you approve.
- **Demo R (Explore):** the Explore subagent maps `auth`/`api`/`utils` read-only before any
  change is proposed.

### Lab 3.3 — TDD loop + headless CI *(optional, no key for the TDD part)*
```powershell
cd module3_claudecode\lab3_3_tdd_ci
py -m pytest -q            # GREEN as shipped
# break calc.divide (e.g. raise NotImplementedError), rerun -> RED,
# then ask Claude to fix it -> GREEN  (the TDD loop)

py parse_output.py        # demo: parses sample JSON -> GATE: FAIL (exit 1)
```
**Shows:** red→green TDD, plus `parse_output.py` turning Claude's JSON review
into a CI pass/fail gate (`.github/workflows/review.yml` is the headless step).

### Lab 3.3 — Claude-native track *(optional)*
The same three ideas packaged as one demo, **with a real runnable pipeline**. In
`module3_claudecode/lab3_3_claude_native/` follow `RUNBOOK.md`:
- **Demo S (TDD loop):** break `calc.divide` → `py -m pytest` RED → Claude iterates to GREEN.
- **Demo T (headless CI):** `run_review.ps1` runs a **real** headless `claude -p` review
  using your `.env` key → JSON → gate; the live GitHub Actions job is at the repo root
  (`.github/workflows/ci-review.yml`, needs an `ANTHROPIC_API_KEY` repo secret).
- **Demo U (JSON gate):** `py parse_output.py sample_review_fail.json` → `GATE: FAIL` (exit
  1); `…_pass.json` → `GATE: PASS` (exit 0). No key needed.

---

## Suggested demo order (mandatory labs first)
1. `lab1_1_agentic_loop.py` → 2. `lab1_1_orchestrator.py` →
3. `lab2_1_tool_interfaces.py` → 4. `lab2_1_structured_errors.py` →
5. `lab2_1_tool_choice.py` → 6. Module 3 in Claude Code (`/review`, path rules,
Plan mode). Add optional labs as time allows.
