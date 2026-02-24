# Architecture Remediation Plan: Dual-Stack Consolidation

[← Back to Wiki](README.md)

**Document version**: 1.0  
**Created**: February 2025  
**Status**: Planning

---

## Executive Summary

IcedMangoes currently runs two parallel, independent stacks (Django + templates and Next.js + Supabase) that implement similar store functionality. This document summarizes the architectural analysis, the system design problems identified, and a detailed remediation plan to consolidate the system into a coherent, maintainable architecture.

---

## 1. What Happened: Context & Current State

### 1.1 Original Intent

The project appears to have evolved to support two deployment paths:

- **Django stack** (`store/`): Self-hosted, full control, Docker-friendly. Uses Django templates, SQLite/MongoDB (djongo), GraphQL, Stripe.
- **Next.js + Supabase stack** (`frontend/`): Serverless, "minimal setup" for artists who want to deploy to Vercel without Docker.

See [Frontend: Vercel + Supabase](frontend-vercel-supabase.md) for the stated goal: *"Ideal for artists who want minimal setup."*

### 1.2 How the Stacks Work Today

| Layer | Django Stack | Next.js Stack |
|-------|--------------|---------------|
| **Backend** | Django (Python) | Supabase (Postgres, BaaS) |
| **Database** | SQLite (dev) / MongoDB (prod, via djongo) | Supabase Postgres |
| **Auth** | Django auth (sessions) | Supabase Auth (JWT, magic links) |
| **Frontend** | Django templates + Tailwind | Next.js 16 + React 19 + Tailwind |
| **Payments** | Stripe (Django views) | Stripe (Next.js API routes) |
| **API** | GraphQL at `/graphql/` | Direct Supabase client (PostgREST) |

**Critical fact**: The two stacks do **not** share a backend. The Next.js app never talks to Django. Each stack has its own data, auth, and business logic.

### 1.3 Recent Additions

- Responsive design (mobile sidebar, hamburger menu)
- Blog page with Substack RSS integration
- Admin Substack configuration in Profile
- Journal-style blog component with month/year navigation

These were implemented in the Django stack only. The Next.js frontend does not have equivalent features.

---

## 2. System Design Problems Identified

### 2.1 Data: Split Source of Truth

Products, orders, and users exist in separate databases:

- **Django**: `Artwork`, `Order`, `OrderItem`, `Artist`, `SiteSettings`, etc. in SQLite/MongoDB
- **Next.js**: `products`, `orders`, `order_items` in Supabase Postgres

**Consequences**:

- No single source of truth for products or orders
- A product added in Django does not appear in the Next.js shop
- Order history is fragmented across systems
- Reporting and analytics require two pipelines
- Inventory or fulfillment logic cannot be unified

---

### 2.2 Domain: Duplicate Feature Implementation

The same domain logic is implemented twice:

| Feature | Django Implementation | Next.js Implementation |
|---------|----------------------|-------------------------|
| Product listing | `ArtworkService.get_available_artworks()` | Supabase `from("products").select()` |
| Cart | Session-based in Django | `CartContext` (client state) |
| Checkout | Django views + Stripe | Next.js API route `/api/checkout` |
| Stripe webhooks | `store/webhooks.py` | `frontend/src/app/api/webhooks/stripe/route.ts` |
| Auth | Django Login/Logout | Supabase Auth |

**Consequences**:

- Bug fixes and security patches must be applied twice
- Business rules can diverge (pricing, tax, validation)
- Feature parity is hard to maintain
- New features require double the implementation effort

---

### 2.3 Architecture: Unclear System Boundary

It is ambiguous whether:

- These are two separate products
- Two deployment options for the same product
- A migration in progress (Django → Next.js or vice versa)

**Consequences**:

- Unclear ownership of features and bugs
- Confusion about which stack to extend for new work
- Configuration and secrets managed in two places
- Monitoring and alerting split across systems

---

### 2.4 Identity: Split Authentication

- **Django**: Sessions, `User` model, `/login/`, `/logout/`
- **Next.js/Supabase**: Supabase Auth (JWT, OAuth, magic links)

**Consequences**:

- No shared user identity across both UIs
- Different user bases and permission models
- Cannot easily expose cross-stack features (e.g. admin in Next.js for Django data)
- User migration or SSO would require custom bridging

---

### 2.5 Integration: Non-Uniform API Surface

