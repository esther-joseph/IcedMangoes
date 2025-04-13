from .models import Artwork

class ArtworkService:
    @staticmethod
    def get_available_artworks():
        return [art for art in Artwork.objects.all() if art.available]
