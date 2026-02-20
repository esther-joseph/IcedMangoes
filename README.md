# IcedMangoes

A backend architecture showcase demonstrating clean architecture, service-layer design, and production-oriented practices.

**Documentation**: [documentation/README.md](documentation/README.md) – wiki with setup, tech stack, and API guides. Built with Django and MongoDB to model a storefront domain suitable for iterative schema evolution.

---

## 1. Project Overview

IcedMangoes implements a storefront API and presentation layer for an artist marketplace. The focus is on maintainable backend design: clear separation of concerns, testable business logic, and reproducible deployment. Views remain thin; domain logic lives in dedicated services.

---

## 2. Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 3.2–4.1 |
| Database | MongoDB (via Djongo) or SQLite (optional, `USE_SQLITE=1`) |
| API | GraphQL (Graphene-Django) |
| ORM (optional) | Prisma Client Python (SQLite) |
| Media | Pillow |
| Runtime | Python 3.11 |
| Frontend | Tailwind CSS, PostCSS, CSS custom properties (theme switching) |
| Build | Node.js, npm (for CSS) |
| Orchestration | Docker Compose |

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
- GraphQL (GraphiQL): http://localhost:8000/graphql/
- Mongo Express: http://localhost:8081 (Docker only)

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

This project is provided as-is. Users are responsible for complying with all applicable laws including data protection and payment processing regulations.
