"""Management command to validate Supabase storage configuration."""
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Validate Supabase storage configuration. Run with Supabase env vars set."

    def handle(self, *args, **options):
        storage_class = getattr(settings, "DEFAULT_FILE_STORAGE", "")
        if "s3boto3" not in storage_class and "SupabaseS3" not in storage_class:
            self.stdout.write(
                self.style.WARNING(
                    "Supabase storage not configured. Set SUPABASE_STORAGE_BUCKET, "
                    "SUPABASE_S3_ENDPOINT, SUPABASE_S3_ACCESS_KEY_ID, SUPABASE_S3_SECRET_ACCESS_KEY."
                )
            )
            self.stdout.write("Using local filesystem for media.")
            return

        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")
        try:
            from django.core.files.storage import default_storage
            client = default_storage.connection.meta.client
            client.head_bucket(Bucket=bucket)
            self.stdout.write(self.style.SUCCESS(f"Storage OK: bucket '{bucket}' accessible."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Storage check failed: {e}"))
