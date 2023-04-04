import threading
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from accounts.models import Account
from art_ecommerce import settings
from artist.models import Artist
from genre.models import Genre
from medium.models import Medium

tz = timezone.get_current_timezone()


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
    isAvailable = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)

    def get_url(self):
        return reverse('artwork_detail', args=[self.genre.slug, self.slug])

    def __str__(self):
        return str(self.artwork_title)

    def get_absolute_url(self):
        return reverse('artwork_detail', kwargs={'artwork_id': self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.artwork_title)
        super(Artwork, self).save(*args, **kwargs)

    def user_liked_artwork(self, user):
        try:
            user_liked_artwork = UserLikedArtwork.objects.get(user=user.user, artwork=self)
            return user_liked_artwork
        except UserLikedArtwork.DoesNotExist:
            return None

    @property
    def is_auction_active(self):
        try:
            auction = Auction.objects.filter(artwork=self, is_active=True).latest('start_time')
            return True
        except Auction.DoesNotExist:
            return False

    @property
    def auction(self):
        try:
            auction = Auction.objects.filter(artwork=self, is_active=True).latest('start_time')
            return auction
        except Auction.DoesNotExist:
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


class Auction(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    starting_price = models.IntegerField(default=0)
    bid = models.ForeignKey('Bid', null=True, blank=True, on_delete=models.SET_NULL, related_name='auction_bid')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Auction for {self.artwork.artwork_title}'

    def get_bids(self):
        return self.bids.all().order_by('-bid_time')

    def save(self, *args, **kwargs):
        if not self.starting_price:
            self.starting_price = self.artwork.price

        # Set end_time
        if not self.end_time:
            self.end_time = timezone.localtime(self.start_time) + timedelta(hours=1)
        elif self.bid:
            self.end_time = timezone.localtime(self.bid.bid_time) + timedelta(minutes=15)

        super().save(*args, **kwargs)

    def end_auction(self):
        if timezone.now() >= self.end_time:
            highest_bid = self.get_bids().first()
            if highest_bid:
                self.artwork.isAvailable = False
                self.is_active = False
                self.bid = highest_bid
                self.save()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bid_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user} bid {self.amount} on {self.auction}'

    class Meta:
        ordering = ['-bid_time']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.auction:
            # Update end_time of auction if bid is higher than previous bid
            if self.amount > self.auction.starting_price:
                new_end_time = self.bid_time + timedelta(minutes=15)
                if not self.auction.end_time or new_end_time > self.auction.end_time:
                    self.auction.end_time = new_end_time
                    self.auction.save()
