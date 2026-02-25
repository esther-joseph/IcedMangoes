import Link from "next/link";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { Hero } from "@/components/molecules/Hero";
import { EmptyState } from "@/components/molecules/EmptyState";
import { ProductGrid } from "@/components/organisms/ProductGrid";
import { PageLayout } from "@/components/templates/PageLayout";

export default async function HomePage() {
  const supabase = await getSupabaseClient();
  let products: { id: string; title: string; description: string; price: number; image_url: string | null }[] = [];

  if (supabase) {
    const { data } = await supabase
      .from("products")
      .select("id, title, description, price, image_url")
      .eq("active", true)
      .order("created_at", { ascending: false })
      .limit(8);
    if (data) products = data;
  }

  return (
    <PageLayout>
      <Hero
        title="Discover & collect art"
        subtitle="A clean, artist-friendly storefront. Deploy to Vercel with Supabase in minutes."
      />

      {products.length === 0 ? (
        <EmptyState
          title="No products yet."
          description={
            <>
              <p className="mb-2">
                Add products via Supabase dashboard or the{" "}
                <Link href="/business" className="underline hover:text-[var(--accent)]">
                  Business
                </Link>{" "}
                page (Phase 3).
              </p>
              <p className="text-xs">
                Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are set
                in .env.local
              </p>
            </>
          }
        />
      ) : (
        <>
          <h2 className="mb-6 text-xl font-medium text-[var(--foreground)]">
            Featured
          </h2>
          <ProductGrid products={products} />
          <div className="mt-10 text-center">
            <Link
              href="/shop"
              className="inline-flex items-center gap-2 rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)]"
            >
              View all
            </Link>
          </div>
        </>
      )}
    </PageLayout>
  );
}
