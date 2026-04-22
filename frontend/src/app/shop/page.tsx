import { Suspense } from "react";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { ProductGrid } from "@/components/organisms/ProductGrid";
import { ShopSearch } from "@/components/molecules/ShopSearch";
import { EmptyState } from "@/components/molecules/EmptyState";
import { Pagination } from "@/components/molecules/Pagination";
import {
  DEMO_PRODUCTS,
  filterDemoProducts,
} from "@/lib/demo-products";

const PRODUCTS_PER_PAGE = 12;

async function ShopContent({
  search,
  page,
}: {
  search?: string;
  page?: number;
}) {
  const supabase = await getSupabaseClient();
  let pageNum = Math.max(1, Number(page) || 1);
  let offset = (pageNum - 1) * PRODUCTS_PER_PAGE;
  const hasSearch = Boolean(search?.trim());

  const searchParams: Record<string, string> = {};
  if (search) searchParams.search = search;

  let useDemo = false;
  let products: {
    id: string;
    title: string;
    description: string;
    price: number;
    image_url: string | null;
  }[] = [];
  let totalCount = 0;

  if (supabase) {
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

    const { data, count, error } = await query;

    if (error || !data) {
      useDemo = true;
    } else if (data.length === 0 && !hasSearch) {
      useDemo = true;
    } else {
      products = data;
      totalCount = count ?? data.length;
    }
  } else {
    useDemo = true;
  }

  if (useDemo) {
    const filtered = filterDemoProducts(DEMO_PRODUCTS, search);
    totalCount = filtered.length;
    const demoTotalPages = Math.max(
      1,
      Math.ceil(filtered.length / PRODUCTS_PER_PAGE)
    );
    pageNum = Math.min(pageNum, demoTotalPages);
    offset = (pageNum - 1) * PRODUCTS_PER_PAGE;
    products = filtered
      .slice(offset, offset + PRODUCTS_PER_PAGE)
      .map((p) => ({ ...p, image_url: p.image_url }));
  }

  const totalPages =
    totalCount > 0 ? Math.max(1, Math.ceil(totalCount / PRODUCTS_PER_PAGE)) : 1;

  if (products.length === 0 && hasSearch) {
    return (
      <div className="space-y-8">
        <EmptyState title="No products found." />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {useDemo && (
        <p
          className="text-center text-sm"
          style={{ color: "var(--theme-text-muted)" }}
        >
          Sample catalog for preview. Configure Supabase with real products to
          replace these listings.
        </p>
      )}
      <ProductGrid products={products} />
      <Pagination
        currentPage={pageNum}
        totalPages={totalPages}
        basePath="/shop"
        searchParams={searchParams}
      />
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
