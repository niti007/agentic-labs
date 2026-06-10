import { validateToken } from "../src/auth";

test("rejects an empty token", () => {
  expect(validateToken("")).toBe(false);
});

test("accepts a fresh token", () => {
  const fresh = `${Math.floor(Date.now() / 1000)}.sig`;
  expect(validateToken(fresh)).toBe(true);
});
