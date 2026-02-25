"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCart } from "@/contexts/CartContext";

const SITE_NAME = "IcedMangoes";

function NavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isActive = pathname === href || (href !== "/" && pathname.startsWith(href));

  return (
    <Link
      href={href}
      className={`py-2 px-3 rounded-lg hover:opacity-80 transition-opacity ${
        isActive ? "font-medium" : "text-sm"
      }`}
      style={{
        color: isActive ? "var(--theme-accent)" : "var(--theme-text-muted)",
      }}
    >
      {children}
    </Link>
  );
}

export function Sidebar() {
  const { itemCount } = useCart();

  return (
    <nav
      className="flex flex-1 min-h-0 flex-col gap-1 p-4"
      style={{ color: "var(--theme-text)" }}
    >
      <Link
        href="/"
        className="py-2 px-3 rounded-lg font-semibold hover:opacity-80 transition-opacity"
        style={{ color: "var(--theme-text)" }}
      >
        {SITE_NAME}
      </Link>
      <NavLink href="/">Gallery</NavLink>
      <NavLink href="/shop">Shop</NavLink>
      <NavLink href="/business">Business</NavLink>

      <div
        className="mt-4 flex flex-col gap-2 border-t pt-4"
        style={{ borderColor: "var(--theme-border)" }}
      >
        <Link
          href="/cart"
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
          style={{
            background: "var(--theme-border)",
            color: "var(--theme-text)",
          }}
        >
          <svg
            className="w-5 h-5 shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <span>Cart</span>
          {itemCount > 0 && (
            <span
              className="flex min-w-[1.25rem] h-5 items-center justify-center rounded-full px-1 text-xs font-semibold text-white"
              style={{ background: "var(--theme-accent)" }}
            >
              {itemCount > 99 ? "99+" : itemCount}
            </span>
          )}
        </Link>
      </div>
    </nav>
  );
}
