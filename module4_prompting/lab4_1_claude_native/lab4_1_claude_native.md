# Lab 4.1 — Precision Prompting *(mandatory — plain-English lab)*

**In one sentence:** how you *word* your request decides how good and how consistent the
AI's answer is — so this lab shows the three wording habits that turn a flaky answer into a
reliable one.

No code. The running example is something everyone gets: **sorting incoming customer
feedback by how urgent it is**, so the worst problems get handled first.

> **Setup:** open this folder (`module4_prompting/lab4_1_claude_native/`) in Claude Code and
> follow `RUNBOOK.md`. Everything is plain text you can read and edit.

The three habits:

| Habit | In plain words | Demo |
|------|----------------|------|
| **Explicit criteria** | Spell out exactly what each label means, so the AI stops guessing. | V |
| **A few examples** | Show 3 done-right samples to lock the format and tone. | W |
| **Generalize** | Trust it to handle new, unseen cases the same sensible way. | X |

The files: `criteria.md` (the rules), `examples.md` (3 worked samples), `feedback_inbox.md`
(today's messages to sort, including a few tricky ones), and a `/triage-feedback` shortcut
that ties them together.

---

## Demo V — write down exactly what you mean
Ask vaguely ("flag the urgent ones") and the AI guesses — it flags too many (false alarms)
or misses real ones, and two runs disagree. Give it the written `criteria.md` and the
guessing stops. **The point:** clear definitions cut false alarms.

## Demo W — show a few examples to lock the format
Without examples, the answers ramble and look different every time. Add three labeled
examples and every answer comes back in the same tidy one-line format and calm tone.
**The point:** examples are the fastest way to get consistent output.

## Demo X — trust it on new cases
The inbox has messages the examples never covered (a privacy slip, a sarcastic "compliment").
Done right, the AI handles them the way the examples *imply* — not just the ones it was
shown. **The point:** good rules + good examples teach a pattern, not a script.

---

## Why a non-tech person should care
You already do this with people: a clear brief and a couple of "here's what good looks like"
examples get a new teammate producing consistent work fast. Same with AI. Spend five minutes
writing the criteria and three examples **once**, and every future answer is sharper,
consistent, and trustworthy — instead of you re-explaining and fixing it each time.
