"""
Django settings for IcedMangoes.

Reads from environment variables. See .env.example for required vars.
"""
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-change-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "store",
]

# GraphQL
GRAPHENE = {
    "SCHEMA": "config.schema.schema",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "store.context_processors.store_context",
            ],
        },
    },
]

# Database - SQLite for local dev without Docker, MongoDB when available
_use_sqlite = os.environ.get("USE_SQLITE", "").lower() in ("true", "1", "yes")

if _use_sqlite:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    _mongo_host = os.environ.get("MONGO_HOST", "mongodb")
    _mongo_port = os.environ.get("MONGO_PORT", "27017")
    _mongo_user = os.environ.get("MONGO_USERNAME", "")
    _mongo_pass = os.environ.get("MONGO_PASSWORD", "")
    _mongo_name = os.environ.get("MONGO_INITDB_DATABASE", "artist_store_db")
    _auth = ""
    if _mongo_user and _mongo_pass:
        _auth = f"{_mongo_user}:{_mongo_pass}@"
    _mongo_uri = f"mongodb://{_auth}{_mongo_host}:{_mongo_port}"
    DATABASES = {
        "default": {
            "ENGINE": "djongo",
            "NAME": _mongo_name,
            "ENFORCE_SCHEMA": False,
            "CLIENT": {"host": _mongo_uri},
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media storage: Supabase (S3-compatible) or local filesystem
_supabase_bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "").strip()
_supabase_endpoint = os.environ.get("SUPABASE_S3_ENDPOINT", "").strip()
_supabase_access = os.environ.get("SUPABASE_S3_ACCESS_KEY_ID", "").strip()
_supabase_secret = os.environ.get("SUPABASE_S3_SECRET_ACCESS_KEY", "").strip()
_supabase_region = os.environ.get("SUPABASE_S3_REGION", "us-east-1").strip()
_use_supabase_storage = all([_supabase_bucket, _supabase_endpoint, _supabase_access, _supabase_secret])

if _use_supabase_storage:
    DEFAULT_FILE_STORAGE = "store.storage_backends.SupabaseS3Storage"
    AWS_ACCESS_KEY_ID = _supabase_access
    AWS_SECRET_ACCESS_KEY = _supabase_secret
    AWS_STORAGE_BUCKET_NAME = _supabase_bucket
    AWS_S3_ENDPOINT_URL = _supabase_endpoint
    AWS_S3_REGION_NAME = _supabase_region
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    _media_private = os.environ.get("MEDIA_PRIVATE", "").lower() in ("true", "1", "yes")
    AWS_QUERYSTRING_AUTH = _media_private
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    _public_base = os.environ.get("SUPABASE_STORAGE_PUBLIC_BASE_URL", "").strip()
    SUPABASE_STORAGE_PUBLIC_BASE_URL = _public_base or None  # For storage backend
    if _public_base and not _media_private:
        MEDIA_URL = _public_base.rstrip("/") + "/"
    else:
        MEDIA_URL = f"{_supabase_endpoint.rstrip('/').rsplit('/', 1)[0]}/object/public/{_supabase_bucket}/"
    MEDIA_ROOT = ""  # Not used with S3
else:
    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Auth
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Stripe
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# Fulfillment providers (see .env.example)
SHIPPO_API_TOKEN = os.environ.get("SHIPPO_API_TOKEN", "")
EASYPOST_API_KEY = os.environ.get("EASYPOST_API_KEY", "")
PRINTFUL_API_KEY = os.environ.get("PRINTFUL_API_KEY", "")
PRINTIFY_API_KEY = os.environ.get("PRINTIFY_API_KEY", "")
GELATO_API_KEY = os.environ.get("GELATO_API_KEY", "")

# Email
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@localhost")
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
