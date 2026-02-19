"""Store domain models."""
from decimal import Decimal

from djongo import models


class Artist(models.Model):
    """Artist who creates artworks."""

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Artwork(models.Model):
    """Artwork for sale in the store."""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    image = models.ImageField(upload_to="artworks/", blank=True, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title
