"""Lab 2.1 (Claude-native) - the 'shopbad' MCP server (FAILURE-MODE contrast).

Same two underlying searches as the 'shop' server, but with vague, overlapping
names and useless descriptions. Swap this in (see .mcp.json + RUNBOOK Demo G) to
watch tool selection get shaky: the model can't tell search_a from search_b.

This is the native analog of USE_BAD_NAMES=True in lab2_1_tool_interfaces.py.

    py lab2_1_badnames_server.py
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shopbad")

_ORDERS = {"10293": {"item": "USB-C cable", "status": "shipped"}}
_PRODUCTS = [{"name": "Mechanical keyboard", "price": 89.0}]


@mcp.tool()
def search_a(q: str) -> str:
    """search for stuff"""
    return json.dumps([f"{k}: {v}" for k, v in _ORDERS.items()])


@mcp.tool()
def search_b(q: str) -> str:
    """another search"""
    return json.dumps(_PRODUCTS)


if __name__ == "__main__":
    mcp.run()
