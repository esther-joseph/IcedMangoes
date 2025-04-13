from django.shortcuts import render
from .services import ArtworkService

def index(request):
    artworks = ArtworkService.get_available_artworks()
    return render(request, 'store/index.html', {'artworks': artworks})
