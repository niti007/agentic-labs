"""Lab 2.2 (Claude-native) - the 'docs' MCP server (source #2 of a multi-source setup).

A minimal documentation source over MCP. Paired with db_server.py ('db') in .mcp.json
so a single project draws on TWO separate tool sources.

    py docs_server.py   # waits on stdio; normally launched by Claude Code via .mcp.json
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("docs")

# Fake docs index so the demo needs no real docs site.
_DOCS = {
    "rate limit": "Default rate limit is 1000 requests/min per key.",
    "auth": "Use a Bearer token in the Authorization header.",
    "pagination": "Use ?page= and ?page_size= (max 100) on list endpoints.",
}


@mcp.tool()
def search_docs(keyword: str) -> str:
    """Search the PRODUCT DOCUMENTATION for a keyword. Use for 'how does X work',
    'what's the limit', 'how do I authenticate' — anything answered by the docs."""
    for k, v in _DOCS.items():
        if k in keyword.lower():
            return v
    return "No matching docs."


if __name__ == "__main__":
    mcp.run()
