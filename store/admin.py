"""Django admin configuration for store models."""
from django.contrib import admin
from .models import Artist, Artwork, Order, OrderItem, SiteSettings


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "price", "available")
    list_filter = ("available",)
    search_fields = ("title", "description")
    raw_id_fields = ("artist",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("artwork",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "created_at")
    inlines = (OrderItemInline,)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "default_theme")
