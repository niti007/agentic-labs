"""PostToolUse hook — LOG every write that actually went through.

Claude Code runs this script AFTER a Write/Edit tool call succeeds (see
`.claude/settings.json`). PostToolUse runs *after* the action, so it cannot block the
write — but it is the right place to log, audit, or flag what happened. We append one
line per write to `.claude/hooks/write-audit.log`.

This is the "log / validate" half of the lab: PreToolUse (guard.py) blocks before,
PostToolUse (this file) records after. Always exits 0 — logging never interrupts work.
"""
import sys, os, json, datetime


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = event.get("tool_name", "?")
    tool_input = event.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or tool_input.get("path") or "?"

    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "write-audit.log")
    # No Math/Date restrictions here — this is plain Python, not a workflow script.
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{stamp}  {tool_name}  {path}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
