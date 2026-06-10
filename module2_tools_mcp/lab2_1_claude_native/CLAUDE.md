# Lab 2.1 (Claude-native) — tool & error-handling rules

This lab demonstrates **designing reliable tools**: clear interfaces that drive correct
selection, structured errors that drive recovery, and scoping tool access. The tools
live in a local MCP server (`shop`, see `.mcp.json`); Claude Code calls them like
built-ins.

## Tool selection (Demo G)
The `shop` server exposes `search_orders` (a customer's past purchases / order status)
and `search_products` (the catalog of items to buy). Pick the tool whose
name+description matches the request; don't guess.

## Error handling for `get_order` (Demo H)
`get_order` returns a JSON object with `isError`, `isRetryable`, and `content`. Follow
this policy:
- `isError: true` **and** `isRetryable: true`  → the failure is transient (e.g. a 504
  timeout). **Call `get_order` again** (a couple of times) until it succeeds.
- `isError: true` **and** `isRetryable: false` → the failure is permanent (e.g. a 404
  not-found). **Stop immediately** and report it; do not retry.
- `isError: false` → success; use the `content`.

## Classification is scoped (Demo I)
Sentiment classification is delegated to the `classifier` subagent, which has access to
**only** the `label` tool. Route "classify / sentiment" requests to it.
