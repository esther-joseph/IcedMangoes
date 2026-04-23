"""Optional Prisma client — scaffolding only, not wired up anywhere.

Prisma's Python client is async-only; it requires prisma.connect() before
use and an async runtime. This does not fit the synchronous Django request
cycle, so prefer Django's ORM for all current queries.

To use: set USE_SQLITE=1, run `prisma generate`, then call get_prisma() and
await prisma.connect() inside an async context.
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
