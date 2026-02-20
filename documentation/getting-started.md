# Getting Started

[← Back to Wiki](README.md)

## Prerequisites

- Python 3.11+
- Node.js 18+ (for CSS build)
- Docker & Docker Compose (optional, for containerized setup)
- MongoDB (required only when not using SQLite)

## Quick Start (Local, SQLite)

```bash
# Clone and enter project
cd IcedMangoes

# Python setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend assets
npm install
npm run build:css

# Database
USE_SQLITE=1 python manage.py migrate
USE_SQLITE=1 python manage.py runserver
```

Open http://localhost:8000

## Docker Setup

```bash
docker-compose up --build
```

In another terminal:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser  # optional
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_SQLITE` | Use SQLite instead of MongoDB | (off) |
| `DATABASE_URL` | Prisma: SQLite path | `file:./db.sqlite3` |
| `MONGO_HOST` | MongoDB host | `mongodb` |
| `MONGO_PORT` | MongoDB port | `27017` |
| `MONGO_INITDB_DATABASE` | MongoDB database name | `artist_store_db` |
| `DJANGO_SECRET_KEY` | Django secret | dev placeholder |
| `DJANGO_DEBUG` | Debug mode | `true` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |

Copy `.env.example` to `.env` and adjust as needed.
