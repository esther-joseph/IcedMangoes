import Link from "next/link";
import { ProductImage } from "@/components/atoms/ProductImage";

interface ProductCardProps {
  product: {
    id: string;
    title: string;
    description: string;
    price: number;
    image_url: string | null;
  };
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <Link
      href={`/product/${product.id}`}
      className="group block overflow-hidden rounded-xl shadow-md transition-shadow duration-300 hover:shadow-xl"
      style={{
        background: "var(--theme-bg-card)",
        boxShadow: "0 4px 6px -1px var(--theme-shadow), 0 2px 4px -2px var(--theme-shadow)",
      }}
    >
      <div className="relative aspect-square overflow-hidden bg-[var(--theme-border)]">
        <ProductImage
          src={product.image_url}
          alt={product.title}
          fill
          sizes="(max-width: 768px) 50vw, 25vw"
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div className="p-4">
        <h3
          className="line-clamp-2 font-semibold"
          style={{ color: "var(--theme-text)" }}
        >
          {product.title}
        </h3>
        <p
          className="mt-2 line-clamp-2 text-sm opacity-90"
          style={{ color: "var(--theme-text)" }}
        >
          {product.description}
        </p>
        <div className="mt-2 flex items-center justify-between gap-2">
          <span
            className="font-semibold"
            style={{ color: "var(--theme-accent)" }}
          >
            From ${Number(product.price).toFixed(2)}
          </span>
          <span
            className="text-xs"
            style={{ color: "var(--theme-text-muted)" }}
          >
            View details →
          </span>
        </div>
      </div>
    </Link>
  );
}
