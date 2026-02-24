import { Suspense } from "react";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { ProductGrid } from "@/components/organisms/ProductGrid";
import { ShopSearch } from "@/components/molecules/ShopSearch";
import { EmptyState } from "@/components/molecules/EmptyState";
import { Pagination } from "@/components/molecules/Pagination";

const PRODUCTS_PER_PAGE = 12;

async function ShopContent({
  search,
  page,
}: {
  search?: string;
  page?: number;
}) {
  const supabase = await getSupabaseClient();
  const pageNum = Math.max(1, Number(page) || 1);
  const offset = (pageNum - 1) * PRODUCTS_PER_PAGE;

  if (!supabase) {
    return (
      <div className="rounded-xl border border-dashed border-[var(--border)] px-8 py-16 text-center text-[var(--muted)]">
        Configure Supabase in .env.local to view products.
      </div>
    );
  }

  let query = supabase
    .from("products")
    .select("id, title, description, price, image_url", { count: "exact" })
    .eq("active", true)
    .order("created_at", { ascending: false })
    .range(offset, offset + PRODUCTS_PER_PAGE - 1);

  if (search?.trim()) {
    const term = search.trim().replace(/%|'/g, "");
    if (term) {
      query = query.or(`title.ilike.%${term}%,description.ilike.%${term}%`);
    }
  }

  const { data: products, count, error } = await query;

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 px-8 py-16 text-center text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
        Error loading products.
      </div>
    );
  }

  const totalPages = count ? Math.ceil(count / PRODUCTS_PER_PAGE) : 0;

  const searchParams: Record<string, string> = {};
  if (search) searchParams.search = search;

  return (
    <div className="space-y-8">
      {products?.length === 0 ? (
        <EmptyState title="No products found." />
      ) : (
        <>
          <ProductGrid products={products ?? []} />
          <Pagination
            currentPage={pageNum}
            totalPages={totalPages}
            basePath="/shop"
            searchParams={searchParams}
          />
        </>
      )}
    </div>
  );
}

export default async function ShopPage({
  searchParams,
}: {
  searchParams: Promise<{ search?: string; page?: string }>;
}) {
  const params = await searchParams;

  return (
    <div className="mx-auto max-w-6xl w-full px-4 py-12">
      <h1 className="mb-8 text-2xl font-semibold text-[var(--foreground)]">
        Shop
      </h1>
      <div className="mb-8">
        <ShopSearch defaultValue={params.search} />
      </div>
      <Suspense
        fallback={
          <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="h-80 animate-pulse rounded-xl bg-[var(--border)]"
              />
            ))}
          </div>
        }
      >
        <ShopContent search={params.search} page={Number(params.page) || 1} />
      </Suspense>
    </div>
  );
}
