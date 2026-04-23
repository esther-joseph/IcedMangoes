"""DRF serializers for the public REST API."""
from rest_framework import serializers

from .models import Artist, Artwork, ArtworkImage, ArtworkProduct, Order, OrderItem


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name")


class ArtworkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImage
        fields = ("id", "image", "order")


class ArtworkProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkProduct
        fields = ("id", "name", "price")


class ArtworkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    images = ArtworkImageSerializer(source="artworkimage_set", many=True, read_only=True)
    products = ArtworkProductSerializer(source="artworkproduct_set", many=True, read_only=True)

    class Meta:
        model = Artwork
        fields = ("id", "title", "description", "price", "image", "tags", "available", "artist", "images", "products")


class OrderItemSerializer(serializers.ModelSerializer):
    artwork_title = serializers.CharField(source="artwork.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "artwork_title", "quantity", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "status", "total", "payment_method",
            "shipping_name", "shipping_city", "shipping_country",
            "tracking_number", "created_at", "items",
        )
