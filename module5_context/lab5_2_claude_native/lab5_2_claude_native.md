# Lab 5.2 — Resilient Systems *(mandatory — plain-English lab)*

**In one sentence:** make the AI **dependable on big, long jobs** — failures show up loudly,
notes keep it from getting lost, and a crash doesn't lose your work.

The running story: you've been dropped into a **big, unfamiliar company project** (`bigapp/`)
and need to find your way around without things silently going wrong.

> **Setup:** open this folder (`module5_context/lab5_2_claude_native/`) in Claude Code and
> follow `RUNBOOK.md`. No code to write. One demo (GG) runs in the **terminal** — it's
> flagged.

The three habits:

| Habit | In plain words | Demo |
|------|----------------|------|
| **Surface failures** | If a helper hits a wall, it says so — it doesn't hide it. | EE |
| **Take notes** | Jot findings in a scratchpad while exploring, so nothing's lost. | FF |
| **Save & recover** | Shrink a long session and pick up after a crash. | GG |

The files: `bigapp/` (the pretend large project, with one deliberately broken file),
`.claude/agents/checker.md` (a helper that reports failures honestly), `scratchpad.md` (the
notepad), and `CLAUDE.md` (the rules).

---

## Demo EE — failures show up, they don't hide
The AI hands a check to a helper. The helper finds a broken config file and reports
**FAILED** with the reason — and the AI passes that straight back to you, instead of quietly
moving on. **The point:** a delegate who hits a wall should tell you, not pretend it's done.

## Demo FF — take notes while exploring
Mapping a big project from memory is how you miss things. The AI writes what it finds — file
paths, what each area does — into `scratchpad.md` as it goes, then answers from those notes.
**The point:** notes beat memory on anything large.

## Demo GG — save progress and recover *(terminal)*
Long sessions can hit limits or the app can close. `/compact` shrinks a long history down to
the essentials before it overflows, and resuming brings you back where you left off after a
crash. **The point:** long work shouldn't be one power-cut away from gone.

---

## Why a non-tech person should care
The scary thing about handing real work to an AI is the *silent* failure — it says "done"
but quietly skipped a broken step, and you find out later. These habits remove that fear:
failures are loud, progress is written down, and a crash is a shrug, not a disaster. That's
what makes it safe to trust an AI with big, multi-step jobs.
