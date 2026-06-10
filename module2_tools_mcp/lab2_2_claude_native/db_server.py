"""Lab 2.2 (Claude-native) - the 'db' MCP server (source #1 of a multi-source setup).

A minimal database source over MCP. Paired with docs_server.py ('docs') in .mcp.json
so the project has TWO independent tool sources wired in at once.

    py db_server.py   # waits on stdio; normally launched by Claude Code via .mcp.json
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("db")

# Fake user table so the demo needs no real database.
_DB = {
    "1": {"name": "Nitish", "plan": "pro"},
    "2": {"name": "Asha", "plan": "free"},
}


@mcp.tool()
def query_db(user_id: str) -> str:
    """Look up a USER RECORD by id from the application database. Use for questions
    about a specific user/account (name, plan, status)."""
    rec = _DB.get(user_id)
    return f"{rec}" if rec else f"No user with id {user_id}"


if __name__ == "__main__":
    mcp.run()
