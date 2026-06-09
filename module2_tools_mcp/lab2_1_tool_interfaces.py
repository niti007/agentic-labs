"""Lab 2.1 (mandatory) - Tool interfaces drive correct selection.

The model picks tools by their NAME + DESCRIPTION. Clear, distinct interfaces
make it pick correctly; vague/overlapping ones make it guess wrong.

This demo asks an ambiguous-ish question and prints which tool the model
chooses. Flip USE_BAD_NAMES = True to show how poor naming causes the model to
grab the wrong tool.

Run:  py module2_tools_mcp/lab2_1_tool_interfaces.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner, show_tool_call

client = get_client()

# GOOD: names and descriptions make the boundary obvious.
GOOD_TOOLS = [
    {
        "name": "search_orders",
        "description": "Look up a CUSTOMER'S PAST PURCHASES / order history by order id, "
                       "email, or date. Use for 'where is my order', 'what did I buy'.",
        "input_schema": {"type": "object",
                         "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
    {
        "name": "search_products",
        "description": "Search the PRODUCT CATALOG of items available to buy by keyword, "
                       "category, or price. Use for 'do you sell', 'show me laptops'.",
        "input_schema": {"type": "object",
                         "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
]

# BAD: vague, overlapping names - the model can't tell them apart.
BAD_TOOLS = [
    {"name": "search1", "description": "search for stuff",
     "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]}},
    {"name": "search2", "description": "another search",
     "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]}},
]

USE_BAD_NAMES = False


def which_tool(question, tools):
    resp = client.messages.create(
        model=MODEL, max_tokens=300, tools=tools,
        messages=[{"role": "user", "content": question}],
    )
    picked = [b.name for b in resp.content if b.type == "tool_use"]
    for b in resp.content:
        if b.type == "tool_use":
            show_tool_call(b.name, b.input)
    return picked, resp.stop_reason


if __name__ == "__main__":
    banner("Lab 2.1 - Tool interfaces & selection")
    tools = BAD_TOOLS if USE_BAD_NAMES else GOOD_TOOLS
    print(f"(using {'BAD' if USE_BAD_NAMES else 'GOOD'} tool names)\n")

    for q in [
        "Where is my order #10293? I ordered last Tuesday.",
        "Do you sell mechanical keyboards under $100?",
    ]:
        print(f"Q: {q}")
        picked, stop = which_tool(q, tools)
        print(f"   model picked -> {picked}  (stop_reason={stop})\n")
