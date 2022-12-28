from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, max_length=500)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.artist_name