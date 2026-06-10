# Lab 1.1 — Claude-native track *(the same three concepts, no Python)*

This is the **Claude Code native** counterpart to the three Python scripts in
`module1_agentic/` (`lab1_1_agentic_loop.py`, `lab1_1_orchestrator.py`,
`lab1_1_pipeline.py`). Same three ideas — the agentic loop, the coordinator /
subagent hub-and-spoke, and the ordered pipeline — but here **Claude Code itself**
is the agent. The harness runs the loop; subagents in `.claude/agents/` are the
spokes; a slash command and `CLAUDE.md` enforce the ordering. No API key, no
`messages.create()`.

> **Setup:** open **this folder** (`module1_agentic/lab1_1_claude_native/`) in
> Claude Code so it loads this lab's `CLAUDE.md`, `.claude/agents/`, and
> `.claude/commands/`. Same model as Module 3 — open the folder, then run the
> prompts below.

The mapping, at a glance:

| Concept                        | Python script                  | Native here                            |
|--------------------------------|--------------------------------|----------------------------------------|
| Agentic loop (`stop_reason`)   | `lab1_1_agentic_loop.py`       | Demo A — Claude Code's own loop        |
| Coordinator / hub-and-spoke    | `lab1_1_orchestrator.py`       | Demo B — subagents via the Task tool   |
| Ordered pipeline + context     | `lab1_1_pipeline.py`           | Demo C — `/pipeline` + `CLAUDE.md`     |

---

## Demo A — the agentic loop (native `stop_reason`)

**Maps to `lab1_1_agentic_loop.py`.** There the loop was hand-written:
`for turn in range(...)` reading `resp.stop_reason` — `tool_use` → run the tool and
loop again, `end_turn` → halt. Here you don't write that loop. Claude Code **is**
the loop; you just watch it act until the task is truly done.

The answer to the question below is **split across files** in `notes/`, so one read
isn't enough — the agent must keep acting.

**Paste this prompt:**

> Using only the files in `notes/`, tell me which service owns rate limiting and
> what its configured limit is. Cite the files.

**What to point at:**
- The agent fires **repeated tool calls** — a Grep, then a Read of `services.md`
  (finds the owner = gateway), then a Read of `gateway.md` (finds 100 req/min).
  **Each tool call is one `tool_use` turn — the loop deciding to keep acting.**
- Then it stops and gives a single synthesized answer with citations. **That final
  message with no tool call is `end_turn` — the agent halting because the task is
  done.** Same branch as the Python script; the harness ran it for you.

---

## Demo B — coordinator / hub-and-spoke

**Maps to `lab1_1_orchestrator.py`.** There a lead agent was *forced* (`tool_choice`)
to `route()` to one of `summarize` / `translate` / `validate`, and each specialist
was its own focused Claude call. Here the **main agent is the coordinator (hub)** and
the spokes are real subagents in `.claude/agents/` (`summarizer`, `translator`,
`validator`). The `CLAUDE.md` in this folder tells the coordinator how to route.

**Paste these, one at a time:**

> Translate to French: "The deployment finished successfully."

> Summarize: Agentic systems loop over tool calls, reading stop_reason to decide
> whether to continue acting or to halt and answer the user.

> Is this valid JSON? {"name": "Nitish", "score": 9}

**What to point at:**
- The coordinator names the specialist it picked and **dispatches via the Task tool**
  to `translator` / `summarizer` / `validator` — the native equivalent of the forced
  `route()` decision plus the spoke call.
- Each task lands on the right specialist, and each specialist has a tiny, narrow job
  (2 bullets / translation only / VALID|INVALID + one line) — same focused system
  prompts as the Python spokes. Specialists with small clear jobs > one giant prompt.

---

## Demo C — ordered pipeline + explicit context passing

**Maps to `lab1_1_pipeline.py`.** There `run_pipeline()` enforced order in code:
`extract(doc)` had to return before `analyze(facts)` ran, and step 2 received step
1's **output**, not the raw doc. Here two subagents do the work — `extractor` (raw
doc → JSON) and `analyzer` (reasons over the JSON only) — and a `/pipeline` command
(plus `CLAUDE.md`) enforces the order instead of Python.

**Run the slash command:**

> /pipeline

(or `/pipeline sample_invoice.txt` — it defaults to that file.)

**What to point at:**
- **STEP 1:** the `extractor` subagent runs first and returns compact JSON facts.
- **GUARD:** if extraction returned nothing, the run halts *before* analysis — the
  same `if not facts.strip(): return` guard, now in the command.
- **STEP 2:** only then does `analyzer` run, and it reasons over **that JSON**, not
  the original invoice. Ordering and context-passing are enforced by the
  coordinator, not left to chance.

---

## Talking point: Python loop vs native loop

The Python lab makes the loop **visible** — you can see `stop_reason` being read.
The native lab makes the loop **invisible and reliable** — Claude Code runs the exact
same act/halt logic, plus retries, tool plumbing, and subagent isolation, so you
build orchestration (routing, ordering, context) on top instead of re-writing the
loop every time. Show both; the concept is identical, the leverage is different.
