# Lab 2.1 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab2_1_claude_native.md` (the concept handout). Lab 2.1 is **mandatory**. This lab is
about **designing reliable tools**: clear interfaces, structured errors, and scoped
access — using a real MCP server wired into Claude Code.

---

## Why this lab at all? (read this first)

Modules 1.1/1.2 were about the agent loop and the controls around it. Lab 2.1 is about
the **tools the agent calls** — and getting tools *right* is most of what makes an agent
reliable. Three design choices, all yours:

- **Interfaces** — a tool's name and description are the only things the model uses to
  decide *which* tool to call. Clear, distinct interfaces → correct selection; vague,
  overlapping ones → wrong guesses.
- **Errors** — when a tool fails, it should tell the agent *how to react*: retry a
  transient blip, but stop on a permanent failure. Structured error fields make that
  automatic instead of the agent flailing.
- **Scope** — sometimes you want to *guarantee* a step uses one specific tool and
  nothing else (e.g. classification). You scope the toolset so it can't do otherwise.

In Claude Code, tools are delivered as **MCP servers** — small programs that expose
tools Claude can call. That's what we build here, so these aren't toy arrays; they're the
real delivery mechanism you'd ship. Each demo ends with **"Where this is written (the
files)"** so it's clear what you authored vs what Claude Code provides.

Demos continue the lettering from Modules 1.1/1.2 (A–F), so this lab is **G/H/I**.

---

