"""Session-based cart utilities."""
from decimal import Decimal

from .models import Artwork, ArtworkProduct


def get_cart(request):
    """Return cart dict. Keys: 'aid' or 'aid:pid' (pid=0 for base price). Values: quantity."""
    raw = request.session.get("cart", {})
    cart = {}
    for k, v in raw.items():
        if v > 0:
            cart[str(k)] = int(v)
    return cart


def set_cart(request, cart):
    """Save cart to session."""
    request.session["cart"] = {str(k): v for k, v in cart.items() if v > 0}
    request.session.modified = True


def _cart_key(artwork_id, product_id=0):
    return f"{artwork_id}:{product_id}"


def add_to_cart(request, artwork_id, product_id=None, quantity=1):
    """Add artwork to cart. product_id=None uses artwork base price."""
    cart = get_cart(request)
    pid = product_id if product_id is not None else 0
    key = _cart_key(artwork_id, pid)
    cart[key] = cart.get(key, 0) + quantity
    set_cart(request, cart)


def remove_from_cart(request, artwork_id, product_id=None):
    """Remove cart line. product_id=None removes base-price line (artwork_id or artwork_id:0)."""
    cart = get_cart(request)
    if product_id is not None:
        cart.pop(_cart_key(artwork_id, product_id), None)
    else:
        cart.pop(str(artwork_id), None)
        cart.pop(_cart_key(artwork_id, 0), None)
    set_cart(request, cart)


def clear_cart(request):
    """Clear cart."""
    request.session["cart"] = {}
    request.session.modified = True


def get_cart_items(request):
    """Return list of {artwork, quantity, unit_price, product_name, cart_key} for cart."""
    cart = get_cart(request)
    if not cart:
        return []
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
        pid_used = pid if pid else 0
        result.append({
            "artwork": artwork,
            "quantity": qty,
            "unit_price": unit_price,
            "product_name": product_name,
            "cart_key": key,
            "product_id": pid_used,
        })
    return result


def get_cart_total(request):
    """Return total price of cart."""
    items = get_cart_items(request)
    return sum((item["unit_price"] * item["quantity"] for item in items), Decimal("0"))
