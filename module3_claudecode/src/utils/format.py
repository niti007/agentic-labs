"""Sample utility module (low-risk) for the relaxed-rules path demo."""


def to_currency(amount: float) -> str:
    """Format a number as USD, e.g. 1649.5 -> '$1,649.50'."""
    return f"${amount:,.2f}"


def truncate(text: str, n: int = 80) -> str:
    """Shorten text to n chars with an ellipsis."""
    return text if len(text) <= n else text[: n - 3] + "..."
