import Link from "next/link";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  basePath?: string;
  searchParams?: Record<string, string>;
}

/** Server component - pagination with Next.js Link. */
export function Pagination({
  currentPage,
  totalPages,
  basePath = "/shop",
  searchParams = {},
}: PaginationProps) {
  if (totalPages <= 1) return null;

  const buildHref = (page: number) => {
    const params = new URLSearchParams(searchParams);
    params.set("page", String(page));
    return `${basePath}?${params.toString()}`;
  };

  return (
    <nav
      className="flex justify-center gap-2"
      aria-label="Pagination"
    >
      {currentPage > 1 && (
        <Link
          href={buildHref(currentPage - 1)}
          className="rounded-lg border border-[var(--border)] px-4 py-2 text-sm hover:bg-[var(--border)]"
          aria-label="Previous page"
        >
          Previous
        </Link>
      )}
      <span
        className="flex items-center px-4 py-2 text-sm text-[var(--muted)]"
        aria-live="polite"
      >
        Page {currentPage} of {totalPages}
      </span>
      {currentPage < totalPages && (
        <Link
          href={buildHref(currentPage + 1)}
          className="rounded-lg border border-[var(--border)] px-4 py-2 text-sm hover:bg-[var(--border)]"
          aria-label="Next page"
        >
          Next
        </Link>
      )}
    </nav>
  );
}
