# Migration for ArtworkProduct (product form options)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_order_status_fulfillment"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtworkProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("artwork", models.ForeignKey(on_delete=models.CASCADE, to="store.artwork")),
            ],
            options={"ordering": ["id"]},
        ),
    ]
