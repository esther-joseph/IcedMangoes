"""Optional Prisma client for type-safe queries.

Use when USE_SQLITE=1 and DATABASE_URL is set (e.g. file:./db.sqlite3).
Run: prisma generate
"""
import os

_prisma_client = None


def get_prisma():
    """Return Prisma client if available (SQLite + prisma generate run)."""
    global _prisma_client
    if _prisma_client is not None:
        return _prisma_client
    if os.environ.get("USE_SQLITE", "").lower() not in ("true", "1", "yes"):
        return None
    try:
        from prisma import Prisma

        _prisma_client = Prisma()
        return _prisma_client
    except ImportError:
        return None
