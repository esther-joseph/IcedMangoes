# Migration for ArtworkImage (multiple images per artwork)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_artwork_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtworkImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="artworks/")),
                ("order", models.PositiveIntegerField(default=0, help_text="Display order")),
                ("artwork", models.ForeignKey(on_delete=models.CASCADE, to="store.artwork")),
            ],
            options={"ordering": ["order", "id"]},
        ),
    ]
