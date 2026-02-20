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

```
store/templates/store/
├── base.html
├── index.html
└── components/
    ├── add_artwork_button.html
    ├── add_artwork_modal.html
    ├── artwork_card.html
    ├── pinterest_board.html
    └── theme_switcher.html
```

## Data Flow

- **Read**: `ArtworkService.get_available_artworks()` → `filter(available=True)`, `select_related("artist")`
- **Write**: `ArtworkService.create_artwork()` → `Artist.get_or_create()`, `Artwork.objects.create()`
- **GraphQL**: Resolvers use Django ORM; schema in `config/schema.py`
