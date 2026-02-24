# Architecture Overview

[← Back to Wiki](README.md)

## Service Layer Pattern

```
HTTP Request → View → Service → Model → Database
```

Views handle HTTP only. Domain logic lives in `store/services.py`.

## SOLID in Practice

- **Single Responsibility**: `services.py` owns logic; `views.py` renders.
- **Open/Closed**: `ArtworkService` can be extended via subclasses.
- **Liskov Substitution**: Alternative services can replace `ArtworkService` where injected.
- **Interface Segregation**: `ArtworkServiceProtocol` defines a narrow interface.
- **Dependency Inversion**: Views depend on the protocol; concrete implementation is injectable.

## Component Structure

### Django backend (`store/templates/store/`)

```
store/templates/store/
├── base.html
├── index.html
└── components/
    ├── add_artwork_button.html
    ├── add_artwork_modal.html      # 3-step: images (min 1), details, review
    ├── artwork_card.html           # Click opens detail modal
    ├── artwork_detail_modal.html   # Image carousel, product options, add to cart
    ├── cart_button.html
    ├── pinterest_board.html
    └── theme_switcher.html
```

### Next.js frontend (`frontend/src/`)

```
frontend/src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Home
│   ├── shop/page.tsx         # Paginated + search
│   ├── product/[id]/page.tsx
│   └── business/page.tsx     # Admin
├── components/
│   ├── Navbar.tsx
│   ├── ProductCard.tsx
│   └── ShopSearch.tsx
└── lib/supabase/
    ├── client.ts
    ├── server.ts
    └── get-client.ts
```

## Data Flow

### Django backend
- **Read**: `ArtworkService.get_available_artworks()` → `filter(available=True)`, `select_related("artist")`, `prefetch_related("artworkproduct_set", "artworkimage_set")`
- **Write**: `ArtworkService.create_artwork()` → `Artist.get_or_create()`, `Artwork.objects.create()`, `ArtworkProduct`, `ArtworkImage`
- **GraphQL**: Resolvers use Django ORM; schema in `config/schema.py`

### Next.js frontend
- **Read**: `getSupabaseClient()` → Supabase `from("products").select()`; RLS allows public read for `active = true`
- **Write**: Phase 2+ (Stripe, admin product CRUD)
