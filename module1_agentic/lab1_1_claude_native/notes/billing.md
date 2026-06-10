# Billing service

Owned by the Payments team. Handles invoices, subscription state, and dunning.

- Invoices are generated nightly.
- Payment terms default to Net 30.
- No traffic-policy responsibilities — billing sits behind the gateway like every
  other service, so it does not configure its own rate limits.
