"""Lab 4.2 (Claude-native) - the 'scoring' tool that works like a strict form.

You never edit this file. It just gives Claude one tool, `record_score`, that:
  - FORCES every answer into the same three boxes: name, score, reason;
  - CHECKS the score is a whole number from 0 to 10 and the reason isn't blank;
  - BOUNCES BACK a clear message when something's wrong, so Claude can fix it and retry.

Two layers of checking:
  1. Schema check (automatic): `score` must be a whole number, or the tool won't even
     accept the call.
  2. Meaning check (below): the number has to make sense (0-10) and the reason can't be
     empty.

    py lead_scoring_server.py   # waits for Claude; normally launched via .mcp.json
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("scoring")


@mcp.tool()
def record_score(name: str, score: int, reason: str) -> str:
    """Record a sales lead's score. name = the lead or company; score = a WHOLE NUMBER
    from 0 to 10 (10 = hottest, ready to buy); reason = one short line. If the score is
    out of range or the reason is empty, this returns an error to fix and call again."""
    problems = []
    # bool is a sneaky subtype of int in Python, so rule it out explicitly
    if isinstance(score, bool) or not isinstance(score, int):
        problems.append(f"score must be a whole number, got {score!r}")
    elif score < 0 or score > 10:
        problems.append(f"score must be between 0 and 10, got {score}")
    if not reason or not reason.strip():
        problems.append("reason must not be empty")

    if problems:
        return json.dumps({
            "ok": False,
            "error": "; ".join(problems) + ". Please correct and call record_score again.",
        })
    return json.dumps({
        "ok": True,
        "recorded": {"name": name, "score": score, "reason": reason.strip()},
    })


if __name__ == "__main__":
    mcp.run()
