interface HeroProps {
  title: string;
  subtitle?: string;
}

export function Hero({ title, subtitle }: HeroProps) {
  return (
    <section className="mb-12 text-center" aria-labelledby="hero-title">
      <h1
        id="hero-title"
        className="mb-4 text-3xl font-semibold tracking-tight text-[var(--foreground)]"
      >
        {title}
      </h1>
      {subtitle != null && (
        <p className="mx-auto max-w-xl text-[var(--muted)]">{subtitle}</p>
      )}
    </section>
  );
}
