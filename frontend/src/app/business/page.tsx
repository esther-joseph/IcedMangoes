export default function BusinessPage() {
  const adminEmails = process.env.ADMIN_EMAILS ?? "";

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-6 text-2xl font-semibold text-[var(--foreground)]">
        Business
      </h1>
      <div className="space-y-6 rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-6">
        <p className="text-[var(--foreground)]">
          Admin dashboard for fulfillment, orders, and settings.
        </p>
        <div className="rounded-lg bg-[var(--border)]/50 p-4">
          <h2 className="mb-2 font-medium text-[var(--foreground)]">
            Phase 3: Access control
          </h2>
          <p className="text-sm text-[var(--muted)]">
            Access will be restricted via Supabase Auth + RLS. Configure{" "}
            <code className="rounded bg-[var(--border)] px-1 py-0.5">
              ADMIN_EMAILS
            </code>{" "}
            (comma-separated) to define who can access this page.
          </p>
        </div>
        {adminEmails && (
          <p className="text-sm text-[var(--muted)]">
            <strong>ADMIN_EMAILS</strong> (from env): {adminEmails}
          </p>
        )}
      </div>
    </div>
  );
}
