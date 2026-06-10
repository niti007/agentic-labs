# Lab 1.1 (Claude-native) — coordinator rules

You are the **coordinator** (the hub) for this lab. Claude Code's own agentic loop
and the subagents in `.claude/agents/` are the moving parts the trainee is watching.

## Routing (hub-and-spoke)
For a single-purpose request, delegate to the matching specialist subagent via the
Task tool instead of answering yourself:
- summarize / shorten / condense  → `summarizer`
- translate to another language    → `translator`
- check / is-this-valid / verify    → `validator`

Route to exactly one specialist and report which one you picked and why (one line),
then return its result. This mirrors the forced `route()` decision in
`lab1_1_orchestrator.py`.

## Document processing (ordered pipeline)
For any "process this document / invoice" request, ALWAYS run the pipeline in order:
1. `extractor` first → produces JSON facts.
2. `analyzer` second → receives **only** the extractor's JSON, never the raw doc.
Never let analysis start before extraction returns. The `/pipeline` command encodes
this; follow the same order if asked directly.
