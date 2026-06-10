# Lab 1.2 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab1_2_claude_native.md` (the concept handout). Lab 1.2 is **optional**. This lab is
about **controlling execution**: hooks, fixed-vs-adaptive decomposition, and session
resume/fork.

---

## Why this lab at all? (read this first)

Same spirit as Lab 1.1: Claude Code already runs the agent loop for you. Lab 1.2 is
about the **controls you put around that loop** — and unlike the loop, **these are
things you genuinely configure yourself**, even in Claude Code:

- **Hooks** — code *you* write that fires on every tool call to log, validate, or block
  it. Claude doesn't invent these; you wire them in `settings.json`.
- **Decomposition** — *you* decide whether a task has known fixed steps (hard-code them)
  or an unknown path (let the model branch). That's a design choice you make.
- **Sessions** — *you* manage long-running work: fork to explore two paths, compact a
  long history into a structured summary, resume later.

Unlike Lab 1.1 (where the point was "the loop is built in, you don't write it"), Lab
1.2's whole point is the opposite: **these are the levers you pull to keep an agent
safe, predictable, and resumable.** Each demo ends with a **"Where this is written (the
files)"** section so it's clear exactly what you authored vs what Claude Code provides.

Each demo continues the lettering from Lab 1.1 (A/B/C), so this lab is **D/E/F**.

---

