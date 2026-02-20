# Installation & Deployment Guide

[← Back to Wiki](README.md)

This guide walks you through installing IcedMangoes (artist storefront template) and deploying it to production.

---

## Installation Checklist

Before you begin, ensure you have the following tools installed and accessible:

| Tool | Required | How to check | Install if missing |
|------|----------|--------------|--------------------|
| **Python 3.11+** | Yes | `python3 --version` or `python --version` | [python.org](https://www.python.org/downloads/) |
| **pip** | Yes | `pip --version` or `pip3 --version` | Usually bundled with Python |
| **Node.js 18+** | Yes (for CSS build) | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | Yes | `npm --version` | Bundled with Node.js |
| **Git** | Yes | `git --version` | [git-scm.com](https://git-scm.com/) |
| **Docker** | Optional (Docker path) | `docker --version` | [docker.com](https://www.docker.com/) |
| **Docker Compose** | Optional | `docker compose version` | Bundled with Docker Desktop |

### Quick verification

Run these commands. All should complete without errors:

```bash
python3 --version   # Expect 3.11 or higher
pip3 --version
node --version      # Expect 18.x or higher
npm --version
git --version
```

---

## Installation Steps

### 1. Clone the repository

```bash
git clone <your-repo-url> IcedMangoes
cd IcedMangoes
```

### 2. Set up Python environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Unix/macOS)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set up frontend assets

```bash
npm install
npm run build:css
```

### 4. Configure environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (see Environment Variables below)
```

### 5. Run migrations

**Option A: SQLite (simplest for local dev)**

```bash
USE_SQLITE=1 python manage.py migrate
```

**Option B: MongoDB (Docker)**

```bash
docker compose up -d mongodb
python manage.py migrate
```

### 6. Create admin user (optional but recommended)

```bash
python manage.py createsuperuser
```

### 7. Run the application

```bash
python manage.py runserver
```

Open http://localhost:8000 in your browser.

---

## Alternative: Docker (all-in-one)

If you have Docker and Docker Compose installed:

```bash
docker compose up --build
```

In a separate terminal:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

The app runs at http://localhost:8000; MongoDB and Mongo Express are included.

---

## Post-Install Verification

1. **Homepage loads** — Visit http://localhost:8000
2. **Login works** — Log in with your superuser account
3. **Admin access** — Click "Admin Panel" and "Business" in the side menu
4. **Add artwork** — Use the + button to add an artwork with an image
5. **Cart & checkout** — Add an item to cart and run through checkout (Stripe or demo mode)
6. **Storage check** (if using Supabase): `python manage.py check_storage`

---

## Deployment

### Render (recommended for artists)

Render offers a free tier and straightforward deployment. The filesystem is ephemeral, so you **must** use Supabase Storage for artwork images.

1. **Create a Render account** at [render.com](https://render.com)
2. **Connect your repository** — New → Web Service → connect GitHub/GitLab
3. **Configure the service:**
   - **Build command:** `pip install -r requirements.txt && npm install && npm run build:css`
   - **Start command:** `gunicorn config.wsgi:application` (add `gunicorn` to `requirements.txt` if not present)
   - **Environment:** Add variables from `.env.example` (see [Deploy to Render](deploy-render.md))
4. **Set up Supabase Storage** — Required for media. Follow [Media Storage (Supabase)](deploy-render.md#media-storage-supabase-storage)
5. **Deploy** — Render builds and deploys automatically on push

Full Render details: [deploy-render.md](deploy-render.md)

### Other platforms

- **Railway, Fly.io, Heroku, etc.** — Use the same build/start commands. Ensure:
  - `DJANGO_ALLOWED_HOSTS` includes your app URL
  - Supabase Storage is configured for media (or equivalent S3-compatible storage)
  - Database (PostgreSQL/MySQL recommended for production; MongoDB via Atlas if needed)

---

## Environment Variables Summary

| Variable | When needed | Description |
|----------|-------------|-------------|
| `USE_SQLITE` | Local dev | `1` to use SQLite instead of MongoDB |
| `DJANGO_SECRET_KEY` | Production | Set a random secret; never use the default |
| `DJANGO_DEBUG` | Production | Set to `false` |
| `DJANGO_ALLOWED_HOSTS` | Production | Include your domain (e.g. `yourapp.onrender.com`) |
| `STRIPE_*` | Paid checkout | Stripe keys for real payments |
| `SUPABASE_*` | Production (Render, etc.) | Required for media storage on ephemeral platforms |

See `.env.example` for the full list.

---

## Troubleshooting

| Issue | Likely cause | Fix |
|-------|--------------|-----|
| `python3: command not found` | Python not installed or not in PATH | Install Python 3.11+; on Windows, ensure "Add to PATH" was checked |
| `npm: command not found` | Node.js not installed | Install Node.js 18+ from nodejs.org |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` with venv active |
| Port 8000 in use | Another process using the port | Use a different port: `python manage.py runserver 8080` |
| CSS looks broken | Tailwind not built | Run `npm run build:css` |
| Database connection error | MongoDB not running or wrong config | Use `USE_SQLITE=1` for local dev, or start MongoDB |
| Images 404 after deploy | Supabase not configured | Set all `SUPABASE_*` env vars; see [deploy-render.md](deploy-render.md) |
