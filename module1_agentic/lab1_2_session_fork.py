"""Lab 1.2 (optional) - Resume / fork sessions + structured summaries.

A "session" is just a list of messages. To explore two solution paths without
losing prior state, you FORK: deep-copy the message history, then let each
branch diverge independently. A structured summary lets you compact a long
session into a compact "case facts" object you can resume from.

This demo is local (no API) so the state mechanics are crystal clear.

Run:  py module1_agentic/lab1_2_session_fork.py
"""
import sys, os, copy, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.client import banner


class Session:
    def __init__(self, name, messages=None):
        self.name = name
        self.messages = messages or []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        return self

    def fork(self, new_name):
        """Deep-copy so the child cannot mutate the parent's history."""
        return Session(new_name, copy.deepcopy(self.messages))

    def summary(self):
        """Structured summary = durable 'case facts' you can resume from."""
        return {
            "session": self.name,
            "turns": len(self.messages),
            "last_user_msg": next((m["content"] for m in reversed(self.messages)
                                   if m["role"] == "user"), None),
        }


if __name__ == "__main__":
    banner("Lab 1.2 - Session resume / fork + summaries")

    # Shared prefix - the work both branches build on.
    base = Session("base").add("user", "Design a rate limiter.")
    base.add("assistant", "Two candidate approaches exist.")
    print(f"[base] {len(base.messages)} messages")

    # Fork into two independent exploration paths.
    path_a = base.fork("token-bucket")
    path_a.add("assistant", "Path A: token bucket - smooth bursts.")

    path_b = base.fork("sliding-window")
    path_b.add("assistant", "Path B: sliding window - strict per-window cap.")

    # Prove isolation: base is untouched by either fork.
    print(f"[base] still {len(base.messages)} messages (unchanged by forks)")
    print(f"[path A] {len(path_a.messages)} messages")
    print(f"[path B] {len(path_b.messages)} messages")

    print("\nStructured summaries (resume from these without full history):")
    for s in (base, path_a, path_b):
        print("  " + json.dumps(s.summary()))
