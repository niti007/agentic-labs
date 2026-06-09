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

### Lab 3.2 — Path rules + Plan mode + Explore *(mandatory)*
Follow `module3_claudecode/lab3_2_planmode.md` live. **Shows:** strict rules
firing only under `src/auth/**`; Plan mode designing before any edit lands; the
Explore subagent mapping code first.

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

---

## Suggested demo order (mandatory labs first)
1. `lab1_1_agentic_loop.py` → 2. `lab1_1_orchestrator.py` →
3. `lab2_1_tool_interfaces.py` → 4. `lab2_1_structured_errors.py` →
5. `lab2_1_tool_choice.py` → 6. Module 3 in Claude Code (`/review`, path rules,
Plan mode). Add optional labs as time allows.
