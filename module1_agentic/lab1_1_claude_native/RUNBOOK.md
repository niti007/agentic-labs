# Lab 1.1 (Claude-native) — trainer RUNBOOK

On-screen, step-by-step script for running the three demos live. Companion to
`lab1_1_claude_native.md` (the concept handout). No API key — all local tools.

---

## Why this lab at all? (read this first)

Fair question: **Claude Code already does all of this by itself. So why am I
"designing" anything?**

That is exactly the point of the lab. Claude Code is a *finished* agent — the loop,
the routing, the step-ordering are already built in and hidden. But when **you build
your own agent** (with the Claude API or Agent SDK, or even by configuring Claude
Code for your team), nothing is automatic — *you* are the one who has to:

- write the loop that keeps calling tools until the task is done,
- decide which specialist handles which request,
- guarantee step 1 finishes before step 2 and pass the right context along.

So we are **not** teaching Claude to do these things — it can. We are making the
hidden machinery **visible** so you recognize the three patterns and can build and
debug them yourself. Think of it like watching an automatic gearbox in slow motion
before you're asked to build a transmission.

Each demo ends with a **"Where this is written (the files)"** section so it's clear
exactly which part is built into Claude Code (you don't write it) versus which part
*you* authored in this folder (`CLAUDE.md`, `.claude/agents/`, `.claude/commands/`).

---

## Setup (once)
1. `cd` into **this** folder, then launch Claude Code (PowerShell — the path has
   spaces/parens, so keep the quotes):
   ```powershell
   cd "C:\Users\nitis\Dropbox\My PC (LAPTOP-4LSAORKH)\Documents\Lead\agentic-labs\module1_agentic\lab1_1_claude_native"
   claude
   ```
   Open *this* folder, not the repo root, so it loads this lab's `CLAUDE.md`,
   `.claude/agents/`, and the `/pipeline` command.
2. Confirm it loaded:
   - Type `/agents` → should list `summarizer`, `translator`, `validator`,
     `extractor`, `analyzer`.
   - Type `/pipeline` in the prompt box → should autocomplete.
   - If neither shows, you opened the wrong folder.

---

## Demo A — the agentic loop (`stop_reason`)

> **Why bother, isn't this automatic?** Yes — Claude Code runs the loop for free
> here. But the loop is the single most important idea in agents: "call a tool → read
> `stop_reason` → if more work is needed, loop again; if done, stop." This demo makes
> that loop *visible* so you understand what the agent is doing. We force the answer
> to span two files so it has to loop more than once instead of finishing in one
> invisible step.

### What we are doing (the scenario)
We act like a new engineer asking a research question about a fake company's
backend. The company's docs live as four small markdown files in the `notes/`
folder. **No single file answers the question** — the answer is deliberately split
across two of them, with one file pointing you to the next. So to answer, the agent
has to *keep going*: search, read a file, realize it needs more, read another file,
and only then answer. That "keep going until done" is the agentic loop.

### What the files in `notes/` are
| File          | What's in it                                                              |
|---------------|---------------------------------------------------------------------------|
| `overview.md` | High-level intro. Says traffic policies are centralized and tells you to look in the service catalog first, then that service's own note. (The breadcrumb.) |
| `services.md` | The service catalog (a table). Says **rate limiting is owned by the `gateway` service** — but does NOT give the number. |
| `gateway.md`  | The gateway service's config. Has the actual value: **rate limit = 100 requests/minute per API key**. |
| `billing.md`  | A decoy. Unrelated service; explicitly says it has no rate-limit config, so the agent learns it's a dead end. |

**The question needs two facts from two different files:** *who owns* rate limiting
(`services.md`) and *what the limit is* (`gateway.md`). That's why one tool call
isn't enough — and that's the whole point.

### Step by step
1. Make sure you're in this folder in Claude Code (see Setup above).
2. Paste this prompt exactly:
   > Using only the files in `notes/`, tell me which service owns rate limiting and
   > what its configured limit is. Cite the files.
3. Press enter. Now **watch the tool calls stack up on screen**, roughly:
   - a **Grep** (search `notes/` for "rate limit"),
   - a **Read** of `services.md` → learns the owner is the `gateway` service,
   - a **Read** of `gateway.md` → finds the number, 100 req/min.
   (Exact order can vary — it may read `overview.md` first. That's fine; the point is
   it makes *several* tool calls, not one.)
4. Wait for the **final written answer** — something like *"The gateway service owns
   rate limiting; the limit is 100 requests/minute per API key (services.md,
   gateway.md)."* This message has **no tool call attached**.

### Point at the screen (the lesson)
- Every tool-call line = one `tool_use` turn → the loop's decision "not done yet,
  act again." Count them out loud: "that's turn one… turn two…"
- It needed **both** `services.md` (owner) and `gateway.md` (number) → so it looped
  more than once. If the answer were in one file it would've stopped after one read —
  the split data is what *makes* the loop visible.
- The final answer with **no tool call** = `stop_reason: end_turn` → the loop halts
  because the task is genuinely done.
- Say: "Each tool call was the agent reading `stop_reason: tool_use` and deciding to
  act again; the final answer was `stop_reason: end_turn` and it stopped. I wrote zero
  loop code — I just asked a question and Claude Code looped until done."

### Where this is written (the files)
- **The loop itself — `call tool → read stop_reason → loop or stop` — is NOT in any
  file in this lab. That is the whole point.** It is built into Claude Code (the
  agent harness). You don't author it; you rely on it.
- **What we authored for this demo is only the *data and the question*:** the four
  files in `notes/` (`overview.md`, `services.md`, `gateway.md`, `billing.md`) and the
  prompt you paste. Nothing else.
- So when someone asks "where did you write the loop?" the answer is: **nowhere — the
  harness runs it.** Your job in a real project is to give the agent good tools and a
  clear task; the loop is the engine underneath.

---

## Demo B — coordinator / hub-and-spoke

> **Why bother, isn't this automatic?** One big assistant *can* answer all three
> requests — but as systems grow, one giant prompt doing everything gets unreliable
> and hard to debug. The skill being taught is **decomposition**: split the work into
> small focused specialists and route to the right one. Unlike the loop in Demo A,
> the specialists and the routing rules **are things you write** — and this demo
> shows you exactly which files hold them.

### What we are doing (the scenario)
Instead of one big assistant trying to do everything, we set up a **lead agent (the
hub)** whose only job is to look at a request and hand it to the right **specialist
(a spoke)**. We have three specialists, each a tiny focused subagent:

| Subagent (in `.claude/agents/`) | Its only job                                  |
|---------------------------------|-----------------------------------------------|
| `summarizer`                    | Condense text → 2 short bullet points only.   |
| `translator`                    | Translate → output the translation only.      |
| `validator`                     | Check correctness → reply VALID/INVALID + one line why. |

The main Claude is the coordinator. The routing rules ("summarize → summarizer,
translate → translator, check → validator") live in this folder's `CLAUDE.md`, so the
coordinator knows where to send each request. We send three different requests and
watch each land on the correct specialist.

### Step by step
Paste these **one at a time** — wait for each to fully finish before the next:
1. > Translate to French: "The deployment finished successfully."
2. > Summarize: Agentic systems loop over tool calls, reading stop_reason to decide
   > whether to continue acting or to halt and answer the user.
3. > Is this valid JSON? {"name": "Nitish", "score": 9}

For each one, watch: the coordinator says which specialist it's picking, then a
**Task tool** call fires that dispatches to that subagent, then the specialist's
short result comes back.

### Point at the screen (the lesson)
- Request 1 → `translator`, request 2 → `summarizer`, request 3 → `validator`. The
  coordinator routes; it does **not** answer itself.
- The **Task tool** line is the hand-off — that's the hub delegating to a spoke.
- Each specialist has a tiny, narrow job, so its output is predictable (always
  2 bullets / translation only / VALID|INVALID).
- Say: "Small focused specialists beat one giant prompt trying to do everything —
  easier to trust, easier to debug."

### Where this is written (the files)
- **The routing rules** ("summarize → `summarizer`, translate → `translator`, check →
  `validator`") are written in **`CLAUDE.md`** in this folder, under the *"Routing
  (hub-and-spoke)"* section. That's what tells the coordinator where to send each
  request.
- **Each specialist (spoke)** is its own file in **`.claude/agents/`**:
  `summarizer.md`, `translator.md`, `validator.md`. Open one — the `description:` line
  tells Claude *when* to use it, and the body is the specialist's narrow system prompt
  (e.g. *"You are a translator. Output ONLY the translation, nothing else."*).
- **The Task-tool hand-off mechanism** (how the hub actually dispatches to a spoke) is
  built into Claude Code — like the loop, you don't write that part.

---

## Demo C — ordered pipeline + explicit context

> **Why bother, isn't this automatic?** Left to itself, an agent might analyze the
> messy raw document directly, or start analysis before extraction is really done —
> and on a bad input it might happily make something up. When **you** build a
> pipeline, you can't leave order and data-flow to chance: you *enforce* "extract
> first, then analyze only the extracted facts," and you add a guard that halts on
> empty extraction. This demo shows how to make a multi-step flow deterministic
> instead of hoping the model does it in the right order.

### What we are doing (the scenario)
We process a document (`sample_invoice.txt` — a fake invoice from "Acme Cloud
Services") in **two strict steps that must happen in order**:

| Step | Subagent    | Its job                                                          |
|------|-------------|-----------------------------------------------------------------|
| 1    | `extractor` | Read the raw invoice → pull the key fields into compact JSON.    |
| 2    | `analyzer`  | Take **only that JSON** → write a 2-line risk/cashflow note.     |

The rule we're demonstrating: **step 2 cannot start until step 1 finishes, and step
2 only ever sees step 1's output (the JSON) — never the raw invoice.** A real
pipeline (extract → then analyze) breaks if analysis runs on raw, messy input or
runs before extraction is done. The `/pipeline` command (in `.claude/commands/`)
plus the `CLAUDE.md` rules enforce this order for us — we don't rely on luck.

### Step by step
1. Run the command (just type it in the prompt box and enter):
   > /pipeline

   It defaults to `sample_invoice.txt`. (You can also write `/pipeline sample_invoice.txt`.)
2. Watch **STEP 1** — the `extractor` subagent runs first and prints compact JSON
   (vendor, date, line items, total, terms).
3. Watch **STEP 2** — only after step 1 is done, the `analyzer` subagent runs and
   prints a 2-line risk/cashflow note, working from that JSON.

### Point at the screen (the lesson)
- The JSON appears **first**; the analysis appears **second**. Order is guaranteed,
  not accidental.
- The analyzer reasons over **that JSON**, not the original invoice text — that's the
  "pass explicit context to the next step" idea.

### Anatomy: what `/pipeline` does, which agents act, and why
When you type `/pipeline`, Claude Code reads the file **`.claude/commands/pipeline.md`**
and follows it as an instruction sheet. Here is what that file tells the coordinator
to do, in order:

1. **Pick the document.** `pipeline.md` says: use whatever you passed as an argument,
   and if you passed nothing, default to `sample_invoice.txt`. (That's the
   `$ARGUMENTS` line in the file.)
2. **STEP 1 — call the `extractor` agent.** The command tells the coordinator to
   dispatch the **`extractor`** subagent (via the Task tool) on that document.
   - *Which agent acts:* `.claude/agents/extractor.md`.
   - *What it does:* its system prompt is *"Extract key fields as compact JSON. Output
     ONLY JSON."* and it's given the `Read` tool so it can open the file itself.
   - *Why we created it:* we want one worker whose ONLY job is turning messy raw text
     into clean structured data — nothing else. Narrow job = reliable output.
3. **GUARD — check the result before going on.** `pipeline.md` says: if the extractor
   returned nothing usable, STOP and report "extraction produced nothing." Do **not**
   start step 2. This is the enforced-ordering safety check.
4. **STEP 2 — call the `analyzer` agent.** Only if step 1 succeeded, the command tells
   the coordinator to dispatch the **`analyzer`** subagent, passing it **only the
   extractor's JSON** — never the raw invoice.
   - *Which agent acts:* `.claude/agents/analyzer.md`.
   - *What it does:* its system prompt is *"You receive extracted invoice facts. Give a
     2-line risk/cashflow note."* It has no file tools, so it physically cannot go read
     the raw doc — it can only reason over what it's handed.
   - *Why we created it:* we want judgment/analysis kept separate from parsing. The
     analyzer trusts the extractor's clean facts and focuses on the insight.

**Why two agents instead of one big "process this invoice" agent?**
- **Separation of concerns:** extraction (parsing) and analysis (judgment) are
  different jobs; small focused agents are more reliable and easier to debug.
- **Enforceable order:** with two steps, the command can *guarantee* extract runs
  first and can halt at the guard if it fails.
- **Controlled context:** because the analyzer only ever receives the JSON, you know
  exactly what it's reasoning over — no chance it wanders back into the raw text.

**How they're wired:** `pipeline.md` is the recipe (order + guard); `extractor.md` and
`analyzer.md` are the two workers; the coordinator (main Claude) runs the recipe and
uses the **Task tool** to hand work to each worker and to pass step 1's output into
step 2. The loop that runs *inside* each worker is, as always, built into Claude Code.

### Where this is written (the files)
- **The order and the guard** ("STEP 1 extract → GUARD: stop if empty → STEP 2
  analyze, using only the JSON") are written in **`.claude/commands/pipeline.md`** —
  that's the `/pipeline` command you ran. Open it: the numbered steps and the
  "halt before analysis" guard are right there.
- **The same ordering rule is also stated in `CLAUDE.md`** (the *"Document processing"*
  section), so even if you ask in plain English instead of `/pipeline`, the
  coordinator still runs extract-before-analyze.
- **The two workers** are subagents in **`.claude/agents/`**: `extractor.md`
  (raw doc → JSON) and `analyzer.md` (reasons over the JSON only). Their system
  prompts are the file bodies.
- As before, the underlying agent loop that runs each subagent is built into Claude
  Code — *you* only wrote the order, the guard, and the two workers.

### Optional — show the GUARD fire (proves order is enforced)
1. Create a blank/empty text file, e.g. `blank.txt`, and run:
   > /pipeline blank.txt
2. The extractor finds nothing to extract → the run **halts at "extraction produced
   nothing"** and the analyzer never runs.
3. Say: "Analysis literally cannot start on empty/failed extraction. The order isn't a
   suggestion — the guard in `pipeline.md` enforces it."

---

## Closing talking point
- **What Claude Code gives you for free:** the agentic loop (Demo A) and the
  mechanism to dispatch to subagents — you never write those.
- **What you author on top:** the specialists and routing rules (`CLAUDE.md`,
  `.claude/agents/`) in Demo B, and the step order + guard (`.claude/commands/pipeline.md`)
  in Demo C.
- That split is the takeaway: you don't rebuild the engine, you build the
  orchestration — routing, ordering, and context — *on top* of a loop the harness
  already runs reliably.
