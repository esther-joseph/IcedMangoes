# Migration: webhook idempotency, cart persistence, shipping address, seller address,
# provider variant IDs, and Printify shop ID.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0009_substack_publication_url"),
    ]

    operations = [
        # ArtworkProduct: provider variant IDs for POD fulfillment
        migrations.AddField(
            model_name="artworkproduct",
            name="provider_variant_ids",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text='Map of provider to variant ID: {"printful": "123", "printify": "abc", "gelato": "xyz"}',
            ),
        ),
        # Order: shipping address fields
        migrations.AddField(
            model_name="order",
            name="shipping_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_email",
            field=models.EmailField(blank=True),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_address_line1",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_address_line2",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_city",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_state",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_postal_code",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_country",
            field=models.CharField(blank=True, max_length=2),
        ),
        # SiteSettings: seller address for Shippo/EasyPost + Printify shop ID
        migrations.AddField(
            model_name="sitesettings",
            name="seller_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="seller_address_line1",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="seller_city",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="seller_state",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="seller_postal_code",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="seller_country",
            field=models.CharField(blank=True, default="US", max_length=2),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="printify_shop_id",
            field=models.CharField(blank=True, max_length=100),
        ),
        # WebhookEvent: idempotency table for Stripe events
        migrations.CreateModel(
            name="WebhookEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("stripe_event_id", models.CharField(max_length=255, unique=True)),
                ("event_type", models.CharField(max_length=100)),
                ("processed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="store.order",
                    ),
                ),
            ],
            options={"ordering": ["-processed_at"]},
        ),
        # Cart: persistent cart for authenticated users
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        # CartItem: line items in a persistent cart
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="store.cart",
                    ),
                ),
                (
                    "artwork",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.artwork",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="store.artworkproduct",
                    ),
                ),
            ],
            options={"unique_together": {("cart", "artwork", "product")}},
        ),
    ]
