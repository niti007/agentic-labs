# Lab 3.3 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab3_3_claude_native.md` (the concept handout). Lab 3.3 is **optional**. This lab is about
**iterative workflows & CI/CD**: a TDD refinement loop, headless Claude Code in a pipeline,
and structured JSON parsed into a pass/fail gate.

---

## Why this lab at all? (read this first)

The earlier labs used Claude *interactively*. Lab 3.3 is the leap to **building Claude into
a pipeline** — so quality checks run automatically, not just when someone remembers. Three
pieces:

- **TDD loop** — write/keep failing tests as the spec, then iterate the implementation
  until green. The test, not a vibe, decides when you're done.
- **Headless Claude Code** — `claude -p` runs one prompt non-interactively, so Claude can
  be a *step in a script or CI job*, no human at the keyboard.
- **Structured JSON output** — `--output-format json` makes the result machine-readable, so
  a downstream step can turn a review into a hard pass/fail gate.

Unlike the earlier Module 3 labs, this one has a **real, runnable pipeline**: `run_review.ps1`
uses your `ANTHROPIC_API_KEY` from `.env` to do a genuine headless review locally. Each demo
ends with **"Where this is written (the files)"**.

Demos continue the lettering from the earlier tracks (A–R), so this lab is **S/T/U**.

---

