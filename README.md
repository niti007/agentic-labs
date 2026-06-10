# Agentic Labs — Modules 1–3 (Claude Code native)

Hands-on demos for a laptop walkthrough of:
- **Module 1** — Agentic Architecture & Orchestration
- **Module 2** — Tool Design & MCP Integration
- **Module 3** — Claude Code Configuration & Workflows
- **Module 4** — Precision Prompting (plain-English, no code)
- **Module 5** — Context Management & Reliability (plain-English)

Every lab is a **self-contained folder you open in Claude Code** and drive live — the
three concepts are demonstrated with Claude Code's *own* features (the agentic loop,
subagents, hooks, MCP servers, CLAUDE.md, slash commands, skills, Plan mode), not by
running scripts that simulate them. Each lab ships a `RUNBOOK.md` (the on-screen trainer
script) and a `lab*_claude_native.md` (the concept handout).

Demos are lettered **A–U** across the labs so you can run them in sequence.

---

## Setup (once)

```powershell
# from the agentic-labs/ folder
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # mcp (MCP servers) + pytest (TDD/CI lab)

# API key — needed only for labs that actually call the model (see note below)
copy .env.example .env
# then edit .env and paste your key from https://console.anthropic.com/settings/keys
```

**How you run a lab:** `cd` into the lab's folder and launch Claude Code there, so it
auto-loads that folder's `CLAUDE.md`, `.claude/` config, and `.mcp.json`. Then follow the
folder's `RUNBOOK.md`.

> **Which labs need the API key?** Almost none — the demos run *inside* Claude Code, which
> is already authenticated. You only need `ANTHROPIC_API_KEY` for **Lab 3.3's** headless
> pipeline (`run_review.ps1` reads it from `.env`; the CI job uses a GitHub repo secret).
> The MCP labs need the `mcp` package; the TDD/gate demos need only `pytest`.

---

## Module 1 — Agentic Architecture & Orchestration

### Lab 1.1 — Agentic loop, hub-and-spoke, ordered pipeline *(mandatory)*
Open `module1_agentic/lab1_1_claude_native/` in Claude Code; follow `RUNBOOK.md`.
- **Demo A (loop):** ask the rate-limiting research question → watch repeated Grep/Read
  tool calls (`tool_use` = keep acting) flip to a final answer (`end_turn` = halt).
- **Demo B (hub-and-spoke):** summarize / translate / validate prompts route via the Task
  tool to the matching subagent in `.claude/agents/`.
- **Demo C (pipeline):** `/pipeline` runs `extractor` then `analyzer` over *its* JSON only;
  a guard halts if extraction is empty.

### Lab 1.2 — Hooks, decomposition, session fork *(optional)*
Open `module1_agentic/lab1_2_claude_native/` (approve the project hooks on first open);
follow `RUNBOOK.md`.
- **Demo D (hooks):** a real PreToolUse hook blocks writes to `protected/` before they
  happen; a PostToolUse hook logs allowed writes to an audit file.
- **Demo E (decomposition):** `/invoice-flow` runs the same fixed 3 steps every time;
  `/triage` branches per ticket.
- **Demo F (resume/fork):** `claude --resume <id> --fork-session` explores two solution
  paths from a shared base; `/compact` makes a structured summary. (Runs from the
  terminal across sessions.)

---

## Module 2 — Tool Design & MCP Integration

### Lab 2.1 — Tool interfaces, structured errors, scoped access *(mandatory)*
Launch `claude` from `module2_tools_mcp/lab2_1_claude_native/` (approve the `shop` MCP
server); follow `RUNBOOK.md`.
- **Demo G (interfaces):** clear MCP tools `search_orders` vs `search_products` → Claude
  picks the right one; swap in the bad-names server to see selection break.
- **Demo H (structured errors):** the flaky `get_order` tool returns `isError/isRetryable`
  → Claude retries a 504 but halts on a 404 (policy in `CLAUDE.md`).
- **Demo I (scoping):** a `classifier` subagent restricted to `tools: mcp__shop__label`
  can only classify — the native analog of forcing `tool_choice`.

### Lab 2.2 — Multi-source MCP + built-in tools *(optional)*
Launch `claude` from `module2_tools_mcp/lab2_2_claude_native/` (approve the `db` and `docs`
servers); follow `RUNBOOK.md`.
- **Demo J (multi-source MCP):** two local servers — `db` (`query_db`) and `docs`
  (`search_docs`) — wired into one `.mcp.json`; a user question routes to `db`, a docs
  question to `docs`.
- **Demo K (built-in tools):** Glob/Grep/Read/Edit/Write on the `sample_app/` codebase —
  e.g. glob all `*.test.ts` before a bulk change.
- **Demo L (incremental exploration):** Grep `validateToken` → Read only `auth.ts` → Edit
  one line; narrow instead of dumping the whole repo.

---

## Module 3 — Claude Code Configuration & Workflows

### Lab 3.1 — CLAUDE.md hierarchy, commands, skills *(mandatory)*
Launch `claude` from `module3_claudecode/lab3_1_claude_native/`; follow `RUNBOOK.md`.
- **Demo M (hierarchy):** repo `CLAUDE.md` + `@import` + strict `src/auth/` vs relaxed
  `src/utils/` rules — same repo, different rules per path.
