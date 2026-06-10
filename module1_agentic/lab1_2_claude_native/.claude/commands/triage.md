---
description: ADAPTIVE decomposition — branch per support ticket, one action at a time
---

Run **adaptive** triage on a support ticket. Unlike the fixed invoice flow, the steps
are **not** known in advance — you decide the single next action each turn based on the
ticket, then continue until the case is resolved or escalated. Different tickets should
take different paths.

Ticket to triage: $ARGUMENTS
(If nothing was given, read `tickets.md` and triage the first ticket.)

## How to run it
Work one step at a time. At each step, choose exactly **one** next action from this set:
- `ask_clarifying_question` — the ticket is too vague to act on.
- `check_account` — you need to look at the customer's account/billing state.
- `issue_refund` — a refund is clearly warranted.
- `escalate_to_human` — legal/threat/edge case beyond self-serve.
- `resolve` — the case is handled; close it.

Print each step as `step N: action — one-line reason`. Keep going (re-deciding the
next action each turn) until you choose `resolve` or `escalate_to_human`, then print
`[done] ended with: <action>`. Cap at ~4 steps.

The point: the **path is chosen at runtime**, so a clear double-charge resolves fast
via `issue_refund`, a vague gripe starts with `ask_clarifying_question`, and a threat
jumps straight to `escalate_to_human`.
