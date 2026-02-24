# Frontend: Vercel + Supabase

[← Back to Wiki](README.md)

The `/frontend` directory contains a **Next.js (App Router) + Supabase** storefront. Deploy to Vercel without Docker. Ideal for artists who want minimal setup.

---

## Quick start (local)

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local: add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon (public) key |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only; for webhook order creation |
| `STRIPE_SECRET_KEY` | Stripe secret key (checkout) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `ADMIN_EMAILS` | Comma-separated emails for /business (Phase 3) |

---

## Supabase setup

1. Create a project at [supabase.com](https://supabase.com)
2. **SQL Editor** → paste contents of `frontend/supabase/migrations/001_initial_schema.sql` → run
3. **Storage** → New bucket → name: `media` → public: yes
4. See [frontend/docs/SUPABASE_SCHEMA.md](../frontend/docs/SUPABASE_SCHEMA.md) for schema details and image URL strategy

---

## Vercel deployment

1. Push the repo to GitHub
2. [Vercel](https://vercel.com) → Import Project
3. Set **Root Directory** to `frontend`
4. Add environment variables
5. Deploy

---

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home — featured products grid |
| `/shop` | Paginated product list with search |
| `/product/[id]` | Product detail, add to cart |
| `/cart` | Cart, checkout with Stripe |
| `/checkout/success` | Post-payment thank-you page |
| `/business` | Admin page, Stripe setup (Phase 3: gated by Supabase Auth) |

---

## Stripe checkout

Stripe is integrated for checkout. Add `STRIPE_SECRET_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` to enable paid checkout. See [Stripe Setup](stripe-setup.md).

---

## Phase 3: Auth & admin gating

Access to `/business` will be restricted via Supabase Auth and `ADMIN_EMAILS`. Until then, the page is accessible to all.