- **Demo N (slash command):** `/review` runs the team checklist with an APPROVE / REQUEST
  CHANGES verdict.
- **Demo O (skill):** "generate API docs for `src/`" fires the `generate-api-docs` skill →
  consistent `docs/API.md`.

### Lab 3.2 — Path rules, Plan mode, Explore *(mandatory)*
Launch `claude` from `module3_claudecode/lab3_2_claude_native/`; follow `RUNBOOK.md`.
- **Demo P (path rules):** edit `src/utils/` (relaxed) vs `src/auth/` (strict) → different
  rules load by glob path.
- **Demo Q (Plan mode):** plan a `sha256 → bcrypt` migration across `login.py` + callers +
  tests → a blueprint lands, no edits until you approve.
- **Demo R (Explore):** the Explore subagent maps `auth`/`api`/`utils` read-only before any
  change is proposed.

### Lab 3.3 — TDD loop, headless CI, JSON gate *(optional)*
In `module3_claudecode/lab3_3_claude_native/`; follow `RUNBOOK.md`.
- **Demo S (TDD loop):** break `calc.divide` → `py -m pytest` RED → Claude iterates to
  GREEN.
- **Demo T (headless CI):** `run_review.ps1` runs a **real** headless `claude -p` review
  using your `.env` key → JSON → gate; the live GitHub Actions job is at the repo root
  (`.github/workflows/ci-review.yml`, needs an `ANTHROPIC_API_KEY` repo secret).
- **Demo U (JSON gate):** `py parse_output.py sample_review_fail.json` → `GATE: FAIL`
  (exit 1); `…_pass.json` → `GATE: PASS` (exit 0). No key needed.

---

## Module 4 — Precision Prompting (plain-English, no code)

### Lab 4.1 — Explicit criteria & few-shot consistency *(mandatory)*
The only no-code lab — about *how you word a request* so the AI is sharp and consistent.
Running example: **sorting customer feedback by urgency**. Open
`module4_prompting/lab4_1_claude_native/`; follow `RUNBOOK.md`.
- **Demo V (explicit criteria):** vague "flag the urgent ones" guesses and over-flags;
  giving it written rules (`criteria.md`) cuts the false alarms.
- **Demo W (few-shot):** without examples the format wobbles; three worked examples
  (`examples.md`) lock the one-line format and calm tone.
- **Demo X (generalize):** it handles tricky messages it was never shown (a privacy slip, a
  sarcastic "compliment") the way the rules imply.

### Lab 4.2 — Enforcing structure: forms, validation & retry *(mandatory)*
Make the AI **fill a form, not write an essay**, so answers are clean data you can trust.
Running example: **scoring sales leads** 0-10. Launch `claude` from
`module4_prompting/lab4_2_claude_native/` (approve the `scoring` tool); follow `RUNBOOK.md`.
- **Demo Y (force a form):** the `record_score` tool makes every answer come back as
  `{name, score, reason}` instead of prose.
- **Demo Z (validation):** a score of 15, "high", or a blank reason gets bounced at the
  door — bad data never lands.
- **Demo AA (self-correct):** when bounced, the AI reads the error and fixes its own answer
  until it's valid.

---

## Module 5 — Context Management & Reliability (plain-English)

### Lab 5.1 — Managing context: pin facts, trim data, ask don't guess *(mandatory)*
Stay sharp over a long conversation. Running example: **one customer's support case**. Open
`module5_context/lab5_1_claude_native/`; follow `RUNBOOK.md`.
- **Demo BB (pin facts):** key details (the order ID) are written to a `case_file.md` sticky
  note, so they survive a long detour.
- **Demo CC (trim data):** a targeted question over a 500-row file returns only the few
  fields needed — not the whole table.
- **Demo DD (ask, don't guess):** with two orders on file, "cancel my order" makes it ask
  *which one* instead of guessing.

### Lab 5.2 — Resilient systems: loud failures, notes, recovery *(mandatory)*
Be dependable on big, long jobs. Running example: a **big unfamiliar project** (`bigapp/`).
Open `module5_context/lab5_2_claude_native/`; follow `RUNBOOK.md`.
- **Demo EE (surface failures):** a `checker` helper reports a broken config as **FAILED**,
  and the coordinator surfaces it instead of silently continuing.
- **Demo FF (scratchpad):** while mapping `bigapp/`, findings accumulate in `scratchpad.md`
  so nothing's lost.
- **Demo GG (save & recover, *terminal*):** `/compact` shrinks a long session; `claude
  --continue` recovers it after a crash.

---

## Suggested demo order (mandatory labs first)
1. **Lab 1.1** (A→B→C) → 2. **Lab 2.1** (G→H→I) → 3. **Lab 3.1** (M→N→O) →
4. **Lab 3.2** (P→Q→R) → 5. **Lab 4.1** (V→W→X) → 6. **Lab 4.2** (Y→Z→AA) →
7. **Lab 5.1** (BB→CC→DD) → 8. **Lab 5.2** (EE→FF→GG). Then add the optional labs
(1.2, 2.2, 3.3) as time allows.
