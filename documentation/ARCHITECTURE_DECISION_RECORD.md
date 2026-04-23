# Architecture Decision Record: Django as Canonical Backend

**ADR-001**  
**Status**: Accepted  
**Date**: 2026-04-22  
**Supersedes**: N/A  

---

## Context

IcedMangoes has two independent stacks — Django (server-rendered storefront) and Next.js + Supabase (serverless SPA) — each with their own database, auth, cart, checkout, and Stripe webhook handler. This creates duplicate maintenance burden, split order history, and no single source of truth for products or users.

See [`architecture-remediation-plan.md`](architecture-remediation-plan.md) for the full analysis.

---

## Decision

**Django is the canonical backend.** The Next.js frontend will be migrated to consume the Django REST API instead of calling Supabase directly.

---

## Rationale

| Factor | Why Django wins |
|--------|----------------|
| Domain logic | Fulfillment, admin panel, business page, GraphQL are already built in Django |
| Data completeness | All real order + artwork data lives in Django (SQLite/MongoDB) |
| Extensibility | Service layer, migrations, and GraphQL schema are already in place |
| Ops overhead | One backend to deploy, monitor, and back up instead of two |

Supabase is kept only for file storage (`SUPABASE_STORAGE_BUCKET`). Auth and data move to Django.

---

## Migration Plan (Phase 2 of `architecture-remediation-plan.md`)

### What's already done (this commit)

- **REST API** at `/api/` — `GET /api/artworks/`, `/api/artworks/<id>/`, `/api/cart/`, `/api/orders/`, `/api/orders/<id>/`
- **CORS** configured via `CORS_ALLOWED_ORIGINS` env var (defaults to `http://localhost:3000`)
- **DRF** (`djangorestframework`) added to the stack with session auth

### Next steps for Next.js migration

| Task | File(s) to change |
|------|------------------|
| Replace `supabase.from("products")` with `fetch("/api/artworks/")` | `frontend/src/app/shop/page.tsx`, `frontend/src/app/product/[id]/page.tsx` |
| Replace Supabase auth with Django session login | `frontend/src/lib/supabase/client.ts` → new `frontend/src/lib/django-client.ts` |
| Point checkout webhook to Django only | Remove `frontend/src/app/api/webhooks/stripe/route.ts` |
| Replace cart context (Supabase) with `/api/cart/` | `frontend/src/contexts/CartContext.tsx` |
| Remove Supabase packages | `frontend/package.json` — remove `@supabase/ssr`, `@supabase/supabase-js` |
| Remove Supabase env vars from Next.js | `frontend/.env.local` / Vercel dashboard |

### API endpoints available now

| Method | Path | Auth required | Description |
|--------|------|--------------|-------------|
| GET | `/api/artworks/` | No | List available artworks with images and product variants |
| GET | `/api/artworks/<id>/` | No | Single artwork detail |
| GET | `/api/cart/` | No | Current cart (session for anon, DB for auth users) |
| GET | `/api/orders/` | Yes (session) | Authenticated user's order history |
| GET | `/api/orders/<id>/` | Yes (session) | Single order detail |

### Future API endpoints needed

| Endpoint | Purpose |
|----------|---------|
| `POST /api/cart/add/` | Add item to cart from Next.js |
| `POST /api/cart/remove/` | Remove item |
| `POST /api/auth/login/` | JSON login for Next.js (returns session cookie) |
| `POST /api/auth/logout/` | JSON logout |
| `GET /api/auth/me/` | Current user info |

---

## Consequences

- **Positive**: Single source of truth, unified order history, one Stripe webhook handler, no data drift between stacks.
- **Negative**: Next.js loses Supabase Realtime (no live updates) and magic-link auth. Both can be added later via Django Channels and email-token login if needed.
- **Neutral**: Supabase Storage can remain for file hosting — it's unrelated to the auth/data split.

---

## Checklist

- [x] ADR created
- [x] Django REST API endpoints for artworks, cart, orders
- [x] CORS configured for Next.js origin
- [x] DRF added to `INSTALLED_APPS` and `requirements.txt`
- [ ] Next.js API client replaces Supabase client
- [ ] Next.js auth uses Django sessions
- [ ] Stripe webhooks centralized in Django (remove `frontend/src/app/api/webhooks/stripe/route.ts`)
- [ ] Supabase `@supabase/ssr` / `@supabase/supabase-js` removed from Next.js
- [ ] Integration tests for REST API
- [ ] Runbook updated
