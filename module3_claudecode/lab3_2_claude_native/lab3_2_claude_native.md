# Lab 3.2 — Claude-native track *(mandatory — targeted behavior)*

Lab 3.2 is pure Claude Code **workflow**: loading rules by path, designing with Plan mode
before risky edits, and using the Explore subagent to map code first. Like Labs 2.2/3.1,
it was **already** native (no Python script). This folder packages the three ideas into the
same self-contained, hands-on format as the other tracks — with a small **multi-file** auth
app so the Plan-mode migration and the Explore survey are real, not toy.

> **Setup:** launch Claude Code **from this folder**
> (`module3_claudecode/lab3_2_claude_native/`) so its `CLAUDE.md` hierarchy loads. No API
> key, no MCP server. Full step-by-step is in `RUNBOOK.md`.

The three concepts:

| Concept                                   | Where it shows up                                   | Demo |
|-------------------------------------------|-----------------------------------------------------|------|
| Path-specific rules load by glob          | `src/auth/CLAUDE.md` (strict) vs `src/utils/CLAUDE.md` (relaxed) | P |
| Plan mode before risky changes            | the `sha256 → bcrypt` migration across `src/` + tests | Q  |
| Explore subagent maps unfamiliar code     | the `auth` / `api` / `utils` tree                   | R    |

Demos are lettered **P/Q/R**, continuing A–O. (The original `module3_claudecode/lab3_2_planmode.md`
still works; this folder is the packaged, self-contained version.)

---

## Demo P — path-specific rules load by glob
Strict auth rules live in `src/auth/CLAUDE.md` and load **only** under `src/auth/**`; the
relaxed `src/utils/CLAUDE.md` loads only under `src/utils/**`. **Point at:** adding a helper
to `src/utils/` (light rules) vs `src/auth/` (strict: hashing, no secret logging,
failure-path test) — same repo, different rules by path, so context stays relevant.

---

## Demo Q — Plan mode before risky changes
For a multi-file migration (`sha256 → salted bcrypt-style`, touching `login.py`, its callers
`session.py` / `signup.py`, and `tests/test_login.py`), Plan mode designs a step-by-step
plan and lands **no edits** until you approve. **Point at:** the blueprint appearing with
zero files changed, then approval gating execution.

---

## Demo R — Explore subagent maps unfamiliar code first
Before proposing where a new validation layer should go, the Explore subagent surveys how
`auth`, `api`, and `utils` fit together — read-only. **Point at:** a structure map produced
first, so the change is planned on solid ground instead of guesswork.

---

## Talking point
These three are about **targeting behavior**: rules scoped to where they matter, a design
gate before risky edits, and understanding before changing. Together they keep Claude
focused, safe, and well-informed on real, multi-file work.
