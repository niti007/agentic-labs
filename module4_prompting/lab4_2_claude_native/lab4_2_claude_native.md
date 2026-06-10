# Lab 4.2 — Enforcing Structure *(mandatory — plain-English lab)*

**In one sentence:** make the AI **fill out a form, not write an essay** — so its answers
come back as clean data you can drop into a spreadsheet, check automatically, and trust.

The running example continues Module 4's story: **scoring sales leads** 0-10. Every answer
should be `{ name, score, reason }` — nothing more, nothing messy.

> **Setup:** launch Claude Code from this folder (`module4_prompting/lab4_2_claude_native/`)
> and approve the `scoring` tool when asked. Then follow `RUNBOOK.md`. You never touch code —
> you just watch the AI fill the form.

The three habits:

| Habit | In plain words | Demo |
|------|----------------|------|
| **Force a structure** | Give the AI a form with fixed boxes it *must* fill. | Y |
| **Check the data** | The form rejects nonsense (a score of 15, or a blank reason). | Z |
| **Auto-fix and retry** | When it's rejected, the AI reads why and corrects itself. | AA |

The files: `lead_scoring_server.py` (the "form" tool — you don't edit it), `.mcp.json`
(connects it), `leads.md` (today's leads to score), `rubric.md` (what 0-10 means),
`CLAUDE.md` (always use the form; fix and retry if rejected).

---

## Demo Y — make it fill a form, not write an essay
Ask plainly and the AI writes a nice paragraph — useless if you wanted a tidy row in a
spreadsheet. The `record_score` "form" forces every answer into the same three boxes:
name, score, reason. **The point:** structured output is what lets AI feed real systems
(CRM, spreadsheet, dashboard) without a human re-typing it.

## Demo Z — let the form reject bad data
Try to record a score of **15**, or "high", or leave the reason blank — the form bounces it
back with a clear reason. Bad data never reaches your spreadsheet. **The point:** a check at
the door beats discovering broken data later.

## Demo AA — let it fix itself
When the form bounces an answer back, the AI reads the message ("score must be 0-10"),
corrects the value, and submits again — no human needed. **The point:** a quick
check-and-retry loop means the output is *always* valid by the time you see it.

---

## Why a non-tech person should care
The moment AI output flows into a real system — a CRM, a spreadsheet, an automated email —
one stray paragraph or a "score: very high" jams the whole machine. Forcing a form,
checking it at the door, and letting the AI fix its own mistakes is what makes AI safe to
plug into your tools. It's the difference between "neat demo" and "I can actually automate
this."
