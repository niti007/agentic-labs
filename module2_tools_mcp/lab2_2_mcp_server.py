"""Lab 2.2 (optional) - A minimal MCP server (stdio) with FastMCP.

Exposes two fake tools - query_db and search_docs - over the Model Context
Protocol. Claude Code (or any MCP client) connects to this via .mcp.json and
can then call these tools like any built-in.

Run standalone to confirm it imports/starts:
    py module2_tools_mcp/lab2_2_mcp_server.py
(It will wait on stdio for an MCP client - Ctrl+C to stop.)

It is normally launched FOR you by Claude Code via .mcp.json.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("labs-demo-server")

# Fake data sources so the demo needs no real DB / docs site.
_DB = {
    "1": {"name": "Nitish", "plan": "pro"},
    "2": {"name": "Asha", "plan": "free"},
}
_DOCS = {
    "rate limit": "Default rate limit is 1000 requests/min per key.",
    "auth": "Use a Bearer token in the Authorization header.",
}


@mcp.tool()
def query_db(user_id: str) -> str:
    """Look up a user record by id from the demo database."""
    rec = _DB.get(user_id)
    return f"{rec}" if rec else f"No user with id {user_id}"


@mcp.tool()
def search_docs(keyword: str) -> str:
    """Search the demo documentation for a keyword."""
    for k, v in _DOCS.items():
        if k in keyword.lower():
            return v
    return "No matching docs."


if __name__ == "__main__":
    mcp.run()  # serves over stdio
