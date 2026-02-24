"use client";

import { useCart } from "@/contexts/CartContext";
import { CheckoutButton } from "@/components/molecules/CheckoutButton";
import { CartItem } from "@/components/molecules/CartItem";
import { EmptyState } from "@/components/molecules/EmptyState";
import { PageLayout } from "@/components/templates/PageLayout";

export default function CartPage() {
  const { items, removeItem, updateQuantity, total } = useCart();

  if (items.length === 0) {
    return (
      <PageLayout maxWidth="md">
        <h1 className="mb-6 text-2xl font-semibold text-[var(--foreground)]">
          Cart
        </h1>
        <EmptyState
          title="Your cart is empty"
          actionLabel="Continue shopping"
          actionHref="/shop"
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout maxWidth="md">
      <h1 className="mb-8 text-2xl font-semibold text-[var(--foreground)]">
        Cart
      </h1>
      <div className="space-y-4">
        {items.map((item) => (
          <CartItem
            key={item.productId}
            item={item}
            onQuantityChange={updateQuantity}
            onRemove={removeItem}
          />
        ))}
      </div>
      <div className="mt-8 flex items-center justify-between border-t border-[var(--border)] pt-6">
        <p className="text-lg font-semibold text-[var(--foreground)]">
          Total: ${total.toFixed(2)}
        </p>
        <CheckoutButton />
      </div>
    </PageLayout>
  );
}
