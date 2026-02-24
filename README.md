# IcedMangoes

A backend architecture showcase and artist storefront template demonstrating clean architecture, service-layer design, and production-oriented practices.

**Documentation**: [documentation/README.md](documentation/README.md) – wiki with setup, tech stack, and API guides. **New?** Start with [Installation & Deployment](documentation/installation-and-deployment.md).

---

## Recent Updates & Features

### Django Store

- **Responsive design** — Mobile-first layout with collapsible sidebar (hamburger menu), touch-friendly controls, and viewport meta
- **Blog page** — Substack RSS integration at `/blog/` with a journal-style list of posts
- **Admin Substack config** — Staff can set the Substack publication URL in Profile; posts appear on the Blog page
- **Month/year navigation** — In-page navigation bar to jump between blog post sections by publication date
- **Atomic design** — Components organized into `atoms/`, `molecules/`, `organisms/` (see [documentation/ATOMIC_DESIGN.md](documentation/ATOMIC_DESIGN.md))
- **Admin/Guest toggle** — Testing toggle at bottom of sidebar to preview nav as admin or guest
- **Profile for all users** — Profile page accessible to both admin and guest; same layout with role-appropriate data and actions (admin-only forms disabled for guests)

### Next.js Frontend

- **Atomic design** — Reusable component hierarchy: atoms (Badge, Button, Input, ProductImage), molecules (Hero, EmptyState, Pagination, CartItem, ShopSearch, etc.), organisms (Navbar, ProductCard, ProductGrid), templates (PageLayout)
- **next/image** — Product images via `ProductImage` with remote patterns for Supabase
- **Link-based pagination** — Shop uses `next/link` for pagination (no `<a>` tags)
- **Shared layout** — `PageLayout` template for consistent page containers
- **Component docs** — [frontend/COMPONENTS.md](frontend/COMPONENTS.md) documents structure and server vs client components

### Architecture

- **Remediation plan** — [documentation/architecture-remediation-plan.md](documentation/architecture-remediation-plan.md) outlines dual-stack consolidation and system design improvements

---

## Two Deployment Paths

| Path | Stack | Best for |
|------|-------|----------|
| **Django Backend** | Django, MongoDB/SQLite, Tailwind, Stripe | Full control, GraphQL API, cart/checkout, fulfillment |
| **Next.js Frontend** | Next.js, Supabase, Vercel | Minimal setup, no Docker, deploy in minutes |

---

## Open Source Philosophy

This project is intentionally structured as a modular, production-oriented template to accelerate storefront development while maintaining architectural clarity.

Contributions, issues, and pull requests are welcome.

---

## Artist-Friendly Deployment (Recommended): Vercel + Supabase

The `/frontend` directory contains a **Next.js (App Router) + Supabase** storefront designed for artists who want to deploy quickly without Docker.

- **Deploy to Vercel** in a few clicks
- **Supabase** provides database + storage (single provider)
- **Stripe** checkout integrated
- No Docker required

### Quick start (local)

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your Supabase URL and anon key
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Environment variables

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon (public) key |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only; for webhook order creation |
| `STRIPE_SECRET_KEY` | Stripe secret key (checkout) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `ADMIN_EMAILS` | Comma-separated emails for /business (Phase 3) |

### Supabase setup

