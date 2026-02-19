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
