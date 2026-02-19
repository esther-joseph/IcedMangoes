"""Store app configuration."""
from django.apps import AppConfig


class StoreConfig(AppConfig):
    """Configuration for the store application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "store"
    verbose_name = "Store"
