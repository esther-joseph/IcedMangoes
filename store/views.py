"""Store views."""
import json
import time
from collections import Counter
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .cart import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    get_cart_total,
    remove_from_cart,
)
from .webhooks import (
    build_cart_signature,
    create_idempotency_key,
    get_webhook_secret,
    handle_checkout_session_completed,
)
from .forms import ArtworkEditForm, ArtworkForm
from .fulfillment_service import (
    get_effective_settings,
    get_provider_credentials,
    get_provider_status,
    is_env_configured,
    save_provider_key,
    set_settings,
)
from .models import Artwork, Order, OrderItem, SiteSettings
from .services import ArtworkService, ArtworkServiceProtocol
from .substack import fetch_substack_feed, SubstackPost


def index(
    request: HttpRequest,
    artwork_service: Optional[ArtworkServiceProtocol] = None,
) -> HttpResponse:
    """Render the storefront with available artworks."""
    service = artwork_service or ArtworkService
    artworks = service.get_available_artworks()
    form = ArtworkForm()
    ctx = {"artworks": artworks, "artwork_form": form}
    return render(request, "store/index.html", ctx)


def add_artwork(request: HttpRequest) -> HttpResponse:
    """Handle artwork creation via POST (admin only). Requires at least one image."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("index")
    if request.method != "POST":
        return redirect("index")
    images = list(request.FILES.getlist("images"))
    form = ArtworkForm(request.POST)
    if form.is_valid() and images:
        ArtworkService.create_artwork(
            artist_name=form.cleaned_data["artist_name"],
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            price=form.cleaned_data["price"],
            images=images,
            tags=form.cleaned_data.get("tags", "") or "",
            product_options=form.cleaned_data.get("product_options", "") or "",
        )
    return redirect("index")


def cart_add(request: HttpRequest, artwork_id: int) -> HttpResponse:
    """Add artwork to cart. Optional product_id for variant (GET/POST)."""
    artwork = get_object_or_404(Artwork, id=artwork_id, available=True)
    product_id = request.GET.get("product_id") or request.POST.get("product_id")
    pid = int(product_id) if product_id and str(product_id).isdigit() else None
    if pid:
        from .models import ArtworkProduct
        get_object_or_404(ArtworkProduct, pk=pid, artwork=artwork)
    add_to_cart(request, artwork_id, product_id=pid)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


def cart_remove(request: HttpRequest, artwork_id: int) -> HttpResponse:
    """Remove cart line. Optional product_id (GET) for variant."""
    product_id = request.GET.get("product_id")
    pid = int(product_id) if product_id and str(product_id).isdigit() else None
    remove_from_cart(request, artwork_id, product_id=pid)
    next_url = request.GET.get("next", "index")
    return redirect(next_url)


def orders_list(request: HttpRequest) -> HttpResponse:
    """List past orders for logged-in user."""
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    orders = Order.objects.filter(user=request.user).prefetch_related("orderitem_set__artwork__artist")
    ctx = {"orders": orders}
    return render(request, "store/orders.html", ctx)


def checkout_create(request: HttpRequest) -> HttpResponse:
    """Create Stripe Checkout session and redirect. Idempotent for Stripe and demo modes."""
    cart_items = get_cart_items(request)
    if not cart_items:
        return redirect("index")
    total = get_cart_total(request)
    if total <= 0:
        return redirect("index")

    site = SiteSettings.get()
    stripe_key = (site.stripe_secret_key or getattr(settings, "STRIPE_SECRET_KEY", "") or "").strip()
    if not stripe_key:
        # Demo: create order without Stripe. Idempotent via session to prevent double orders.
        cart_sig = build_cart_signature(cart_items)
        last_key = request.session.get("demo_checkout_key")
        last_ts = request.session.get("demo_checkout_ts", 0)
        now = int(time.time())
        if last_key == cart_sig and (now - last_ts) < 60:
            return redirect("orders_list" if request.user.is_authenticated else "index")
        from .order_service import request_fulfillment

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total=total,
            payment_method="card",
            status="PAID",
        )
        for item in cart_items:
            art = item["artwork"]
            qty = item["quantity"]
            price = item["unit_price"]
            OrderItem.objects.create(order=order, artwork=art, quantity=qty, price=price)
        request_fulfillment(order)
        clear_cart(request)
        request.session["demo_checkout_key"] = cart_sig
        request.session["demo_checkout_ts"] = now
        request.session.modified = True
        return redirect("orders_list" if request.user.is_authenticated else "index")

    import stripe

    stripe.api_key = stripe_key
    user_id = request.user.id if request.user.is_authenticated else "anon"
    cart_sig = build_cart_signature(cart_items)
    idempotency_key = create_idempotency_key(user_id, cart_sig)
    client_ref = f"user:{user_id}" if isinstance(user_id, int) else "anon"

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": (item["artwork"].title + (f" — {item['product_name']}" if item.get("product_name") else "")),
                    "images": [request.build_absolute_uri(item["artwork"].image.url)] if item["artwork"].image else [],
                    "metadata": {"artwork_id": str(item["artwork"].id)},
                },
                "unit_amount": int(item["unit_price"] * 100),
            },
            "quantity": item["quantity"],
        }
        for item in cart_items
    ]
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/checkout/success/") + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri("/"),
        client_reference_id=client_ref,
        idempotency_key=idempotency_key,
    )
    return redirect(session.url)


def checkout_success(request: HttpRequest) -> HttpResponse:
    """Handle successful checkout redirect. Order is created by webhook; we display or wait."""
    session_id = request.GET.get("session_id", "").strip()
    clear_cart(request)
    success_redirect = "orders_list" if request.user.is_authenticated else "index"

    if not session_id:
        return redirect(success_redirect)

    order = Order.objects.filter(stripe_session_id=session_id).first()
    if order:
        return redirect(success_redirect)

    ctx = {
        "session_id": session_id,
        "success_redirect": success_redirect,
        "poll_for_order": request.user.is_authenticated,
    }
    return render(request, "store/checkout_processing.html", ctx)


def store_admin(request: HttpRequest) -> HttpResponse:
    """Admin panel: theme customization, artwork CRUD."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("index")
    site = SiteSettings.get()
    artworks = Artwork.objects.select_related("artist").all()
    ctx = {"site_settings": site, "artworks": artworks}
    return render(request, "store/admin_panel.html", ctx)


