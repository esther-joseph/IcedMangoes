import Link from "next/link";
import { getSupabaseClient } from "@/lib/supabase/get-client";
import { ProductCard } from "@/components/ProductCard";

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
    <div className="mx-auto max-w-6xl px-4 py-12">
      <section className="mb-12 text-center">
        <h1 className="mb-4 text-3xl font-semibold tracking-tight text-[var(--foreground)]">
          Discover & collect art
        </h1>
        <p className="mx-auto max-w-xl text-[var(--muted)]">
          A clean, artist-friendly storefront. Deploy to Vercel with Supabase in
          minutes.
        </p>
      </section>

      {products.length === 0 ? (
        <div className="rounded-xl border border-dashed border-[var(--border)] bg-[var(--card-bg)] px-8 py-16 text-center">
          <p className="mb-4 text-[var(--muted)]">No products yet.</p>
          <p className="text-sm text-[var(--muted)]">
            Add products via Supabase dashboard or the{" "}
            <Link href="/business" className="underline hover:text-[var(--accent)]">
              Business
            </Link>{" "}
            page (Phase 3).
          </p>
          <p className="mt-4 text-xs text-[var(--muted)]">
            Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are
            set in .env.local
          </p>
        </div>
      ) : (
        <>
          <h2 className="mb-6 text-xl font-medium text-[var(--foreground)]">
            Featured
          </h2>
          <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-4">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
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
    </div>
  );
}
