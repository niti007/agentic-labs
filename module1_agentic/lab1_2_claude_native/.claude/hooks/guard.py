"""PreToolUse hook — BLOCK writes that touch a protected directory.

Claude Code runs this script BEFORE every Write/Edit tool call (see
`.claude/settings.json`). It receives a JSON payload on stdin describing the tool
call. If the target path is under a protected location, we print a reason to stderr
and exit 2 — which Claude Code treats as "block this tool call" and feeds the reason
back to the model. Any other exit 0 = allow.

This is the native equivalent of the `post_tool_use_hook` in lab1_2_hooks_demo.py,
except here it is a REAL interception point wired into Claude Code — not a simulation.

Note: PreToolUse blocks *before* the action happens. (PostToolUse, see audit_log.py,
runs *after* and can only log/flag — it cannot un-write a file.)
"""
import sys, json

# Paths under these prefixes are off-limits. Edit to taste.
PROTECTED_PREFIXES = ("protected/", "/etc/", "C:/Windows/")


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        # Can't parse the payload -> don't get in the way.
        sys.exit(0)

    tool_input = event.get("tool_input", {}) or {}
    # Write uses "file_path"; be tolerant of other key names just in case.
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    norm = path.replace("\\", "/")

    for prefix in PROTECTED_PREFIXES:
        pfx = prefix.replace("\\", "/")
        # match an absolute prefix anywhere, or a relative prefix at the start
        if pfx in norm or norm.startswith(pfx):
            print(
                f"BLOCKED by guard.py: '{path}' is under protected location "
                f"'{prefix}'. Writes there are not allowed in this lab.",
                file=sys.stderr,
            )
            sys.exit(2)  # <- exit 2 tells Claude Code to block the tool call

    sys.exit(0)  # allow everything else


if __name__ == "__main__":
    main()
