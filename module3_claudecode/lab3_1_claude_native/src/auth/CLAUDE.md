# STRICT security rules — applies under src/auth/** only

This is the **path-specific rule file** for auth code. Because it lives in `src/auth/`,
Claude Code loads it only when working on files in this directory — so the strict rules
stay relevant and don't pollute unrelated work.

## Hard rules for auth code
- NEVER log passwords, tokens, secrets, or full credentials.
- ALWAYS hash passwords with a slow KDF (bcrypt/argon2) — never store plaintext.
- Reject any change that weakens input validation on login.
- All auth functions MUST have tests covering the failure/denial path.
- No `eval`, no string-built SQL — parameterize everything.
