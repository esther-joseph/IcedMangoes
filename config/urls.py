"""URL configuration for IcedMangoes."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from graphene_django.views import GraphQLView

from store.api import artwork_detail, artwork_list, cart_detail, order_detail, order_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
    path("login/", auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # REST API — consumed by Next.js frontend (see documentation/ARCHITECTURE_DECISION_RECORD.md)
    path("api/artworks/", artwork_list, name="api_artworks"),
    path("api/artworks/<int:pk>/", artwork_detail, name="api_artwork_detail"),
    path("api/cart/", cart_detail, name="api_cart"),
    path("api/orders/", order_list, name="api_orders"),
    path("api/orders/<int:pk>/", order_detail, name="api_order_detail"),
    path("", include("store.urls")),
]
