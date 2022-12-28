from django.db import models

# Create your models here.
from django.urls import reverse


class Medium(models.Model):
    medium_title = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, max_length=500)
    description = models.TextField(max_length=1000, blank=True)

    def get_url(self):
        return reverse('artwork_by_mediums', args=[self.slug])

    def __str__(self):
        return self.medium_title