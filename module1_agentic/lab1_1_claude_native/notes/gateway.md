# Gateway service

The gateway is the single edge entry point for all inbound API traffic.

## Configuration
- TLS termination: enabled
- Routing: path-based, to the service catalog entries.
- **Rate limiting: 100 requests/minute per API key** (burst of 20 allowed).
  Over-limit requests get HTTP 429.

Rate-limit counters are stored in Redis and reset on a sliding 60-second window.