- **Django**: GraphQL at `/graphql/` (Graphene-Django)
- **Next.js**: Direct Supabase client calls (PostgREST)

There is no single API contract that both frontends consume. Changes to data models or business rules require updates in multiple places.

---

### 2.6 Operations: Divergent Infrastructure

- **Django**: Typically Docker, self-hosted, MongoDB or SQLite
- **Next.js**: Vercel (serverless), Supabase (managed Postgres)

**Consequences**:

- Two deployment pipelines
- Different backup, scaling, and monitoring strategies
- Higher operational overhead
- More complex onboarding for new contributors

---

### 2.7 Communication: Missing Architecture Decision Records

No explicit documentation of:

- Why two stacks exist
- Which stack to use for new features
- Data ownership and migration strategy
- Long-term consolidation roadmap

This leads to ambiguity and drift.

---

## 3. Remediation Plan: Overview

**Goal**: Move to a single source of truth and a clear, maintainable architecture.

**Principle**: Pick one backend as canonical. Frontends become thin clients that consume a shared API.

---

## 4. Phase 1: Decision & Documentation (1–2 weeks)

### 4.1 Choose the Canonical Backend

| Option | Pros | Cons |
|--------|------|------|
| **Django** | Richer domain logic, GraphQL, fulfillment, admin, business page | Requires hosting; MongoDB/SQLite vs Supabase |
| **Supabase** | Managed, scalable, realtime, Vercel-friendly | Less domain logic; would need to rebuild admin, fulfillment, GraphQL |

**Recommendation**: Choose **Django** if the project emphasizes fulfillment, admin tooling, and business features. Choose **Supabase** if the priority is minimal ops and Vercel-only deployment.

### 4.2 Document the Decision

1. Create `documentation/ARCHITECTURE_DECISION_RECORD.md` (ADR).
2. Record: chosen backend, deprecation timeline for the other, migration approach.
3. Update [Architecture Overview](architecture.md) to reflect the target state.

### 4.3 Define Target Architecture

Document the intended layout, for example:

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  Django Templates (storefront)  │  Next.js (optional SPA)   │
└─────────────────┬───────────────┴──────────────┬────────────┘
                  │                              │
                  ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER                                 │
│           Django REST / GraphQL (single API)                 │
└─────────────────────────────────┬───────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                 │
│        Django ORM → SQLite (dev) / MongoDB or Postgres       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Phase 2: Consolidate on Django Backend (8–12 weeks)

*Assumes Django is chosen as the canonical backend.*

### 5.1 Expand Django API Surface

| Task | Description |
|------|-------------|
| **REST endpoints** | Add REST API (Django REST Framework or manual) for products, cart, checkout, orders. GraphQL can remain for admin/internal use. |
| **Auth for SPA** | Add JWT or session-based auth suitable for Next.js (e.g. `django-rest-framework-simplejwt`, or session cookies with same-site). |
| **CORS** | Configure CORS for the Next.js origin (e.g. `localhost:3000`, Vercel domain). |

### 5.2 Migrate Next.js to Use Django API

| Task | Description |
|------|-------------|
| **Replace Supabase client** | Create an API client (fetch/axios) that calls Django REST/GraphQL instead of Supabase. |
| **Remove Supabase Auth** | Implement login/logout via Django; store session/JWT in Next.js. |
| **Migrate product queries** | Swap Supabase `from("products")` for Django API calls. |
| **Migrate checkout flow** | Point Next.js checkout to Django checkout endpoint. |
| **Migrate Stripe webhooks** | Route Stripe webhooks to Django only; remove duplicate webhook handler from Next.js. |

### 5.3 Data Migration (if Supabase has production data)

| Task | Description |
|------|-------------|
| **Export from Supabase** | Export products, orders, order_items from Supabase. |
| **Transform** | Map Supabase schema to Django models (products → Artwork, etc.). |
| **Import** | Load into Django DB with idempotency/conflict handling. |
| **Verify** | Compare counts, spot-check records. |

### 5.4 Deprecate Supabase

| Task | Description |
|------|-------------|
| **Remove Supabase deps** | Remove `@supabase/ssr`, `@supabase/supabase-js` from Next.js. |
| **Remove Supabase schema** | Archive migration files; no longer run against Supabase. |
| **Update env vars** | Remove Supabase env vars from Next.js; add Django API URL and auth config. |

