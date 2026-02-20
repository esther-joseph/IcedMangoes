# IcedMangoes Frontend

Next.js (App Router) + Supabase artist storefront. Vercel-ready, no Docker.

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
- `/product/[id]` – Product detail
- `/business` – Admin page (Phase 3: gated by Supabase Auth + ADMIN_EMAILS)
