"use client";

import { useCart } from "@/contexts/CartContext";

interface AddToCartButtonProps {
  productId: string;
  title: string;
  price: number;
  imageUrl?: string;
}

export function AddToCartButton({
  productId,
  title,
  price,
  imageUrl,
}: AddToCartButtonProps) {
  const { addItem } = useCart();

  return (
    <button
      type="button"
      onClick={() => addItem({ productId, title, price, imageUrl })}
      className="w-full rounded-lg bg-[var(--accent)] px-5 py-3 text-sm font-medium text-white hover:bg-[var(--accent-hover)]"
    >
      Add to cart
    </button>
  );
}
