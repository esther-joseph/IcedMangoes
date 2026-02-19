"""Store views."""
from typing import Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import ArtworkService, ArtworkServiceProtocol


def index(
    request: HttpRequest,
    artwork_service: Optional[ArtworkServiceProtocol] = None,
) -> HttpResponse:
    """Render the storefront with available artworks."""
    service = artwork_service or ArtworkService
    artworks = service.get_available_artworks()
    return render(request, "store/index.html", {"artworks": artworks})
