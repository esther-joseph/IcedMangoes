# Add Artwork Flow

[← Back to Wiki](README.md)

## Overview

Artworks can be added via:

1. **Storefront modal** – 3-step form (recommended)
2. **GraphQL mutation** – metadata only (no image)
3. **Django admin** – full control

## Storefront Modal Flow

### Step 1: Image Upload

- **Input**: File input, `name="images"`, `multiple`, accept `image/*`
- **Validation**: At least one image required
- **Requirements**:
  - Formats: PNG, JPG, JPEG, GIF
  - Max size: 5 MB per image
  - Recommended: 1200×1200 px or larger
- First image is the main artwork image; additional images stored as `ArtworkImage` for the carousel

### Step 2: Details

| Field | Type | Required |
|-------|------|----------|
| Artist name | text | Yes |
| Title | text | Yes |
| Description | textarea | Yes |
| Tags | text (comma-separated) | No |
| Price | number (≥ 0) | Yes |
| Product form options | textarea (one per line: `Name, Price`) | No |

### Step 3: Review & Post

- Summary of all entered data including product options
- **Post** submits the form to `POST /artworks/add/`
- On success: redirect to `/`; new artwork appears in gallery
- **Close** (X, Escape, click outside) discards data; nothing saved

## Backend Process

1. Form POST hits `add_artwork` view
2. `request.FILES.getlist("images")` — at least one image required
3. `ArtworkForm` validates other fields
4. `ArtworkService.create_artwork(images=...)` runs
5. Artist is fetched or created; artwork created with first image
6. `ArtworkImage` rows created for extra images; `ArtworkProduct` for product options
7. Response: redirect to index

## GraphQL Alternative

Use `createArtwork` mutation for metadata-only creation (no image). Image upload still requires the form or admin.
