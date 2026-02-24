import Link from "next/link";
import { PageLayout } from "@/components/templates/PageLayout";

export default function CheckoutSuccessPage() {
  return (
    <PageLayout maxWidth="md">
      <div className="text-center">
        <h1 className="mb-4 text-2xl font-semibold text-[var(--foreground)]">
          Thank you for your order
        </h1>
        <p className="mb-8 text-[var(--muted)]">
          Your payment was successful. You will receive a confirmation email shortly.
        </p>
        <Link
          href="/shop"
          className="inline-block rounded-lg bg-[var(--accent)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--accent-hover)]"
        >
          Continue shopping
        </Link>
      </div>
    </PageLayout>
  );
}
