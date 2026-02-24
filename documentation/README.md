# IcedMangoes Documentation Wiki

Central documentation hub for the IcedMangoes artist storefront project. Use this page as your starting point.

---

## Table of Contents

### Getting Started

| Document | Description |
|----------|-------------|
| [Installation & Deployment](installation-and-deployment.md) | **Start here** — Installation checklist, tools verification, step-by-step setup, deployment |
| [Frontend: Vercel + Supabase](frontend-vercel-supabase.md) | **Artist-friendly** — Next.js storefront, deploy to Vercel without Docker |
| [Getting Started](getting-started.md) | Quick start, environment variables reference (Django) |
| [Deploy to Render](deploy-render.md) | Render deployment (Django), Supabase Storage for media (required for production) |

### Project Usage

| Document | Description |
|----------|-------------|
| [Using the Storefront](using-the-storefront.md) | How to browse artworks, switch themes, add artworks via the modal |
| [Admin Guide](admin-guide.md) | Django admin: artists, artworks, user management |
| [Business Page](business-page.md) | Fulfillment configuration, provider integrations, webhooks (admin only) |
| [Stripe Setup](stripe-setup.md) | Connect Stripe for checkout (Django & Next.js), webhooks, test keys |
| [Protecting Artwork from AI Training & Style Mimicry](ART_PROTECTION.md) | Glaze, WebGlaze, Nightshade — workflow to protect art before uploading |

### Tech Stack & Tools

| Document | Description |
|----------|-------------|
| [Django](tech-django.md) | Framework overview, models, views, services, migrations |
| [Tailwind CSS](tech-tailwind.md) | CSS build, theme variables, component styling |
| [GraphQL](tech-graphql.md) | Graphene-Django, schema, queries, mutations |
| [Prisma](tech-prisma.md) | Prisma Client Python, schema, optional type-safe queries |

### API & Processes

| Document | Description |
|----------|-------------|
| [API Reference](api-reference.md) | Endpoints, GraphQL schema, request/response examples |
| [Add Artwork Flow](api-add-artwork.md) | Step-by-step add artwork process, form fields, validation |

### Architecture

| Document | Description |
|----------|-------------|
| [Architecture Overview](architecture.md) | Service layer, SOLID principles, project structure |
| [Architecture Remediation Plan](architecture-remediation-plan.md) | Dual-stack consolidation plan, system design problems, phased remediation |
| [Atomic Design](ATOMIC_DESIGN.md) | Component hierarchy: atoms, molecules, organisms; folder structure for Django and Next.js |

### Legal Templates

| Document | Description |
|----------|-------------|
| [Legal Templates Overview](legal-templates-overview.md) | Privacy Policy, Terms, and Cookie Policy templates – **templates only; customize for your business and jurisdiction** |
| [Privacy Policy Template](legal-templates/privacy-policy-template.md) | Template for privacy policy |
| [Terms Template](legal-templates/terms-template.md) | Template for terms of service |
| [Cookie Policy Template](legal-templates/cookie-policy-template.md) | Template for cookie policy |

---

## Quick Links

**Django backend**
- **App**: http://localhost:8000
- **Blog**: http://localhost:8000/blog/
- **Profile**: http://localhost:8000/profile/
- **Business (admin)**: http://localhost:8000/business/
- **GraphQL (GraphiQL)**: http://localhost:8000/graphql/
- **Admin**: http://localhost:8000/admin/

**Next.js frontend** (`cd frontend && npm run dev`)
- **App**: http://localhost:3000
- **Shop**: http://localhost:3000/shop
- **Cart**: http://localhost:3000/cart
- **Business**: http://localhost:3000/business

**Main README**: [../README.md](../README.md)
