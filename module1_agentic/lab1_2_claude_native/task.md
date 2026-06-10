# Base task (Demo F — resume / fork + structured summaries)

Use this as the shared starting point that two forked sessions will build on.

> Design a rate limiter for our API gateway. First, propose exactly **two** candidate
> approaches at a high level (one paragraph each) and name them. Do not pick a winner
> yet — we will explore each one separately.

Expected two approaches (so the forks are predictable in the demo):
- **Path A — token bucket:** smooths bursts; refill rate + bucket size.
- **Path B — sliding window:** strict per-window request cap; more even, less bursty.

After this base turn you will `/compact` a structured summary, then fork the session
twice (one per approach) so each path diverges without losing the shared groundwork.
See `RUNBOOK.md` → Demo F for the exact commands.
