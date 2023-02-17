from django.db import models

# Create your models here.
from django.urls import reverse

from accounts.models import Account
from artist.models import Artist
from genre.models import Genre
from medium.models import Medium


class Artwork(models.Model):
    artwork_title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, unique=True)
    artist_name = models.ForeignKey(Artist, on_delete=models.CASCADE)
    medium_title = models.ForeignKey(Medium, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    is_verified = models.BooleanField(default=True)
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/artworks', blank=False)

    def get_url(self):
        return reverse('artwork_detail', args=[self.genre.slug, self.slug])

    def __str__(self):
        return str(self.artwork_title)

    def get_absolute_url(self):
        return reverse('artwork_detail', kwargs={'artwork_id': self.id})

    def user_liked_artwork(self, user):
        try:
            user_liked_artwork = UserLikedArtwork.objects.get(user=user, artwork=self)
            return user_liked_artwork
        except UserLikedArtwork.DoesNotExist:
            return None


class ArtworkComment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]


class UserLikedArtwork(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.user) + str(self.artwork))