## Setup (once)
1. `cd` into **this** folder:
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module3_claudecode\lab3_3_claude_native"
   ```
2. Tests run with no key: `py -m pytest -q` → should be GREEN as shipped.
3. For the **real** headless run (Demo T live), you need:
   - the `claude` CLI on PATH, and
   - `ANTHROPIC_API_KEY` in the repo `.env` (`agentic-labs/.env`). `run_review.ps1` loads it
     for you.
   The JSON-gate demo (U) and the TDD demo (S) need **no key**.

> **Security:** the real key lives only in `.env` (local) or a GitHub **repo secret** (CI) —
> never in a committed file. Make sure `.env` is git-ignored.

---

## Demo S — TDD / refinement loop

> **Why bother, isn't this automatic?** Without a test, "done" is a judgment call. A failing
> test turns the spec into something objective: Claude iterates until it's green, and you
> know exactly when the work is finished. This is the tightest, most reliable refinement
> loop there is.

### What we are doing (the scenario)
We break a function, watch the suite go red, and let Claude refine the implementation until
the failing test passes — without touching the test.

### The files involved
| File            | Role                                                    |
|-----------------|---------------------------------------------------------|
| `calc.py`       | Implementation under test (`add`, `multiply`, `divide`).|
| `test_calc.py`  | The spec — 4 tests incl. divide-by-zero.                |

### Step by step
1. Show GREEN as shipped:
   > (terminal) `py -m pytest -q`  → 4 passed.
2. **Go RED.** Break `divide` — paste in Claude Code:
   > In `calc.py`, replace the body of `divide` with `raise NotImplementedError`.
   Then `py -m pytest -q` → the divide tests FAIL.
3. **Refine to GREEN.** Paste:
   > The divide tests are failing. Make them pass — fix `calc.py`, don't change the tests.
   Claude reads the failures, restores correct `divide` logic (incl. the zero check), and
   reruns until GREEN.

### Point at the screen (the lesson)
- The **test was the spec**; Claude iterated the *code* until the spec was met. It didn't
  edit the test to cheat.
- Say: "Write the failing test first, then let the loop close it. That's TDD with an agent —
  fast, and the finish line is objective."

### Where this is written (the files)
- **The spec** is `test_calc.py`; **the code under test** is `calc.py`. The red→green loop
  itself is Claude Code's agentic loop — you supply the failing test, it iterates.

---

## Demo T — headless Claude Code in CI/CD

> **Why bother, isn't this automatic?** Interactive Claude needs you at the keyboard. A
> pipeline can't wait for that. Headless mode (`claude -p`) makes Claude a *script step* —
> it runs the prompt, emits a result, and exits, so it can review every PR automatically.

### What we are doing (the scenario)
We run a real, no-human review: load the API key, run the tests, have Claude review
`calc.py` in headless mode emitting JSON, and gate on it. Then we look at how the same job
runs in GitHub Actions.

### The files involved
| File                                   | Role                                                      |
|----------------------------------------|-----------------------------------------------------------|
| `run_review.ps1`                       | **Real local pipeline** — key → tests → headless review → gate. |
| `.github/workflows/review.yml`         | Reference copy of the CI job (for reading).               |
| `agentic-labs/.github/workflows/ci-review.yml` | **Live** CI job — runs on every PR (repo root).   |

### Step by step — real local run
1. Make sure `ANTHROPIC_API_KEY` is in `agentic-labs/.env` and `claude` is on PATH.
2. From this folder, run:
   ```powershell
   .\run_review.ps1
   ```
3. Watch all four steps: key loaded → tests run → `claude -p ... --output-format json >
   review.json` (a **real** review) → `parse_output.py` prints the gate and sets the exit
   code. Open `review.json` to show the structured result.

### Step by step — wire it into GitHub Actions (real CI)
1. The live workflow already sits at the repo root: `agentic-labs/.github/workflows/ci-review.yml`
   (it triggers on `pull_request` and `workflow_dispatch`).
2. On GitHub: **Settings → Secrets and variables → Actions → New repository secret**, name
   `ANTHROPIC_API_KEY`, paste the key. (CI uses the **secret**, never the `.env`.)
3. Open a PR (or run the workflow via *Actions → ci-review → Run workflow*). The job runs
   tests, then the headless review, then the gate — green check or red X on the PR.

### Point at the screen (the lesson)
- `claude -p` ran a complete review with **no human in the loop** — locally via the script,
  and identically in CI.
- Say: "Headless mode is what lets Claude live inside automation. Same prompt, same JSON,
  whether you run it on your laptop or on every pull request."

### Where this is written (the files)
- **The local pipeline** is `run_review.ps1` (it loads the key, runs tests, calls `claude
  -p`, and gates). **The CI job** is `agentic-labs/.github/workflows/ci-review.yml` (live)
  with a reference copy in this folder's `.github/workflows/review.yml`.
- **Headless mode + `--output-format json`** are built into the `claude` CLI — you write the
  prompt and the pipeline around it.

---

## Demo U — structured JSON → pass/fail gate

> **Why bother, isn't this automatic?** A prose review can't fail a build. Automation needs a
> machine-readable verdict. Structured JSON output turns "looks fine to me" into an exit code
> a pipeline can act on — pass merges, fail blocks.

### What we are doing (the scenario)
We parse a review JSON into a gate — both outcomes — **without** needing the API, using two
shipped sample files. (Demo T produced a real `review.json`; this shows the parsing/gating
half in isolation.)

### The files involved
| File                       | Role                                                       |
|----------------------------|------------------------------------------------------------|
| `parse_output.py`          | Unwraps the JSON envelope, reads `verdict`, sets exit code.|
| `sample_review_fail.json`  | A "fail" verdict (in the `claude --output-format json` shape). |
| `sample_review_pass.json`  | A "pass" verdict.                                          |

### Step by step
1. **Fail gate** — run:
   ```powershell
   py parse_output.py sample_review_fail.json   # prints issues, "GATE: FAIL", exit code 1
   echo $LASTEXITCODE
   ```
2. **Pass gate** — run:
   ```powershell
   py parse_output.py sample_review_pass.json   # "GATE: PASS", exit code 0
   echo $LASTEXITCODE
   ```
3. (Optional) `py parse_output.py` with no arg → uses the built-in SAMPLE (a fail).

### Point at the screen (the lesson)
- Same parser, two **exit codes** — that exit code is exactly what CI keys off to pass or
  fail the build.
- Say: "Structured output is the contract between the model and your automation. JSON in,
  exit code out — no human interpreting prose."

### Where this is written (the files)
- **The gate logic** is `parse_output.py` (`verdict == "pass"` → exit 0, else exit 1; it
  also unwraps the `{"result": "<json>"}` envelope the CLI produces).
- **The sample verdicts** are `sample_review_fail.json` / `sample_review_pass.json`.

---

## Closing talking point
- **TDD loop** (Demo S) makes "done" objective — iterate until the failing test is green.
- **Headless Claude Code** (Demo T) makes Claude a pipeline step — `claude -p`, no human in
  the loop, real locally and in CI.
- **Structured JSON** (Demo U) turns a review into an exit code a gate can act on.
- Chain them and code review stops being a thing someone remembers to do and becomes a
  standard, automated pipeline step.
