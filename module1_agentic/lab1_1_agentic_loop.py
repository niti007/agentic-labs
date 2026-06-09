"""Lab 1.1 (mandatory) - The Agentic Loop.

Demonstrates the single most important pattern: a stable loop that reads
`stop_reason` correctly so the agent knows when to ACT vs. when to HALT.

Flow:
    call Claude
      -> stop_reason == "tool_use"  : run the tool, feed result back, LOOP
      -> stop_reason == "end_turn"  : the model is done talking, HALT

The "research assistant" keeps calling web_search until it has enough to
answer, then calls `done`. Watch the stop_reason print on each turn.

Run:  py module1_agentic/lab1_1_agentic_loop.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner, show_turn, show_tool_call, show_tool_result, show_text

# ---- mock tools (canned data so the demo needs no internet) -----------------

FAKE_SEARCH_DB = {
    "quantum computing 2024": [
        "IBM unveiled the 1,121-qubit 'Condor' processor.",
        "Google reported a breakthrough in below-threshold error correction.",
        "Atom Computing announced a 1,180-qubit neutral-atom machine.",
    ],
    "quantum error correction": [
        "Google's 2024 result showed logical error rate dropping as qubits scale.",
        "Surface codes remain the leading approach for fault tolerance.",
    ],
}


def web_search(query):
    """Mock search: returns canned bullet points for known queries."""
    for key, hits in FAKE_SEARCH_DB.items():
        if any(word in query.lower() for word in key.split()):
            return "\n".join(f"- {h}" for h in hits)
    return "- No results found."


# ---- tool schemas given to the model ----------------------------------------

TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for recent information. Use repeatedly to gather enough facts before answering.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"],
        },
    },
    {
        "name": "done",
        "description": "Call this ONLY when you have gathered enough information to fully answer the user. Provide the final answer.",
        "input_schema": {
            "type": "object",
            "properties": {"answer": {"type": "string", "description": "The final answer for the user"}},
            "required": ["answer"],
        },
    },
]


def run_agent(task, max_turns=8):
    client = get_client()
    messages = [{"role": "user", "content": task}]

    for turn in range(1, max_turns + 1):
        resp = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        show_turn(turn, resp.stop_reason)

        # --- THE CORE BRANCH: read stop_reason and decide what to do ---
        if resp.stop_reason == "end_turn":
            # Model finished without a tool call - print its text and halt.
            for block in resp.content:
                if block.type == "text":
                    show_text(block.text)
            print("\n[HALT] stop_reason=end_turn -> agent is done.")
            return

        if resp.stop_reason == "tool_use":
            # Append the assistant's turn, then run every tool it asked for.
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "text" and block.text.strip():
                    show_text(block.text)
                if block.type == "tool_use":
                    show_tool_call(block.name, block.input)

                    if block.name == "done":
                        # Agent signalled completion via an explicit tool.
                        print(f"\n[HALT] agent called done().")
                        show_text(block.input["answer"])
                        return

                    result = web_search(block.input["query"])
                    show_tool_result(block.name, result)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )
            messages.append({"role": "user", "content": tool_results})
            continue  # LOOP back to call Claude again

        print(f"\n[HALT] unexpected stop_reason: {resp.stop_reason}")
        return

    print(f"\n[HALT] hit max_turns={max_turns} safety limit.")


if __name__ == "__main__":
    banner("Lab 1.1 - Agentic Loop (research assistant)")
    run_agent(
        "Research the biggest quantum computing breakthroughs of 2024, "
        "then give me a 3-bullet summary. Search as many times as you need."
    )
