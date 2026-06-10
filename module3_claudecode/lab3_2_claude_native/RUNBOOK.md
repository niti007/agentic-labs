# Lab 3.2 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab3_2_claude_native.md` (the concept handout). Lab 3.2 is **mandatory**. This lab is
about **targeted behavior**: rules that load by path, Plan mode before risky edits, and the
Explore subagent for mapping unfamiliar code. No API key, no MCP server.

---

## Why this lab at all? (read this first)

Lab 3.1 set up *which* rules and tools exist. Lab 3.2 is about **applying the right
behavior at the right moment** — so Claude is focused on a small file, cautious on a risky
change, and informed before it touches unfamiliar code. Three workflow levers:

- **Path-specific rules** — strict rules load *only* where they matter (e.g. `src/auth/`),
  so the agent isn't carrying security rules while editing a formatting helper. Relevant
  context, no noise.
- **Plan mode** — for risky or multi-file changes, design first and land **no edits** until
  you approve the blueprint. A migration you can review before it touches disk.
- **Explore subagent** — survey unfamiliar code (read-only) *before* proposing changes, so
  you plan on facts instead of guesses.

Like Labs 2.2/3.1, **this lab never had a Python twin** — it's pure Claude Code workflow.
This folder ships a small **multi-file** auth app so the migration and survey are real. Each
demo ends with **"Where this is written (the files)"**.

Demos continue the lettering from the earlier tracks (A–O), so this lab is **P/Q/R**.

---

