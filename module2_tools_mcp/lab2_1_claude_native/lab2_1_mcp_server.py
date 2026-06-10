"""Lab 2.1 (Claude-native) - the 'shop' MCP server.

One local MCP server that exposes the tools all three Lab 2.1 demos use. Claude
Code launches it via .mcp.json and can then call these tools like built-ins.

Tools:
  - search_orders / search_products  -> clear, distinct interfaces (Demo G)
  - get_order                        -> structured errors isError/isRetryable (Demo H)
  - label                            -> sentiment classification (Demo I)

Run standalone to confirm it imports/starts (waits on stdio, Ctrl+C to stop):
    py lab2_1_mcp_server.py
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shop")

# ---- fake data so the demo needs no real backend ---------------------------
_ORDERS = {
    "10293": {"item": "USB-C cable", "status": "shipped", "eta": "2026-06-11"},
    "order-123": {"item": "Mechanical keyboard", "status": "delivered", "eta": "-"},
}
_PRODUCTS = [
    {"name": "Mechanical keyboard", "price": 89.0, "category": "accessories"},
    {"name": "27-inch monitor", "price": 240.0, "category": "displays"},
    {"name": "USB-C cable", "price": 12.5, "category": "accessories"},
]

# stateful flakiness for get_order(), mirroring _attempts in the Python script
_attempts = {"count": 0}


# ---- Demo G: clear, distinct tool interfaces --------------------------------

@mcp.tool()
def search_orders(query: str) -> str:
    """Look up a CUSTOMER'S PAST PURCHASES / order history by order id, email, or
    date. Use for 'where is my order', 'what did I buy', order status/tracking."""
    for oid, rec in _ORDERS.items():
        if oid in query:
            return f"Order {oid}: {rec}"
    return "No matching order. Provide an order id like 10293."


@mcp.tool()
def search_products(query: str) -> str:
    """Search the PRODUCT CATALOG of items available to buy by keyword, category, or
    price. Use for 'do you sell', 'show me laptops', 'what's in stock under $100'."""
    hits = [p for p in _PRODUCTS if query.lower() in p["name"].lower()
            or query.lower() in p["category"].lower()]
    return json.dumps(hits or _PRODUCTS)


# ---- Demo H: structured errors (isError / isRetryable) ----------------------

@mcp.tool()
def get_order(order_id: str) -> str:
    """Fetch a single order from the (flaky) orders API. Returns a JSON object with
    fields: isError (bool), isRetryable (bool), content (str). Callers should RETRY
    when isRetryable is true and HALT when it is false."""
    if order_id == "missing-999":
        # Permanent error: the resource does not exist -> do NOT retry.
        return json.dumps({
            "isError": True, "isRetryable": False,
            "content": f"404 Not Found: order '{order_id}' does not exist.",
        })

    _attempts["count"] += 1
    if _attempts["count"] == 1:
        # Transient error on the first attempt -> safe to retry.
        return json.dumps({
            "isError": True, "isRetryable": True,
            "content": "504 Gateway Timeout (transient). Retry the request.",
        })

    rec = _ORDERS.get(order_id, {"item": "unknown", "status": "unknown"})
    return json.dumps({
        "isError": False, "isRetryable": False,
        "content": f"OK: order {order_id} -> {rec}",
    })


# ---- Demo I: the single labeling tool the classifier is scoped to -----------

@mcp.tool()
def label(text: str, sentiment: str, confidence: float) -> str:
    """Record a sentiment label for the input text. `sentiment` must be one of
    positive | neutral | negative; `confidence` is 0.0-1.0. This is the ONLY tool a
    classification step should be allowed to use."""
    return json.dumps({"text": text, "sentiment": sentiment, "confidence": confidence})


if __name__ == "__main__":
    mcp.run()  # serves over stdio
