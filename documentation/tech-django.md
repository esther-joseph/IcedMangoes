# Django

[← Back to Wiki](README.md)

## Overview

IcedMangoes uses Django 3.2–4.1 with a service-layer architecture. Views are thin; business logic lives in `store/services.py`.

## Project Structure

```
config/           # Project settings
  settings.py
  urls.py
  schema.py       # GraphQL schema
store/            # Main app
  models.py       # Artist, Artwork
  views.py        # HTTP handlers
  services.py     # Domain logic
  forms.py        # ArtworkForm
  urls.py
  templates/
```

## Models

- **Artist**: `id`, `name`
- **Artwork**: `artist` (FK), `title`, `description`, `price`, `image`, `tags`, `available`

See [../store/models.py](../store/models.py).

## Migrations

```bash
# Create migrations
python manage.py makemigrations store

# Apply
USE_SQLITE=1 python manage.py migrate   # SQLite
# or
docker-compose exec web python manage.py migrate   # Docker/MongoDB
```

## Key Commands

| Command | Description |
|---------|-------------|
| `runserver` | Start dev server |
| `migrate` | Apply migrations |
| `makemigrations` | Create migrations |
| `createsuperuser` | Create admin user |
| `collectstatic` | Gather static files (production) |
