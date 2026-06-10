import { formatPrice, slugify } from "../src/utils";

test("formats price from cents", () => {
  expect(formatPrice(1250)).toBe("$12.50");
});

test("slugifies text", () => {
  expect(slugify("Hello World")).toBe("hello-world");
});
