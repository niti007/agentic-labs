# SOP — What this project is, in plain English

This is a **training kit** for teaching people how to use **Claude Code** (an AI assistant
that can read files, write code, and run tasks on your computer). It's made of **7 small
lessons** ("labs"), grouped into 3 modules. Each lab is a little practice playground: you
open its folder, ask Claude a few things, and watch it behave — so you *learn by seeing*,
not by reading theory.

> **The golden rule for every lab:** open that lab's folder in Claude Code, then follow the
> file called **`RUNBOOK.md`** inside it. The RUNBOOK is the step-by-step script — what to
> type, what will happen, and what to point out. If you only read one file per lab, read
> that one.

---

## The same few files show up in every lab

Before the labs, here's what the repeating filenames mean (so you don't have to re-learn
them each time):

| File | What it is, in one line |
|------|--------------------------|
| `RUNBOOK.md` | The trainer's script: do this, then this — the thing you actually present from. |
| `lab*_claude_native.md` | A short "what this lab teaches" summary (the handout). |
| `CLAUDE.md` | A notes file Claude reads automatically — your house rules for that folder. |
| `.claude/` | A hidden settings folder Claude looks inside for extra abilities (below). |
| `.claude/agents/` | "Specialist assistants" — each file is one helper with one job. |
| `.claude/commands/` | Saved shortcuts you trigger by typing `/name` (like a saved macro). |
| `.claude/skills/` | A packaged how-to Claude follows when a task matches. |
| `.claude/hooks/` | Little guard/automation scripts that run automatically around actions. |
| `.mcp.json` | A wiring list that connects Claude to outside data sources (a "tool socket"). |

Everything else in a folder is just **practice material** (fake notes, a fake invoice, a
tiny sample app) so the demo has something real to work on.

---

# Module 1 — How an AI assistant thinks and organizes work

## Lab 1.1 — How the assistant keeps working until a task is done
**What we're doing:** giving Claude a question whose answer is split across several notes,
and watching it look things up step by step until it has the full answer — then stop. It
also shows how one "lead" assistant can hand work to specialist helpers, and how to force
steps to happen in the right order.
**Why it matters:** this is the core habit of any AI assistant — keep going until the job is
truly finished, and split big jobs into smaller, reliable pieces.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab1_1_claude_native.md` | The short "what this teaches" handout. |
| `CLAUDE.md` | House rules: how the lead assistant should hand off work. |
| `.claude/agents/` | Five specialist helpers (summarizer, translator, validator, extractor, analyzer). |
| `.claude/commands/pipeline.md` | A `/pipeline` shortcut that runs two helpers in a fixed order. |
| `notes/` | Four short fake company notes; the answer is spread across them on purpose. |
| `sample_invoice.txt` | A fake invoice used by the ordered-steps demo. |

## Lab 1.2 — Putting guardrails and controls on the assistant
**What we're doing:** showing three ways to keep the assistant safe and predictable —
automatically blocking it from touching protected files, choosing between a fixed recipe vs.
letting it decide each step, and saving/branching work so you can explore two ideas without
losing your place.
**Why it matters:** before you let an AI act on real work, you want guardrails, the right
amount of freedom, and the ability to undo or branch.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab1_2_claude_native.md` | The short handout. |
| `CLAUDE.md` | House rules: which folder is off-limits, and the decision rules. |
| `.claude/settings.json` | Switches on the automatic guards (the "hooks"). |
| `.claude/hooks/guard.py` | Blocks any attempt to write into the protected folder. |
| `.claude/hooks/audit_log.py` | Keeps a log of every file the assistant writes. |
| `.claude/commands/invoice-flow.md` | A `/invoice-flow` shortcut: always the same 3 steps. |
| `.claude/commands/triage.md` | A `/triage` shortcut: decides each step based on the case. |
| `protected/` | The "do not touch" folder used to prove the guard works. |
| `output/` | A safe folder where writing is allowed. |
| `sample_invoice.txt`, `tickets.md`, `task.md` | Practice material (an invoice, sample tickets, a sample task). |

---

# Module 2 — Giving the assistant the right tools

