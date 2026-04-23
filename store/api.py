"""Public REST API views (Django REST Framework).

Consumed by the Next.js frontend as part of the dual-stack consolidation plan
(see documentation/ARCHITECTURE_DECISION_RECORD.md). These endpoints replace
direct Supabase calls once the Next.js app is migrated.

All endpoints are read-only for the public storefront; order history requires
authentication.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .cart import get_cart_items, get_cart_total
from .models import Artwork, Order
from .serializers import ArtworkSerializer, OrderSerializer


@api_view(["GET"])
def artwork_list(request):
    """List available artworks. ?available=false includes sold/hidden items (admin only)."""
    show_all = request.query_params.get("available", "true").lower() == "false"
    if show_all and not request.user.is_staff:
        show_all = False
    qs = Artwork.objects.select_related("artist").prefetch_related(
        "artworkimage_set", "artworkproduct_set"
    )
    if not show_all:
        qs = qs.filter(available=True)
    serializer = ArtworkSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def artwork_detail(request, pk):
    """Retrieve a single artwork by ID."""
    try:
        artwork = Artwork.objects.select_related("artist").prefetch_related(
            "artworkimage_set", "artworkproduct_set"
        ).get(pk=pk)
    except Artwork.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ArtworkSerializer(artwork, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def cart_detail(request):
    """Return the current user's cart items and total."""
    items = get_cart_items(request)
    total = get_cart_total(request)
    return Response({
        "items": [
            {
                "artwork_id": item["artwork"].id,
                "artwork_title": item["artwork"].title,
                "artwork_image": request.build_absolute_uri(item["artwork"].image.url)
                if item["artwork"].image else None,
                "product_name": item["product_name"],
                "unit_price": str(item["unit_price"]),
                "quantity": item["quantity"],
                "cart_key": item["cart_key"],
            }
            for item in items
        ],
        "total": str(total),
        "count": sum(i["quantity"] for i in items),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_list(request):
    """Return the authenticated user's order history."""
    orders = Order.objects.filter(user=request.user).prefetch_related("orderitem_set__artwork")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """Return a single order belonging to the authenticated user."""
    try:
        order = Order.objects.prefetch_related("orderitem_set__artwork").get(
            pk=pk, user=request.user
        )
    except Order.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
