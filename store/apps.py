"""Store app configuration."""
from django.apps import AppConfig


class StoreConfig(AppConfig):
    """Configuration for the store application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "store"
    verbose_name = "Store"

    def ready(self):
        import store.cart  # noqa: F401 — registers user_logged_in signal for cart merge
