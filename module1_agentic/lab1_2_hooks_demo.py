"""Lab 1.2 (optional) - PostToolUse-style hook that intercepts tool calls.

A hook sits between the agent and the real action. Here it inspects every
`write_file` call and BLOCKS any write that touches a protected directory,
logging the decision. Same idea as Claude Code's PostToolUse hooks.

This demo is fully local (no API needed) so you can show the guard logic
clearly. The "agent" just emits tool calls; the hook decides allow vs block.

Run:  py module1_agentic/lab1_2_hooks_demo.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import banner

PROTECTED_PREFIXES = ("protected/", "/etc/", "C:\\Windows\\")


def post_tool_use_hook(tool_name, tool_input):
    """Return (allowed: bool, message: str). This is the interception point."""
    if tool_name == "write_file":
        path = tool_input.get("path", "")
        for prefix in PROTECTED_PREFIXES:
            if path.replace("\\", "/").startswith(prefix.replace("\\", "/")):
                return False, f"BLOCKED: '{path}' is under protected location '{prefix}'"
    return True, "allowed"


def write_file(path, content):
    """The 'real' action - only runs if the hook allows it."""
    return f"(pretend) wrote {len(content)} bytes to {path}"


def dispatch(tool_name, tool_input):
    """Every tool call goes through here, where the hook fires first."""
    allowed, msg = post_tool_use_hook(tool_name, tool_input)
    print(f"  [hook] {tool_name}({tool_input.get('path','')!r}) -> {msg}")
    if not allowed:
        return {"isError": True, "content": msg}
    result = write_file(**tool_input)
    print(f"  [exec] {result}")
    return {"isError": False, "content": result}


if __name__ == "__main__":
    banner("Lab 1.2 - PostToolUse hook (block protected writes)")

    calls = [
        ("write_file", {"path": "output/report.txt", "content": "hello"}),    # allowed
        ("write_file", {"path": "protected/secrets.env", "content": "leak"}),  # blocked
        ("write_file", {"path": "C:\\Windows\\system.ini", "content": "x"}),   # blocked
        ("write_file", {"path": "notes/todo.md", "content": "- demo"}),        # allowed
    ]
    for name, args in calls:
        dispatch(name, args)
