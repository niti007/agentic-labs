"""Lab 2.1 (mandatory) - Structured errors: isError / isRetryable.

A tool that fails should tell the agent HOW to react:
  - isError=True, isRetryable=True   -> transient (timeout) -> RETRY
  - isError=True, isRetryable=False  -> permanent (404)     -> HALT

This demo wires that policy into the loop. The mock API fails with a timeout
the first time (agent retries) and a 404 for a missing id (agent stops).

Run:  py module2_tools_mcp/lab2_1_structured_errors.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import banner, show_tool_result

# ---- mock API that returns MCP-style structured results ---------------------

_attempts = {"count": 0}


def call_api(resource_id):
    """Returns dict with isError / isRetryable, mimicking an MCP tool result."""
    if resource_id == "missing-999":
        return {"isError": True, "isRetryable": False,
                "content": "404 Not Found: resource 'missing-999' does not exist."}

    _attempts["count"] += 1
    if _attempts["count"] == 1:
        return {"isError": True, "isRetryable": True,
                "content": "504 Gateway Timeout (transient)."}
    return {"isError": False, "isRetryable": False,
            "content": f"OK: data for {resource_id}"}


def fetch_with_policy(resource_id, max_retries=3):
    """The recovery policy the agent follows based on the structured flags."""
    print(f"\nfetch('{resource_id}')")
    for attempt in range(1, max_retries + 1):
        result = call_api(resource_id)
        show_tool_result("call_api", result["content"], is_error=result["isError"])

        if not result["isError"]:
            print(f"   [SUCCESS] after {attempt} attempt(s).")
            return result

        if result["isRetryable"]:
            print(f"   [RETRY] retryable error -> attempt {attempt+1}...")
            continue

        print("   [HALT] non-retryable error -> stop and surface to caller.")
        return result

    print("   [HALT] exhausted retries.")
    return result


if __name__ == "__main__":
    banner("Lab 2.1 - Structured errors (retry vs halt)")
    fetch_with_policy("order-123")   # timeout once, then succeeds (RETRY path)
    fetch_with_policy("missing-999")  # 404 -> stops immediately (HALT path)
