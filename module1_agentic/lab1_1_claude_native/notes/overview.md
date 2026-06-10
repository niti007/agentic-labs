# Platform overview

Our backend is split into a handful of independent services. Each service owns a
slice of functionality and is documented in its own note in this folder:

- `services.md` — the service catalog: who owns what.
- `gateway.md` — the edge/API gateway config.
- `billing.md` — the billing service.

Traffic policies (auth, rate limiting, routing) are NOT handled per-service in the
application code — they are centralized. See the service catalog to find which
service owns those policies, then that service's own note for the exact settings.
