import Link from "next/link";

export function Navbar() {
  const adminEmails = process.env.ADMIN_EMAILS?.split(",").map((e) =>
    e.trim().toLowerCase()
  );
  const showBusiness = true; // Phase 3: gate by auth, check adminEmails

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