---

## 6. Phase 3: Consolidate on Supabase (Alternative, 8–12 weeks)

*If Supabase is chosen instead.*

### 6.1 Migrate Django Features to Supabase/Next.js

| Task | Description |
|------|-------------|
| **Fulfillment logic** | Reimplement fulfillment, provider integrations in Next.js API routes or Supabase Edge Functions. |
| **Admin panel** | Build admin UI in Next.js (or keep minimal Django admin for internal use only). |
| **Business page** | Recreate in Next.js. |
| **GraphQL** | Add GraphQL layer (e.g. Hasura, PostGraphile) over Supabase, or use REST/PostgREST. |

### 6.2 Migrate Data from Django to Supabase

| Task | Description |
|------|-------------|
| **Export** | Dump Artwork, Order, OrderItem, Artist from Django. |
| **Transform** | Map to Supabase tables (products, orders, order_items). |
| **Import** | Load into Supabase; handle relations and constraints. |

### 6.3 Deprecate Django Storefront

| Task | Description |
|------|-------------|
| **Redirect** | Point root domain to Next.js (Vercel). |
| **Archive** | Move Django app to read-only or archive; document for historical reference. |

---

## 7. Phase 4: Single-Stack Simplification (Optional, 4–6 weeks)

*After backend consolidation.*

### 7.1 Option A: Keep Both UIs, One Backend

- Django templates and Next.js both call Django API.
- Useful if you want server-rendered (Django) and SPA (Next.js) options.

### 7.2 Option B: Deprecate One UI

| Deprecate Django templates | Deprecate Next.js |
|----------------------------|-------------------|
| Make Next.js the only storefront | Make Django templates the only storefront |
| Redirect Django routes to Next.js | Remove Next.js app; simplify deployment |
| Reduces maintenance of two UIs | Simpler stack; fewer moving parts |

### 7.3 Option C: Hybrid

- Django templates for core store (home, shop, product, cart, checkout).
- Next.js only for specific experiences (e.g. business dashboard) that benefit from React.

---

## 8. Phase 5: Shared Code & Standards (Ongoing)

### 8.1 Design System

- Extract shared Tailwind config, theme variables, and component patterns.
- Option: Publish a small shared package or use a monorepo with a `packages/design-system` workspace.

### 8.2 Type & Schema Sharing

- Define shared TypeScript types (Product, Order, CartItem) that mirror Django models.
- Consider code generation from Django models or OpenAPI/GraphQL schema.

### 8.3 Documentation

- Keep [Architecture Overview](architecture.md) current.
- Add ADRs for major decisions.
- Document API contracts (REST/GraphQL) in [API Reference](api-reference.md).

---

## 9. Implementation Checklist (Django Backend Path)

Use this checklist if consolidating on Django:

- [ ] ADR created: Django chosen as canonical backend
- [ ] Django REST/GraphQL endpoints for products, cart, checkout, orders
- [ ] JWT or session auth for Next.js
- [ ] CORS configured for Next.js origin
- [ ] Next.js API client replaces Supabase
- [ ] Next.js auth uses Django
- [ ] Stripe webhooks centralized in Django
- [ ] Data migrated from Supabase (if any)
- [ ] Supabase removed from Next.js
- [ ] Integration tests for API and checkout
- [ ] Architecture docs updated
- [ ] Runbook for deployment and operations

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Data loss during migration | Full backups; dry-run imports; rollback plan |
| Downtime | Blue-green or staged cutover; feature flags |
| Regression in checkout | Automated E2E tests; parallel running period |
| Team unfamiliarity | Pairing; documentation; small incremental changes |

---

## 11. Timeline Summary

| Phase | Duration | Outcome |
|-------|----------|---------|
| Phase 1: Decision & documentation | 1–2 weeks | ADR, target architecture doc |
| Phase 2 or 3: Backend consolidation | 8–12 weeks | Single source of truth |
| Phase 4: UI simplification (optional) | 4–6 weeks | One or two UIs, clearly scoped |
| Phase 5: Shared code (ongoing) | Continuous | Less duplication, clearer standards |

---

## 12. References

- [Architecture Overview](architecture.md)
- [Frontend: Vercel + Supabase](frontend-vercel-supabase.md)
- [API Reference](api-reference.md)
- [Tech: Django](tech-django.md)
- [Tech: GraphQL](tech-graphql.md)
