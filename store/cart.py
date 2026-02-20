"""Session-based cart utilities."""
from decimal import Decimal

from .models import Artwork


def get_cart(request):
    """Return cart dict: {artwork_id: quantity}."""
    cart = request.session.get("cart", {})
    return {int(k): int(v) for k, v in cart.items() if v > 0}


def set_cart(request, cart):
    """Save cart to session."""
    request.session["cart"] = {str(k): v for k, v in cart.items() if v > 0}
    request.session.modified = True


def add_to_cart(request, artwork_id, quantity=1):
    """Add artwork to cart."""
    cart = get_cart(request)
    cart[artwork_id] = cart.get(artwork_id, 0) + quantity
    set_cart(request, cart)


def remove_from_cart(request, artwork_id):
    """Remove artwork from cart."""
    cart = get_cart(request)
    cart.pop(artwork_id, None)
    set_cart(request, cart)


def clear_cart(request):
    """Clear cart."""
    request.session["cart"] = {}
    request.session.modified = True


def get_cart_items(request):
    """Return list of (artwork, quantity) for cart."""
    cart = get_cart(request)
    if not cart:
        return []
    artworks = Artwork.objects.filter(id__in=cart.keys()).select_related("artist")
    return [(a, cart[a.id]) for a in artworks]


def get_cart_total(request):
    """Return total price of cart."""
    items = get_cart_items(request)
    return sum((a.price * q for a, q in items), Decimal("0"))
