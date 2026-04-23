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


class ArtworkImage(models.Model):
    """Extra image for an artwork (for carousel, multiple views)."""

    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="artworks/")
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.artwork.title} — image {self.order}"


class ArtworkProduct(models.Model):
    """Product form option for an artwork (e.g. Print 8x10, Canvas 16x20) with its price."""

    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider_variant_ids = models.JSONField(
        default=dict,
        blank=True,
        help_text='Map of provider → variant ID: {"printful": "123", "printify": "abc", "gelato": "xyz"}',
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.artwork.title} — {self.name} (${self.price})"


class Order(models.Model):
    """Order placed by a user."""

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PENDING_PAYMENT", "Pending payment"),
        ("PAID", "Paid"),
        ("FULFILLMENT_PENDING", "Fulfillment pending"),
        ("IN_PRODUCTION", "In production"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
        ("REFUNDED", "Refunded"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    stripe_session_id = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, default="card")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="PENDING_PAYMENT")
    fulfilling_provider = models.CharField(max_length=50, blank=True)
    tracking_number = models.CharField(max_length=255, blank=True)
    # Shipping address — populated from Stripe session on checkout.session.completed
    shipping_name = models.CharField(max_length=255, blank=True)
    shipping_email = models.EmailField(blank=True)
    shipping_address_line1 = models.CharField(max_length=255, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    """Singleton settings for theme, Stripe, and store configuration (admin configurable)."""

    default_theme = models.CharField(
        max_length=50,
        default="cute-beige",
        help_text="Default theme: cute-beige, lavender, baby-blue, peach-pink, slate-gray, mint-green, coral-red",
    )
    site_name = models.CharField(max_length=100, default="Artist Store")
    tagline = models.CharField(max_length=200, default="Discover and collect artworks")
    stripe_publishable_key = models.CharField(max_length=255, blank=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True)
    substack_publication_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Substack publication URL (e.g. https://yourname.substack.com) for blog feed",
    )
    # Seller address — used as "from" address for Shippo / EasyPost shipments
    seller_name = models.CharField(max_length=255, blank=True)
    seller_address_line1 = models.CharField(max_length=255, blank=True)
    seller_city = models.CharField(max_length=100, blank=True)
    seller_state = models.CharField(max_length=100, blank=True)
    seller_postal_code = models.CharField(max_length=20, blank=True)
    seller_country = models.CharField(max_length=2, blank=True, default="US")
    # Printify requires a shop ID (found in your Printify dashboard)
    printify_shop_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Site settings"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FulfillmentSettings(models.Model):
    """
    Singleton admin settings for fulfillment mode and provider selection.
    No secrets stored by default; use_env_secrets=True prefers environment variables.
    """

    fulfillment_mode = models.CharField(
        max_length=20,
        choices=[("MANUAL", "Self-Fulfillment"), ("POD", "Print-on-Demand")],
        default="MANUAL",
    )
    manual_provider = models.CharField(
        max_length=20,
        choices=[("shippo", "Shippo"), ("easypost", "EasyPost"), ("none", "None")],
        default="none",
    )
    pod_provider = models.CharField(
        max_length=20,
        choices=[
            ("printful", "Printful"),
            ("printify", "Printify"),
            ("gelato", "Gelato"),
            ("none", "None"),
        ],
        default="none",
    )
    use_env_secrets = models.BooleanField(
        default=True,
        help_text="If True, read API keys from env. If False, use DB-stored keys (local dev only).",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Fulfillment settings"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ProviderSecret(models.Model):
    """
    Stores provider API keys for local demos when use_env_secrets=False.

    WARNING: Keys are stored in plaintext. Do NOT use in production with real
    API keys. For production, set use_env_secrets=True and supply keys via
    environment variables, or encrypt this field using django-cryptography
    (EncryptedCharField) and run a migration before storing real secrets.
    """

    provider_name = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Provider secret"
        verbose_name_plural = "Provider secrets"


class WebhookEvent(models.Model):
    """Tracks processed Stripe events to guarantee idempotent webhook handling.

    The unique constraint on stripe_event_id means a concurrent duplicate delivery
    will raise IntegrityError on the second insert, which the handler catches and
    ignores rather than creating a duplicate order.
    """

    stripe_event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100)
    processed_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-processed_at"]

    def __str__(self) -> str:
        return f"{self.event_type} — {self.stripe_event_id}"


class Cart(models.Model):
    """Persistent cart for authenticated users. Anonymous users use the session cart."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart for {self.user}"


class CartItem(models.Model):
    """Line item in a persistent cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ArtworkProduct, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "artwork", "product")

    def __str__(self) -> str:
        return f"{self.artwork.title} x {self.quantity}"
