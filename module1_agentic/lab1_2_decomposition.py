"""Lab 1.2 (optional) - Fixed vs. adaptive decomposition.

When you KNOW the steps, hard-code them (fixed decomposition): reliable,
cheap, predictable. When you DON'T (open-ended triage), let the model choose
the next step at each turn (adaptive decomposition): flexible, but costs a
model call per decision.

This demo runs the same-ish goal both ways and prints the two traces so you
can contrast them. Uses the API for the adaptive path.

Run:  py module1_agentic/lab1_2_decomposition.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner, show_text


# ---- FIXED: invoice flow with 3 known steps, always in this order -----------

def fixed_invoice_flow(invoice):
    print("\n[FIXED] 3 hard-coded steps, no model needed for control flow:")
    steps = ["1. parse_fields", "2. check_totals", "3. mark_for_payment"]
    state = {"invoice": invoice}
    for step in steps:
        print(f"   -> {step}")
        state[step] = "done"
    print("   [done] fixed flow always runs exactly these 3 steps.")


# ---- ADAPTIVE: model decides the next action until it says 'resolved' --------

NEXT_STEP_TOOL = {
    "name": "next_step",
    "description": "Decide the single next action for this support ticket, or resolve it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["ask_clarifying_question", "check_account", "issue_refund",
                         "escalate_to_human", "resolve"],
            },
            "note": {"type": "string"},
        },
        "required": ["action", "note"],
    },
}


def adaptive_triage(ticket, max_steps=4):
    client = get_client()
    print(f"\n[ADAPTIVE] model branches per turn for: {ticket!r}")
    messages = [{"role": "user", "content": f"Support ticket: {ticket}"}]
    for i in range(1, max_steps + 1):
        resp = client.messages.create(
            model=MODEL, max_tokens=300, tools=[NEXT_STEP_TOOL],
            tool_choice={"type": "tool", "name": "next_step"}, messages=messages,
        )
        block = next(b for b in resp.content if b.type == "tool_use")
        action, note = block.input["action"], block.input["note"]
        print(f"   step {i}: {action}  - {note}")
        if action in ("resolve", "escalate_to_human"):
            print(f"   [done] adaptive flow ended with: {action}")
            return
        # Feed the chosen action back so the model picks the next one.
        messages.append({"role": "assistant", "content": resp.content})
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": block.id, "content": f"{action} completed."}
        ]})
    print("   [done] hit step cap.")


if __name__ == "__main__":
    banner("Lab 1.2 - Fixed vs Adaptive decomposition")
    fixed_invoice_flow("INVOICE #4471, total $1,649.50")
    adaptive_triage("I was charged twice for my subscription this month and I'm upset.")
