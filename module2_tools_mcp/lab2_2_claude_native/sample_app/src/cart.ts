// Shopping-cart helpers for the sample app.

export interface CartItem {
  sku: string;
  qty: number;
  price: number;
}

export function addToCart(cart: CartItem[], item: CartItem): CartItem[] {
  const existing = cart.find((c) => c.sku === item.sku);
  if (existing) {
    existing.qty += item.qty;
    return cart;
  }
  return [...cart, item];
}

export function cartTotal(cart: CartItem[]): number {
  return cart.reduce((sum, c) => sum + c.qty * c.price, 0);
}
