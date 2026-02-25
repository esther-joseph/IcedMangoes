# API Reference

[← Back to Wiki](README.md)

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Storefront (HTML) |
| `/graphql/` | GET, POST | GraphQL API (GraphiQL UI on GET) |
| `/artworks/add/` | POST | Create artwork (multipart form) |
| `/admin/` | GET | Django admin |

## GraphQL Schema

### Queries

```graphql
type Query {
  artists: [ArtistType!]!
  artist(id: Int): ArtistType
  artworks(available: Boolean): [ArtworkType!]!
  artwork(id: Int): ArtworkType
}
```

### Mutations

```graphql
type Mutation {
  createArtwork(
    artistName: String!
    title: String!
    description: String!
    price: Decimal!
    tags: String
  ): CreateArtwork
}
```

### Types

```graphql
type ArtistType {
  id: Int!
  name: String!
}

type ArtworkType {
  id: Int!
  title: String!
  description: String!
  price: Decimal!
  image: String
  tags: String
  available: Boolean!
  artist: ArtistType!
}
```

## REST: Add Artwork (POST /artworks/add/)

| Field | Type | Required |
|-------|------|----------|
| `csrfmiddlewaretoken` | string | Yes |
| `image` | file | Yes |
| `artist_name` | string | Yes |
| `title` | string | Yes |
| `description` | string | Yes |
| `tags` | string | No |
| `price` | decimal | Yes |

**Response**: 302 redirect to `/` on success.
