from djongo import models

class Artist(models.Model):
    name = models.CharField(max_length=100)

class Artwork(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='artworks/')
    available = models.BooleanField(default=True)
