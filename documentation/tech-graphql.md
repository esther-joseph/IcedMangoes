# GraphQL

[← Back to Wiki](README.md)

## Overview

GraphQL is provided by **Graphene-Django**. The schema lives in `config/schema.py`. Interactive docs: http://localhost:8000/graphql/

## Types

- **ArtistType**: `id`, `name`
- **ArtworkType**: `id`, `title`, `description`, `price`, `image`, `tags`, `available`, `artist`

## Queries

| Query | Args | Description |
|-------|------|-------------|
| `artists` | — | List all artists |
| `artist` | `id` | Get one artist |
| `artworks` | `available` (bool) | List artworks, filter by availability |
| `artwork` | `id` | Get one artwork |

## Mutations

| Mutation | Args | Description |
|----------|------|-------------|
| `createArtwork` | `artistName`, `title`, `description`, `price`, `tags` | Create artwork (metadata; image via form) |

## Example Queries

```graphql
# List artworks
query {
  artworks {
    id
    title
    price
    artist { name }
  }
}

# Single artwork
query {
  artwork(id: 1) {
    title
    description
    tags
  }
}
```

## Example Mutation

```graphql
mutation {
  createArtwork(
    artistName: "Jane Doe"
    title: "Sunset"
    description: "Oil on canvas"
    price: 199.99
    tags: "abstract, landscape"
  ) {
    ok
    artwork { id title }
  }
}
```
