# IcedMangoes Frontend

Next.js (App Router) + Supabase artist storefront. Vercel-ready, no Docker.

**Full docs**: [documentation/frontend-vercel-supabase.md](../documentation/frontend-vercel-supabase.md)

## Local development

```bash
npm install
cp .env.example .env.local
# Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build

```bash
npm run build
npm start
```

## Pages

- `/` – Home (featured products)
- `/shop` – Paginated product list with search
- `/product/[id]` – Product detail, add to cart
- `/cart` – Cart and Stripe checkout
- `/checkout/success` – Post-payment thank-you page
- `/business` – Admin page, Stripe setup (Phase 3: gated by Supabase Auth)

## Component structure

Components follow atomic design. See [COMPONENTS.md](COMPONENTS.md) for details.

```
src/components/
├── atoms/       Badge, Button, Input, ProductImage
├── molecules/   AddToCartButton, CartItem, CartLink, CheckoutButton, EmptyState, Hero, Pagination, ShopSearch
├── organisms/   Navbar, ProductCard, ProductGrid
└── templates/   PageLayout
```

## Stripe

Add `STRIPE_SECRET_KEY`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` to enable paid checkout. See [documentation/stripe-setup.md](../documentation/stripe-setup.md).
