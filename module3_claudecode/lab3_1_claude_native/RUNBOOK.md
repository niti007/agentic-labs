# Lab 3.1 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab3_1_claude_native.md` (the concept handout). Lab 3.1 is **mandatory**. This lab is
about **configuring Claude Code**: the CLAUDE.md hierarchy, custom slash commands, and
packaged Skills. No API key, no MCP server — just config.

---

## Why this lab at all? (read this first)

Out of the box, Claude Code is a *general* assistant. This lab is how you make it **your
team's** assistant — one that follows your conventions, runs your repeatable actions, and
carries your workflows with the repo. Three configuration mechanisms, all authored by you:

- **CLAUDE.md hierarchy** — layered rule files (global → repo → path-specific) that Claude
  loads automatically, so it follows the right conventions *for the file it's touching*
  without you repeating them.
- **Slash commands** — a saved prompt/checklist (`/review`) that turns a repeatable action
  into one keystroke for the whole team.
- **Skills** — a packaged workflow (`generate-api-docs`) Claude invokes when relevant, so
  a common task is one invocation away and shareable across projects.

Like Lab 2.2, **this lab never had a Python twin** — it's pure Claude Code configuration.
This folder packages the three mechanisms into a hands-on demo with a small sample
codebase. Each demo ends with **"Where this is written (the files)"**.

Demos continue the lettering from the earlier tracks (A–L), so this lab is **M/N/O**.

---

