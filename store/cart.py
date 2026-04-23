"""Cart utilities — session-based for anonymous users, DB-backed for authenticated users."""
import logging
from decimal import Decimal

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Artwork, ArtworkProduct, Cart, CartItem

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API — callers don't need to know which backend is in use
# ---------------------------------------------------------------------------

def get_cart(request) -> dict:
    """Return cart dict. Keys: 'aid:pid' (pid=0 for base price). Values: quantity."""
    if request.user.is_authenticated:
        return _db_cart_to_dict(request.user)
    return _clean_session_cart(request)


def set_cart(request, cart: dict) -> None:
    """Persist full cart. Replaces existing contents."""
    if request.user.is_authenticated:
        _save_db_cart(request.user, cart)
    else:
        request.session["cart"] = {str(k): v for k, v in cart.items() if v > 0}
        request.session.modified = True


def add_to_cart(request, artwork_id, product_id=None, quantity: int = 1) -> None:
    """Add artwork to cart. product_id=None uses artwork base price."""
    pid = product_id if product_id is not None else 0
    key = _cart_key(artwork_id, pid)
    if request.user.is_authenticated:
        db_cart, _ = Cart.objects.get_or_create(user=request.user)
        prod_fk = product_id if pid != 0 else None
        item, created = CartItem.objects.get_or_create(
            cart=db_cart,
            artwork_id=artwork_id,
            product_id=prod_fk,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
    else:
        cart = _clean_session_cart(request)
        cart[key] = cart.get(key, 0) + quantity
        request.session["cart"] = cart
        request.session.modified = True


def remove_from_cart(request, artwork_id, product_id=None) -> None:
    """Remove a cart line."""
    if request.user.is_authenticated:
        db_cart = _get_db_cart(request.user)
        if db_cart is None:
            return
        prod_fk = product_id if product_id not in (None, 0) else None
        CartItem.objects.filter(
            cart=db_cart, artwork_id=artwork_id, product_id=prod_fk
        ).delete()
        if product_id is None:
            CartItem.objects.filter(
                cart=db_cart, artwork_id=artwork_id, product_id=None
            ).delete()
    else:
        cart = _clean_session_cart(request)
        if product_id is not None:
            cart.pop(_cart_key(artwork_id, product_id), None)
        else:
            cart.pop(str(artwork_id), None)
            cart.pop(_cart_key(artwork_id, 0), None)
        request.session["cart"] = cart
        request.session.modified = True


def clear_cart(request) -> None:
    """Clear all items from cart."""
    if request.user.is_authenticated:
        db_cart = _get_db_cart(request.user)
        if db_cart:
            db_cart.items.all().delete()
    else:
        request.session["cart"] = {}
        request.session.modified = True


def get_cart_items(request) -> list[dict]:
    """Return list of {artwork, quantity, unit_price, product_name, cart_key} dicts."""
    cart = get_cart(request)
    if not cart:
        return []
    return _resolve_cart_items(cart)


def get_cart_total(request) -> Decimal:
    """Return total price of cart."""
    items = get_cart_items(request)
    return sum((item["unit_price"] * item["quantity"] for item in items), Decimal("0"))


# ---------------------------------------------------------------------------
# Login signal — merge session cart into DB cart on authentication
# ---------------------------------------------------------------------------

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs) -> None:
    """Merge anonymous session cart into the user's persistent cart on login."""
    session_cart = request.session.get("cart", {})
    if not session_cart:
        return
    db_cart, _ = Cart.objects.get_or_create(user=user)
    for key, qty in session_cart.items():
        if qty <= 0:
            continue
        parts = key.split(":")
        aid_str = parts[0]
        pid_str = parts[1] if len(parts) > 1 else "0"
        if not aid_str.isdigit():
            continue
        aid = int(aid_str)
        prod_fk = int(pid_str) if pid_str.isdigit() and pid_str != "0" else None
        try:
            item, created = CartItem.objects.get_or_create(
                cart=db_cart,
                artwork_id=aid,
                product_id=prod_fk,
                defaults={"quantity": qty},
            )
            if not created:
                item.quantity += qty
                item.save(update_fields=["quantity"])
        except Exception:
            logger.exception("Failed to merge cart item %s on login for user %s", key, user.id)
    request.session["cart"] = {}
    request.session.modified = True


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _cart_key(artwork_id, product_id=0) -> str:
    return f"{artwork_id}:{product_id}"


def _clean_session_cart(request) -> dict:
    raw = request.session.get("cart", {})
    return {str(k): int(v) for k, v in raw.items() if isinstance(v, int) and v > 0}


def _get_db_cart(user) -> Cart | None:
    try:
        return Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return None


def _db_cart_to_dict(user) -> dict:
    db_cart = _get_db_cart(user)
    if db_cart is None:
        return {}
    result = {}
    for item in db_cart.items.all():
        pid = item.product_id or 0
        key = _cart_key(item.artwork_id, pid)
        result[key] = item.quantity
    return result


def _save_db_cart(user, cart: dict) -> None:
    db_cart, _ = Cart.objects.get_or_create(user=user)
    db_cart.items.all().delete()
    for key, qty in cart.items():
        if qty <= 0:
            continue
        parts = key.split(":")
        if not parts[0].isdigit():
            continue
        aid = int(parts[0])
        pid_str = parts[1] if len(parts) > 1 else "0"
        prod_fk = int(pid_str) if pid_str.isdigit() and pid_str != "0" else None
        try:
            CartItem.objects.create(cart=db_cart, artwork_id=aid, product_id=prod_fk, quantity=qty)
        except Exception:
            logger.exception("Failed to save cart item %s for user %s", key, user.id)


def _resolve_cart_items(cart: dict) -> list[dict]:
    result = []
    for key, qty in cart.items():
        parts = key.split(":")
        aid = int(parts[0]) if parts[0].isdigit() else None
        pid = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        if aid is None:
            continue
        try:
            artwork = Artwork.objects.select_related("artist").get(pk=aid, available=True)
        except Artwork.DoesNotExist:
            continue
        if pid == 0:
            unit_price = artwork.price
            product_name = None
        else:
            try:
                ap = ArtworkProduct.objects.get(pk=pid, artwork=artwork)
                unit_price = ap.price
                product_name = ap.name
            except ArtworkProduct.DoesNotExist:
                unit_price = artwork.price
                product_name = None
        result.append({
            "artwork": artwork,
            "quantity": qty,
            "unit_price": unit_price,
            "product_name": product_name,
            "cart_key": key,
            "product_id": pid,
        })
    return result
