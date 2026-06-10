# Lab 5.2 (Claude-native) — resilient work rules

This lab is about not falling over on big or long jobs: make failures **visible**, take
**notes** so you don't get lost, and **save progress** so a crash isn't a disaster.

## Surface failures — never hide them
- When you hand work to a helper (a subagent) and it reports **FAILED**, surface that
  failure to me clearly, with the reason. **Never** continue as if it worked, and never
  quietly skip it. A hidden failure is worse than a loud one.

## Take notes while exploring
- When mapping or exploring the `bigapp/` project, write discovered file paths and short
  findings into `scratchpad.md` as you go, then answer from those notes. Don't try to hold
  the whole project in your head at once.