## Setup (once)
1. `cd` into **this** folder, then launch Claude Code (PowerShell — the path has
   spaces/parens, so keep the quotes):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module1_agentic\lab1_2_claude_native"
   claude
   ```
   Open *this* folder, not the repo root, so it loads this lab's `CLAUDE.md`,
   `.claude/settings.json` (hooks), and `.claude/commands/`.
2. **Approve the project hooks.** On first open, Claude Code detects the hooks in
   `.claude/settings.json` and asks you to approve them. **Approve** — if you don't,
   Demo D's guard won't fire. (You can re-check with `/hooks`.)
3. Confirm it loaded:
   - Type `/hooks` → should show a PreToolUse and a PostToolUse hook on `Write|Edit`.
   - Type `/invoice-flow` and `/triage` in the prompt box → should autocomplete.
   - If none of that shows, you opened the wrong folder.

> **Python note:** the hooks call `py .claude/hooks/guard.py`. The repo standardizes on
> the `py` launcher (see the main README). If `py` isn't on PATH on your machine, edit
> `.claude/settings.json` and change `py` to `python`.

---

## Demo D — hooks: intercept, log, block

> **Why bother, isn't this automatic?** No — and that's the point. Claude Code will
> happily write wherever you ask unless *you* put a guard in place. A **hook** is your
> code, running on every tool call, that can log it, validate it, or block it. This
> demo wires a real one in `settings.json` so a write to a protected folder is stopped
> before it happens — exactly the kind of guardrail you'd add for secrets or prod.

### What we are doing (the scenario)
We protect a sensitive directory. We've told Claude Code (via `.claude/settings.json`)
to run two small scripts around every `Write`/`Edit`:
- **before** the write — a guard that **blocks** it if the target is under `protected/`;
- **after** an allowed write — a logger that **records** it to an audit file.

Then we ask Claude to do one harmless write (allowed) and one dangerous write
(blocked), and watch the hooks fire.

### A note on PreToolUse vs PostToolUse (say this out loud)
The lab title says "PostToolUse hooks to … block." In Claude Code:
- **PreToolUse** runs *before* the tool → it's the one that can **block** (we use it to
  stop protected writes).
- **PostToolUse** runs *after* the tool → the file is already written, so it can only
  **log / validate / flag** (we use it for the audit log).

We use **both** so you see the real distinction. "Block before, log after."

### The files involved
| File                              | Role                                                        |
|-----------------------------------|-------------------------------------------------------------|
| `.claude/settings.json`           | Registers the two hooks on the `Write|Edit` tools.          |
| `.claude/hooks/guard.py`          | **PreToolUse** — blocks writes under `protected/` (exit 2). |
| `.claude/hooks/audit_log.py`      | **PostToolUse** — appends each write to `write-audit.log`.  |
| `protected/`                      | The off-limits directory.                                   |
| `output/`                         | An allowed write target.                                    |

### Step by step
1. Make sure you approved the hooks (Setup step 2).
2. **Allowed write** — paste:
   > Create a file `output/report.txt` containing the text "hello from the lab".
   Claude writes it. It succeeds.
3. **Blocked write** — paste:
   > Now write the text "leak" to `protected/secrets.env`.
   The PreToolUse guard fires and **denies** it. Claude reports it can't — it sees the
   reason from the hook ("BLOCKED by guard.py: … under protected location 'protected/'").
4. **Show the audit log** — paste (or open the file):
   > Show me the contents of `.claude/hooks/write-audit.log`.
   You'll see a line for the allowed `output/report.txt` write. (The blocked write is
   *not* there — it never executed.)

### Point at the screen (the lesson)
- The protected write was stopped **before** anything was written — that's PreToolUse
  blocking, your guard code deciding allow vs deny.
- The reason text the hook printed shows up to Claude — the agent *learns why* it was
  blocked, not just that it failed.
- The audit log has the allowed write but not the blocked one — PostToolUse logs what
  actually happened.
- Say: "Claude didn't decide any of this — I did, in `settings.json` and two tiny
  scripts. That's how you make an agent safe to let loose."

### Where this is written (the files)
- **The decision to run a hook at all** — on which tools, which event — is written in
  **`.claude/settings.json`** (`PreToolUse` and `PostToolUse` blocks, `matcher:
  "Write|Edit"`).
- **The block logic** is in **`.claude/hooks/guard.py`**: it reads the tool call from
  stdin, checks `tool_input.file_path` against a list of protected prefixes, and
  `exit(2)` to block (with a reason on stderr).
- **The logging logic** is in **`.claude/hooks/audit_log.py`**: it appends the tool name
  and path to `write-audit.log` and always `exit(0)`.
- **The mechanism that calls these scripts on every tool use** is built into Claude Code
  — you don't write that part, you just register the hook.

---

## Demo E — fixed vs adaptive decomposition

> **Why bother, isn't this automatic?** Claude *can* figure out steps on its own — but
> for known, repeatable work you usually don't *want* it improvising: you want the same
> reliable steps every time. The skill here is choosing: **fixed** decomposition when
> the steps are known (predictable, cheap, auditable) vs **adaptive** when the path
> depends on the input (flexible). You design which one each task gets.

### What we are doing (the scenario)
We run two flows that are deliberate opposites:
- **Fixed** — processing an invoice always means the same 3 steps. We hard-code them in
  a slash command so every run is identical.
- **Adaptive** — triaging a support ticket has no fixed path; the right next action
  depends on what the customer said. We let the coordinator decide step by step.

### The files involved
| File                               | Role                                                       |
|------------------------------------|------------------------------------------------------------|
| `.claude/commands/invoice-flow.md` | **Fixed** — always `parse_fields → check_totals → mark_for_payment`. |
| `.claude/commands/triage.md`       | **Adaptive** — pick the next action per ticket until resolved/escalated. |
| `sample_invoice.txt`               | Input for the fixed flow.                                  |
| `tickets.md`                       | Three tickets that each take a different adaptive path.    |

### Step by step — fixed
1. Run:
   > /invoice-flow
2. Watch it print exactly three steps in order, then `[done]`.
3. Run it **again**:
   > /invoice-flow
4. Confirm the trace is the **same three steps** as before.

### Step by step — adaptive
Open `tickets.md` and triage each one separately:
1. > /triage I was charged twice for my subscription this month. Same plan, two identical $29.00 charges on the 3rd. Order IDs #A1021 and #A1022. Please refund one.
2. > /triage Your app isn't working and I'm not happy about it. Fix it.
3. > /triage This is the third time you've billed me wrongly. My lawyer will be contacting you and I'm filing a complaint with my bank and the regulator today.

### Point at the screen (the lesson)
- **Fixed** `/invoice-flow`: same three steps every time — predictable and auditable.
  Great when you already know the procedure.
- **Adaptive** `/triage`: ticket 1 goes straight to `issue_refund` → `resolve`; ticket
  2 starts with `ask_clarifying_question`; ticket 3 jumps to `escalate_to_human`.
  **Same command, three different paths**, because the model picks the next step from
  the input.
- Say: "Fixed when you know the steps; adaptive when you don't. Picking the right one is
  the design decision — over-using adaptive costs a model call per branch and is harder
  to predict; over-using fixed can't handle messy real input."

### Where this is written (the files)
- **The fixed sequence** (the three steps, in order, no branching) is written in
  **`.claude/commands/invoice-flow.md`** — the steps are literally listed and the file
  says "do not add, skip, or reorder."
- **The adaptive policy** (the action vocabulary and "decide one step at a time until
  resolve/escalate") is written in **`.claude/commands/triage.md`**.
- **The actual reasoning/branching** at each adaptive step is done by Claude Code's loop
  — you wrote the *rules*; the harness runs them.

---

## Demo F — resume / fork + structured summaries
*(This is the one demo that runs from the **terminal**, across multiple `claude`
invocations — not as pasteable prompts. Session management is a CLI feature.)*

> **Why bother, isn't this automatic?** Long pieces of work don't fit in one neat chat.
> When you want to explore two solutions from the same starting point — without one
> polluting the other, and without redoing the groundwork — you **fork** the session.
> And when a session gets long, you **compact** it into a structured summary you can
> resume from. These are real, durable Claude Code features; *you* drive them.

### What we are doing (the scenario)
We do some shared groundwork (propose two rate-limiter approaches), summarize it, then
fork into two independent sessions — one per approach — so each can go deep without
losing or disturbing the shared base.

### The files involved
| File        | Role                                                               |
|-------------|--------------------------------------------------------------------|
| `task.md`   | The base task + the two expected approaches (so the demo is reproducible). |
| (on disk)   | Session transcripts live at `~/.claude/projects/<project-hash>/<session-id>.jsonl`. |

### Step by step (run these in a terminal, in this folder)
1. **Start the base session and do the groundwork.** Launch Claude Code here and paste
   the task from `task.md`:
   > Design a rate limiter for our API gateway. Propose exactly two candidate approaches
   > at a high level (one paragraph each) and name them. Don't pick a winner yet.
   Claude proposes **Path A (token bucket)** and **Path B (sliding window)**.
2. **Make a structured summary** of the groundwork:
   > /compact focus on the two rate-limiter approaches and the open decision
   `/compact` replaces the long history with a focused summary you can carry forward.
3. **Note the session id.** Run `/status` (or check the picker via `/resume`) to get the
   current session id. You can also see the file:
   `~/.claude/projects/<hash>/<session-id>.jsonl`.
4. **Fork into Path A** — in a new terminal:
   ```powershell
   claude --resume <session-id> --fork-session
   ```
   Then: *"Go deep on Path A, the token bucket. Ignore Path B."* This branch builds on
   the shared base but is its **own** session — the original is untouched.
5. **Fork into Path B** — in another terminal, same base id:
   ```powershell
   claude --resume <session-id> --fork-session
   ```
   Then: *"Go deep on Path B, the sliding window. Ignore Path A."*
6. **Show isolation on disk.** List the session files:
   ```powershell
   Get-ChildItem "$env:USERPROFILE\.claude\projects" -Recurse -Filter *.jsonl | Sort-Object LastWriteTime | Select-Object -Last 5
   ```
   The base session and the two forks are **separate `.jsonl` files** — neither fork
   changed the base.

### Point at the screen (the lesson)
- Both forks start from the **same** groundwork (the two approaches) — you didn't redo
  it. That's the value of forking from a shared base.
- The two forks diverge independently; the base session is unchanged. **Isolated
  state.**
- `/compact` turned a long history into a compact, structured summary — the durable
  "case facts" you resume from instead of dragging the whole transcript along.
- Say: "Fork to explore alternatives in parallel without cross-contamination; compact to
  keep long work manageable; resume to pick any of them back up later."

### Where this is written (the files)
- **Nothing in this lab implements forking or summaries — they are built into Claude
  Code.** `--fork-session`, `--resume`, and `/compact` are real CLI/session features.
- **What we authored** is only `task.md` (the reproducible starting point). The session
  state itself lives on disk under `~/.claude/projects/<hash>/` as `.jsonl` transcripts
  that Claude Code manages.

### Why fork at all? Benefits + real-world uses (cover this at the end)

**The core problem fork solves.** You've done real, expensive groundwork in a session —
read the codebase, gathered requirements, made decisions. Now you face a question with
*more than one good answer* and you want to try them. Your options without fork are bad:
- **Keep going in one session** → the two attempts bleed into each other; the model
  gets confused about which approach it's on, and you can't cleanly compare.
- **Start fresh for each attempt** → you throw away all the groundwork and re-explain
  everything twice.

Fork gives you the third option: **branch from the exact shared state, so each attempt
starts with all the groundwork but evolves independently.** The base is frozen and
safe; nothing one branch does can corrupt the other or the original.

**The concrete benefits.**
- **Isolation** — each branch has its own history; no cross-contamination between
  attempts.
- **No rework** — the shared setup (analysis, context, decisions) is inherited, not
  redone.
- **Cheap comparison** — run alternatives side by side, then keep the winner and discard
  the rest.
- **Safety / reversibility** — the original session is untouched, so a branch is a
  no-risk experiment you can abandon.
- **Resumability** — any branch (or the base) can be `--resume`d later; combined with
  `/compact`, long work stays manageable instead of ballooning.

**Where this shows up in real work (give one or two of these as examples):**
- **Two implementation strategies.** "Should this be a background job or an inline
  handler?" Fork, build a sketch of each from the same analyzed codebase, compare the
  diffs, keep the better one.
- **Risky refactor vs safe patch.** From a session that already understands the bug,
  fork one branch for the minimal hotfix and one for the proper refactor; ship the
  hotfix now, keep the refactor branch to finish later.
- **Library / framework bake-off.** Same requirements, fork per candidate (e.g. one
  branch wires up library X, another library Y), evaluate against the same context.
- **Debugging hypotheses.** Several plausible root causes — fork one investigation per
  hypothesis so each can chase its theory without muddying the others.
- **Migration trials.** Try a migration approach on a fork; if it goes sideways, throw
  the branch away — the base session (and your understanding) is intact.
- **Reviewer/author split.** One branch keeps building; fork another to play devil's
  advocate and critique the design, then bring the critique back.

**When NOT to bother.** If there's only one obvious path, or the groundwork is trivial
to redo, just continue or start fresh — forking adds session-management overhead you
don't need. Fork earns its keep when *both* the shared groundwork is valuable *and* you
genuinely have multiple paths worth exploring.

**How it pairs with `/compact`.** Long sessions get heavy. Before (or after) forking,
`/compact` distills the history into a structured summary — the durable "what we
decided and why" — so each branch carries the *conclusions* forward instead of dragging
the entire raw transcript. Fork = explore in parallel; compact = keep each line of work
lean enough to go the distance.

---

## Closing talking point
- **Lab 1.1** was "the loop is built in — you don't write it."
- **Lab 1.2 is the opposite lesson: the *controls* around the loop are yours to set.**
  Hooks (`settings.json` + scripts) decide what the agent may do; decomposition
  (fixed command vs adaptive command) decides how a task is broken down; sessions
  (`--fork-session`, `/compact`, `--resume`) decide how long-running work is explored
  and preserved.
- Together that's the difference between a demo agent and one you can trust to run real,
  multi-step, safety-sensitive work.
