"""GraphQL schema for IcedMangoes."""
import graphene
from graphene_django import DjangoObjectType

from store.models import Artist, Artwork, ArtworkImage, ArtworkProduct


class ArtistType(DjangoObjectType):
    """GraphQL type for Artist."""

    class Meta:
        model = Artist
        fields = ("id", "name")


class ArtworkImageType(DjangoObjectType):
    """GraphQL type for ArtworkImage."""

    class Meta:
        model = ArtworkImage
        fields = ("id", "image", "order")


class ArtworkProductType(DjangoObjectType):
    """GraphQL type for ArtworkProduct."""

    class Meta:
        model = ArtworkProduct
        fields = ("id", "name", "price")


class ArtworkType(DjangoObjectType):
    """GraphQL type for Artwork."""

    images = graphene.List(ArtworkImageType)
    products = graphene.List(ArtworkProductType)

    class Meta:
        model = Artwork
        fields = ("id", "title", "description", "price", "image", "tags", "available", "artist")

    def resolve_images(self, info):
        return self.artworkimage_set.all()

    def resolve_products(self, info):
        return self.artworkproduct_set.all()


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
    artwork_products = graphene.List(ArtworkProductType, artwork_id=graphene.Int(required=True))
    artwork_images = graphene.List(ArtworkImageType, artwork_id=graphene.Int(required=True))

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

    def resolve_artwork_products(self, info, artwork_id):
        return ArtworkProduct.objects.filter(artwork_id=artwork_id)

    def resolve_artwork_images(self, info, artwork_id):
        return ArtworkImage.objects.filter(artwork_id=artwork_id)


schema = graphene.Schema(query=Query, mutation=Mutation)
