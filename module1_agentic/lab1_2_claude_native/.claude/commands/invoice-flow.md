---
description: FIXED decomposition — always run the same 3 invoice steps in order
---

Run the **fixed** invoice flow. The steps are known in advance, so they are
hard-coded: **always these three, always in this order, no branching, no improvising.**

Invoice to process: $ARGUMENTS
(If nothing was given, use `sample_invoice.txt`.)

## Steps (always exactly these three)
1. **parse_fields** — read the invoice and pull out vendor, date, line items, total,
   and payment terms.
2. **check_totals** — verify the line items add up to the stated total; note any
   mismatch.
3. **mark_for_payment** — state the payment decision (approve for payment under the
   stated terms, or hold if step 2 found a mismatch).

Print each step as `-> N. step_name` before its result, then a one-line `[done]`.
Do **not** add, skip, or reorder steps — running this command twice on the same
invoice must produce the same three-step trace. That predictability is the point of
fixed decomposition.
