import { addToCart, cartTotal, CartItem } from "../src/cart";

test("adds a new item", () => {
  const cart: CartItem[] = [];
  const out = addToCart(cart, { sku: "A", qty: 1, price: 100 });
  expect(out.length).toBe(1);
});

test("totals the cart", () => {
  const cart: CartItem[] = [{ sku: "A", qty: 2, price: 100 }];
  expect(cartTotal(cart)).toBe(200);
});
