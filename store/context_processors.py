"""Template context processors."""
from .cart import get_cart_items, get_cart_total
from .models import SiteSettings


def store_context(request):
    """Add cart and nav context to all store templates."""
    is_staff = request.user.is_authenticated and request.user.is_staff
    return {
        "cart_items": get_cart_items(request),
        "cart_total": get_cart_total(request),
        "is_admin": is_staff,
        "is_user": request.user.is_authenticated and not request.user.is_staff,
        "is_public": not request.user.is_authenticated,
        "show_add_artwork": is_staff,
        "site_settings": SiteSettings.get(),
    }
