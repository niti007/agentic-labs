# Lab 3.1 — Claude-native track *(mandatory — configuring Claude Code)*

Lab 3.1 is pure Claude Code **configuration** — the CLAUDE.md hierarchy, custom slash
commands, and Skills. Like Lab 2.2, it was **already** native (there was never a Python
script), so this folder simply **packages** the three ideas into the same self-contained,
hands-on format as the other native tracks, with a small sample codebase the config acts
on.

> **Setup:** launch Claude Code **from this folder**
> (`module3_claudecode/lab3_1_claude_native/`) so it loads this lab's `CLAUDE.md`
> hierarchy, `.claude/commands/`, and `.claude/skills/`. Full step-by-step is in
> `RUNBOOK.md`. No API key, no MCP server — just config.

The three concepts:

| Concept                                       | Where it lives                                    | Demo |
|-----------------------------------------------|---------------------------------------------------|------|
| CLAUDE.md hierarchy + `@import` + modular rules | `CLAUDE.md`, `src/auth/CLAUDE.md`, `src/utils/CLAUDE.md` | M |
| Custom slash command                          | `.claude/commands/review.md`                      | N    |
| Packaged Skill                                | `.claude/skills/generate-api-docs/SKILL.md`       | O    |

Demos are lettered **M/N/O**, continuing A–L from the earlier native tracks. (The original
Module 3 assets under `module3_claudecode/` still work unchanged; this folder is the
packaged, self-contained version of Lab 3.1.)

---

## Demo M — CLAUDE.md hierarchy, @import, modular rules
Claude Code loads memory in tiers: your global `~/.claude/CLAUDE.md`, then this repo's
`CLAUDE.md`, then **path-specific** files that apply only under their directory. This
folder's repo `CLAUDE.md` carries the testing convention and an `@./src/auth/CLAUDE.md`
import; `src/auth/CLAUDE.md` is **strict** (security), `src/utils/CLAUDE.md` is
**relaxed**. **Point at:** the `@import` line pulling auth rules in, and the same repo
applying *different* rules to `src/auth/` vs `src/utils/`.

---

## Demo N — custom slash command (`/review`)
A slash command packages a repeatable action. `/review` (in `.claude/commands/review.md`)
runs the team's standard checklist — correctness, security, tests, readability,
consistency — and ends with APPROVE / REQUEST CHANGES. **Point at:** one invocation
running the whole checklist on a diff, instead of re-typing it every time.

---

## Demo O — packaged Skill (`generate-api-docs`)
A Skill packages a whole workflow that Claude invokes when relevant. Asking "generate API
docs for `src/`" triggers `generate-api-docs` (in `.claude/skills/`), which turns each
public function into a consistent `docs/API.md`. **Point at:** one skill producing the
same structured docs every time — and it's shareable across projects.

---

## Talking point
This is how you turn Claude Code from a general assistant into **your team's** assistant:
layered rules so it follows your conventions automatically, commands so repeatable actions
are one keystroke, and skills so whole workflows travel with the repo. Configuration is
what makes the tool consistent across people and projects.
