// Auth helpers for the sample app.

const TOKEN_TTL_SECONDS = 3600;

export function validateToken(token: string): boolean {
  // Demo logic: a token is valid if it's non-empty and not expired.
  if (!token) return false;
  return !isExpired(token);
}

function isExpired(token: string): boolean {
  const issuedAt = Number(token.split(".")[0] || 0);
  const now = Math.floor(Date.now() / 1000);
  return now - issuedAt > TOKEN_TTL_SECONDS;
}