1. Create a project at [supabase.com](https://supabase.com)
2. Run the schema: copy `frontend/supabase/migrations/001_initial_schema.sql` into SQL Editor and execute
3. Create a **Storage bucket** named `media` (public) for product images
4. See [frontend/docs/SUPABASE_SCHEMA.md](frontend/docs/SUPABASE_SCHEMA.md) for details

### Vercel deployment

1. Push to GitHub
2. Import the repo in Vercel
3. Set the **Root Directory** to `frontend`
4. Add the environment variables above
5. Deploy

See [frontend/README.md](frontend/README.md) and [documentation/frontend-vercel-supabase.md](documentation/frontend-vercel-supabase.md) for details.

---

## 1. Project Overview

IcedMangoes implements a storefront API and presentation layer for an artist marketplace. The focus is on maintainable backend design: clear separation of concerns, testable business logic, and reproducible deployment. Views remain thin; domain logic lives in dedicated services.

---

## 2. Tech Stack

### Django backend (store root)

| Layer | Technology |
|-------|------------|
| Framework | Django 3.2–4.1 |
| Database | MongoDB (via Djongo) or SQLite (optional, `USE_SQLITE=1`) |
| API | GraphQL (Graphene-Django) |
| ORM (optional) | Prisma Client Python (SQLite) |
| Media | Pillow, django-storages (Supabase S3 for production) |
| Runtime | Python 3.11 |
| Frontend | Tailwind CSS, PostCSS, CSS custom properties (theme switching) |
| Build | Node.js, npm (for CSS) |
| Orchestration | Docker Compose |

### Next.js frontend (`/frontend`)

| Layer | Technology |
|-------|------------|
| Framework | Next.js 16 (App Router) |
| Database | Supabase (PostgreSQL) |
| Storage | Supabase Storage (media bucket) |
| Payments | Stripe Checkout |
| Hosting | Vercel |
| Styling | Tailwind CSS 4 |

---

## 3. Architectural Design

### Service Layer Pattern

Views delegate to a service layer instead of embedding business logic. `ArtworkService` encapsulates queries and filtering; views handle HTTP concerns only. This improves testability and keeps controllers focused on request/response handling.

```
Request -> View -> Service -> Model -> Database
```

### SOLID in Practice

- **Single Responsibility**: `services.py` owns domain logic; `views.py` handles rendering and HTTP. Each module has one reason to change.
- **Open/Closed**: `ArtworkService` can be extended via subclasses or composition without modifying existing code.
- **Liskov Substitution**: A different implementation (e.g., cached, read-replica) can replace `ArtworkService` where it is injected.
- **Interface Segregation**: Service interfaces are narrow and purpose-specific rather than monolithic.
- **Dependency Inversion**: Views depend on the service abstraction; the concrete implementation can be injected for testing or swapping backends.

---

## 4. Containerized Development Environment

Docker Compose provides environment parity across machines and CI. No "works on my machine" variance: the same images run locally and in pipeline contexts.

- **web**: Django application (port 8000)
- **mongodb**: MongoDB instance (port 27017)
- **mongo-express**: Database UI for inspection (port 8081)

Volumes persist data; `.env` holds credentials. The setup mirrors a minimal production topology.

---

## 5. Local Setup Instructions

For a full installation checklist, tool verification, and deployment guide, see [Installation & Deployment](documentation/installation-and-deployment.md).

**Option A: Docker**

Prerequisites: Docker and Docker Compose.

```bash
docker-compose up --build
```

In a separate terminal:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser   # optional
```

**Option B: Local Python (no Docker)**

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install
npm run build:css
USE_SQLITE=1 python manage.py migrate
USE_SQLITE=1 python manage.py runserver
```

**Prisma (optional, SQLite only)**:

```bash
export DATABASE_URL="file:./db.sqlite3"
prisma generate
```

**GraphQL examples** (http://localhost:8000/graphql/):

```graphql
# Query artworks
query { artworks { id title price artist { name } } }

# Query single artwork
query { artwork(id: 1) { title description price } }

# Create artwork (metadata only; image via form)
mutation {
  createArtwork(
    artistName: "Jane Doe"
    title: "Sunset"
    description: "Oil on canvas"
    price: 199.99
    tags: "abstract, landscape"
  ) { ok artwork { id title } }
}
```

**Endpoints**:

- Application: http://localhost:8000
- Blog: http://localhost:8000/blog/ — Substack feed with month/year navigation
- Business (admin): http://localhost:8000/business/ — fulfillment configuration, provider integrations
- Profile: http://localhost:8000/profile/ — dashboard (admin), or layout preview (guest)
- GraphQL (GraphiQL): http://localhost:8000/graphql/
- Mongo Express: http://localhost:8081 (Docker only)

**Business (Admin) Page** — Staff users can configure fulfillment mode (Self-Fulfillment vs Print-on-Demand), select providers (Shippo, EasyPost, Printful, Printify, Gelato), and manage API keys. Use env vars for production; DB-stored keys are for local demos only. See [documentation/business-page.md](documentation/business-page.md).

**Media Storage (Supabase)** — Render and similar platforms have ephemeral filesystems. For production, use [Supabase Storage](documentation/deploy-render.md#media-storage-supabase-storage) for artwork images. When `SUPABASE_*` env vars are set, uploads go to Supabase; otherwise they use local `media/`.

**Protecting Artwork from AI Training & Style Mimicry** — Use [Glaze](https://glaze.cs.uchicago.edu/), [WebGlaze](https://glaze.cs.uchicago.edu/webglaze.html), or [Nightshade](https://nightshade.cs.uchicago.edu/) (University of Chicago SAND Lab) to preprocess images before uploading. See [documentation/ART_PROTECTION.md](documentation/ART_PROTECTION.md) for workflow and best practices.

---

## 6. Engineering Decisions and Tradeoffs

**MongoDB over PostgreSQL/SQLite**

- Schema flexibility for early-stage product iteration; adding fields or nesting documents does not require migrations.
- Faster prototyping when requirements are still evolving.
- Tradeoff: Fewer relational guarantees and joins; eventual consistency model. Appropriate for read-heavy, document-centric domains like catalogs.

**Djongo**

- Bridges Django ORM with MongoDB for familiar query patterns and admin integration.
- Tradeoff: Not every ORM feature maps cleanly to MongoDB; some queries may be less optimal than native aggregation pipelines.

**Service layer instead of fat views**

- Keeps views under 10 lines; logic is unit-testable without HTTP.
- Tradeoff: Extra indirection for trivial use cases; justified as the domain grows.

---

## 7. Scalability and Future Improvements

- **Caching**: Add Redis for `get_available_artworks` and other read-heavy endpoints.
- **Async**: Migrate I/O-bound paths to async views and async DB drivers where beneficial.
- **API-first**: Extract a REST or GraphQL API; keep templates as one consumer.
- **Read replicas**: Route read traffic to replicas if write load increases.
- **Background jobs**: Offload image processing and notifications to Celery or similar.

---

## 8. What This Project Demonstrates

- **Clean architecture**: Layered design with explicit boundaries between HTTP, business logic, and data access.
- **SOLID principles**: Applied concretely in service and view structure.
- **Environment parity**: Containerized setup for reproducible development and deployment.
- **Deliberate technology choices**: Documented tradeoffs for database and ORM selection.
- **Production-minded practices**: Structure that supports testing, extension, and future scaling without major rewrites.

---

## Disclaimer

This project is provided "as is", without warranty of any kind. The author is not responsible for any damages, data loss, legal issues, or compliance violations resulting from the use or deployment of this software.

Users are solely responsible for ensuring compliance with all applicable laws, including but not limited to data protection, e-commerce regulations, and payment processing requirements.

---

## Artist Storefront Checklist

Before deploying your store:

- [ ] Configure Stripe keys — see [Stripe Setup](documentation/stripe-setup.md)
- [ ] Decide your protection workflow (Glaze / WebGlaze / Nightshade) — see [Protecting Artwork](documentation/ART_PROTECTION.md)
- [ ] Keep original masters private; never upload them to the web
- [ ] Upload web-optimized protected images only
- [ ] Configure storage (Supabase / S3) and CDN if needed for production
- [ ] Review privacy policy and terms if you deploy publicly

---

## Template Usage Notice

IcedMangoes is a free backend storefront template. The repository author does not operate, host, or manage any live deployments built from this code.

If you deploy this template publicly, you are responsible for:

- Data protection compliance (e.g., GDPR, CCPA, etc.)
- Payment processor compliance (e.g., Stripe requirements)
- Hosting security and configuration
- Providing your own Privacy Policy and Terms of Service

Optional legal document templates may be included for convenience, but they must be reviewed and customized for your jurisdiction.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and deploy this template for personal or commercial projects.
