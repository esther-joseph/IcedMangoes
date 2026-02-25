# Prisma

[← Back to Wiki](README.md)

## Overview

**Prisma Client Python** is an optional type-safe ORM that can be used alongside Django when running with SQLite.

## Limitations

- Works only when `USE_SQLITE=1`
- Requires `DATABASE_URL="file:./db.sqlite3"`
- Schema must match Django tables; Prisma maps to `store_artist` and `store_artwork`

## Setup

```bash
# 1. Set DATABASE_URL (in .env or shell)
export DATABASE_URL="file:./db.sqlite3"

# 2. Run Django migrations first (creates tables)
USE_SQLITE=1 python manage.py migrate

# 3. Generate Prisma client
prisma generate
```

## Schema

`schema.prisma` defines:

- `Artist` → `store_artist`
- `Artwork` → `store_artwork` (with `artist` relation)

## Usage

```python
from prisma import Prisma

db = Prisma()
db.connect()

artworks = db.artwork.find_many(where={"available": True})
for a in artworks:
    print(a.title, a.artist.name)

db.disconnect()
```

See `store/prisma_client.py` for a helper that returns the client when available.