## Setup (once)
1. `cd` into **this** folder and launch Claude Code (PowerShell — keep the quotes):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module3_claudecode\lab3_2_claude_native"
   claude
   ```
2. Confirm it loaded: run `/memory` → the repo `CLAUDE.md` is listed, and opening it shows
   the `@./src/auth/CLAUDE.md` import. If not, you opened the wrong folder.
3. (Optional) outside Claude Code, confirm the sample app is green so the migration demo has
   a real test to update:
   ```powershell
   py -m pytest tests\ -q
   ```

### The sample app (what's in `src/`)
```
src/auth/login.py     hash_password / verify  (sha256 — the migration target)
src/auth/session.py   login_user()            (caller of verify)
src/api/signup.py     register()              (caller of hash_password, different package)
src/utils/format.py   to_currency / truncate  (low-risk helpers)
tests/test_login.py   tests asserting the current sha256 behavior
```

---

## Demo P — path-specific rules load by glob

> **Why bother, isn't this automatic?** Claude doesn't need your auth security rules in
> context while it edits a formatting helper — that's noise that can even cause it to
> over-engineer. Path-specific rules load **only** under their directory, so the agent gets
> exactly the conventions relevant to the file it's touching.

### What we are doing (the scenario)
We make Claude edit two different paths and watch the rules change: a low-risk helper under
`src/utils/` (light rules) and an auth function under `src/auth/` (strict rules).

### The files involved
| File                  | Rules that apply when editing it                              |
|-----------------------|---------------------------------------------------------------|
| `src/utils/CLAUDE.md` | **Relaxed** — small pure helper, docstring is enough.         |
| `src/auth/CLAUDE.md`  | **Strict** — hash with a KDF, no secret logging, failure-path test. |

### Step by step
1. **Relaxed path** — paste:
   > Add a `to_percent(value)` helper to `src/utils/format.py`.
   Watch Claude follow the **light** `src/utils/` rules — a docstring, no ceremony.
2. **Strict path** — paste:
   > Add a `reset_password(user, new_password, salt)` function to `src/auth/login.py`.
   Watch the **strict** `src/auth/` rules kick in: it hashes properly, refuses to log the
   password/secret, and adds (or insists on) a failure-path test.

### Point at the screen (the lesson)
- Same repo, **two different rule sets**, selected purely by *which directory the file is
  in*. The auth rules never showed up while editing utils.
- Say: "Scope the strict stuff to where it matters. The agent stays relevant instead of
  dragging security rules into a formatting change."

### Where this is written (the files)
- **The scoped rules** are in **`src/auth/CLAUDE.md`** (strict) and **`src/utils/CLAUDE.md`**
  (relaxed); the repo **`CLAUDE.md`** holds the shared convention and the `@import`.
- **Deciding which rule files apply** to a given path is built into Claude Code — you author
  the files; the harness loads them by glob.

---

## Demo Q — Plan mode before risky changes

> **Why bother, isn't this automatic?** On a one-line fix, just let Claude edit. But a
> migration that rewrites a security primitive across several files is exactly where you
> want a **blueprint you approve** before anything touches disk. Plan mode gives you that
> gate — design first, execute only after sign-off.

### What we are doing (the scenario)
We ask for a genuinely risky, multi-file change — migrate password hashing from sha256 to a
salted bcrypt-style API — and use Plan mode so Claude maps out the whole change (every
caller, the tests) and lands **no edits** until we approve.

### Step by step
1. **Enter Plan mode.** Press **Shift+Tab** to cycle modes until it shows *plan mode* (or
   use your version's `/plan`). The indicator should say you're planning.
2. **Give the migration task** — paste:
   > Migrate `src/auth/login.py` from sha256 to a salted bcrypt-style hashing API, and
   > update every caller and test (`session.py`, `signup.py`, `tests/test_login.py`).
3. **Read the plan.** Claude produces a step-by-step plan — which files change, in what
   order, how callers and tests are updated. **No files have changed yet.** Show that.
4. **Approve.** Only after you approve does execution begin and edits start landing.

### Point at the screen (the lesson)
- The plan named **every file** the migration touches (two callers in different packages,
  plus the tests) — caught *before* any edit, so nothing is half-migrated.
- Nothing changed on disk until approval — the gate is real.
- Say: "For migrations and multi-file refactors, you review the blueprint first. Plan mode
  turns 'hope it works' into 'approve, then execute.'"

### Where this is written (the files)
- **Nothing — Plan mode is built into Claude Code.** What this folder provides is the
  *multi-file target* (`login.py` + `session.py` + `signup.py` + `tests/`) that makes the
  plan worth reviewing.
- The strict `src/auth/CLAUDE.md` rules also ride along, so the planned migration respects
  them (proper KDF, failure-path tests).

---

## Demo R — Explore subagent maps unfamiliar code first

> **Why bother, isn't this automatic?** Proposing a change to code you haven't mapped is how
> you miss a caller or break an assumption. The Explore subagent surveys the structure
> read-only and reports back, so you design on facts. It's the "measure twice, cut once" of
> agentic coding.

### What we are doing (the scenario)
We pretend the `src/` tree is unfamiliar and ask Explore to map how `auth`, `api`, and
`utils` relate — before proposing where a new input-validation layer should live.

### Step by step
1. Paste:
   > Use the Explore subagent to map how `src/auth`, `src/api`, and `src/utils` are
   > structured and how they call each other, before we decide where a new input-validation
   > layer should go. Don't change anything yet.
2. Watch the Explore subagent fan out (read-only): it reads the modules, traces that
   `signup.py` and `session.py` both depend on `auth/login.py`, and reports the structure.
3. *Then* ask for a recommendation, now grounded in that map.

### Point at the screen (the lesson)
- Explore produced a **structure survey** — who calls whom — without changing a thing. The
  proposal that follows is informed, not guessed.
- Say: "Understand first, change second. On a real unfamiliar codebase, this is the step
  that stops you from breaking a caller you didn't know existed."

### Where this is written (the files)
- **Nothing — the Explore subagent is built into Claude Code.** This folder just gives it a
  real multi-package structure (`auth` ← `api`, `auth` ← `session`, plus `utils`) worth
  mapping.

---

## Closing talking point
- **Path-specific rules** (Demo P) apply the right conventions to the right files — strict
  where it matters, light elsewhere.
- **Plan mode** (Demo Q) is the design-and-approve gate before risky, multi-file edits.
- **Explore** (Demo R) maps unfamiliar code before you touch it.
- None of the three is code you write — they're Claude Code workflows. Your job is to reach
  for the right one: scope rules by path, plan before risky changes, explore before
  proposing. That discipline is what separates a safe agentic workflow from a reckless one.