## Setup (once)
1. Make sure the `mcp` Python package is installed (it's in the repo `requirements.txt`;
   activate the repo venv if you haven't):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs"
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. `cd` into **this** folder and launch Claude Code:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module2_tools_mcp\lab2_1_claude_native"
   claude
   ```
   Launching from *this* folder makes Claude Code auto-load `./.mcp.json` and this lab's
   `CLAUDE.md` + `.claude/agents/`.
3. **Approve the MCP server.** Claude Code detects `shop` in `.mcp.json` and asks to
   approve it — **approve**. Then confirm it loaded:
   - Type `/mcp` → `shop` should be **connected**, exposing `search_orders`,
     `search_products`, `get_order`, `label`.
   - Type `/agents` → should list `classifier`.
   - If `shop` shows as failed, see the Python note below.

> **Python note:** `.mcp.json` starts the server with `py lab2_1_mcp_server.py`. If `py`
> isn't on PATH, edit `.mcp.json` and change `"py"` to `"python"`. The server needs the
> `mcp` package (Setup step 1). Sanity check outside Claude Code: `py lab2_1_mcp_server.py`
> should start and wait on stdio (Ctrl+C to stop).

---

## Demo G — tool interfaces drive correct selection

> **Why bother, isn't this automatic?** The model has nothing to go on but each tool's
> **name and description** when it decides which to call. Two well-named tools → it picks
> right every time; two vague ones → it guesses and gets it wrong. Writing clear tool
> interfaces is the cheapest, highest-leverage reliability win you have.

### What we are doing (the scenario)
Our `shop` server exposes two search tools that are easy to confuse if described badly:
one for a customer's **past orders**, one for the **product catalog**. We ask two
questions that each clearly belong to one tool, and watch Claude route correctly. Then
(optional) we swap in deliberately-vague tools and watch it fall apart.

### The tools involved
| Tool (on the `shop` server) | What its description says it's for                       |
|-----------------------------|----------------------------------------------------------|
| `search_orders`             | A customer's PAST PURCHASES / order status by id/email/date. "Where is my order?" |
| `search_products`           | The PRODUCT CATALOG of items to buy, by keyword/category/price. "Do you sell …?" |

### Step by step
1. Paste:
   > Where is my order #10293? I ordered last Tuesday.
   Watch Claude call **`search_orders`** (you'll see the `mcp__shop__search_orders` tool
   call), then answer.
2. Paste:
   > Do you sell mechanical keyboards under $100?
   Watch Claude call **`search_products`**.

### Point at the screen (the lesson)
- Each question landed on the right tool — Claude read the *descriptions* and matched
  intent to interface. No routing code; good naming did the work.
- Say: "The model never sees your implementation — only the name and description. That
  text *is* the contract."

### Optional — show the failure mode (bad names)
Swapping servers is a **whole-file replace of `.mcp.json`**. Don't hand-edit fragments —
just overwrite the entire file with one of the two blocks below, save, and restart Claude
Code (it reloads MCP servers on startup).

**Step 1 — switch to BAD names.** Replace the **entire contents** of `.mcp.json` with:
```json
{
  "mcpServers": {
    "shopbad": {
      "command": "py",
      "args": ["lab2_1_badnames_server.py"]
    }
  }
}
```
Save → restart Claude Code → approve `shopbad`. Confirm with `/mcp` (you should see
`shopbad` with `search_a` / `search_b`, and `shop` gone).

**Step 2 — ask the same two questions** ("Where is my order #10293?" and "Do you sell
mechanical keyboards under $100?"). The only tools now are `search_a` ("search for
stuff") and `search_b` ("another search") — Claude has no basis to choose and will guess
or ask which one you mean.

**Point at:** identical questions, unreliable selection — proving the names/descriptions
are what carry the meaning. (Native analog of `USE_BAD_NAMES=True` in the Python lab.)

**Step 3 — switch back to GOOD names** when done. Replace the **entire contents** of
`.mcp.json` with:
```json
{
  "mcpServers": {
    "shop": {
      "command": "py",
      "args": ["lab2_1_mcp_server.py"]
    }
  }
}
```
Save → restart Claude Code → approve `shop`. This is the default the lab ships with.

### Where this is written (the files)
- **The tool names and descriptions** are written in **`lab2_1_mcp_server.py`** — each
  `@mcp.tool()` function's name and docstring *is* the interface the model selects on.
- **The bad-names contrast** is in **`lab2_1_badnames_server.py`** (`search_a`/`search_b`).
- **Which server Claude connects to** is in **`.mcp.json`**.
- **The selection itself** — matching a question to a tool — is done by Claude Code; you
  only authored the interfaces it chooses between.

---

## Demo H — structured errors: retry vs halt

> **Why bother, isn't this automatic?** When a tool call fails, a naive agent either
> gives up or retries forever. Neither is right. A well-designed tool returns *structured*
> error info — is this transient or permanent? — so the agent can recover from a blip but
> stop cold on a real failure. That's the difference between a flaky demo and a robust one.

### What we are doing (the scenario)
The `get_order` tool talks to a deliberately **flaky** orders API. The first call to a
valid order times out (transient), then succeeds on retry. A missing order id returns a
404 (permanent). The tool reports each failure with `isError` + `isRetryable`, and the
retry/halt policy in `CLAUDE.md` tells Claude what to do.

### The contract (returned by `get_order`)
| Result                         | Meaning            | Agent should… |
|--------------------------------|--------------------|---------------|
| `isError:true, isRetryable:true`  | transient (504)  | **retry**     |
| `isError:true, isRetryable:false` | permanent (404)  | **halt**      |
| `isError:false`                   | success          | use `content` |

### Step by step
1. **Retry path** — paste:
   > Use the get_order tool to fetch order `order-123`.
   First call returns a **504 timeout** (`isRetryable:true`). Per the policy, Claude
   **calls `get_order` again** — the second call **succeeds**. Watch the two tool calls.
2. **Halt path** — paste:
   > Now use get_order to fetch order `missing-999`.
   It returns a **404** (`isRetryable:false`). Claude **stops** and reports it cannot find
   the order — and does **not** retry.

### Point at the screen (the lesson)
- Same tool, two outcomes: a transient error became a **recovered success** (retry); a
  permanent error became a **clean stop** (halt). The *flags*, not guesswork, drove it.
- Say: "Retrying a 404 wastes calls and never succeeds; not retrying a timeout fails work
  that would've worked. Structured errors let the agent tell the two apart."

### Where this is written (the files)
- **The error behavior** (504-then-success for valid ids, 404 for `missing-999`, and the
  `isError`/`isRetryable` fields) is written in **`lab2_1_mcp_server.py`**, in the
  `get_order` tool.
- **The recovery policy** (retryable → call again; non-retryable → stop) is written in
  this folder's **`CLAUDE.md`**.
- **The retry loop itself** — actually calling the tool again — is run by Claude Code's
  agent loop; you wrote the *contract* and the *policy*, the harness executes them.

---

## Demo I — scope tool access (the tool_choice analog)

> **Why bother, isn't this automatic?** Sometimes you don't want the agent to *decide* —
> you want to guarantee a step does exactly one thing. The Python lab forced this with
> `tool_choice`. In Claude Code you guarantee it by **scoping the toolset**: give the step
> only the tool it's allowed to use, and it physically can't do anything else.

### What we are doing (the scenario)
We want sentiment classification to *always* come back as a clean, structured label —
never as chatty prose. So we built a `classifier` subagent whose entire toolset is the
single `label` tool. When it runs, labeling is the only move available to it.

> **Honesty note (say this):** Claude Code doesn't expose the raw API
> `tool_choice={"type":"tool",...}` knob in interactive use. The native equivalent of
> "force this one tool" is **restricting which tools the step can access** — here via the
> subagent's `tools:` list. Same outcome: the step can only use `label`.

### The files involved
| File                                 | Role                                                  |
|--------------------------------------|-------------------------------------------------------|
| `.claude/agents/classifier.md`       | Subagent scoped to `tools: mcp__shop__label` only.    |
| `lab2_1_mcp_server.py` (`label` tool) | The single tool it's allowed to call.                |

### Step by step
Route three texts to the classifier (the coordinator will dispatch to it; or say
"use the classifier subagent"):
1. > Classify this: "This product completely changed my workflow, I love it!"
2. > Classify this: "It arrived. It works. Nothing special."
3. > Classify this: "Worst support experience of my life. Never again."

### Point at the screen (the lesson)
- Each run produces a clean `label` tool call → `sentiment + confidence`. No prose, no
  wandering, no other tool — because `label` is the *only* tool the classifier has.
- Say: "Scoping the toolset is how you make a step deterministic in shape. The agent
  can't go off-script if the script is the only thing in the room."

### Where this is written (the files)
- **The scoping** is written in **`.claude/agents/classifier.md`** — the frontmatter
  `tools: mcp__shop__label` is what limits it to one tool (note the `mcp__<server>__<tool>`
  naming for MCP tools).
- **The tool it's scoped to** is the `label` function in **`lab2_1_mcp_server.py`**.
- **Dispatching to the subagent** (the Task tool) is built into Claude Code — you wrote
  the *scope*, the harness enforces it.

---

## Closing talking point
- **Interfaces** decide *which* tool gets called — your names and descriptions are the
  contract (Demo G).
- **Structured errors** decide *how failure is handled* — retry the transient, halt the
  permanent (Demo H).
- **Scope** decides *what a step is even allowed to do* — give it one tool and it can't
  misbehave (Demo I).
- All three live in things you author — an MCP server's tool definitions, a `CLAUDE.md`
  policy, a subagent's tool list — while Claude Code runs the selection, the retry loop,
  and the dispatch. Reliable tools are designed, not hoped for.
