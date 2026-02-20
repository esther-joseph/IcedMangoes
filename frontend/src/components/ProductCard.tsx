import Link from "next/link";

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
      className="group block overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--card-bg)] transition hover:border-[var(--accent)]"
    >
      <div className="aspect-square overflow-hidden bg-[var(--border)]">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.title}
            className="h-full w-full object-cover transition group-hover:scale-105"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-[var(--muted)]">
            No image
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="line-clamp-2 font-medium text-[var(--foreground)]">
          {product.title}
        </h3>
        <p className="mt-1 line-clamp-2 text-sm text-[var(--muted)]">
          {product.description}
        </p>
        <p className="mt-2 font-semibold text-[var(--accent)]">
          ${Number(product.price).toFixed(2)}
        </p>
      </div>
    </Link>
  );
}
