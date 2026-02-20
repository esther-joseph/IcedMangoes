# Generated migration for FulfillmentSettings and ProviderSecret

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_add_stripe_to_site_settings"),
    ]

    operations = [
        migrations.CreateModel(
            name="FulfillmentSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "fulfillment_mode",
                    models.CharField(
                        choices=[("MANUAL", "Self-Fulfillment"), ("POD", "Print-on-Demand")],
                        default="MANUAL",
                        max_length=20,
                    ),
                ),
                (
                    "manual_provider",
                    models.CharField(
                        choices=[("shippo", "Shippo"), ("easypost", "EasyPost"), ("none", "None")],
                        default="none",
                        max_length=20,
                    ),
                ),
                (
                    "pod_provider",
                    models.CharField(
                        choices=[("printful", "Printful"), ("printify", "Printify"), ("gelato", "Gelato"), ("none", "None")],
                        default="none",
                        max_length=20,
                    ),
                ),
                (
                    "use_env_secrets",
                    models.BooleanField(
                        default=True,
                        help_text="If True, read API keys from env. If False, use DB-stored keys (local dev only).",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name_plural": "Fulfillment settings"},
        ),
        migrations.CreateModel(
            name="ProviderSecret",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider_name", models.CharField(max_length=50, unique=True)),
                ("api_key", models.CharField(blank=True, max_length=512)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Provider secret", "verbose_name_plural": "Provider secrets"},
        ),
    ]
