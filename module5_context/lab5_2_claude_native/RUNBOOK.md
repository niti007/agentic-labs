# Lab 5.2 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script. Companion to `lab5_2_claude_native.md`. Lab 5.2 is
**mandatory**. Plain idea: make the AI **dependable on big, long jobs** — failures show up
loudly, notes stop it getting lost, and a crash doesn't lose your work. Running story: you've
been dropped into a big, unfamiliar project (`bigapp/`). **No code to write;** one demo runs
in the terminal (flagged).

---

## Why this lab at all? (say this first, in plain words)

The scariest way an AI lets you down isn't a loud error — it's a **silent** one: it says
"all done" but quietly skipped a broken step, and you find out next week. And on long jobs,
it can run out of room or the app can close and take your progress with it.

This lab fixes the three big reliability worries:
1. **Loud failures** — if a helper hits a wall, it tells you, clearly.
2. **Notes, not memory** — it writes findings down while exploring, so nothing's lost.
3. **Save & recover** — shrink a long session before it overflows, and come back after a
   crash.

Demos are lettered **EE/FF/GG**, continuing the earlier labs.

---

## Setup (once)
1. Open this folder in Claude Code:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module5_context\lab5_2_claude_native"
   claude
   ```
2. Confirm: type `/agents` → you should see **`checker`**. Open `bigapp/README.md` on screen
   so people see the "big project" we're working in.

---

## Demo EE — failures show up, they don't hide

> **Why do we need this?** The worst outcome is an AI that says "done" but quietly skipped
> something broken. We want the opposite: if a helper can't finish, the bad news travels
> straight back to you, with the reason.

### What we are doing
The AI (the coordinator) hands a config check to a helper called `checker`. One config file
in the project is deliberately broken (missing a required setting). We watch the failure
travel back instead of being swallowed.

### Step by step
1. Paste:
   > Use the `checker` subagent to validate `bigapp/services/billing/config.yaml`, then tell
   > me the result.
2. Watch: `checker` reads the file, finds `account_id` missing, and returns
   **`FAILED: … missing required key(s): account_id`**. The coordinator reports that failure
   to you plainly — it does **not** say "looks fine" or move on.
3. (Optional contrast) Ask it to also check a healthy file and note how a pass looks
   different from a fail.

### Point at the screen
- The failure surfaced word-for-word, with the reason — nothing was hidden.
- Say: "This is the behaviour you want before trusting an AI with real work: when a delegate
  hits a wall, you hear about it immediately."

### Where this is written
- The honest-failure behaviour is in **`.claude/agents/checker.md`** ("never pretend it
  passed"). The rule "surface failures, never continue silently" is in **`CLAUDE.md`**. The
  broken file is `bigapp/services/billing/config.yaml`.

---

## Demo FF — take notes while exploring (scratchpad)

> **Why do we need this?** Mapping a big project from memory means missing things. A good
> explorer takes notes as they go — paths, what each area does — and answers from the notes.
> It also means the work survives even if the chat gets long.

### Step by step
1. Paste:
   > Map the `bigapp/` project. As you explore, write what you find (file paths and a
   > one-line note on each area) into `scratchpad.md`. Then give me a short overview from
   > your notes.
2. Watch findings **accumulate in `scratchpad.md`** — the billing/auth/web/shared files get
   listed with short notes. Open the file to show the running list growing.
3. Ask a follow-up that uses the notes:
   > Based on your scratchpad, which area would I touch to change how invoices are taxed?
   It answers from the notes (billing), without re-reading everything.

### Point at the screen
- The scratchpad is a written map — open it and show the captured paths and notes.
- Say: "On a real giant codebase you can't hold it all in your head. Notes are how you stay
  oriented — same trick a new engineer uses on day one."

### Where this is written
- The "jot findings to `scratchpad.md` as you go" rule is in **`CLAUDE.md`**; the notepad is
  **`scratchpad.md`**; the project being mapped is **`bigapp/`**.

---

## Demo GG — save progress and recover  ⚠️ RUN THIS IN THE TERMINAL

> **Run this demo in a terminal, not the app GUI** — these are command-line/session
> features (same as Lab 1.2's fork demo).
>
> **Why do we need this?** Long jobs can hit a size limit, or the app can close. `/compact`
> shrinks a long history to its essentials so it doesn't overflow; resuming brings you back
> after a crash. Long work shouldn't be one closed window away from gone.

### Step by step (in a terminal, from this folder)
1. Start a session and do some real work so there's history to keep:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module5_context\lab5_2_claude_native"
   claude
   ```
   Then map a couple of areas of `bigapp/` (as in Demo FF) so the conversation has content.
2. **Compact before it overflows.** In the session, run:
   > /compact focus on the bigapp map and any failures found
   The long back-and-forth is replaced by a short summary; the key facts stay.
3. **Simulate a crash:** close the window / press `Ctrl+C` to end the session abruptly.
4. **Recover:** reopen the terminal in the same folder and run:
   ```powershell
   claude --continue
   ```
   (or `claude --resume` to pick the session from a list). The session comes back with its
   summarized history — you carry on instead of starting over.

### Point at the screen
- After `/compact`, the history is much shorter but the important facts survived. After the
  "crash," `--continue` brought the work back.
- Say: "Compact keeps long sessions from hitting the wall; resume means a crash costs you
  seconds, not the whole session."

### Where this is written
- Nothing in this folder — `/compact`, `--continue`, and `--resume` are built into Claude
  Code itself. This demo just shows when and how to use them.

---

## Closing talking point
- **Loud failures** (EE) mean you never get a fake "all done."
- **Notes, not memory** (FF) keep the AI oriented on huge projects.
- **Save & recover** (GG) make long sessions and crashes survivable.
- Together these are what turn "impressive in a demo" into "dependable on real, big,
  multi-step work."
