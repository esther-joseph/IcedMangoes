"""Stripe webhook handlers for idempotent payment processing."""
import hashlib
import logging

from django.conf import settings
from django.db import IntegrityError, transaction

from .models import Artwork, Order, OrderItem, WebhookEvent

logger = logging.getLogger(__name__)


def get_webhook_secret() -> str:
    """Return Stripe webhook secret from settings (STRIPE_WEBHOOK_SECRET env)."""
    return (getattr(settings, "STRIPE_WEBHOOK_SECRET", "") or "").strip()


def create_idempotency_key(user_id: str | int, cart_signature: str) -> str:
    """Generate deterministic idempotency key for Stripe API calls."""
    payload = f"{user_id}|{cart_signature}"
    return hashlib.sha256(payload.encode()).hexdigest()[:64]


def build_cart_signature(cart_items: list) -> str:
    """Build deterministic signature from cart items for idempotency."""
    if cart_items and isinstance(cart_items[0], dict):
        parts = sorted(
            (item["artwork"].id, item.get("product_id") or 0, item["quantity"])
            for item in cart_items
        )
        return "|".join(f"{a}:{p}:{q}" for a, p, q in parts)
    parts = sorted((a.id, qty) for a, qty in cart_items)
    return "|".join(f"{aid}:{q}" for aid, q in parts)


def handle_checkout_session_completed(session, stripe_event_id: str) -> Order | None:
    """
    Create order from Stripe checkout session. Fully idempotent: uses WebhookEvent
    with a unique constraint on stripe_event_id to guarantee at-most-once processing
    even under concurrent duplicate webhook delivery.
    """
    stripe_session_id = session.get("id")
    if not stripe_session_id:
        logger.warning("checkout.session.completed missing session id")
        return None

    # Attempt to record this event. If another request already inserted it,
    # IntegrityError is raised and we return the existing order without doing any work.
    try:
        with transaction.atomic():
            event_record = WebhookEvent.objects.create(
                stripe_event_id=stripe_event_id,
                event_type="checkout.session.completed",
            )
    except IntegrityError:
        logger.info("Duplicate Stripe event %s — already processed, skipping", stripe_event_id)
        existing = WebhookEvent.objects.filter(stripe_event_id=stripe_event_id).first()
        return existing.order if existing else None

    # Fetch full session with expanded line items
    import stripe

    stripe_key = _get_stripe_key()
    if not stripe_key:
        logger.error("No Stripe key configured for webhook")
        return None
    stripe.api_key = stripe_key
    try:
        full_session = stripe.checkout.Session.retrieve(
            stripe_session_id, expand=["line_items.data.price.product"]
        )
    except Exception as e:
        logger.exception("Failed to retrieve session %s: %s", stripe_session_id, e)
        return None

    line_items_data = full_session.get("line_items") or {}
    if isinstance(line_items_data, dict):
        line_items_data = line_items_data.get("data", [])
    if not isinstance(line_items_data, list):
        line_items_data = []

    amount_total = (full_session.get("amount_total") or 0) / 100
    client_reference_id = full_session.get("client_reference_id") or ""

    user_id = None
    if client_reference_id.startswith("user:"):
        try:
            user_id = int(client_reference_id.replace("user:", ""))
        except ValueError:
            pass

    shipping = _extract_shipping(full_session)

    from .order_service import request_fulfillment

    with transaction.atomic():
        order = Order.objects.create(
            user_id=user_id,
            stripe_session_id=stripe_session_id,
            total=amount_total,
            payment_method="card",
            status="PAID",
            **shipping,
        )
        for line in line_items_data:
            _create_order_item_from_line(order, line)

        # Link the webhook event record to this order
        event_record.order = order
        event_record.save(update_fields=["order"])

    result = request_fulfillment(order)
    if not result.get("success"):
        logger.warning("Fulfillment for order %s: %s", order.id, result.get("message", ""))
    logger.info("Created order %s for Stripe session %s", order.id, stripe_session_id)
    return order


def _extract_shipping(session) -> dict:
    """Extract shipping address from a Stripe session into Order field kwargs."""
    details = session.get("shipping_details") or session.get("shipping") or {}
    address = details.get("address") or {}
    return {
        "shipping_name": details.get("name") or "",
        "shipping_email": session.get("customer_details", {}).get("email") or "",
        "shipping_address_line1": address.get("line1") or "",
        "shipping_address_line2": address.get("line2") or "",
        "shipping_city": address.get("city") or "",
        "shipping_state": address.get("state") or "",
        "shipping_postal_code": address.get("postal_code") or "",
        "shipping_country": (address.get("country") or "")[:2],
    }


def _create_order_item_from_line(order: Order, line: dict) -> OrderItem | None:
    """Create OrderItem from Stripe line item. Uses metadata.artwork_id if present."""
    qty = line.get("quantity", 1)
    amount = (line.get("amount_total") or 0) / 100
    price = (line.get("price", {}) or {}).get("unit_amount")
    unit_price = (price / 100) if price is not None else (amount / qty if qty else 0)

    product = line.get("price", {}).get("product") or line.get("product") or {}
    if isinstance(product, str):
        product = {}
    metadata = product.get("metadata") or {}
    artwork_id = metadata.get("artwork_id")
    if artwork_id:
        try:
            artwork_id = int(artwork_id)
        except (ValueError, TypeError):
            artwork_id = None

    if artwork_id:
        try:
            artwork = Artwork.objects.get(pk=artwork_id)
        except Artwork.DoesNotExist:
            logger.warning("Artwork %s not found for line item", artwork_id)
            return None
    else:
        name = (product.get("name") or "").strip()
        if not name:
            return None
        artwork = Artwork.objects.filter(title=name).first()
        if not artwork:
            logger.warning("No artwork matching '%s' for line item", name)
            return None

    return OrderItem.objects.create(
        order=order, artwork=artwork, quantity=qty, price=unit_price
    )


def _get_stripe_key() -> str:
    from .models import SiteSettings

    site = SiteSettings.get()
    return (
        (site.stripe_secret_key or getattr(settings, "STRIPE_SECRET_KEY", "") or "").strip()
    )
