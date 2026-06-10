# Lab 3.3 — Claude-native track *(optional — workflows & CI/CD)*

Lab 3.3 is about turning refinement into a **pipeline**: a TDD loop, headless Claude Code
in CI/CD, and structured JSON output that automation can gate on. Like the other Module 3
labs it was already native; this folder packages the three ideas into the standard
self-contained format — and includes a **real, runnable** local pipeline that uses your
`ANTHROPIC_API_KEY` from `.env`.

> **Setup:** for the TDD and gate demos, just need `py` + pytest (no key). For the **real**
> headless run (`run_review.ps1` / CI), you need the `claude` CLI and an
> `ANTHROPIC_API_KEY` — in the repo `.env` for local, or a **repo secret** for GitHub
> Actions. Full step-by-step is in `RUNBOOK.md`.

The three concepts:

| Concept                                  | Where it lives                                       | Demo |
|------------------------------------------|------------------------------------------------------|------|
| TDD / interview-style refinement loop    | `calc.py` + `test_calc.py`                           | S    |
| Headless Claude Code in CI/CD            | `run_review.ps1` (local) + `.github/workflows/`      | T    |
| Structured JSON output → pass/fail gate  | `parse_output.py` + `sample_review_*.json`           | U    |

Demos are lettered **S/T/U**, continuing A–R. (The original `lab3_3_tdd_ci/` assets still
work; this folder is the packaged, self-contained version with a live local pipeline.)

---

## Demo S — TDD / refinement loop
Break `calc.divide` (e.g. `raise NotImplementedError`) → `py -m pytest` goes **RED** → ask
Claude to make the failing test pass → it iterates until **GREEN**. **Point at:** the
failing test as the spec, and Claude refining the implementation (not the test) until it's
satisfied.

---

## Demo T — headless Claude Code in CI/CD
`claude -p "<prompt>" --output-format json` runs one prompt non-interactively and emits a
machine-readable result — perfect for a pipeline. **`run_review.ps1`** does this for real
locally (loads the key from `.env`, runs tests, runs the headless review, gates the
result). The repo-root **`.github/workflows/ci-review.yml`** does the same on every PR
(using the `ANTHROPIC_API_KEY` repo secret). **Point at:** a real review running with no
human in the loop.

---

## Demo U — structured JSON → pass/fail gate
`parse_output.py` unwraps the `claude --output-format json` envelope, reads the `verdict`,
and exits 0 (pass) or 1 (fail) — so CI can gate on it. Two sample files demonstrate both
outcomes with no key. **Point at:** `GATE: FAIL` (exit 1) vs `GATE: PASS` (exit 0) — JSON
turns a model's review into an automatable decision.

---

## Talking point
This is the leap from *using* Claude interactively to *building it into your pipeline*: a
test loop that refines until green, a headless run that needs no human, and structured
output a gate can act on. That's how agentic review becomes a standard pipeline step.
