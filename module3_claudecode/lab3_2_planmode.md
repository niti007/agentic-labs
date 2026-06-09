# Lab 3.2 (mandatory) — Path-specific rules + Plan mode + Explore subagent

Three things to show live, all inside Claude Code, using this `module3_claudecode/` folder.

---

## Part A — Path-specific rules load by glob
**Show that the strict auth rules fire only under `src/auth/**`.**

1. Ask Claude to edit `src/utils/format.py` (relaxed path):
   > "Add a `to_percent` helper to src/utils/format.py."
   → Claude follows the light `src/utils/CLAUDE.md` rules.

2. Now ask it to touch auth:
   > "Add a `reset_password` function to src/auth/login.py."
   → Claude pulls in `src/auth/CLAUDE.md`: it will insist on hashing, no secret
     logging, and a failure-path test. **Point at the difference in behavior.**

The takeaway: same repo, different rules by path — context stays relevant.

---

## Part B — Plan mode before risky changes
**Show that Plan mode designs first and lands NO edits until you approve.**

1. Enter Plan mode (Shift+Tab cycles modes, or `/plan` depending on version).
2. Give a multi-file task:
   > "Migrate src/auth/login.py from sha256 to a salted bcrypt-style API and
   >  update every caller and test."
3. Claude produces a step-by-step plan — **no files change yet**. Show the plan.
4. Approve it. Only now does execution begin.

The takeaway: for migrations / multi-file changes, you review the blueprint
before any edit touches disk.

---

## Part C — Explore subagent maps unfamiliar code first
**Show surveying before proposing changes.**

> "Use the Explore subagent to map how auth and utils are structured in
>  module3_claudecode before suggesting where a new validation layer should go."

The Explore agent fans out (read-only), reports the structure, and *then* you
plan the change on solid ground instead of guessing.

---

## What the audience should remember
- **Rules follow paths** → relevant context, no noise.
- **Plan mode** → design + approval gate before risky edits.
- **Explore** → understand first, change second.
