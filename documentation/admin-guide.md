# Admin Guide

[← Back to Wiki](README.md)

## Accessing the Admin

1. Create a superuser (if not done):
   ```bash
   USE_SQLITE=1 python manage.py createsuperuser
   ```
2. Open http://localhost:8000/admin/
3. Log in with the superuser credentials.

## Artists

- **Add Artist**: Admin → Store → Artists → Add Artist
- **Edit**: Click an artist to change the name.
- Artworks are linked to artists via a foreign key.

## Artworks

- **Add Artwork**: Admin → Store → Artworks → Add Artwork
- **Fields**:
  - Artist (required)
  - Title, Description, Price
  - Image (optional)
  - Tags (comma-separated)
  - Available (checkbox; unchecked hides from storefront)
- **Filters**: Available
- **Search**: Title, description

## Mongo Express (Docker)

When using Docker with MongoDB, Mongo Express is available at http://localhost:8081 for direct database inspection.
