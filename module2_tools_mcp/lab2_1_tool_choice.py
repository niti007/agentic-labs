"""Lab 2.1 (mandatory) - Scope behavior with tool_choice.

tool_choice constrains WHAT the model may do:
  - {"type": "auto"}                       -> model decides (default)
  - {"type": "any"}                        -> must use some tool
  - {"type": "tool", "name": "label"}      -> must use THIS exact tool

Forcing the labeling tool guarantees a clean classification every time - the
model can't wander off into prose.

Run:  py module2_tools_mcp/lab2_1_tool_choice.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import get_client, MODEL, banner

client = get_client()

LABEL_TOOL = {
    "name": "label",
    "description": "Assign a sentiment label to the input text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
            "confidence": {"type": "number", "description": "0.0 - 1.0"},
        },
        "required": ["sentiment", "confidence"],
    },
}


def classify(text):
    resp = client.messages.create(
        model=MODEL, max_tokens=200, tools=[LABEL_TOOL],
        tool_choice={"type": "tool", "name": "label"},  # FORCE the label tool
        messages=[{"role": "user", "content": f"Classify: {text}"}],
    )
    block = next(b for b in resp.content if b.type == "tool_use")
    return block.input


if __name__ == "__main__":
    banner("Lab 2.1 - tool_choice forces classification")
    for text in [
        "This product completely changed my workflow, I love it!",
        "It arrived. It works. Nothing special.",
        "Worst support experience of my life. Never again.",
    ]:
        out = classify(text)
        print(f"  {out['sentiment']:>8}  ({out['confidence']:.2f})  <- {text}")
