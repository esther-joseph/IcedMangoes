import Link from "next/link";
import { notFound } from "next/navigation";
import { getSupabaseClient } from "@/lib/supabase/get-client";

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
    <div className="mx-auto max-w-4xl px-4 py-12">
      <div className="grid gap-8 md:grid-cols-2">
        <div className="aspect-square overflow-hidden rounded-xl bg-[var(--border)]">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.title}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-[var(--muted)]">
              No image
            </div>
          )}
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
          <p className="mt-6 text-sm text-[var(--muted)]">
            Stripe checkout coming in Phase 2.
          </p>
        </div>
      </div>
    </div>
  );
}
