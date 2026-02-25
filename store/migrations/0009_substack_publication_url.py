# Migration: Add Substack publication URL to SiteSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0008_artworkimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="substack_publication_url",
            field=models.CharField(
                blank=True,
                max_length=255,
                help_text="Substack publication URL (e.g. https://yourname.substack.com) for blog feed",
            ),
        ),
    ]
