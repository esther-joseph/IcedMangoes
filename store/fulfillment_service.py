"""Fulfillment settings and provider credential resolution service."""
import os
from typing import Any

from django.conf import settings

from .models import FulfillmentSettings, ProviderSecret

# Map provider name -> settings attr (falls back to env)
PROVIDER_SETTINGS_ATTRS = {
    "shippo": "SHIPPO_API_TOKEN",
    "easypost": "EASYPOST_API_KEY",
    "printful": "PRINTFUL_API_KEY",
    "printify": "PRINTIFY_API_KEY",
    "gelato": "GELATO_API_KEY",
}


def get_effective_settings() -> dict[str, Any]:
    """
    Single source of truth for fulfillment configuration.
    DB override > env fallback.
    """
    fs = FulfillmentSettings.get()
    return {
        "fulfillment_mode": fs.fulfillment_mode,
        "manual_provider": fs.manual_provider,
        "pod_provider": fs.pod_provider,
        "use_env_secrets": fs.use_env_secrets,
        "updated_at": fs.updated_at,
    }


def set_settings(
    fulfillment_mode: str,
    manual_provider: str,
    pod_provider: str,
    use_env_secrets: bool = True,
) -> FulfillmentSettings:
    """Persist fulfillment settings (admin-only)."""
    fs = FulfillmentSettings.get()
    fs.fulfillment_mode = fulfillment_mode
    fs.manual_provider = manual_provider
    fs.pod_provider = pod_provider
    fs.use_env_secrets = use_env_secrets
    fs.save()
    return fs


def get_provider_credentials(provider_name: str) -> str:
    """
    Resolve API key for a provider.
    If use_env_secrets: read from env/settings.
    Else: read from ProviderSecret (local dev).
    """
    fs = FulfillmentSettings.get()
    if fs.use_env_secrets:
        attr = PROVIDER_SETTINGS_ATTRS.get(provider_name)
        if attr:
            val = getattr(settings, attr, None) or os.environ.get(attr, "")
            return (val or "").strip()
        return (os.environ.get(f"{provider_name.upper()}_API_KEY", "") or "").strip()
    try:
        secret = ProviderSecret.objects.get(provider_name=provider_name)
        return (secret.api_key or "").strip()
    except ProviderSecret.DoesNotExist:
        return ""


def save_provider_key(provider_name: str, api_key: str) -> None:
    """Store provider key in DB (only when use_env_secrets=False)."""
    ProviderSecret.objects.update_or_create(
        provider_name=provider_name,
        defaults={"api_key": api_key},
    )


def get_provider_status(provider_name: str) -> str:
    """
    Return status: 'configured', 'not_configured', or 'test_failed'.
    'verified' can be set after a successful test (we don't persist that for now).
    """
    key = get_provider_credentials(provider_name)
    if not key:
        return "not_configured"
    return "configured"


def is_env_configured(provider_name: str) -> bool:
    """Check if env var exists for provider (without revealing value)."""
    attr = PROVIDER_SETTINGS_ATTRS.get(provider_name)
    if attr:
        val = getattr(settings, attr, None) or os.environ.get(attr, "")
        return bool(str(val).strip())
    return bool(os.environ.get(f"{provider_name.upper()}_API_KEY", "").strip())
