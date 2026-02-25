"""Service layer for store domain logic."""
from decimal import Decimal
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
        """Return available artworks with artist and product options pre-fetched."""
        return (
            Artwork.objects.filter(available=True)
            .select_related("artist")
            .prefetch_related("artworkproduct_set", "artworkimage_set")
            .order_by("-id")
        )

    @staticmethod
    def create_artwork(artist_name: str, title: str, description: str, price, images, tags: str = "", product_options: str = "") -> Artwork:
        """Create an artwork and its artist. images: list of uploaded files (min 1); first is main image."""
        from .models import Artist, ArtworkImage, ArtworkProduct

        if not images:
            raise ValueError("At least one image is required")
        first_image = images[0]
        artist, _ = Artist.objects.get_or_create(name=artist_name.strip())
        artwork = Artwork.objects.create(
            artist=artist,
            title=title.strip(),
            description=description.strip(),
            price=price,
            image=first_image,
            tags=tags.strip() if tags else "",
        )
        for order, img in enumerate(images[1:], start=1):
            ArtworkImage.objects.create(artwork=artwork, image=img, order=order)
        for line in (product_options or "").strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",", 1)]
            if len(parts) >= 2 and parts[0]:
                try:
                    pprice = Decimal(parts[1].replace("$", "").strip())
                    ArtworkProduct.objects.create(artwork=artwork, name=parts[0][:100], price=pprice)
                except (ValueError, Exception):
                    pass
        return artwork
