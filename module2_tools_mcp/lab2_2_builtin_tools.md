# Lab 2.2 (optional) — Built-in Claude Code tools + incremental exploration

**Goal on screen:** show that Claude Code explores a codebase *surgically* —
Grep → Read only the hit → Edit — instead of loading the whole repo into context.

## The built-in tools
| Tool | What it does | Demo line |
|------|--------------|-----------|
| `Glob` | Find files by pattern | "Find all test files" → `**/*.test.ts` / `test_*.py` |
| `Grep` | Search file *contents* (ripgrep) | "Where is `run_agent` defined?" |
| `Read` | Read one file (or a slice) | Read only the file Grep pointed at |
| `Edit` | Exact-string replace in a file | One surgical change |
| `Write` | Create / overwrite a file | New file only |

## Demo script (run these as prompts inside Claude Code)

1. **Glob first — don't open everything**
   > "Glob all Python lab files in this repo."
   → returns the file list; nothing loaded yet.

2. **Grep to locate, not browse**
   > "Grep for `def run_agent` across the repo."
   → one hit: `module1_agentic/lab1_1_agentic_loop.py`.

3. **Read only the hit**
   > "Read just that file."
   → context stays small; you didn't read 12 other files.

4. **Edit surgically**
   > "In that file, change `max_turns=8` to `max_turns=10`."
   → single exact-string Edit, no rewrite of the file.

## The point to make to the audience
- Each step **narrows** scope. Glob → list, Grep → location, Read → one file,
  Edit → one line.
- This is the opposite of "paste the whole repo into the prompt." It keeps the
  context window clean and the agent fast and accurate.
