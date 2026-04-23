"""Order lifecycle and fulfillment service."""
import base64
import json
import logging
import urllib.error
import urllib.request

from .fulfillment_service import get_effective_settings, get_provider_credentials
from .models import Order

logger = logging.getLogger(__name__)


def mark_paid(order: Order, stripe_session_id: str) -> Order:
    """Mark order as paid after Stripe checkout.session.completed."""
    order.status = "PAID"
    order.stripe_session_id = stripe_session_id
    order.save(update_fields=["status", "stripe_session_id", "updated_at"])
    return order


def request_fulfillment(order: Order) -> dict:
    """
    Request fulfillment using admin-selected provider.
    Returns {"success": bool, "message": str}.
    """
    cfg = get_effective_settings()
    mode = cfg["fulfillment_mode"]
    provider = cfg["manual_provider"] if mode == "MANUAL" else cfg["pod_provider"]

    order.fulfilling_provider = provider
    order.status = "FULFILLMENT_PENDING"
    order.save(update_fields=["fulfilling_provider", "status", "updated_at"])

    if provider == "none":
        return {"success": True, "message": "Manual fulfillment; no provider integration"}

    key = get_provider_credentials(provider)
    if not key:
        return {"success": False, "message": f"API key not configured for {provider}"}

    dispatch = {
        "shippo": _call_shippo,
        "easypost": _call_easypost,
        "printful": _call_printful,
        "printify": _call_printify,
        "gelato": _call_gelato,
    }
    handler = dispatch.get(provider)
    if not handler:
        return {"success": False, "message": f"Unknown provider: {provider}"}
    return handler(order, key)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _post_json(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={**headers, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def _shipping_complete(order: Order) -> bool:
    return bool(order.shipping_address_line1 and order.shipping_city and order.shipping_country)


def _handle_http_error(exc: urllib.error.HTTPError, provider: str, order_id) -> dict:
    body = exc.read().decode(errors="replace")
    logger.error("%s HTTP %s for order %s: %s", provider, exc.code, order_id, body)
    return {"success": False, "message": f"{provider} error {exc.code}: {body[:300]}"}


def _handle_unexpected(exc: Exception, provider: str, order_id) -> dict:
    logger.exception("%s unexpected error for order %s", provider, order_id)
    return {"success": False, "message": f"{provider} error: {exc}"}


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

def _call_shippo(order: Order, api_key: str) -> dict:
    from .models import SiteSettings
    site = SiteSettings.get()

    if not _shipping_complete(order):
        return {"success": False, "message": "Order is missing shipping address; configure Stripe to collect it"}

    payload = {
        "address_from": {
            "name": site.seller_name or "Artist",
            "street1": site.seller_address_line1,
            "city": site.seller_city,
            "state": site.seller_state,
            "zip": site.seller_postal_code,
            "country": site.seller_country or "US",
        },
        "address_to": {
            "name": order.shipping_name,
            "email": order.shipping_email,
            "street1": order.shipping_address_line1,
            "street2": order.shipping_address_line2,
            "city": order.shipping_city,
            "state": order.shipping_state,
            "zip": order.shipping_postal_code,
            "country": order.shipping_country or "US",
        },
        "parcels": [
            {"length": "10", "width": "8", "height": "2",
             "distance_unit": "in", "weight": "1", "mass_unit": "lb"}
        ],
        "async": False,
    }
    try:
        resp = _post_json(
            "https://api.goshippo.com/shipments/",
            payload,
            {"Authorization": f"ShippoToken {api_key}"},
        )
        tracking = resp.get("tracking_number") or resp.get("object_id", "")
        if tracking:
            order.tracking_number = tracking
        order.status = "IN_PRODUCTION"
        order.save(update_fields=["tracking_number", "status", "updated_at"])
        return {"success": True, "message": f"Shippo shipment created (id: {resp.get('object_id', '')})"}
    except urllib.error.HTTPError as exc:
        return _handle_http_error(exc, "Shippo", order.id)
    except Exception as exc:
        return _handle_unexpected(exc, "Shippo", order.id)


def _call_easypost(order: Order, api_key: str) -> dict:
    from .models import SiteSettings
    site = SiteSettings.get()

    if not _shipping_complete(order):
        return {"success": False, "message": "Order is missing shipping address; configure Stripe to collect it"}

    auth = base64.b64encode(f"{api_key}:".encode()).decode()
    payload = {
        "shipment": {
            "from_address": {
                "name": site.seller_name or "Artist",
                "street1": site.seller_address_line1,
                "city": site.seller_city,
                "state": site.seller_state,
                "zip": site.seller_postal_code,
                "country": site.seller_country or "US",
            },
            "to_address": {
                "name": order.shipping_name,
                "email": order.shipping_email,
                "street1": order.shipping_address_line1,
                "street2": order.shipping_address_line2,
                "city": order.shipping_city,
                "state": order.shipping_state,
                "zip": order.shipping_postal_code,
                "country": order.shipping_country or "US",
            },
            "parcel": {
                "length": 10, "width": 8, "height": 2,
                "distance_unit": "in", "weight": 1, "mass_unit": "lb",
            },
        }
    }
    try:
        resp = _post_json(
            "https://api.easypost.com/v2/shipments",
            payload,
            {"Authorization": f"Basic {auth}"},
        )
        order.status = "IN_PRODUCTION"
        order.save(update_fields=["status", "updated_at"])
        return {"success": True, "message": f"EasyPost shipment created (id: {resp.get('id', '')})"}
    except urllib.error.HTTPError as exc:
        return _handle_http_error(exc, "EasyPost", order.id)
    except Exception as exc:
        return _handle_unexpected(exc, "EasyPost", order.id)


def _pod_items(order: Order, provider: str) -> tuple[list, str | None]:
    """
    Build provider-specific line items from order items.
    Returns (items_list, error_message_or_None).
    Each ArtworkProduct must have provider_variant_ids[provider] set in the admin.
    """
    from .models import ArtworkProduct
    items = []
    missing = []
    for item in order.orderitem_set.select_related("artwork").all():
        ap = ArtworkProduct.objects.filter(artwork=item.artwork).first()
        variant_id = (ap.provider_variant_ids or {}).get(provider) if ap else None
        if not variant_id:
            missing.append(item.artwork.title)
            continue
        items.append((variant_id, item.quantity, item))
    if missing:
        logger.warning(
            "%s: no variant IDs for artworks %s (order %s)", provider, missing, order.id
        )
    if not items:
        return [], (
            f"No {provider} variant IDs configured for this order's products. "
            "Set them in the admin for each ArtworkProduct → provider_variant_ids."
        )
    return items, None


def _call_printful(order: Order, api_key: str) -> dict:
    if not _shipping_complete(order):
        return {"success": False, "message": "Order is missing shipping address"}

    items, err = _pod_items(order, "printful")
    if err:
        return {"success": False, "message": err}

    payload = {
        "recipient": {
            "name": order.shipping_name,
            "email": order.shipping_email,
            "address1": order.shipping_address_line1,
            "address2": order.shipping_address_line2,
            "city": order.shipping_city,
            "state_code": order.shipping_state,
            "zip": order.shipping_postal_code,
            "country_code": order.shipping_country or "US",
        },
        "items": [
            {"sync_variant_id": int(variant_id), "quantity": qty}
            for variant_id, qty, _ in items
        ],
    }
    try:
        resp = _post_json(
            "https://api.printful.com/orders",
            payload,
            {"Authorization": f"Bearer {api_key}"},
        )
        printful_id = (resp.get("result") or {}).get("id", "")
        order.status = "IN_PRODUCTION"
        order.save(update_fields=["status", "updated_at"])
        return {"success": True, "message": f"Printful order created (id: {printful_id})"}
    except urllib.error.HTTPError as exc:
        return _handle_http_error(exc, "Printful", order.id)
    except Exception as exc:
        return _handle_unexpected(exc, "Printful", order.id)


def _call_printify(order: Order, api_key: str) -> dict:
    from .models import SiteSettings
    shop_id = SiteSettings.get().printify_shop_id
    if not shop_id:
        return {"success": False, "message": "Printify shop_id not set in Site Settings"}
    if not _shipping_complete(order):
        return {"success": False, "message": "Order is missing shipping address"}

    items, err = _pod_items(order, "printify")
    if err:
        return {"success": False, "message": err}

    name_parts = (order.shipping_name or "").split(" ", 1)
    payload = {
        "label": f"Order #{order.id}",
        "line_items": [
            {"product_id": variant_id, "variant_id": variant_id, "quantity": qty}
            for variant_id, qty, _ in items
        ],
        "shipping_method": 1,
        "address_to": {
            "first_name": name_parts[0],
            "last_name": name_parts[1] if len(name_parts) > 1 else "",
            "email": order.shipping_email,
            "address1": order.shipping_address_line1,
            "address2": order.shipping_address_line2,
            "city": order.shipping_city,
            "region": order.shipping_state,
            "zip": order.shipping_postal_code,
            "country": order.shipping_country or "US",
        },
    }
    try:
        resp = _post_json(
            f"https://api.printify.com/v1/shops/{shop_id}/orders.json",
            payload,
            {"Authorization": f"Bearer {api_key}"},
        )
        order.status = "IN_PRODUCTION"
        order.save(update_fields=["status", "updated_at"])
        return {"success": True, "message": f"Printify order created (id: {resp.get('id', '')})"}
    except urllib.error.HTTPError as exc:
        return _handle_http_error(exc, "Printify", order.id)
    except Exception as exc:
        return _handle_unexpected(exc, "Printify", order.id)


def _call_gelato(order: Order, api_key: str) -> dict:
    if not _shipping_complete(order):
        return {"success": False, "message": "Order is missing shipping address"}

    items, err = _pod_items(order, "gelato")
    if err:
        return {"success": False, "message": err}

    name_parts = (order.shipping_name or "").split(" ", 1)
    payload = {
        "orderReferenceId": f"order-{order.id}",
        "customerReferenceId": f"customer-{order.user_id or 'anon'}",
        "currency": "USD",
        "items": [
            {
                "itemReferenceId": str(item_obj.id),
                "productUid": variant_id,
                "quantity": qty,
                "files": [],
            }
            for variant_id, qty, item_obj in items
        ],
        "shippingAddress": {
            "firstName": name_parts[0],
            "lastName": name_parts[1] if len(name_parts) > 1 else "",
            "addressLine1": order.shipping_address_line1,
            "addressLine2": order.shipping_address_line2,
            "city": order.shipping_city,
            "postCode": order.shipping_postal_code,
            "country": order.shipping_country or "US",
            "email": order.shipping_email,
        },
    }
    try:
        resp = _post_json(
            "https://order.gelatoapis.com/v4/orders",
            payload,
            {"X-API-KEY": api_key},
        )
        order.status = "IN_PRODUCTION"
        order.save(update_fields=["status", "updated_at"])
        return {"success": True, "message": f"Gelato order created (id: {resp.get('id', '')})"}
    except urllib.error.HTTPError as exc:
        return _handle_http_error(exc, "Gelato", order.id)
    except Exception as exc:
        return _handle_unexpected(exc, "Gelato", order.id)
