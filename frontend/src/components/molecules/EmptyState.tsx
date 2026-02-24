import Link from "next/link";

interface EmptyStateProps {
  title: string;
  description?: React.ReactNode;
  actionLabel?: string;
  actionHref?: string;
}

export function EmptyState({
  title,
  description,
  actionLabel,
  actionHref,
}: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed border-[var(--border)] bg-[var(--card-bg)] px-8 py-16 text-center">
      <p className="mb-4 text-[var(--muted)]">{title}</p>
      {description != null && (
        <div className="text-sm text-[var(--muted)]">{description}</div>
      )}
      {actionLabel != null && actionHref != null && (
        <Link
          href={actionHref}
          className="mt-4 inline-block rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)]"
        >
          {actionLabel}
        </Link>
      )}
    </div>
  );
}
