"""Shared helpers for all Module 1 & 2 labs.

Keeps every demo consistent: one place to load the API key, build the client,
pick the model, and pretty-print the agentic trace so the audience can follow
along on screen.
"""
import os
import sys
import json

# Load .env if python-dotenv is installed (optional; env var also works).
try:
    from dotenv import load_dotenv

    # Look for a .env next to the repo root regardless of where script is run.
    _here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(_here, "..", ".env"))
except ImportError:
    pass

# All labs use the same model so behavior is consistent across demos.
MODEL = "claude-sonnet-4-6"


def get_client():
    """Return an Anthropic client, with a friendly error if the key is missing.

    The `anthropic` import is lazy so the purely-local labs (hooks, session
    fork, structured errors) run with nothing installed.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        print(
            "\n[!] The 'anthropic' package isn't installed.\n"
            "    Run:  pip install -r requirements.txt\n",
            file=sys.stderr,
        )
        sys.exit(1)

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print(
            "\n[!] ANTHROPIC_API_KEY is not set.\n"
            "    1. Copy .env.example to .env\n"
            "    2. Paste your key from https://console.anthropic.com/settings/keys\n"
            "    (or set the env var: $env:ANTHROPIC_API_KEY = 'sk-ant-...')\n",
            file=sys.stderr,
        )
        sys.exit(1)
    return Anthropic(api_key=key)


# ---- demo-friendly printing -------------------------------------------------

def banner(title):
    line = "=" * 70
    print(f"\n{line}\n  {title}\n{line}")


def show_turn(n, stop_reason):
    print(f"\n--- turn {n}  |  stop_reason = {stop_reason!r} ---")


def show_tool_call(name, args):
    print(f"  [tool_use] {name}({json.dumps(args)})")


def show_tool_result(name, result, is_error=False):
    tag = "tool_error" if is_error else "tool_result"
    text = result if isinstance(result, str) else json.dumps(result)
    if len(text) > 300:
        text = text[:300] + " ...(truncated)"
    print(f"  [{tag}] {name} -> {text}")


def show_text(text):
    print(f"\n  [assistant] {text}")
