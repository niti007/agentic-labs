"""Lab 3.3 (optional) - parse Claude's structured review JSON into a CI gate.

Exit code 0 = pass (gate green), 1 = fail (gate red). CI uses the exit code.

The `claude --output-format json` envelope wraps the model's text in a
`result` field; we pull our verdict JSON out of that. Falls back to treating
the whole file as the verdict JSON (handy for local testing with a sample).

Usage:
    py parse_output.py review.json
    py parse_output.py            # uses the built-in SAMPLE below (demo)
"""
import sys
import json

SAMPLE = '{"result": "{\\"verdict\\": \\"fail\\", \\"issues\\": [\\"divide() missing zero check\\"]}"}'


def extract_verdict(raw):
    data = json.loads(raw)
    # claude CLI wraps output: {"result": "<model text>", ...}
    payload = data.get("result", data) if isinstance(data, dict) else data
    if isinstance(payload, str):
        payload = json.loads(payload)
    return payload


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        print("[demo] no file given - using built-in SAMPLE")
        raw = SAMPLE

    verdict = extract_verdict(raw)
    print(f"verdict: {verdict.get('verdict')}")
    for issue in verdict.get("issues", []):
        print(f"  - {issue}")

    if verdict.get("verdict") == "pass":
        print("GATE: PASS")
        sys.exit(0)
    print("GATE: FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
