# Lab 5.1 — Managing Context *(mandatory — plain-English lab)*

**In one sentence:** over a long conversation, keep the AI sharp by **remembering the key
facts, not drowning in data, and asking instead of guessing**.

The running story: you're a support agent handling **one customer's case** all day —
Maria Lopez, who has two orders and a broken desk lamp.

> **Setup:** open this folder (`module5_context/lab5_1_claude_native/`) in Claude Code and
> follow `RUNBOOK.md`. No code — just plain notes and a sample order list.

The three habits:

| Habit | In plain words | Demo |
|------|----------------|------|
| **Pin the key facts** | Keep a sticky note so important details survive a long chat. | BB |
| **Don't drown in data** | Pull the few rows you need, not the whole 500-row file. | CC |
| **Ask, don't guess** | When something's unclear, ask one quick question. | DD |

The files: `customer_case.md` (the scenario), `case_file.md` (the sticky note the AI keeps
updated), `orders_export.csv` (a 500-row order list), and a `/case-fact` shortcut to pin a
fact in one step.

---

## Demo BB — pin the key facts so they survive
Long chats make AIs (and people) forget early details. The AI writes the important facts —
customer, **order ID**, the issue — into `case_file.md` and reads them back when needed. So
even after a long detour, the order ID is still right there. **The point:** a small,
deliberate "memory note" beats hoping it remembers.

## Demo CC — don't drown in data
The order list has 500 rows. If the AI reads the whole thing every time, it gets slow and
loses focus. Instead it **looks up just the order you asked about** and reports the few
fields that matter. **The point:** pull one folder, don't photocopy the whole cabinet.

## Demo DD — ask, don't guess
Maria has **two** orders. If she says "cancel my order," guessing could cancel the wrong
one. The AI asks **which order** before doing anything. **The point:** one quick question is
far cheaper than a wrong refund.

---

## Why a non-tech person should care
Anyone who's had to repeat their order number to a call centre three times knows the pain of
an assistant that forgets. These three habits are exactly what a *good* human agent does —
keep notes, look up only what's needed, and check before acting. Setting them up once is what
lets an AI handle long, real conversations without losing the plot or making an expensive
mistake.
