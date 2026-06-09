"""Lab 1.1 (mandatory) - Coordinator / Subagent (hub-and-spoke).

ONE lead agent (the hub) looks at a task and ROUTES it to a specialist
subagent (a spoke): summarize, translate, or validate. Each subagent is its
own focused Claude call with its own narrow system prompt.

Why this matters: specialists with small, clear jobs are more reliable than
one giant prompt trying to do everything.

    lead.route(task) --(tool_choice forces a routing decision)--> "summarize"
                                                                    |
                                                       subagent_summarize(task)

Run:  py module1_agentic/lab1_1_orchestrator.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner, show_tool_call, show_text

client = get_client()

# ---- the routing tool the LEAD agent must use -------------------------------

ROUTE_TOOL = {
    "name": "route",
    "description": (
        "Route the user's request to exactly one specialist subagent. "
        "Use 'summarize' to condense text, 'translate' to convert language, "
        "'validate' to check correctness/quality."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "specialist": {
                "type": "string",
                "enum": ["summarize", "translate", "validate"],
            },
            "reason": {"type": "string", "description": "One line: why this specialist"},
        },
        "required": ["specialist", "reason"],
    },
}


def lead_route(task):
    """Hub: force the model to pick exactly one specialist via tool_choice."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=[ROUTE_TOOL],
        tool_choice={"type": "tool", "name": "route"},  # MUST route
        messages=[{"role": "user", "content": task}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            show_tool_call("route", block.input)
            return block.input["specialist"]
    raise RuntimeError("lead did not route")


# ---- the specialist subagents (spokes) --------------------------------------

def _subagent(system, task):
    resp = client.messages.create(
        model=MODEL, max_tokens=512, system=system,
        messages=[{"role": "user", "content": task}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def subagent_summarize(task):
    return _subagent("You are a summarizer. Reply with 2 short bullet points only.", task)


def subagent_translate(task):
    return _subagent("You are a translator. Output ONLY the translation, nothing else.", task)


def subagent_validate(task):
    return _subagent("You are a validator. Reply VALID or INVALID and one line why.", task)


SPECIALISTS = {
    "summarize": subagent_summarize,
    "translate": subagent_translate,
    "validate": subagent_validate,
}


def orchestrate(task):
    print(f"\n[LEAD] received task: {task}")
    specialist = lead_route(task)
    print(f"[LEAD] -> delegating to subagent: {specialist}")
    result = SPECIALISTS[specialist](task)
    show_text(f"({specialist} subagent) {result}")


if __name__ == "__main__":
    banner("Lab 1.1 - Orchestrator (hub-and-spoke)")
    orchestrate("Translate to French: 'The deployment finished successfully.'")
    orchestrate("Summarize: Agentic systems loop over tool calls, reading stop_reason to "
                "decide whether to continue acting or to halt and answer the user.")
    orchestrate("Is this valid JSON? {\"name\": \"Nitish\", \"score\": 9}")
