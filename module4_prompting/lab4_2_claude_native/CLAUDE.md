# Lab 4.2 (Claude-native) — structured output rules

This lab is about getting **clean, machine-ready answers** — data you could drop straight
into a spreadsheet or CRM — instead of a paragraph.

When scoring leads in this folder:
- **Always record each score with the `record_score` tool** (it's the "form"). Don't just
  write the answer as prose.
- Each call needs: `name`, a `score` that is a **whole number 0-10** (see `rubric.md`),
  and a short `reason`.
- **If `record_score` returns an error**, read the message, fix the value, and call it
  again — keep going until it's accepted. Never leave a lead unrecorded because of a
  rejected value.
