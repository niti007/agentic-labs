"""Lab 1.1 (mandatory) - Explicit context passing + enforced step order.

A document pipeline where EXTRACTION must finish before ANALYSIS begins.
The order is enforced in *code*, not left to the model's discretion - and the
output of step 1 is passed explicitly as the input to step 2.

    extract(doc) -> facts            # step 1 must complete first
    analyze(facts) -> insight        # step 2 receives step 1's output

Run:  py module1_agentic/lab1_1_pipeline.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner, show_text

client = get_client()

DOC = """
INVOICE #4471
Vendor: Acme Cloud Services
Date: 2026-05-12
Line items:
  - Compute (May): $1,240.00
  - Storage (May): $310.50
  - Support plan: $99.00
Total due: $1,649.50
Payment terms: Net 30
"""


def extract(doc):
    """STEP 1 - pull structured facts out of raw text."""
    resp = client.messages.create(
        model=MODEL, max_tokens=400,
        system="Extract key fields as compact JSON. Output ONLY JSON.",
        messages=[{"role": "user", "content": doc}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def analyze(facts):
    """STEP 2 - reason over the EXTRACTED facts (not the raw doc)."""
    resp = client.messages.create(
        model=MODEL, max_tokens=400,
        system="You receive extracted invoice facts. Give a 2-line risk/cashflow note.",
        messages=[{"role": "user", "content": f"Extracted facts:\n{facts}"}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def run_pipeline(doc):
    print("\n[STEP 1] extract() running...")
    facts = extract(doc)
    show_text(facts)

    # Enforced ordering: analysis CANNOT start until extract returned something.
    if not facts.strip():
        print("[GUARD] extraction produced nothing -> halting before analysis.")
        return

    print("\n[STEP 2] analyze() running on STEP 1's output...")
    insight = analyze(facts)
    show_text(insight)


if __name__ == "__main__":
    banner("Lab 1.1 - Ordered pipeline (extract -> analyze)")
    run_pipeline(DOC)
