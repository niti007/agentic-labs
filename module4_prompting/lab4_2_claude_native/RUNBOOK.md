# Lab 4.2 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script. Companion to `lab4_2_claude_native.md`. Lab 4.2 is
**mandatory**. The big idea in plain words: **make the AI fill out a form, not write an
essay** — so its answers are clean data you can trust and automate. Running example:
**scoring sales leads** 0-10.

---

## Why this lab at all? (say this first, in plain words)

Imagine you ask someone to "score these leads" and they hand you three paragraphs. Nice to
read — useless if you wanted to paste rows into a spreadsheet or your CRM. Worse, one of
them writes "score: really high" and another writes "8/10" — now your data is a mess.

This lab fixes that with three simple habits:
1. **Give the AI a form** with fixed boxes (name, score, reason) it *must* fill.
2. **Put a checker on the form** so nonsense (a score of 15, a blank reason) gets bounced.
3. **Let the AI fix its own mistakes** when something's bounced, with no human stepping in.

The payoff: the answer is *always* clean, in range, and ready to drop into a real system.
Demos are lettered **Y/Z/AA**, continuing the earlier labs (A–X).

---

## Setup (once)
1. Make sure the `mcp` package is installed (it's in the repo `requirements.txt`).
2. Launch Claude Code from this folder and approve the `scoring` tool:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module4_prompting\lab4_2_claude_native"
   claude
   ```
3. Confirm: type `/mcp` → `scoring` is **connected** (it provides the `record_score` tool).
   Open `leads.md` on screen so people can see what we're scoring.

> **Python note:** the tool starts with `py lead_scoring_server.py`. If `py` isn't found,
> change `"py"` to `"python"` in `.mcp.json`. You never edit the tool itself.

---

## Demo Y — make it fill a form, not write an essay

> **Why do we need this?** If the answer is a paragraph, a human has to re-read it and type
> it into a spreadsheet. If the answer is a filled-in form, it drops straight into your CRM.
> Structured output is what makes AI useful *inside* your tools, not just in a chat window.

### Step by step
1. **Ask the essay way first.** Paste:
   > Look at the leads in `leads.md` and tell me how promising each one is.
   You'll get readable prose — but every lead is described a bit differently, and you
   couldn't paste it into a spreadsheet.
2. **Now use the form.** Paste:
   > Now score each lead in `leads.md` using the `record_score` tool, following `rubric.md`.
   Watch each lead come back as the **same three filled boxes** — name, score, reason —
   because the tool only accepts that shape.

### Point at the screen
- Essay version: nice, but inconsistent and not machine-ready. Form version: identical,
  tidy rows you could paste anywhere.
- Say: "Same AI, same leads — but now the answer is *data*, not prose. That's the whole
  trick: give it a form to fill."

### Where this is written
- The "form" is the `record_score` tool in **`lead_scoring_server.py`** (it requires name,
  score, reason). **`CLAUDE.md`** tells Claude to always use it.

---

## Demo Z — let the form reject bad data

> **Why do we need this?** Even a filled form can hold garbage — a score of 15, or "high"
> in a number box, or a blank reason. Checking at the door means broken data never reaches
> your spreadsheet, where it would quietly cause problems later.

### Step by step
1. **Out-of-range number.** Paste:
   > Use record_score to record BrightWave with a score of 15 and a reason.
   The tool **bounces it**: "score must be between 0 and 10." Nothing gets recorded.
2. **Wrong type.** Paste:
   > Try to record BrightWave with a score of "high".
   The form won't even accept it — a score box only takes a whole number. (This is the
   *automatic* check, before our own rule even runs.)
3. **Blank reason.** Paste:
   > Record Acme Corp with a score of 9 but leave the reason empty.
   Bounced again: "reason must not be empty."

### Point at the screen
- Two layers of safety: the box type is checked automatically, *and* our rule checks the
  number makes sense (0-10) and the reason isn't blank.
- Say: "Bad data gets stopped at the door, not discovered next week in a broken report."

### Where this is written
- The checks live in **`lead_scoring_server.py`** — the score range and non-empty reason
  rules, each returning a plain message saying what's wrong.

---

## Demo AA — let it fix itself (check-and-retry)

> **Why do we need this?** A check that just says "no" still needs a human to fix it. The
> real win is when the AI reads *why* it was rejected and corrects itself — so by the time
> you look, the answer is already valid. No babysitting.

### Step by step
1. Set up the mistake on purpose. Paste:
   > Score BrightWave. It seems amazing, so start by trying a score of 12 — and if the tool
   > rejects it, fix it and record a valid score.
2. Watch the loop on screen:
   - Claude calls `record_score` with **12** → tool returns "score must be between 0 and 10."
   - Claude **reads that**, picks a valid score (e.g. 9 or 10), and calls again → accepted.
3. (Optional) Just say *"Score all the leads in `leads.md` and make sure every one is
   recorded."* — if it ever trips a rule, it self-corrects without you asking.

### Point at the screen
- The rejection wasn't a dead end — the AI used the error message to fix its own answer.
- Say: "This is the payoff. The form forces the shape, the checker catches mistakes, and
  the AI fixes them itself — so the data you get is *always* clean. That's what makes it
  safe to automate."

### Where this is written
- The self-correcting loop is Claude's own behavior, guided by the rule in **`CLAUDE.md`**
  ("if record_score returns an error, read it, fix the value, and call again"). The clear
  error messages from **`lead_scoring_server.py`** are what make the fix possible.

---

## Closing talking point (for the skeptic in the room)
- **A form** (Y) makes answers clean and machine-ready — paste straight into your tools.
- **A checker** (Z) stops bad data at the door instead of in next week's report.
- **Self-correction** (AA) means valid output every time, with no human in the loop.
- Together that's the difference between "the AI gave a nice answer" and "I can plug the AI
  into my CRM and trust what comes out."