## Lab 2.1 — Designing tools the assistant can use reliably
**What we're doing:** giving Claude a small set of pretend business tools (look up an order,
search products, fetch an order that sometimes fails) and showing three things: clear tool
names make it pick the right one, good error messages let it retry or stop sensibly, and you
can limit a helper to exactly one tool.
**Why it matters:** an AI is only as good as the tools you give it — clear, well-labeled,
well-behaved tools are what make it trustworthy.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab2_1_claude_native.md` | The short handout. |
| `CLAUDE.md` | House rules: when to retry vs. stop, and which helper does classifying. |
| `.mcp.json` | Connects Claude to the pretend "shop" toolset. |
| `lab2_1_mcp_server.py` | The pretend shop: the well-named, well-behaved tools. |
| `lab2_1_badnames_server.py` | A "bad version" with vague tool names, to show what goes wrong. |
| `.claude/agents/classifier.md` | A helper allowed to use only one tool (a labeling tool). |

## Lab 2.2 — Connecting multiple data sources and exploring code neatly
**What we're doing:** wiring up two separate data sources at once (a pretend database and a
pretend docs library), and showing how Claude searches a codebase surgically — find the
exact file, open just that one, change one line — instead of dumping everything.
**Why it matters:** real work pulls from many sources, and you want the assistant to be
precise and fast, not to grab the whole haystack.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab2_2_claude_native.md` | The short handout. |
| `CLAUDE.md` | House rules: the two data sources, and "find first, read only what you need." |
| `.mcp.json` | Connects Claude to both data sources at once. |
| `db_server.py` | The pretend database (look up a user). |
| `docs_server.py` | The pretend documentation library (search docs). |
| `sample_app/` | A tiny pretend app (a few code files + their tests) to explore and edit. |

---

# Module 3 — Setting up Claude Code for your team

## Lab 3.1 — Teaching the assistant your team's rules and shortcuts
**What we're doing:** showing how to give Claude house rules (general ones, plus stricter
rules only for sensitive folders), a saved review shortcut, and a reusable "skill" that
writes documentation the same way every time.
**Why it matters:** this is how you turn a general assistant into *your team's* assistant —
it follows your standards automatically and repeats your common tasks consistently.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab3_1_claude_native.md` | The short handout. |
| `CLAUDE.md` | The main house rules, which also pull in the stricter ones below. |
| `src/auth/CLAUDE.md` | Stricter rules that apply only to the sensitive "auth" folder. |
| `src/utils/CLAUDE.md` | Lighter rules for the low-risk "utils" folder. |
| `src/auth/login.py`, `src/utils/format.py` | Sample code the rules apply to. |
| `.claude/commands/review.md` | A `/review` shortcut: runs the team's checklist. |
| `.claude/skills/generate-api-docs/` | A reusable "write the docs" skill. |

## Lab 3.2 — Right rules at the right time, and planning before risky changes
**What we're doing:** showing that strict rules switch on only in sensitive folders, that
"Plan mode" makes Claude write a plan you approve *before* it changes anything, and that it
can survey unfamiliar code before suggesting changes.
**Why it matters:** for risky or unfamiliar work, you want a review-the-plan-first safety
step — not an assistant that edits everything immediately.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab3_2_claude_native.md` | The short handout. |
| `CLAUDE.md` + `src/auth/CLAUDE.md` + `src/utils/CLAUDE.md` | Rules that switch on by folder. |
| `src/auth/login.py`, `src/auth/session.py`, `src/api/signup.py` | A small app spread across files (so a change touches several). |
| `src/utils/format.py` | A low-risk helper file. |
| `tests/test_login.py` | The tests that must keep passing after a change. |

## Lab 3.3 — Automating reviews in a pipeline
**What we're doing:** showing the "write a failing test, then fix until it passes" loop, then
running Claude *without a human* (in a script and in an automated pipeline) to review code
and produce a clear pass/fail result.
**Why it matters:** this turns code review from "someone remembers to do it" into an
automatic, every-time step — the same way a factory line has an automatic quality check.

| Inside the folder | What it contains |
|-------------------|------------------|
| `RUNBOOK.md` | The step-by-step demo script. |
| `lab3_3_claude_native.md` | The short handout. |
| `CLAUDE.md` | House rules: the test loop and how the automated check works. |
| `calc.py`, `test_calc.py` | A tiny program and its tests (for the test loop). |
| `run_review.ps1` | A one-click script that runs a real automated review on your machine. |
| `.github/workflows/review.yml` | A reference copy of the automated pipeline step. |
| `parse_output.py` | Turns the AI's review into a simple pass or fail. |
| `sample_review_pass.json`, `sample_review_fail.json` | Two example results, to show both outcomes. |

> The **live** version of this pipeline runs automatically on the project itself; its file
> lives at the top of the project in `.github/workflows/ci-review.yml`.

---

## If you only remember three things
1. **Each lab is a folder you open in Claude Code; follow its `RUNBOOK.md`.**
2. **`CLAUDE.md` = the assistant's house rules; `.claude/` = its extra abilities; `.mcp.json` = its connections to data.**
3. **Everything else in a folder is just pretend practice material** so you can watch the
   assistant work safely.