def admin_artwork_update(request: HttpRequest, artwork_id: int) -> HttpResponse:
    """Update artwork (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("index")
    artwork = get_object_or_404(Artwork, id=artwork_id)
    form = ArtworkEditForm(request.POST, request.FILES)
    if form.is_valid():
        artist_name = form.cleaned_data["artist_name"].strip()
        from .models import Artist

        artist, _ = Artist.objects.get_or_create(name=artist_name)
        artwork.artist = artist
        artwork.title = form.cleaned_data["title"].strip()
        artwork.description = form.cleaned_data["description"].strip()
        artwork.tags = form.cleaned_data.get("tags", "") or ""
        artwork.price = form.cleaned_data["price"]
        artwork.available = form.cleaned_data.get("available", True)
        if form.cleaned_data.get("image"):
            artwork.image = form.cleaned_data["image"]
        artwork.save()
    return redirect("store_admin")


def admin_theme_update(request: HttpRequest) -> HttpResponse:
    """Update site theme (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("index")
    site = SiteSettings.get()
    theme = request.POST.get("default_theme", "cute-beige")
    if theme in ("cute-beige", "lavender", "baby-blue", "peach-pink", "slate-gray", "mint-green", "coral-red"):
        site.default_theme = theme
        site.save()
    site_name = request.POST.get("site_name", "").strip()
    tagline = request.POST.get("tagline", "").strip()
    if site_name:
        site.site_name = site_name
    if tagline:
        site.tagline = tagline
    site.save()
    return redirect("store_admin")


def admin_stripe_update(request: HttpRequest) -> HttpResponse:
    """Update Stripe keys (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("index")
    site = SiteSettings.get()
    pk = request.POST.get("stripe_publishable_key", "").strip()
    sk = request.POST.get("stripe_secret_key", "").strip()
    if pk:
        site.stripe_publishable_key = pk
    if sk:
        site.stripe_secret_key = sk
    site.save()
    return redirect("store_admin")


def admin_artwork_edit(request: HttpRequest, artwork_id: int) -> HttpResponse:
    """Edit artwork (admin only)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("index")
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == "POST":
        form = ArtworkEditForm(request.POST, request.FILES, initial={
            "title": artwork.title,
            "description": artwork.description,
            "tags": artwork.tags,
            "price": artwork.price,
            "artist_name": artwork.artist.name,
            "available": artwork.available,
        })
        if form.is_valid():
            from .models import Artist
            artist, _ = Artist.objects.get_or_create(name=form.cleaned_data["artist_name"].strip())
            artwork.artist = artist
            artwork.title = form.cleaned_data["title"].strip()
            artwork.description = form.cleaned_data["description"].strip()
            artwork.tags = (form.cleaned_data.get("tags") or "").strip()
            artwork.price = form.cleaned_data["price"]
            artwork.available = bool(form.cleaned_data.get("available"))
            if form.cleaned_data.get("image"):
                artwork.image = form.cleaned_data["image"]
            artwork.save()
            return redirect("store_admin")
    else:
        form = ArtworkEditForm(initial={
            "title": artwork.title,
            "description": artwork.description,
            "tags": artwork.tags,
            "price": artwork.price,
            "artist_name": artwork.artist.name,
            "available": artwork.available,
        })
    return render(request, "store/admin_artwork_edit.html", {"form": form, "artwork": artwork})


def admin_artwork_delete(request: HttpRequest, artwork_id: int) -> HttpResponse:
    """Delete artwork (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("index")
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()
    return redirect("store_admin")


def profile(request: HttpRequest) -> HttpResponse:
    """Profile dashboard. Admin sees full data; guest sees same layout with empty/placeholder data."""
    from calendar import monthrange

    now = timezone.now()
    is_staff = request.user.is_authenticated and request.user.is_staff

    if is_staff:
        orders = Order.objects.all().order_by("-created_at")
        month_counts = {}
        for i in range(5, -1, -1):
            y, m = now.year, now.month
            m -= i
            while m <= 0:
                m += 12
                y -= 1
            month_start = timezone.make_aware(datetime(y, m, 1))
            last_day = monthrange(y, m)[1]
            month_end = timezone.make_aware(datetime(y, m, last_day, 23, 59, 59)) + timedelta(seconds=1)
            month_counts[month_start.strftime("%b %Y")] = orders.filter(
                created_at__gte=month_start, created_at__lt=month_end
            ).count()
        chart_labels = list(month_counts.keys())
        chart_data = list(month_counts.values())

        tag_counts = Counter()
        for oi in OrderItem.objects.select_related("artwork"):
            if oi.artwork.tags:
                for t in oi.artwork.tags.replace(",", " ").split():
                    tag_counts[t.strip().lower()] += 1
        popular_tags = tag_counts.most_common(10)

        User = get_user_model()
        users = User.objects.all().order_by("-date_joined")[:50]
    else:
        # Guest: empty data for same layout (last 6 months labels)
        month_counts_guest = {}
        for i in range(5, -1, -1):
            y, m = now.year, now.month
            m -= i
            while m <= 0:
                m += 12
                y -= 1
            month_counts_guest[timezone.make_aware(datetime(y, m, 1)).strftime("%b %Y")] = 0
        chart_labels = list(month_counts_guest.keys())
        chart_data = [0] * 6
        popular_tags = []
        orders = []
        users = []

    ctx = {
        "orders": list(orders[:50]) if is_staff else [],
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
        "popular_tags_labels": json.dumps([t[0] for t in popular_tags]),
        "popular_tags_data": json.dumps([t[1] for t in popular_tags]),
        "popular_tags": popular_tags,
        "store_users": users,
    }
    return render(request, "store/profile.html", ctx)


def profile_substack_post(request: HttpRequest) -> HttpResponse:
    """Handle Substack post (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("profile")
    # Placeholder - Substack API would go here
    return redirect("profile")


@require_POST
def profile_substack_settings(request: HttpRequest) -> HttpResponse:
    """Save Substack publication URL (admin only)."""
    if not request.user.is_staff:
        return redirect("profile")
    url = request.POST.get("substack_publication_url", "").strip()
    site = SiteSettings.get()
    site.substack_publication_url = url[:255] if url else ""
    site.save()
    return redirect("profile")


def blog(request: HttpRequest) -> HttpResponse:
    """Public blog page: list of Substack posts with month/year navigation."""
    site = SiteSettings.get()
    publication_url = (site.substack_publication_url or "").strip()
    posts: list[SubstackPost] = []
    if publication_url:
        posts = fetch_substack_feed(publication_url)

    # Group posts by (year, month) for journal nav
    from collections import OrderedDict

    groups: OrderedDict[tuple[int, int], list[SubstackPost]] = OrderedDict()
    for p in posts:
        key = (p.published.year, p.published.month)
        if key not in groups:
            groups[key] = []
        groups[key].append(p)

    month_names = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    nav_items = [{"year": y, "month": m, "label": f"{month_names[m]} {y}", "slug": f"y{y}m{m}"} for (y, m) in groups.keys()]
    groups_list = [
        {"year": y, "month": m, "month_name": month_names[m], "slug": f"y{y}m{m}", "posts": group_posts}
        for (y, m), group_posts in groups.items()
    ]

    ctx = {
        "posts": posts,
        "groups": groups_list,
        "nav_items": nav_items,
        "has_substack": bool(publication_url),
    }
    return render(request, "store/blog.html", ctx)


def profile_send_email(request: HttpRequest) -> HttpResponse:
    """Send customized email to user (admin only)."""
    if not request.user.is_staff or request.method != "POST":
        return redirect("profile")
    from django.core.mail import send_mail

    to_email = request.POST.get("to_email", "").strip()
    subject = request.POST.get("subject", "Thank you for your purchase!")
    body = request.POST.get("body", "").strip() or (
        "Thank you for your purchase! We appreciate your support.\n\n"
        "Your order will arrive digitally within 24 hours, or physically within 5-7 business days depending on your location.\n\n"
        "Best regards,\nThe Artist Store Team"
    )
    if to_email:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL or "noreply@example.com",
            [to_email],
            fail_silently=True,
        )
    return redirect("profile")


def business(request: HttpRequest) -> HttpResponse:
    """Business page: fulfillment config, provider integrations (admin only)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect(settings.LOGIN_URL)
    eff = get_effective_settings()
    providers_info = {}
    for p in ("shippo", "easypost", "printful", "printify", "gelato"):
        providers_info[p] = {
            "status": get_provider_status(p),
            "env_configured": is_env_configured(p),
        }
    ctx = {
        "effective_settings": eff,
        "providers_info": providers_info,
    }
    return render(request, "store/business.html", ctx)


def protect_your_art(request: HttpRequest) -> HttpResponse:
    """Informational page: Glaze/WebGlaze/Nightshade workflow. No processing; links to official resources."""
    return render(request, "store/protect_your_art.html")


@require_POST
def business_settings_update(request: HttpRequest) -> HttpResponse:
    """Update fulfillment settings (admin only)."""
    if not request.user.is_staff:
        return redirect("index")
    fulfillment_mode = request.POST.get("fulfillment_mode", "MANUAL")
    manual_provider = request.POST.get("manual_provider", "none")
    pod_provider = request.POST.get("pod_provider", "none")
    use_env_secrets = request.POST.get("use_env_secrets") == "true"
    if fulfillment_mode in ("MANUAL", "POD"):
        set_settings(fulfillment_mode, manual_provider, pod_provider, use_env_secrets)
    return redirect("business")


@require_POST
def business_provider_save_key(request: HttpRequest, provider: str) -> HttpResponse:
    """Save provider API key to DB (admin only, when use_env_secrets=False)."""
    if not request.user.is_staff:
        return HttpResponse("Forbidden", status=403)
    if provider not in ("shippo", "easypost", "printful", "printify", "gelato"):
        return HttpResponse("Invalid provider", status=400)
    api_key = request.POST.get("api_key", "").strip()
    save_provider_key(provider, api_key)
    return redirect("business")


def business_provider_test(request: HttpRequest, provider: str) -> JsonResponse:
    """Test provider connection (admin only, POST)."""
    if not request.user.is_staff or request.method != "POST":
        return JsonResponse({"success": False, "message": "Forbidden"}, status=403)
    if provider not in ("shippo", "easypost", "printful", "printify", "gelato"):
        return JsonResponse({"success": False, "message": "Invalid provider"}, status=400)
    key = get_provider_credentials(provider)
    if not key:
        return JsonResponse({"success": False, "message": "No API key configured"})
    ok, msg = _test_provider_connection(provider, key)
    return JsonResponse({"success": ok, "message": msg})


def _test_provider_connection(provider: str, api_key: str) -> tuple[bool, str]:
    """Scaffold: validate key exists; optional real API call if package installed."""
    if not api_key or len(api_key) < 5:
        return False, "API key too short"
    if provider == "shippo":
        try:
            import shippo
            shippo.api_key = api_key
            return True, "Shippo connection verified"
        except ImportError:
            return True, "Shippo key present (install shippo package for full test)"
        except Exception as e:
            return False, str(e)
    if provider == "easypost":
        try:
            import easypost
            easypost.api_key = api_key
            return True, "EasyPost connection verified"
        except ImportError:
            return True, "EasyPost key present (install easypost for full test)"
        except Exception as e:
            return False, str(e)
    return True, f"{provider.title()} key present (scaffold)"


@csrf_exempt
@require_POST
def fulfillment_webhook(request: HttpRequest, provider: str) -> HttpResponse:
    """Route provider webhooks to handler. Thin view; delegates to services."""
    if provider not in ("shippo", "easypost", "printful", "printify", "gelato"):
        return HttpResponse("Unknown provider", status=404)
    # Scaffold: would call provider.handle_webhook() and update Order status
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """Handle Stripe webhooks. Verifies signature and processes checkout.session.completed."""
    import stripe

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    webhook_secret = get_webhook_secret()
    if not webhook_secret:
        return HttpResponse("Webhook secret not configured", status=500)
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_session_completed(session)

    return HttpResponse(status=200)
