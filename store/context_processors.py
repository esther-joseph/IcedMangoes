"""Template context processors."""
from .cart import get_cart_items, get_cart_total
from .models import SiteSettings


def store_context(request):
    """Add cart and nav context to all store templates."""
    is_staff = request.user.is_authenticated and request.user.is_staff
    is_authenticated = request.user.is_authenticated

    # Testing toggle: view_as_test cookie overrides display (admin/guest) for nav preview
    view_as = request.COOKIES.get("view_as_test", "").strip().lower()
    if view_as == "admin":
        is_admin = True
        is_user = False
        is_public = False
        show_add_artwork = True
        view_as_override = "admin"
    elif view_as == "guest":
        is_admin = False
        is_user = False
        is_public = True
        show_add_artwork = False
        view_as_override = "guest"
    else:
        is_admin = is_staff
        is_user = is_authenticated and not is_staff
        is_public = not is_authenticated
        show_add_artwork = is_staff
        view_as_override = None

    return {
        "cart_items": get_cart_items(request),
        "cart_total": get_cart_total(request),
        "is_admin": is_admin,
        "is_user": is_user,
        "is_public": is_public,
        "show_add_artwork": show_add_artwork,
        "site_settings": SiteSettings.get(),
        "view_as_override": view_as_override,
    }
