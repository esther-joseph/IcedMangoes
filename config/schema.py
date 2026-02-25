"""GraphQL schema for IcedMangoes."""
import graphene
from graphene_django import DjangoObjectType

from store.models import Artist, Artwork


class ArtistType(DjangoObjectType):
    """GraphQL type for Artist."""

    class Meta:
        model = Artist
        fields = ("id", "name")


class ArtworkType(DjangoObjectType):
    """GraphQL type for Artwork."""

    class Meta:
        model = Artwork
        fields = ("id", "title", "description", "price", "image", "tags", "available", "artist")


class CreateArtwork(graphene.Mutation):
    """Mutation to create an artwork."""

    class Arguments:
        artist_name = graphene.String(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        tags = graphene.String()
        image = graphene.String()  # Base64 or URL - for simplicity use String; file upload via REST

    artwork = graphene.Field(ArtworkType)
    ok = graphene.Boolean()

    def mutate(self, info, artist_name, title, description, price, tags="", image=None):
        from store.services import ArtworkService

        # Image must be uploaded via the form/multipart; GraphQL mutation for metadata only
        # For full create with image, use the existing POST form or add file upload handling
        artwork = Artwork.objects.filter(
            artist__name=artist_name, title=title
        ).first()
        if not artwork:
            artist, _ = Artist.objects.get_or_create(name=artist_name.strip())
            artwork = Artwork.objects.create(
                artist=artist,
                title=title.strip(),
                description=description.strip(),
                price=price,
                tags=tags.strip() if tags else "",
            )
        return CreateArtwork(artwork=artwork, ok=True)


class Mutation(graphene.ObjectType):
    """GraphQL mutations."""

    create_artwork = CreateArtwork.Field()


class Query(graphene.ObjectType):
    """GraphQL queries."""

    artists = graphene.List(ArtistType)
    artist = graphene.Field(ArtistType, id=graphene.Int())
    artworks = graphene.List(ArtworkType, available=graphene.Boolean())
    artwork = graphene.Field(ArtworkType, id=graphene.Int())

    def resolve_artists(self, info):
        return Artist.objects.all()

    def resolve_artist(self, info, id=None):
        if id is None:
            return None
        return Artist.objects.filter(id=id).first()

    def resolve_artworks(self, info, available=True):
        qs = Artwork.objects.select_related("artist").all()
        if available is not None:
            qs = qs.filter(available=available)
        return qs.order_by("-id")

    def resolve_artwork(self, info, id=None):
        if id is None:
            return None
        return Artwork.objects.select_related("artist").filter(id=id).first()


schema = graphene.Schema(query=Query, mutation=Mutation)
