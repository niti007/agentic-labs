# Lab 5.1 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script. Companion to `lab5_1_claude_native.md`. Lab 5.1 is
**mandatory**. Plain idea: over a **long** conversation, keep the AI sharp by **remembering
the key facts, not drowning in data, and asking instead of guessing**. Running story: a
support agent handling one customer (Maria Lopez) all day. **No code.**

---

## Why this lab at all? (say this first, in plain words)

You've all phoned a call centre, given your order number, been transferred, and been asked
for the order number *again*. Annoying — and exactly what a careless AI does over a long
chat: it forgets early details, it tries to read everything at once and gets sluggish, and
it guesses when it should ask.

This lab shows the three habits a *good* support agent already has, taught to the AI:
1. **Keep a sticky note** of the key facts so nothing important gets lost.
2. **Look up only what you need** instead of re-reading the whole filing cabinet.
3. **Ask a quick question** when something's unclear, instead of guessing.

Demos are lettered **BB/CC/DD**, continuing the earlier labs.

---

## Setup (once)
1. Open this folder in Claude Code:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module5_context\lab5_1_claude_native"
   claude
   ```
2. Open `customer_case.md` and `case_file.md` on screen so people can see the scenario and
   the (empty) sticky note we'll fill.

---

## Demo BB — pin the key facts so they survive a long chat

> **Why do we need this?** In a long conversation the early details slip away. If the AI
> writes the important facts down in one place and checks them, it never loses the order
> number — no matter how long you talk.

### Step by step
1. **Start the case and pin the facts.** Paste:
   > Read `customer_case.md`. Record the key facts (customer, email, order IDs, the issue)
   > into `case_file.md`, then show me the pinned facts.
   The sticky note (`case_file.md`) fills in — customer Maria, order **A-3002**, broken lamp.
   *(Shortcut: you can also pin a single fact any time with `/case-fact she prefers a refund over a replacement`.)*
2. **Go on a long detour.** Ask several unrelated things to simulate a long chat:
   > What's our general return policy? … Draft a friendly apology paragraph. … What are
   > common causes of shipping damage?
3. **Now test the memory.** Paste:
   > Remind me — which order is this case about, and what's the customer's email?
   It answers **A-3002 / maria.lopez@example.com** correctly, because it reads the sticky
   note — not because it happened to remember.

### Point at the screen
- After a long detour, the key facts are still exact. Open `case_file.md` to show *why* —
  they were written down, not left to memory.
- Say: "This is the difference between an agent that makes you repeat your order number and
  one that just… remembers. It kept a note."

### Where this is written
- The sticky note is **`case_file.md`**; the rule "always read and update it" is in
  **`CLAUDE.md`**; `/case-fact` (in `.claude/commands/`) pins a fact in one step.

---

## Demo CC — don't drown in data (pull only what you need)

> **Why do we need this?** The order list has 500 rows. If the AI swallows the whole file
> every time, it gets slow and distracted. A good agent looks up the one order you asked
> about. Same result, a fraction of the effort — and it scales to files far too big to read
> whole.

### Step by step
1. Paste a targeted question:
   > Using `orders_export.csv`, what's the status and amount of order A-3002?
   Watch it **search** the file for that one order and answer with just the few fields:
   *A-3002 — Desk lamp — $39.00 — shipped.*
2. (Optional contrast) Say:
   > How many rows are in that file, and did you need to read all of them to answer?
   It'll confirm it only needed the matching row, not all 500.

### Point at the screen
- It pulled one row out of 500. It did **not** dump the whole table into the chat.
- Say: "You don't photocopy the whole filing cabinet to answer one question. Neither should
  the AI — especially when the 'cabinet' is too big to hold at all."

### Where this is written
- The rule "don't read the whole file; search for what you need" is in **`CLAUDE.md`**. The
  big file is **`orders_export.csv`** (500 rows).

---

## Demo DD — ask, don't guess

> **Why do we need this?** Maria has *two* orders. If she says "cancel my order" and the AI
> guesses, it might cancel the wrong one — a real, costly mistake. A quick "which one?" is
> always cheaper than undoing a wrong action.

### Step by step
1. Paste the deliberately ambiguous request:
   > Maria says: "Please just cancel my order." Go ahead and cancel it.
2. Watch the AI **stop and ask** — something like: "You have two orders, A-3001 (standing
   desk) and A-3002 (desk lamp). Which one should I cancel?" — instead of picking one.
3. Answer it ("A-3002") and watch it proceed correctly.

### Point at the screen
- It refused to guess on an action that's hard to undo, and asked one short question.
- Say: "This is judgement, not timidity. On anything irreversible — a refund, a cancel, a
  send — one clarifying question saves a mess."

### Where this is written
- The rule "if two readings are plausible, ask one short question before acting" is in
  **`CLAUDE.md`**. The two-orders setup is in `customer_case.md`.

---

## Closing talking point
- **Pin the facts** (BB) so long chats don't lose the plot.
- **Pull only what you need** (CC) so the AI stays fast and can handle huge data.
- **Ask, don't guess** (DD) so irreversible actions are never a coin flip.
- All three are just what a great human agent does. Teach them once and the AI can handle
  long, real conversations without forgetting, stalling, or guessing wrong.
