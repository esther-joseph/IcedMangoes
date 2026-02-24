import { ProductCard } from "./ProductCard";

export interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  image_url: string | null;
}

interface ProductGridProps {
  products: Product[];
}

export function ProductGrid({ products }: ProductGridProps) {
  return (
    <div
      className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4"
      role="list"
    >
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
