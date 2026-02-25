"""Custom storage backend for Supabase S3-compatible storage with public URLs."""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class SupabaseS3Storage(S3Boto3Storage):
    """
    S3-compatible storage for Supabase.
    Overrides url() to return public object URLs when using a public bucket,
    since Supabase public URLs use /object/public/<bucket>/ path structure.
    """

    def url(self, name):
        if getattr(settings, "AWS_QUERYSTRING_AUTH", True):
            return super().url(name)
        public_base = getattr(settings, "SUPABASE_STORAGE_PUBLIC_BASE_URL", None)
        if not public_base:
            endpoint = getattr(settings, "AWS_S3_ENDPOINT_URL", "") or ""
            bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "") or ""
            if endpoint and bucket:
                base = endpoint.rstrip("/").rsplit("/", 1)[0] + f"/object/public/{bucket}/"
                public_base = base
        if public_base:
            return public_base.rstrip("/") + "/" + name
        return super().url(name)
