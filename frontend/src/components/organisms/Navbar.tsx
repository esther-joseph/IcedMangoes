import Link from "next/link";
import { CartLink } from "@/components/molecules/CartLink";

export function Navbar() {
  const showBusiness = true; // Phase 3: gate by auth

  return (
    <nav className="border-b border-[var(--border)] bg-[var(--card-bg)]">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="text-lg font-semibold text-[var(--foreground)]">
          IcedMangoes
        </Link>
        <div className="flex items-center gap-6">
          <Link
            href="/"
            className="text-sm text-[var(--foreground)] hover:text-[var(--accent)]"
          >
            Home
          </Link>
          <Link
            href="/shop"
            className="text-sm text-[var(--foreground)] hover:text-[var(--accent)]"
          >
            Shop
          </Link>
          <CartLink />
          {showBusiness && (
            <Link
              href="/business"
              className="text-sm text-[var(--muted)] hover:text-[var(--accent)]"
            >
              Business
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
