"""Order lifecycle and fulfillment service."""
from .fulfillment_service import get_effective_settings, get_provider_credentials
from .models import Order


def mark_paid(order: Order, stripe_session_id: str) -> Order:
    """Mark order as paid after Stripe checkout.session.completed."""
    order.status = "PAID"
    order.stripe_session_id = stripe_session_id
    order.save(update_fields=["status", "stripe_session_id", "updated_at"])
    return order


def request_fulfillment(order: Order) -> dict:
    """
    Request fulfillment using admin-selected provider.
    Returns {success: bool, message: str}.
    """
    settings = get_effective_settings()
    mode = settings["fulfillment_mode"]
    if mode == "MANUAL":
        provider = settings["manual_provider"]
    else:
        provider = settings["pod_provider"]

    order.fulfilling_provider = provider
    order.status = "FULFILLMENT_PENDING"
    order.save(update_fields=["fulfilling_provider", "status", "updated_at"])

    if provider == "none":
        return {"success": True, "message": "Manual fulfillment; no provider integration"}

    key = get_provider_credentials(provider)
    if not key:
        return {"success": False, "message": f"API key not configured for {provider}"}

    # Scaffold: real provider calls would go here
    return {"success": True, "message": f"Fulfillment requested via {provider} (scaffold)"}
