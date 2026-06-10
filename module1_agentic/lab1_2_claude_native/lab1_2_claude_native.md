# Lab 1.2 — Claude-native track *(optional — controlling execution)*

The **Claude Code native** counterpart to the three Lab 1.2 Python scripts
(`lab1_2_hooks_demo.py`, `lab1_2_decomposition.py`, `lab1_2_session_fork.py`). Same
three ideas — intercepting tool calls with hooks, fixed vs adaptive decomposition, and
session resume/fork with structured summaries — but here they run on **Claude Code's
real features**, not a Python simulation. In fact all three are first-class Claude Code
capabilities: hooks live in `.claude/settings.json`, decomposition is slash commands,
and resume/fork is the actual CLI.

> **Setup:** open **this folder** (`module1_agentic/lab1_2_claude_native/`) in Claude
> Code so it loads this lab's `CLAUDE.md`, `.claude/settings.json` (hooks),
> `.claude/commands/`, and fixtures. On first open, Claude Code will ask you to
> **approve the project hooks** — approve them, or Demo D won't fire. Full step-by-step
> is in `RUNBOOK.md`.

The mapping, at a glance:

| Concept                              | Python script                  | Native here                                  |
|--------------------------------------|--------------------------------|----------------------------------------------|
| Hooks — intercept / log / block      | `lab1_2_hooks_demo.py`         | Demo D — real `settings.json` hooks          |
| Fixed vs adaptive decomposition      | `lab1_2_decomposition.py`      | Demo E — `/invoice-flow` vs `/triage`        |
| Resume / fork + structured summaries | `lab1_2_session_fork.py`       | Demo F — `--fork-session` + `/compact`       |

---

## Demo D — hooks (intercept, log, block)
**Maps to `lab1_2_hooks_demo.py`.** A hook sits between the agent and the real action.
Here two real Claude Code hooks are wired in `.claude/settings.json`:
- a **PreToolUse** hook (`.claude/hooks/guard.py`) that **blocks** any Write/Edit under
  `protected/` *before* it happens (prints why, exits 2);
- a **PostToolUse** hook (`.claude/hooks/audit_log.py`) that **logs** every write that
  did go through, to `.claude/hooks/write-audit.log`.

> Note on the lab title ("PostToolUse … block"): in Claude Code, the event that can
> *block before* an action is **PreToolUse**; **PostToolUse** runs *after* and is for
> logging/validating/flagging — it can't un-write a file. We use both so you see the
> real distinction.

**Try (full steps in RUNBOOK):** ask Claude to write `output/report.txt` (allowed →
logged), then `protected/secrets.env` (blocked by the guard). **Point at:** the denial
message coming from the hook, and the new line in `write-audit.log`.

---

## Demo E — fixed vs adaptive decomposition
**Maps to `lab1_2_decomposition.py`.** When you know the steps, hard-code them (fixed:
reliable, predictable). When you don't, let the model choose the next step each turn
(adaptive: flexible).
- **Fixed:** `/invoice-flow` always runs the same three steps
  (`parse_fields → check_totals → mark_for_payment`) on `sample_invoice.txt`.
- **Adaptive:** `/triage` reads a support ticket and decides the next action one step
  at a time, branching per ticket (`tickets.md` has three that take different paths).

**Point at:** `/invoice-flow` produces the *same* 3-step trace every run; `/triage`
produces a *different* path per ticket (refund vs clarify vs escalate).

---

## Demo F — resume / fork + structured summaries
**Maps to `lab1_2_session_fork.py`.** A long-running session is a list of messages; to
explore two solution paths without losing prior state, you **fork** — and you can
**`/compact`** a long history into a structured summary you resume from. These are real
CLI features, so this demo runs from the **terminal**, not as pasteable prompts:
1. Start a session and do the base task in `task.md` (two rate-limiter approaches).
2. `/compact focus on the two rate-limiter approaches` → a structured summary.
3. `claude --resume <id> --fork-session` twice → explore Path A (token bucket) and
   Path B (sliding window) independently; the base session stays intact.

**Point at:** the base session unchanged, two forks diverging, and the separate
`.jsonl` session files under `~/.claude/projects/<hash>/`.

---

## Talking point: hand-rolled control vs native control
The Python lab makes each control mechanism **visible** — you can read the `if`
that blocks, the `for` that runs fixed steps, the `deepcopy` that forks. The native
lab shows the **same controls as real, production features**: hooks that fire on every
tool call across the whole session, slash commands your team shares, and durable
sessions you can fork and resume days later. Same concepts; the native versions are the
ones you actually ship.
