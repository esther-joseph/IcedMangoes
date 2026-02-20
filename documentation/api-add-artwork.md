# Add Artwork Flow

[← Back to Wiki](README.md)

## Overview

Artworks can be added via:

1. **Storefront modal** – 3-step form (recommended)
2. **GraphQL mutation** – metadata only (no image)
3. **Django admin** – full control

## Storefront Modal Flow

### Step 1: Image Upload

- **Input**: File input, accept `image/*`
- **Validation**: File selected, image type
- **Requirements**:
  - Formats: PNG, JPG, JPEG, GIF
  - Max size: 5 MB
  - Recommended: 1200×1200 px or larger
  - Aspect ratio: Any (square works best for grid)

### Step 2: Details

| Field | Type | Required |
|-------|------|----------|
| Artist name | text | Yes |
| Title | text | Yes |
| Description | textarea | Yes |
| Tags | text (comma-separated) | No |
| Price | number (≥ 0) | Yes |

### Step 3: Review & Post

- Summary of all entered data
- **Post** submits the form to `POST /artworks/add/`
- On success: redirect to `/`; new artwork appears in gallery

## Backend Process

1. Form POST hits `add_artwork` view
2. `ArtworkForm` validates input
3. `ArtworkService.create_artwork()` runs
4. Artist is fetched or created (`get_or_create` by name)
5. Artwork is created with `available=True`
6. Response: redirect to index

## GraphQL Alternative

Use `createArtwork` mutation for metadata-only creation (no image). Image upload still requires the form or admin.
