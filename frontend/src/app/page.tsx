import Link from "next/link";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { Hero } from "@/components/molecules/Hero";
import { ProductGrid } from "@/components/organisms/ProductGrid";
import { PageLayout } from "@/components/templates/PageLayout";
import {
  DEMO_PRODUCTS,
  getDemoProductsForGrid,
} from "@/lib/demo-products";

export default async function HomePage() {
  const supabase = await getSupabaseClient();
  let products: {
    id: string;
    title: string;
    description: string;
    price: number;
    image_url: string | null;
  }[] = [];
  let showingDemo = false;

  if (supabase) {
    const { data, error } = await supabase
      .from("products")
      .select("id, title, description, price, image_url")
      .eq("active", true)
      .order("created_at", { ascending: false })
      .limit(8);
    if (!error && data?.length) products = data;
  }

  if (products.length === 0) {
    products = getDemoProductsForGrid()
      .slice(0, 8)
      .map((p) => ({ ...p, image_url: p.image_url }));
    showingDemo = true;
  }

  return (
    <PageLayout>
      <Hero
        title="Discover & collect art"
        subtitle="A clean, artist-friendly storefront. Deploy to Vercel with Supabase in minutes."
      />

      {showingDemo && (
        <p
          className="mb-6 text-center text-sm"
          style={{ color: "var(--theme-text-muted)" }}
        >
          Showing sample artwork from the demo catalog ({DEMO_PRODUCTS.length}{" "}
          pieces). Connect Supabase and add products to replace this gallery.
        </p>
      )}

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
    </PageLayout>
  );
}
