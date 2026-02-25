import Link from "next/link";

export default function ProductNotFound() {
  return (
    <div className="mx-auto max-w-xl px-4 py-16 text-center">
      <h1 className="text-xl font-semibold text-[var(--foreground)]">
        Product not found
      </h1>
      <p className="mt-2 text-[var(--muted)]">
        This product may have been removed or does not exist.
      </p>
      <Link
        href="/shop"
        className="mt-6 inline-block rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)]"
      >
        Back to shop
      </Link>
    </div>
  );
}
