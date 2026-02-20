"""Service layer for store domain logic."""
from typing import Protocol

from django.db.models import QuerySet

from .models import Artwork


class ArtworkServiceProtocol(Protocol):
    """Protocol for artwork retrieval service (dependency inversion)."""

    def get_available_artworks(self) -> QuerySet[Artwork]:
        """Return available artworks for display."""
        ...


class ArtworkService:
    """Service for artwork-related operations."""

    @staticmethod
    def get_available_artworks() -> QuerySet[Artwork]:
        """Return available artworks with artist pre-fetched to avoid N+1 queries."""
        return (
            Artwork.objects.filter(available=True)
            .select_related("artist")
            .order_by("-id")
        )

    @staticmethod
    def create_artwork(artist_name: str, title: str, description: str, price, image, tags: str = "") -> Artwork:
        """Create an artwork and its artist if needed."""
        from .models import Artist

        artist, _ = Artist.objects.get_or_create(name=artist_name.strip())
        return Artwork.objects.create(
            artist=artist,
            title=title.strip(),
            description=description.strip(),
            price=price,
            image=image,
            tags=tags.strip() if tags else "",
        )
