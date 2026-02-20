"""Store domain models."""
import os
from decimal import Decimal

from django.conf import settings

if os.environ.get("USE_SQLITE", "").lower() in ("true", "1", "yes"):
    from django.db import models
else:
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
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    """Order placed by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    stripe_session_id = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, default="card")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order #{self.id} - ${self.total}"


class OrderItem(models.Model):
    """Line item in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.artwork.title} x {self.quantity}"


class SiteSettings(models.Model):
    """Singleton settings for theme, Stripe, and creative visuals (admin configurable)."""

    default_theme = models.CharField(
        max_length=50, default="cute-beige",
        help_text="Default theme: cute-beige, lavender, baby-blue, peach-pink, slate-gray, mint-green, coral-red"
    )
    site_name = models.CharField(max_length=100, default="Artist Store")
    tagline = models.CharField(max_length=200, default="Discover and collect artworks")
    stripe_publishable_key = models.CharField(max_length=255, blank=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Site settings"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
