import { PageLayout } from "@/components/templates/PageLayout";

export default function BusinessPage() {
  const adminEmails = process.env.ADMIN_EMAILS ?? "";

  return (
    <PageLayout maxWidth="md">
      <h1 className="mb-6 text-2xl font-semibold text-[var(--foreground)]">
        Business
      </h1>
      <div className="space-y-6">
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-6">
          <h2 className="mb-2 font-medium text-[var(--foreground)]">
            Stripe Integration
          </h2>
          <p className="mb-4 text-sm text-[var(--muted)]">
            Add Stripe keys to your environment variables to enable checkout.
            Get keys from{" "}
            <a
              href="https://dashboard.stripe.com/apikeys"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-[var(--accent)]"
            >
              Stripe Dashboard
            </a>
            .
          </p>
          <p className="text-sm text-[var(--muted)]">
            <code className="rounded bg-[var(--border)] px-1 py-0.5">
              STRIPE_SECRET_KEY
            </code>
            ,{" "}
            <code className="rounded bg-[var(--border)] px-1 py-0.5">
              NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
            </code>
            ,{" "}
            <code className="rounded bg-[var(--border)] px-1 py-0.5">
              STRIPE_WEBHOOK_SECRET
            </code>
          </p>
          <p className="mt-4 text-sm text-[var(--muted)]">
            See{" "}
            <code className="rounded bg-[var(--border)] px-1 py-0.5">
              documentation/stripe-setup.md
            </code>{" "}
            in the repo for full setup steps.
          </p>
        </div>
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card-bg)] p-6">
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
    </PageLayout>
  );
}
