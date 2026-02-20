# Deploy to Render

[← Back to Wiki](README.md)

This guide covers deploying IcedMangoes to Render, including media storage with Supabase (required because Render's filesystem is ephemeral).

---

## Media Storage (Supabase Storage)

**Why Supabase?** Render's filesystem is ephemeral — uploaded files are lost on redeploy or restart. Artwork images must be stored externally. This template supports Supabase Storage via its S3-compatible API.

### Setup Steps

1. **Create a Supabase project** at [supabase.com](https://supabase.com).

2. **Create a Storage bucket**
   - Go to Storage → New bucket
   - Name: `media` (recommended)
   - Set as **public** for storefront product images (simplest)

3. **Generate S3 credentials**
   - Go to Project Settings → Storage → S3 access
   - Enable S3 Access and copy the credentials

4. **Copy the S3 endpoint and region**
   - Endpoint format: `https://<project-ref>.supabase.co/storage/v1/s3`
   - Region is usually shown in the Supabase dashboard (e.g. `us-east-1`)

5. **Set environment variables in Render**
   - Dashboard → Your Service → Environment
   - Add these variables:

   | Variable | Value | Required |
   |----------|-------|----------|
   | `SUPABASE_STORAGE_BUCKET` | `media` | Yes |
   | `SUPABASE_S3_ENDPOINT` | `https://<project-ref>.supabase.co/storage/v1/s3` | Yes |
   | `SUPABASE_S3_REGION` | `us-east-1` (or your region) | Yes |
   | `SUPABASE_S3_ACCESS_KEY_ID` | (from Supabase S3 settings) | Yes |
   | `SUPABASE_S3_SECRET_ACCESS_KEY` | (from Supabase S3 settings) | Yes |
   | `SUPABASE_STORAGE_PUBLIC_BASE_URL` | `https://<project-ref>.supabase.co/storage/v1/object/public/media` | Yes (for public bucket) |

6. **Redeploy** the service after setting env vars.

### Public vs Private Bucket

- **Public bucket (recommended):** Product images are publicly accessible. Set `SUPABASE_STORAGE_PUBLIC_BASE_URL` so the app generates correct image URLs. No signed URLs needed.
- **Private bucket:** Set `MEDIA_PRIVATE=true`. The app uses signed URLs. Requires additional configuration for display; advanced use case.

### Security Note

S3 keys are powerful. Store them only as **server-side environment variables** in Render. Never put these keys in frontend code or commit them to the repository.

---

## Storage validation

Run this to verify Supabase storage connectivity (with env vars set):

```bash
python manage.py check_storage
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Images 404 after upload | `SUPABASE_STORAGE_PUBLIC_BASE_URL` missing or wrong | Set it to `https://<project-ref>.supabase.co/storage/v1/object/public/media` (no trailing slash in value; app adds it) |
| "Missing region" or endpoint errors | `SUPABASE_S3_REGION` not set | Add `SUPABASE_S3_REGION=us-east-1` (or your Supabase region) |
| Bucket not found | Wrong bucket name | Ensure `SUPABASE_STORAGE_BUCKET` matches the bucket name exactly (e.g. `media`) |
| Permission denied / 403 | Keys incorrect or bucket policy | Regenerate S3 credentials in Supabase; ensure bucket exists and keys have write access |
| Images work locally but not on Render | Local uses filesystem; Render needs Supabase | All four required Supabase env vars must be set on Render |

---

## Other Render Configuration

- **Build command:** `pip install -r requirements.txt && npm install && npm run build:css`
- **Start command:** `gunicorn config.wsgi:application` (or your WSGI server)
- **Health check path:** `/` if applicable
- Ensure `DJANGO_ALLOWED_HOSTS` includes your Render URL
- Set `DJANGO_DEBUG=false` for production
