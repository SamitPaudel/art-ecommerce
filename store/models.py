from django.db import models

# Create your models here.
from artist.models import Artist
from genre.models import Genre
from medium.models import Medium


class Artwork(models.Model):
    artwork_title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, unique=True)
    artist_name = models.ForeignKey(Artist, on_delete=models.CASCADE)
    medium_title = models.ForeignKey(Medium, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    is_verified = models.BooleanField(default=True)
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/artworks', blank=False)

    def __str__(self):
        return self.artwork_title
