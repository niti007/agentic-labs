# Lab 3.3 (Claude-native) — iterative workflows & CI rules

This lab demonstrates **refinement loops and CI/CD integration**: TDD red→green, headless
Claude Code in a pipeline, and structured JSON parsed into a pass/fail gate.

## TDD convention
- The failing test is the spec. Iterate on the implementation until the suite is GREEN —
  don't change the tests to match buggy code.
- Run the suite with `py -m pytest -q`.

## Headless + structured output
- `claude -p "<prompt>"` runs one prompt non-interactively (for scripts/CI).
- `--output-format json` makes the result machine-readable; `parse_output.py` turns the
  verdict into an exit code (0 = pass, 1 = fail) for a gate.

## Secrets
- CI reads `ANTHROPIC_API_KEY` from a **repository secret**, never from a committed file.
- The local pipeline (`run_review.ps1`) reads it from the repo `.env`, which must stay
  untracked/ignored.
