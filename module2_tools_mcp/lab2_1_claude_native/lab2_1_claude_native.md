# Lab 2.1 — Claude-native track *(mandatory — reliable tools)*

The **Claude Code native** counterpart to the three Lab 2.1 Python scripts
(`lab2_1_tool_interfaces.py`, `lab2_1_structured_errors.py`, `lab2_1_tool_choice.py`).
Same three ideas — tool interfaces that drive correct selection, structured errors that
drive recovery, and scoping tool access — but here the tools are a **real MCP server**
wired into Claude Code, not Python `tools=[...]` arrays. This is exactly how you ship
tools to Claude in production.

> **Setup:** launch Claude Code **from this folder**
> (`module2_tools_mcp/lab2_1_claude_native/`) so `./.mcp.json` auto-loads, and
> **approve the `shop` MCP server** when prompted. Requires the `mcp` package
> (already in the repo `requirements.txt`). Full step-by-step is in `RUNBOOK.md`.

The mapping, at a glance:

| Concept                              | Python script                  | Native here                                |
|--------------------------------------|--------------------------------|--------------------------------------------|
| Tool interfaces → correct selection  | `lab2_1_tool_interfaces.py`    | Demo G — `search_orders` vs `search_products` |
| Structured errors (isError/isRetryable) | `lab2_1_structured_errors.py` | Demo H — flaky `get_order`: retry vs halt  |
| Scope tool access (tool_choice)      | `lab2_1_tool_choice.py`        | Demo I — `classifier` subagent scoped to `label` |

Demos are lettered **G/H/I**, continuing A–F from the Module 1 native tracks.

---

## Demo G — tool interfaces drive correct selection
**Maps to `lab2_1_tool_interfaces.py`.** The model picks tools by their **name +
description**. The `shop` server exposes two clearly-distinct tools — `search_orders`
(a customer's past purchases / order status) and `search_products` (the catalog of
items to buy) — so Claude routes each question to the right one.

**Try:** ask "Where is my order #10293?" (→ `search_orders`) and "Do you sell
mechanical keyboards under $100?" (→ `search_products`). **Failure mode:** swap in the
`shopbad` server (`search_a` / `search_b`, vague descriptions) and watch selection get
shaky — the native analog of the Python `USE_BAD_NAMES` flag.

---

## Demo H — structured errors: retry vs halt
**Maps to `lab2_1_structured_errors.py`.** A good tool tells the agent *how to react* to
failure. The `get_order` tool returns `{isError, isRetryable, content}`:
- transient **504 timeout** → `isRetryable: true` → Claude **retries** and then succeeds;
- **404 not found** → `isRetryable: false` → Claude **halts** and reports, no retry.

The retry/halt policy lives in this folder's `CLAUDE.md`. **Point at:** the same tool
producing a recover-and-continue path vs a stop-immediately path, decided by the flags.

---

## Demo I — scope tool access (the tool_choice analog)
**Maps to `lab2_1_tool_choice.py`.** The Python script forced
`tool_choice={"type":"tool","name":"label"}` so classification was always clean.
Claude Code doesn't expose that exact API knob interactively; the native way to scope
behavior is to **restrict which tools a step can use.** The `classifier` subagent has
`tools: mcp__shop__label` — the `label` tool and nothing else — so it *cannot* do
anything but classify.

**Try:** route three sample texts to the `classifier`. **Point at:** every result is a
clean `sentiment + confidence` from the `label` tool — the agent physically can't wander
into prose or call other tools.

---

## Talking point: arrays in a script vs real tools in production
The Python lab defines tools as in-memory `tools=[...]` arrays passed to one API call.
The native lab serves the **same tools from a real MCP server** that Claude Code
connects to, lists under `/mcp`, and calls across a whole session — and scopes access
with subagent tool lists. Same three principles (clear interfaces, structured errors,
scoped access); the native versions are the ones a team actually deploys.
