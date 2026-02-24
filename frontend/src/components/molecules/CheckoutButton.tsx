"use client";

import { useState } from "react";
import { useCart } from "@/contexts/CartContext";

export function CheckoutButton() {
  const { items, clearCart } = useCart();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleCheckout() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items: items.map((i) => ({
            productId: i.productId,
            productTitle: i.title,
            priceCents: Math.round(i.price * 100),
            quantity: i.quantity,
          })),
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "Checkout failed");
        return;
      }
      if (data.url) {
        clearCart();
        window.location.href = data.url;
      } else {
        setError("No checkout URL returned");
      }
    } catch (err) {
      setError("Network error. Check that Stripe is configured.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      {error && (
        <p className="mb-2 text-sm text-red-600 dark:text-red-400">{error}</p>
      )}
      <button
        type="button"
        onClick={handleCheckout}
        disabled={loading}
        className="rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)] disabled:opacity-50"
      >
        {loading ? "Redirecting..." : "Checkout with Stripe"}
      </button>
    </div>
  );
}
