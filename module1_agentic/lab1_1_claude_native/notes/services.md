# Service catalog

| Service   | Owner team   | Responsibility                                        |
|-----------|--------------|-------------------------------------------------------|
| gateway   | Platform     | Edge entry point. Owns ALL inbound traffic policies — |
|           |              | auth termination, routing, and **rate limiting**.     |
| billing   | Payments     | Invoices, subscriptions, dunning.                     |
| notify    | Growth       | Email/SMS/push fan-out.                               |

So: rate limiting is owned by the **gateway** service. The exact configured limit
is not listed here — it lives in the gateway's own note (`gateway.md`).
