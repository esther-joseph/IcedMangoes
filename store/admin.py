"""Django admin configuration for store models."""
from django.contrib import admin
from .models import Artist, Artwork


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    """Admin for Artist model."""

    list_display = ("id", "name")


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    """Admin for Artwork model."""

    list_display = ("id", "title", "artist", "price", "available")
    list_filter = ("available",)
    search_fields = ("title", "description")
    raw_id_fields = ("artist",)
