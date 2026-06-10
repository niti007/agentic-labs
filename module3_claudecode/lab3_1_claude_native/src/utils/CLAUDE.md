# Relaxed rules — applies under src/utils/** only

Contrast file: utility helpers are low-risk, so the rules here are lighter than
`src/auth/`. This shows how the SAME repo can carry different rules per path.

## Guidance for utils
- Keep helpers small and pure (no side effects where avoidable).
- A docstring is enough; exhaustive failure-path tests are optional.
- Readability over micro-optimization.
