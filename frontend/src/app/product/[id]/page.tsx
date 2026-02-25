import Link from "next/link";
import { notFound } from "next/navigation";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { AddToCartButton } from "@/components/molecules/AddToCartButton";
import { ProductImage } from "@/components/atoms/ProductImage";
import { PageLayout } from "@/components/templates/PageLayout";

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const supabase = await getSupabaseClient();

  if (!supabase) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12 text-center text-[var(--muted)]">
        Configure Supabase in .env.local to view products.
      </div>
    );
  }

  const { data: product, error } = await supabase
    .from("products")
    .select("*")
    .eq("id", id)
    .eq("active", true)
    .single();

  if (error || !product) {
    notFound();
  }

  const tags = (product.tags as string[] | null) ?? [];

  return (
    <PageLayout maxWidth="lg">
      <div className="grid gap-8 md:grid-cols-2">
        <div className="relative aspect-square overflow-hidden rounded-xl bg-[var(--border)]">
          <ProductImage
            src={product.image_url}
            alt={product.title}
            fill
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </div>
        <div>
          <Link
            href="/shop"
            className="mb-4 inline-block text-sm text-[var(--muted)] hover:text-[var(--accent)]"
          >
            ← Back to shop
          </Link>
          <h1 className="text-2xl font-semibold text-[var(--foreground)]">
            {product.title}
          </h1>
          <p className="mt-4 text-lg font-semibold text-[var(--accent)]">
            ${Number(product.price).toFixed(2)}
            <span className="ml-1 text-sm font-normal text-[var(--muted)]">
              {product.currency}
            </span>
          </p>
          <p className="mt-4 whitespace-pre-wrap text-[var(--foreground)]">
            {product.description}
          </p>
          {tags.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-[var(--border)] px-3 py-1 text-xs text-[var(--muted)]"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
          <div className="mt-6">
            <AddToCartButton
              productId={product.id}
              title={product.title}
              price={Number(product.price)}
              imageUrl={product.image_url ?? undefined}
            />
          </div>
        </div>
      </div>
    </PageLayout>
  );
}
