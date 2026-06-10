// Small formatting utilities for the sample app.

export function formatPrice(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

export function slugify(text: string): string {
  return text.toLowerCase().trim().replace(/\s+/g, "-");
}
