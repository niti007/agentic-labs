---
description: Run the ordered document pipeline — extractor must finish before analyzer
---

Run the two-step document pipeline with **enforced ordering**. Do NOT analyze the
raw document yourself — orchestrate the two subagents in order.

Document to process: $ARGUMENTS
(If no path/text was given, use `sample_invoice.txt`.)

## Steps (order is mandatory)
1. **STEP 1 — extract.** Dispatch the `extractor` subagent (Task tool) on the
   document. It returns compact JSON facts. Show that JSON.
2. **GUARD.** If the extractor returned nothing / no usable JSON, STOP here and
   say "extraction produced nothing — halting before analysis." Do not run step 2.
3. **STEP 2 — analyze.** Only after step 1 succeeded, dispatch the `analyzer`
   subagent (Task tool), passing **only the extractor's JSON** as its input — never
   the raw document. Show its 2-line risk/cashflow note.

The lesson: step 2 begins only after step 1 completes, and step 2 reasons over
step 1's *output*, not the original source.
