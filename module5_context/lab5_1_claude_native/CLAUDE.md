# Lab 5.1 (Claude-native) — managing context rules

This lab is about staying sharp over a **long** conversation: remember the key facts, don't
drown in data, and ask instead of guessing.

## Keep the case facts pinned
- Read `case_file.md` before answering, and **write key facts into it** as soon as you learn
  them (customer, email, order ID(s), the issue, any promise made).
- Never re-ask the customer for something already pinned in the case file.

## Don't drown in data
- `orders_export.csv` is large (~500 rows). **Do not read the whole file** into the
  conversation. Search for the specific order or customer and report only the few fields
  that answer the question.

## Ask, don't guess
- If a request could reasonably mean two different things (for example, the customer has two
  orders and says "cancel my order"), **ask one short clarifying question** instead of
  guessing. A wrong guess on a real action (refund, cancel) is worse than a quick question.
