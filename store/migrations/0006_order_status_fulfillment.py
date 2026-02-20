# Migration for Order status and fulfillment fields

from django.utils import timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_fulfillment_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Draft"),
                    ("PENDING_PAYMENT", "Pending payment"),
                    ("PAID", "Paid"),
                    ("FULFILLMENT_PENDING", "Fulfillment pending"),
                    ("IN_PRODUCTION", "In production"),
                    ("SHIPPED", "Shipped"),
                    ("DELIVERED", "Delivered"),
                    ("CANCELLED", "Cancelled"),
                    ("REFUNDED", "Refunded"),
                ],
                default="PENDING_PAYMENT",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="fulfilling_provider",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="order",
            name="tracking_number",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, default=timezone.now),
            preserve_default=False,
        ),
    ]
