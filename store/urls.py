"""Store URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("artworks/add/", views.add_artwork, name="add_artwork"),
    path("cart/add/<int:artwork_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:artwork_id>/", views.cart_remove, name="cart_remove"),
    path("orders/", views.orders_list, name="orders_list"),
    path("checkout/", views.checkout_create, name="checkout_create"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("admin-panel/", views.store_admin, name="store_admin"),
    path("admin-panel/theme/", views.admin_theme_update, name="admin_theme_update"),
    path("admin-panel/stripe/", views.admin_stripe_update, name="admin_stripe_update"),
    path("admin-panel/artwork/<int:artwork_id>/edit/", views.admin_artwork_edit, name="admin_artwork_edit"),
    path("admin-panel/artwork/<int:artwork_id>/delete/", views.admin_artwork_delete, name="admin_artwork_delete"),
    path("profile/", views.profile, name="profile"),
    path("profile/substack/", views.profile_substack_post, name="profile_substack_post"),
    path("profile/send-email/", views.profile_send_email, name="profile_send_email"),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
