"use client";

import Link from "next/link";
import Image from "next/image";
import type { CartItem as CartItemType } from "@/contexts/CartContext";

interface CartItemProps {
  item: CartItemType;
  onQuantityChange: (productId: string, quantity: number) => void;
  onRemove: (productId: string) => void;
}

export function CartItem({ item, onQuantityChange, onRemove }: CartItemProps) {
  return (
    <div className="flex gap-4 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-4">
      {item.imageUrl ? (
        <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-lg">
          <Image
            src={item.imageUrl}
            alt={item.title}
            fill
            sizes="80px"
            className="object-cover"
            unoptimized
          />
        </div>
      ) : null}
      <div className="min-w-0 flex-1">
        <Link
          href={`/product/${item.productId}`}
          className="font-medium text-[var(--foreground)] hover:text-[var(--accent)]"
        >
          {item.title}
        </Link>
        <p className="mt-1 text-sm font-semibold text-[var(--accent)]">
          ${item.price.toFixed(2)} × {item.quantity} = $
          {(item.price * item.quantity).toFixed(2)}
        </p>
      </div>
      <div className="flex items-center gap-2">
        <select
          value={item.quantity}
          onChange={(e) =>
            onQuantityChange(item.productId, parseInt(e.target.value, 10))
          }
          className="rounded border border-[var(--border)] bg-[var(--card-bg)] px-2 py-1 text-sm"
          aria-label={`Quantity for ${item.title}`}
        >
          {[1, 2, 3, 4, 5, 10].map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={() => onRemove(item.productId)}
          className="text-sm text-red-600 hover:underline dark:text-red-400"
        >
          Remove
        </button>
      </div>
    </div>
  );
}