## Setup (once)
1. `cd` into **this** folder and launch Claude Code (PowerShell — keep the quotes):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module3_claudecode\lab3_1_claude_native"
   claude
   ```
   Launching from *this* folder makes Claude Code load this lab's `CLAUDE.md` hierarchy,
   `.claude/commands/`, and `.claude/skills/`.
2. Confirm it loaded:
   - Type `/memory` → the repo `CLAUDE.md` should be listed (and you can open it to see the
     `@import`).
   - Type `/review` in the prompt box → should autocomplete (the command).
   - Ask "what skills are available?" or watch for `generate-api-docs` to fire in Demo O.
   - If none of that shows, you opened the wrong folder.

---

## Demo M — CLAUDE.md hierarchy, @import, modular rules

> **Why bother, isn't this automatic?** Claude doesn't know your team's conventions until
> you write them down. The CLAUDE.md hierarchy lets you state a rule **once**, at the right
> level, and have Claude apply it automatically — repo-wide rules in the repo file, and
> stricter rules only where they belong (e.g. auth code). You author the layers; Claude
> loads the right ones for each file.

### What we are doing (the scenario)
We show the three tiers of memory and prove that **path-specific** rules really do scope:
the same repo applies *strict* rules under `src/auth/` and *relaxed* rules under
`src/utils/`. We also show the `@import` line that pulls a module's rules into context.

### The files involved
| File                  | Tier / role                                                    |
|-----------------------|----------------------------------------------------------------|
| `~/.claude/CLAUDE.md` | **Global** (your machine) — explained, not shipped here.       |
| `CLAUDE.md`           | **Repo** — testing convention + `@./src/auth/CLAUDE.md` import.|
| `src/auth/CLAUDE.md`  | **Path-specific (strict)** — security rules, only under auth.  |
| `src/utils/CLAUDE.md` | **Path-specific (relaxed)** — light rules, only under utils.   |
| `src/auth/login.py`, `src/utils/format.py` | Sample code the rules apply to.           |

### Step by step
1. **Show the hierarchy + import.** Open the repo `CLAUDE.md` (or run `/memory`). Point at
   the diagram and the `@./src/auth/CLAUDE.md` line — that import pulls the strict auth
   rules into context.
2. **Strict path fires** — paste:
   > Add a new function `reset_password(user, new_password, salt)` to `src/auth/login.py`.
   Watch Claude follow the **strict** rules: it won't log secrets, it hashes properly, and
   it adds/【asks for】a failure-path test — because `src/auth/CLAUDE.md` is in scope.
3. **Relaxed path fires** — paste:
   > Add a `pluralize(word, n)` helper to `src/utils/format.py`.
   Watch the **relaxed** rules apply: a docstring is enough, exhaustive failure-path tests
   optional — because `src/utils/CLAUDE.md` is in scope instead.

### Point at the screen (the lesson)
- Same repo, **two different rule sets**, chosen by *which directory the file is in*. You
  didn't repeat yourself — you scoped the rules.
- The `@import` shows rules can be **modular**: compose a big rule set from smaller files.
- Say: "Write the rule once, at the right level. Global for your personal style, repo for
  team conventions, path-specific for the parts that need special care."

> Optional — show inheritance from global: add one line to your `~/.claude/CLAUDE.md`
> (e.g. *"Always use British spelling in comments."*), restart, and watch it apply here on
> top of the repo rules. (That's your machine, not this folder.)

### Where this is written (the files)
- **The repo conventions + the import** are in this folder's **`CLAUDE.md`**.
- **The strict and relaxed scoped rules** are in **`src/auth/CLAUDE.md`** and
  **`src/utils/CLAUDE.md`** — they apply only under their own directories.
- **The loading + scoping** (deciding which CLAUDE.md files apply to a given file) is built
  into Claude Code — you author the files; the harness layers them.

---

## Demo N — custom slash command (`/review`)

> **Why bother, isn't this automatic?** Repeatable actions shouldn't depend on someone
> remembering the full checklist each time. A slash command bottles a prompt once so the
> whole team runs the *same* review, the same way, with one keystroke.

### What we are doing (the scenario)
We run the team's standard code review as a single command instead of re-typing the
checklist. `/review` is defined in `.claude/commands/review.md`.

### Step by step
1. (Optional, to give it something to review) make a small change — e.g. ask Claude to
   tweak a function in `src/utils/format.py`, or just point it at a file.
2. Run:
   > /review
   Watch Claude work the checklist — correctness, security (applying the strict auth rules
   for auth files), tests, readability, consistency — and finish with **APPROVE** or
   **REQUEST CHANGES**.

### Point at the screen (the lesson)
- One keystroke ran a five-point team review with a clear verdict — no one had to remember
  or paste the checklist.
- Say: "Anything your team does repeatedly — review, release notes, a triage flow — can be
  a command. Define it once, everyone runs it identically."

### Where this is written (the files)
- **The command** is **`.claude/commands/review.md`** — its frontmatter `description` is
  what shows in the `/` menu, and the body is the checklist Claude executes.
- **Running it when you type `/review`** is built into Claude Code — you wrote the command,
  the harness wires up the slash.

---

## Demo O — packaged Skill (`generate-api-docs`)

> **Why bother, isn't this automatic?** A command is a saved prompt; a **skill** is a saved
> *workflow* that Claude pulls in on its own when the task matches. Package a common
> multi-step job once and it's available — consistently — across every project that ships
> the skill.

### What we are doing (the scenario)
We ask for API documentation and let the `generate-api-docs` skill (in `.claude/skills/`)
run the whole documented workflow, producing a consistent `docs/API.md` from the sample
code.

### Step by step
1. Paste:
   > Generate API docs for `src/`.
2. Watch the **`generate-api-docs`** skill activate: it reads the public functions in
   `src/auth/login.py` and `src/utils/format.py`, formats each (signature, params, returns,
   summary), and writes **`docs/API.md`**.
3. Open `docs/API.md` to show the structured result.

### Point at the screen (the lesson)
- Claude chose the skill because the request matched its `description` — you didn't have to
  name it. The output is structured and repeatable.
- Say: "Skills travel with the repo. Anyone who opens this project gets 'generate API docs'
  for free, producing the same format every time. That's a reusable workflow, not a
  one-off prompt."

### Where this is written (the files)
- **The skill** is **`.claude/skills/generate-api-docs/SKILL.md`** — the frontmatter
  `description` tells Claude *when* to use it; the body is the step-by-step workflow.
- **Choosing and running the skill** is built into Claude Code — you authored the workflow;
  the harness invokes it when the task matches.

---

## Closing talking point
- **CLAUDE.md hierarchy** (Demo M) makes Claude follow your conventions automatically —
  global, repo, and path-specific, composed with `@import`.
- **Slash commands** (Demo N) make repeatable actions one keystroke for the whole team.
- **Skills** (Demo O) package whole workflows that travel with the repo and fire when
  relevant.
- All three are things you *write once* and Claude Code applies forever — the difference
  between a generic assistant and one tuned to how your team actually works.
