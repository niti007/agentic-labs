# Lab 4.1 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script. Companion to `lab4_1_claude_native.md`. Lab 4.1 is
**mandatory**. **No code in this lab** — it's about *how you word a request* so the AI
gives sharp, consistent answers. The running example is **sorting customer feedback by
urgency** (so the worst problems get handled first).

---

## Why this lab at all? (say this first, in plain words)

Think about asking a brand-new teammate to "flag the important complaints." Without a brief,
one person flags everything, another flags nothing, and you spend the day fixing it. AI is
exactly the same: **vague request → vague, inconsistent answer.**

This lab shows the three simple wording habits that fix that — and they're the same habits
you'd use to brief a person:
1. **Say exactly what you mean** (write down what "urgent" actually means).
2. **Show a couple of examples** of a good answer.
3. Then you can **trust it on new situations** you didn't spell out.

Five minutes of setup, done once, and every answer after that is reliable. Demos are
lettered **V/W/X**, continuing the earlier labs (A–U).

---

## Setup (once)
1. Open this folder in Claude Code:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module4_prompting\lab4_1_claude_native"
   claude
   ```
2. Open `feedback_inbox.md` on screen so the audience can see the messages we'll sort.
3. That's it — no install, no key. Everything is plain text.

---

## Demo V — write down exactly what you mean (cut the false alarms)

> **Why do we need this?** If you don't define "urgent," the AI guesses. It either cries
> wolf (marks calm messages as emergencies) or misses a real one. Writing down the rule
> once stops the guessing — fewer false alarms, nothing important missed.

### Step by step
1. **Ask the vague way first.** Paste:
   > Here are some customer messages (in `feedback_inbox.md`). Just flag the urgent ones for me.
   Watch it guess: it may over-flag, under-explain, or label things differently than you
   would. Run it twice — notice the answers don't fully match.
2. **Now give it the written rules.** Paste:
   > Now sort the same messages using the exact rules in `criteria.md`. Use the labels
   > CRITICAL, MAJOR, MINOR as defined there.
   The answers tighten up: only true cancellations / legal / money / safety land as
   CRITICAL, and the reasons match your definitions.

### Point at the screen
- Vague version = inconsistent, too many "urgent." Rules version = clean and repeatable.
- Say: "We didn't make the AI smarter — we just told it exactly what we meant. That one
  written page is what cut the false alarms."

### Where this is written
- The rules are in **`criteria.md`** — plain definitions of CRITICAL / MAJOR / MINOR, plus
  a "when unsure, pick the higher one" tie-breaker.

---

## Demo W — show a few examples (lock the format and tone)

> **Why do we need this?** Even with good rules, the AI might answer in paragraphs one time
> and bullet points the next, in a chirpy tone or a cold one. Three quick "here's a good
> answer" examples lock the format and tone so every result looks the same — easy to scan,
> easy to hand to the team.

### Step by step
1. **Without examples.** Ask:
   > Using `criteria.md`, label each message in `feedback_inbox.md` with a severity and a
   > short reason.
   Note how the *shape* of the answer wobbles — different length, different wording.
2. **With examples.** Paste:
   > Now follow the three worked examples in `examples.md` exactly — same one-line format
   > and the same calm tone — for every message.
   Every answer snaps to the same tidy line:
   `SEVERITY | one-line reason | suggested first action`.

### Point at the screen
- Before: each answer looks a little different. After: identical format, calm tone, every
  time.
- Say: "We didn't write a long style guide. We just showed three good examples — that's the
  fastest way to get consistency out of AI *or* a new hire."

### Where this is written
- The examples are in **`examples.md`** — three labeled messages that fix the exact format
  and tone.

---

## Demo X — trust it on new, unseen cases (generalize)

> **Why do we need this?** You can't write an example for every possible message. The real
> test is whether the AI handles a situation you *didn't* show it, the way your rules imply.
> Done right, it applies the spirit of the rules — so you don't have to babysit every case.

### Step by step
1. Run the bundled shortcut so rules + examples are applied together:
   > /triage-feedback
   (It reads `criteria.md` + `examples.md` and sorts the whole `feedback_inbox.md`.)
2. **Look at the three tricky messages** (4, 5, 6 in the inbox) — none are spelled out in
   the examples:
   - **#4 "This is honestly so frustrating."** — vague. Watch it avoid crying CRITICAL on no
     evidence (likely MAJOR, or it asks for detail) instead of guessing an emergency.
   - **#5 the sarcastic "great job… deleted all my templates."** — watch it read the real
     meaning (data loss + an angry customer) rather than the polite-sounding words.
   - **#6 "I can see another customer's invoices."** — the word "privacy" never appears in
     the examples, yet it should land as **CRITICAL** because the rules say security/privacy
     is critical. This is the money shot: it applied the *spirit*, not the script.

### Point at the screen
- The AI handled cases it was never shown, the way the rules intended.
- Say: "This is the payoff. Good criteria + a few examples don't just cover the samples —
  they teach a *pattern* the AI carries to brand-new situations. That's what makes it
  trustworthy enough to actually save you time."

### Where this is written
- Nothing extra — generalizing is what the AI does once `criteria.md` and `examples.md`
  give it a clear pattern. The `/triage-feedback` shortcut (in `.claude/commands/`) just
  bundles them so it's one click.

---

## Closing talking point (for the skeptic in the room)
- **Criteria** (V) stop the guessing — fewer false alarms.
- **Examples** (W) lock the format and tone — consistent, scannable answers.
- **Generalizing** (X) means it handles new cases sensibly — so you set it up once, not
  every time.
- It's the same thing that makes a good brief to a person work. Five minutes writing the
  rules and three examples turns AI from "nice but unpredictable" into "reliable enough to
  delegate to."
